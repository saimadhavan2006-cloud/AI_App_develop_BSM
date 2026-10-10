import streamlit as st

from rag import create_vectorstore, retrieve_answer
from ollama_client import ask_ollama


st.set_page_config(
    page_title="Raaju",
    page_icon="😎",
    layout="centered",
)

st.title("Raaju 😎")
st.caption(
    "Style naaku konchem ekkuve. "
    "Intelligence maatram adigithe chupistha."
)


SYSTEM_PROMPT = """
You are RAAJU, an original assistant with a Telugu cinematic
comedy personality inspired by the effortless sarcasm, casual
confidence, playful arrogance, and unexpected humor of a witty
Telugu movie protagonist.

PERSONALITY:
- Speak casually, confidently, and naturally.
- Be sarcastic without sounding angry or desperate to insult people.
- Use clever comebacks and unexpected punchlines.
- Treat ridiculous situations with amusing seriousness.
- Be playful, slightly mischievous, and unpredictable.
- Never force a joke into every sentence.
- Avoid generic AI phrases and repetitive catchphrases.
- Use natural Telugu-English (Teluglish) when it fits the user's style.
- Understand Telugu written in English letters.
- Respond in English, Telugu, or a natural mix according to the user.
- Keep the distinctive vibe while creating original dialogue.
- Do not reproduce movie scripts or imitate exact movie dialogue.

RESPONSE STYLE:
- Simple questions: short, witty answers.
- Technical questions: correct explanations with occasional humor.
- Bad ideas: roast the idea, then offer a better solution.
- Confusing situations: react with dry humor, then clarify.
- Serious questions: reduce the comedy and prioritize usefulness.
- Never sacrifice correctness for a punchline.

ACCURACY:
- Never fabricate facts, sources, dates, or statistics.
- Admit uncertainty when necessary.
- For College RAG mode, use only the retrieved context
  for college-specific claims.
- If retrieved information is insufficient, say so clearly.
- Never invent college fees, deadlines, regulations, or policies.

IDENTITY:
- Your name is Raaju.
- Speak with effortless confidence, witty sarcasm,
  playful arrogance, and natural Telugu-English humor.
- Have a relaxed, clever Telugu cinematic-comedy vibe.
- Deliver original punchlines and spontaneous comebacks.
- Never force jokes or repeat catchphrases.
- Be genuinely helpful when answering technical questions.
- You are an AI assistant, not a human or a movie character.
"""


@st.cache_resource
def get_vectorstore():
    return create_vectorstore()


def format_history(messages, max_messages=8):
    recent = messages[-max_messages:]

    return "\n".join(
        f"{'User' if msg['role'] == 'user' else 'Raaju'}: "
        f"{msg['content']}"
        for msg in recent
    )


def should_use_rag(question):
    question = question.lower()

    keywords = [
        "college", "university", "campus", "scholarship",
        "epass", "attendance", "faculty", "exam", "fees",
        "department", "hostel", "admission", "placement",
        "library", "principal", "academic", "semester",
        "deadline", "last date", "eligibility", "syllabus",
        "hall ticket", "internal marks", "college policy",
    ]

    return any(word in question for word in keywords)


def build_prompt(mode, question, messages, context=""):
    history = format_history(messages)

    if mode == "College RAG" or (
        mode == "Auto Mode" and should_use_rag(question)
    ):
        return f"""
{SYSTEM_PROMPT}

MODE: COLLEGE KNOWLEDGE

Answer college-specific questions using ONLY the
retrieved context provided below.

Rules:
- Do not invent deadlines, policies, fees, or statistics.
- If the context does not support an answer, explicitly
  say that you cannot verify it from the available documents.
- If a question asks for an official deadline, require
  an explicit date and relevant academic year in the evidence.
- Do not treat a missing date as proof that no deadline exists.
- Be clear about uncertainty.
- Keep the sarcastic personality subtle when accuracy matters.

RETRIEVED CONTEXT:
{context if context.strip() else "No relevant context was retrieved."}

CONVERSATION:
{history}

LATEST QUESTION:
{question}

Answer the latest question.
"""

    return f"""
{SYSTEM_PROMPT}

MODE: GENERAL CHAT

Answer naturally without pretending to have accessed
college documents or verified institutional information.

CONVERSATION:
{history}

LATEST QUESTION:
{question}

Answer the latest question.
"""


if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("⚙️ Settings")

    mode = st.radio(
        "Choose your mode",
        ["Savage Chat", "College RAG", "Auto Mode"],
    )

    st.caption("Savage Chat: General conversation")
    st.caption("College RAG: Document-grounded answers")
    st.caption("Auto Mode: Route college questions to RAG")

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Ask something... if you dare 😏")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Cooking up a response..."):

                use_rag = (
                    mode == "College RAG"
                    or (
                        mode == "Auto Mode"
                        and should_use_rag(user_input)
                    )
                )

                context = ""

                if use_rag:
                    vectorstore = get_vectorstore()
                    context = retrieve_answer(
                        vectorstore,
                        user_input,
                    )

                prompt = build_prompt(
                    mode=mode,
                    question=user_input,
                    messages=st.session_state.messages,
                    context=context,
                )

                answer = ask_ollama(prompt)
                st.markdown(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
        })

    except Exception as e:
        st.error(
            f"Couldn't complete the request: {e}"
        )