# -*- coding: utf-8 -*-
# src/cli/core/__init__.py

"""
Core CLI functionality module.
"""

from .cli import main, show_indicator_help
from .argument_parser import parse_arguments, create_argument_parser
from .argument_validator import validate_and_process_arguments
from .cli_show_mode import main_show_mode, show_help
from .help_formatter import ColoredHelpFormatter
from .special_flags_handler import handle_special_flags
from .indicator_help import show_indicator_help as indicator_help

__all__ = [
    'main',
    'show_indicator_help',
    'parse_arguments',
    'create_argument_parser',
    'validate_and_process_arguments',
    'main_show_mode',
    'show_help',
    'ColoredHelpFormatter',
    'handle_special_flags',
    'indicator_help'
]
