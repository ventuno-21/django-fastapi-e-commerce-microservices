from typing import Optional
from sqlmodel import SQLModel, Field, Column, String, DateTime
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)

    username: str = Field(
        sa_column=Column("username", String(length=50), unique=True, nullable=False)
    )

    email: str = Field(
        sa_column=Column("email", String(length=100), unique=True, nullable=False)
    )
    hashed_password: str

    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    created_at: datetime = Field(
        sa_column=Column("created_at", DateTime, nullable=False),
        default_factory=datetime.utcnow,
    )

    updated_at: datetime = Field(
        sa_column=Column("updated_at", DateTime, nullable=False),
        default_factory=datetime.utcnow,
    )


class UserCreate(SQLModel):
    username: str
    email: str
    password: str


class UserRead(SQLModel):
    id: int
    username: str
    email: str
    is_active: bool


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
