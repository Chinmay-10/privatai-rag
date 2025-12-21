from typing import List
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "dev"

    # ---------------- DATABASE ----------------
    DATABASE_URL: str = "sqlite:///./data/privatai.db"

    # ---------------- SECURITY ----------------
    SECRET_KEY: str = "change-this-in-prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ---------------- CORS ----------------
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # ---------------- STORAGE ----------------
    FILE_STORE: str = "data/uploads"

    # ---------------- VECTOR STORE ----------------
    QDRANT_HOST: str = "qdrant"
    QDRANT_PORT: int = 6333

    # ---------------- LLM ----------------
    OLLAMA_URL: str = "http://privatai-ollama:11434"
    OLLAMA_MODEL: str = "phi"

    # ---------------- EMBEDDINGS ----------------
    EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

    class Config:
        env_file = ".env"
        extra = "forbid"


settings = Settings()

Path(settings.FILE_STORE).mkdir(parents=True, exist_ok=True)
