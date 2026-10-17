from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class LearningHistory(Base):
    __tablename__ = "learning_history"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    level = Column(String(30), nullable=False)
    language = Column(String(40), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
