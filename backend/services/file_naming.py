from datetime import datetime
from typing import Optional
from slugify import slugify


def generate_note_filename(title: str, meeting_start_time: Optional[datetime] = None) -> str:
    """
    Generate a filename for a note based on title and optional meeting start time.
    
    Format: slugified-title-HHMM.md (with meeting time) or slugified-title.md (without)
    
    Args:
        title: The note title to slugify
        meeting_start_time: Optional meeting start time to append
        
    Returns:
        Generated filename with .md extension
    """
    # Slugify the title
    slug = slugify(title, max_length=50, word_boundary=True)
    
    # Ensure we have a valid slug
    if not slug:
        slug = "untitled"
    
    # Append meeting time if provided
    if meeting_start_time:
        time_suffix = meeting_start_time.strftime("%H%M")
        filename = f"{slug}-{time_suffix}.md"
    else:
        filename = f"{slug}.md"
    
    return filename


def generate_date_directory(created_at: datetime) -> str:
    """
    Generate a date-based directory name for note storage.
    
    Format: YYYYMMDD
    
    Args:
        created_at: The note creation timestamp
        
    Returns:
        Directory name in YYYYMMDD format
    """
    return created_at.strftime("%Y%m%d")


def generate_note_id(title: str, created_at: datetime) -> str:
    """
    Generate a unique ID for a note based on title and creation time.
    
    Format: YYYYMMDD-HHMMSS-slugified-title
    
    Args:
        title: The note title
        created_at: The note creation timestamp
        
    Returns:
        Unique note identifier
    """
    slug = slugify(title, max_length=30, word_boundary=True)
    if not slug:
        slug = "untitled"
    
    timestamp = created_at.strftime("%Y%m%d-%H%M%S")
    return f"{timestamp}-{slug}"
