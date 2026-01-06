# -*- coding: utf-8 -*-
# src/plotting/term_chunked_plot_indicators.py

"""
Indicator functions for terminal chunked plotting.
Contains all functions to add indicators to subplots.
"""

import pandas as pd
import plotext as plt
from typing import List

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
except ImportError:
    try:
        from src.common import logger
    except ImportError:
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.common import logger

def _add_macd_chart_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    """
    Add MACD chart to a separate subplot with proper scaling.

    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (List): X-axis values
    """
    try:
        # Add MACD lines with proper scaling
        if 'MACD_Line' in chunk.columns:
            macd_values = chunk['MACD_Line'].fillna(0).tolist()
            plt.plot(x_values, macd_values, color="blue+", label="MACD Line")

        if 'MACD_signal' in chunk.columns:
            signal_values = chunk['MACD_signal'].fillna(0).tolist()
            plt.plot(x_values, signal_values, color="orange+", label="signal Line")

        # Add MACD histogram if available
        if 'MACD_Histogram' in chunk.columns:
            histogram_values = chunk['MACD_Histogram'].fillna(0).tolist()
            # Use bars for histogram
            for i, value in enumerate(histogram_values):
                if value >= 0:
                    plt.plot([x_values[i], x_values[i]], [0, value], color="green+")
                else:
                    plt.plot([x_values[i], x_values[i]], [0, value], color="red+")

        # Add zero line for reference (plotext doesn't support axhline, so we'll skip it)
        # plt.axhline(y=0, color="white+", linestyle="-", alpha=0.5)

    except Exception as e:
        logger.print_error(f"Error adding MACD chart to subplot: {e}")


