# Voice Learning Tutor

An AI-powered learning assistant that helps students explore academic concepts through text and voice interaction. It combines a local language model, speech processing, textbook indexing, retrieval, and a REST API.

## Features

- **AI-generated explanations:** Uses Ollama with Llama 3.2.
- **8051 answer validation:** Checks selected classic 8051 architecture facts and retries generation when validation identifies issues.
- **Speech recognition:** Uses Faster-Whisper for voice input.
- **Text-to-speech:** Uses Edge TTS for spoken responses.
- **REST API:** FastAPI backend with interactive Swagger documentation.
- **Learning history:** Stores learning-related data using SQLite.
- **Textbook indexing:** Extracts PDF content and creates searchable embeddings.
- **Vector storage:** Uses ChromaDB for indexed knowledge.
- **OCR support:** Supports scanned-document processing with Tesseract OCR and PDF image conversion tools.
- **Web interface:** Provides a Streamlit frontend.
- **Automated tests:** Includes API, accuracy-validation, and retry tests.

## Project Structure

```text
voice_learning_tutor/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes/
│   └── services/
├── frontend/
│   └── streamlit_app.py
├── knowledge_base/
├── tests/
│   ├── test_8051_accuracy.py
│   ├── test_accuracy_retry.py
│   ├── test_api.py
│   └── test_llm_retry.py
├── index_textbooks.py
├── requirements.txt
├── README.md
└── .gitignore
```

Local databases, vector indexes, generated audio, virtual environments, and credentials are excluded from this overview because they are local or generated artifacts.

## Installation

From the cloned repository, enter the project directory:

```powershell
cd AI_App_develop_BSM/voice_learning_tutor
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Run the application

Start Ollama and make sure the configured models are available:

```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

Start the FastAPI server:

```powershell
python -m uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the Swagger UI.

In a separate terminal, activate the same virtual environment and start the frontend:

```powershell
streamlit run frontend/streamlit_app.py
```

## Testing

Run the automated test suite:

```powershell
python -m pytest -q
```

The latest reported test run completed with **21 passed**. Test results may vary as code and dependencies change.

## Important Notes

- Keep `.env`, API keys, local databases, vector indexes, and generated audio out of version control.
- Tesseract and Poppler require separate installation for applicable OCR/PDF workflows.
- Edge TTS relies on an online service; Ollama runs locally.
- Only process textbook files you are authorized to use.
- Rebuild local indexes when necessary rather than committing generated ChromaDB files.

## Author

**B. Sai Madhavan**

AI App Development Project
