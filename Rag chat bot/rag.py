from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
def create_vectorstore():
    loader = TextLoader("information.txt")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

    documents = loader.load()
    splits = text_splitter.split_documents(documents)
    print(documents)
    print(splits)
    print(f"Number of splits: {len(splits)}")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
    return vectorstore
def retrieve_answer(vectorstore, question):
    results = vectorstore.similarity_search(question, k=2)
    context = "\n\n".join([result.page_content for result in results])
   
    return context