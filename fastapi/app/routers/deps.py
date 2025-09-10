from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.future import select

from ..auth import decode_token
from ..database.db import AsyncSessionLocal
from ..services.s_user import get_user_by_id
from ..database.models import User

http_bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user_id = payload.get("sub")
    async with AsyncSessionLocal() as session:  # AsyncSession from SQLAlchemy
        result = await session.execute(select(User).where(User.id == int(user_id)))
        user = result.scalars().first()  # like result.first() in SQLModel
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user


# with sqlmodel instead of sqlalchemy
# async def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
# ):
#     token = credentials.credentials
#     payload = decode_token(token)
#     if not payload:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
#         )
#     user_id = payload.get("sub")
#     async with AsyncSessionLocal() as session:
#         q = select(User).where(User.id == int(user_id))
#         result = await session.exec(q)
#         user = result.first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user
