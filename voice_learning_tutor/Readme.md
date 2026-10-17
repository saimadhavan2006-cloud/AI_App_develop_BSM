# 🎓 Voice-Enabled Interactive Learning Tutor

An AI-powered learning assistant that helps students understand academic concepts through text and voice. Built as part of my AI App Development Bootcamp.

## ✨ Features

- AI-generated educational explanations using Ollama and Llama 3.2.
- Voice input using Faster-Whisper speech recognition.
- Text-to-speech using Edge TTS.
- Voice-based question answering.
- Learning history stored in SQLite.
- Textbook indexing using ChromaDB and embeddings.
- OCR support for scanned PDFs using Tesseract.
- REST API built with FastAPI.
- Interactive API documentation through Swagger UI.

## 🛠️ Tech Stack

- **Language:** Python
- **Backend:** FastAPI
- **LLM:** Ollama — Llama 3.2
- **Embeddings:** nomic-embed-text
- **Speech recognition:** Faster-Whisper
- **Text-to-speech:** Edge TTS
- **Database:** SQLite
- **Vector database:** ChromaDB
- **PDF processing:** pypdf, pdf2image, Poppler
- **OCR:** Tesseract

## 📁 Project Structure

```text
voice_learning_tutor/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── routes/
│   └── services/
├── frontend/
├── knowledge_base/
├── tests/
├── index_textbooks.py
├── requirements.txt
└── README.md
```

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI_App_development.git
cd AI_App_development/voice_learning_tutor
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Set up Ollama

Install Ollama and download the required models:

```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 5. Configure OCR

Install Tesseract OCR and Poppler separately if you want to process scanned textbooks. Update their paths in the application configuration to match your computer.

### 6. Run the API

From the `voice_learning_tutor` directory:

```powershell
python -m uvicorn app.main:app --reload
```

Open these URLs in your browser:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## 📚 Textbook Indexing

Place authorized PDF files in `knowledge_base/MC textbooks/` and run:

```powershell
python index_textbooks.py
```

The indexing process extracts PDF text, uses OCR when necessary, creates embeddings, and stores searchable chunks in ChromaDB.

Textbook retrieval must be connected to the question-answering pipeline for answers to be grounded in retrieved textbook content.

## 🔒 Important Notes

- Keep `.env`, credentials, virtual environments, databases, generated audio, and local vector indexes out of GitHub.
- Do not upload copyrighted textbooks unless you have permission to redistribute them.
- Ollama runs locally, while Edge TTS uses an online service.
- Install Tesseract and Poppler separately; they are not installed through `requirements.txt`.

## 🚀 Future Improvements

- Complete textbook-grounded RAG question answering.
- Add an interactive student frontend.
- Add quizzes and assessments.
- Support multilingual learning.
- Add textbook source and page references.

## 👨‍💻 Author

Developed as part of an AI App Development Bootcamp.
