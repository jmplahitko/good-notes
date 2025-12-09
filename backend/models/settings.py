from typing import Optional
from pydantic import BaseModel, Field


class SettingsBase(BaseModel):
    """Base settings model."""
    notes_directory: Optional[str] = Field(
        default=None, 
        description="Directory path where notes are stored"
    )
    elasticsearch_url: Optional[str] = Field(
        default=None, 
        description="Elasticsearch server URL"
    )
    elasticsearch_enabled: bool = Field(
        default=False, 
        description="Whether Elasticsearch is enabled for search"
    )


class SettingsUpdate(SettingsBase):
    """Model for updating settings."""
    pass


class Settings(SettingsBase):
    """Complete settings model."""
    
    class Config:
        from_attributes = True

