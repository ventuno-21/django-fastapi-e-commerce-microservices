# basic CRUD helpers for User
# from sqlmodel import select
from sqlalchemy import select

from ..database.models import User
from ..database.db import AsyncSessionLocal


async def get_user_by_username(username: str):
    async with AsyncSessionLocal() as session:
        q = select(User).where(User.username == username)
        result = await session.execute(q)
        return result.scalars().first()


# with sqlmodel
# async def get_user_by_username(username: str):
#     async with AsyncSessionLocal() as session:
#         q = select(User).where(User.username == username)
#         result = await session.exec(q)
#         return result.first()


async def get_user_by_id(user_id: int):
    async with AsyncSessionLocal() as session:
        q = select(User).where(User.id == user_id)
        result = await session.execute(q)
        return result.scalars().first()


# with sqlmodel
# async def get_user_by_id(user_id: int):
#     async with AsyncSessionLocal() as session:
#         q = select(User).where(User.id == user_id)
#         result = await session.exec(q)
#         return result.first()


async def create_user(username: str, email: str, hashed_password: str):
    async with AsyncSessionLocal() as session:
        user = User(username=username, email=email, hashed_password=hashed_password)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


# with sqlmodel
# async def create_user(username: str, email: str, hashed_password: str):
#     async with AsyncSessionLocal() as session:
#         user = User(username=username, email=email, hashed_password=hashed_password)
#         session.add(user)
#         await session.commit()
#         await session.refresh(user)
#         return user
