# -*- coding: utf-8 -*-
# src/cli/core/argument_validator.py

"""
Argument validation and post-processing for CLI.
"""

import sys
from colorama import Fore, Style


def validate_and_process_arguments(args):
    """Validates and processes parsed arguments."""
    
    # --- Post-parsing validation ---
    effective_mode = 'yfinance' if args.mode == 'yf' else args.mode

    # Normalize stoch aliases to 'stoch:'
    if args.rule:
        if args.rule.lower().startswith('stochastic:'):
            args.rule = 'stoch:' + args.rule.split(':', 1)[1]
        elif args.rule.lower().startswith('stochoscillator:'):
            args.rule = 'stoch:' + args.rule.split(':', 1)[1]
        # Monte Carlo aliases
        elif args.rule.lower().startswith('montecarlo:'):
            args.rule = 'monte:' + args.rule.split(':', 1)[1]
        elif args.rule.lower().startswith('mc:'):
            args.rule = 'monte:' + args.rule.split(':', 1)[1]
        # Fear & Greed aliases
        elif args.rule.lower().startswith('fg:'):
            args.rule = 'feargreed:' + args.rule.split(':', 1)[1]
        # Time Series Forecast aliases
        elif args.rule.lower().startswith('tsforecast:'):
            args.rule = 'tsf:' + args.rule.split(':', 1)[1]

    # Validate rule argument
    if args.rule:
        # Check if it's a parameterized rule
        if ':' in args.rule:
            # Parameterized rule - validate the indicator name part
            indicator_name = args.rule.split(':', 1)[0].lower()
            valid_indicators = ['rsi', 'rsi_mom', 'rsi_div', 'macd', 'stoch', 'stochastic', 'stochoscillator', 'ema', 'sma', 'bb', 'atr', 'cci', 'vwap', 'pivot', 'hma', 'tsf', 'monte', 'montecarlo', 'kelly', 'putcallratio', 'cot', 'feargreed', 'fg', 'donchain', 'fibo', 'obv', 'stdev', 'adx', 'sar', 'supertrend', 'wave']
            if indicator_name not in valid_indicators:
                # Provide detailed help for parameterized indicators
                help_info = {
                    'hma': 'HMA (Hull Moving Average): hma:period,price_type (e.g., hma:20,close)',
                    'tsf': 'TSF (Time Series Forecast): tsf:period,price_type (e.g., tsf:20,close)',
                    'monte': 'Monte Carlo: monte:simulations,period (e.g., monte:1000,252)',
                    'kelly': 'Kelly Criterion: kelly:period (e.g., kelly:20)',
                    'putcallratio': 'Put/Call Ratio: putcallratio:period,price_type (e.g., putcallratio:20,close)',
                    'cot': 'COT: cot:period,price_type (e.g., cot:20,close)',
                    'feargreed': 'Fear & Greed: feargreed:period,price_type (e.g., feargreed:20,close)',
                    'donchain': 'Donchian Channel: donchain:period (e.g., donchain:20)',
                    'fibo': 'Fibonacci: fibo:levels or fibo:all (e.g., fibo:0.236,0.382,0.618)',
                    'obv': 'OBV: obv (no parameters needed)',
                    'stdev': 'Standard Deviation: stdev:period,price_type (e.g., stdev:20,close)',
                    'adx': 'ADX: adx:period (e.g., adx:14)',
                    'sar': 'SAR: sar:acceleration,maximum (e.g., sar:0.02,0.2)',
                    'supertrend': 'SuperTrend: supertrend:period,multiplier[,price_type] (e.g., supertrend:10,3.0)',
                    'rsi': 'RSI: rsi:period,oversold,overbought,price_type (e.g., rsi:14,30,70,close)',
                    'macd': 'MACD: macd:fast,slow,signal,price_type (e.g., macd:12,26,9,close)',
                    'stoch': 'Stochastic: stoch:k_period,d_period,price_type (e.g., stoch:14,3,close)',
                    'ema': 'EMA: ema:period,price_type (e.g., ema:20,close)',
                    'sma': 'SMA: sma:period,price_type (e.g., sma:20,close)',
                    'bb': 'Bollinger Bands: bb:period,std_dev,price_type (e.g., bb:20,2.0,close)',
                    'atr': 'ATR: atr:period (e.g., atr:14)',
                    'cci': 'CCI: cci:period,price_type (e.g., cci:20,close)',
                    'vwap': 'VWAP: vwap:price_type (e.g., vwap:close)',
                    'pivot': 'Pivot Points: pivot:price_type (e.g., pivot:close)',
                    'wave': 'wave:339,10,2,fast,22,11,4,fast,prime,22,open'
                }
                
                if indicator_name in help_info:
                    raise ValueError(f"Invalid indicator name '{indicator_name}' in parameterized rule '{args.rule}'.\n\n{help_info[indicator_name]}\n\nValid indicators: {', '.join(valid_indicators)}")
                else:
                    raise ValueError(f"Invalid indicator name '{indicator_name}' in parameterized rule '{args.rule}'. Valid indicators: {', '.join(valid_indicators)}")
        else:
            # Regular rule - validate against choices
            from src.common.constants import TradingRule
            rule_aliases_map = {
                'PHLD': 'Predict_High_Low_Direction', 
                'PV': 'Pressure_Vector', 
                'SR': 'Support_Resistants',
                'BB': 'Bollinger_Bands'
            }
            rule_names = list(TradingRule.__members__.keys())
            all_rule_choices = rule_names + list(rule_aliases_map.keys()) + ['OHLCV', 'AUTO']
            
            if args.rule not in all_rule_choices:
                # Check if it might be a parameterized indicator
                if args.rule.lower() in ['hma', 'tsf', 'monte', 'montecarlo', 'kelly', 'putcallratio', 'cot', 'feargreed', 'fg', 'donchain', 'fibo', 'obv', 'stdev', 'adx', 'sar', 'supertrend', 'rsi', 'macd', 'stoch', 'stochastic', 'stochoscillator', 'ema', 'sma', 'bb', 'atr', 'cci', 'vwap', 'pivot', 'wave']:
                    raise ValueError(f"Invalid rule '{args.rule}'. This is a parameterized indicator. Use format: {args.rule}:parameters\n\nExamples:\n  {args.rule}:20,close\n  {args.rule}:14,3,close (for stochastic)\n  {args.rule}:1000,252 (for monte carlo)\n\nUse --help for more information about parameterized indicators.")
                else:
                    raise ValueError(f"Invalid rule '{args.rule}'. Use one of {all_rule_choices}")

    # Handle interactive mode
    if effective_mode == 'interactive':
        from src.cli.core.interactive_mode import start_interactive_mode
        start_interactive_mode()
        sys.exit(0)

    # Handle positional arguments for 'show' mode
    if effective_mode == 'show':
        # Default to empty source if no args provided (will show help)
        if not args.show_args:
            args.source = ''
        else:
            # First positional argument is the source (if provided)
            args.source = args.show_args[0]
            # Normalize 'yf' to 'yfinance'
            if args.source == 'yf':
                args.source = 'yfinance'

            # Remaining arguments are keywords
            if len(args.show_args) > 1:
                args.keywords = args.show_args[1:]

    # Handle positional arguments for 'csv' mode (mask support)
    if effective_mode == 'csv' and args.show_args:
        # If positional arguments are provided for CSV mode, treat first as mask
        if not args.csv_mask:
            args.csv_mask = args.show_args[0]
            print(f"{Fore.YELLOW}Using positional argument '{args.csv_mask}' as CSV mask{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Warning: Both --csv-mask '{args.csv_mask}' and positional argument '{args.show_args[0]}' provided. Using --csv-mask.{Style.RESET_ALL}")

    # Check requirements for CSV mode
    if effective_mode == 'csv':
        if not args.csv_file and not args.csv_folder:
            raise ValueError("argument --csv-file or --csv-folder is required when mode is 'csv'")
        if args.csv_file and args.csv_folder:
            raise ValueError("cannot use both --csv-file and --csv-folder together")
        if args.csv_mask and not args.csv_folder:
            raise ValueError("argument --csv-mask can only be used with --csv-folder")
        if args.point is None:
            # Set default point value for folder processing
            if args.csv_folder:
                args.point = 0.00001
                print(f"{Fore.YELLOW}Using default point value 0.00001 for folder processing{Style.RESET_ALL}")
            else:
                raise ValueError("argument --point is required when mode is 'csv' with --csv-file")

    # Check requirements for API modes (yfinance, polygon, binance, exrate)
    api_modes = ['yfinance', 'polygon', 'binance', 'exrate']
    if effective_mode in api_modes:
        if not args.ticker:
            raise ValueError(f"argument --ticker is required when mode is '{effective_mode}'")

    # Check date/period requirements for yfinance
    if effective_mode == 'yfinance':
        if not args.period and not (args.start and args.end):
            raise ValueError("for yfinance mode, provide either --period OR both --start and --end")
        if args.start and not args.end:
            raise ValueError("argument --end is required when --start is provided for yfinance mode")
        if args.end and not args.start:
            raise ValueError("argument --start is required when --end is provided for yfinance mode")
        if args.period and (args.start or args.end):
            raise ValueError("cannot use --period together with --start or --end for yfinance mode")

    # Check requirements for Polygon and Binance (but not Exchange Rate API)
    polygon_binance_modes = ['polygon', 'binance']
    if effective_mode in polygon_binance_modes:
        if not args.start or not args.end:
            raise ValueError(f"arguments --start and --end are required when mode is '{effective_mode}'")
        if args.point is None:
            raise ValueError(f"argument --point is required when mode is '{effective_mode}'")

    # Check requirements for Exchange Rate API (only point and ticker)
    if effective_mode == 'exrate':
        if args.point is None:
            raise ValueError("argument --point is required when mode is 'exrate'")
        # Note: exrate uses --interval for both free (current) and paid (historical) plans

    # Check point value if provided
    if args.point is not None and args.point <= 0:
        raise ValueError("argument --point: value must be positive")

    # Normalize source for show mode
    if effective_mode == 'show' and args.source == 'yf':
        args.source = 'yfinance'

    # --- Fix: Merge positional show_args into source/keywords for show mode ---
    if effective_mode == 'show':
        # If user provided positional arguments after 'show', use them as source/keywords
        if hasattr(args, 'show_args') and args.show_args:
            # If the first positional arg is a valid source, treat as source
            valid_sources = ['yfinance', 'yf', 'csv', 'polygon', 'binance', 'exrate', 'ind', 'mql5', 'samples']
            # Remove any flags from show_args (e.g. --raw, --cleaned, --draw, etc.)
            filtered_args = [a for a in args.show_args if not a.startswith('--')]
            if filtered_args:
                if filtered_args[0] in valid_sources:
                    args.source = filtered_args[0]
                    args.keywords = filtered_args[1:]
                    if args.source == 'yf':
                        args.source = 'yfinance'
                else:
                    args.keywords = filtered_args

    # --- Fix: Map --show-rule to args.rule for show mode compatibility ---
    if effective_mode == 'show' and hasattr(args, 'show_rule') and args.show_rule:
        args.rule = args.show_rule

    # Parse strategy parameters
    if args.strategy:
        try:
            strategy_parts = args.strategy.split(',')
            if len(strategy_parts) != 3:
                raise ValueError("--strategy must have exactly 3 values: lot_size,risk_reward_ratio,fee_per_trade")
            
            lot_size = float(strategy_parts[0])
            risk_reward_ratio = float(strategy_parts[1])
            fee_per_trade = float(strategy_parts[2])
            
            # Validate strategy parameters
            if lot_size <= 0:
                raise ValueError("lot_size must be positive")
            if risk_reward_ratio <= 0:
                raise ValueError("risk_reward_ratio must be positive")
            if fee_per_trade < 0:
                raise ValueError("fee_per_trade must be non-negative")
            
            # Store parsed values
            args.lot_size = lot_size
            args.risk_reward_ratio = risk_reward_ratio
            args.fee_per_trade = fee_per_trade
            
        except ValueError as e:
            raise ValueError(f"Invalid strategy parameters: {e}. Use format: lot_size,risk_reward_ratio,fee_per_trade")
    else:
        # Default strategy parameters
        args.lot_size = 1.0
        args.risk_reward_ratio = 2.0
        args.fee_per_trade = 0.07

    # --- Restrict export flags for forbidden modes ---
    # Allow export flags only for demo, show (except show ind), and csv folder mode
    forbidden_export_modes = ['yfinance', 'polygon', 'binance', 'exrate']
    if effective_mode in forbidden_export_modes:
        if getattr(args, 'export_parquet', False) or getattr(args, 'export_csv', False) or getattr(args, 'export_json', False) or getattr(args, 'export_indicators_info', False):
            raise ValueError("Export flags (--export-parquet, --export-csv, --export-json, --export-indicators-info) are only allowed in 'demo' and 'show' modes (except 'show ind'). Use 'show' mode to export indicators from downloaded data.")
    
    # Special handling for CSV mode - allow export only for folder processing
    if effective_mode == 'csv':
        if args.csv_file and (getattr(args, 'export_parquet', False) or getattr(args, 'export_csv', False) or getattr(args, 'export_json', False) or getattr(args, 'export_indicators_info', False)):
            raise ValueError("Export flags (--export-parquet, --export-csv, --export-json, --export-indicators-info) are only allowed in 'demo', 'show' modes, and CSV folder processing. Use 'show' mode to export indicators from single CSV files.")
    # Disallow export flags for 'show ind' (indicator viewing)
    if effective_mode == 'show' and hasattr(args, 'source') and args.source == 'ind':
        if getattr(args, 'export_parquet', False) or getattr(args, 'export_csv', False) or getattr(args, 'export_json', False) or getattr(args, 'export_indicators_info', False):
            raise ValueError("Export flags (--export-parquet, --export-csv, --export-json, --export-indicators-info) are not allowed in 'show ind' mode. Use 'demo' or other show modes to export indicators.")

    return args
