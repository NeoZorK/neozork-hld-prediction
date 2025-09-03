"""
Unit tests for cli.core.command_manager module.
"""

import pytest
from unittest.mock import Mock

from src.cli.core.command_manager import CommandManager
from src.core.exceptions import CLIError


class TestCommandManager:
    """Test cases for CommandManager class."""
    
    def test_command_manager_initialization(self):
        """Test command manager initialization."""
        config = {"test": "value"}
        manager = CommandManager(config)
        
        assert manager.config == config
        assert isinstance(manager, CommandManager)
    
    def test_register_command(self):
        """Test command registration."""
        manager = CommandManager({})
        
        def test_handler():
            return "test_result"
        
        manager.register_command("test_cmd", test_handler)
        
        assert "test_cmd" in manager.commands
        assert manager.commands["test_cmd"] == test_handler
    
    def test_execute_command(self):
        """Test command execution."""
        manager = CommandManager({})
        
        def test_handler(args):
            return "test_result"
        
        manager.register_command("test_cmd", test_handler)
        result = manager.execute_command("test_cmd", {})
        
        assert result == "test_result"
    
    def test_execute_nonexistent_command(self):
        """Test executing non-existent command."""
        manager = CommandManager({})
        
        with pytest.raises(CLIError):
            manager.execute_command("nonexistent", {})


__all__ = ["TestCommandManager"]
