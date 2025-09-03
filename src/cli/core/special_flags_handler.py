# -*- coding: utf-8 -*-
# src/cli/core/special_flags_handler.py

"""
Handler for special CLI flags that don't require mode argument.
"""

import sys
from colorama import Fore, Style


def handle_special_flags():
    """
    Handle special flags that don't require mode argument.
    Returns True if a special flag was handled and program should exit.
    """
    # Handle --examples flag
    if '--examples' in sys.argv:
        handle_examples_flag()
        return True
    
    # Handle --metric encyclopedia
    if '--metric' in sys.argv:
        handle_metric_flag()
        return True
    
    # Handle --interactive flag
    if '--interactive' in sys.argv:
        handle_interactive_flag()
        return True
    
    return False


def handle_examples_flag():
    """Handle --examples flag."""
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Indicator Usage Examples:{Style.RESET_ALL}")
    print("  Show all indicators:   --indicators")
    print("  Show oscillators:      --indicators oscillators")
    print("  Show RSI info:         --indicators oscillators rsi")
    print("  Show trend indicators: --indicators trend")
    print("  Show MACD info:        --indicators momentum macd")
    print("  Interactive mode:      python run_analysis.py interactive")
    
    try:
        from src.cli.examples.cli_examples import show_cli_examples_colored
        show_cli_examples_colored()
    except ImportError:
        print(f"{Fore.RED}Examples module not available{Style.RESET_ALL}")
    
    sys.exit(0)


def handle_metric_flag():
    """Handle --metric flag."""
    idx = sys.argv.index('--metric')
    args_list = sys.argv[idx+1:]
    
    try:
        from src.cli.encyclopedia.quant_encyclopedia import QuantEncyclopedia
        encyclopedia = QuantEncyclopedia()
        
        if not args_list:
            # Show all metrics and tips
            encyclopedia.show_all_metrics()
            encyclopedia.show_all_tips()
        elif len(args_list) == 1:
            # Single argument - could be type or filter
            arg = args_list[0].lower()
            if arg in ['metrics', 'tips', 'notes']:
                if arg == 'metrics':
                    encyclopedia.show_all_metrics()
                elif arg == 'tips':
                    encyclopedia.show_all_tips()
                elif arg == 'notes':
                    encyclopedia.show_all_tips()  # Notes are part of tips
            else:
                # Treat as filter text
                encyclopedia.show_filtered_content(arg)
        elif len(args_list) >= 2:
            # Two or more arguments: type and filter
            metric_type = args_list[0].lower()
            filter_text = ' '.join(args_list[1:])
            
            if metric_type == 'metrics':
                encyclopedia.show_all_metrics(filter_text)
            elif metric_type == 'tips':
                encyclopedia.show_all_tips(filter_text)
            elif metric_type == 'notes':
                encyclopedia.show_all_tips(filter_text)  # Notes are part of tips
            else:
                # Invalid type, treat first as filter
                encyclopedia.show_filtered_content(' '.join(args_list))
        
    except ImportError:
        print(f"{Fore.RED}Encyclopedia module not available{Style.RESET_ALL}")
    
    sys.exit(0)


def handle_interactive_flag():
    """Handle --interactive flag."""
    try:
        from src.cli.core.interactive_mode import start_interactive_mode
        start_interactive_mode()
    except ImportError:
        print(f"{Fore.RED}Interactive mode not available{Style.RESET_ALL}")
    
    sys.exit(0)
