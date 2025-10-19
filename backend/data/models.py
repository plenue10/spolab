"""Data ingestion and access models."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, LargeBinary, String, Text
from sqlalchemy.orm import relationship

from backend.database import Base


class DataSet(Base):
    """Structured NBA dataset uploaded by administrators."""

    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    filename = Column(String(255), nullable=False)
    content_type = Column(String(100), nullable=False)
    blob = Column(LargeBinary, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    upload_history = relationship("UploadHistory", back_populates="dataset", uselist=False)
    view_records = relationship(
        "DataViewRecord",
        back_populates="dataset",
        cascade="all, delete-orphan",
    )


class UploadHistory(Base):
    """Audit trail for uploads."""

    __tablename__ = "upload_history"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    uploader_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(Text, nullable=True)

    dataset = relationship("DataSet", back_populates="upload_history")
    uploader = relationship("backend.auth.models.User", back_populates="uploads")


class DataViewRecord(Base):
    """Record of dataset access for quota enforcement."""

    __tablename__ = "data_view_records"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    viewed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    dataset = relationship("DataSet", back_populates="view_records")
    user = relationship("backend.auth.models.User", back_populates="view_logs")
