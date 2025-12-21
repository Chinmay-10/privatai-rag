from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.core.security import require_scopes
from app.db.session import get_db
from app.db.models import Document, DocumentPolicy
from app.services.document_loader import load_and_chunk
from app.services.rag_pipeline import index_chunks

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("/")
def upload_document(
    file: UploadFile = File(...),
    user=Depends(require_scopes(["documents:upload"])),
    db: Session = Depends(get_db),
):
    # Load + chunk
    chunks, metadata = load_and_chunk(
        file=file,
        tenant_id=user.tenant_id,
    )

    
    index_chunks(
        chunks=chunks,
        metadata=metadata,
    )

    
    document = Document(
        id=metadata["document_id"],
        tenant_id=user.tenant_id,
        name=metadata["doc_name"],
        file_path=metadata["file_path"],
        content_hash=metadata["content_hash"],
        created_by=int(user.sub),
    )
    db.add(document)


    policy = DocumentPolicy(
        document_id=document.id,
        allowed_role=user.role,
        allow_query=True,
        allow_summary=True,
    )
    db.add(policy)

    db.commit()

    return {
        "status": "indexed",
        "document_id": metadata["document_id"],
        "chunks": len(chunks),
    }
