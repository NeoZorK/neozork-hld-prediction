# -*- coding: utf-8 -*-
# src/cli/cli_show_mode.py

"""
Refactored CLI show mode with modular structure.
This is the main entry point that delegates to specialized modules.
"""

# Import from refactored modules
from .cli_show_indicators import handle_indicator_mode
from .cli_show_common import _initialize_metrics

def handle_show_mode(args):
    """
    Main entry point for show mode - delegates to appropriate handlers.
    """
    # Handle indicator files mode
    if hasattr(args, 'source') and args.source == 'ind':
        return handle_indicator_mode(args)
    
    # For other modes, use the original logic from cli_show_mode_new
    from .cli_show_mode_new import handle_show_mode as handle_original_show_mode
    return handle_original_show_mode(args)

# Keep backward compatibility
show_mode_handler = handle_show_mode