def _add_indicator_chart_to_subplot(
        chunk: pd.DataFrame,
        x_values: List,
        indicator_name: str,
        rule: str = "") -> None:
    """
    Add indicator chart to a separate subplot with proper scaling.

    Args:
        chunk (pd.DataFrame): DataFrame chunk
        x_values (List): X-axis values
        indicator_name (str): Name of the indicator
        rule (str): Original rule string for parameter extraction
    """
    try:
        indicator_upper = indicator_name.upper()

        # RSI indicators
        if indicator_upper.startswith('RSI'):
            _add_rsi_indicator_to_subplot(chunk, x_values, rule)

        # Stochastic indicators
        elif indicator_upper in ['STOCH', 'STOCHASTIC', 'STOCHOSCILLATOR']:
            _add_stochastic_indicator_to_subplot(chunk, x_values)

        # CCI indicator
        elif indicator_upper == 'CCI':
            _add_cci_indicator_to_subplot(chunk, x_values)

        # Bollinger Bands
        elif indicator_upper in ['BOLLINGER_BANDS', 'BB']:
            _add_bollinger_bands_to_subplot(chunk, x_values)

        # EMA indicators
        elif indicator_upper == 'EMA':
            _add_ema_indicator_to_subplot(chunk, x_values)

        # SMA indicators
        elif indicator_upper == 'SMA':
            _add_sma_indicator_to_subplot(chunk, x_values)

        # ADX indicator
        elif indicator_upper == 'ADX':
            _add_adx_indicator_to_subplot(chunk, x_values)

        # SAR indicator
        elif indicator_upper == 'SAR':
            _add_sar_indicator_to_subplot(chunk, x_values)

        # SuperTrend indicator
        elif indicator_upper == 'SUPERTREND':
            _add_supertrend_indicator_to_subplot(chunk, x_values)

        # ATR indicator
        elif indicator_upper == 'ATR':
            _add_atr_indicator_to_subplot(chunk, x_values)

        # Standard Deviation
        elif indicator_upper in ['STANDARD_DEVIATION', 'STDEV']:
            _add_std_indicator_to_subplot(chunk, x_values)

        # OBV indicator
        elif indicator_upper == 'OBV':
            _add_obv_indicator_to_subplot(chunk, x_values)

        # VWAP indicator
        elif indicator_upper == 'VWAP':
            _add_vwap_indicator_to_subplot(chunk, x_values)

        # HMA indicator
        elif indicator_upper == 'HMA':
            _add_hma_indicator_to_subplot(chunk, x_values)

        # Time Series Forecast
        elif indicator_upper in ['TIME_SERIES_FORECAST', 'TSF']:
            _add_tsf_indicator_to_subplot(chunk, x_values)

        # Monte Carlo
        elif indicator_upper in ['MONTE_CARLO', 'MONTE']:
            _add_monte_carlo_indicator_to_subplot(chunk, x_values)

        # Kelly Criterion
        elif indicator_upper in ['KELLY_CRITERION', 'KELLY']:
            _add_kelly_indicator_to_subplot(chunk, x_values)

        # Put/Call Ratio
        elif indicator_upper in ['PUT_Call_RATIO', 'PUTCallRATIO']:
            _add_putcall_indicator_to_subplot(chunk, x_values)

        # COT indicator
        elif indicator_upper == 'COT':
            _add_cot_indicator_to_subplot(chunk, x_values)

        # Fear & Greed
        elif indicator_upper in ['FEAR_GREED', 'FEARGREED']:
            _add_fear_greed_indicator_to_subplot(chunk, x_values)

        # Pivot Points
        elif indicator_upper in ['PIVOT_POINTS', 'PIVOT']:
            _add_pivot_points_to_subplot(chunk, x_values)

        # Fibonacci Retracement
        elif indicator_upper in ['FIBONACCI_RETRACEMENT', 'FIBO']:
            _add_fibonacci_indicator_to_subplot(chunk, x_values)

        # Donchian Channel
        elif indicator_upper in ['DONCHIAN_CHANNEL', 'DONCHAIN']:
            _add_donchian_indicator_to_subplot(chunk, x_values)

        # Wave indicator
        elif indicator_upper == 'WAVE':
            _add_wave_indicator_to_subplot(chunk, x_values)

        # Default: try to find any column with indicator name
        else:
            _add_generic_indicator_to_subplot(chunk, x_values, indicator_name)

    except Exception as e:
        logger.print_error(f"Error adding {indicator_name} chart to subplot: {e}")


def _add_rsi_indicator_to_subplot(chunk: pd.DataFrame, x_values: List, rule: str = "") -> None:
    try:
        # check for RSI column (case insensitive)
        rsi_col = None
        for col in chunk.columns:
            if col.lower() == 'rsi':
                rsi_col = col
                break

        if rsi_col:
            rsi_values = chunk[rsi_col].fillna(50).tolist()
            plt.plot(x_values, rsi_values, color="purple+", label="RSI")

            # Extract overbought/oversold levels from rule
            overbought_level = 70  # default
            oversold_level = 30  # default

            if rule and ':' in rule:
                try:
                    # Parse rule like "rsi:14,10,90,open" -> extract 10 and 90
                    params = rule.split(':')[1].split(',')
                    if len(params) >= 3:
                        oversold_level = float(params[1])  # second parameter
                        overbought_level = float(params[2])  # third parameter
                except (ValueError, IndexError):
                    # If parsing fails, Use defaults
                    pass

            # Add overbought/oversold lines with extracted levels
            plt.plot(x_values, [overbought_level] * len(x_values), color="red+")
            plt.plot(x_values, [oversold_level] * len(x_values), color="green+")
            plt.plot(x_values, [50] * len(x_values), color="white+")
        else:
            logger.print_warning("RSI column not found in chunk data")

    except Exception as e:
        logger.print_error(f"Error adding RSI indicator: {e}")


