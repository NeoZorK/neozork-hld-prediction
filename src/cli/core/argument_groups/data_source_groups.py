# -*- coding: utf-8 -*-
# src/cli/core/argument_groups/data_source_groups.py

"""
Data source argument groups for the argument parser.
"""

import argparse


class DataSourceArgumentGroups:
    """Builder class for creating data source argument groups."""
    
    @staticmethod
    def add_data_source_options(parser: argparse.ArgumentParser) -> None:
        """Add data source specific options group."""
        data_source_group = parser.add_argument_group('Data Source Options')
        
        # CSV options
        DataSourceArgumentGroups._add_csv_options(data_source_group)
        
        # API options
        DataSourceArgumentGroups._add_api_options(data_source_group)
        
        # History selection
        DataSourceArgumentGroups._add_history_options(data_source_group)
    
    @staticmethod
    def _add_csv_options(group: argparse._ArgumentGroup) -> None:
        """Add CSV-specific options."""
        group.add_argument(
            '--csv-file', 
            metavar='PATH',
            help="Path to input CSV file (required for 'csv' mode when processing single file)"
        )
        group.add_argument(
            '--csv-folder', 
            metavar='PATH',
            help="Path to folder containing CSV files (required for 'csv' mode when processing multiple files)"
        )
        group.add_argument(
            '--csv-mask', 
            metavar='MASK',
            help="Optional mask to filter CSV files by name (case-insensitive, used with --csv-folder)"
        )
    
    @staticmethod
    def _add_api_options(group: argparse._ArgumentGroup) -> None:
        """Add API-specific options."""
        group.add_argument(
            '--ticker', 
            metavar='SYMBOL',
            help="Ticker symbol. Examples: 'EURUSD=X' (yfinance), 'AAPL' (polygon), 'BTCUSDT' (binance)"
        )
        group.add_argument(
            '--interval', 
            metavar='TIME', 
            default='D1',
            help="Timeframe: 'M1', 'H1', 'D1', 'W1', 'MN1'. Default: D1"
        )
        group.add_argument(
            '--point', 
            metavar='SIZE', 
            type=float,
            help="Point size. Examples: 0.00001 (EURUSD), 0.01 (stocks/crypto)"
        )
    
    @staticmethod
    def _add_history_options(group: argparse._ArgumentGroup) -> None:
        """Add history selection options."""
        history_group = group.add_mutually_exclusive_group()
        history_group.add_argument(
            '--period', 
            metavar='TIME',
            help="History period for yfinance. Examples: '1mo', '1y', '5d'"
        )
        history_group.add_argument(
            '--start', 
            metavar='DATE',
            help="Start date for data range (yfinance, polygon, binance)"
        )
        group.add_argument(
            '--end', 
            metavar='DATE',
            help="End date for data range (required with --start)"
        )
