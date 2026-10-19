from pathlib import Path
import hashlib
import re

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
RETRIEVAL_DISTANCE_THRESHOLD = 0.70

client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = client.get_or_create_collection(name="microcontroller_textbooks_v2")


def get_embedding(text: str) -> list[float]:
    """Generate an embedding with the local Ollama embedding model."""
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
            pages.append({"page": page_number, "text": text})

    return pages


def split_page_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[str]:
    """Split one page into overlapping chunks."""
    text = " ".join(text.split())

    if not text:
        return []
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")

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
    """Extract, embed, and index PDFs in the configured knowledge folder."""
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
                for chunk_text in split_page_text(page_data["text"]):
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
                    json={"model": EMBEDDING_MODEL, "input": batch},
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


def _normalize_text(text: str) -> str:
    """Normalize whitespace for matching without changing wording."""
    return re.sub(r"\s+", " ", text).strip()


def _merge_overlapping_text(previous: str, current: str) -> str:
    """Merge chunks only when a reliable exact overlap is found."""
    previous = _normalize_text(previous)
    current = _normalize_text(current)

    if not previous:
        return current
    if not current:
        return previous
    if current in previous:
        return previous
    if previous in current:
        return current

    max_overlap = min(len(previous), len(current), 500)
    for size in range(max_overlap, 39, -1):
        if previous[-size:] == current[:size]:
            return previous + current[size:]

    # Never discard text if an exact overlap cannot be established.
    return previous + " " + current


def _text_similarity(first: str, second: str) -> float:
    """Calculate word-set Jaccard similarity for duplicate suppression."""
    first_words = set(re.findall(r"\b\w+\b", first.lower()))
    second_words = set(re.findall(r"\b\w+\b", second.lower()))

    if not first_words or not second_words:
        return 0.0

    return len(first_words & second_words) / len(first_words | second_words)


def get_adjacent_chunks(
    source: str,
    page: int,
    chunk: int,
    radius: int = 1,
) -> list[dict]:
    """Fetch nearby chunks from the same source and PDF page."""
    results = collection.get(
        where={"$and": [{"source": source}, {"page": page}]},
        include=["documents", "metadatas"],
    )

    nearby = []
    for document, metadata in zip(
        results.get("documents") or [],
        results.get("metadatas") or [],
    ):
        chunk_number = metadata.get("chunk")
        if (
            isinstance(chunk_number, int)
            and abs(chunk_number - chunk) <= radius
        ):
            nearby.append({"document": document, "metadata": metadata})

    nearby.sort(key=lambda item: item["metadata"]["chunk"])
    return nearby


def _assemble_passage(
    source: str,
    page: int,
    chunk: int,
    radius: int = 1,
) -> str:
    """Join neighboring chunks and remove confirmed exact overlap."""
    nearby = get_adjacent_chunks(source, page, chunk, radius)
    combined = ""

    for item in nearby:
        combined = _merge_overlapping_text(combined, item["document"])

    return combined