def _add_stochastic_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Look for different possible column names for Stochastic
        k_col = None
        d_col = None

        # check for various possible column names
        for col in chunk.columns:
            if 'stoch' in col.lower() and 'k' in col.lower():
                k_col = col
            elif 'stoch' in col.lower() and 'd' in col.lower():
                d_col = col

        # If not found, try exact matches
        if k_col is None and 'Stoch_K' in chunk.columns:
            k_col = 'Stoch_K'
        if d_col is None and 'Stoch_D' in chunk.columns:
            d_col = 'Stoch_D'

        # Plot %K line
        if k_col:
            k_values = chunk[k_col].fillna(50).tolist()
            plt.plot(x_values, k_values, color="blue+", label="%K")

        # Plot %D line
        if d_col:
            d_values = chunk[d_col].fillna(50).tolist()
            plt.plot(x_values, d_values, color="red+", label="%D")

        # Add overbought/oversold lines
        plt.plot(x_values, [80] * len(x_values), color="red+")
        plt.plot(x_values, [20] * len(x_values), color="green+")

    except Exception as e:
        logger.print_error(f"Error adding Stochastic indicator: {e}")


def _add_cci_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        if 'CCI' in chunk.columns:
            cci_values = chunk['CCI'].fillna(0).tolist()
        plt.plot(x_values, cci_values, color="orange+", label="CCI")

        # Add overbought/oversold lines
        plt.plot(x_values, [100] * len(x_values), color="red+")
        plt.plot(x_values, [-100] * len(x_values), color="green+")
        plt.plot(x_values, [0] * len(x_values), color="white+")

    except Exception as e:
        logger.print_error(f"Error adding CCI indicator: {e}")


def _add_bollinger_bands_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        if 'BB_Upper' in chunk.columns:
            upper_values = chunk['BB_Upper'].fillna(0).tolist()
            # Only plot if we have valid data
            if upper_values and any(v != 0 for v in upper_values):
                plt.plot(numeric_x_values, upper_values, color="green+", label="Upper Band")

        if 'BB_Middle' in chunk.columns:
            middle_values = chunk['BB_Middle'].fillna(0).tolist()
            # Only plot if we have valid data
            if middle_values and any(v != 0 for v in middle_values):
                plt.plot(numeric_x_values, middle_values, color="white+", label="Middle Band")

        if 'BB_lower' in chunk.columns:
            lower_values = chunk['BB_lower'].fillna(0).tolist()
            # Only plot if we have valid data
            if lower_values and any(v != 0 for v in lower_values):
                plt.plot(numeric_x_values, lower_values, color="red+", label="lower Band")

    except Exception as e:
        logger.print_error(f"Error adding Bollinger Bands: {e}")


def _add_ema_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Look for EMA columns
        ema_columns = [col for col in chunk.columns if col.startswith('EMA')]

        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        for ema_col in ema_columns:
            ema_values = chunk[ema_col].fillna(0).tolist()
            try:
                # Try to plot with numeric x_values
                plt.plot(numeric_x_values, ema_values, label=ema_col)
            except Exception as plot_error:
                # If plotting fails, skip this column
                continue

    except Exception as e:
        logger.print_error(f"Error adding EMA indicator: {e}")


def _add_sma_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Look for SMA columns (case insensitive)
        sma_columns = [col for col in chunk.columns if col.upper().startswith('SMA') or col.lower() == 'sma']

        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        for sma_col in sma_columns:
            sma_values = chunk[sma_col].fillna(0).tolist()
            try:
                # Try to plot with numeric x_values
                plt.plot(numeric_x_values, sma_values, color="blue+", label=sma_col)
            except Exception as plot_error:
                # If plotting fails, skip this column
                continue

        # Debug: print available columns if no SMA found
        if not sma_columns:
            logger.print_warning(f"No SMA columns found. available columns: {list(chunk.columns)}")

    except Exception as e:
        logger.print_error(f"Error adding SMA indicator: {e}")


