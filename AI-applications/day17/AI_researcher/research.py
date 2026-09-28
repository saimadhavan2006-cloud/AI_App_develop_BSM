from google import genai
from google.genai import types
import numpy as np
from dotenv import load_dotenv
import os
from pathlib import Path
import time

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found.")
    print("Please check your .env file.")
    exit()

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.8-flash"



BASE_DIR = Path(__file__).resolve().parent
ramayana_file = BASE_DIR / "ramayana.txt"

with open(ramayana_file, "r", encoding="utf-8") as file:
    ramayana_text = file.read()

chat = client.chats.create(
    model=MODEL
)

print("My MAHARSHI AI")
print("Welcome to Maharshi AI, your personal AI researcher!")
print("Ask anything")
print("Type 'exit' to end the conversation.")
while True:
    question = input("You: ")
    if question.lower() == 'exit':
        print("MAHARSHI AI: Goodbye!")
        break
    prompt=f"""
You are my personal AI researcher. 
Use the information about Ramayana below to answer the user's questions.
If something is not mentioned in the information, you can say "I don't know" or "I don't have that information".
Do not make up any information.
My information: {ramayana_text}
My questions: {question}
"""
    for attempt in range(3):
        try:
            response = chat.send_message(prompt)
            print("\nMAHARSHI AI:", response.text)
            break

        except Exception as e:
            if "503" in str(e):
                wait_time = 5 * (attempt + 1)
                print(f"\nGemini is busy. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print("\nGemini API Error:", e)
                break