import os
from google import genai

# -----------------------------------
# 1. Get Gemini API Key
# -----------------------------------

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY is not set.")
    print("Please set your API key in the VS Code terminal.")
    exit()

# Create Gemini client
client = genai.Client(api_key=api_key)


# -----------------------------------
# 2. UV System Instruction
# -----------------------------------

system_prompt = """
You are "UV", a friendly and helpful AI personal assistant.

Your goal is to help the user with:
- Everyday tasks
- Planning
- Learning
- Answering questions
- General assistance

Keep your answers concise, clear, and structured.
Use bullet points when helpful.
"""


# -----------------------------------
# 3. Ask UV
# -----------------------------------

def ask_assistant(user_message):

    interaction = client.interactions.create(
        model="gemini-3.6-flash",
        input=user_message,
        system_instruction=system_prompt
    )

    return interaction.output_text


# -----------------------------------
# 4. Chat Loop
# -----------------------------------

print("--- UV: Your AI Personal Assistant ---")
print("Type 'exit' or 'quit' to end the conversation.\n")

while True:

    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("\nUV: Goodbye! Have a great day!")
        break

    if user_input.strip() == "":
        continue

    try:
        assistant_response = ask_assistant(user_input)

        print(f"\nUV: {assistant_response}\n")
        print("-" * 40)

    except Exception as e:
        print("\nError communicating with Gemini:")
        print(e)