def _add_adx_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        # check for both possible column naming conventions
        adx_column = None
        di_plus_column = None
        di_minus_column = None

        # Try ADX_* naming convention first (from calculation function)
        if 'ADX' in chunk.columns:
            adx_column = 'ADX'

        if 'ADX_PlusDI' in chunk.columns:
            di_plus_column = 'ADX_PlusDI'
        elif 'DI_Plus' in chunk.columns:
            di_plus_column = 'DI_Plus'

        if 'ADX_MinusDI' in chunk.columns:
            di_minus_column = 'ADX_MinusDI'
        elif 'DI_Minus' in chunk.columns:
            di_minus_column = 'DI_Minus'

        # Plot ADX
        if adx_column:
            adx_values = chunk[adx_column].fillna(0).tolist()
        # Only plot if we have valid data
        if adx_values and any(v != 0 for v in adx_values):
            plt.plot(numeric_x_values, adx_values, color="blue+", label="ADX")

        # Plot DI+
        if di_plus_column:
            di_plus_values = chunk[di_plus_column].fillna(0).tolist()
        # Only plot if we have valid data
        if di_plus_values and any(v != 0 for v in di_plus_values):
            plt.plot(numeric_x_values, di_plus_values, color="green+", label="DI+")

        # Plot DI-
        if di_minus_column:
            di_minus_values = chunk[di_minus_column].fillna(0).tolist()
        # Only plot if we have valid data
        if di_minus_values and any(v != 0 for v in di_minus_values):
            plt.plot(numeric_x_values, di_minus_values, color="red+", label="DI-")

        # Fallback to Diff column (DI+ - DI- difference)
        if not any([adx_column, di_plus_column, di_minus_column]) and 'Diff' in chunk.columns:
            diff_values = chunk['Diff'].fillna(0).tolist()
        if diff_values and any(v != 0 for v in diff_values):
            plt.plot(numeric_x_values, diff_values, color="blue+", label="DI+ - DI-")

    except Exception as e:
        logger.print_error(f"Error adding ADX indicator: {e}")


def _add_sar_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        # check for both possible column naming conventions
        sar_column = None

        # Try SAR naming convention first (from calculation function)
        if 'SAR' in chunk.columns:
            sar_column = 'SAR'

        # Plot SAR
        if sar_column:
            sar_values = chunk[sar_column].fillna(0).tolist()
        # Only plot if we have valid data
        if sar_values and any(v != 0 for v in sar_values):
            plt.plot(numeric_x_values, sar_values, color="yellow+", label="SAR")

        # Fallback to PPrice* naming convention (support and resistance levels)
        if not sar_column and 'PPrice1' in chunk.columns and 'PPrice2' in chunk.columns:
            pprice1_values = chunk['PPrice1'].fillna(0).tolist()
            pprice2_values = chunk['PPrice2'].fillna(0).tolist()

        # Plot PPrice1 (support level - SAR with buffer)
        if pprice1_values and any(v != 0 for v in pprice1_values):
            plt.plot(numeric_x_values, pprice1_values, color="yellow+", label="SAR Support")

        # Plot PPrice2 (resistance level - SAR with buffer)
        if pprice2_values and any(v != 0 for v in pprice2_values):
            plt.plot(numeric_x_values, pprice2_values, color="orange+", label="SAR Resistance")

    except Exception as e:
        logger.print_error(f"Error adding SAR indicator: {e}")


