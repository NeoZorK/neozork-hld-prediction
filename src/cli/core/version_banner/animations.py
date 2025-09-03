# -*- coding: utf-8 -*-
# src/cli/core/version_banner/animations.py

"""
Animation utilities for version banner display.
"""

import random
import time
from colorama import Fore, Style

from .constants import VersionBannerConstants


class AnimationUtils:
    """Utility class for banner animations."""
    
    @staticmethod
    def create_aligned_line(text: str, clean_text_len: int, total_width: int = 66, 
                           move_border_left: int = 0, move_border_right: int = 0) -> str:
        """Create perfectly aligned line with exact width."""
        content_width = 60 - move_border_left + move_border_right
        needed_spaces = max(0, content_width - clean_text_len)
        return f'{Fore.CYAN}║{Style.RESET_ALL}  {text}' + ' ' * needed_spaces + f' {Fore.CYAN}║{Style.RESET_ALL}'
    
    @staticmethod
    def glitch_effect(text: str, intensity: int = 3) -> str:
        """Add cyberpunk glitch effect to text."""
        return ''.join(
            random.choice(VersionBannerConstants.GLITCH_CHARS) 
            if random.random() < 0.05 * intensity else char
            for char in text
        )
    
    @staticmethod
    def typewriter_effect(text: str, delay: float = 0.00025) -> None:
        """Ultra fast typewriter effect with border symbols."""
        for i in range(len(text) + 1):
            print('\r' + text[:i] + ('█' if i < len(text) else ''), end='', flush=True)
            time.sleep(delay)
        print()
    
    @staticmethod
    def typewriter_effect_clean(text: str, delay: float = 0.0025) -> None:
        """Ultra fast typewriter effect without border symbols."""
        for i in range(len(text) + 1):
            print('\r' + text[:i], end='', flush=True)
            time.sleep(delay)
        print()
    
    @staticmethod
    def animate_border(border: str, delay: float) -> None:
        """Animate border drawing."""
        for i in range(len(border)):
            print('\r' + border[:i+1], end='', flush=True)
            time.sleep(delay)
        print()
    
    @staticmethod
    def animate_ascii_art() -> None:
        """Animate ASCII art with color transitions."""
        for i, ascii_line in enumerate(VersionBannerConstants.ASCII_LOGO_LINES):
            # Character by character reveal with perfect alignment
            revealed_chars = ''
            for char in ascii_line:
                revealed_chars += char
                colored_text = f'{VersionBannerConstants.ASCII_COLORS[i]}{Style.BRIGHT}{revealed_chars}{Style.RESET_ALL}'
                display_line = AnimationUtils.create_aligned_line(colored_text, len(revealed_chars))
                print('\r' + display_line, end='', flush=True)
                time.sleep(VersionBannerConstants.ASCII_ANIMATION_DELAY)
            print()
            time.sleep(VersionBannerConstants.ASCII_LINE_DELAY)
    
    @staticmethod
    def display_info_section() -> None:
        """Display information section with typewriter effect."""
        for text in VersionBannerConstants.INFO_LINES:
            # Calculate clean text length without color codes
            clean_text = text.replace(Style.BRIGHT, '').replace(Style.RESET_ALL, '')
            for color in [Fore.YELLOW, Fore.GREEN, Fore.RED, Fore.BLUE]:
                clean_text = clean_text.replace(color, '')
            clean_text_len = len(clean_text)
            
            line = AnimationUtils.create_aligned_line(text, clean_text_len, move_border_right=0)
            AnimationUtils.typewriter_effect_clean(line, VersionBannerConstants.TYPEWRITER_DELAY)
            time.sleep(VersionBannerConstants.INFO_LINE_DELAY)
    
    @staticmethod
    def display_status_section() -> None:
        """Display status section with emoji handling."""
        for text in VersionBannerConstants.STATUS_LINES:
            # Calculate proper alignment accounting for emoji display width
            clean_text = text.replace('⚡', '').replace('🔮', '').replace('🚀', '').strip()
            emoji_count = text.count('⚡') + text.count('🔮') + text.count('🚀')
            actual_display_len = len(clean_text) + emoji_count * 2  # Each emoji displays as 2 chars
            
            line = AnimationUtils.create_aligned_line(
                f'{Style.BRIGHT}{text}{Style.RESET_ALL}', 
                actual_display_len, 
                move_border_left=2
            )
            print(line)
            time.sleep(VersionBannerConstants.STATUS_LINE_DELAY)
