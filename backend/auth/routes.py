"""FastAPI routers for authentication and authorization."""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth import models, schemas, utils
from backend.auth.dependencies import get_current_user, get_db, require_role

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/roles", response_model=schemas.RoleRead)
def create_role(
    payload: schemas.RoleCreate,
    _: models.User = Depends(require_role("admin")),
    db: Session = Depends(get_db),
) -> models.Role:
    existing = db.query(models.Role).filter(models.Role.name == payload.name).one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role already exists")

    role = models.Role(name=payload.name, view_limit=payload.view_limit)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@router.get("/roles", response_model=list[schemas.RoleRead])
def list_roles(db: Session = Depends(get_db)) -> list[models.Role]:
    return db.query(models.Role).all()


@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register_user(payload: schemas.UserCreate, db: Session = Depends(get_db)) -> models.User:
    if db.query(models.User).filter(models.User.email == payload.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    role = None
    if payload.role_id:
        role = db.get(models.Role, payload.role_id)
        if role is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
    else:
        role = db.query(models.Role).filter(models.Role.name == "standard").one_or_none()

    user = models.User(
        email=payload.email,
        hashed_password=utils.hash_password(payload.password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)) -> schemas.TokenResponse:
    user = db.query(models.User).filter(models.User.email == payload.email).one_or_none()
    if user is None or not utils.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = models.AuthToken.issue_for_user(user)
    db.add(token)
    db.commit()
    db.refresh(token)

    return schemas.TokenResponse(
        access_token=token.token,
        expires_at=token.expires_at,
    )


@router.get("/me", response_model=schemas.UserRead)
def read_current_user(current_user: models.User = Depends(get_current_user)) -> models.User:
    return current_user
