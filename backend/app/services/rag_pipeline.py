from typing import List, Dict, Optional
import uuid

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
    MatchAny,
)

from app.core.config import settings
from app.db.session import SessionLocal
from app.db.models import Document, DocumentPolicy, AuditLog
from app.services.llm import call_ollama


COLLECTION_NAME = "privatai_docs"

qdrant = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
)

embedder = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)


def ensure_collection(dim: int):
    collections = qdrant.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in collections]:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=dim,
                distance=Distance.COSINE,
            ),
        )


def index_chunks(
    *,
    chunks: List[str],
    metadata: Dict,
):
    vectors = embedder.encode(
        chunks,
        convert_to_numpy=True,
        show_progress_bar=False,
    )

    ensure_collection(vectors.shape[1])

    points = []

    for idx, vector in enumerate(vectors):
        points.append(
            {
                "id": str(uuid.uuid4()),
                "vector": vector.tolist(),
                "payload": {
                    "tenant_id": metadata["tenant_id"],
                    "document_id": metadata["document_id"],
                    "doc_name": metadata["doc_name"],
                    "chunk_index": idx,
                    "content_hash": metadata["content_hash"],
                    "text": chunks[idx],
                },
            }
        )

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )


def _allowed_documents(
    *,
    tenant_id: str,
    role: str,
) -> List[str]:
    db = SessionLocal()
    try:
        rows = (
            db.query(Document.id)
            .join(DocumentPolicy)
            .filter(
                Document.tenant_id == tenant_id,
                DocumentPolicy.allowed_role == role,
                DocumentPolicy.allow_query.is_(True),
            )
            .all()
        )
        return [r[0] for r in rows]
    finally:
        db.close()

def query_with_context(
    *,
    question: str,
    tenant_id: str,
    role: str,
    top_k: int = 8,
) -> List[Dict]:

    allowed_doc_ids = _allowed_documents(
        tenant_id=tenant_id,
        role=role,
    )

    if not allowed_doc_ids:
        return []

    query_vector = embedder.encode(question).tolist()

    flt = Filter(
        must=[
            FieldCondition(
                key="tenant_id",
                match=MatchValue(value=tenant_id),
            ),
            FieldCondition(
                key="document_id",
                match=MatchAny(any=allowed_doc_ids),
            ),
        ]
    )

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        query_filter=flt,
        limit=top_k,
        with_payload=True,
    )

    return [
        {
            "document_id": hit.payload["document_id"],
            "doc_name": hit.payload["doc_name"],
            "chunk_index": hit.payload["chunk_index"],
            "text": hit.payload["text"],
            "score": hit.score,
        }
        for hit in results
    ]




def generate_answer(
    *,
    question: str,
    contexts: List[Dict],
    tenant_id: str,
    user_id: Optional[int] = None,
) -> str:

    db = SessionLocal()

    try:
        if not contexts:
            answer = "No relevant information found in authorized documents."
        else:
            context_block = "\n\n".join(
                f"[{c['doc_name']} | chunk {c['chunk_index']}]\n{c['text']}"
                for c in contexts
            )

            prompt = f"""
You are a secure enterprise AI assistant.

Use only the provided context.
Do not use external knowledge.
Do not fabricate facts.
If the question is broad, summarize only from the context.

Context:
{context_block}

Question:
{question}

Answer:
"""

            answer = call_ollama(prompt)

        db.add(
            AuditLog(
                actor_id=user_id,
                tenant_id=tenant_id,
                action="QUERY",
                resource="RAG",
                detail=f"Retrieved {len(contexts)} chunks",
            )
        )
        db.commit()

        return answer

    finally:
        db.close()
