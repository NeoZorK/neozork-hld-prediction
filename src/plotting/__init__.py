# src/plotting/__init__.py

"""
Exposes the main plot generation function.
"""

# Import from the module that contains the primary plotting entry point
from .plotting_generation import generate_plot

__all__ = [
    'generate_plot'
]
