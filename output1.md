Beginner's Guide to Building an AI Content Creator

A comprehensive study guide & step-by-step tutorial for Google Colab & Hugging Face

100% Free & Open Source

No Paid API Keys

Python & AI Pipeline

1. Essential Core Concepts Explained

This guide explains the underlying principles of modern open-source Generative AI applications so you can confidently
complete the practical challenge.

1. Google Colab (Colaboratory)

Google Colab is a free cloud notebook environment from Google that runs Python in your browser. You do not need to
install Python or expensive software locally. It provides free compute RAM and optional access to GPUs.

2. Open-Source Models vs. Paid APIs

Unlike proprietary APIs (such as OpenAI's GPT-4) which charge per request and require credit cards, Open-Source
models hosted on Hugging Face are completely free to download, run, and customize.

3. SmolLM2-360M-Instruct Model

We use  HuggingFaceTB/SmolLM2-360M-Instruct :

•

360M: Has 360 million parameters. Compact enough to run fast on basic Colab CPUs.

•

Instruct: Fine-tuned specifically to listen to instructions, follow templates, and answer user queries.

4. Transformers Library & Pipeline

Hugging Face's  transformers  library enables easy loading of open-source models. The  pipeline("text-
generation")  wrapper handles complex tokenization and model inference automatically.

5. Hyperparameters (Generation Controls)

•

max_new_tokens : Upper limit on how many words/tokens the model generates (e.g., 300).

•

do_sample = True : Enables creative word sampling instead of picking the exact same words every time.

•

temperature : Controls creativity/randomness (0.2 = strict/factual; 0.7 = balanced/creative).

•

return_full_text = False : Removes the original prompt from the output result.

2. System Data Flow

Step

Component

Action / Explanation

1

2

3

4

5

User Input

User enters Subject, Platform (Instagram/LinkedIn), Tone, and Language.

Prompt Template

Python combines user inputs into a structured system prompt.

Inference

Hugging Face model processes input tokens and generates response.

Content Output

Formatted output containing Title, Hook, Caption, Script, Hashtags & CTA.

Save File

Program writes the result into a local  .txt  file in Colab.

AI Content Creator - Beginner Guide & Student Activity

Page 1 of 3

3. Step-by-Step Code Walkthrough

Step 1 & 2: Install Required Libraries

In Google Colab, open a new notebook and run:

!pip -q install -U transformers accelerate sentencepiece

Step 3: Load the Open-Source Model

from transformers import pipeline

model_name = "HuggingFaceTB/SmolLM2-360M-Instruct"
generator = pipeline("text-generation", model=model_name)
print("Model loaded successfully!")

Step 4: Create Content Generation Function

def create_content(topic, platform, tone, language):
    prompt = (
        f"You are a social media content creator.\n"
        f"Create content in {language}.\n"
        f"Topic: {topic}\n"
        f"Platform: {platform}\n"
        f"Tone: {tone}\n"
        f"Give me:\n"
        f"1. Catchy title\n"
        f"2. Strong hook\n"
        f"3. Short caption\n"
        f"4. 30-second video script\n"
        f"5. 5 hashtags\n"
        f"6. Call to action\n"
        f"Keep it clear, useful and engaging."
    )

    result = generator(
        prompt,
        max_new_tokens=300,
        do_sample=True,
        temperature=0.7,
        return_full_text=False
    )
    return result[0]["generated_text"]

Step 5 & 6: Interactive Inputs & Testing

topic = input("Enter topic: ")
platform = input("Enter platform: ")
tone = input("Enter tone: ")
language = input("Enter language: ")

content = create_content(topic, platform, tone, language)
print("\n===== YOUR AI CONTENT =====\n")
print(content)

Step 7: Save to Text File

with open("ai_content.txt", "w", encoding="utf-8") as f:
    f.write(content)

print("Saved as ai_content.txt! Download it from Colab's Files panel.")

AI Content Creator - Beginner Guide & Student Activity

Page 2 of 3

Step 8: Generate Multiple Ideas

prompt = f"Create 5 different social media post ideas about {topic}."
result = generator(prompt, max_new_tokens=500, do_sample=True, temperature=0.8, return_full_text=False)
print(result[0]["generated_text"])

4. Troubleshooting Common Errors

Important Fixes:

•

Model is Slow: Free CPU takes 15-30 seconds. Switch to GPU in Colab via  Runtime → Change runtime type → T4 GPU .

•

Out of Memory Error: Go to  Runtime → Restart session  to clear memory.

•

Bad or Repetitive Output: Adjust temperature (between 0.6 - 0.8) or make the prompt more specific.

•

Colab Disconnected: Re-run library installation and model loading steps.

5. Product Evolution Stages

Stage

Feature Goal

Technology Used

1 & 2

Input variables & complete post package

Python, Transformers

3

4

5

6

7

File Download

Web User Interface

AI Image Generation

Text-To-Speech & Captions

Content Calendar

Python File I/O (TXT/CSV)

Gradio / Streamlit

Diffusers (Stable Diffusion)

gTTS, OpenAI Whisper

Pandas & Scheduler

🎯 Student Project Challenge: "AI Student Content Creator"

Goal: Complete this activity to demonstrate your understanding of open-source AI.

Instructions Checklist:

[ ]

Create a new Google Colab Notebook.

[ ]

Install  transformers ,  accelerate , and  sentencepiece .

[ ]

Load  HuggingFaceTB/SmolLM2-360M-Instruct  model using  pipeline .

[ ]

Write input statements for Subject (e.g. "Machine Learning"), Platform (e.g. "Instagram"), Language (e.g. "Hindi/
English/Telugu"), and Tone.

[ ]

Pass these parameters into the  create_content()  function.

[ ]

Save the complete generated output package to a file named  student_ai_content.txt .

[ ]

Locate and download  student_ai_content.txt  from Colab's left file manager pane.

AI Content Creator - Beginner Guide & Student Activity

Page 3 of 3

