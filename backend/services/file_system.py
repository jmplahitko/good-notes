import os
from pathlib import Path
from typing import Generator


def read_file(path: Path) -> str:
    """
    Read content from a file.
    
    Args:
        path: Path to the file
        
    Returns:
        File content as string
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_file(path: Path, content: str) -> None:
    """
    Write content to a file, creating parent directories if needed.
    
    Args:
        path: Path to the file
        content: Content to write
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def delete_file(path: Path) -> bool:
    """
    Delete a file if it exists.
    
    Args:
        path: Path to the file
        
    Returns:
        True if file was deleted, False if it didn't exist
    """
    try:
        path.unlink()
        return True
    except FileNotFoundError:
        return False


def file_exists(path: Path) -> bool:
    """
    Check if a file exists.
    
    Args:
        path: Path to the file
        
    Returns:
        True if file exists
    """
    return path.is_file()


def directory_exists(path: Path) -> bool:
    """
    Check if a directory exists.
    
    Args:
        path: Path to the directory
        
    Returns:
        True if directory exists
    """
    return path.is_dir()


def ensure_directory(path: Path) -> None:
    """
    Create a directory if it doesn't exist.
    
    Args:
        path: Path to the directory
    """
    path.mkdir(parents=True, exist_ok=True)


def list_markdown_files(directory: Path, recursive: bool = True) -> Generator[Path, None, None]:
    """
    List all markdown files in a directory.
    
    Args:
        directory: Directory to search
        recursive: Whether to search subdirectories
        
    Yields:
        Paths to markdown files
    """
    if not directory.exists():
        return
    
    if recursive:
        for path in directory.rglob("*.md"):
            yield path
    else:
        for path in directory.glob("*.md"):
            yield path


def list_subdirectories(directory: Path) -> Generator[Path, None, None]:
    """
    List all subdirectories in a directory.
    
    Args:
        directory: Directory to list
        
    Yields:
        Paths to subdirectories
    """
    if not directory.exists():
        return
    
    for path in directory.iterdir():
        if path.is_dir():
            yield path


def rename_file(old_path: Path, new_path: Path) -> None:
    """
    Rename/move a file.
    
    Args:
        old_path: Current path
        new_path: New path
    """
    new_path.parent.mkdir(parents=True, exist_ok=True)
    old_path.rename(new_path)


def get_file_modification_time(path: Path) -> float:
    """
    Get the modification time of a file.
    
    Args:
        path: Path to the file
        
    Returns:
        Modification time as Unix timestamp
    """
    return path.stat().st_mtime

