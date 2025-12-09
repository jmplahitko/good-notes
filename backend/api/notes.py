from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query

from ..models.note import Note, NoteCreate, NoteUpdate
from ..models.action_item import ActionItemCreate
from ..services.notes_manager import get_notes_manager
from ..services.action_items_manager import get_action_items_manager


router = APIRouter(prefix="/notes", tags=["notes"])


def _populate_action_items(note: Note) -> Note:
    """Populate a note with its associated action items."""
    action_items_manager = get_action_items_manager()
    
    # Get action item IDs from the note
    notes_manager = get_notes_manager()
    action_item_ids = notes_manager.get_action_item_ids(note.id)
    
    if action_item_ids:
        action_items = action_items_manager.get_action_items_by_ids(action_item_ids)
    else:
        # Fallback: get action items by note_id
        action_items = action_items_manager.get_action_items_by_note(note.id)
    
    # Create a new note with populated action items
    return Note(
        id=note.id,
        title=note.title,
        content=note.content,
        attendees=note.attendees,
        meeting_start_time=note.meeting_start_time,
        created_at=note.created_at,
        updated_at=note.updated_at,
        action_items=action_items,
    )


@router.post("", response_model=Note)
async def create_note(note_data: NoteCreate) -> Note:
    """
    Create a new note.
    
    The note will be saved as a markdown file in the notes directory,
    organized by creation date (YYYYMMDD subdirectory).
    """
    notes_manager = get_notes_manager()
    action_items_manager = get_action_items_manager()
    
    # First create the note to get its ID
    note = notes_manager.create_note(note_data)
    
    # Create action items if provided
    created_action_items = []
    if note_data.action_items:
        created_action_items = action_items_manager.create_action_items_batch(
            note_data.action_items,
            note_id=note.id
        )
    
    # Update the note with action item IDs
    if created_action_items:
        note = notes_manager.update_note(
            note.id,
            NoteUpdate(),  # No field updates, just re-save with action items
            action_items=created_action_items
        )
    
    return _populate_action_items(note)


@router.get("", response_model=List[Note])
async def get_notes(
    date: Optional[str] = Query(None, description="Filter by date (YYYY-MM-DD)"),
) -> List[Note]:
    """
    Get all notes, optionally filtered by date.
    """
    notes_manager = get_notes_manager()
    
    if date:
        try:
            filter_date = datetime.strptime(date, "%Y-%m-%d")
            notes = notes_manager.get_notes_by_date(filter_date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid date format. Use YYYY-MM-DD"
            )
    else:
        notes = notes_manager.get_all_notes()
    
    return [_populate_action_items(note) for note in notes]


@router.get("/today", response_model=List[Note])
async def get_todays_notes() -> List[Note]:
    """Get notes created today."""
    notes_manager = get_notes_manager()
    today = datetime.now()
    notes = notes_manager.get_notes_by_date(today)
    return [_populate_action_items(note) for note in notes]


@router.get("/yesterday", response_model=List[Note])
async def get_yesterdays_notes() -> List[Note]:
    """Get notes created yesterday."""
    notes_manager = get_notes_manager()
    yesterday = datetime.now() - timedelta(days=1)
    notes = notes_manager.get_notes_by_date(yesterday)
    return [_populate_action_items(note) for note in notes]


@router.get("/{note_id}", response_model=Note)
async def get_note(note_id: str) -> Note:
    """Get a specific note by ID."""
    notes_manager = get_notes_manager()
    note = notes_manager.get_note(note_id)
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return _populate_action_items(note)


@router.put("/{note_id}", response_model=Note)
async def update_note(note_id: str, update_data: NoteUpdate) -> Note:
    """
    Update an existing note.
    
    Only provided fields will be updated.
    """
    notes_manager = get_notes_manager()
    action_items_manager = get_action_items_manager()
    
    # Get existing action items
    existing_action_items = action_items_manager.get_action_items_by_note(note_id)
    
    # Handle action items update
    action_items = existing_action_items
    if update_data.action_items is not None:
        # Delete existing action items and create new ones
        action_items_manager.delete_action_items_by_note(note_id)
        action_items = action_items_manager.create_action_items_batch(
            update_data.action_items,
            note_id=note_id
        )
    
    note = notes_manager.update_note(note_id, update_data, action_items=action_items)
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return _populate_action_items(note)


@router.delete("/{note_id}")
async def delete_note(note_id: str) -> Dict[str, str]:
    """Delete a note and its associated action items."""
    notes_manager = get_notes_manager()
    action_items_manager = get_action_items_manager()
    
    # Delete associated action items first
    action_items_manager.delete_action_items_by_note(note_id)
    
    # Delete the note
    deleted = notes_manager.delete_note(note_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {"message": "Note deleted successfully"}
