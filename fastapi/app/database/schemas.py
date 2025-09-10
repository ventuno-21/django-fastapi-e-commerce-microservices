# For this project we use models.py SQLModel classes as lightweight schemas too,
# but we define a couple simple pydantic-style schemas for requests.
from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