def retrieve_passages(
    question: str,
    top_k: int = 6,
) -> tuple[str, list[dict]]:
    """Retrieve relevant passages, group nearby chunks, and suppress duplicates."""
    if top_k <= 0 or collection.count() == 0:
        return "", []

    question_embedding = get_embedding(question)
    candidate_count = min(max(top_k * 5, 30), collection.count())

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=candidate_count,
        include=["documents", "metadatas", "distances"],
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    candidates = []
    seen_locations = set()

    for document, metadata, distance in zip(
        documents, metadatas, distances
    ):
        if (
            not document
            or metadata is None
            or distance is None
            or distance > RETRIEVAL_DISTANCE_THRESHOLD
        ):
            continue

        source = metadata.get("source", "Unknown textbook")
        page = metadata.get("page")
        chunk = metadata.get("chunk")

        if page is None or chunk is None:
            continue

        try:
            chunk = int(chunk)
            distance = float(distance)
        except (TypeError, ValueError):
            continue

        location = (source, page, chunk)
        if location in seen_locations:
            continue
        seen_locations.add(location)

        candidates.append({
            "source": source,
            "page": page,
            "chunk": chunk,
            "document": _normalize_text(document),
            "distance": distance,
        })

    if not candidates:
        return "", []

    # Group nearby candidate chunks from the same source and page.
    candidates.sort(
        key=lambda item: (
            item["source"],
            str(item["page"]),
            item["chunk"],
        )
    )

    groups = []
    current_group = []

    for candidate in candidates:
        if not current_group:
            current_group = [candidate]
            continue

        previous = current_group[-1]
        same_page = (
            candidate["source"] == previous["source"]
            and candidate["page"] == previous["page"]
        )
        nearby = candidate["chunk"] - previous["chunk"] <= 2

        if same_page and nearby:
            current_group.append(candidate)
        else:
            groups.append(current_group)
            current_group = [candidate]

    if current_group:
        groups.append(current_group)

    assembled = []

    for group in groups:
        # Expand around every retrieved chunk, then merge overlapping windows.
        windows = []

        for candidate in group:
            nearby_chunks = get_adjacent_chunks(
                candidate["source"],
                candidate["page"],
                candidate["chunk"],
                radius=1,
            )

            for item in nearby_chunks:
                text = _normalize_text(item.get("document", ""))
                chunk_number = item.get("metadata", {}).get("chunk")

                if text:
                    windows.append({
                        "chunk": chunk_number,
                        "text": text,
                    })

        # Include retrieved text as a fallback if the collection lookup
        # did not return any adjacent chunks.
        if not windows:
            windows = [
                {
                    "chunk": item["chunk"],
                    "text": item["document"],
                }
                for item in group
                if item["document"]
            ]

        windows.sort(
            key=lambda item: (
                item["chunk"] is None,
                item["chunk"] if item["chunk"] is not None else 0,
            )
        )

        passage_text = ""
        included_chunks = []

        for window in windows:
            passage_text = _merge_overlapping_text(
                passage_text,
                window["text"],
            )

            chunk_number = window.get("chunk")
            if isinstance(chunk_number, int):
                included_chunks.append(chunk_number)


        if not passage_text:
            continue

        best_candidate = min(group, key=lambda item: item["distance"])

        assembled.append({
            "source": best_candidate["source"],
            "page": best_candidate["page"],
            "chunk": best_candidate["chunk"],
            "chunks": sorted(set(included_chunks)),
            "text": passage_text,
            "distance": best_candidate["distance"],
        })

    assembled.sort(key=lambda item: item["distance"])

    selected = []

    for candidate in assembled:
        redundant = False

        for existing in selected:
            similarity = _text_similarity(
                candidate["text"], existing["text"]
            )

            same_location = (
                candidate["source"] == existing["source"]
                and candidate["page"] == existing["page"]
            )

            if same_location and similarity >= 0.55:
                redundant = True
                break

            if similarity >= 0.85:
                redundant = True
                break

        if not redundant:
            selected.append(candidate)

        if len(selected) >= top_k:
            break

    passages = []
    sources = []

    for index, candidate in enumerate(selected, start=1):
        passages.append(
            f"[Source {index}]\n"
            f"Textbook: {candidate['source']}\n"
            f"PDF page: {candidate['page']}\n"
            f"Chunks included: {candidate['chunks']}\n"
            f"Passage:\n{candidate['text']}"
        )

        sources.append({
            "label": f"Source {index}",
            "textbook": candidate["source"],
            "page": candidate["page"],
            "chunk": candidate["chunk"],
            "chunks": candidate.get("chunks", []),
            "text": candidate["text"],
            "distance": candidate["distance"],
        })

    print(
        f"DEBUG: Retrieved {len(passages)} usable passages "
        f"from {len(candidates)} candidate chunks."
    )

    return "\n\n".join(passages), sources

def retrieve_context(question: str, top_k: int = 4) -> str:
    """Return retrieved context for the language model."""
    context, _ = retrieve_passages(question, top_k)
    return context
