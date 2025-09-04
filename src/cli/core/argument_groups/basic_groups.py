# -*- coding: utf-8 -*-
# src/cli/core/argument_groups/basic_groups.py

"""
Basic argument groups for the argument parser.
"""

import argparse

from .config import ArgumentParserConfig


class BasicArgumentGroups:
    """Builder class for creating basic argument groups."""
    
    @staticmethod
    def add_examples_option(parser: argparse.ArgumentParser) -> None:
        """Add examples option to parser."""
        parser.add_argument(
            '--examples',
            action='store_true',
            help='Show usage examples and exit.'
        )
    
    @staticmethod
    def add_indicators_option(parser: argparse.ArgumentParser) -> None:
        """Add indicators search option to parser."""
        parser.add_argument(
            '--indicators',
            nargs='*',
            metavar=('CATEGORY', 'NAME'),
            help='Show available indicators by category and name. Usage: --indicators [category] [name]'
        )
    
    @staticmethod
    def add_metrics_option(parser: argparse.ArgumentParser) -> None:
        """Add metrics encyclopedia option to parser."""
        parser.add_argument(
            '--metric',
            nargs='*',
            metavar=('TYPE', 'FILTER'),
            help='Show trading metrics encyclopedia and strategy tips. Usage: --metric [metrics|tips|notes] [filter_text]'
        )
    
    @staticmethod
    def add_required_arguments(parser: argparse.ArgumentParser) -> None:
        """Add required arguments group."""
        required_group = parser.add_argument_group('Required Arguments')
        required_group.add_argument(
            'mode', 
            nargs='?', 
            choices=ArgumentParserConfig.AVAILABLE_MODES,
            help="Operating mode: 'demo', 'yfinance'/'yf', 'csv', 'polygon', 'binance', 'show'."
        )
        
        # Show mode positional arguments
        parser.add_argument(
            'show_args', 
            nargs='*', 
            default=[],
            help=argparse.SUPPRESS  # Hide from help but collect positional args after 'mode'
        )
    
    @staticmethod
    def add_other_options(parser: argparse.ArgumentParser) -> None:
        """Add other options group."""
        other_group = parser.add_argument_group('Other Options')
        other_group.add_argument(
            '-h', 
            action='help', 
            default=argparse.SUPPRESS,
            help='Show this help message and exit'
        )
        other_group.add_argument(
            '--version', 
            action='store_true',
            help="Show program version and exit"
        )
