# JNTUH AI Campus Assistant 🎓

A Python-based AI campus assistant designed to answer questions about Jawaharlal Nehru Technological University Hyderabad (JNTUH), Kukatpally, using campus information and Retrieval-Augmented Generation (RAG).

The project combines a Streamlit interface, local knowledge retrieval, ChromaDB, and Ollama to provide context-aware answers.

## Features

- **Campus question answering:** Responds to questions using the available campus knowledge.
- **Retrieval-Augmented Generation (RAG):** Retrieves relevant information before generating an answer.
- **Local language model:** Uses Ollama for AI response generation.
- **Vector database:** Uses ChromaDB to store and retrieve embedded information.
- **Campus knowledge source:** Uses `information.txt` as a built-in information source.
- **PDF support:** Supports document-based knowledge ingestion if enabled in the application.

## Technology Stack

- Python
- Streamlit
- Ollama
- ChromaDB
- LangChain
- Sentence Transformers
- Retrieval-Augmented Generation (RAG)

## Project Structure

```text
Rag_chat_bot/
├── app.py
├── rag.py
├── rag_backup.py
├── ollama_client.py
├── information.txt
├── requirements.txt
├── README.md
└── chroma_db/   # Locally generated database; excluded from Git
```

## How It Works

1. Campus information is loaded from the configured knowledge source.
2. The RAG pipeline splits information into chunks and creates embeddings.
3. ChromaDB stores the embeddings for similarity-based retrieval.
4. Relevant information is retrieved when a user asks a question.
5. Ollama generates a response using the retrieved context.
6. Streamlit provides the user interface.

## Setup

### Prerequisites

- Python
- Ollama installed and running
- The language model configured in `ollama_client.py`
- Dependencies listed in `requirements.txt`

### Installation

From the project directory, create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Ensure Ollama is running and the required model is available. Then launch the application:

```powershell
streamlit run app.py
```

## Knowledge Base

The built-in campus knowledge is stored in `information.txt`. The application may also support uploaded documents, depending on the configured ingestion workflow.

## Generated Files

The `chroma_db/` directory contains generated vector-database data. It should be recreated by the application's indexing process when needed rather than committed to Git.

## Future Improvements

- Expand the campus knowledge base.
- Improve retrieval accuracy and answer citations.
- Add more university documents and regulations.
- Improve error handling and user feedback.
- Add evaluation tests for retrieval and answer quality.

## Project Status

An ongoing AI and RAG learning project.

## Author

B. Sai Madhavan