"""Shared pytest fixtures for backend tests."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from backend import database
from backend.auth import models as auth_models
from backend.auth.dependencies import get_db
from backend.main import app

TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_all():
    database.Base.metadata.create_all(bind=test_engine)
    with TestingSessionLocal() as session:
        auth_models.get_or_create_default_roles(session)


def drop_all():
    database.Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(autouse=True)
def setup_database(monkeypatch):
    monkeypatch.setattr("backend.database.engine", test_engine)
    monkeypatch.setattr("backend.database.SessionLocal", TestingSessionLocal)
    create_all()
    app.dependency_overrides[get_db] = override_get_db
    yield
    drop_all()
    app.dependency_overrides.clear()


@pytest.fixture()
def db_session() -> Session:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)
