# -*- coding: utf-8 -*-
# src/cli/cli.py

"""
Main CLI entry point that uses the refactored structure.
"""

from .core.cli import main, show_indicator_help
from .core.argument_parser import parse_arguments
from .core.argument_validator import validate_and_process_arguments
from .parsers.indicator_parsers import parse_indicator_parameters
from .parsers.indicators.advanced_parsers import parse_supertrend_parameters, parse_wave_parameters

# Re-export main functions for backward compatibility
__all__ = [
    'main',
    'show_indicator_help',
    'parse_arguments',
    'validate_and_process_arguments',
    'parse_indicator_parameters',
    'parse_supertrend_parameters',
    'parse_wave_parameters'
]
