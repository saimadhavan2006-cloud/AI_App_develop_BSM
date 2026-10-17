
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

# Keep the original collection intact during migration.
collection = client.get_or_create_collection(
    name="microcontroller_textbooks_v2"
)


def get_embedding(text: str) -> list[float]:
    response = httpx.post(
        EMBEDDING_URL,
        json={"model": EMBEDDING_MODEL, "input": text},
        timeout=120.0,
    )
    response.raise_for_status()
    return response.json()["embeddings"][0]


def extract_pdf_pages(pdf_path: Path) -> list[dict]:
    """Extract text page by page, using OCR for image-based pages."""
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
                poppler_path=POPPLER_PATH,
            )

            if images:
                text = pytesseract.image_to_string(
                    images[0], lang="eng"
                ).strip()

        if text:
            pages.append({
                "page": page_number,
                "text": text,
            })

    return pages


def split_page_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[str]:
    """Split a single page into overlapping chunks."""
    text = " ".join(text.split())

    if not text:
        return []

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

            pages = extract_pdf_pages(pdf_path)

            if not pages:
                print("  Warning: no text extracted; skipping.")
                continue

            file_hash = hashlib.sha256(
                str(pdf_path.resolve()).encode("utf-8")
            ).hexdigest()[:12]

            documents = []
            ids = []
            metadatas = []
            chunk_number = 0

            for page_data in pages:
                page_number = page_data["page"]
                page_chunks = split_page_text(page_data["text"])

                for chunk_text in page_chunks:
                    documents.append(chunk_text)
                    ids.append(f"{file_hash}_p{page_number}_c{chunk_number}")
                    metadatas.append({
                        "source": pdf_path.name,
                        "page": page_number,
                        "chunk": chunk_number,
                    })
                    chunk_number += 1

            for start in range(0, len(documents), 16):
                batch = documents[start:start + 16]

                response = http.post(
                    EMBEDDING_URL,
                    json={
                        "model": EMBEDDING_MODEL,
                        "input": batch,
                    },
                )
                response.raise_for_status()
                embeddings = response.json()["embeddings"]

                collection.upsert(
                    ids=ids[start:start + 16],
                    documents=batch,
                    metadatas=metadatas[start:start + 16],
                    embeddings=embeddings,
                )

                print(
                    f"  Indexed chunks: "
                    f"{min(start + len(batch), len(documents))}"
                    f"/{len(documents)}"
                )

            total_chunks += len(documents)
            indexed_files.append(pdf_path.name)

    return {
        "files_indexed": indexed_files,
        "total_chunks": total_chunks,
        "collection": "microcontroller_textbooks_v2",
    }


def retrieve_passages(
    question: str,
    top_k: int = 4,
) -> tuple[str, list[dict]]:
    if collection.count() == 0:
        return "", []

    question_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    passages = []
    sources = []

    for index, (document, metadata) in enumerate(
        zip(documents, metadatas),
        start=1,
    ):
        source = metadata.get("source", "Unknown textbook")
        page = metadata.get("page")
        chunk = metadata.get("chunk", -1)

        page_label = str(page) if page is not None else "Unknown"

        passages.append(
            f"[Source {index}]\n"
            f"Textbook: {source}\n"
            f"PDF page: {page_label}\n"
            f"Chunk: {chunk}\n"
            f"Passage:\n{document}"
        )

        distance = (
            distances[index - 1]
            if index - 1 < len(distances)
            else None
        )

        sources.append({
            "label": f"Source {index}",
            "textbook": source,
            "page": page,
            "chunk": chunk,
            "distance": distance,
        })

    return "\n\n".join(passages), sources


def retrieve_context(question: str, top_k: int = 4) -> str:
    context, _ = retrieve_passages(question, top_k)
    return context