from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


def create_vectorstore():
    loader = TextLoader(
        "information.txt",
        encoding="utf-8",
    )

    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=80,
    )

    splits = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    return Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
    )


def retrieve_answer(vectorstore, question, k=4):
    results = vectorstore.similarity_search(
        question,
        k=k,
    )

    if not results:
        return ""

    context_parts = []

    for i, doc in enumerate(results, start=1):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page")

        citation = f"Source: {source}"

        if page is not None:
            citation += f", Page: {page}"

        context_parts.append(
            f"[Document {i}]\n"
            f"{citation}\n"
            f"{doc.page_content}"
        )

    return "\n\n".join(context_parts)