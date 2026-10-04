from gtts import gTTS

text = "Welcome to Day 20 of AI Training. Today we learn Speech AI!"

tts = gTTS(text=text, lang="en")
tts.save("welcome.mp3")

print("Speech generated successfully!")
print("Saved as welcome.mp3")