"""Database models for authentication and authorization."""
from __future__ import annotations

from datetime import datetime, timedelta
from secrets import token_urlsafe

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from backend.database import Base


class Role(Base):
    """Role definition that controls view limits."""

    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    view_limit = Column(Integer, nullable=True, default=10)

    users = relationship("User", back_populates="role")


class User(Base):
    """Application user with a role-based view allocation."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    is_active = Column(Integer, default=1)

    role = relationship("Role", back_populates="users")
    tokens = relationship("AuthToken", back_populates="user", cascade="all, delete-orphan")
    view_logs = relationship(
        "backend.data.models.DataViewRecord",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    uploads = relationship(
        "backend.data.models.UploadHistory",
        back_populates="uploader",
        cascade="all, delete-orphan",
    )


class AuthToken(Base):
    """Simple database-backed bearer token."""

    __tablename__ = "auth_tokens"
    __table_args__ = (UniqueConstraint("token"),)

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="tokens")

    @classmethod
    def issue_for_user(cls, user: "User", lifetime_minutes: int = 60) -> "AuthToken":
        """Factory helper to issue a new token for *user*."""

        return cls(
            token=token_urlsafe(32),
            user=user,
            expires_at=datetime.utcnow() + timedelta(minutes=lifetime_minutes),
        )

    def is_valid(self) -> bool:
        """Check whether the token is still valid."""

        return datetime.utcnow() < self.expires_at


def get_or_create_default_roles(session) -> None:
    """Seed base roles with sensible defaults if they do not exist."""

    defaults = {
        "admin": None,
        "standard": 10,
        "premium": 100,
    }
    for name, limit in defaults.items():
        role = session.query(Role).filter_by(name=name).one_or_none()
        if role is None:
            role = Role(name=name, view_limit=limit)
            session.add(role)
    session.commit()
