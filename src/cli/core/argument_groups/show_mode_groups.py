# -*- coding: utf-8 -*-
# src/cli/core/argument_groups/show_mode_groups.py

"""
Show mode argument groups for the argument parser.
"""

import argparse

from .config import ArgumentParserConfig


class ShowModeArgumentGroups:
    """Builder class for creating show mode argument groups."""
    
    @staticmethod
    def add_show_mode_options(parser: argparse.ArgumentParser) -> None:
        """Add show mode options group."""
        show_group = parser.add_argument_group('Show Mode Options')
        all_rule_choices = ArgumentParserConfig.get_all_rule_choices()
        
        show_group.add_argument(
            '--source', 
            metavar='SRC', 
            default='yfinance',
            choices=ArgumentParserConfig.DATA_SOURCE_CHOICES,
            help="Data source filter: yfinance, csv, polygon, binance, ind (indicators)"
        )
        show_group.add_argument(
            '--keywords', 
            metavar='WORD', 
            nargs='+', 
            default=[],
            help="Filter keywords (e.g., ticker symbol, date patterns)"
        )
        show_group.add_argument(
            '--show-start', 
            metavar='DATE', 
            type=str, 
            default=None,
            help="Start date/datetime to filter data before calculation"
        )
        show_group.add_argument(
            '--show-end', 
            metavar='DATE', 
            type=str, 
            default=None,
            help="End date/datetime to filter data before calculation"
        )
        show_group.add_argument(
            '--show-rule', 
            metavar='RULE', 
            type=str, 
            choices=all_rule_choices, 
            default=None,
            help="Trading rule for indicator calculation (single file mode)"
        )
