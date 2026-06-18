import sqlite3

from backend.config import settings

DDL = """
CREATE TABLE IF NOT EXISTS query_logs (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    question     TEXT    NOT NULL,
    answer       TEXT    NOT NULL,
    timestamp    DATETIME NOT NULL,
    latency_ms   REAL    NOT NULL,
    answer_found BOOLEAN NOT NULL
);
"""


def init_db() -> None:
    conn = sqlite3.connect(settings.SQLITE_DB_PATH)
    try:
        conn.executescript(DDL)
        conn.commit()
    finally:
        conn.close()
