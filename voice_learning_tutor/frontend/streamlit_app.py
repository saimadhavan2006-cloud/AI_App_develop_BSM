import os

import requests
import streamlit as st

API_BASE_URL = os.getenv(
    "TUTOR_API_URL",
    "http://127.0.0.1:8000",
)

st.set_page_config(
    page_title="Voice Learning Tutor",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Voice Learning Tutor")
st.caption("Learn from your textbooks with AI-powered explanations.")

with st.sidebar:
    st.header("Learning preferences")

    level = st.selectbox(
        "Your level",
        ["beginner", "intermediate", "advanced"],
    )

    depth = st.selectbox(
        "Explanation depth",
        ["short", "medium", "detailed"],
        index=1,
    )

    language = st.selectbox(
        "Answer language",
        ["English", "Telugu", "Hindi"],
    )

    st.divider()
    st.caption(f"Backend: {API_BASE_URL}")


with st.form("question_form"):
    question = st.text_area(
        "What would you like to learn?",
        placeholder="Example: Explain the classic 8051 architecture.",
        height=120,
    )

    submitted = st.form_submit_button(
        "✨ Explain this topic",
        type="primary",
        use_container_width=True,
    )


if submitted:
    if not question.strip():
        st.warning("Enter a question first.")
    else:
        with st.spinner("Finding textbook passages and preparing your answer..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/ask",
                    json={
                        "question": question.strip(),
                        "level": level,
                        "language": language,
                        "depth": depth,
                    },
                    timeout=(5, 360),
                )
                response.raise_for_status()
                result = response.json()

                st.session_state["last_question"] = result["question"]
                st.session_state["last_answer"] = result["answer"]
                st.session_state["last_sources"] = result.get("sources", [])

            except requests.exceptions.Timeout:
                st.error(
                    "The request timed out. The AI may still be processing "
                    "your question. Please check the backend before retrying."
                )
            except requests.exceptions.ConnectionError:
                st.error(
                    "Cannot connect to the backend. Start FastAPI on port 8000 "
                    "and try again."
                )
            except requests.exceptions.HTTPError as exc:
                detail = ""
                try:
                    detail = response.json().get("detail", "")
                except ValueError:
                    pass
                st.error(f"Backend error: {detail or exc}")
            except (ValueError, KeyError) as exc:
                st.error(f"Could not read the backend response: {exc}")


if "last_answer" in st.session_state:
    st.divider()
    st.subheader("📘 Explanation")
    st.markdown(st.session_state["last_answer"])

    sources = st.session_state.get("last_sources", [])

    st.subheader("📚 Textbook sources")

    if not sources:
        st.info("No textbook passages were returned for this answer.")
    else:
        for index, source in enumerate(sources, start=1):
            textbook = source.get("textbook") or source.get("label") or "Unknown textbook"
            page = source.get("page", "Unknown")
            chunks = source.get("chunks") or [source.get("chunk")]

            with st.expander(
                f"Source {index}: {textbook} — page {page}"
            ):
                st.markdown(f"**Textbook:** {textbook}")
                st.markdown(f"**Page:** {page}")

                if chunks and chunks != [None]:
                    st.markdown(
                        "**Retrieved chunks:** "
                        + ", ".join(str(chunk) for chunk in chunks)
                    )

                passage = source.get("text", "")
                if passage:
                    st.markdown("**Retrieved passage**")
                    st.markdown(passage)

                distance = source.get("distance")
                if distance is not None:
                    st.caption(
                        f"Retrieval distance: {distance:.3f}"
                    )
