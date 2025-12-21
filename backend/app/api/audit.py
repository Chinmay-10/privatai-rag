from fastapi import APIRouter, Depends
from app.core.security import require_scopes
from app.db.session import SessionLocal
from app.db.models import AuditLog

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/")
def get_audit_logs(
    user=Depends(require_scopes(["documents:query"])),
):
    db = SessionLocal()
    try:
        logs = (
            db.query(AuditLog)
            .filter(AuditLog.tenant_id == user.tenant_id)
            .order_by(AuditLog.created_at.desc())
            .limit(50)
            .all()
        )
        return logs
    finally:
        db.close()
