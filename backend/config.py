import os
from pathlib import Path
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Application configuration settings."""
    
    # API settings
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    api_prefix: str = "/api"
    
    # Storage paths
    notes_base_directory: Path = Path.home() / "Documents" / "GoodNotes" / "notes"
    notes_index_file: Path = Path.home() / "Documents" / "GoodNotes" / "notes_index.yaml"
    action_items_file: Path = Path.home() / "Documents" / "GoodNotes" / "action_items.yaml"
    settings_file: Path = Path.home() / "Documents" / "GoodNotes" / "settings.yaml"
    
    # Elasticsearch settings
    elasticsearch_url: str = "http://localhost:9200"
    elasticsearch_enabled: bool = False
    elasticsearch_notes_index: str = "goodnotes_notes"
    elasticsearch_action_items_index: str = "goodnotes_action_items"
    
    # CORS settings (for Electron/browser frontend)
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "app://.",  # Electron
    ]
    
    class Config:
        env_prefix = "GOODNOTES_"
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        self.notes_base_directory.mkdir(parents=True, exist_ok=True)
        self.action_items_file.parent.mkdir(parents=True, exist_ok=True)
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_config() -> Config:
    """Get cached configuration instance."""
    config = Config()
    config.ensure_directories()
    return config
