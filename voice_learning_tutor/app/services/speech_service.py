
from pathlib import Path
from threading import Lock

from faster_whisper import WhisperModel
import edge_tts


VOICE = "en-IN-PrabhatNeural"
WHISPER_MODEL_SIZE = "base"

TECHNICAL_PROMPT = (
    "Engineering lecture about electronics and computer architecture. "
    "Technical terms include 8051, 8086, microcontroller, microprocessor, "
    "registers, timers, counters, interrupts, UART, SPI, I2C, GPIO, "
    "ADC, DAC, embedded systems, Verilog, and digital logic design."
)

_whisper_model = None
_model_lock = Lock()


def get_whisper_model():
    global _whisper_model

    if _whisper_model is None:
        with _model_lock:
            if _whisper_model is None:
                _whisper_model = WhisperModel(
                    WHISPER_MODEL_SIZE,
                    device="cpu",
                    compute_type="int8",
                )

    return _whisper_model


def transcribe_audio(audio_path: str, language: str = None) -> str:
    model = get_whisper_model()

    segments, _ = model.transcribe(
        audio_path,
        language=language,
        task="transcribe",
        beam_size=5,
        vad_filter=True,
        condition_on_previous_text=False,
        initial_prompt=TECHNICAL_PROMPT,
    )

    text = " ".join(
        segment.text.strip()
        for segment in segments
        if segment.text.strip()
    )

    return text.strip()



import re


def prepare_text_for_speech(text: str) -> str:
    """Expand selected technical abbreviations for clearer speech."""
    replacements = {
        r"\bUART\b": "U A R T",
        r"\bGPIO\b": "G P I O",
        r"\bSPI\b": "S P I",
        r"\bI2C\b": "I two C",
        r"\bADC\b": "A D C",
        r"\bDAC\b": "D A C",
        r"\bRAM\b": "R A M",
        r"\bROM\b": "R O M",
        r"\bCPU\b": "C P U",
        r"\b8051\b": "eighty fifty one",
        r"\b8086\b": "eighty eighty six",
    }

    spoken_text = text

    for pattern, replacement in replacements.items():
        spoken_text = re.sub(
            pattern,
            replacement,
            spoken_text,
            flags=re.IGNORECASE,
        )

    return spoken_text


async def generate_speech(text: str, output_path: str) -> str:
    if not text or not text.strip():
        raise ValueError("Cannot generate speech from empty text.")

    from pathlib import Path
    import edge_tts

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    spoken_text = prepare_text_for_speech(text.strip())

    communicator = edge_tts.Communicate(
        text=spoken_text,
        voice=VOICE,
    )

    await communicator.save(str(path))
    return str(path)

