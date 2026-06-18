import sqlite3
from datetime import datetime

from backend.config import settings


def get_connection():
    return sqlite3.connect(settings.SQLITE_DB_PATH)


def insert_query_log(
    question: str,
    answer: str,
    latency_ms: float,
    answer_found: bool,
) -> int:
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO query_logs
        (
            question,
            answer,
            timestamp,
            latency_ms,
            answer_found
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            question,
            answer,
            datetime.now(),
            latency_ms,
            answer_found,
        ),
    )

    conn.commit()

    row_id = cursor.lastrowid

    conn.close()

    return row_id


def get_total_queries() -> int:
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM query_logs"
    )

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_average_latency() -> float:
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT AVG(latency_ms) FROM query_logs"
    )

    value = cursor.fetchone()[0]

    conn.close()

    return value or 0


def get_unanswered_queries() -> int:
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM query_logs
        WHERE answer_found = 0
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_frequent_questions(limit: int = 5):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            question,
            COUNT(*) AS frequency
        FROM query_logs
        GROUP BY question
        ORDER BY frequency DESC
        LIMIT ?
        """,
        (limit,),
    )

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "question": row[0],
            "count": row[1],
        }
        for row in rows
    ]