"""Entry point for the FastAPI backend application."""
from __future__ import annotations

from fastapi import FastAPI

from backend import database
from backend.auth import models as auth_models
from backend.auth.routes import router as auth_router
from backend.data import models as data_models
from backend.data.views import router as data_router

app = FastAPI(title="SPO Lab NBA Insights")


def init_database() -> None:
    """Create all database tables and seed default roles."""

    database.Base.metadata.create_all(bind=database.engine)
    with database.get_session() as session:
        auth_models.get_or_create_default_roles(session)


init_database()

app.include_router(auth_router)
app.include_router(data_router)


@app.get("/")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
