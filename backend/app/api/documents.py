from fastapi import APIRouter, Depends
from app.core.security import require_scopes
from app.services.document_loader import list_documents

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/")
def get_documents(
    user=Depends(require_scopes(["documents:query"])),
):
    return list_documents(user.tenant_id)
