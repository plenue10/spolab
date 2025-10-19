"""API routes for dataset ingestion and retrieval."""
from __future__ import annotations

import csv
import io

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_user, get_db, require_role
from backend.auth.models import User
from backend.data import models, schemas, services

router = APIRouter(prefix="/data", tags=["data"])


@router.post("/upload", response_model=schemas.DataUploadResponse, status_code=status.HTTP_201_CREATED)
def upload_dataset(
    title: str,
    description: str | None = None,
    notes: str | None = None,
    file: UploadFile = File(...),
    uploader: User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
) -> schemas.DataUploadResponse:
    """Accept an uploaded NBA dataset and store the raw bytes."""

    raw_bytes = file.file.read()
    if not raw_bytes:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty upload")

    # Simple CSV validation to ensure integrity.
    if "csv" in (file.content_type or ""):
        _validate_csv(raw_bytes)

    dataset = services.store_dataset(
        db=db,
        uploader=uploader,
        title=title,
        description=description,
        filename=file.filename,
        content_type=file.content_type or "application/octet-stream",
        file_bytes=raw_bytes,
        notes=notes,
    )
    return schemas.DataUploadResponse(dataset=dataset, message="Upload successful")


@router.get("/datasets", response_model=list[schemas.DataSetRead])
def list_datasets(db: Session = Depends(get_db)) -> list[models.DataSet]:
    return db.query(models.DataSet).all()


@router.get("/datasets/{dataset_id}", response_model=schemas.DataSetRead)
def get_dataset(
    dataset_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> models.DataSet:
    dataset = db.get(models.DataSet, dataset_id)
    if dataset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dataset not found")

    services.enforce_view_limit(user, dataset, db)
    return dataset


@router.get("/uploads", response_model=list[schemas.UploadHistoryRead])
def list_upload_history(_: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    records = db.query(models.UploadHistory).order_by(models.UploadHistory.uploaded_at.desc()).all()
    response: list[schemas.UploadHistoryRead] = []
    for record in records:
        response.append(
            schemas.UploadHistoryRead(
                id=record.id,
                uploader_email=record.uploader.email,
                uploaded_at=record.uploaded_at,
                notes=record.notes,
                dataset=record.dataset,
            )
        )
    return response


def _validate_csv(raw_bytes: bytes) -> None:
    sample = raw_bytes.decode("utf-8")
    reader = csv.reader(io.StringIO(sample))
    try:
        header = next(reader)
    except StopIteration as exc:  # pragma: no cover - defensive programming
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid CSV") from exc
    if not header:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CSV missing header")
