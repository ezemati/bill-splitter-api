from fastapi import APIRouter, Depends

from ..core import Settings, settings
from ..dependencies import get_current_admin_user

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_admin_user)],
)


@router.get("/settings")
async def get_settings() -> Settings:
    return settings
