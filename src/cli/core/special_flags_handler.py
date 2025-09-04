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
    # Check if there's a specific parameter after --examples
    examples_idx = sys.argv.index('--examples')
    if examples_idx + 1 < len(sys.argv):
        search_term = sys.argv[examples_idx + 1].lower()
        handle_filtered_examples(search_term)
        return
    
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Indicator Usage Examples:{Style.RESET_ALL}")
    print("  Show all indicators:   --indicators")
    print("  Show oscillators:      --indicators oscillators")
    print("  Show RSI info:         --indicators oscillators rsi")
    print("  Show trend indicators: --indicators trend")
    print("  Show MACD info:        --indicators momentum macd")
    print("  Search examples:       --examples <search_term>")
    print("  Interactive mode:      python run_analysis.py interactive")
    
    try:
        from src.cli.examples.main_examples import show_all_cli_examples
        show_all_cli_examples()
    except ImportError:
        print(f"{Fore.RED}Examples module not available{Style.RESET_ALL}")
    
    sys.exit(0)


def handle_filtered_examples(search_term: str):
    """Handle filtered examples based on search term."""
    import io
    from contextlib import redirect_stdout
    
    print(f"\n{Fore.YELLOW}{Style.BRIGHT}Searching examples for: '{search_term}'{Style.RESET_ALL}")
    print("=" * 60)
    
    try:
        from src.cli.examples.main_examples import show_all_cli_examples
        
        # Capture the output
        output_buffer = io.StringIO()
        with redirect_stdout(output_buffer):
            show_all_cli_examples()
        
        # Get the captured output
        full_output = output_buffer.getvalue()
        
        # Filter lines containing the search term
        lines = full_output.split('\n')
        filtered_lines = []
        found_matches = False
        
        for line in lines:
            if search_term.lower() in line.lower():
                filtered_lines.append(line)
                found_matches = True
        
        if found_matches:
            print('\n'.join(filtered_lines))
        else:
            print(f"{Fore.RED}No examples found containing '{search_term}'{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Try searching for: wave, rsi, macd, ema, sma, stoch, cci, adx, sar{Style.RESET_ALL}")
            
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
