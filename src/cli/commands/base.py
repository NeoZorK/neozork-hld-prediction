"""
Base CLI Command Components

This module provides base classes for CLI commands.
"""

import argparse
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

from ...core.base import BaseComponent
from ...core.exceptions import CLIError


class BaseCommand(BaseComponent, ABC):
    """
    Base class for CLI commands.
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize command.
        
        Args:
            name: Command name
            config: Configuration dictionary
        """
        super().__init__(name, config or {})
        self.description = ""
        self.parser = None
    
    @abstractmethod
    def setup_parser(self, parser: argparse.ArgumentParser) -> None:
        """
        Setup command-specific arguments.
        
        Args:
            parser: Argument parser to configure
        """
        pass
    
    @abstractmethod
    def execute(self, args: argparse.Namespace) -> Any:
        """
        Execute the command.
        
        Args:
            args: Parsed command arguments
            
        Returns:
            Command execution result
        """
        pass
    
    def validate_args(self, args: argparse.Namespace) -> None:
        """
        Validate command arguments.
        
        Args:
            args: Parsed command arguments
        """
        # Default implementation - override in subclasses
        pass


__all__ = ["BaseCommand"]
