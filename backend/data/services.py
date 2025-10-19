"""Business logic for dataset uploads and access control."""
from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.auth.models import User
from backend.data import models


def remaining_views(user: User, db: Session) -> int:
    """Return how many views *user* has left based on their role."""

    if user.role is None:
        return 0

    if user.role.view_limit is None:
        return 10**9  # effectively unlimited

    used = (
        db.query(models.DataViewRecord)
        .filter(models.DataViewRecord.user_id == user.id)
        .count()
    )
    remaining = max(user.role.view_limit - used, 0)
    return remaining


def enforce_view_limit(user: User, dataset: models.DataSet, db: Session) -> models.DataViewRecord:
    """Validate that *user* may view *dataset* and record the attempt."""

    if user.role and user.role.name == "admin":
        return _log_view(user, dataset, db)

    views_left = remaining_views(user, db)
    if views_left <= 0:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="View limit exceeded. Upgrade required.",
        )

    return _log_view(user, dataset, db)


def _log_view(user: User, dataset: models.DataSet, db: Session) -> models.DataViewRecord:
    record = models.DataViewRecord(user=user, dataset=dataset)
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def store_dataset(
    *,
    db: Session,
    uploader: User,
    title: str,
    description: str | None,
    filename: str,
    content_type: str,
    file_bytes: bytes,
    notes: str | None = None,
) -> models.DataSet:
    """Persist a dataset blob and audit trail."""

    dataset = models.DataSet(
        title=title,
        description=description,
        filename=filename,
        content_type=content_type,
        blob=file_bytes,
    )
    db.add(dataset)
    db.flush()

    history = models.UploadHistory(dataset=dataset, uploader=uploader, notes=notes)
    db.add(history)
    db.commit()
    db.refresh(dataset)
    return dataset
