# Raaju — Personal AI Assistant

Raaju is a Python-based personal AI assistant project designed to provide conversational AI through a local language model, with Retrieval-Augmented Generation (RAG) capabilities.

The project is being developed toward a more capable desktop assistant with voice interaction and practical automation features.

## Features

- **AI conversation:** Generate responses using Ollama.
- **RAG integration:** Retrieve relevant information from a local knowledge source.
- **Modular architecture:** Separate application logic, AI communication, and retrieval functionality.
- **Extensible design:** A foundation for future voice interaction and desktop automation.

## Technology Stack

- Python
- Ollama
- Large Language Models (LLMs)
- Retrieval-Augmented Generation (RAG)
- Git and GitHub

## Project Structure

```text
Raju_Savage_Ai/
├── app.py
├── ollama_client.py
├── rag.py
├── info.txt
├── requre.txt
└── README.md
```

### File Description

| File | Purpose |
|---|---|
| `app.py` | Main application entry point |
| `ollama_client.py` | Handles communication with Ollama |
| `rag.py` | Implements retrieval-related functionality |
| `info.txt` | Local information source |
| `requre.txt` | Existing dependency list |

## Getting Started

### Prerequisites

- Python installed on your system
- Ollama installed and running
- A compatible language model downloaded in Ollama

### Setup

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Create and activate a Python virtual environment.
4. Install the dependencies listed in `requre.txt`.
5. Ensure Ollama is running and the model configured in the application is available.
6. Run the application using the appropriate command for `app.py`.

## Future Improvements

- Voice input and text-to-speech
- Wake-word or hands-free listening
- Safe Windows desktop automation
- Improved knowledge retrieval
- A more polished desktop interface

## Project Status

Under active development. Features listed under future improvements may not yet be implemented.

## Author

B. Sai Madhavan