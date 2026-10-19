
import os
import tempfile
import uuid
from pathlib import Path

import httpx
from fastapi import (APIRouter, Depends, File, HTTPException, UploadFile, Form)
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask

from app.database import SessionLocal
from app.models import LearningHistory
from app.services.llm_services import generate_explanation
from app.services.speech_service import generate_speech, transcribe_audio


router = APIRouter(prefix="/voice", tags=["Voice"])

AUDIO_DIR = Path("audio_outputs")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

MAX_AUDIO_SIZE = 5 * 1024 * 1024  # 5 MB


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def save_audio_upload(file: UploadFile) -> str:
    """Validate and save an audio upload with a 5 MB size limit."""
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an audio file.",
        )

    suffix = Path(file.filename or "recording.wav").suffix or ".wav"
    temp_path = None
    total_size = 0

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            delete=False,
            suffix=suffix,
        ) as temp:
            temp_path = temp.name

            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break

                total_size += len(chunk)

                if total_size > MAX_AUDIO_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="Audio file exceeds the 5 MB limit.",
                    )

                temp.write(chunk)

        if total_size == 0:
            raise HTTPException(
                status_code=400,
                detail="The uploaded audio file is empty.",
            )

        return temp_path

    except Exception:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
        raise

    finally:
        await file.close()


def remove_file(path: str) -> None:
    """Remove a file if it exists."""
    try:
        if os.path.exists(path):
            os.remove(path)
    except OSError:
        pass


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    temp_path = None

    try:
        temp_path = await save_audio_upload(file)
        text = transcribe_audio(temp_path)

        if not text:
            raise HTTPException(
                status_code=422,
                detail="No speech was detected. Please try again.",
            )

        return {"transcribed_text": text}

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Audio transcription failed. Please try again.",
        )
    finally:
        if temp_path:
            remove_file(temp_path)


@router.post("/speak")
async def speak(text: str):
    if not text or not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty.",
        )

    filename = f"speech_{uuid.uuid4().hex}.mp3"
    output_path = str(AUDIO_DIR / filename)

    try:
        await generate_speech(text.strip(), output_path)

        return FileResponse(
            output_path,
            media_type="audio/mpeg",
            filename=filename,
            background=BackgroundTask(remove_file, output_path),
        )

    except Exception:
        remove_file(output_path)
        raise HTTPException(
            status_code=500,
            detail="Speech generation failed. Please try again.",
        )

@router.post("/ask")
async def voice_ask(
    file: UploadFile = File(...),
    level: str = Form("beginner"),
    language: str = Form("English"),
    depth: str = Form("medium"),
    db: Session = Depends(get_db),
):
    temp_path = None

    allowed_levels = {"beginner", "intermediate", "advanced"}
    allowed_languages = {"English", "Telugu", "Hindi"}
    allowed_depths = {"short", "medium", "detailed"}

    if level not in allowed_levels:
        raise HTTPException(status_code=422, detail="Invalid learning level.")

    if language not in allowed_languages:
        raise HTTPException(status_code=422, detail="Invalid answer language.")

    if depth not in allowed_depths:
        raise HTTPException(status_code=422, detail="Invalid explanation depth.")

    try:
        temp_path = await save_audio_upload(file)
        question = transcribe_audio(temp_path)

        if not question:
            raise HTTPException(
                status_code=422,
                detail="No speech was detected. Please try again.",
            )

        answer = await generate_explanation(
            question,
            level=level,
            language=language,
            depth=depth,
        )

        record = LearningHistory(
            question=question,
            answer=answer,
            level=level,
            language=language,
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        audio_path = str(AUDIO_DIR / f"answer_{record.id}.mp3")

        try:
            await generate_speech(answer, audio_path)
        except Exception:
            remove_file(audio_path)
            raise HTTPException(
                status_code=502,
                detail=(
                    "The answer was saved, but speech generation failed. "
                    "Please try again."
                ),
            )

        return {
            "question": question,
            "transcribed_text": question,
            "answer": answer,
            "saved_id": record.id,
            "level": level,
            "language": language,
            "depth": depth,
            "audio_url": f"/voice/audio/{record.id}",
            "message": "Answer generated, saved, and converted to speech.",
        }

    except HTTPException:
        db.rollback()
        raise
    except httpx.ConnectError:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Ollama is unavailable. Check that it is running.",
        )
    except httpx.TimeoutException:
        db.rollback()
        raise HTTPException(
            status_code=504,
            detail="Ollama took too long to respond.",
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Voice tutor failed. Please try again.",
        )
    finally:
        if temp_path:
            remove_file(temp_path)



@router.get("/audio/{record_id}")
async def get_audio(record_id: int):
    audio_path = AUDIO_DIR / f"answer_{record_id}.mp3"

    if not audio_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Audio file not found.",
        )

    return FileResponse(
        str(audio_path),
        media_type="audio/mpeg",
        filename=audio_path.name,
    )
