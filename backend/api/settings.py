from fastapi import APIRouter

from ..models.settings import Settings, SettingsUpdate
from ..services.settings_manager import get_settings_manager


router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=Settings)
async def get_settings() -> Settings:
    """Get current application settings."""
    manager = get_settings_manager()
    return manager.get_settings()


@router.put("", response_model=Settings)
async def update_settings(update_data: SettingsUpdate) -> Settings:
    """
    Update application settings.
    
    Only provided fields will be updated.
    """
    manager = get_settings_manager()
    return manager.update_settings(update_data)

