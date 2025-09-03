# -*- coding: utf-8 -*-
# src/cli/core/argument_parser.py

"""
Argument parser setup and configuration for CLI.
"""

import argparse
import textwrap
import sys
from colorama import init, Fore, Style

from src.calculation.indicators.trend.wave_ind import ENUM_MOM_TR, ENUM_GLOBAL_TR
from src.cli.indicators.indicators_search import IndicatorSearcher
from .help_formatter import ColoredHelpFormatter

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Use absolute imports for constants and version within the src package
from src.common.constants import TradingRule
from src import __version__


def show_cool_version():
    """Display the most epic, modern techno-style version banner with insane animations and sounds!"""
    import time
    import os
    import threading
    import random
    from datetime import datetime
    
    def play_hacker_sound():
        """Play epic hacker/cyberpunk startup sound effects with real audio!"""
        try:
            # Enhanced sound system for macOS
            if os.system('which afplay > /dev/null 2>&1') == 0:
                # Create temporary sound files with system audio synthesis
                sound_commands = [
                    # Startup beep sequence
                    'say -v "Zarvox" "System initializing" -r 300 &',
                    # Cyberpunk beeps using audio synthesis
                    'for i in {1..5}; do (speaker-test -t sine -f 1000 -l 1 > /dev/null 2>&1 & sleep 0.1; kill $!) 2>/dev/null; sleep 0.1; done &',
                    # Alternative: use built-in audio
                    'osascript -e "set volume output volume 50" &',
                    'afplay /System/Library/Sounds/Ping.aiff &',
                    'sleep 0.2; afplay /System/Library/Sounds/Pop.aiff &',
                    'sleep 0.3; afplay /System/Library/Sounds/Tink.aiff &'
                ]
                
                for cmd in sound_commands[:3]:  # Play first 3 for startup
                    try:
                        os.system(cmd)
                    except:
                        pass
                        
            # Python-based sound generation as backup
            try:
                import subprocess
                # Generate sine wave beeps using Python
                frequencies = [800, 1000, 1200, 1500, 1100, 900]
                for freq in frequencies:
                    # Use system beep with different frequencies
                    subprocess.run(['python3', '-c', f'''
import math
import sys
import time
try:
    # Generate beep sound
    duration = 0.1
    sample_rate = 8000
    t = [i/sample_rate for i in range(int(duration * sample_rate))]
    wave = [int(4095 * math.sin(2 * math.pi * {freq} * time_point)) for time_point in t]
    # Output as system beep
    sys.stdout.write("\a")
    sys.stdout.flush()
    time.sleep(0.05)
except:
    pass
'''], capture_output=True, timeout=1)
                    time.sleep(0.08)
            except:
                pass
                
            # Fallback to enhanced terminal beeps
            beep_patterns = [
                ["\a", 0.1], ["\a\a", 0.15], ["\a", 0.08], 
                ["\a\a\a", 0.2], ["\a", 0.1], ["\a\a", 0.12]
            ]
            
            for pattern, delay in beep_patterns:
                print(pattern, end='', flush=True)
                time.sleep(delay)
                
        except Exception as e:
            # Ultimate fallback - at least some sound!
            for _ in range(8):
                print('\a', end='', flush=True)
                time.sleep(0.12)
    
    def matrix_rain_effect():
        """Create epic Matrix-style digital rain effect."""
        rain_chars = ['0', '1', '█', '▓', '▒', '░', '|', '/', '-', '\\']
        colors = [Fore.GREEN, Fore.CYAN, Fore.WHITE, '\033[38;5;46m', '\033[38;5;82m']
        
        lines = []
        for i in range(3):
            line = ''
            for j in range(62):
                if random.random() > 0.7:
                    char = random.choice(rain_chars)
                    color = random.choice(colors)
                    line += f'{color}{char}{Style.RESET_ALL}'
                else:
                    line += ' '
            lines.append(f'{Fore.CYAN}║{Style.RESET_ALL}{line}{Fore.CYAN}║{Style.RESET_ALL}')
        return lines
    
    def glitch_effect(text, intensity=3):
        """Add cyberpunk glitch effect to text."""
        glitched = ''
        for char in text:
            if random.random() < 0.05 * intensity:
                # Random glitch characters
                glitched += random.choice(['█', '▓', '▒', '░', '▀', '▄', '▌', '▐'])
            else:
                glitched += char
        return glitched
    
    def typewriter_effect(text, delay=0.03):
        """Epic typewriter effect with glitches."""
        for i in range(len(text) + 1):
            print('\r' + text[:i] + ('█' if i < len(text) else ''), end='', flush=True)
            time.sleep(delay)
        print()  # New line after typing
    
    def play_background_music():
        """Play epic background techno music during animation!"""
        try:
            # Generate cyberpunk background sounds
            music_commands = [
                # Say cool phrases with robotic voice
                'say -v "Zarvox" "Neo Zork. High Level Dominance." -r 200 &',
                'sleep 2; say -v "Zarvox" "Quantum algorithms activated" -r 180 &',
                'sleep 4; say -v "Zarvox" "Market prediction engine online" -r 190 &',
                
                # System sounds for atmosphere
                'sleep 1; afplay /System/Library/Sounds/Ping.aiff &',
                'sleep 1.5; afplay /System/Library/Sounds/Pop.aiff &', 
                'sleep 2.2; afplay /System/Library/Sounds/Tink.aiff &',
                'sleep 3; afplay /System/Library/Sounds/Ping.aiff &',
                'sleep 4; afplay /System/Library/Sounds/Pop.aiff &',
                'sleep 5; afplay /System/Library/Sounds/Tink.aiff &',
                
                # Final dramatic sounds
                'sleep 6; say -v "Zarvox" "System ready for market domination" -r 220 &',
            ]
            
            for cmd in music_commands:
                try:
                    os.system(cmd)
                except:
                    pass
                    
        except:
            # Fallback rhythmic beeps
            rhythm_pattern = [0.3, 0.1, 0.1, 0.4, 0.2, 0.1, 0.3, 0.2]
            for delay in rhythm_pattern * 3:  # Repeat 3 times
                print('\a', end='', flush=True)
                time.sleep(delay)
    
    def play_typewriter_sounds():
        """Play typewriter clicking sounds during text animation"""
        try:
            # Simulate typewriter/keyboard sounds
            for _ in range(20):
                if random.random() > 0.3:
                    os.system('afplay /System/Library/Sounds/Tink.aiff > /dev/null 2>&1 &')
                time.sleep(random.uniform(0.05, 0.15))
        except:
            pass
    
    # Start multiple sound threads for layered audio experience
    sound_thread = threading.Thread(target=play_hacker_sound, daemon=True)
    music_thread = threading.Thread(target=play_background_music, daemon=True)
    typewriter_thread = threading.Thread(target=play_typewriter_sounds, daemon=True)
    
    sound_thread.start()
    music_thread.start()
    typewriter_thread.start()
    
    # Clear screen for maximum effect
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Epic loading sequence
    loading_messages = [
        f'{Fore.GREEN}[SYSTEM]{Style.RESET_ALL} Initializing NeoZorK HLD System...',
        f'{Fore.CYAN}[CORE]{Style.RESET_ALL} Loading Advanced ML Algorithms...',
        f'{Fore.YELLOW}[AI]{Style.RESET_ALL} Quantum Financial Analysis Engine Online...',
        f'{Fore.RED}[SECURITY]{Style.RESET_ALL} Cybersecurity Protocols Activated...',
        f'{Fore.MAGENTA}[READY]{Style.RESET_ALL} All Systems Operational!'
    ]
    
    for msg in loading_messages:
        typewriter_effect(msg, 0.02)
        time.sleep(0.3)
    
    print('\n' + '='*64)
    time.sleep(0.5)
    
    # Show matrix rain effect with sounds
    print(f'{Fore.GREEN}{Style.BRIGHT}DIGITAL RAIN INITIALIZING...{Style.RESET_ALL}')
    # Play matrix sound effect
    os.system('say -v "Zarvox" "Digital rain initializing" -r 250 > /dev/null 2>&1 &')
    time.sleep(0.5)
    rain_lines = matrix_rain_effect()
    for i, line in enumerate(rain_lines):
        print(line)
        # Add sound for each rain line
        if i == 0:
            os.system('afplay /System/Library/Sounds/Ping.aiff > /dev/null 2>&1 &')
        elif i == 1:
            os.system('afplay /System/Library/Sounds/Pop.aiff > /dev/null 2>&1 &')
        else:
            os.system('afplay /System/Library/Sounds/Tink.aiff > /dev/null 2>&1 &')
        time.sleep(0.1)
    
    time.sleep(0.3)
    os.system('clear' if os.name == 'posix' else 'cls')
    
    # Epic animated logo reveal
    ascii_lines = [
        '███╗   ██╗███████╗ ██████╗ ███████╗ ██████╗ ██████╗ ██╗  ██╗',
        '████╗  ██║██╔════╝██╔═══██╗╚══███╔╝██╔═══██╗██╔══██╗██║ ██╔╝',
        '██╔██╗ ██║█████╗  ██║   ██║  ███╔╝ ██║   ██║██████╔╝█████╔╝ ',
        '██║╚██╗██║██╔══╝  ██║   ██║ ███╔╝  ██║   ██║██╔══██╗██╔═██╗ ',
        '██║ ╚████║███████╗╚██████╔╝███████╗╚██████╔╝██║  ██║██║  ██╗',
        '╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝'
    ]
    
    # Top border with epic animation and sound
    border = '╔══════════════════════════════════════════════════════════════╗'
    os.system('say -v "Zarvox" "Initializing logo" -r 300 > /dev/null 2>&1 &')
    for i in range(len(border)):
        print('\r' + border[:i+1], end='', flush=True)
        # Add typing sound occasionally
        if i % 10 == 0:
            os.system('afplay /System/Library/Sounds/Tink.aiff > /dev/null 2>&1 &')
        time.sleep(0.02)
    print()
    # Border complete sound
    os.system('afplay /System/Library/Sounds/Ping.aiff > /dev/null 2>&1 &')
    
    # Animate ASCII art line by line with color transitions
    colors = ['\033[38;5;46m', '\033[38;5;82m', '\033[38;5;118m', '\033[38;5;154m', '\033[38;5;190m', '\033[38;5;226m']
    
    for i, ascii_line in enumerate(ascii_lines):
        # Add glitch effect occasionally
        if random.random() > 0.7:
            glitched_line = glitch_effect(ascii_line, 2)
            full_line = f'{Fore.CYAN}║{Style.RESET_ALL}  {colors[i]}{Style.BRIGHT}{glitched_line}{Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}'
            print(full_line)
            time.sleep(0.05)
            # Show correct line after glitch
            print('\r' + ' ' * 66 + '\r', end='')
        
        # Real line with epic color
        full_line = f'{Fore.CYAN}║{Style.RESET_ALL}  {colors[i]}{Style.BRIGHT}{ascii_line}{Style.RESET_ALL}{Fore.CYAN}║{Style.RESET_ALL}'
        
        # Character by character reveal with proper padding
        revealed_chars = ''
        for char in ascii_line:
            revealed_chars += char
            # Calculate proper padding to maintain 64 character width
            remaining_chars = len(ascii_line) - len(revealed_chars)
            padding_needed = 64 - 3 - len(revealed_chars)  # 64 total - '║  ' - revealed chars - '║'
            if padding_needed < 0:
                padding_needed = 0
            
            display_line = f'{Fore.CYAN}║{Style.RESET_ALL}  {colors[i]}{Style.BRIGHT}{revealed_chars}{Style.RESET_ALL}'
            display_line += ' ' * padding_needed + f'{Fore.CYAN}║{Style.RESET_ALL}'
            print('\r' + display_line, end='', flush=True)
            time.sleep(0.01)
        print()
        time.sleep(0.1)
    
    # Middle border with animation
    border = '╠══════════════════════════════════════════════════════════════╣'
    for i in range(len(border)):
        print('\r' + border[:i+1], end='', flush=True)
        time.sleep(0.01)
    print()
    
    # Info section with epic effects
    info_lines = [
        (f'{Fore.YELLOW}{Style.BRIGHT}Shcherbyna Pressure Vector Indicator{Style.RESET_ALL}', 24),
        (f'{Fore.GREEN}{Style.BRIGHT}Advanced Financial Analysis System{Style.RESET_ALL}', 26),
        (f'{Fore.RED}{Style.BRIGHT}Version: {__version__}{Style.RESET_ALL}', 46),
        (f'{Fore.BLUE}{Style.BRIGHT}Powered by Advanced ML & Technical Analysis{Style.RESET_ALL}', 17)
    ]
    
    for text, spaces in info_lines:
        line = f'{Fore.CYAN}║{Style.RESET_ALL}  {text}' + ' ' * spaces + f'{Fore.CYAN}║{Style.RESET_ALL}'
        typewriter_effect(line, 0.02)
        time.sleep(0.2)
    
    # Second middle border
    border = '╠══════════════════════════════════════════════════════════════╣'
    for i in range(len(border)):
        print('\r' + border[:i+1], end='', flush=True)
        time.sleep(0.01)
    print()
    
    # Status section with pulsing effects
    status_lines = [
        (f'⚡ Ready for high-frequency trading analysis ⚡', 15),
        (f'🔮 Predicting market movements with precision 🔮', 14), 
        (f'🚀 Optimized for performance and accuracy 🚀', 18)
    ]
    
    for text, spaces in status_lines:
        # Pulsing effect
        for pulse in range(3):
            if pulse % 2 == 0:
                line = f'{Fore.CYAN}║{Style.RESET_ALL}  {Style.BRIGHT}{text}{Style.RESET_ALL}' + ' ' * spaces + f'{Fore.CYAN}║{Style.RESET_ALL}'
            else:
                line = f'{Fore.CYAN}║{Style.RESET_ALL}  {Style.DIM}{text}{Style.RESET_ALL}' + ' ' * spaces + f'{Fore.CYAN}║{Style.RESET_ALL}'
            print('\r' + line, end='', flush=True)
            time.sleep(0.3)
        print()
        time.sleep(0.1)
    
    # Bottom border with final animation
    border = '╚══════════════════════════════════════════════════════════════╝'
    for i in range(len(border)):
        print('\r' + border[:i+1], end='', flush=True)
        time.sleep(0.01)
    print()
    
    # Final epic message with dramatic sounds
    time.sleep(0.5)
    
    # Play dramatic completion sound
    os.system('say -v "Zarvox" "All systems operational. Ready for deployment" -r 200 > /dev/null 2>&1 &')
    
    final_messages = [
        (f'{Fore.GREEN}{Style.BRIGHT}>>> SYSTEM STATUS: FULLY OPERATIONAL <<<{Style.RESET_ALL}', 'afplay /System/Library/Sounds/Ping.aiff'),
        (f'{Fore.CYAN}{Style.BRIGHT}>>> QUANTUM ALGORITHMS: LOADED <<<{Style.RESET_ALL}', 'afplay /System/Library/Sounds/Pop.aiff'),
        (f'{Fore.YELLOW}{Style.BRIGHT}>>> READY FOR MARKET DOMINATION <<<{Style.RESET_ALL}', 'say -v "Zarvox" "Ready for market domination" -r 250')
    ]
    
    for msg, sound_cmd in final_messages:
        # Play sound for each message
        os.system(f'{sound_cmd} > /dev/null 2>&1 &')
        typewriter_effect(f'\n{" " * ((64 - len(msg.replace(Style.BRIGHT, "").replace(Style.RESET_ALL, "").replace(Fore.GREEN, "").replace(Fore.CYAN, "").replace(Fore.YELLOW, ""))) // 2)}{msg}', 0.03)
        time.sleep(0.5)
    
    # Final victory fanfare
    time.sleep(0.5)
    victory_sounds = [
        'afplay /System/Library/Sounds/Ping.aiff > /dev/null 2>&1',
        'sleep 0.2; afplay /System/Library/Sounds/Pop.aiff > /dev/null 2>&1', 
        'sleep 0.4; afplay /System/Library/Sounds/Tink.aiff > /dev/null 2>&1',
        'sleep 0.6; say -v "Zarvox" "Neo Zork H L D. Mission accomplished" -r 180 > /dev/null 2>&1'
    ]
    
    for sound in victory_sounds:
        os.system(f'{sound} &')
    
    print('\n')


