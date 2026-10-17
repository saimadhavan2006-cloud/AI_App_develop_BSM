
from pathlib import Path
import hashlib

import chromadb
import httpx
import pytesseract
from pdf2image import convert_from_path
from pypdf import PdfReader

PROJECT_DIR = Path(__file__).resolve().parents[2]
KNOWLEDGE_DIR = PROJECT_DIR / "knowledge_base" / "MC textbooks"
CHROMA_DIR = PROJECT_DIR / "chroma_db"

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH = (
    r"C:\Users\saima\Downloads\Release-26.09.0-0"
    r"\poppler-26.09.0\Library\bin"
)

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

EMBEDDING_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "nomic-embed-text:latest"

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection(
    name="microcontroller_textbooks"
)


def get_embedding(text: str) -> list[float]:
    response = httpx.post(
        EMBEDDING_URL,
        json={"model": EMBEDDING_MODEL, "input": text},
        timeout=120.0
    )
    response.raise_for_status()
    return response.json()["embeddings"][0]


def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()

        if len(text) < 40:
            print(
                f"  OCR: {pdf_path.name}, "
                f"page {page_number}/{len(reader.pages)}"
            )

            images = convert_from_path(
                str(pdf_path),
                first_page=page_number,
                last_page=page_number,
                dpi=200,
                poppler_path=POPPLER_PATH
            )

            if images:
                text = pytesseract.image_to_string(
                    images[0],
                    lang="eng"
                ).strip()

        if text:
            pages.append(
                f"\n[Page {page_number}]\n{text}"
            )

    return "\n".join(pages)


def split_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150
) -> list[str]:
    text = " ".join(text.split())
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])

        if end == len(text):
            break

        start = end - overlap

    return chunks


def index_textbooks() -> dict:
    if not KNOWLEDGE_DIR.exists():
        raise FileNotFoundError(
            f"Knowledge folder not found: {KNOWLEDGE_DIR}"
        )

    pdf_files = sorted(KNOWLEDGE_DIR.rglob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF files found in {KNOWLEDGE_DIR}"
        )

    total_chunks = 0
    indexed_files = []

    with httpx.Client(timeout=120.0) as http:
        for file_number, pdf_path in enumerate(pdf_files, start=1):
            print(
                f"\n[{file_number}/{len(pdf_files)}] "
                f"Processing: {pdf_path.name}"
            )

            text = extract_pdf_text(pdf_path)

            if not text.strip():
                print("  Warning: no text extracted; skipping.")
                continue

            chunks = split_text(text)
            documents = chunks
            ids = []
            metadatas = []

            file_hash = hashlib.sha256(
                str(pdf_path.resolve()).encode("utf-8")
            ).hexdigest()[:12]

            for index, chunk in enumerate(chunks):
                ids.append(f"{file_hash}_{index}")
                metadatas.append({
                    "source": pdf_path.name,
                    "chunk": index
                })

            for start in range(0, len(documents), 16):
                batch = documents[start:start + 16]

                response = http.post(
                    EMBEDDING_URL,
                    json={
                        "model": EMBEDDING_MODEL,
                        "input": batch
                    }
                )
                response.raise_for_status()
                embeddings = response.json()["embeddings"]

                batch_ids = ids[start:start + 16]
                batch_metadata = metadatas[start:start + 16]

                collection.upsert(
                    ids=batch_ids,
                    documents=batch,
                    metadatas=batch_metadata,
                    embeddings=embeddings
                )

                print(
                    f"  Indexed chunks: "
                    f"{min(start + len(batch), len(documents))}"
                    f"/{len(documents)}"
                )

            total_chunks += len(chunks)
            indexed_files.append(pdf_path.name)

    return {
        "files_indexed": indexed_files,
        "total_chunks": total_chunks
    }


def retrieve_context(question: str, top_k: int = 4) -> str:
    if collection.count() == 0:
        return ""

    question_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, collection.count())
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    passages = []

    for document, metadata in zip(documents, metadatas):
        passages.append(
            f"Source: {metadata['source']}\n{document}"
        )

    return "\n\n".join(passages)
