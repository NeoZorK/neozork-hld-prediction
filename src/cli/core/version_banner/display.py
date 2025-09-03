# -*- coding: utf-8 -*-
# src/cli/core/version_banner/display.py

"""
Main display class for version banner.
"""

import os
import time

from .animations import AnimationUtils
from .constants import VersionBannerConstants


class VersionBannerDisplay:
    """Handles the display of the version banner with animations and effects."""
    
    @classmethod
    def display_banner(cls) -> None:
        """Display the complete version banner with all animations."""
        # Clear screen for maximum effect
        os.system('clear' if os.name == 'posix' else 'cls')
        
        # Display loading sequence
        cls._display_loading_sequence()
        
        # Clean transition to logo
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
    def _display_loading_sequence(cls) -> None:
        """Display loading sequence with typewriter effect."""
        for msg in VersionBannerConstants.LOADING_MESSAGES:
            AnimationUtils.typewriter_effect(msg, VersionBannerConstants.LOADING_MESSAGE_DELAY)
            time.sleep(VersionBannerConstants.LOADING_PAUSE_DELAY)
    
    @classmethod
    def _display_top_border(cls) -> None:
        """Display top border with animation."""
        AnimationUtils.animate_border(
            VersionBannerConstants.TOP_BORDER, 
            VersionBannerConstants.BORDER_ANIMATION_DELAY
        )
    
    @classmethod
    def _display_ascii_art(cls) -> None:
        """Display ASCII art with animation."""
        AnimationUtils.animate_ascii_art()
    
    @classmethod
    def _display_middle_border(cls) -> None:
        """Display middle border with animation."""
        AnimationUtils.animate_border(
            VersionBannerConstants.MIDDLE_BORDER, 
            VersionBannerConstants.ASCII_ANIMATION_DELAY
        )
    
    @classmethod
    def _display_info_section(cls) -> None:
        """Display information section."""
        AnimationUtils.display_info_section()
    
    @classmethod
    def _display_second_middle_border(cls) -> None:
        """Display second middle border with animation."""
        AnimationUtils.animate_border(
            VersionBannerConstants.MIDDLE_BORDER, 
            VersionBannerConstants.ASCII_ANIMATION_DELAY
        )
    
    @classmethod
    def _display_status_section(cls) -> None:
        """Display status section."""
        AnimationUtils.display_status_section()
    
    @classmethod
    def _display_bottom_border(cls) -> None:
        """Display bottom border with animation."""
        AnimationUtils.animate_border(
            VersionBannerConstants.BOTTOM_BORDER, 
            VersionBannerConstants.ASCII_ANIMATION_DELAY
        )
