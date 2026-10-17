import asyncio
from pathlib import Path

from faster_whisper import WhisperModel
import edge_tts


VOICE = "en-IN-PrabhatNeural"
WHISPER_MODEL_SIZE = "base"

_whisper_model = None


def get_whisper_model():
    global _whisper_model

    if _whisper_model is None:
        _whisper_model = WhisperModel(
            WHISPER_MODEL_SIZE,
            device="cpu",
            compute_type="int8"
        )

    return _whisper_model


def transcribe_audio(audio_path: str, language: str = None) -> str:
    model = get_whisper_model()

    segments, info = model.transcribe(
        audio_path,
        language=language,
        vad_filter=True
    )

    text = " ".join(segment.text.strip() for segment in segments)
    return text.strip()


async def generate_speech(text: str, output_path: str) -> str:
    if not text.strip():
        raise ValueError("Cannot generate speech from empty text.")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    communicator = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicator.save(str(path))
    return str(path)
