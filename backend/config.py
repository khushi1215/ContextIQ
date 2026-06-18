import os
from dotenv import dotenv_values

_env = dotenv_values(os.path.join(os.path.dirname(__file__), "..", ".env"))


class Settings:
    # Application
    APP_TITLE = "RAG Document Q&A System"
    APP_VERSION = "0.1.0"

    # Database
    DATABASE_URL = _env.get(
        "DATABASE_URL",
        "sqlite:///./logs.db"
    )

    SQLITE_DB_PATH = _env.get(
        "SQLITE_DB_PATH",
        "logs.db"
    )

    # Data Paths
    BASE_DIR = os.path.dirname(__file__)

    DATA_PATH = os.path.join(
        BASE_DIR,
        "data"
    )

    VECTORSTORE_PATH = os.path.join(
        BASE_DIR,
        "vectorstore"
    )

    #RAG Configuration
    CHUNK_SIZE = int(
        _env.get("CHUNK_SIZE", "900")
    )

    CHUNK_OVERLAP = int(
        _env.get("CHUNK_OVERLAP", "150")
    )

    TOP_K_RESULTS = int(
        _env.get("TOP_K_RESULTS", "3")
    )

    EMBEDDING_MODEL = _env.get(
        "EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    EMBEDDING_DIMENSION = int(
        _env.get("EMBEDDING_DIMENSION", "384")
    )

    # LLM
    LLM_PROVIDER = _env.get(
        "LLM_PROVIDER",
        "ollama"
    )

    LLM_MODEL = _env.get(
    "LLM_MODEL",
    "qwen2.5:1.5b")

    OLLAMA_URL = _env.get(
        "OLLAMA_URL",
        "http://localhost:11434/api/generate"
    )

    # Future Support
    OPENAI_API_KEY = _env.get(
        "OPENAI_API_KEY",
        ""
    )


settings = Settings()