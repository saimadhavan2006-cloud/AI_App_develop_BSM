import sys
import os

# --------------------------------------------------
# PyAudioWPatch
# --------------------------------------------------
import pyaudiowpatch as pyaudio

# Make SpeechRecognition see PyAudioWPatch as "pyaudio"
sys.modules["pyaudio"] = pyaudio

# --------------------------------------------------
# SpeechRecognition
# --------------------------------------------------
import speech_recognition as sr
import speech_recognition.audio as sr_audio


# --------------------------------------------------
# Force SpeechRecognition to use its bundled FLAC
# --------------------------------------------------
FLAC_PATH = (
    r"C:\Users\saima\OneDrive\Documents\AI_App_development"
    r"\python-with-AI\day12\AI_Personal_Assistant"
    r"\venv\Lib\site-packages\speech_recognition"
    r"\flac-win32.exe"
)

if not os.path.exists(FLAC_PATH):
    print("ERROR: FLAC executable not found!")
    print(FLAC_PATH)
    sys.exit()

# Replace SpeechRecognition's automatic FLAC detection
sr_audio.get_flac_converter = lambda: FLAC_PATH


# --------------------------------------------------
# Voice input function
# --------------------------------------------------
def listen():
    recognizer = sr.Recognizer()

    try:
        print("\n🎤 Listening...")

        with sr.Microphone() as source:
            print("Adjusting for background noise...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            print("Speak now!")

            audio = recognizer.listen(source)

        print("🔄 Processing...")

        text = recognizer.recognize_google(audio)

        print("You:", text)

        return text

    except sr.UnknownValueError:
        print("UV: Sorry, I couldn't understand you.")
        return ""

    except sr.RequestError as e:
        print("UV: Speech recognition service error.")
        print(e)
        return ""

    except Exception as e:
        print("Microphone error:")
        print(e)
        return ""


# --------------------------------------------------
# Test
# --------------------------------------------------
if __name__ == "__main__":

    print("=" * 50)
    print("       UV VOICE INPUT TEST")
    print("=" * 50)

    text = listen()

    print("\nRecognized text:", text)

