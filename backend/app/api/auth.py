from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import User
from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


class SignupIn(BaseModel):
    username: str
    password: str
    tenant_id: str


class LoginIn(BaseModel):
    username: str
    password: str


@router.post("/signup")
def signup(data: SignupIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        tenant_id=data.tenant_id,
        role="user",
    )
    db.add(user)
    db.commit()

    return {"status": "user_created"}


@router.post("/login")
def login(data: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        user_id=str(user.id),
        tenant_id=user.tenant_id,
        role=user.role,
        scopes=[
            "documents:upload",
            "documents:query",
        ],
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "tenant_id": user.tenant_id,
        "role": user.role,
    }
