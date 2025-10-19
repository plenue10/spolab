"""Tests for dataset upload permissions."""
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


def get_role(session, name: str, default_limit: int) -> Role:
    role = session.query(Role).filter(Role.name == name).one()
    role.view_limit = default_limit
    session.commit()
    session.refresh(role)
    return role


def test_standard_user_cannot_upload(client, db_session):
    role = get_role(db_session, "standard", 2)
    user = create_user(db_session, "viewer@example.com", role)

    token = client.post(
        "/auth/login",
        json={"email": user.email, "password": "password123"},
    ).json()["access_token"]

    file_bytes = "col1\nvalue".encode()
    response = client.post(
        "/data/upload",
        data={"title": "Sample", "description": "desc"},
        files={"file": ("sample.csv", file_bytes, "text/csv")},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_can_upload(client, db_session):
    admin_role = get_role(db_session, "admin", 0)
    admin = create_user(db_session, "admin@example.com", admin_role)

    token = client.post(
        "/auth/login",
        json={"email": admin.email, "password": "password123"},
    ).json()["access_token"]

    file_bytes = "col1\nvalue".encode()
    response = client.post(
        "/data/upload",
        data={"title": "Sample", "description": "desc"},
        files={"file": ("sample.csv", file_bytes, "text/csv")},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
