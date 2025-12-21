from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.core.security import require_scopes
from app.services.rag_pipeline import (
    query_with_context,
    generate_answer,
)

router = APIRouter(prefix="/query", tags=["query"])


class QueryIn(BaseModel):
    question: str
    top_k: int = 8


@router.post("/")
def query_documents(
    payload: QueryIn,
    user=Depends(require_scopes(["documents:query"])),
):
    contexts = query_with_context(
        question=payload.question,
        tenant_id=user.tenant_id,
        role=user.role,
        top_k=payload.top_k,
    )

    answer = generate_answer(
        question=payload.question,
        contexts=contexts,
        tenant_id=user.tenant_id,
        user_id=int(user.sub),
    )

    return {"answer": answer}
