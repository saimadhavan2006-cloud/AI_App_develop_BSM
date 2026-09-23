import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# -----------------------------------
# 1. Load API key from .env
# -----------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found.")
    print("Please check your .env file.")
    exit()

# Create Gemini client
client = genai.Client(api_key=api_key)


# -----------------------------------
# 2. Assistant personality
# -----------------------------------

system_prompt = """
You are UV, a friendly and helpful AI personal assistant.

Your goal is to help the user with:
- Everyday tasks
- Planning
- Learning
- General questions
- Programming
- Study assistance

Keep your answers clear, concise and structured.
"""


# -----------------------------------
# 3. Ask Gemini
# -----------------------------------

def ask_assistant(user_message):

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7
        )
    )

    return response.text


# -----------------------------------
# 4. Start the assistant
# -----------------------------------

print("=" * 50)
print("       UV - AI PERSONAL ASSISTANT")
print("=" * 50)

print("Type 'exit' or 'quit' to close the assistant.")
print()


# -----------------------------------
# 5. Chat loop
# -----------------------------------

while True:

    user_input = input("You: ")

    # Exit command
    if user_input.lower() in ["exit", "quit"]:

        print("\nUV: Goodbye! Have a great day!")
        break

    # Ignore empty input
    if user_input.strip() == "":
        continue

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"{system_prompt}\n\nUser: {user_input}"
        )

        print("\nUV:", response.text)
        print("-" * 50)

    except Exception as e:
        print("\nGemini temporarily unavailable.")
        print("Please try again in a few seconds.")
        print("Error:", e)