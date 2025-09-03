# -*- coding: utf-8 -*-
# src/common/parsing.py

"""
Common parsing functions to avoid circular imports.
"""

def parse_indicator_parameters(rule_str: str) -> tuple[str, dict]:
    """
    Parse indicator rule string in format 'indicator:param1,param2,param3,param4'.
    
    Args:
        rule_str (str): Rule string like 'rsi:14,30,70,open' or 'rsi'
    
    Returns:
        tuple: (indicator_name, parameters_dict)
    """
    if ':' not in rule_str:
        # No parameters provided, return indicator name and empty dict
        return rule_str.lower(), {}
    
    try:
        # Split by ':' to separate indicator name from parameters
        parts = rule_str.split(':', 1)
        if len(parts) != 2:
            raise ValueError(f"Invalid rule format: {rule_str}")
        
        indicator_name = parts[0].lower().strip()
        params_str = parts[1].strip()
        
        # Parse parameters based on indicator type
        if indicator_name in ['stoch', 'stochastic', 'stochoscillator']:
            # Always parse as stoch and return 'stoch' as indicator name
            _, params = parse_stoch_parameters(params_str)
            return 'stoch', params
        elif indicator_name in ['monte', 'montecarlo', 'mc']:
            # Always parse as monte and return 'monte' as indicator name
            _, params = parse_monte_parameters(params_str)
            return 'monte', params
        elif indicator_name in ['feargreed', 'fg']:
            # Always parse as feargreed and return 'feargreed' as indicator name
            _, params = parse_feargreed_parameters(params_str)
            return 'feargreed', params
        elif indicator_name in ['tsf', 'tsforecast']:
            # Always parse as tsf and return 'tsf' as indicator name
            _, params = parse_tsf_parameters(params_str)
            return 'tsf', params
        elif indicator_name == 'rsi':
            return parse_rsi_parameters(params_str)
        elif indicator_name == 'rsi_mom':
            return parse_rsi_momentum_parameters(params_str)
        elif indicator_name == 'rsi_div':
            return parse_rsi_divergence_parameters(params_str)
        elif indicator_name == 'macd':
            return parse_macd_parameters(params_str)
        elif indicator_name == 'ema':
            return parse_ema_parameters(params_str)
        elif indicator_name == 'sma':
            return parse_sma_parameters(params_str)
        elif indicator_name == 'bb':
            return parse_bb_parameters(params_str)
        elif indicator_name == 'atr':
            return parse_atr_parameters(params_str)
        elif indicator_name == 'cci':
            return parse_cci_parameters(params_str)
        elif indicator_name == 'vwap':
            return parse_vwap_parameters(params_str)
        elif indicator_name == 'pivot':
            return parse_pivot_parameters(params_str)
        elif indicator_name == 'hma':
            return parse_hma_parameters(params_str)
        elif indicator_name == 'kelly':
            return parse_kelly_parameters(params_str)
        elif indicator_name == 'donchain':
            return parse_donchain_parameters(params_str)
        elif indicator_name == 'fibo':
            return parse_fibo_parameters(params_str)
        elif indicator_name == 'obv':
            return parse_obv_parameters(params_str)
        elif indicator_name == 'stdev':
            return parse_stdev_parameters(params_str)
        elif indicator_name == 'adx':
            return parse_adx_parameters(params_str)
        elif indicator_name == 'sar':
            return parse_sar_parameters(params_str)
        elif indicator_name == 'supertrend':
            return parse_supertrend_parameters(params_str)
        elif indicator_name == 'putcallratio':
            return parse_putcallratio_parameters(params_str)
        elif indicator_name == 'cot':
            return parse_cot_parameters(params_str)
        elif indicator_name == 'wave':
            # Special handling for wave indicator - show help if no parameters
            if not params_str:
                # Import and show beautiful help
                try:
                    from src.cli.error_handling import show_enhanced_indicator_help
                    show_enhanced_indicator_help("Wave indicator requires parameters", "wave", show_error_header=False)
                    # After showing help, exit with error
                    import sys
                    sys.exit(1)
                except ImportError:
                    # Fallback if error_handling module not available
                    raise ValueError("Wave indicator requires parameters. Use format: wave:339,10,2,fast,22,11,4,fast,prime,22,open")
            return parse_wave_parameters(params_str)
        else:
            # Unknown indicator, show help and raise error
            raise ValueError(f"Unknown indicator: {indicator_name}")
            
    except Exception as e:
        # For now, just raise the error - we'll handle this differently
        raise ValueError(f"Error parsing indicator parameters: {e}")


