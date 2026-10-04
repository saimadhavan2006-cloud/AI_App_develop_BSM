from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import AutoModelForQuestionAnswering
import torch


class AIResearchAssistant:

    def __init__(self):
        print("Loading AI Research Assistant...")

        # Summarization model
        self.summary_name = "sshleifer/distilbart-cnn-12-6"
        self.summary_tokenizer = AutoTokenizer.from_pretrained(self.summary_name)
        self.summary_model = AutoModelForSeq2SeqLM.from_pretrained(self.summary_name)

        # Question Answering model
        self.qa_name = "deepset/roberta-base-squad2"
        self.qa_tokenizer = AutoTokenizer.from_pretrained(self.qa_name)
        self.qa_model = AutoModelForQuestionAnswering.from_pretrained(self.qa_name)

        print("Models loaded successfully!")


    def summarize(self, text):

        inputs = self.summary_tokenizer(
            text,
            return_tensors="pt",
            max_length=1024,
            truncation=True
        )

        summary_ids = self.summary_model.generate(
            inputs["input_ids"],
            max_length=60,
            min_length=25,
            num_beams=4,
            early_stopping=True
        )

        return self.summary_tokenizer.decode(
            summary_ids[0],
            skip_special_tokens=True
        )


    def ask(self, question, context):

        inputs = self.qa_tokenizer(
            question,
            context,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        with torch.no_grad():
            outputs = self.qa_model(**inputs)

        start_index = torch.argmax(outputs.start_logits)
        end_index = torch.argmax(outputs.end_logits)

        answer_tokens = inputs["input_ids"][0][
            start_index:end_index + 1
        ]

        answer = self.qa_tokenizer.decode(
            answer_tokens,
            skip_special_tokens=True
        )

        return answer


# Load research text
with open("research.txt", "r", encoding="utf-8") as file:
    research_text = file.read()


# Create assistant
assistant = AIResearchAssistant()


# Generate summary
print("\n--- RESEARCH SUMMARY ---")
print(assistant.summarize(research_text))


# Ask questions
print("\n--- QUESTION ANSWERING ---")

question1 = "What does AI detect faster than humans?"
print("Question:", question1)
print("Answer:", assistant.ask(question1, research_text))

question2 = "What is a critical goal for researchers?"
print("\nQuestion:", question2)
print("Answer:", assistant.ask(question2, research_text))