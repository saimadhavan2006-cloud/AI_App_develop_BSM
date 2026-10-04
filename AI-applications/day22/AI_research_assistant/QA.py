from transformers import AutoTokenizer, AutoModelForQuestionAnswering
import torch

print("Loading Question Answering Model...")

model_name = "deepset/roberta-base-squad2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForQuestionAnswering.from_pretrained(model_name)

with open("research.txt", "r", encoding="utf-8") as file:
    research_text = file.read()

question = "What does AI detect faster than humans?"

inputs = tokenizer(
    question,
    research_text,
    return_tensors="pt",
    truncation=True,
    max_length=512
)

with torch.no_grad():
    outputs = model(**inputs)

start_index = torch.argmax(outputs.start_logits)
end_index = torch.argmax(outputs.end_logits)

answer_tokens = inputs["input_ids"][0][start_index:end_index + 1]

answer = tokenizer.decode(
    answer_tokens,
    skip_special_tokens=True
)

start_score = torch.softmax(outputs.start_logits, dim=1)[0][start_index]
end_score = torch.softmax(outputs.end_logits, dim=1)[0][end_index]

confidence = ((start_score + end_score) / 2).item()

print("\n--- QUESTION ANSWERING ---")
print("Question:", question)
print("Answer:", answer)
print("Confidence:", round(confidence, 4))