def _add_supertrend_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        # check for both possible column naming conventions
        supertrend_column = None

        # Try SuperTrend naming convention first (from calculation function)
        if 'SuperTrend' in chunk.columns:
            supertrend_column = 'SuperTrend'

        # Plot SuperTrend
        if supertrend_column:
            supertrend_values = chunk[supertrend_column].fillna(0).tolist()
        # Only plot if we have valid data
        if supertrend_values and any(v != 0 for v in supertrend_values):
            plt.plot(numeric_x_values, supertrend_values, color="green+", label="SuperTrend")

        # Fallback to PPrice* naming convention (support and resistance levels)
        if not supertrend_column and 'PPrice1' in chunk.columns and 'PPrice2' in chunk.columns:
            pprice1_values = chunk['PPrice1'].fillna(0).tolist()
            pprice2_values = chunk['PPrice2'].fillna(0).tolist()

        # Plot PPrice1 (support level - SuperTrend with buffer)
        if pprice1_values and any(v != 0 for v in pprice1_values):
            plt.plot(numeric_x_values, pprice1_values, color="green+", label="SuperTrend Support")

        # Plot PPrice2 (resistance level - SuperTrend with buffer)
        if pprice2_values and any(v != 0 for v in pprice2_values):
            plt.plot(numeric_x_values, pprice2_values, color="red+", label="SuperTrend Resistance")

    except Exception as e:
        logger.print_error(f"Error adding SuperTrend indicator: {e}")


def _add_atr_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        if 'ATR' in chunk.columns:
            atr_values = chunk['ATR'].fillna(0).tolist()
        plt.plot(numeric_x_values, atr_values, color="magenta+", label="ATR")

    except Exception as e:
        logger.print_error(f"Error adding ATR indicator: {e}")


def _add_std_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        # check for both possible column names
        std_column = None
        if 'StDev' in chunk.columns:
            std_column = 'StDev'
        elif 'Standard_Deviation' in chunk.columns:
            std_column = 'Standard_Deviation'
        elif 'Diff' in chunk.columns:
            std_column = 'Diff'  # STDEV values are stored in Diff column

        if std_column:
            std_values = chunk[std_column].fillna(0).tolist()
        # Only plot if we have valid data
        if std_values and any(v != 0 for v in std_values):
            plt.plot(numeric_x_values, std_values, color="yellow+", label="Std Dev")

    except Exception as e:
        logger.print_error(f"Error adding Standard Deviation indicator: {e}")


def _add_obv_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        # check for both possible column names
        obv_column = None
        if 'OBV' in chunk.columns:
            obv_column = 'OBV'
        elif 'Diff' in chunk.columns:
            obv_column = 'Diff'  # OBV values are stored in Diff column

        if obv_column:
            obv_values = chunk[obv_column].fillna(0).tolist()
        # Only plot if we have valid data
        if obv_values and any(v != 0 for v in obv_values):
            plt.plot(numeric_x_values, obv_values, color="blue+", label="OBV")

    except Exception as e:
        logger.print_error(f"Error adding OBV indicator: {e}")


def _add_vwap_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        if 'VWAP' in chunk.columns:
            vwap_values = chunk['VWAP'].fillna(0).tolist()
        plt.plot(numeric_x_values, vwap_values, color="orange+", label="VWAP")

    except Exception as e:
        logger.print_error(f"Error adding VWAP indicator: {e}")


def _add_hma_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        if 'HMA' in chunk.columns:
            hma_values = chunk['HMA'].fillna(0).tolist()
        # check if we have valid HMA values
        if any(v != 0 for v in hma_values):
            plt.plot(x_values, hma_values, color="purple+", label="HMA")

    except Exception as e:
        logger.print_error(f"Error adding HMA indicator: {e}")


def _add_tsf_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        if 'TSForecast' in chunk.columns:
            tsf_values = chunk['TSForecast'].fillna(0).tolist()
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        plt.plot(numeric_x_values, tsf_values, color="cyan+", label="TSF")

    except Exception as e:
        logger.print_error(f"Error adding TSF indicator: {e}")


def _add_monte_carlo_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        if 'MonteCarlo' in chunk.columns:
            mc_values = chunk['MonteCarlo'].fillna(0).tolist()
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        plt.plot(numeric_x_values, mc_values, color="green+", label="Monte Carlo")

    except Exception as e:
        logger.print_error(f"Error adding Monte Carlo indicator: {e}")


