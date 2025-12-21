from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.upload import router as upload_router
from app.api.query import router as query_router
from app.api.documents import router as documents_router
from app.api.audit import router as audit_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(upload_router)
router.include_router(query_router)
router.include_router(documents_router)
router.include_router(audit_router)
