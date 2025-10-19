"""Tests for dataset viewing quotas."""
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


def get_role(session, name: str, limit: int) -> Role:
    role = session.query(Role).filter(Role.name == name).one()
    role.view_limit = limit
    session.commit()
    session.refresh(role)
    return role


def upload_dataset(client, token: str):
    file_bytes = "col1\nvalue".encode()
    response = client.post(
        "/data/upload",
        data={"title": "Sample", "description": "desc"},
        files={"file": ("sample.csv", file_bytes, "text/csv")},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()["dataset"]["id"]


def test_view_limit_enforced(client, db_session):
    admin_role = get_role(db_session, "admin", 0)
    standard_role = get_role(db_session, "standard", 1)

    admin = create_user(db_session, "admin@example.com", admin_role)
    viewer = create_user(db_session, "viewer@example.com", standard_role)

    admin_token = client.post(
        "/auth/login", json={"email": admin.email, "password": "password123"}
    ).json()["access_token"]
    viewer_token = client.post(
        "/auth/login", json={"email": viewer.email, "password": "password123"}
    ).json()["access_token"]

    dataset_id = upload_dataset(client, admin_token)

    first_view = client.get(
        f"/data/datasets/{dataset_id}",
        headers={"Authorization": f"Bearer {viewer_token}"},
    )
    assert first_view.status_code == status.HTTP_200_OK

    second_view = client.get(
        f"/data/datasets/{dataset_id}",
        headers={"Authorization": f"Bearer {viewer_token}"},
    )
    assert second_view.status_code == status.HTTP_402_PAYMENT_REQUIRED
