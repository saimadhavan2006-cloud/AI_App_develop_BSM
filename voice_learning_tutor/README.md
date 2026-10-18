# Voice Learning Tutor

An AI-powered learning assistant designed to help students explore academic concepts through text and voice interaction. This project combines a local language model, speech processing, textbook indexing, and a REST API.

## Features

- **AI-generated explanations:** Uses Ollama with Llama 3.2.
- **Speech recognition:** Uses Faster-Whisper for voice input.
- **Text-to-speech:** Uses Edge TTS for spoken responses.
- **REST API:** FastAPI backend with interactive Swagger documentation.
- **Learning history:** SQLite database integration.
- **Textbook indexing:** Processes PDF content and creates searchable embeddings.
- **Vector storage:** Uses ChromaDB for indexed knowledge.
- **OCR support:** Tesseract OCR and PDF image conversion tools support scanned-document processing.
- **Web interface:** Includes a Streamlit frontend.
- **Automated tests:** Includes API tests and separate OCR/PDF test scripts.

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Backend API | FastAPI, Uvicorn |
| Language model | Ollama, Llama 3.2 |
| Embeddings | Ollama, `nomic-embed-text` |
| Speech recognition | Faster-Whisper |
| Text-to-speech | Edge TTS |
| Database | SQLite |
| Vector database | ChromaDB |
| PDF processing | pypdf, pdf2image |
| OCR | Tesseract |
| Frontend | Streamlit |
| Testing | pytest |

## Project Structure

```text
voice_learning_tutor/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routes/
│   └── services/
├── frontend/
│   └── streamlit_app.py
├── knowledge_base/
├── tests/
│   └── tests_api.py
├── index_textbooks.py
├── requirement.txt
├── Readme.md
└── .gitignore
```

Local databases, vector indexes, audio outputs, virtual environments, and credentials are excluded from this overview because they are generated or machine-specific files.

## Architecture Overview

1. The frontend provides an interface for interacting with the tutor.
2. FastAPI exposes backend endpoints.
3. Ollama generates answers using the configured language model.
4. Speech recognition and text-to-speech support voice interaction.
5. SQLite stores learning-related data.
6. The textbook indexing script extracts document content, generates embeddings, and stores indexed data in ChromaDB.

**RAG status:** Textbook indexing is available in the project. Answers should only be described as textbook-grounded when the retrieval results are actually connected to the answer-generation workflow.

## Getting Started

### Prerequisites

- Python
- Ollama
- Git
- Tesseract OCR and Poppler for scanned-PDF processing
- The Ollama models used by the application

### 1. Clone the repository

```powershell
git clone https://github.com/saimadhavan2006-cloud/AI_App_develop_BSM.git
cd AI_App_develop_BSM/voice_learning_tutor
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

The dependency file is currently named `requirement.txt`.

```powershell
python -m pip install -r requirement.txt
```

### 4. Start Ollama and download the models

```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

Make sure the models match the configuration used in the application.

### 5. Configure environment variables

Create a local `.env` file containing the required configuration. Use the variable names expected by the application.

**Never commit `.env` or API keys to GitHub.** Keep secrets out of source code and screenshots.

### 6. Run the API

From the `voice_learning_tutor` directory:

```powershell
python -m uvicorn app.main:app --reload
```

If the server starts successfully, open:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

Check `app/main.py` for the actual health-check route before relying on a health endpoint.

### 7. Run the Streamlit frontend

If the frontend is configured to connect to the API:

```powershell
streamlit run frontend/streamlit_app.py
```

### 8. Index textbooks

Place PDFs you are authorized to process in the configured knowledge-base directory, then run:

```powershell
python index_textbooks.py
```

The script's configured paths and dependencies determine which documents are indexed and where the generated vector database is stored.

## Testing

Run the API tests with:

```powershell
python -m pytest tests/
```

OCR and PDF test scripts can be run separately when their external dependencies are installed.

## Important Notes

- Keep `.env`, virtual environments, local databases, generated audio, and vector indexes out of version control.
- Tesseract and Poppler require separate installation.
- Edge TTS relies on an online service; Ollama runs locally.
- Only use textbook files you are authorized to process or redistribute.
- Rebuild local indexes when necessary instead of committing generated ChromaDB files.

## Future Improvements

- Complete and verify textbook-grounded RAG responses.
- Add source and page references to textbook answers.
- Improve frontend integration and error handling.
- Expand automated tests for voice, retrieval, and database workflows.
- Add learning quizzes and progress tracking.

## Author

**B. Sai Madhavan**

AI App Development Project