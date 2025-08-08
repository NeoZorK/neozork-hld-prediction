# -*- coding: utf-8 -*-
# src/plotting/term_navigation.py

"""
Terminal navigation system for chunked plotting.
Provides interactive navigation controls for viewing data chunks.
"""

import pandas as pd
import plotext as plt
from typing import Optional, List, Dict, Any, Callable
import re
from datetime import datetime, date
import sys
import os

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    try:
        # Fallback to relative imports when run as module
        from ..common import logger
        from ..common.constants import TradingRule, BUY, SELL, NOTRADE
    except ImportError:
        # Final fallback for test environments
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        try:
            from src.common import logger
            from src.common.constants import TradingRule, BUY, SELL, NOTRADE
        except ImportError:
            # Mock logger for test environments
            class MockLogger:
                @staticmethod
                def print_warning(msg): print(f"WARNING: {msg}")
                @staticmethod
                def print_error(msg): print(f"ERROR: {msg}")
                @staticmethod
                def print_success(msg): print(f"SUCCESS: {msg}")
            
            logger = MockLogger()
            # Mock constants
            class TradingRule:
                pass
            BUY = "BUY"
            SELL = "SELL"
            NOTRADE = "NOTRADE"


class TerminalNavigator:
    """
    Interactive terminal navigator for chunked data viewing.
    Supports navigation commands: n/p/s/e/c for next/previous/start/end/choose.
    """
    
    def __init__(self, chunks: List[pd.DataFrame], title: str = "Terminal Navigation"):
        """
        Initialize the terminal navigator.
        
        Args:
            chunks (List[pd.DataFrame]): List of data chunks
            title (str): Navigation title
        """
        self.chunks = chunks
        self.title = title
        self.current_chunk_index = 0
        self.total_chunks = len(chunks)
        self.navigation_active = True
        
        # Navigation commands mapping
        self.commands = {
            'n': self._next_chunk,
            'p': self._previous_chunk,
            's': self._start_chunk,
            'e': self._end_chunk,
            'c': self._choose_chunk,
            'q': self._quit_navigation,

        }
    
    def _next_chunk(self) -> bool:
        """Navigate to next chunk."""
        if self.current_chunk_index < self.total_chunks - 1:
            self.current_chunk_index += 1
            return True
        else:
            logger.print_warning("Already at the last chunk")
            return False
    
    def _previous_chunk(self) -> bool:
        """Navigate to previous chunk."""
        if self.current_chunk_index > 0:
            self.current_chunk_index -= 1
            return True
        else:
            logger.print_warning("Already at the first chunk")
            return False
    
    def _start_chunk(self) -> bool:
        """Navigate to first chunk."""
        if self.current_chunk_index != 0:
            self.current_chunk_index = 0
            return True
        else:
            logger.print_warning("Already at the first chunk")
            return False
    
    def _end_chunk(self) -> bool:
        """Navigate to last chunk."""
        if self.current_chunk_index != self.total_chunks - 1:
            self.current_chunk_index = self.total_chunks - 1
            return True
        else:
            logger.print_warning("Already at the last chunk")
            return False
    
    def _choose_chunk(self) -> bool:
        """Choose specific chunk by number."""
        try:
            choice = input(f"Enter chunk number (1-{self.total_chunks}): ").strip()
            chunk_num = int(choice)
            if 1 <= chunk_num <= self.total_chunks:
                self.current_chunk_index = chunk_num - 1
                return True
            else:
                logger.print_error(f"Invalid chunk number. Must be between 1 and {self.total_chunks}")
                return True  # Continue navigation instead of exiting
        except ValueError:
            logger.print_error("Invalid input. Please enter a number.")
            return True  # Continue navigation instead of exiting
        except KeyboardInterrupt:
            print("\nCancelled chunk selection.")
            return True  # Continue navigation instead of exiting
    
    def _choose_date(self) -> bool:
        """Choose chunk by date."""
        try:
            date_input = input("Enter date (YYYY-MM-DD or YYYY-MM-DD HH:MM): ").strip()
            
            # Try different date formats
            date_formats = [
                '%Y-%m-%d',
                '%Y-%m-%d %H:%M',
                '%Y-%m-%d %H:%M:%S'
            ]
            
            target_date = None
            for fmt in date_formats:
                try:
                    target_date = datetime.strptime(date_input, fmt)
                    break
                except ValueError:
                    continue
            
            if target_date is None:
                logger.print_error("Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM")
                return True  # Continue navigation instead of exiting
            
            # Find chunk containing the target date
            for i, chunk in enumerate(self.chunks):
                if len(chunk) > 0:
                    chunk_start = chunk.index[0]
                    chunk_end = chunk.index[-1]
                    
                    # Convert to datetime if needed
                    if isinstance(chunk_start, str):
                        try:
                            chunk_start = datetime.strptime(chunk_start, '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            try:
                                chunk_start = datetime.strptime(chunk_start, '%Y-%m-%d')
                            except ValueError:
                                continue
                    
                    if isinstance(chunk_end, str):
                        try:
                            chunk_end = datetime.strptime(chunk_end, '%Y-%m-%d %H:%M:%S')
                        except ValueError:
                            try:
                                chunk_end = datetime.strptime(chunk_end, '%Y-%m-%d')
                            except ValueError:
                                continue
                    
                    if chunk_start <= target_date <= chunk_end:
                        self.current_chunk_index = i
                        logger.print_success(f"Found date in chunk {i+1}")
                        return True
            
            logger.print_warning(f"Date {date_input} not found in any chunk")
            return True  # Continue navigation instead of exiting
            
        except KeyboardInterrupt:
            print("\nCancelled date selection.")
            return True  # Continue navigation instead of exiting
    
    def _quit_navigation(self) -> bool:
        """Quit navigation."""
        self.navigation_active = False
        return True
    
    def _show_help(self) -> bool:
        """Show navigation help."""
        print("\n" + "="*60)
        print("TERMINAL NAVIGATION HELP")
        print("="*60)
        print("Navigation Commands:")
        print("  n - Next chunk")
        print("  p - Previous chunk")
        print("  s - Start (first chunk)")
        print("  e - End (last chunk)")
        print("  c - Choose chunk by number")
        print("  d - Choose chunk by date (YYYY-MM-DD)")
        print("  h/? - Show this help")
        print("  q - Quit navigation")
        print("  Enter - Continue to next chunk (original behavior)")
        print("="*60)
        return True  # Continue navigation after showing help
    
    def get_current_chunk(self) -> pd.DataFrame:
        """Get current chunk."""
        return self.chunks[self.current_chunk_index]
    
    def get_current_chunk_info(self) -> Dict[str, Any]:
        """Get information about current chunk."""
        chunk = self.get_current_chunk()
        if len(chunk) == 0:
            return {
                'index': self.current_chunk_index + 1,
                'total': self.total_chunks,
                'start_date': 'N/A',
                'end_date': 'N/A',
                'rows': 0
            }
        
        start_date = chunk.index[0] if len(chunk) > 0 else "N/A"
        end_date = chunk.index[-1] if len(chunk) > 0 else "N/A"
        
        return {
            'index': self.current_chunk_index + 1,
            'total': self.total_chunks,
            'start_date': start_date,
            'end_date': end_date,
            'rows': len(chunk)
        }
    
    def show_navigation_prompt(self) -> str:
        """Show navigation prompt and get user input."""
        info = self.get_current_chunk_info()
        
        print(f"\n[Navigation: type 'n/p/s/e/c/d/q' -> next/previous/start/end/choose chunk/choose date/quit]")
        print(f"Current: Chunk {info['index']}/{info['total']} ({info['start_date']} to {info['end_date']})")
        
        user_input = input("Press Enter to continue or type navigation command: ").strip().lower()
        return user_input
    
    def process_navigation_input(self, user_input: str) -> bool:
        """
        Process navigation input and return True if should continue navigation.
        
        Args:
            user_input (str): User input command
            
        Returns:
            bool: True if should continue navigation, False if should quit
        """
        if not user_input:
            # Empty input - continue to next chunk (original behavior)
            return self._next_chunk()
        
        # Check for date selection command
        if user_input.startswith('d'):
            return self._choose_date()
        
        # Check for chunk selection with number
        if user_input.startswith('c'):
            return self._choose_chunk()
        
        # Check for other navigation commands
        if user_input in self.commands:
            result = self.commands[user_input]()
            # For navigation commands, always continue navigation even if command fails
            # (e.g., trying to go previous when at start)
            return True
        
        # Unknown command - continue navigation instead of quitting
        logger.print_warning(f"Unknown command '{user_input}'. Type 'n/p/s/e/c/d/q' for navigation.")
        return True
    
    def navigate(self, plot_function: Callable[[pd.DataFrame, int, Dict[str, Any]], None]) -> None:
        """
        Main navigation loop.
        
        Args:
            plot_function: Function to call for plotting each chunk
        """
        while self.navigation_active and self.current_chunk_index < self.total_chunks:
            # Get current chunk info
            chunk_info = self.get_current_chunk_info()
            current_chunk = self.get_current_chunk()
            
            # Plot current chunk
            plot_function(current_chunk, self.current_chunk_index, chunk_info)
            
            # Note: We don't automatically exit when reaching the end
            # User can continue navigating even at the last chunk
            
            # Show navigation prompt
            user_input = self.show_navigation_prompt()
            
            # Process navigation input
            if not self.process_navigation_input(user_input):
                # If process_navigation_input returns False, it means we should quit
                break
        
        if self.navigation_active:
            logger.print_success("Navigation completed successfully!")


def create_navigation_prompt(chunk_index: int, total_chunks: int, start_date: str, end_date: str) -> str:
    """
    Create navigation prompt string.
    
    Args:
        chunk_index (int): Current chunk index (1-based)
        total_chunks (int): Total number of chunks
        start_date (str): Start date of current chunk
        end_date (str): End date of current chunk
        
    Returns:
        str: Navigation prompt string
    """
    return f"\n[Navigation: type 'n/p/s/e/c/d/q' -> next/previous/start/end/choose chunk/choose date/quit]\nCurrent: Chunk {chunk_index}/{total_chunks} ({start_date} to {end_date})\nPress Enter to continue or type navigation command: "


def parse_navigation_input(user_input: str) -> Dict[str, Any]:
    """
    Parse navigation input and return command details.
    
    Args:
        user_input (str): User input
        
    Returns:
        Dict[str, Any]: Parsed command details
    """
    user_input = user_input.strip().lower()
    
    if not user_input:
        return {'command': 'next', 'valid': True}
    
    # Check for date selection
    if user_input.startswith('d'):
        return {'command': 'date', 'valid': True}
    
    # Check for chunk selection
    if user_input.startswith('c'):
        return {'command': 'choose', 'valid': True}
    
    # Check for other commands
    commands = ['n', 'p', 's', 'e', 'h', 'q', '?']
    if user_input in commands:
        return {'command': user_input, 'valid': True}
    
    return {'command': user_input, 'valid': False, 'error': f"Unknown command '{user_input}'"}


def validate_date_input(date_str: str) -> Optional[datetime]:
    """
    Validate and parse date input.
    
    Args:
        date_str (str): Date string to validate
        
    Returns:
        Optional[datetime]: Parsed datetime or None if invalid
    """
    date_formats = [
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M',
        '%Y-%m-%d %H:%M:%S'
    ]
    
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    return None


class AutoTerminalNavigator(TerminalNavigator):
    """
    Extended terminal navigator for AUTO mode with field array switching.
    Supports switching between different field arrays (OHLC, pressure_high, pressure_low, etc.).
    """
    
    def __init__(self, chunks: List[pd.DataFrame], title: str = "AUTO Terminal Navigation", field_columns: List[str] = None):
        """
        Initialize the AUTO terminal navigator.
        
        Args:
            chunks (List[pd.DataFrame]): List of data chunks
            title (str): Navigation title
            field_columns (List[str]): List of field columns to navigate through
        """
        super().__init__(chunks, title)
        
        # Field navigation state
        self.current_field_index = 0
        self.field_columns = field_columns or []
        self.total_fields = len(self.field_columns) if field_columns else 0
        
        # Field groups for better organization
        self.field_groups = self._organize_field_groups()
        self.current_group_index = 0
        self.total_groups = len(self.field_groups)
        
        # Extended commands for field navigation
        self.commands.update({
            'f': self._next_field,
            'b': self._previous_field,
            'g': self._next_group,
            'h': self._previous_group,
            '?': self._show_help,
            'help': self._show_help,
        })
    
    def _organize_field_groups(self) -> List[Dict[str, Any]]:
        """Organize fields into logical groups."""
        groups = []
        
        # Group 1: OHLC (always first)
        ohlc_fields = [col for col in self.field_columns if col.lower() in ['open', 'high', 'low', 'close', 'volume']]
        if ohlc_fields:
            groups.append({
                'name': 'OHLC',
                'fields': ohlc_fields,
                'description': 'Price and Volume Data'
            })
        
        # Group 2: Pressure indicators
        pressure_fields = [col for col in self.field_columns if 'pressure' in col.lower()]
        if pressure_fields:
            groups.append({
                'name': 'Pressure',
                'fields': pressure_fields,
                'description': 'Pressure Indicators'
            })
        
        # Group 3: Predicted values
        predicted_fields = [col for col in self.field_columns if 'predicted' in col.lower()]
        if predicted_fields:
            groups.append({
                'name': 'Predicted',
                'fields': predicted_fields,
                'description': 'Predicted Values'
            })
        
        # Group 4: Other indicators
        other_fields = [col for col in self.field_columns 
                       if col not in ohlc_fields and col not in pressure_fields and col not in predicted_fields]
        if other_fields:
            groups.append({
                'name': 'Other',
                'fields': other_fields,
                'description': 'Other Indicators'
            })
        
        return groups
    
    def _next_field(self) -> bool:
        """Navigate to next field within current group."""
        if self.total_groups == 0:
            logger.print_warning("No field groups available")
            return False
        
        current_group = self.field_groups[self.current_group_index]
        if self.current_field_index < len(current_group['fields']) - 1:
            self.current_field_index += 1
            return True
        else:
            # Try to move to next group
            return self._next_group()
    
    def _previous_field(self) -> bool:
        """Navigate to previous field within current group."""
        if self.total_groups == 0:
            logger.print_warning("No field groups available")
            return False
        
        if self.current_field_index > 0:
            self.current_field_index -= 1
            return True
        else:
            # Try to move to previous group
            return self._previous_group()
    
    def _next_group(self) -> bool:
        """Navigate to next field group."""
        if self.current_group_index < self.total_groups - 1:
            self.current_group_index += 1
            # Set field index to first field in new group
            self.current_field_index = 0
            return True
        else:
            logger.print_warning("Already at the last field group")
            return False
    
    def _previous_group(self) -> bool:
        """Navigate to previous field group."""
        if self.current_group_index > 0:
            self.current_group_index -= 1
            # Set field index to last field in new group
            group_fields = self.field_groups[self.current_group_index]['fields']
            self.current_field_index = len(group_fields) - 1
            return True
        else:
            logger.print_warning("Already at the first field group")
            return False
    
    def get_current_field(self) -> str:
        """Get the current field name."""
        if self.total_groups == 0:
            return None
        
        current_group = self.field_groups[self.current_group_index]
        if self.current_field_index < len(current_group['fields']):
            return current_group['fields'][self.current_field_index]
        return None
    
    def get_current_group_info(self) -> Dict[str, Any]:
        """Get information about the current field group."""
        if self.total_groups == 0:
            return {'name': 'None', 'description': 'No fields available', 'current_field': None}
        
        group = self.field_groups[self.current_group_index]
        current_field = group['fields'][self.current_field_index] if self.current_field_index < len(group['fields']) else None
        
        return {
            'name': group['name'],
            'description': group['description'],
            'field_index': self.current_field_index + 1,
            'total_fields': len(group['fields']),
            'current_field': current_field
        }
    
    def show_navigation_prompt(self) -> str:
        """Show extended navigation prompt with field information."""
        chunk_info = self.get_current_chunk_info()
        group_info = self.get_current_group_info()
        
        print(f"\n[AUTO Navigation: n/p/s/e/c/d for chunks, f/b/g/h for fields, ?/help for help, q to quit]")
        print(f"Chunk: {chunk_info['index']}/{chunk_info['total']} ({chunk_info['start_date']} to {chunk_info['end_date']})")
        print(f"Field: {group_info['name']} - {group_info['description']}")
        if group_info['current_field']:
            print(f"Current: {group_info['current_field']} ({group_info['field_index']}/{group_info['total_fields']})")
        
        user_input = input("Press Enter to continue or type navigation command: ").strip().lower()
        return user_input
    
    def _show_help(self) -> bool:
        """Show extended navigation help."""
        print("=" * 60)
        print("AUTO TERMINAL NAVIGATION HELP")
        print("=" * 60)
        print("Chunk Navigation:")
        print("  n - Next chunk")
        print("  p - Previous chunk")
        print("  s - Start (first chunk)")
        print("  e - End (last chunk)")
        print("  c - Choose chunk by number")
        print("  d - Choose chunk by date (YYYY-MM-DD)")
        print()
        print("Field Navigation:")
        print("  f - Next field")
        print("  b - Previous field")
        print("  g - Next field group")
        print("  h - Previous field group")
        print()
        print("System Commands:")
        print("  ? - Show this help")
        print("  q - Quit navigation")
        print("  Enter - Continue to next chunk (original behavior)")
        print("=" * 60)
        return True 