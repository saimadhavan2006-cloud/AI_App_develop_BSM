import pyttsx3

engine = pyttsx3.init()

# Speech settings
engine.setProperty("rate", 170)
engine.setProperty("volume", 1.0)


def speak(text):
    print("UV:", text)

    engine.say(text)
    engine.runAndWait()


if __name__ == "__main__":
    print("=" * 50)
    print("       UV VOICE OUTPUT TEST")
    print("=" * 50)

    speak("Hello! I am UV, your personal assistant.")
    speak("Voice output is working successfully.")