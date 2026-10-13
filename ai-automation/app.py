from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, StringConstraints
from transformers import pipeline

from database import (
    initialize_database,
    save_sentiment,
    get_sentiment_history,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="AI Sentiment Automation",
    version="2.0.0",
    lifespan=lifespan,
)

Text = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=5000,
    ),
]


class SentimentRequest(BaseModel):
    text: Text


# Load the model once when the module is imported.
analyser = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english",
    framework="pt",
    device=-1,
)


@app.get("/")
def home():
    return {"message": "AI Sentiment Automation API is ready"}


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}


@app.post("/analyse")
def analyse_sentiment(request: SentimentRequest):
    try:
        prediction = analyser(
            request.text,
            truncation=True,
            max_length=512,
        )[0]

        sentiment = prediction["label"]
        confidence = float(prediction["score"])

        if sentiment == "NEGATIVE":
            action = "Flag for customer support review"
        else:
            action = "Record as positive feedback"

        record_id = save_sentiment(
            request.text,
            sentiment,
            confidence,
            action,
        )

        return {
            "id": record_id,
            "text": request.text,
            "sentiment": sentiment,
            "confidence": round(confidence, 4),
            "suggested_action": action,
            "saved_to_database": True,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Sentiment analysis or database storage failed.",
        ) from exc


@app.get("/history")
def sentiment_history(
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
):
    try:
        records = get_sentiment_history(limit)
        return {
            "count": len(records),
            "records": records,
        }
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve sentiment history.",
        ) from exc