from typing import Annotated

from fastapi import APIRouter, Depends

from ..dependencies import get_current_user
from ..models import User
from .schemas import MeResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/me")
async def me(current_user: Annotated[User, Depends(get_current_user)]) -> MeResponse:
    return MeResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
    )
