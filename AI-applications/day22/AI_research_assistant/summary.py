from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

print("Loading summarization model...")

model_name = "sshleifer/distilbart-cnn-12-6"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

with open("research.txt", "r", encoding="utf-8") as file:
    research_text = file.read()

inputs = tokenizer(
    research_text,
    return_tensors="pt",
    max_length=1024,
    truncation=True
)

summary_ids = model.generate(
    inputs["input_ids"],
    max_length=60,
    min_length=25,
    num_beams=4,
    early_stopping=True
)

summary = tokenizer.decode(
    summary_ids[0],
    skip_special_tokens=True
)

print("\n--- GENERATED RESEARCH SUMMARY ---")
print(summary)