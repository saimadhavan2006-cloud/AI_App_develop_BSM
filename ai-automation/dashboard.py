import sqlite3

import pandas as pd
import streamlit as st

from database import DB_PATH

st.set_page_config(
    page_title="AI Sentiment Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 AI Sentiment Automation")
st.caption("Customer feedback analytics powered by AI and SQLite")

# Load saved records directly from the existing database.
def load_data():
    with sqlite3.connect(DB_PATH, timeout=10) as connection:
        return pd.read_sql_query(
            """
            SELECT id, text, sentiment, confidence,
                   suggested_action, created_at
            FROM sentiment_history
            ORDER BY id DESC
            """,
            connection,
        )


if st.button("🔄 Refresh Data"):
    st.rerun()

try:
    df = load_data()
except (sqlite3.Error, pd.errors.DatabaseError) as exc:
    st.error(f"Could not load the database: {exc}")
    st.stop()

if df.empty:
    st.info(
        "No feedback records yet. Analyze some text using "
        "your FastAPI endpoint at http://127.0.0.1:8000/docs."
    )
    st.stop()

df["sentiment"] = df["sentiment"].str.upper()
df["confidence"] = pd.to_numeric(df["confidence"], errors="coerce")

total = len(df)
positive = int((df["sentiment"] == "POSITIVE").sum())
negative = int((df["sentiment"] == "NEGATIVE").sum())
average_confidence = df["confidence"].mean()

st.subheader("Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Analyses", total)
col2.metric("Positive Feedback", positive)
col3.metric("Negative Feedback", negative)
col4.metric(
    "Average Confidence",
    f"{average_confidence:.1%}"
    if pd.notna(average_confidence)
    else "N/A",
)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Sentiment Distribution")

    sentiment_counts = (
        df["sentiment"]
        .value_counts()
        .reindex(["POSITIVE", "NEGATIVE"], fill_value=0)
    )

    st.bar_chart(sentiment_counts)

with right:
    st.subheader("Confidence Scores")

    confidence_data = df.dropna(subset=["confidence"])

    if not confidence_data.empty:
        st.bar_chart(
            confidence_data.set_index("id")[["confidence"]]
            .sort_index()
        )
    else:
        st.info("No confidence scores available.")

st.divider()
st.subheader("Feedback History")

filter_col, search_col = st.columns([1, 2])

with filter_col:
    sentiment_filter = st.selectbox(
        "Filter by sentiment",
        ["ALL", "POSITIVE", "NEGATIVE"],
    )

with search_col:
    search_text = st.text_input(
        "Search feedback",
        placeholder="Enter a word or phrase...",
    )

filtered = df.copy()

if sentiment_filter != "ALL":
    filtered = filtered[
        filtered["sentiment"] == sentiment_filter
    ]

if search_text.strip():
    filtered = filtered[
        filtered["text"].str.contains(
            search_text.strip(),
            case=False,
            na=False,
            regex=False,
        )
    ]

st.caption(f"Showing {len(filtered)} of {total} records")

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True,
    column_config={
        "id": st.column_config.NumberColumn("ID"),
        "text": st.column_config.TextColumn(
            "Feedback",
            width="large",
        ),
        "sentiment": st.column_config.TextColumn("Sentiment"),
        "confidence": st.column_config.NumberColumn(
            "Confidence",
            format="%.4f",
        ),
        "suggested_action": st.column_config.TextColumn(
            "Suggested Action",
            width="large",
        ),
        "created_at": st.column_config.TextColumn("Created At"),
    },
)

st.caption(
    "Data source: sentiment.db | "
    "Refresh the dashboard to load the latest records."
)
