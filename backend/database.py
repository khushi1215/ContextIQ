import sqlite3
from contextlib import contextmanager
from datetime import datetime
from typing import Generator

from backend.config import settings


def get_connection() -> sqlite3.Connection:
    """Return a new SQLite connection with row factory set."""
    conn = sqlite3.connect(settings.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def managed_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager that opens, yields, and closes a SQLite connection."""
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def insert_query_log(
    question: str,
    answer: str,
    latency_ms: float,
    answer_found: bool,
) -> int:
    """Insert a new interaction record and return its row id."""
    sql = """
        INSERT INTO query_logs (question, answer, timestamp, latency_ms, answer_found)
        VALUES (?, ?, ?, ?, ?)
    """
    with managed_connection() as conn:
        cursor = conn.execute(
            sql,
            (question, answer, datetime.utcnow().isoformat(), latency_ms, answer_found),
        )
        return cursor.lastrowid


def fetch_all_logs() -> list[sqlite3.Row]:
    """Return all rows from the query_logs table."""
    with managed_connection() as conn:
        return conn.execute("SELECT * FROM query_logs ORDER BY timestamp DESC").fetchall()


def fetch_log_count() -> int:
    """Return the total number of logged interactions."""
    with managed_connection() as conn:
        row = conn.execute("SELECT COUNT(*) AS cnt FROM query_logs").fetchone()
        return row["cnt"]


def fetch_average_latency() -> float:
    """Return the average latency across all logged interactions."""
    with managed_connection() as conn:
        row = conn.execute("SELECT AVG(latency_ms) AS avg FROM query_logs").fetchone()
        return row["avg"] or 0.0


def fetch_unanswered_count() -> int:
    """Return the number of interactions where no answer was found."""
    with managed_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS cnt FROM query_logs WHERE answer_found = 0"
        ).fetchone()
        return row["cnt"]


def fetch_frequent_questions(limit: int = 5) -> list[dict]:
    """Return the most frequently asked questions."""
    sql = """
        SELECT question, COUNT(*) AS frequency
        FROM query_logs
        GROUP BY question
        ORDER BY frequency DESC
        LIMIT ?
    """
    with managed_connection() as conn:
        rows = conn.execute(sql, (limit,)).fetchall()
        return [{"question": r["question"], "frequency": r["frequency"]} for r in rows]
