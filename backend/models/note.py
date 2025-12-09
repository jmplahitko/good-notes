from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from .action_item import ActionItem, ActionItemCreate


class NoteBase(BaseModel):
    """Base note model with shared fields."""
    title: str = Field(..., min_length=1, description="Note title")
    attendees: Optional[List[str]] = Field(default=None, description="List of attendees")
    meeting_start_time: Optional[datetime] = Field(default=None, description="Meeting start time")
    content: str = Field(default="", description="Note content in markdown format")


class NoteCreate(NoteBase):
    """Model for creating a new note."""
    action_items: Optional[List[ActionItemCreate]] = Field(default=None, description="Action items to create with the note")


class NoteUpdate(BaseModel):
    """Model for updating an existing note."""
    title: Optional[str] = Field(default=None, min_length=1, description="Note title")
    attendees: Optional[List[str]] = Field(default=None, description="List of attendees")
    meeting_start_time: Optional[datetime] = Field(default=None, description="Meeting start time")
    content: Optional[str] = Field(default=None, description="Note content in markdown format")
    action_items: Optional[List[ActionItemCreate]] = Field(default=None, description="Action items")


class Note(NoteBase):
    """Complete note model with all fields including system-generated ones."""
    id: str = Field(..., description="Unique note identifier")
    created_at: datetime = Field(..., description="Timestamp when note was created")
    updated_at: Optional[datetime] = Field(default=None, description="Timestamp when note was last updated")
    action_items: List[ActionItem] = Field(default_factory=list, description="Action items associated with the note")

    class Config:
        from_attributes = True
