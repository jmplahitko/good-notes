from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query

from ..models.action_item import ActionItem, ActionItemCreate, ActionItemUpdate
from ..services.action_items_manager import get_action_items_manager


router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("", response_model=ActionItem)
async def create_action_item(item_data: ActionItemCreate) -> ActionItem:
    """Create a new action item."""
    manager = get_action_items_manager()
    return manager.create_action_item(item_data)


@router.get("", response_model=List[ActionItem])
async def get_action_items(
    note_id: Optional[str] = Query(None, description="Filter by note ID"),
    incomplete_only: bool = Query(False, description="Only return incomplete items"),
    limit: Optional[int] = Query(None, description="Limit number of results"),
) -> List[ActionItem]:
    """
    Get all action items with optional filters.
    """
    manager = get_action_items_manager()
    
    if note_id:
        items = manager.get_action_items_by_note(note_id)
    elif incomplete_only:
        items = manager.get_incomplete_action_items(limit=limit)
    else:
        items = manager.get_all_action_items()
        if limit:
            items = items[:limit]
    
    return items


@router.get("/incomplete", response_model=List[ActionItem])
async def get_incomplete_action_items(
    limit: int = Query(5, description="Number of items to return"),
) -> List[ActionItem]:
    """
    Get oldest incomplete action items.
    
    Default returns 5 oldest incomplete items for the home page.
    """
    manager = get_action_items_manager()
    return manager.get_incomplete_action_items(limit=limit)


@router.get("/{item_id}", response_model=ActionItem)
async def get_action_item(item_id: str) -> ActionItem:
    """Get a specific action item by ID."""
    manager = get_action_items_manager()
    item = manager.get_action_item(item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    
    return item


@router.put("/{item_id}", response_model=ActionItem)
async def update_action_item(item_id: str, update_data: ActionItemUpdate) -> ActionItem:
    """
    Update an existing action item.
    
    Only provided fields will be updated.
    """
    manager = get_action_items_manager()
    item = manager.update_action_item(item_id, update_data)
    
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    
    return item


@router.post("/{item_id}/complete", response_model=ActionItem)
async def complete_action_item(item_id: str) -> ActionItem:
    """Mark an action item as complete."""
    manager = get_action_items_manager()
    item = manager.complete_action_item(item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    
    return item


@router.post("/{item_id}/uncomplete", response_model=ActionItem)
async def uncomplete_action_item(item_id: str) -> ActionItem:
    """Mark an action item as incomplete."""
    manager = get_action_items_manager()
    item = manager.uncomplete_action_item(item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    
    return item


@router.delete("/{item_id}")
async def delete_action_item(item_id: str) -> Dict[str, str]:
    """Delete an action item."""
    manager = get_action_items_manager()
    deleted = manager.delete_action_item(item_id)
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Action item not found")
    
    return {"message": "Action item deleted successfully"}