def _add_kelly_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        # check for both possible column names
        kelly_column = None
        if 'Kelly' in chunk.columns:
            kelly_column = 'Kelly'
        elif 'Kelly_Criterion' in chunk.columns:
            kelly_column = 'Kelly_Criterion'
        elif 'Diff' in chunk.columns:
            kelly_column = 'Diff'  # Kelly values are stored in Diff column

        if kelly_column:
            kelly_values = chunk[kelly_column].fillna(0).tolist()
        # Only plot if we have valid data
        if kelly_values and any(v != 0 for v in kelly_values):
            plt.plot(numeric_x_values, kelly_values, color="yellow+", label="Kelly")

    except Exception as e:
        logger.print_error(f"Error adding Kelly Criterion indicator: {e}")


def _add_putcall_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        if 'PutCallRatio' in chunk.columns:
            pcr_values = chunk['PutCallRatio'].fillna(50).tolist()
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
        plt.plot(numeric_x_values, pcr_values, color="red+", label="Put/Call Ratio")

        # Add neutral line
        plt.plot(numeric_x_values, [50] * len(numeric_x_values), color="white+")

    except Exception as e:
        logger.print_error(f"Error adding Put/Call Ratio indicator: {e}")


def _add_cot_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        if 'COT' in chunk.columns:
            cot_values = chunk['COT'].fillna(0).tolist()
        plt.plot(x_values, cot_values, color="blue+", label="COT")

    except Exception as e:
        logger.print_error(f"Error adding COT indicator: {e}")


def _add_fear_greed_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        # check for both possible column names
        fg_column = None
        if 'FearGreed' in chunk.columns:
            fg_column = 'FearGreed'
        elif 'Fear_Greed' in chunk.columns:
            fg_column = 'Fear_Greed'
        elif 'Diff' in chunk.columns:
            fg_column = 'Diff'  # Fear & Greed values are stored in Diff column

        if fg_column:
            fg_values = chunk[fg_column].fillna(50).tolist()
        # Only plot if we have valid data
        if fg_values and any(v != 50 for v in fg_values):
            plt.plot(numeric_x_values, fg_values, color="orange+", label="Fear & Greed")

        # Add extreme levels
        plt.plot(numeric_x_values, [80] * len(numeric_x_values), color="green+")
        plt.plot(numeric_x_values, [20] * len(numeric_x_values), color="red+")
        plt.plot(numeric_x_values, [50] * len(numeric_x_values), color="white+")

    except Exception as e:
        logger.print_error(f"Error adding Fear & Greed indicator: {e}")


def _add_pivot_points_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # check for both possible column naming conventions
        pivot_columns = []
        colors = []

        # Try Pivot_* naming convention first (from calculation function)
        if 'Pivot_PP' in chunk.columns:
            pivot_columns = ['Pivot_PP', 'Pivot_R1', 'Pivot_S1']
            colors = ['white+', 'green+', 'red+']
        # Fallback to short naming convention
        elif 'PP' in chunk.columns:
            pivot_columns = ['PP', 'R1', 'R2', 'R3', 'S1', 'S2', 'S3']
            colors = ['white+', 'green+', 'green+', 'green+', 'red+', 'red+', 'red+']

        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        for i, col in enumerate(pivot_columns):
            if col in chunk.columns:
                values = chunk[col].fillna(0).tolist()
                # Only plot if we have valid data
                if values and any(v != 0 for v in values):
                    plt.plot(numeric_x_values, values, color=colors[i], label=col)

    except Exception as e:
        logger.print_error(f"Error adding Pivot Points: {e}")


