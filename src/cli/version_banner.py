# -*- coding: utf-8 -*-
# src/cli/version_banner.py

"""
Version banner display system for NeoZorK HLD Prediction.

This module provides functionality for displaying the version banner
with ASCII art logo and animations.
"""

import os
import time
import random
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

from src import __version__


class VersionBannerDisplay:
    """Handles the display of the version banner with ASCII art logo."""
    
    # ASCII art for NEOZORK logo (60 characters each line)
    ASCII_LOGO_LINES = [
        '███╗   ██╗███████╗ ██████╗ ███████╗ ██████╗ ██████╗ ██╗  ██╗',
        '████╗  ██║██╔════╝██╔═══██╗╚══███╔╝██╔═══██╗██╔══██╗██║ ██╔╝',
        '██╔██╗ ██║█████╗  ██║   ██║  ███╔╝ ██║   ██║██████╔╝█████╔╝ ',
        '██║╚██╗██║██╔══╝  ██║   ██║ ███╔╝  ██║   ██║██╔══██╗██╔═██╗ ',
        '██║ ╚████║███████╗╚██████╔╝███████╗╚██████╔╝██║  ██║██║  ██╗',
        '╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝'
    ]
    
    # Color palette for ASCII art animation
    ASCII_COLORS = [
        '\033[38;5;46m', '\033[38;5;82m', '\033[38;5;118m',
        '\033[38;5;154m', '\033[38;5;190m', '\033[38;5;226m'
    ]
    
    # Information lines for the banner
    INFO_LINES = [
        f'{Fore.YELLOW}{Style.BRIGHT}Shcherbyna Pressure Vector Indicator{Style.RESET_ALL}',
        f'{Fore.GREEN}{Style.BRIGHT}Advanced Financial Analysis System{Style.RESET_ALL}',
        f'{Fore.RED}{Style.BRIGHT}Version: {__version__}{Style.RESET_ALL}',
        f'{Fore.BLUE}{Style.BRIGHT}Powered by Advanced ML & Technical Analysis{Style.RESET_ALL}'
    ]
    
    # Status lines with emojis
    STATUS_LINES = [
        f'⚡ Ready for high-frequency trading analysis ⚡',
        f'🔮 Predicting market movements with precision 🔮',
        f'🚀 Optimized for performance and accuracy 🚀'
    ]
    
    # Border characters
    TOP_BORDER = '╔═══════════════════════════════════════════════════════════════╗'
    MIDDLE_BORDER = '╠═══════════════════════════════════════════════════════════════╣'
    BOTTOM_BORDER = '╚═══════════════════════════════════════════════════════════════╝'
    
    @classmethod
    def display_banner(cls) -> None:
        """Display the complete version banner with ASCII art logo."""
        # Clear screen for maximum effect
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Display banner sections
        cls._display_top_border()
        cls._display_ascii_art()
        cls._display_middle_border()
        cls._display_info_section()
        cls._display_second_middle_border()
        cls._display_status_section()
        cls._display_bottom_border()
        
        # Clean ending
        print('\n')
    
    @classmethod
    def _display_top_border(cls) -> None:
        """Display top border."""
        print(f'{Fore.CYAN}{cls.TOP_BORDER}{Style.RESET_ALL}')
    
    @classmethod
    def _display_ascii_art(cls) -> None:
        """Display ASCII art with colors."""
        for i, ascii_line in enumerate(cls.ASCII_LOGO_LINES):
            colored_text = f'{cls.ASCII_COLORS[i]}{Style.BRIGHT}{ascii_line}{Style.RESET_ALL}'
            print(f'{Fore.CYAN}║{Style.RESET_ALL}  {colored_text}  {Fore.CYAN}║{Style.RESET_ALL}')
    
    @classmethod
    def _display_middle_border(cls) -> None:
        """Display middle border."""
        print(f'{Fore.CYAN}{cls.MIDDLE_BORDER}{Style.RESET_ALL}')
    
    @classmethod
    def _display_info_section(cls) -> None:
        """Display information section."""
        for text in cls.INFO_LINES:
            # Calculate clean text length without color codes
            clean_text = text.replace(Style.BRIGHT, '').replace(Style.RESET_ALL, '')
            for color in [Fore.YELLOW, Fore.GREEN, Fore.RED, Fore.BLUE]:
                clean_text = clean_text.replace(color, '')
            clean_text_len = len(clean_text)
            
            # Create aligned line
            needed_spaces = max(0, 60 - clean_text_len)
            line = f'{Fore.CYAN}║{Style.RESET_ALL}  {text}' + ' ' * needed_spaces + f' {Fore.CYAN}║{Style.RESET_ALL}'
            print(line)
    
    @classmethod
    def _display_second_middle_border(cls) -> None:
        """Display second middle border."""
        print(f'{Fore.CYAN}{cls.MIDDLE_BORDER}{Style.RESET_ALL}')
    
    @classmethod
    def _display_status_section(cls) -> None:
        """Display status section with emoji handling."""
        for text in cls.STATUS_LINES:
            # Calculate proper alignment accounting for emoji display width
            clean_text = text.replace('⚡', '').replace('🔮', '').replace('🚀', '').strip()
            emoji_count = text.count('⚡') + text.count('🔮') + text.count('🚀')
            actual_display_len = len(clean_text) + emoji_count * 2  # Each emoji displays as 2 chars
            
            # Create aligned line
            needed_spaces = max(0, 60 - actual_display_len)
            line = f'{Fore.CYAN}║{Style.RESET_ALL}  {Style.BRIGHT}{text}{Style.RESET_ALL}' + ' ' * needed_spaces + f' {Fore.CYAN}║{Style.RESET_ALL}'
            print(line)
    
    @classmethod
    def _display_bottom_border(cls) -> None:
        """Display bottom border."""
        print(f'{Fore.CYAN}{cls.BOTTOM_BORDER}{Style.RESET_ALL}')


def show_version_banner():
    """Convenience function to display the version banner."""
    VersionBannerDisplay.display_banner()
