from pathlib import Path
import hashlib
import shutil

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Define the project paths FIRST.
BASE_DIR = Path(__file__).resolve().parent
INFO_FILE = BASE_DIR / "information.txt"
DB_DIR = BASE_DIR / "chroma_db"
HASH_FILE = DB_DIR / "information_hash.txt"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )
    return splitter.split_documents(documents)


def create_vectorstore():
    """Load the saved index or rebuild it when information.txt changes."""

    if not INFO_FILE.exists():
        raise FileNotFoundError(
            f"Knowledge file not found: {INFO_FILE}"
        )

    # Detect changes to the built-in knowledge file.
    file_text = INFO_FILE.read_text(encoding="utf-8")
    current_hash = hashlib.sha256(
        file_text.encode("utf-8")
    ).hexdigest()

    saved_hash = None
    if HASH_FILE.exists():
        saved_hash = HASH_FILE.read_text(
            encoding="utf-8"
        ).strip()

    # Reuse the existing database if the source has not changed.
    if DB_DIR.exists() and saved_hash == current_hash:
        print("Loading existing persistent Chroma database...")

        return Chroma(
            persist_directory=str(DB_DIR),
            embedding_function=get_embeddings()
        )

    # Rebuild if this is the first run or the source changed.
    if DB_DIR.exists():
        print("Knowledge file changed. Rebuilding Chroma database...")
        shutil.rmtree(DB_DIR)

    print("Creating persistent Chroma database...")

    documents = TextLoader(
        str(INFO_FILE),
        encoding="utf-8"
    ).load()

    for doc in documents:
        doc.metadata["source"] = "information.txt"
        doc.metadata["source_type"] = "built_in"

    chunks = split_documents(documents)

    if not chunks:
        raise ValueError(
            "No readable text found in information.txt"
        )

    DB_DIR.mkdir(parents=True, exist_ok=True)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings(),
        persist_directory=str(DB_DIR)
    )

    # Save the source hash only after indexing succeeds.
    HASH_FILE.write_text(
        current_hash,
        encoding="utf-8"
    )

    print(f"Indexed {len(chunks)} chunks successfully.")

    return vectorstore


def load_uploaded_pdf(file_path, filename):
    documents = PyPDFLoader(str(file_path)).load()

    for doc in documents:
        doc.metadata["source"] = filename
        doc.metadata["source_type"] = "uploaded_pdf"
        doc.metadata["page"] = doc.metadata.get("page", 0) + 1

    return split_documents(documents)


def retrieve_documents(vectorstore, question, k=5):
    """Retrieve more evidence to improve coverage."""
    if vectorstore is None:
        return []

    try:
        # Retrieve relevant chunks without an overly strict score cutoff.
        return vectorstore.similarity_search(
            question,
            k=k
        )
    except Exception as e:
        print(f"Retrieval error: {e}")
        return []


def format_context(documents):
    sections = []

    for doc in documents:
        source = doc.metadata.get("source", "Unknown source")
        page = doc.metadata.get("page")

        location = f", page {page}" if page else ""

        sections.append(
            f"Source: {source}{location}\n"
            f"Content: {doc.page_content}"
        )

    return "\n\n---\n\n".join(sections)
