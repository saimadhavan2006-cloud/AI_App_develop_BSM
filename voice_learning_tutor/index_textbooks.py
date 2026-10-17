from app.services.rag_service import index_textbooks

if __name__ == "__main__":
    try:
        result = index_textbooks()
        print("Indexing completed!")
        print("Files:", result["files_indexed"])
        print("Total chunks:", result["total_chunks"])
    except Exception as exc:
        print("Indexing failed:", exc)