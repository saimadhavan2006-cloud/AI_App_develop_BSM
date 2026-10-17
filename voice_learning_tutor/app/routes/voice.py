from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import SessionLocal
from app.models import LearningHistory
from app.services.llm_services import generate_explanation
import os
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.services.speech_service import (
    transcribe_audio,
    generate_speech,
)

router = APIRouter(prefix="/voice", tags=["Voice"])

AUDIO_DIR = "audio_outputs"
os.makedirs(AUDIO_DIR, exist_ok=True)


@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("audio/"):
        raise HTTPException(
            status_code=400,
            detail="Please upload an audio file."
        )

    suffix = os.path.splitext(file.filename or "recording.wav")[1]
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp:
            temp_path = temp.name
            content = await file.read()
            temp.write(content)

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded audio file is empty."
            )

        text = transcribe_audio(temp_path)

        if not text:
            raise HTTPException(
                status_code=422,
                detail="No speech was detected. Please try again."
            )

        return {"transcribed_text": text}

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Audio transcription failed: {exc}"
        )
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@router.post("/speak")
async def speak(text: str):
    if not text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty."
        )

    output_path = os.path.join(AUDIO_DIR, "tutor_response.mp3")

    try:
        await generate_speech(text, output_path)
        return FileResponse(
            output_path,
            media_type="audio/mpeg",
            filename="tutor_response.mp3"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Speech generation failed: {exc}"
        )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/ask")
async def voice_ask(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    import httpx

    temp_path = None

    try:
        if not file.content_type or not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=400,
                detail="Please upload an audio file."
            )

        suffix = os.path.splitext(file.filename or "recording.wav")[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp:
            temp_path = temp.name
            content = await file.read()
            temp.write(content)

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded audio file is empty."
            )

        question = transcribe_audio(temp_path)

        if not question:
            raise HTTPException(
                status_code=422,
                detail="No speech was detected."
            )

        answer = await generate_explanation(question)
        

        record = LearningHistory(
            question=question,
            answer=answer,
            level="beginner",
            language="English"
        )

        db.add(record)
        db.commit()
        db.refresh(record)
        audio_path = os.path.join(
            AUDIO_DIR,
            f"answer_{record.id}.mp3"
        )

        await generate_speech(answer, audio_path)

        return {
            "question": question,
            "answer": answer,
            "saved_id": record.id,
            "audio_url": f"/voice/audio/{record.id}",
            "message": "Answer generated, saved, and converted to speech."
        }

    except HTTPException:
        raise
    except httpx.ConnectError:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Ollama is unavailable. Check that it is running."
        )
    except httpx.TimeoutException:
        db.rollback()
        raise HTTPException(
            status_code=504,
            detail="Ollama took too long to respond."
        )
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Voice tutor failed: {exc}"
        )
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)  

@router.get("/audio/{record_id}")
async def get_audio(record_id: int):
    audio_path = os.path.join(
        AUDIO_DIR,
        f"answer_{record_id}.mp3"
    )

    if not os.path.exists(audio_path):
        raise HTTPException(
            status_code=404,
            detail="Audio file not found."
        )

    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        filename=f"answer_{record_id}.mp3"
    )