from fastapi import APIRouter, Depends

from ..database.models import UserRead
from ..database.schemas import MeResponse
from .deps import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=MeResponse)
async def read_current_user(current_user=Depends(get_current_user)):
    return MeResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
    )