def _add_fibonacci_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        # check for both possible column naming conventions
        fib_columns = []
        colors = []

        # Try FibRetr_* naming convention first (from calculation function)
        if 'FibRetr_236' in chunk.columns:
            fib_columns = ['FibRetr_236', 'FibRetr_382', 'FibRetr_618']
            colors = ['yellow+', 'orange+', 'purple+']
        # Fallback to Fib_* naming convention
        elif 'Fib_236' in chunk.columns:
            fib_columns = ['Fib_0', 'Fib_236', 'Fib_382', 'Fib_500', 'Fib_618', 'Fib_786', 'Fib_100']
            colors = ['white+', 'yellow+', 'orange+', 'red+', 'purple+', 'blue+', 'green+']
        # Fallback to PPrice* naming convention (support and resistance levels)
        elif 'PPrice1' in chunk.columns and 'PPrice2' in chunk.columns:
            fib_columns = ['PPrice1', 'PPrice2']  # Support and resistance levels
            colors = ['green+', 'red+']  # Support (green), Resistance (red)

        for i, col in enumerate(fib_columns):
            if col in chunk.columns:
                values = chunk[col].fillna(0).tolist()
                # Only plot if we have valid data
                if values and any(v != 0 for v in values):
                    plt.plot(numeric_x_values, values, color=colors[i], label=col)

    except Exception as e:
        logger.print_error(f"Error adding Fibonacci Retracement: {e}")


def _add_donchian_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        # check for both possible column naming conventions
        upper_column = None
        middle_column = None
        lower_column = None

        # Try Donchain_* naming convention first (from calculation function)
        if 'Donchain_Upper' in chunk.columns:
            upper_column = 'Donchain_Upper'
        elif 'Donchian_Upper' in chunk.columns:
            upper_column = 'Donchian_Upper'

        if 'Donchain_Middle' in chunk.columns:
            middle_column = 'Donchain_Middle'
        elif 'Donchian_Middle' in chunk.columns:
            middle_column = 'Donchian_Middle'

        if 'Donchain_lower' in chunk.columns:
            lower_column = 'Donchain_lower'
        elif 'Donchian_lower' in chunk.columns:
            lower_column = 'Donchian_lower'

        # Plot upper band
        if upper_column:
            upper_values = chunk[upper_column].fillna(0).tolist()
        # Only plot if we have valid data
        if upper_values and any(v != 0 for v in upper_values):
            plt.plot(numeric_x_values, upper_values, color="green+", label="Upper")

        # Plot middle band
        if middle_column:
            middle_values = chunk[middle_column].fillna(0).tolist()
        # Only plot if we have valid data
        if middle_values and any(v != 0 for v in middle_values):
            plt.plot(numeric_x_values, middle_values, color="white+", label="Middle")

        # Plot lower band
        if lower_column:
            lower_values = chunk[lower_column].fillna(0).tolist()
        # Only plot if we have valid data
        if lower_values and any(v != 0 for v in lower_values):
            plt.plot(numeric_x_values, lower_values, color="red+", label="lower")

        # Fallback to PPrice* naming convention (support and resistance levels)
        if not any([upper_column, middle_column, lower_column]) and 'PPrice1' in chunk.columns and 'PPrice2' in chunk.columns:
            upper_column = 'PPrice2'  # Resistance level (upper band)
            middle_column = None  # No middle band in PPrice columns
            lower_column = 'PPrice1'  # Support level (lower band)

        # Plot upper band (PPrice2)
            upper_values = chunk[upper_column].fillna(0).tolist()
        if upper_values and any(v != 0 for v in upper_values):
            plt.plot(numeric_x_values, upper_values, color="green+", label="Upper")

        # Plot lower band (PPrice1)
            lower_values = chunk[lower_column].fillna(0).tolist()
        if lower_values and any(v != 0 for v in lower_values):
            plt.plot(numeric_x_values, lower_values, color="red+", label="lower")

    except Exception as e:
        logger.print_error(f"Error adding Donchian Channel: {e}")


