import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from cal import calculate
from time_utils import get_current_time, get_current_date, get_current_datetime
from voice_input import listen
from voice_output import speak
from weather import get_weather
from web_search import web_search

# ==========================================
# 1. LOAD API KEY
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found.")
    print("Please check your .env file.")
    exit()


# ==========================================
# 2. CREATE GEMINI CLIENT
# ==========================================

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.8-flash"


# ==========================================
# 3. UV PERSONALITY
# ==========================================

system_prompt = """
You are UV, a friendly and helpful AI personal assistant.

Your responsibilities include:

- Answering general questions
- Helping with studies
- Helping with programming
- Explaining technical concepts
- Helping with planning
- Performing simple calculations
- Providing date and time information
- Helping with everyday tasks

Keep your answers clear, concise and structured.

You should behave like a personal assistant called UV.
"""


# ==========================================
# 4. CREATE CHAT
# ==========================================

chat = client.chats.create(
    model=MODEL,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt
    )
)


# ==========================================
# 5. ASK UV
# ==========================================

def ask_assistant(user_message):

    try:

        response = chat.send_message(user_message)

        return response.text

    except Exception as e:

        return f"Gemini error: {e}"

def ask_web_assistant(query):
    search_results = web_search(query)

    prompt = f"""
Answer the user's question using the web search results below.

User question:
{query}

Web search results:
{search_results}

Rules:
- Give ONE concise answer.
- Do not list the search results.
- Do not mention that you are reading search results.
- Use simple language.
- If the information is uncertain or conflicting, say so.
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        return f"Sorry, I couldn't generate an answer from the web search. {e}"    

def handle_local_command(user_input):

    text = user_input.lower().strip()

    # -------------------------
    # TIME
    # -------------------------

    if "what time" in text or "current time" in text:
        return f"The current time is {get_current_time()}."

    # -------------------------
    # DATE
    # -------------------------

    if "today's date" in text or "todays date" in text:
        return f"Today's date is {get_current_date()}."

    if text == "date":
        return f"Today's date is {get_current_date()}."

    # -------------------------
    # DATE + TIME
    # -------------------------

    if "date and time" in text:
        return f"It is {get_current_datetime()}."

    # -------------------------
    # CALCULATOR
    # -------------------------

    if text.startswith("calculate "):

        expression = user_input[10:].strip()

        result = calculate(expression)

        if result is not None:
            return f"The answer is {result}."

        return "Sorry, I could not calculate that."

    if "weather" in text:
        city = user_input.lower()

        keywords = [
           "weather in ",
            "weather at ",
            "weather for "
        ]

        for keyword in keywords:
            if keyword in city:
                city = city.split(keyword, 1)[1].strip()
                return get_weather(city)

        return "Please tell me the city. For example: weather in Hyderabad."

    if text.startswith("search "):
        query = user_input[7:].strip()

        if not query:
            return "Please tell me what you want me to search for."

        return ask_web_assistant(query)
    return None

# ==========================================
# 6. START UV
# ==========================================

print("=" * 55)
print("              UV - AI PERSONAL ASSISTANT")
print("=" * 55)

print("UV is ready!")
print("Type 'exit' or 'quit' to close.")
print()


# ==========================================
# 7. CHAT LOOP
# ==========================================

while True:
    print("\nChoose input mode:")
    print("1. Text")
    print("2. Voice")
    print("3. Exit")

    choice = input("Enter choice: ").strip()

    if choice == "3":
        print("UV: Goodbye! Have a great day!")
        break

    if choice == "1":
        user_input = input("\nYou: ")

    elif choice == "2":
        user_input = listen()

    else:
        print("Please choose 1, 2, or 3.")
        continue

    if not user_input:
        continue

    if user_input.lower().strip() in ["exit", "quit"]:
        if choice == "2":
            speak("Goodbye! Have a great day!")
        else:
            print("UV: Goodbye! Have a great day!")
        break

    local_response = handle_local_command(user_input)

    if local_response is not None:
        print("\nUV:", local_response)

        # Speak ONLY in Voice mode
        if choice == "2":
            speak(local_response)

        print("-" * 55)
        continue

    response = ask_assistant(user_input)

    print("\nUV:", response)

    # Speak ONLY in Voice mode
    if choice == "2":
        speak(response)

    print("-" * 55)