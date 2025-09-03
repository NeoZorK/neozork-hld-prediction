# -*- coding: utf-8 -*-
# src/cli/core/argument_groups/output_groups.py

"""
Output and plotting argument groups for the argument parser.
"""

import argparse

from .config import ArgumentParserConfig


class OutputArgumentGroups:
    """Builder class for creating output and plotting argument groups."""
    
    @staticmethod
    def add_plotting_options(parser: argparse.ArgumentParser) -> None:
        """Add plotting options group."""
        plotting_group = parser.add_argument_group('Plotting Options')
        plotting_group.add_argument(
            '-d', '--draw',
            dest='draw',
            choices=ArgumentParserConfig.DRAW_CHOICES,
            default='fastest',
            help="Plot method: fastest, fast, plotly, mplfinance, seaborn, term"
        )
    
    @staticmethod
    def add_output_options(parser: argparse.ArgumentParser) -> None:
        """Add output options group."""
        output_group = parser.add_argument_group('Output Options')
        output_group.add_argument(
            '--export-parquet',
            action='store_true',
            help="Export indicators to parquet format (../data/indicators/parquet/)"
        )
        output_group.add_argument(
            '--export-csv',
            action='store_true',
            help="Export indicators to CSV format (../data/indicators/csv/)"
        )
        output_group.add_argument(
            '--export-json',
            action='store_true',
            help="Export indicators to JSON format (../data/indicators/json/)"
        )
        output_group.add_argument(
            '--export-indicators-info',
            action='store_true',
            help="Export indicator metadata to JSON format (../data/indicators/metadata/)"
        )
