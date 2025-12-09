import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from ..config import get_config
from ..models.action_item import ActionItem, ActionItemCreate, ActionItemUpdate
from . import file_system as fs


class ActionItemsManager:
    """
    Service for managing action items with YAML file storage.
    
    All action items are stored in a single YAML file for simplicity,
    efficient querying (filtering, sorting), and human readability.
    """
    
    def __init__(self):
        self.config = get_config()
        self.storage_file = self.config.action_items_file
        self._items: Dict[str, Dict[str, Any]] = {}
        self._loaded = False
    
    def _ensure_loaded(self) -> None:
        """Load action items from disk if not already loaded."""
        if not self._loaded:
            self._load_from_disk()
            self._loaded = True
    
    def _load_from_disk(self) -> None:
        """Load action items from the YAML file."""
        self._items.clear()
        
        if not fs.file_exists(self.storage_file):
            return
        
        try:
            content = fs.read_file(self.storage_file)
            data = yaml.safe_load(content)
            
            if isinstance(data, dict) and "items" in data:
                for item_data in data["items"]:
                    if "id" in item_data:
                        self._items[item_data["id"]] = item_data
        except Exception:
            # Start with empty items if file can't be read
            pass
    
    def _save_to_disk(self) -> None:
        """Save all action items to the YAML file."""
        data = {
            "items": list(self._items.values()),
            "updated_at": datetime.now().isoformat(),
        }
        
        content = yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False)
        fs.write_file(self.storage_file, content)
    
    def _serialize_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize an action item for storage."""
        result = {**item}
        
        # Convert datetime objects to ISO strings
        for field in ["created_at", "updated_at", "completed_at"]:
            if field in result and result[field] is not None:
                if isinstance(result[field], datetime):
                    result[field] = result[field].isoformat()
        
        return result
    
    def _deserialize_item(self, data: Dict[str, Any]) -> ActionItem:
        """Deserialize an action item from storage."""
        # Parse datetime strings
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        updated_at = data.get("updated_at")
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)
        
        completed_at = data.get("completed_at")
        if isinstance(completed_at, str):
            completed_at = datetime.fromisoformat(completed_at)
        
        return ActionItem(
            id=data["id"],
            title=data["title"],
            note_id=data.get("note_id"),
            created_at=created_at,
            updated_at=updated_at,
            completed_at=completed_at,
            completed=data.get("completed", False),
        )
    
    def create_action_item(self, item_data: ActionItemCreate) -> ActionItem:
        """
        Create a new action item.
        
        Args:
            item_data: Action item creation data
            
        Returns:
            The created action item with generated ID and timestamps
        """
        self._ensure_loaded()
        
        now = datetime.now()
        item_id = str(uuid.uuid4())
        
        item = ActionItem(
            id=item_id,
            title=item_data.title,
            note_id=item_data.note_id,
            created_at=now,
            completed=False,
        )
        
        self._items[item_id] = self._serialize_item(item.model_dump())
        self._save_to_disk()
        
        return item
    
    def create_action_items_batch(
        self, 
        items_data: List[ActionItemCreate],
        note_id: Optional[str] = None
    ) -> List[ActionItem]:
        """
        Create multiple action items at once.
        
        Args:
            items_data: List of action item creation data
            note_id: Optional note ID to associate with all items
            
        Returns:
            List of created action items
        """
        self._ensure_loaded()
        
        now = datetime.now()
        created_items: List[ActionItem] = []
        
        for item_data in items_data:
            item_id = str(uuid.uuid4())
            
            item = ActionItem(
                id=item_id,
                title=item_data.title,
                note_id=note_id or item_data.note_id,
                created_at=now,
                completed=False,
            )
            
            self._items[item_id] = self._serialize_item(item.model_dump())
            created_items.append(item)
        
        self._save_to_disk()
        return created_items
    
    def get_action_item(self, item_id: str) -> Optional[ActionItem]:
        """
        Get an action item by ID.
        
        Args:
            item_id: The action item's unique identifier
            
        Returns:
            The action item if found, None otherwise
        """
        self._ensure_loaded()
        
        item_data = self._items.get(item_id)
        if not item_data:
            return None
        
        return self._deserialize_item(item_data)
    
    def get_all_action_items(self) -> List[ActionItem]:
        """
        Get all action items.
        
        Returns:
            List of all action items, sorted by created_at descending
        """
        self._ensure_loaded()
        
        items = [self._deserialize_item(data) for data in self._items.values()]
        items.sort(key=lambda i: i.created_at, reverse=True)
        return items
    
    def get_action_items_by_note(self, note_id: str) -> List[ActionItem]:
        """
        Get all action items for a specific note.
        
        Args:
            note_id: The note's unique identifier
            
        Returns:
            List of action items associated with the note
        """
        self._ensure_loaded()
        
        items = [
            self._deserialize_item(data)
            for data in self._items.values()
            if data.get("note_id") == note_id
        ]
        items.sort(key=lambda i: i.created_at)
        return items
    
    def get_incomplete_action_items(self, limit: Optional[int] = None) -> List[ActionItem]:
        """
        Get incomplete action items, ordered by oldest first.
        
        Args:
            limit: Optional limit on number of items to return
            
        Returns:
            List of incomplete action items
        """
        self._ensure_loaded()
        
        items = [
            self._deserialize_item(data)
            for data in self._items.values()
            if not data.get("completed", False)
        ]
        
        # Sort by created_at ascending (oldest first)
        items.sort(key=lambda i: i.created_at)
        
        if limit:
            items = items[:limit]
        
        return items
    
    def update_action_item(
        self, 
        item_id: str, 
        update_data: ActionItemUpdate
    ) -> Optional[ActionItem]:
        """
        Update an existing action item.
        
        Args:
            item_id: The action item's unique identifier
            update_data: Fields to update
            
        Returns:
            The updated action item if found, None otherwise
        """
        self._ensure_loaded()
        
        if item_id not in self._items:
            return None
        
        existing = self._items[item_id]
        now = datetime.now()
        
        # Update fields
        if update_data.title is not None:
            existing["title"] = update_data.title
        
        if update_data.completed is not None:
            existing["completed"] = update_data.completed
            if update_data.completed:
                existing["completed_at"] = now.isoformat()
            else:
                existing["completed_at"] = None
        
        existing["updated_at"] = now.isoformat()
        
        self._save_to_disk()
        return self._deserialize_item(existing)
    
    def complete_action_item(self, item_id: str) -> Optional[ActionItem]:
        """
        Mark an action item as complete.
        
        Args:
            item_id: The action item's unique identifier
            
        Returns:
            The updated action item if found, None otherwise
        """
        return self.update_action_item(
            item_id, 
            ActionItemUpdate(completed=True)
        )
    
    def uncomplete_action_item(self, item_id: str) -> Optional[ActionItem]:
        """
        Mark an action item as incomplete.
        
        Args:
            item_id: The action item's unique identifier
            
        Returns:
            The updated action item if found, None otherwise
        """
        return self.update_action_item(
            item_id,
            ActionItemUpdate(completed=False)
        )
    
    def delete_action_item(self, item_id: str) -> bool:
        """
        Delete an action item.
        
        Args:
            item_id: The action item's unique identifier
            
        Returns:
            True if item was deleted, False if not found
        """
        self._ensure_loaded()
        
        if item_id not in self._items:
            return False
        
        del self._items[item_id]
        self._save_to_disk()
        return True
    
    def delete_action_items_by_note(self, note_id: str) -> int:
        """
        Delete all action items associated with a note.
        
        Args:
            note_id: The note's unique identifier
            
        Returns:
            Number of items deleted
        """
        self._ensure_loaded()
        
        to_delete = [
            item_id
            for item_id, data in self._items.items()
            if data.get("note_id") == note_id
        ]
        
        for item_id in to_delete:
            del self._items[item_id]
        
        if to_delete:
            self._save_to_disk()
        
        return len(to_delete)
    
    def get_action_items_by_ids(self, item_ids: List[str]) -> List[ActionItem]:
        """
        Get action items by a list of IDs.
        
        Args:
            item_ids: List of action item IDs
            
        Returns:
            List of found action items (in order of IDs)
        """
        self._ensure_loaded()
        
        items: List[ActionItem] = []
        for item_id in item_ids:
            item_data = self._items.get(item_id)
            if item_data:
                items.append(self._deserialize_item(item_data))
        
        return items


# Singleton instance
_action_items_manager: Optional[ActionItemsManager] = None


def get_action_items_manager() -> ActionItemsManager:
    """Get the singleton ActionItemsManager instance."""
    global _action_items_manager
    if _action_items_manager is None:
        _action_items_manager = ActionItemsManager()
    return _action_items_manager
