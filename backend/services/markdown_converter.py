from datetime import datetime
from typing import Any, Dict, List, Optional
import frontmatter


def note_to_markdown(
    id: str,
    title: str,
    content: str,
    created_at: datetime,
    updated_at: Optional[datetime] = None,
    attendees: Optional[List[str]] = None,
    meeting_start_time: Optional[datetime] = None,
    action_item_ids: Optional[List[str]] = None,
) -> str:
    """
    Convert note data to markdown format with frontmatter.
    
    Structure:
    - Frontmatter: id, created_at, updated_at, meeting_start_time, action_item_ids
    - h1: Title
    - h2 Attendees (optional): List of attendees
    - Content: Note content
    
    Args:
        id: Note unique identifier
        title: Note title
        content: Note content (markdown)
        created_at: Creation timestamp
        updated_at: Last update timestamp (optional)
        attendees: List of attendees (optional)
        meeting_start_time: Meeting start time (optional)
        action_item_ids: List of action item IDs associated with note
        
    Returns:
        Markdown string with frontmatter
    """
    # Build frontmatter metadata
    metadata: Dict[str, Any] = {
        "id": id,
        "created_at": created_at.isoformat(),
    }
    
    if updated_at:
        metadata["updated_at"] = updated_at.isoformat()
    
    if meeting_start_time:
        metadata["meeting_start_time"] = meeting_start_time.isoformat()
    
    if action_item_ids:
        metadata["action_item_ids"] = action_item_ids
    
    # Build content sections
    content_parts = []
    
    # Title as h1
    content_parts.append(f"# {title}")
    content_parts.append("")  # Empty line after title
    
    # Attendees section (optional, as h2 with bullet list)
    if attendees:
        content_parts.append("## Attendees")
        content_parts.append("")
        for attendee in attendees:
            content_parts.append(f"- {attendee}")
        content_parts.append("")  # Empty line after attendees
    
    # Main content
    if content:
        content_parts.append(content)
    
    # Create the markdown document
    markdown_content = "\n".join(content_parts)
    post = frontmatter.Post(markdown_content, **metadata)
    
    return frontmatter.dumps(post)


def markdown_to_note(markdown_text: str) -> Dict[str, Any]:
    """
    Parse markdown file content back to note data.
    
    Extracts:
    - Frontmatter metadata (id, timestamps, meeting_start_time, action_item_ids)
    - Title from h1 heading
    - Attendees from optional h2 Attendees section
    - Content (everything after title/attendees)
    
    Args:
        markdown_text: Raw markdown file content with frontmatter
        
    Returns:
        Dictionary with parsed note data
    """
    # Parse frontmatter and content
    post = frontmatter.loads(markdown_text)
    
    # Extract metadata
    metadata = dict(post.metadata)
    content = post.content
    
    # Parse the content to extract title, attendees, and body
    lines = content.split("\n")
    
    title = ""
    attendees: List[str] = []
    body_lines: List[str] = []
    
    in_attendees_section = False
    title_found = False
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Extract title from h1
        if not title_found and stripped.startswith("# "):
            title = stripped[2:].strip()
            title_found = True
            i += 1
            continue
        
        # Check for Attendees section
        if stripped.lower() == "## attendees":
            in_attendees_section = True
            i += 1
            continue
        
        # If in attendees section, collect bullet points
        if in_attendees_section:
            if stripped.startswith("- "):
                attendees.append(stripped[2:].strip())
                i += 1
                continue
            elif stripped.startswith("## ") or (stripped and not stripped.startswith("-")):
                # New section or non-list content, end attendees section
                in_attendees_section = False
                # Don't increment i, we want to process this line
            elif stripped == "":
                # Empty line in attendees section, skip it
                i += 1
                continue
            else:
                # End of attendees section
                in_attendees_section = False
        
        # Collect body content (after title and optional attendees)
        if title_found:
            body_lines.append(line)
        
        i += 1
    
    # Clean up body content - remove leading empty lines
    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)
    
    # Remove trailing empty lines
    while body_lines and not body_lines[-1].strip():
        body_lines.pop()
    
    body = "\n".join(body_lines)
    
    # Build the result
    result: Dict[str, Any] = {
        "id": metadata.get("id", ""),
        "title": title,
        "content": body,
        "attendees": attendees if attendees else None,
    }
    
    # Parse timestamps
    if "created_at" in metadata:
        result["created_at"] = datetime.fromisoformat(metadata["created_at"])
    
    if "updated_at" in metadata:
        result["updated_at"] = datetime.fromisoformat(metadata["updated_at"])
    
    if "meeting_start_time" in metadata:
        result["meeting_start_time"] = datetime.fromisoformat(metadata["meeting_start_time"])
    
    if "action_item_ids" in metadata:
        result["action_item_ids"] = metadata["action_item_ids"]
    
    return result
