import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import LearningHistory
from app.services.llm_services import generate_explanation

router = APIRouter(prefix="/ask", tags=["Tutor"])


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    language: str = Field(default="English", min_length=1, max_length=40)
    depth: Literal["short", "medium", "detailed"] = "medium"


class AskResponse(BaseModel):
    question: str
    answer: str
    model: str
    saved_id: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=AskResponse)
async def ask_tutor(
    request: AskRequest,
    db: Session = Depends(get_db)
):
    try:
        answer = await generate_explanation(
            question=request.question,
            level=request.level,
            language=request.language,
            depth=request.depth,
        )

        record = LearningHistory(
            question=request.question,
            answer=answer,
            level=request.level,
            language=request.language,
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        return AskResponse(
            question=request.question,
            answer=answer,
            model="llama3.2:latest",
            saved_id=record.id,
        )

    except httpx.ConnectError:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Ollama is unavailable. Check that Ollama is running."
        )
    except httpx.TimeoutException:
        db.rollback()
        raise HTTPException(
            status_code=504,
            detail="Ollama took too long to respond."
        )
    except httpx.HTTPStatusError:
        db.rollback()
        raise HTTPException(
            status_code=502,
            detail="Ollama returned an error."
        )
    except Exception:
        db.rollback()
        raise
