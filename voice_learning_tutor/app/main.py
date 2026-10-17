from app.routes.history import router as history_router
from fastapi import FastAPI
from app.routes.voice import router as voice_router
from app.database import Base, engine
from app.models import LearningHistory
from app.routes.ask import router as ask_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Voice-Enabled Interactive Learning Tutor",
    description="An AI tutor that explains concepts through text and voice.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Voice Learning Tutor API is running!",
        "status": "ready"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


app.include_router(ask_router)
app.include_router(history_router)
app.include_router(voice_router)
