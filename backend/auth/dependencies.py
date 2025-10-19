"""FastAPI dependencies shared across routers."""
from __future__ import annotations

from typing import Generator

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from backend.database import SessionLocal
from backend.auth import models

security_scheme = HTTPBearer()


def get_db() -> Generator[Session, None, None]:
    """Provide a SQLAlchemy session per request."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_token(
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    db: Session = Depends(get_db),
) -> models.AuthToken:
    token = (
        db.query(models.AuthToken)
        .filter(models.AuthToken.token == credentials.credentials)
        .one_or_none()
    )
    if token is None or not token.is_valid():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return token


def get_current_user(token: models.AuthToken = Depends(get_current_token)) -> models.User:
    user = token.user
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user


def require_role(role_name: str):
    """Dependency factory ensuring the current user has the required role."""

    def dependency(user: models.User = Depends(get_current_user)) -> models.User:
        if user.role is None or user.role.name != role_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role",
            )
        return user

    return dependency
