"""Tests for upload audit trail."""
from __future__ import annotations

from fastapi import status

from backend.auth import utils
from backend.auth.models import Role, User


def create_user(session, email: str, role: Role) -> User:
    user = User(email=email, hashed_password=utils.hash_password("password123"), role=role)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_upload_history_recorded(client, db_session):
    admin_role = db_session.query(Role).filter(Role.name == "admin").one()
    admin = create_user(db_session, "admin@example.com", admin_role)

    token = client.post(
        "/auth/login", json={"email": admin.email, "password": "password123"}
    ).json()["access_token"]

    file_bytes = "col1\nvalue".encode()
    upload_response = client.post(
        "/data/upload",
        data={"title": "Sample", "description": "desc", "notes": "weekly update"},
        files={"file": ("sample.csv", file_bytes, "text/csv")},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert upload_response.status_code == status.HTTP_201_CREATED

    history_response = client.get(
        "/data/uploads",
        headers={"Authorization": f"Bearer {token}"},
    )
    payload = history_response.json()
    assert len(payload) == 1
    assert payload[0]["uploader_email"] == admin.email
    assert payload[0]["notes"] == "weekly update"
