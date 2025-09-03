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
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['iterations'] = int(parts[0].strip())
    if len(parts) >= 2:
        params['confidence'] = float(parts[1].strip())
    
    return 'monte', params


def parse_feargreed_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Fear & Greed parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['lookback'] = int(parts[0].strip())
    
    return 'feargreed', params


def parse_tsf_parameters(params_str: str) -> tuple[str, dict]:
    """Parse TSF parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'tsf', params


def parse_rsi_momentum_parameters(params_str: str) -> tuple[str, dict]:
    """Parse RSI Momentum parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'rsi_mom', params


def parse_rsi_divergence_parameters(params_str: str) -> tuple[str, dict]:
    """Parse RSI Divergence parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'rsi_div', params


def parse_macd_parameters(params_str: str) -> tuple[str, dict]:
    """Parse MACD parameters."""
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
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'ema', params


def parse_sma_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SMA parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'sma', params


def parse_bb_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Bollinger Bands parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    if len(parts) >= 2:
        params['std_dev'] = float(parts[1].strip())
    
    return 'bb', params


def parse_atr_parameters(params_str: str) -> tuple[str, dict]:
    """Parse ATR parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'atr', params


def parse_cci_parameters(params_str: str) -> tuple[str, dict]:
    """Parse CCI parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'cci', params


def parse_vwap_parameters(params_str: str) -> tuple[str, dict]:
    """Parse VWAP parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'vwap', params


def parse_pivot_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Pivot Points parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['method'] = parts[0].strip().lower()
    
    return 'pivot', params


def parse_hma_parameters(params_str: str) -> tuple[str, dict]:
    """Parse HMA parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'hma', params


def parse_kelly_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Kelly Criterion parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['lookback'] = int(parts[0].strip())
    
    return 'kelly', params


def parse_donchain_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Donchian Channel parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'donchain', params


def parse_fibo_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Fibonacci Retracement parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['method'] = parts[0].strip().lower()
    
    return 'fibo', params


def parse_obv_parameters(params_str: str) -> tuple[str, dict]:
    """Parse OBV parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'obv', params


def parse_stdev_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Standard Deviation parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'stdev', params


def parse_adx_parameters(params_str: str) -> tuple[str, dict]:
    """Parse ADX parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    
    return 'adx', params


def parse_sar_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SAR parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['acceleration'] = float(parts[0].strip())
    if len(parts) >= 2:
        params['maximum'] = float(parts[1].strip())
    
    return 'sar', params


def parse_supertrend_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SuperTrend parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['period'] = int(parts[0].strip())
    if len(parts) >= 2:
        params['multiplier'] = float(parts[1].strip())
    
    return 'supertrend', params


def parse_putcallratio_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Put-Call Ratio parameters."""
    params = {}
    parts = params_str.split(',')
    
    if len(parts) >= 1:
        params['lookback'] = int(parts[0].strip())
    
    return 'putcallratio', params


def parse_cot_parameters(params_str: str) -> tuple[str, dict]:
    """Parse COT parameters."""
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