def create_argument_parser():
    """Creates and configures the argument parser."""
    
    # --- Main description ---
    main_description = textwrap.dedent(f"""
       {Fore.CYAN}{Style.BRIGHT}Shcherbyna Pressure Vector Indicator Analysis Tool{Style.RESET_ALL}
       
       Calculate and plot pressure vector indicators from multiple data sources: demo data, Yahoo Finance, CSV files, Polygon.io, Binance, and Exchange Rate API. Export calculated indicators in parquet, CSV, or JSON formats.
       
       {Fore.YELLOW}Quick Start:{Style.RESET_ALL}
         python run_analysis.py --indicators                    # List all available indicators
         python run_analysis.py --metric                        # Show trading metrics encyclopedia
         python run_analysis.py demo --rule RSI                 # Run with demo data and RSI indicator
         python run_analysis.py interactive                     # Start interactive mode
       """).strip()

    # --- Argument Parser Setup ---
    parser = argparse.ArgumentParser(
        description=main_description,
        formatter_class=ColoredHelpFormatter,
        epilog=None,  # no epilog
        add_help=False  # Disable default help to add it to a specific group
    )

    # --- Examples Option ---
    parser.add_argument(
        '--examples',
        action='store_true',
        help='Show usage examples and exit.'
    )

    # --- Indicators Search Option ---
    parser.add_argument(
        '--indicators',
        nargs='*',
        metavar=('CATEGORY', 'NAME'),
        help='Show available indicators by category and name. Usage: --indicators [category] [name]'
    )

    # --- Metrics Encyclopedia Option ---
    parser.add_argument(
        '--metric',
        nargs='*',
        metavar=('TYPE', 'FILTER'),
        help='Show trading metrics encyclopedia and strategy tips. Usage: --metric [metrics|tips|notes] [filter_text]'
    )

    # --- Interactive Mode Option ---
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Start interactive mode for guided indicator selection and analysis.'
    )

    # --- Required Arguments Group ---
    required_group = parser.add_argument_group('Required Arguments')
    required_group.add_argument('mode', nargs='?', choices=['demo', 'yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'show', 'interactive'],
                                help="Operating mode: 'demo', 'yfinance'/'yf', 'csv', 'polygon', 'binance', 'exrate', 'show', 'interactive'. Not required when using --interactive flag.")

    # --- Show Mode Positional Arguments ---
    parser.add_argument('show_args', nargs='*', default=[],
                        help=argparse.SUPPRESS)  # Hide from help but collect positional args after 'mode'

    # --- Data Source Specific Options Group ---
    data_source_group = parser.add_argument_group('Data Source Options')
    # CSV options
    data_source_group.add_argument('--csv-file', metavar='PATH',
                                   help="Path to input CSV file (required for 'csv' mode when processing single file)")
    data_source_group.add_argument('--csv-folder', metavar='PATH',
                                   help="Path to folder containing CSV files (required for 'csv' mode when processing multiple files)")
    data_source_group.add_argument('--csv-mask', metavar='MASK',
                                   help="Optional mask to filter CSV files by name (case-insensitive, used with --csv-folder)")
    # API options (Yahoo Finance / Polygon.io / Binance)
    data_source_group.add_argument('--ticker', metavar='SYMBOL',
                                   help="Ticker symbol. Examples: 'EURUSD=X' (yfinance), 'AAPL' (polygon), 'BTCUSDT' (binance)")
    data_source_group.add_argument('--interval', metavar='TIME', default='D1',
                                   help="Timeframe: 'M1', 'H1', 'D1', 'W1', 'MN1'. Default: D1")
    # Point size argument
    data_source_group.add_argument('--point', metavar='SIZE', type=float,
                                   help="Point size. Examples: 0.00001 (EURUSD), 0.01 (stocks/crypto)")
    # History selection (period or start/end dates)
    history_group = data_source_group.add_mutually_exclusive_group()
    history_group.add_argument('--period', metavar='TIME',
                               help="History period for yfinance. Examples: '1mo', '1y', '5d'")
    history_group.add_argument('--start', metavar='DATE',
                               help="Start date for data range (yfinance, polygon, binance)")
    # Make --end related only to --start (not period)
    data_source_group.add_argument('--end', metavar='DATE',
                                   help="End date for data range (required with --start)")

    # --- Indicator Options Group ---
    indicator_group = parser.add_argument_group('Indicator Options')
    rule_aliases_map = {
        'PHLD': 'Predict_High_Low_Direction', 
        'PV': 'Pressure_Vector', 
        'SR': 'Support_Resistants',
        'BB': 'Bollinger_Bands'
    }
    rule_names = list(TradingRule.__members__.keys())
    all_rule_choices = rule_names + list(rule_aliases_map.keys()) + ['OHLCV', 'AUTO']
    default_rule_name = 'OHLCV'
    indicator_group.add_argument(
        '--rule',
        default=default_rule_name,
        help=f"Trading rule to apply. Default: {default_rule_name}. Aliases: PHLD=Predict_High_Low_Direction, PV=Pressure_Vector, SR=Support_Resistants, BB=Bollinger_Bands."
    )
    
    # Strategy parameters
    indicator_group.add_argument(
        '--strategy',
        metavar='LOT,RISK_REWARD,FEE',
        help="Strategy parameters: lot_size,risk_reward_ratio,fee_per_trade. Example: --strategy 1,2,0.07 means lot=1.0, risk:reward=2:1, fee=0.07%%. Default: 1.0,2.0,0.07"
    )

    # Add price type selection for indicators that support it
    indicator_group.add_argument(
        '--price-type', metavar='TYPE',
        choices=['open', 'close'],
        default='close',
        help="Price type for indicator calculation: 'open' or 'close' (default: close). Supported by all indicators with price_type parameter"
    )

    # --- Show Mode Options Group ---
    show_group = parser.add_argument_group('Show Mode Options')
    show_group.add_argument(
        '--source', metavar='SRC', default='yfinance',
        choices=['yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'ind'],
        help="Data source filter: yfinance, csv, polygon, binance, exrate, ind (indicators)"
    )
    show_group.add_argument(
        '--keywords', metavar='WORD', nargs='+', default=[],
        help="Filter keywords (e.g., ticker symbol, date patterns)"
    )
    show_group.add_argument(
        '--show-start', metavar='DATE', type=str, default=None,
        help="Start date/datetime to filter data before calculation"
    )
    show_group.add_argument(
        '--show-end', metavar='DATE', type=str, default=None,
        help="End date/datetime to filter data before calculation"
    )
    show_group.add_argument(
        '--show-rule', metavar='RULE', type=str, choices=all_rule_choices, default=None,
        help="Trading rule for indicator calculation (single file mode)"
    )

    # --- Plotting Options Group ---
    plotting_group = parser.add_argument_group('Plotting Options')
    plotting_group.add_argument(
        '-d', '--draw',
        dest='draw',
        choices=['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term'],
        default='fastest',
        help="Plot method: fastest, fast, plotly, mplfinance, seaborn, term"
    )

    # --- Output Options Group ---
    output_group = parser.add_argument_group('Output Options')
    output_group.add_argument('--export-parquet',
                              action='store_true',
                              help="Export indicators to parquet format (../data/indicators/parquet/)")
    output_group.add_argument('--export-csv',
                              action='store_true',
                              help="Export indicators to CSV format (../data/indicators/csv/)")
    output_group.add_argument('--export-json',
                              action='store_true',
                              help="Export indicators to JSON format (../data/indicators/json/)")
    output_group.add_argument('--export-indicators-info',
                              action='store_true',
                              help="Export indicator metadata to JSON format (../data/indicators/metadata/)")

    # --- Other Options Group ---
    other_group = parser.add_argument_group('Other Options')
    other_group.add_argument('-h', action='help', default=argparse.SUPPRESS,
                             help='Show this help message and exit')
    other_group.add_argument('--version', action='store_true',
                             help="Show program version and exit")

    return parser


def parse_arguments():
    """Sets up argument parser using ColoredHelpFormatter and returns the parsed arguments."""
    
    parser = create_argument_parser()
    
    # --- Parse Arguments ---
    try:
        # If --indicators is present, always handle it first and exit
        if '--indicators' in sys.argv:
            idx = sys.argv.index('--indicators')
            args_list = sys.argv[idx+1:]
            searcher = IndicatorSearcher()
            if not args_list:
                searcher.display_categories()
            elif len(args_list) == 1:
                query = args_list[0]
                if query in searcher.indicators:
                    searcher.display_category(query, detailed=True)
                else:
                    results = searcher.search_indicators(query)
                    if results:
                        print(f"\n{Fore.YELLOW}Search results for '{query}' across all categories:{Style.RESET_ALL}")
                        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
                        for ind in results:
                            print(ind.display(detailed=True))
                    else:
                        print(f"{Fore.RED}No indicators found matching: {query}{Style.RESET_ALL}")
                        print(f"{Fore.YELLOW}Available categories: {', '.join(searcher.list_categories())}{Style.RESET_ALL}")
            elif len(args_list) >= 2:
                category = args_list[0]
                name = ' '.join(args_list[1:])
                print(f"\n{Fore.YELLOW}Search in category '{category}' for '{name}':{Style.RESET_ALL}")
                results = searcher.search_indicators(name)
                filtered = [ind for ind in results if ind.category == category]
                if filtered:
                    for ind in filtered:
                        print(ind.display(detailed=True))
                else:
                    print(f"No indicators found in category '{category}' matching '{name}'")
            sys.exit(0)

        # If no arguments provided, show help
        if len(sys.argv) == 1:
            parser.print_help()
            sys.exit(0)

        # Handle --help flag before parsing to avoid mode requirement
        if '--help' in sys.argv or '-h' in sys.argv:
            parser.print_help()
            sys.exit(0)
            
        # Handle --version flag before parsing to avoid mode requirement
        if '--version' in sys.argv:
            show_cool_version()
            sys.exit(0)

        # Handle special flags that don't require mode argument BEFORE parsing
        try:
            from .special_flags_handler import handle_special_flags
            if handle_special_flags():
                return  # Special flag was handled, exit
        except ImportError:
            # Fallback if special flags handler is not available
            pass
            
        # Now parse arguments for normal operation
        args = parser.parse_args()
    except SystemExit as e:
        if e.code != 0:
            print(f"Argument parsing error (Code: {e.code}). Exiting.", file=sys.stderr)
        sys.exit(e.code)

    return args
