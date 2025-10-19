"""Pydantic schemas for authentication."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class RoleBase(BaseModel):
    name: str = Field(..., max_length=50)
    view_limit: Optional[int] = Field(None, ge=0)


class RoleCreate(RoleBase):
    pass


class RoleRead(RoleBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    role_id: Optional[int] = None


class UserRead(UserBase):
    id: int
    role: Optional[RoleRead]

    class Config:
        orm_mode = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