def parse_rsi_parameters(params_str: str) -> tuple[str, dict]:
    """Parse RSI parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("RSI indicator requires parameters", "rsi", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("RSI indicator requires parameters. Use format: rsi:period,oversold,overbought,price_type")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    if len(parts) >= 2:
        params['overbought'] = float(parts[1].strip())
    if len(parts) >= 3:
        params['oversold'] = float(parts[2].strip())
    if len(parts) >= 4:
        params['price'] = parts[3].strip().lower()
    
    return 'rsi', params


def parse_stoch_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Stochastic parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("Stochastic indicator requires parameters", "stoch", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("Stochastic indicator requires parameters. Use format: stoch:k_period,d_period,slowing")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['k_period'] = int(parts[0].strip())
    if len(parts) >= 2:
        params['d_period'] = int(parts[1].strip())
    if len(parts) >= 3:
        params['slowing'] = int(parts[2].strip())
    
    return 'stoch', params


def parse_monte_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Monte Carlo parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("Monte Carlo indicator requires parameters", "monte", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("Monte Carlo indicator requires parameters. Use format: monte:iterations,confidence")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['iterations'] = int(parts[0].strip())
    if len(parts) >= 2:
        params['confidence'] = float(parts[1].strip())
    
    return 'monte', params


def parse_feargreed_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Fear & Greed parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("Fear & Greed indicator requires parameters", "feargreed", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("Fear & Greed indicator requires parameters. Use format: feargreed:lookback")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['lookback'] = int(parts[0].strip())
    
    return 'feargreed', params


def parse_tsf_parameters(params_str: str) -> tuple[str, dict]:
    """Parse TSF parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("TSF indicator requires parameters", "tsf", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("TSF indicator requires parameters. Use format: tsf:period")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'tsf', params


def parse_rsi_momentum_parameters(params_str: str) -> tuple[str, dict]:
    """Parse RSI Momentum parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("RSI Momentum indicator requires parameters", "rsi_mom", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("RSI Momentum indicator requires parameters. Use format: rsi_mom:period")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'rsi_mom', params


def parse_rsi_divergence_parameters(params_str: str) -> tuple[str, dict]:
    """Parse RSI Divergence parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("RSI Divergence indicator requires parameters", "rsi_div", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("RSI Divergence indicator requires parameters. Use format: rsi_div:period")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'rsi_div', params


def parse_macd_parameters(params_str: str) -> tuple[str, dict]:
    """Parse MACD parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("MACD indicator requires parameters", "macd", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("MACD indicator requires parameters. Use format: macd:fast_period,slow_period,signal_period,price_type")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['fast'] = int(parts[0].strip())
    if len(parts) >= 2:
        params['slow'] = int(parts[1].strip())
    if len(parts) >= 3:
        params['signal'] = int(parts[2].strip())
    
    return 'macd', params


def parse_ema_parameters(params_str: str) -> tuple[str, dict]:
    """Parse EMA parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("EMA indicator requires parameters", "ema", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("EMA indicator requires parameters. Use format: ema:period,price_type")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'ema', params


def parse_sma_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SMA parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("SMA indicator requires parameters", "sma", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("SMA indicator requires parameters. Use format: sma:period,price_type")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'sma', params


def parse_bb_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Bollinger Bands parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("Bollinger Bands indicator requires parameters", "bb", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("Bollinger Bands indicator requires parameters. Use format: bb:period,std_dev,price_type")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    if len(parts) >= 2:
        params['std_dev'] = float(parts[1].strip())
    
    return 'bb', params


def parse_atr_parameters(params_str: str) -> tuple[str, dict]:
    """Parse ATR parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("ATR indicator requires parameters", "atr", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("ATR indicator requires parameters. Use format: atr:period")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'atr', params


def parse_cci_parameters(params_str: str) -> tuple[str, dict]:
    """Parse CCI parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("CCI indicator requires parameters", "cci", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("CCI indicator requires parameters. Use format: cci:period")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'cci', params


def parse_vwap_parameters(params_str: str) -> tuple[str, dict]:
    """Parse VWAP parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("VWAP indicator requires parameters", "vwap", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("VWAP indicator requires parameters. Use format: vwap:period")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'vwap', params


def parse_pivot_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Pivot Points parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("Pivot Points indicator requires parameters", "pivot", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("Pivot Points indicator requires parameters. Use format: pivot:price_type")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['method'] = parts[0].strip().lower()
    
    return 'pivot', params


def parse_hma_parameters(params_str: str) -> tuple[str, dict]:
    """Parse HMA parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("HMA indicator requires parameters", "hma", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("HMA indicator requires parameters. Use format: hma:period,price_type")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'hma', params


def parse_kelly_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Kelly Criterion parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("Kelly Criterion indicator requires parameters", "kelly", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("Kelly Criterion indicator requires parameters. Use format: kelly:period")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['lookback'] = int(parts[0].strip())
    
    return 'kelly', params


def parse_donchain_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Donchian Channel parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("Donchian Channel indicator requires parameters", "donchain", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("Donchian Channel indicator requires parameters. Use format: donchain:period")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'donchain', params


def parse_fibo_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Fibonacci Retracement parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("Fibonacci indicator requires parameters", "fibo", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("Fibonacci indicator requires parameters. Use format: fibo:method")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['method'] = parts[0].strip().lower()
    
    return 'fibo', params


def parse_obv_parameters(params_str: str) -> tuple[str, dict]:
    """Parse OBV parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("OBV indicator requires parameters", "obv", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("OBV indicator requires parameters. Use format: obv:period")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'obv', params


def parse_stdev_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Standard Deviation parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("Standard Deviation indicator requires parameters", "stdev", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("Standard Deviation indicator requires parameters. Use format: stdev:period")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'stdev', params


def parse_adx_parameters(params_str: str) -> tuple[str, dict]:
    """Parse ADX parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("ADX indicator requires parameters", "adx", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("ADX indicator requires parameters. Use format: adx:period")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'adx', params


def parse_sar_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SAR parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("SAR indicator requires parameters", "sar", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("SAR indicator requires parameters. Use format: sar:acceleration,maximum")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['acceleration'] = float(parts[0].strip())
    if len(parts) >= 2:
        params['maximum'] = float(parts[1].strip())
    
    return 'sar', params


def parse_supertrend_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SuperTrend parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("SuperTrend indicator requires parameters", "supertrend", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("SuperTrend indicator requires parameters. Use format: supertrend:period,multiplier")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    if len(parts) >= 2:
        params['multiplier'] = float(parts[1].strip())
    
    return 'supertrend', params


def parse_putcallratio_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Put-Call Ratio parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("Put-Call Ratio indicator requires parameters", "putcallratio", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("Put-Call Ratio indicator requires parameters. Use format: putcallratio:lookback")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['lookback'] = int(parts[0].strip())
    
    return 'putcallratio', params


def parse_cot_parameters(params_str: str) -> tuple[str, dict]:
    """Parse COT parameters."""
    # Check if parameters string is empty and show help
    if not params_str.strip():
        try:
            from src.cli.error_handling import show_enhanced_indicator_help
            show_enhanced_indicator_help("COT indicator requires parameters", "cot", show_error_header=False)
            import sys
            sys.exit(1)
        except ImportError:
            # Fallback if error_handling module not available
            raise ValueError("COT indicator requires parameters. Use format: cot:lookback")
    
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['lookback'] = int(parts[0].strip())
    
    return 'cot', params


def parse_wave_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Wave parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'wave', params
