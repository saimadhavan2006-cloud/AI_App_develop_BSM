from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import LearningHistory

router = APIRouter(prefix="/history", tags=["Learning History"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
def get_history(db: Session = Depends(get_db)):
    records = (
        db.query(LearningHistory)
        .order_by(LearningHistory.id.desc())
        .all()
    )

    return [
        {
            "id": record.id,
            "question": record.question,
            "answer": record.answer,
            "level": record.level,
            "language": record.language,
            "created_at": record.created_at.isoformat()
            if record.created_at else None
        }
        for record in records
    ]
