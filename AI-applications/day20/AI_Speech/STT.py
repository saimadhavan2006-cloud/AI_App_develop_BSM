import whisper

print("Loading Whisper model...")

model = whisper.load_model("base")

print("Transcribing welcome.mp3...")

result = model.transcribe("welcome.mp3", fp16=False)

print("\n--- TRANSCRIPTION RESULTS ---")
print("Detected Language:", result.get("language", "en").upper())
print("Full Text:", result["text"].strip())

print("\n--- TIMED SEGMENTS ---")

for seg in result["segments"]:
    print(
        f"[{seg['start']:.1f}s -> {seg['end']:.1f}s]: "
        f"{seg['text'].strip()}"
    )