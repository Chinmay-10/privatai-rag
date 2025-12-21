from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


from datetime import datetime, timedelta
from typing import List, Optional, Dict

from fastapi import Depends, Header, HTTPException, status
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel

from app.core.config import settings

# PASSWORD SECURITY
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    password = password.encode("utf-8")[:72]
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    plain = plain.encode("utf-8")[:72]
    return pwd_context.verify(plain, hashed)

bearer_scheme = HTTPBearer(auto_error=False)

# TOKEN SCHEMA (EXPLICIT TRUST MODEL)

class TokenPayload(BaseModel):
    sub: str              # user_id
    tenant_id: str
    role: str
    scopes: List[str]
    exp: datetime


# TOKEN CREATION

def create_access_token(
    *,
    user_id: str,
    tenant_id: str,
    role: str,
    scopes: List[str],
    expires_minutes: int = 60,
) -> str:
    payload = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "role": role,
        "scopes": scopes,
        "exp": datetime.utcnow() + timedelta(minutes=expires_minutes),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


# TOKEN VERIFICATION

def decode_token(token: str) -> TokenPayload:
    try:
        decoded = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return TokenPayload(**decoded)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


# ZERO-TRUST DEPENDENCY

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> TokenPayload:
    """
    Extracts and validates the JWT token.
    """

    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = credentials.credentials
    return decode_token(token)



def require_scopes(required_scopes: List[str]):
    """
    Dependency factory to enforce scopes.
    """
    def dependency(
        user: TokenPayload = Depends(get_current_user),
    ) -> TokenPayload:
        missing = set(required_scopes) - set(user.scopes)
        if missing:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing scopes: {missing}",
            )
        return user

    return dependency

