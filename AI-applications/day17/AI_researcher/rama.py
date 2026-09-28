from google import genai
from google.genai import types
import numpy as np
from dotenv import load_dotenv
import os
from pathlib import Path


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found.")
    print("Please check your .env file.")
    exit()

client = genai.Client(api_key=api_key)

MODEL = "gemini-3.8-flash"

BASE_DIR = Path(__file__).resolve().parent
ramayana_file = BASE_DIR / "raamayana.txt"

with open(ramayana_file, "r", encoding="utf-8") as file:
    ramayana_text = file.read()
print("Ramayana file loaded successfully")
print("CHaracters",len(ramayana_text))

def create_chunks(text,chunk_size=1000):
    chunks=[]
    for i in range(0,len(text),chunk_size):
        chunk=text[i:i + chunk_size]
        chunks.append(chunk)
    return chunks
chunks=create_chunks(ramayana_text)
print("Number of chuns: ",len(chunks))

def create_embeds(text):
    result=client.models.embed_content(
        model="gemini-embedding-001",
        contents=text,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT")
    )
    return np.array(result.embeddings[0].values)
print("\n Creating embeddings...")
document_embeddings=[]
for chunk in chunks:
    embedding=create_embeds(chunk)
    document_embeddings.append(embedding)
print("Embeddings created successfully")

def cosine_similarity(a,b):
    return np.dot(a,b)/(np.linalg.norm(a)**np.linalg.norm(b))

def retrive_context(question,top_n=3):
    result=client.models.embed_content(
            model="gemini-embedding-001",
            contents=question,
            config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
        )
    question_embedding=np.array(result.embeddings[0].values)
    scores=[]
    for i,document_embedding in enumerate(document_embeddings):
        score=cosine_similarity(question_embedding,document_embedding)
        scores.append((score,i))
        scores.sort(reverse=True)
        selected_chuns=[]
        for score,index in scores[:top_n]:
            selected_chuns.append(chunks[index])
        return "\n\n".join(selected_chuns)
import time

def ramayana_question_adagandi(question):
    context = retrive_context(question)

    prompt = f"""
You are a Ramayana assistant. Answer the user's question using ONLY the information
provided in the context.

If the answer cannot be found in the context, say:
"I could not find that information in the provided Ramayana document."

Do not invent facts.

Context:
{context}

======

Question:
{question}

Answer clearly and simply.
"""

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )
            return response.text

        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                print(f"Gemini is busy. Retrying... ({attempt + 1}/3)")
                time.sleep(5)
            else:
                raise

    return "Gemini is temporarily unavailable. Please try again in a moment."

print("\n=========================")
print("   RAMAYANA AI ASSISTANT   ")
print("Asq questiosn about Ramayana")
print("Type 'exit' to stop")
while True:
    question=input("\nYou: ")
    if question.lower()=="exit":
        print("Assistant: Goodbye")
        break
    answer=ramayana_question_adagandi(question)
    print("\nAssistant:")
    print(answer)