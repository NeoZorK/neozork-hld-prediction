# -*- coding: utf-8 -*-
# src/plotting/term_chunked/indicators/overlays.py

"""
Overlay functions for terminal chunked plotting indicators.
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Dict, Any

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from src.common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    try:
        # Fallback to relative imports when run as module
        from src.common import logger
        from src.common.constants import TradingRule, BUY, SELL, NOTRADE
    except ImportError:
        # Final fallback for pytest with -n auto
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
        from src.common import logger
        from src.common.constants import TradingRule, BUY, SELL, NOTRADE


def _add_pv_overlays_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add Pressure Vector overlays to chunk.
    
    Args:
        chunk: DataFrame chunk
        x_values: X-axis values
    """
    try:
        if 'pressure_vector' in chunk.columns:
            pv_values = chunk['pressure_vector'].tolist()
            plt.plot(x_values, pv_values, color='cyan', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding PV overlays: {e}")


def _add_sr_overlays_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add Support/Resistance overlays to chunk.
    
    Args:
        chunk: DataFrame chunk
        x_values: X-axis values
    """
    try:
        if 'support' in chunk.columns:
            support_values = chunk['support'].tolist()
            plt.plot(x_values, support_values, color='white', marker='█')
        
        if 'resistance' in chunk.columns:
            resistance_values = chunk['resistance'].tolist()
            plt.plot(x_values, resistance_values, color='white', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding SR overlays: {e}")


def _add_phld_overlays_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add PHLD overlays to chunk.
    
    Args:
        chunk: DataFrame chunk
        x_values: X-axis values
    """
    try:
        if 'phld_signal' in chunk.columns:
            # Add trading signals
            _add_trading_signals_to_chunk(chunk, x_values)
    except Exception as e:
        logger.print_error(f"Error adding PHLD overlays: {e}")


def _add_rsi_overlays_to_chunk(chunk: pd.DataFrame, x_values: list, 
                               rule_type: str, params: Dict[str, Any]) -> None:
    """
    Add RSI overlays to chunk.
    
    Args:
        chunk: DataFrame chunk
        x_values: X-axis values
        rule_type: RSI rule type
        params: RSI parameters
    """
    try:
        if 'rsi' in chunk.columns:
            rsi_values = chunk['rsi'].tolist()
            plt.plot(x_values, rsi_values, color='bright_red', marker='█')
            
            # Add overbought/oversold lines
            overbought = params.get('overbought', 70)
            oversold = params.get('oversold', 30)
            
            plt.hline(overbought, color='red', style='dashed')
            plt.hline(oversold, color='green', style='dashed')
    except Exception as e:
        logger.print_error(f"Error adding RSI overlays: {e}")


def _add_macd_overlays_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add MACD overlays to chunk.
    
    Args:
        chunk: DataFrame chunk
        x_values: X-axis values
    """
    try:
        if 'macd' in chunk.columns:
            macd_values = chunk['macd'].tolist()
            plt.plot(x_values, macd_values, color='bright_cyan', marker='█')
        
        if 'macd_signal' in chunk.columns:
            signal_values = chunk['macd_signal'].tolist()
            plt.plot(x_values, signal_values, color='bright_yellow', marker='█')
        
        if 'macd_histogram' in chunk.columns:
            hist_values = chunk['macd_histogram'].tolist()
            plt.plot(x_values, hist_values, color='bright_white', marker='█')
    except Exception as e:
        logger.print_error(f"Error adding MACD overlays: {e}")


def _add_trading_signals_to_chunk(chunk: pd.DataFrame, x_values: list) -> None:
    """
    Add trading signals to chunk.
    
    Args:
        chunk: DataFrame chunk
        x_values: X-axis values
    """
    try:
        signal_columns = ['phld_signal', 'rsi_signal', 'macd_signal', 'stochastic_signal']
        
        for signal_col in signal_columns:
            if signal_col in chunk.columns:
                signals = chunk[signal_col]
                
                # Plot buy signals
                buy_indices = [i for i, signal in enumerate(signals) if signal == BUY]
                if buy_indices:
                    buy_prices = [chunk.iloc[i]['close'] for i in buy_indices]
                    buy_x = [x_values[i] for i in buy_indices]
                    plt.plot(buy_x, buy_prices, color='bright_green', marker='▲')
                
                # Plot sell signals
                sell_indices = [i for i, signal in enumerate(signals) if signal == SELL]
                if sell_indices:
                    sell_prices = [chunk.iloc[i]['close'] for i in sell_indices]
                    sell_x = [x_values[i] for i in sell_indices]
                    plt.plot(sell_x, sell_prices, color='bright_red', marker='▼')
    except Exception as e:
        logger.print_error(f"Error adding trading signals: {e}")
