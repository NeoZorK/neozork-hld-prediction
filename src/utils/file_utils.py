"""
File Utilities

This module provides file operation utilities.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

from ..core.exceptions import FileError


logger = logging.getLogger(__name__)


def ensure_directory(path: str) -> None:
    """
    Ensure directory exists, create if necessary.
    
    Args:
        path: Directory path
    """
    try:
        Path(path).mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory exists: {path}")
    except Exception as e:
        raise FileError(f"Failed to create directory {path}: {e}")


def file_exists(path: str) -> bool:
    """
    Check if file exists.
    
    Args:
        path: File path
        
    Returns:
        True if file exists, False otherwise
    """
    return Path(path).exists()


def get_file_size(path: str) -> int:
    """
    Get file size in bytes.
    
    Args:
        path: File path
        
    Returns:
        File size in bytes
    """
    try:
        return Path(path).stat().st_size
    except Exception as e:
        raise FileError(f"Failed to get file size for {path}: {e}")


def copy_file(source: str, destination: str) -> None:
    """
    Copy file from source to destination.
    
    Args:
        source: Source file path
        destination: Destination file path
    """
    try:
        ensure_directory(str(Path(destination).parent))
        shutil.copy2(source, destination)
        logger.debug(f"Copied file from {source} to {destination}")
    except Exception as e:
        raise FileError(f"Failed to copy file: {e}")


def delete_file(path: str) -> None:
    """
    Delete file if it exists.
    
    Args:
        path: File path
    """
    try:
        if file_exists(path):
            Path(path).unlink()
            logger.debug(f"Deleted file: {path}")
    except Exception as e:
        raise FileError(f"Failed to delete file {path}: {e}")


def get_file_extension(path: str) -> str:
    """
    Get file extension.
    
    Args:
        path: File path
        
    Returns:
        File extension (without dot)
    """
    return Path(path).suffix.lstrip('.')


def list_files(directory: str, pattern: str = "*") -> List[str]:
    """
    List files in directory matching pattern.
    
    Args:
        directory: Directory path
        pattern: File pattern (default: all files)
        
    Returns:
        List of file paths
    """
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return []
        
        files = [str(f) for f in dir_path.glob(pattern) if f.is_file()]
        logger.debug(f"Found {len(files)} files in {directory}")
        return files
        
    except Exception as e:
        raise FileError(f"Failed to list files in {directory}: {e}")


__all__ = [
    "ensure_directory",
    "file_exists",
    "get_file_size",
    "copy_file",
    "delete_file",
    "get_file_extension",
    "list_files",
]
