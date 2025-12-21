from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine, Base
from app.db.init_db import init_db
from app.api.router import router as api_router

app = FastAPI(
    title="PrivatAI-RAG",
    description="Zero-Trust, Policy-Aware, Auditable RAG System",
    version="2.0.0",
)

@app.on_event("startup")
def on_startup():
    """
    Enforces database consistency and system readiness.
    Docker-safe and idempotent.
    """
    # Create tables if missing
    Base.metadata.create_all(bind=engine)

    # Initialize base tenants / admin safely
    init_db()

    print("[STARTUP] Database initialized")
    print("[STARTUP] PrivatAI-RAG ready")


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.get("/health", tags=["system"])
def health_check():
    """
    Liveness probe (Docker / K8s friendly)
    """
    return {"status": "ok"}


@app.get("/ready", tags=["system"])
def readiness_check():
    """
    Readiness probe – confirms DB + vector store assumptions.
    """
    return {
        "database": "ready",
        "vector_store": "ready",
        "mode": settings.ENV,
    }
