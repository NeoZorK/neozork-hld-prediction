"""
Base CLI Parser Components

This module provides base classes for argument parsing.
"""

import argparse
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

from ...core.base import BaseComponent
from ...core.exceptions import CLIError, ValidationError


class BaseParser(BaseComponent, ABC):
    """
    Base class for CLI argument parsers.
    """
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """
        Initialize parser.
        
        Args:
            name: Parser name
            config: Configuration dictionary
        """
        super().__init__(name, config or {})
        self.parser = None
    
    @abstractmethod
    def create_parser(self) -> argparse.ArgumentParser:
        """
        Create argument parser.
        
        Returns:
            Configured argument parser
        """
        pass
    
    def parse_args(self, args: Optional[List[str]] = None) -> argparse.Namespace:
        """
        Parse command-line arguments.
        
        Args:
            args: Arguments to parse (uses sys.argv if None)
            
        Returns:
            Parsed arguments namespace
        """
        if self.parser is None:
            self.parser = self.create_parser()
        
        try:
            parsed_args = self.parser.parse_args(args)
            self.validate_parsed_args(parsed_args)
            return parsed_args
        except SystemExit as e:
            # argparse calls sys.exit on error
            if e.code != 0:
                raise CLIError(f"Argument parsing failed with code {e.code}")
            raise
        except Exception as e:
            raise CLIError(f"Argument parsing failed: {e}")
    
    def validate_parsed_args(self, args: argparse.Namespace) -> None:
        """
        Validate parsed arguments.
        
        Args:
            args: Parsed arguments to validate
        """
        # Default implementation - override in subclasses
        pass


__all__ = ["BaseParser"]
