import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "sentiment.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS sentiment_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                sentiment TEXT NOT NULL,
                confidence REAL NOT NULL,
                suggested_action TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT
                    (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
            )
        """)


def save_sentiment(text, sentiment, confidence, action):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO sentiment_history
                (text, sentiment, confidence, suggested_action)
            VALUES (?, ?, ?, ?)
            """,
            (text, sentiment, confidence, action),
        )
        return cursor.lastrowid


def get_sentiment_history(limit=50):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, text, sentiment, confidence,
                   suggested_action, created_at
            FROM sentiment_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [dict(row) for row in rows]