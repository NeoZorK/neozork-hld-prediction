# src/cache_manager/__init__.py

"""
Makes cache management functions available for import.
"""

# Expose functions from the cache_manager module
from .cache_manager import (
    find_cached_files,
    load_cached_file,
    display_cached_files_info,
    parse_filename, # Expose if needed elsewhere, otherwise optional
    get_file_metadata # Expose if needed elsewhere, otherwise optional
)

# You can define __all__ to control what `from src.cache_manager import *` imports
__all__ = [
    'find_cached_files',
    'load_cached_file',
    'display_cached_files_info',
    'parse_filename',
    'get_file_metadata'
]

