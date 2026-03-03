import os
from pathlib import Path
from typing import Optional

# Base upload directory (relative to project root)
BASE_UPLOAD_DIR = Path(__file__).parent.parent.parent.parent / "uploaded_files"


def ensure_upload_dir(upload_dir: Optional[Path] = None) -> Path:
    """
    Ensure the upload directory exists. Creates it if it doesn't.
    
    Args:
        upload_dir: Optional custom upload directory path. Defaults to BASE_UPLOAD_DIR.
    
    Returns:
        Path: The upload directory path.
    """
    dir_path = upload_dir or BASE_UPLOAD_DIR
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def validate_pdf(filename: str) -> bool:
    """
    Validate that a file is a PDF.
    
    Args:
        filename: The filename to validate.
    
    Returns:
        bool: True if the file ends with .pdf (case-insensitive), False otherwise.
    """
    return filename.lower().endswith(".pdf")


def validate_file_size(file_size: int, max_size_mb: int = 25) -> bool:
    """
    Validate that a file size is within acceptable limits.
    
    Args:
        file_size: Size of the file in bytes.
        max_size_mb: Maximum allowed file size in MB (default: 25MB).
    
    Returns:
        bool: True if file size is acceptable, False otherwise.
    """
    max_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_bytes


def clear_upload_dir(upload_dir: Optional[Path] = None) -> int:
    """
    Clear all files in the upload directory.
    
    Args:
        upload_dir: Optional custom upload directory path. Defaults to BASE_UPLOAD_DIR.
    
    Returns:
        int: Number of files deleted.
    """
    dir_path = upload_dir or BASE_UPLOAD_DIR
    
    if not dir_path.exists():
        return 0
    
    deleted_count = 0
    for file_path in dir_path.iterdir():
        if file_path.is_file():
            file_path.unlink()
            deleted_count += 1
    
    return deleted_count


def file_exists(filename: str, upload_dir: Optional[Path] = None) -> bool:
    """
    Check if a file already exists in the upload directory.
    
    Args:
        filename: The filename to check.
        upload_dir: Optional custom upload directory path. Defaults to BASE_UPLOAD_DIR.
    
    Returns:
        bool: True if the file exists, False otherwise.
    """
    dir_path = upload_dir or BASE_UPLOAD_DIR
    file_path = dir_path / filename
    return file_path.exists()


def get_file_path(filename: str, upload_dir: Optional[Path] = None) -> Path:
    """
    Get the full path for a file in the upload directory.
    
    Args:
        filename: The filename.
        upload_dir: Optional custom upload directory path. Defaults to BASE_UPLOAD_DIR.
    
    Returns:
        Path: The full file path.
    """
    dir_path = upload_dir or BASE_UPLOAD_DIR
    return dir_path / filename


def save_file(content: bytes, filename: str, upload_dir: Optional[Path] = None) -> Path:
    """
    Save file content to the upload directory.
    
    Args:
        content: The file content as bytes.
        filename: The filename to save as.
        upload_dir: Optional custom upload directory path. Defaults to BASE_UPLOAD_DIR.
    
    Returns:
        Path: The path where the file was saved.
    
    Raises:
        ValueError: If the file already exists.
    """
    dir_path = ensure_upload_dir(upload_dir)
    file_path = dir_path / filename
    
    if file_path.exists():
        raise ValueError(f"File '{filename}' already exists in upload directory.")
    
    file_path.write_bytes(content)
    return file_path


def delete_file(filename: str, upload_dir: Optional[Path] = None) -> bool:
    """
    Delete a file from the upload directory.
    
    Args:
        filename: The filename to delete.
        upload_dir: Optional custom upload directory path. Defaults to BASE_UPLOAD_DIR.
    
    Returns:
        bool: True if the file was deleted, False if it didn't exist.
    """
    dir_path = upload_dir or BASE_UPLOAD_DIR
    file_path = dir_path / filename
    
    if file_path.exists():
        file_path.unlink()
        return True
    
    return False
