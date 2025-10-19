"""Pydantic schemas for dataset management."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DataSetBase(BaseModel):
    title: str
    description: Optional[str]


class DataSetRead(DataSetBase):
    id: int
    filename: str
    content_type: str
    created_at: datetime

    class Config:
        orm_mode = True


class UploadHistoryRead(BaseModel):
    id: int
    uploader_email: str
    uploaded_at: datetime
    notes: Optional[str]
    dataset: DataSetRead

    class Config:
        orm_mode = True


class DataUploadResponse(BaseModel):
    dataset: DataSetRead
    message: str
