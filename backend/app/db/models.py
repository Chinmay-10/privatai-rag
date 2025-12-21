from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Boolean,
    Text,
    Index,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="tenant")
    documents = relationship("Document", back_populates="tenant")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)

    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)
    role = Column(String, default="user")  # admin | user | auditor
    active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tenant = relationship("Tenant", back_populates="users")


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)  # UUID
    tenant_id = Column(String, ForeignKey("tenants.id"), nullable=False)

    name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    content_hash = Column(String, nullable=False, index=True)

    classification = Column(
        String, default="internal"
    )  # public | internal | confidential | restricted

    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    tenant = relationship("Tenant", back_populates="documents")
    policies = relationship("DocumentPolicy", back_populates="document")


Index("idx_doc_tenant_name", Document.tenant_id, Document.name)


class DocumentPolicy(Base):
    __tablename__ = "document_policies"

    id = Column(Integer, primary_key=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)

    allowed_role = Column(String, nullable=False)  # user | admin | auditor
    allow_query = Column(Boolean, default=True)
    allow_summary = Column(Boolean, default=False)

    document = relationship("Document", back_populates="policies")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)

    actor_id = Column(Integer, nullable=True)
    tenant_id = Column(String, nullable=False)

    action = Column(String, nullable=False)  
    resource = Column(String, nullable=True)
    detail = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