def _add_wave_indicator_to_subplot(chunk: pd.DataFrame, x_values: List) -> None:
    try:
        # Ensure x_values are numeric for plotext compatibility
        numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]

        # check for Wave indicator columns with different naming conventions
        plot_wave_col = None
        plot_color_col = None
        plot_fastline_col = None
        ma_line_col = None

        # Try different column naming conventions
        if '_plot_wave' in chunk.columns:
            plot_wave_col = '_plot_wave'
        elif '_Plot_Wave' in chunk.columns:
            plot_wave_col = '_Plot_Wave'

        if '_plot_color' in chunk.columns:
            plot_color_col = '_plot_color'
        elif '_Plot_Color' in chunk.columns:
            plot_color_col = '_Plot_Color'

        if '_plot_fastline' in chunk.columns:
            plot_fastline_col = '_plot_fastline'
        elif '_Plot_FastLine' in chunk.columns:
            plot_fastline_col = '_Plot_FastLine'

        if 'MA_Line' in chunk.columns:
            ma_line_col = 'MA_Line'

        # Plot Wave line with dynamic colors based on signals
        if plot_wave_col and plot_color_col:
            wave_values = chunk[plot_wave_col].fillna(0).tolist()
            color_values = chunk[plot_color_col].fillna(0).tolist()

        # Create separate arrays for different signal types
        red_x = []
        red_y = []
        blue_x = []
        blue_y = []

        for i, (wave_val, color_val) in enumerate(zip(wave_values, color_values)):
            if wave_val != 0 and not pd.isna(wave_val):
                if color_val == 1:  # BUY signal
                    red_x.append(numeric_x_values[i])
                    red_y.append(wave_val)
                elif color_val == 2:  # SELL signal
                    blue_x.append(numeric_x_values[i])
                    blue_y.append(wave_val)

        # Plot red segments (BUY signals)
        if red_x and red_y:
            plt.plot(red_x, red_y, color="red+", label="Wave (BUY)")

        # Plot blue segments (SELL signals)
        if blue_x and blue_y:
            plt.plot(blue_x, blue_y, color="blue+", label="Wave (SELL)")

        # Plot Fast Line (thin red dotted line)
        if plot_fastline_col:
            fastline_values = chunk[plot_fastline_col].fillna(0).tolist()
        if fastline_values and any(v != 0 for v in fastline_values):
            plt.plot(numeric_x_values, fastline_values, color="red+", label="Fast Line")

        # Plot MA Line (light blue line)
        if ma_line_col:
            ma_values = chunk[ma_line_col].fillna(0).tolist()
        if ma_values and any(v != 0 for v in ma_values):
            plt.plot(numeric_x_values, ma_values, color="cyan+", label="MA Line")

        # Add zero line for reference
        plt.plot(numeric_x_values, [0] * len(numeric_x_values), color="white+", label="Zero Line")

    except Exception as e:
        logger.print_error(f"Error adding Wave indicator: {e}")


def _add_generic_indicator_to_subplot(chunk: pd.DataFrame, x_values: List, indicator_name: str) -> None:
    try:
        # Look for columns containing the indicator name
        indicator_columns = [col for col in chunk.columns if indicator_name.upper() in col.upper()]

        if not indicator_columns:
            # Try exact match (case insensitive)
            if indicator_name.lower() in [col.lower() for col in chunk.columns]:
                indicator_columns = [col for col in chunk.columns if col.lower() == indicator_name.lower()]
            elif indicator_name in chunk.columns:
                indicator_columns = [indicator_name]

        if indicator_columns:
            for col in indicator_columns:
                values = chunk[col].fillna(0).tolist()
                # Ensure x_values are numeric for plotext compatibility
                numeric_x_values = [float(x) if isinstance(x, (int, float)) else i for i, x in enumerate(x_values)]
                plt.plot(numeric_x_values, values, label=col)
        else:
            logger.print_warning(f"No columns found for indicator: {indicator_name}")

    except Exception as e:
        logger.print_error(f"Error adding generic indicator {indicator_name}: {e}")
