# -*- coding: utf-8 -*-
# src/cli/core/argument_parser.py

"""
Argument parser setup and configuration for CLI.

This module provides argument parsing functionality for the NeoZorK HLD Prediction tool,
including a sophisticated version banner display system and comprehensive CLI argument handling.
"""

import argparse
import sys

from .help_formatter import ColoredHelpFormatter
from .version_banner import VersionBannerDisplay
from .argument_groups import (
    ArgumentParserConfig,
    BasicArgumentGroups,
    DataSourceArgumentGroups,
    IndicatorArgumentGroups,
    ShowModeArgumentGroups,
    OutputArgumentGroups
)
from .handlers import IndicatorsSearchHandler


def create_argument_parser() -> argparse.ArgumentParser:
    """Creates and configures the argument parser."""
    parser = argparse.ArgumentParser(
        description=ArgumentParserConfig.get_main_description(),
        formatter_class=ColoredHelpFormatter,
        epilog=None,
        add_help=False  # Disable default help to add it to a specific group
    )
    
    # Add all argument groups
    BasicArgumentGroups.add_examples_option(parser)
    BasicArgumentGroups.add_indicators_option(parser)
    BasicArgumentGroups.add_metrics_option(parser)
    BasicArgumentGroups.add_required_arguments(parser)
    BasicArgumentGroups.add_other_options(parser)
    
    DataSourceArgumentGroups.add_data_source_options(parser)
    IndicatorArgumentGroups.add_indicator_options(parser)
    ShowModeArgumentGroups.add_show_mode_options(parser)
    OutputArgumentGroups.add_plotting_options(parser)
    OutputArgumentGroups.add_output_options(parser)
    
    return parser


def parse_arguments():
    """Sets up argument parser using ColoredHelpFormatter and returns the parsed arguments."""
    parser = create_argument_parser()
    
    try:
        # Handle --indicators flag first
        if '--indicators' in sys.argv:
            idx = sys.argv.index('--indicators')
            args_list = sys.argv[idx+1:]
            IndicatorsSearchHandler.handle_indicators_search(args_list)
            sys.exit(0)
        
        # Handle no arguments case
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(0)
        
        # Handle help flags
        if '--help' in sys.argv or '-h' in sys.argv:
            parser.print_help()
            sys.exit(0)
        
        # Handle version flag
        if '--version' in sys.argv:
            VersionBannerDisplay.display_banner()
            sys.exit(0)
        
        # Handle special flags
        try:
            from .special_flags_handler import handle_special_flags
            if handle_special_flags():
                return  # Special flag was handled, exit
        except ImportError:
            # Fallback if special flags handler is not available
            pass
        
        # Parse arguments for normal operation
        args = parser.parse_args()
        
    except SystemExit as e:
        if e.code != 0:
            print(f"Argument parsing error (Code: {e.code}). Exiting.", file=sys.stderr)
        sys.exit(e.code)
    
    return args


# ============================================================================
# LEGACY FUNCTION COMPATIBILITY
# ============================================================================

def show_cool_version():
    """Legacy function for backward compatibility."""
    VersionBannerDisplay.display_banner()