"""
Interactive CLI Components

This module provides interactive command-line functionality.
"""

import sys
from typing import Dict, Any, Optional, List
import readline

from ...core.base import BaseComponent
from ...core.exceptions import CLIError


class InteractiveCLI(BaseComponent):
    """
    Interactive command-line interface.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize interactive CLI.
        
        Args:
            config: Configuration dictionary
        """
        super().__init__("interactive_cli", config or {})
        self.prompt = config.get("prompt", "neozork> ") if config else "neozork> "
        self.commands = {}
        self.running = False
    
    def register_command(self, name: str, handler: callable, help_text: str = "") -> None:
        """
        Register an interactive command.
        
        Args:
            name: Command name
            handler: Command handler function
            help_text: Help text for the command
        """
        self.commands[name] = {
            'handler': handler,
            'help': help_text
        }
        self.logger.debug(f"Registered interactive command: {name}")
    
    def start(self) -> None:
        """
        Start the interactive CLI session.
        """
        self.running = True
        self.logger.info("Starting interactive CLI session")
        
        print("Neozork HLD Prediction Interactive CLI")
        print("Type 'help' for available commands, 'quit' to exit")
        
        while self.running:
            try:
                user_input = input(self.prompt).strip()
                
                if not user_input:
                    continue
                
                self._process_command(user_input)
                
            except KeyboardInterrupt:
                print("\nExiting...")
                self.running = False
            except EOFError:
                print("\nExiting...")
                self.running = False
            except Exception as e:
                print(f"Error: {e}")
    
    def _process_command(self, user_input: str) -> None:
        """
        Process a user command.
        
        Args:
            user_input: User input string
        """
        parts = user_input.split()
        if not parts:
            return
        
        command = parts[0]
        args = parts[1:] if len(parts) > 1 else []
        
        # Built-in commands
        if command == "quit" or command == "exit":
            self.running = False
            return
        
        if command == "help":
            self._show_help()
            return
        
        # Registered commands
        if command in self.commands:
            try:
                handler = self.commands[command]['handler']
                result = handler(args)
                if result:
                    print(result)
            except Exception as e:
                print(f"Command error: {e}")
        else:
            print(f"Unknown command: {command}. Type 'help' for available commands.")
    
    def _show_help(self) -> None:
        """Show help for available commands."""
        print("\nAvailable commands:")
        print("  help          - Show this help message")
        print("  quit, exit    - Exit the interactive session")
        
        for name, info in self.commands.items():
            help_text = info['help'] if info['help'] else "No description"
            print(f"  {name:<12} - {help_text}")
        
        print()


__all__ = ["InteractiveCLI"]
