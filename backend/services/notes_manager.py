from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import yaml

from ..config import get_config
from ..models.note import Note, NoteCreate, NoteUpdate
from ..models.action_item import ActionItem
from . import file_system as fs
from . import markdown_converter as md
from . import file_naming as naming


class NotesManager:
    """
    Service for managing notes with markdown file storage.
    
    Notes are stored as markdown files in date-organized directories:
    - Base directory: ~/Documents/GoodNotes/notes/
    - Subdirectories: YYYYMMDD/ (based on created_at date)
    - Filenames: slugified-title-HHMM.md (with meeting time) or slugified-title.md
    
    The note index (ID -> file path mapping) is persisted to a YAML file
    for fast startup without needing to scan all markdown files.
    """
    
    def __init__(self):
        self.config = get_config()
        self.base_directory = self.config.notes_base_directory
        self.index_file = self.config.notes_index_file
        # In-memory index of note ID -> file path for fast lookups
        self._note_index: Dict[str, Path] = {}
        self._index_loaded = False
        self._index_dirty = False
    
    def _ensure_index_loaded(self) -> None:
        """Load the note index from disk if not already loaded."""
        if not self._index_loaded:
            self._load_index()
            self._index_loaded = True
    
    def _load_index(self) -> None:
        """
        Load the note index from the YAML file.
        
        If the index file doesn't exist or is invalid, rebuild from markdown files.
        """
        self._note_index.clear()
        
        if fs.file_exists(self.index_file):
            try:
                content = fs.read_file(self.index_file)
                data = yaml.safe_load(content)
                
                if isinstance(data, dict) and "notes" in data:
                    for note_id, path_str in data["notes"].items():
                        path = Path(path_str)
                        # Verify the file still exists
                        if fs.file_exists(path):
                            self._note_index[note_id] = path
                    
                    # If we loaded successfully, we're done
                    if self._note_index:
                        return
            except Exception:
                # Fall through to rebuild
                pass
        
        # Index file doesn't exist or is invalid - rebuild from markdown files
        self._rebuild_index()
    
    def _rebuild_index(self) -> None:
        """Rebuild the in-memory index by scanning all markdown files."""
        self._note_index.clear()
        
        for md_path in fs.list_markdown_files(self.base_directory):
            try:
                content = fs.read_file(md_path)
                note_data = md.markdown_to_note(content)
                if note_data.get("id"):
                    self._note_index[note_data["id"]] = md_path
            except Exception:
                # Skip files that can't be parsed
                continue
        
        # Save the rebuilt index
        self._save_index()
    
    def _save_index(self) -> None:
        """Save the note index to the YAML file."""
        # Convert Path objects to strings for YAML serialization
        data = {
            "notes": {
                note_id: str(path) 
                for note_id, path in self._note_index.items()
            },
            "updated_at": datetime.now().isoformat(),
        }
        
        content = yaml.dump(data, default_flow_style=False, allow_unicode=True)
        fs.write_file(self.index_file, content)
        self._index_dirty = False
    
    def _mark_index_dirty(self) -> None:
        """Mark the index as needing to be saved."""
        self._index_dirty = True
        # Auto-save immediately for data integrity
        self._save_index()
    
    def _get_note_path(self, note_id: str) -> Optional[Path]:
        """Get the file path for a note by ID."""
        self._ensure_index_loaded()
        return self._note_index.get(note_id)
    
    def _calculate_note_path(
        self, 
        title: str, 
        created_at: datetime,
        meeting_start_time: Optional[datetime] = None
    ) -> Path:
        """Calculate the file path for a new note."""
        date_dir = naming.generate_date_directory(created_at)
        filename = naming.generate_note_filename(title, meeting_start_time)
        return self.base_directory / date_dir / filename
    
    def create_note(
        self, 
        note_data: NoteCreate,
        action_items: Optional[List[ActionItem]] = None
    ) -> Note:
        """
        Create a new note and save it to disk.
        
        Args:
            note_data: Note creation data
            action_items: Optional list of already-created action items to associate
            
        Returns:
            The created note with generated ID and timestamps
        """
        self._ensure_index_loaded()
        now = datetime.now()
        
        # Generate note ID
        note_id = naming.generate_note_id(note_data.title, now)
        
        # Prepare action item IDs for markdown
        action_item_ids = [ai.id for ai in (action_items or [])]
        
        # Convert to markdown
        markdown_content = md.note_to_markdown(
            id=note_id,
            title=note_data.title,
            content=note_data.content,
            created_at=now,
            attendees=note_data.attendees,
            meeting_start_time=note_data.meeting_start_time,
            action_item_ids=action_item_ids if action_item_ids else None,
        )
        
        # Calculate file path and write
        file_path = self._calculate_note_path(
            note_data.title, 
            now, 
            note_data.meeting_start_time
        )
        fs.write_file(file_path, markdown_content)
        
        # Update and save index
        self._note_index[note_id] = file_path
        self._mark_index_dirty()
        
        # Return the created note
        return Note(
            id=note_id,
            title=note_data.title,
            content=note_data.content,
            attendees=note_data.attendees,
            meeting_start_time=note_data.meeting_start_time,
            created_at=now,
            action_items=action_items or [],
        )
    
    def get_note(self, note_id: str) -> Optional[Note]:
        """
        Get a note by ID.
        
        Args:
            note_id: The note's unique identifier
            
        Returns:
            The note if found, None otherwise
        """
        file_path = self._get_note_path(note_id)
        if not file_path or not fs.file_exists(file_path):
            return None
        
        try:
            content = fs.read_file(file_path)
            note_data = md.markdown_to_note(content)
            
            # Note: Action items will be fetched separately and injected by the API layer
            return Note(
                id=note_data["id"],
                title=note_data["title"],
                content=note_data["content"],
                attendees=note_data.get("attendees"),
                meeting_start_time=note_data.get("meeting_start_time"),
                created_at=note_data["created_at"],
                updated_at=note_data.get("updated_at"),
                action_items=[],  # Will be populated by API layer
            )
        except Exception:
            return None
    
    def get_all_notes(self) -> List[Note]:
        """
        Get all notes.
        
        Returns:
            List of all notes, sorted by created_at descending
        """
        self._ensure_index_loaded()
        notes: List[Note] = []
        
        for note_id in self._note_index:
            note = self.get_note(note_id)
            if note:
                notes.append(note)
        
        # Sort by created_at descending (newest first)
        notes.sort(key=lambda n: n.created_at, reverse=True)
        return notes
    
    def get_notes_by_date(self, date: datetime) -> List[Note]:
        """
        Get all notes for a specific date.
        
        Args:
            date: The date to filter by
            
        Returns:
            List of notes created on that date
        """
        date_str = naming.generate_date_directory(date)
        date_dir = self.base_directory / date_str
        
        if not fs.directory_exists(date_dir):
            return []
        
        notes: List[Note] = []
        for md_path in fs.list_markdown_files(date_dir, recursive=False):
            try:
                content = fs.read_file(md_path)
                note_data = md.markdown_to_note(content)
                note = Note(
                    id=note_data["id"],
                    title=note_data["title"],
                    content=note_data["content"],
                    attendees=note_data.get("attendees"),
                    meeting_start_time=note_data.get("meeting_start_time"),
                    created_at=note_data["created_at"],
                    updated_at=note_data.get("updated_at"),
                    action_items=[],
                )
                notes.append(note)
            except Exception:
                continue
        
        notes.sort(key=lambda n: n.created_at, reverse=True)
        return notes
    
    def update_note(
        self, 
        note_id: str, 
        update_data: NoteUpdate,
        action_items: Optional[List[ActionItem]] = None
    ) -> Optional[Note]:
        """
        Update an existing note.
        
        Args:
            note_id: The note's unique identifier
            update_data: Fields to update
            action_items: Optional list of action items to associate
            
        Returns:
            The updated note if found, None otherwise
        """
        existing_note = self.get_note(note_id)
        if not existing_note:
            return None
        
        old_path = self._get_note_path(note_id)
        now = datetime.now()
        
        # Merge updates with existing data
        title = update_data.title if update_data.title is not None else existing_note.title
        content = update_data.content if update_data.content is not None else existing_note.content
        attendees = update_data.attendees if update_data.attendees is not None else existing_note.attendees
        meeting_start_time = (
            update_data.meeting_start_time 
            if update_data.meeting_start_time is not None 
            else existing_note.meeting_start_time
        )
        
        # Prepare action item IDs
        action_item_ids = [ai.id for ai in (action_items or [])]
        
        # Convert to markdown
        markdown_content = md.note_to_markdown(
            id=note_id,
            title=title,
            content=content,
            created_at=existing_note.created_at,
            updated_at=now,
            attendees=attendees,
            meeting_start_time=meeting_start_time,
            action_item_ids=action_item_ids if action_item_ids else None,
        )
        
        # Calculate new path (might change if title changed)
        new_path = self._calculate_note_path(
            title,
            existing_note.created_at,
            meeting_start_time
        )
        
        # If path changed, delete old file
        if old_path and old_path != new_path:
            fs.delete_file(old_path)
        
        # Write updated file
        fs.write_file(new_path, markdown_content)
        
        # Update and save index
        self._note_index[note_id] = new_path
        self._mark_index_dirty()
        
        return Note(
            id=note_id,
            title=title,
            content=content,
            attendees=attendees,
            meeting_start_time=meeting_start_time,
            created_at=existing_note.created_at,
            updated_at=now,
            action_items=action_items or [],
        )
    
    def delete_note(self, note_id: str) -> bool:
        """
        Delete a note.
        
        Args:
            note_id: The note's unique identifier
            
        Returns:
            True if note was deleted, False if not found
        """
        file_path = self._get_note_path(note_id)
        if not file_path:
            return False
        
        deleted = fs.delete_file(file_path)
        if deleted:
            del self._note_index[note_id]
            self._mark_index_dirty()
        
        return deleted
    
    def get_action_item_ids(self, note_id: str) -> List[str]:
        """
        Get the action item IDs associated with a note.
        
        Args:
            note_id: The note's unique identifier
            
        Returns:
            List of action item IDs
        """
        file_path = self._get_note_path(note_id)
        if not file_path or not fs.file_exists(file_path):
            return []
        
        try:
            content = fs.read_file(file_path)
            note_data = md.markdown_to_note(content)
            return note_data.get("action_item_ids", [])
        except Exception:
            return []
    
    def rebuild_index_from_files(self) -> int:
        """
        Force rebuild the index by scanning all markdown files.
        
        Useful if the index gets out of sync with the actual files.
        
        Returns:
            Number of notes indexed
        """
        self._rebuild_index()
        self._index_loaded = True
        return len(self._note_index)


# Singleton instance
_notes_manager: Optional[NotesManager] = None


def get_notes_manager() -> NotesManager:
    """Get the singleton NotesManager instance."""
    global _notes_manager
    if _notes_manager is None:
        _notes_manager = NotesManager()
    return _notes_manager
