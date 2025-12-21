from app.db.session import SessionLocal
from app.db.models import Tenant, User, DocumentPolicy
from app.core.security import hash_password


def init_db():
    """
    Idempotent database bootstrap.
    Safe for Docker restarts.
    """
    db = SessionLocal()

    try:
        # -------- Tenant --------
        tenant = db.query(Tenant).filter(Tenant.id == "finance").first()
        if not tenant:
            tenant = Tenant(id="finance", name="Finance")
            db.add(tenant)
            db.commit()

        # -------- Admin --------
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                password_hash=hash_password("admin123"),
                tenant_id="finance",
                role="admin",
            )
            db.add(admin)
            db.commit()

        
        policies = db.query(DocumentPolicy).count()
        if policies == 0:
            db.add(
                DocumentPolicy(
                    document_id="*",
                    allowed_role="admin",
                    allow_query=True,
                    allow_summary=True,
                )
            )
            db.commit()

    finally:
        db.close()
