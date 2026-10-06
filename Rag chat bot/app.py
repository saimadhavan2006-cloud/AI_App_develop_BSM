import streamlit as st
from rag import create_vectorstore, retrieve_answer
from ollama_client import ask_ollama
st.set_page_config(page_title="College Information Chatbot", page_icon=":robot_face:")
st.title("College Information Chatbot")
st.write("Ask questions about the college and get answers based on the provided information.")
@st.cache_resource
def get_vectorstore():
    return create_vectorstore()
vectorstore = get_vectorstore()
question = st.text_input("Enter your question:")
if question:
    context = retrieve_answer(vectorstore, question)
    prompt= f""" you are college information assistant. 
    answer the question based on the context below.
    if the answer is not available in the context, say "I don't know".
    context: {context}
    question: {question}
    answer: """ 

    answer = ask_ollama(prompt)
    st.subheader("🤖 Answer:")
    st.write(answer)

 
