# -*- coding: utf-8 -*-
# src/cli/core/version_banner/constants.py

"""
Constants and configuration for version banner display.
"""

from colorama import Fore, Style

from src import __version__


class VersionBannerConstants:
    """Constants for version banner display system."""
    
    # Animation timing constants (100x faster than original)
    BORDER_ANIMATION_DELAY = 0.00018
    ASCII_ANIMATION_DELAY = 0.0000008
    ASCII_LINE_DELAY = 0.000008
    TYPEWRITER_DELAY = 0.0000018
    INFO_LINE_DELAY = 0.000018
    STATUS_LINE_DELAY = 0.000018
    LOADING_MESSAGE_DELAY = 0.02
    LOADING_PAUSE_DELAY = 0.02
    
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
    
    # Loading messages for system initialization
    LOADING_MESSAGES = [
        f'{Fore.GREEN}[SYSTEM]{Style.RESET_ALL} Initializing NeoZorK HLD System...',
        f'{Fore.CYAN}[CORE]{Style.RESET_ALL} Loading Advanced ML Algorithms...',
        f'{Fore.YELLOW}[AI]{Style.RESET_ALL} Quantum Financial Analysis Engine Online...',
        f'{Fore.RED}[SECURITY]{Style.RESET_ALL} Cybersecurity Protocols Activated...',
        f'{Fore.MAGENTA}[READY]{Style.RESET_ALL} All Systems Operational!'
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
    
    # Glitch effect characters
    GLITCH_CHARS = ['█', '▓', '▒', '░', '▀', '▄', '▌', '▐']
    
    # Border characters
    TOP_BORDER = '╔═══════════════════════════════════════════════════════════════╗'
    MIDDLE_BORDER = '╠═══════════════════════════════════════════════════════════════╣'
    BOTTOM_BORDER = '╚═══════════════════════════════════════════════════════════════╝'
