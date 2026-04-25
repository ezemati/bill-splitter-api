from fastapi import APIRouter

from ..core import Settings, settings

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/settings")
async def get_settings() -> Settings:
    return settings
