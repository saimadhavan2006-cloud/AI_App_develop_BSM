
from pathlib import Path

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

BASE_DIR = Path(__file__).resolve().parent
INFO_FILE = BASE_DIR / "information.txt"

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
    if not INFO_FILE.exists():
        return None

    documents = TextLoader(
        str(INFO_FILE),
        encoding="utf-8"
    ).load()

    for doc in documents:
        doc.metadata["source"] = "information.txt"
        doc.metadata["source_type"] = "built_in"

    chunks = split_documents(documents)

    return Chroma.from_documents(
        documents=chunks,
        embedding=get_embeddings()
    )

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
