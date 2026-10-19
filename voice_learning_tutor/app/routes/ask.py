

from tracemalloc import start

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from sqlalchemy.orm import Session
import time

from app.database import SessionLocal
from app.models import LearningHistory
from app.services.llm_services import generate_explanation_result

from app.services.rag_service import retrieve_passages
router = APIRouter(prefix="/ask", tags=["Tutor"])


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    language: str = Field(default="English", min_length=1, max_length=40)
    depth: Literal["short", "medium", "detailed"] = "medium"



class CitationSource(BaseModel):
    label: str
    textbook: str
    page: int
    chunk: int
    chunks: list[int] = Field(default_factory=list)
    text: str
    distance: float



class AskResponse(BaseModel):
    question: str
    answer: str
    model: str
    saved_id: int
    sources: list[CitationSource]
    accuracy_warnings: list[str] = Field(default_factory=list)
    retry_count: int = 0



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
        start = time.perf_counter()
        print("Starting RAG retrieval...")
        context, sources = retrieve_passages(
            request.question,
            top_k=6
        )
        print(f"RAG retrieval took {time.perf_counter() - start:.2f}s")
        print("\n========== FASTAPI RETRIEVAL DEBUG ==========")
        print("Question:", request.question)
        print("Sources returned:", len(sources))

        for source in sources:
            print(
                source.get("textbook"),
                "page:", source.get("page"),
                "chunk:", source.get("chunk"),
                "distance:", source.get("distance"),
            )

        print("=============================================")

        print("\n========== RETRIEVED TEXTBOOK PASSAGES ==========")
        print(context)
        print("=================================================\n")
        start = time.perf_counter()
        print("Starting LLM generation...")

        result = await generate_explanation_result(
            question=request.question,
            level=request.level,
            language=request.language,
            depth=request.depth,
            context=context,
        )
        answer = result.answer

        print(f"LLM generation took {time.perf_counter() - start:.2f}s")

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
            sources=sources,
            accuracy_warnings=result.warnings,
            retry_count=result.retry_count,
        )

    except httpx.ConnectError:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Ollama is unavailable. Check that Ollama is running."
        )
    except httpx.TimeoutException as exc:
        db.rollback()
        print(f"LLM/Ollama timeout: {type(exc).__name__}: {exc}")
        raise HTTPException(
            status_code=504,
            detail="Ollama took too long to respond."
        ) from exc
    except httpx.HTTPStatusError:
        db.rollback()
        raise HTTPException(
            status_code=502,
            detail="Ollama returned an error."
        )
    except Exception:
        db.rollback()
        raise
