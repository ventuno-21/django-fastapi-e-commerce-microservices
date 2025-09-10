from fastapi import APIRouter, Depends, HTTPException, status

from .. import auth
from ..database.db import init_db
from ..database.models import User, UserRead
from ..database.schemas import LoginRequest, MeResponse, RegisterRequest, TokenResponse
from ..services import s_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
async def register(payload: RegisterRequest):
    existing = await s_user.get_user_by_username(payload.username)
    if existing:
        raise HTTPException(status_code=400, detail="username already exists")

    hashed = auth.hash_password(payload.password)
    user = await s_user.create_user(payload.username, payload.email, hashed)

    # ✅ Pydantic v2 syntax: convert SQLAlchemy/SQLModel object → schema
    return UserRead.model_validate(user, from_attributes=True)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    user = await s_user.get_user_by_username(payload.username)
    if not user or not auth.verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
        )
    token = auth.create_access_token({"sub": str(user.id), "username": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=MeResponse)
async def me(current_user: User = Depends(lambda: None)):
    # This endpoint will be protected by get_current_user in main router mount
    raise HTTPException(
        status_code=500, detail="Should be handled by dependency in main"
    )
