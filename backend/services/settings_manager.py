from datetime import datetime
from typing import Any, Dict, Optional

import yaml

from ..config import get_config
from ..models.settings import Settings, SettingsUpdate
from . import file_system as fs


class SettingsManager:
    """
    Service for managing application settings with YAML file storage.
    """
    
    def __init__(self):
        self.config = get_config()
        self.storage_file = self.config.settings_file
        self._settings: Optional[Dict[str, Any]] = None
        self._loaded = False
    
    def _ensure_loaded(self) -> None:
        """Load settings from disk if not already loaded."""
        if not self._loaded:
            self._load_from_disk()
            self._loaded = True
    
    def _load_from_disk(self) -> None:
        """Load settings from the YAML file."""
        if not fs.file_exists(self.storage_file):
            # Initialize with defaults
            self._settings = {
                "notes_directory": str(self.config.notes_base_directory),
                "elasticsearch_url": self.config.elasticsearch_url,
                "elasticsearch_enabled": self.config.elasticsearch_enabled,
            }
            self._save_to_disk()
            return
        
        try:
            content = fs.read_file(self.storage_file)
            self._settings = yaml.safe_load(content)
        except Exception:
            # Use defaults if file can't be read
            self._settings = {
                "notes_directory": str(self.config.notes_base_directory),
                "elasticsearch_url": self.config.elasticsearch_url,
                "elasticsearch_enabled": self.config.elasticsearch_enabled,
            }
    
    def _save_to_disk(self) -> None:
        """Save settings to the YAML file."""
        if self._settings is None:
            return
        
        data = {
            **self._settings,
            "updated_at": datetime.now().isoformat(),
        }
        
        content = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
        fs.write_file(self.storage_file, content)
    
    def get_settings(self) -> Settings:
        """
        Get current application settings.
        
        Returns:
            Current settings
        """
        self._ensure_loaded()
        
        return Settings(
            notes_directory=self._settings.get("notes_directory"),
            elasticsearch_url=self._settings.get("elasticsearch_url"),
            elasticsearch_enabled=self._settings.get("elasticsearch_enabled", False),
        )
    
    def update_settings(self, update_data: SettingsUpdate) -> Settings:
        """
        Update application settings.
        
        Args:
            update_data: Fields to update
            
        Returns:
            Updated settings
        """
        self._ensure_loaded()
        
        if update_data.notes_directory is not None:
            self._settings["notes_directory"] = update_data.notes_directory
        
        if update_data.elasticsearch_url is not None:
            self._settings["elasticsearch_url"] = update_data.elasticsearch_url
        
        if update_data.elasticsearch_enabled is not None:
            self._settings["elasticsearch_enabled"] = update_data.elasticsearch_enabled
        
        self._save_to_disk()
        return self.get_settings()


# Singleton instance
_settings_manager: Optional[SettingsManager] = None


def get_settings_manager() -> SettingsManager:
    """Get the singleton SettingsManager instance."""
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager
