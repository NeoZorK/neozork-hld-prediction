"""
Base CLI Formatter Components

This module provides base classes for output formatting.
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

from ...core.base import BaseComponent
from ...core.exceptions import CLIError


class BaseFormatter(BaseComponent, ABC):
    """
    Base class for CLI output formatters.
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize formatter.
        
        Args:
            name: Formatter name
            config: Configuration dictionary
        """
        super().__init__(name, config or {})
        self.indent_size = config.get("indent_size", 2) if config else 2
        self.max_width = config.get("max_width", 80) if config else 80
    
    @abstractmethod
    def format(self, data: Any) -> str:
        """
        Format data for output.
        
        Args:
            data: Data to format
            
        Returns:
            Formatted string
        """
        pass
    
    def format_error(self, error: Exception) -> str:
        """
        Format error message.
        
        Args:
            error: Error to format
            
        Returns:
            Formatted error string
        """
        return f"Error: {error}"
    
    def format_success(self, message: str) -> str:
        """
        Format success message.
        
        Args:
            message: Success message
            
        Returns:
            Formatted success string
        """
        return f"✓ {message}"
    
    def format_warning(self, message: str) -> str:
        """
        Format warning message.
        
        Args:
            message: Warning message
            
        Returns:
            Formatted warning string
        """
        return f"⚠ {message}"


class SimpleFormatter(BaseFormatter):
    """
    Simple text formatter.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize simple formatter.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("simple_formatter", config)
    
    def format(self, data: Any) -> str:
        """
        Format data as simple string.
        
        Args:
            data: Data to format
            
        Returns:
            Formatted string
        """
        if isinstance(data, dict):
            return self._format_dict(data)
        elif isinstance(data, list):
            return self._format_list(data)
        else:
            return str(data)
    
    def _format_dict(self, data: dict, indent: int = 0) -> str:
        """Format dictionary data."""
        lines = []
        prefix = " " * (indent * self.indent_size)
        
        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(self._format_dict(value, indent + 1))
            else:
                lines.append(f"{prefix}{key}: {value}")
        
        return "\n".join(lines)
    
    def _format_list(self, data: list) -> str:
        """Format list data."""
        return "\n".join(f"- {item}" for item in data)


__all__ = ["BaseFormatter", "SimpleFormatter"]
