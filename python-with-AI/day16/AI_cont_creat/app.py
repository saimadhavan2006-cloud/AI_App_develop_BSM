from transformers import pipeline

from content_generator import create_content, generate_ideas
from file_manager import save_content


# ==========================================
# LOAD AI MODEL
# ==========================================

model_name = "HuggingFaceTB/SmolLM2-360M-Instruct"

print("Loading AI model...")

generator = pipeline(
    "text-generation",
    model=model_name
)

print("Model loaded successfully!")


# ==========================================
# USER INPUT
# ==========================================

print("\n================================")
print("       AI CONTENT CREATOR")
print("================================\n")

topic = input("Enter topic: ")
platform = input("Enter platform: ")
tone = input("Enter tone: ")
language = input("Enter language: ")


# ==========================================
# GENERATE CONTENT
# ==========================================

print("\nGenerating content...\n")

content = create_content(
    generator,
    topic,
    platform,
    tone,
    language
)


# ==========================================
# DISPLAY CONTENT
# ==========================================

print("\n================================")
print("       GENERATED CONTENT")
print("================================\n")

print(content)


# ==========================================
# SAVE CONTENT
# ==========================================

file_path = save_content(
    content,
    "ai_content.txt"
)

print("\nContent saved successfully!")
print(f"File: {file_path}")


# ==========================================
# GENERATE 5 IDEAS
# ==========================================

choice = input(
    "\nDo you want 5 more content ideas? (yes/no): "
)

if choice.lower() == "yes":

    print("\nGenerating 5 content ideas...\n")

    ideas = generate_ideas(
        generator,
        topic
    )

    print("\n================================")
    print("       CONTENT IDEAS")
    print("================================\n")

    print(ideas)

    save_content(
        ideas,
        "content_ideas.txt"
    )

    print("\nIdeas saved to output/content_ideas.txt")