"""Utility helpers for authentication flows."""
from __future__ import annotations

import hashlib
from typing import Final

PASSWORD_SALT: Final = "spolab-nba-insight"


def hash_password(raw_password: str) -> str:
    """Return a deterministic salted hash for *raw_password*."""

    digest = hashlib.sha256()
    digest.update(PASSWORD_SALT.encode())
    digest.update(raw_password.encode())
    return digest.hexdigest()


def verify_password(raw_password: str, hashed_password: str) -> bool:
    """Check whether *raw_password* matches the stored hash."""

    return hash_password(raw_password) == hashed_password
