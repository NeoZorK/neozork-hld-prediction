"""
Command Manager for CLI

This module provides command management functionality.
"""

from typing import Dict, Any, Callable, Optional, List
import logging

from ...core.base import BaseComponent
from ...core.exceptions import CLIError


class CommandManager(BaseComponent):
    """
    Manager for CLI commands.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize command manager.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("command_manager", config or {})
        self.commands: Dict[str, Callable] = {}
        self.command_help: Dict[str, str] = {}
    
    def register_command(self, name: str, handler: Callable, help_text: str = "") -> None:
        """
        Register a command handler.
        
        Args:
            name: Command name
            handler: Command handler function
            help_text: Help text for the command
        """
        self.commands[name] = handler
        self.command_help[name] = help_text
        self.logger.debug(f"Registered command: {name}")
    
    def execute_command(self, name: str, args: Dict[str, Any]) -> Any:
        """
        Execute a registered command.
        
        Args:
            name: Command name
            args: Command arguments
            
        Returns:
            Command execution result
        """
        if name not in self.commands:
            available = ", ".join(self.commands.keys())
            raise CLIError(f"Unknown command '{name}'. Available commands: {available}")
        
        try:
            handler = self.commands[name]
            self.logger.info(f"Executing command: {name}")
            result = handler(args)
            self.logger.debug(f"Command {name} completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Command {name} failed: {e}")
            raise CLIError(f"Command execution failed: {e}")
    
    def get_available_commands(self) -> List[str]:
        """
        Get list of available commands.
        
        Returns:
            List of command names
        """
        return list(self.commands.keys())
    
    def get_command_help(self, name: str) -> str:
        """
        Get help text for a command.
        
        Args:
            name: Command name
            
        Returns:
            Help text for the command
        """
        return self.command_help.get(name, "No help available")


__all__ = ["CommandManager"]
