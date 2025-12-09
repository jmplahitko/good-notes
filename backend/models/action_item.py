from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ActionItemBase(BaseModel):
    """Base action item model with shared fields."""
    title: str = Field(..., min_length=1, description="Action item title/description")


class ActionItemCreate(ActionItemBase):
    """Model for creating a new action item."""
    note_id: Optional[str] = Field(default=None, description="ID of the associated note")


class ActionItemUpdate(BaseModel):
    """Model for updating an existing action item."""
    title: Optional[str] = Field(default=None, min_length=1, description="Action item title/description")
    completed: Optional[bool] = Field(default=None, description="Whether the action item is completed")


class ActionItem(ActionItemBase):
    """Complete action item model with all fields."""
    id: str = Field(..., description="Unique action item identifier")
    note_id: Optional[str] = Field(default=None, description="ID of the associated note")
    created_at: datetime = Field(..., description="Timestamp when action item was created")
    updated_at: Optional[datetime] = Field(default=None, description="Timestamp when action item was last updated")
    completed_at: Optional[datetime] = Field(default=None, description="Timestamp when action item was completed")
    completed: bool = Field(default=False, description="Whether the action item is completed")

    class Config:
        from_attributes = True

