# -*- coding: utf-8 -*-
# src/plotting/term_phld_plot.py

"""
Specialized terminal plotti            plt.candlestick(x_values, ohlc_data)
            plt.title(f"{title} - PHLD Candlestick Chart") for PHLD (Predict High Low Direction) indicators using plotext.
Beautiful candlestick charts with enhanced styling and trading signals.
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Optional, Union

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    # Fallback to relative imports when run as module
    from ..common import logger
    from ..common.constants import TradingRule, BUY, SELL, NOTRADE


def plot_phld_indicator_terminal(df: pd.DataFrame, 
                                rule: Union[TradingRule, str], 
                                title: str = "PHLD Terminal Plot",
                                output_path: Optional[str] = None) -> None:
    """
    Plot PHLD (Predict High Low Direction) indicators in terminal using candlestick charts.
    Specialized for displaying pressure, PV, HL, predicted prices, and trading signals.
    
    Args:
        df (pd.DataFrame): DataFrame with PHLD calculation results
        rule (TradingRule | str): Trading rule (should be PHLD-related)
        title (str): Title for the plot
        output_path (str, optional): Not used for terminal plots, kept for compatibility
    """
    try:
        logger.print_info("Generating PHLD terminal plot with candlestick charts...")
        
        # Clear any previous plots
        plt.clear_data()
        plt.clear_figure()
        
        # Validate input data
        if df is None or df.empty:
            logger.print_error("DataFrame is None or empty, cannot plot")
            return
        
        # Check available data
        ohlc_columns = ['Open', 'High', 'Low', 'Close']
        has_ohlc = all(col in df.columns for col in ohlc_columns)
        has_volume = 'Volume' in df.columns and df['Volume'].notna().any()
        
        # Set up layout based on available data - PHLD typically has volume
        if has_ohlc and has_volume:
            plt.subplots(2, 1)  # Price + Volume panels
            main_plot_size = (140, 40)
        elif has_ohlc:
            plt.subplots(1, 1)  # Single price panel
            main_plot_size = (140, 30)
        else:
            plt.subplots(1, 1)  # Single indicator panel
            main_plot_size = (140, 30)
        
        plt.plot_size(*main_plot_size)
        plt.theme('matrix')  # Matrix theme for unified green style
        
        # Create time axis
        x_values = list(range(len(df)))
        
        # Convert rule to string
        rule_str = rule.name if hasattr(rule, 'name') else str(rule)
        
        # MAIN PANEL: Candlestick Chart with PHLD overlays
        if has_ohlc:
            logger.print_info("Creating PHLD candlestick chart...")
            
            if has_volume:
                plt.subplot(1, 1)  # Top panel
            
            # Prepare OHLC data for candlestick
            ohlc_data = {
                'Open': df['Open'].ffill().fillna(df['Close']).tolist(),
                'High': df['High'].ffill().fillna(df['Close']).tolist(),
                'Low': df['Low'].ffill().fillna(df['Close']).tolist(),
                'Close': df['Close'].ffill().fillna(df['Open']).tolist()
            }
            
            plt.candlestick(x_values, ohlc_data)
            plt.title(f"{title} - PHLD Candlestick Chart")
            
            if not has_volume:
                plt.xlabel("Time / Bar Index")
            plt.ylabel("Price")
            
            # Add PHLD-specific overlays
            _add_phld_overlays(df, x_values)
            
        else:
            logger.print_info("Creating PHLD indicators chart...")
            plt.title(f"{title} - PHLD Indicators")
            plt.xlabel("Time / Bar Index")
            plt.ylabel("Values")
            
            # Plot PHLD indicators without OHLC base
            _add_phld_overlays(df, x_values, plot_base_indicators=True)
        
        # VOLUME PANEL (if available)
        if has_volume:
            logger.print_info("Creating beautiful PHLD volume panel...")
            plt.subplot(2, 1)  # Bottom panel
            
            # Convert volume to integers, handling NaN values properly
            volume_values = df['Volume'].fillna(0).astype(float).astype(int).tolist()
            plt.bar(x_values, volume_values, color="cyan+", label="Volume")
            
            plt.title("PHLD Trading Volume")
            plt.xlabel("Time / Bar Index")
            plt.ylabel("Volume")
        
        # Display the plot
        logger.print_info("Displaying PHLD terminal plot...")
        plt.show()
        
        # Show enhanced PHLD statistics
        _show_phld_statistics(df, rule_str)
        
        logger.print_success("PHLD terminal plot generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating PHLD terminal plot: {e}")
        logger.print_debug(f"Exception details: {type(e).__name__}: {e}")


def _add_phld_overlays(df: pd.DataFrame, x_values: list, plot_base_indicators: bool = False) -> None:
    """Add PHLD-specific overlays with beautiful styling."""
    
    # PHLD-specific color scheme
    phld_colors = {
        'predicted': "yellow+",    # Predicted prices - bright yellow
        'pressure': "magenta+",    # Pressure indicators - bright magenta  
        'hl': "cyan+",            # HL range - bright cyan
        'pv': "green+",           # PV indicators - bright green
        'signals': "red+",        # Trading signals - bright red
        'direction': "blue+",     # Direction - bright blue
        'other': "white"          # Other indicators - white
    }
    
    # Clean labels without emojis for better terminal compatibility
    phld_indicator_labels = {
        'PPrice1': 'Predicted Low', 'PPrice2': 'Predicted High', 'predicted_low': 'Predicted Low', 'predicted_high': 'Predicted High',
        'Pressure': 'Pressure', 'pressure': 'Pressure', 'HL': 'HL Range', 'PV': 'PV', 'Direction': 'Direction',
        'Signal': 'Signal', 'Buy': 'BUY', 'Sell': 'SELL', 'signal': 'Signal'
    }
    
    # Skip columns already handled by main chart
    skip_columns = {'Open', 'High', 'Low', 'Close', 'Volume', 'DateTime', 'Timestamp', 'Date', 'Time', 'index'}
    
    for col in df.columns:
        if col not in skip_columns and pd.api.types.is_numeric_dtype(df[col]):
            try:
                # First convert Series to a normal Python list to avoid any Series comparison issues
                values_series = df[col].fillna(0)
                values = [float(val) for val in values_series.values]

                # Skip empty data
                if not any(v != 0 for v in values):
                    continue
                
                # Determine color and label based on indicator type
                color = phld_colors['other']  # default
                label = col  # default to column name
                
                col_lower = col.lower()
                if 'pprice' in col_lower or 'predicted' in col_lower:
                    color = phld_colors['predicted']
                    label = phld_indicator_labels.get('PPrice1', col)
                elif 'pressure' in col_lower:
                    color = phld_colors['pressure']
                    label = phld_indicator_labels.get('Pressure', col)
                elif 'hl' in col_lower:
                    color = phld_colors['hl']
                    label = phld_indicator_labels.get('HL', col)
                elif 'pv' in col_lower:
                    color = phld_colors['pv']
                    label = phld_indicator_labels.get('PV', col)
                elif 'direction' in col_lower:
                    color = phld_colors['direction']
                    label = phld_indicator_labels.get('Direction', col)
                elif 'signal' in col_lower or 'buy' in col_lower or 'sell' in col_lower:
                    color = phld_colors['signals']
                    label = phld_indicator_labels.get('Signal', col)
                
                # Choose appropriate marker style
                if 'signal' in col_lower or 'direction' in col_lower:
                    # Trading signals - position relative to price action
                    if 'Close' in df.columns:
                        # Convert all Series to normal Python lists
                        close_values = df['Close'].fillna(0).values.tolist()
                        high_values = df['High'].fillna(0).values.tolist() if 'High' in df.columns else close_values
                        low_values = df['Low'].fillna(0).values.tolist() if 'Low' in df.columns else close_values

                        # Position signals above/below price action - using normal Python list operations
                        positioned_values = []
                        for i, sig in enumerate(values):
                            # Handle simple Python numeric comparison
                            if abs(sig - 1.0) < 0.0001:  # Buy signal (using approximate equality)
                                positioned_values.append(low_values[i] * 0.995)  # Slightly below low
                            elif abs(sig - (-1.0)) < 0.0001:  # Sell signal (using approximate equality)
                                positioned_values.append(high_values[i] * 1.005)  # Slightly above high
                            else:
                                positioned_values.append(None)

                        # Plot as scatter for signals
                        valid_indices = [i for i, v in enumerate(positioned_values) if v is not None]
                        valid_x = [x_values[i] for i in valid_indices]
                        valid_y = [positioned_values[i] for i in valid_indices]
                        
                        if valid_x and valid_y:
                            plt.scatter(valid_x, valid_y, color=color, label=label, marker="*")
                    else:
                        plt.scatter(x_values, values, color=color, label=label, marker="*")
                
                elif 'pprice' in col_lower or 'predicted' in col_lower:
                    # Predicted prices - thick lines with diamonds
                    plt.plot(x_values, values, color=color, label=label, marker="D")
                
                else:
                    # Other indicators - standard lines
                    marker = "+" if 'pressure' in col_lower else "."
                    plt.plot(x_values, values, color=color, label=label, marker=marker)
                
                logger.print_debug(f"Plotted PHLD indicator: {col}")
                
            except Exception as e:
                logger.print_warning(f"Could not plot PHLD indicator {col}: {e}")
                logger.print_debug(f"Exception details for {col}: {type(e).__name__}: {e}")


def _show_phld_statistics(df: pd.DataFrame, rule_str: str) -> None:
    """Display PHLD-specific statistics."""
    
    header_line = "═" * 85
    print(f"\n{header_line}")
    print(f"{' PHLD PLOT STATISTICS':^85}")
    print(f"{rule_str:^85}")
    print(f"{header_line}")
    
    # Data overview
    print(f"DATA OVERVIEW:")
    print(f"   Total Rows:     {len(df)}")
    print(f"   Total Columns:  {len(df.columns)}")
    print(f"   Rule Type:      {rule_str}")
    
    # OHLC statistics if available
    ohlc_columns = ['Open', 'High', 'Low', 'Close']
    if all(col in df.columns for col in ohlc_columns):
        print(f"\nOHLC STATISTICS:")
        print(f"   Highest:        {df['High'].max():.5f}")
        print(f"   Lowest:         {df['Low'].min():.5f}")
        print(f"   Final Close:    {df['Close'].iloc[-1]:.5f}")
        print(f"   Initial Open:   {df['Open'].iloc[0]:.5f}")
        
        price_change = df['Close'].iloc[-1] - df['Open'].iloc[0]
        price_change_pct = (price_change / df['Open'].iloc[0]) * 100
        # Ensure price_change is a scalar value, not a Series
        if isinstance(price_change, pd.Series):
            price_change = price_change.iloc[0] if not price_change.empty else 0
        direction_text = "UP" if price_change >= 0 else "DOWN"
        print(f"   Total Change:   {price_change:+.5f} ({price_change_pct:+.2f}%) {direction_text}")
    
    # PHLD-specific statistics
    phld_indicators = ['PPrice1', 'PPrice2', 'Pressure', 'HL', 'PV', 'Direction']
    phld_found = [col for col in phld_indicators if col in df.columns]
    
    if phld_found:
        print(f"\nPHLD INDICATORS:")
        for col in phld_found:
            try:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    if col == 'PPrice1':
                        print(f"   Predicted Low:   Min={col_data.min():.5f}, Max={col_data.max():.5f}, Avg={col_data.mean():.5f}")
                    elif col == 'PPrice2':
                        print(f"   Predicted High:  Min={col_data.min():.5f}, Max={col_data.max():.5f}, Avg={col_data.mean():.5f}")
                    elif col == 'Pressure':
                        print(f"   Pressure:        Min={col_data.min():.3f}, Max={col_data.max():.3f}, Avg={col_data.mean():.3f}")
                    elif col == 'HL':
                        print(f"   HL Range:        Min={col_data.min():.3f}, Max={col_data.max():.3f}, Avg={col_data.mean():.3f}")
                    elif col == 'PV':
                        print(f"   PV Indicator:    Min={col_data.min():.3f}, Max={col_data.max():.3f}, Avg={col_data.mean():.3f}")
                    elif col == 'Direction':
                        buy_signals = (col_data == 1).sum()
                        sell_signals = (col_data == -1).sum()
                        no_trade = (col_data == 0).sum()
                        print(f"   Direction:       Buy={buy_signals}, Sell={sell_signals}, NoTrade={no_trade}")
            except Exception:
                pass
    
    # Trading signals analysis
    signal_columns = [col for col in df.columns if 'signal' in col.lower() or 'direction' in col.lower()]
    if signal_columns:
        print(f"\nTRADING SIGNALS:")
        for col in signal_columns:
            try:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    buy_count = (col_data == 1).sum()
                    sell_count = (col_data == -1).sum()
                    total_signals = buy_count + sell_count
                    signal_rate = (total_signals / len(col_data)) * 100 if len(col_data) > 0 else 0
                    print(f"   {col}: Buy={buy_count}, Sell={sell_count}, Rate={signal_rate:.1f}%")
            except Exception:
                pass
    
    # Prediction accuracy if available
    if 'PPrice1' in df.columns and 'Low' in df.columns:
        try:
            pred_low_accuracy = _calculate_prediction_accuracy(df['PPrice1'], df['Low'])
            print(f"\nPREDICTION ACCURACY:")
            print(f"   Low Prediction:  {pred_low_accuracy:.1f}% accuracy")
        except Exception:
            pass
    
    if 'PPrice2' in df.columns and 'High' in df.columns:
        try:
            pred_high_accuracy = _calculate_prediction_accuracy(df['PPrice2'], df['High'])
            print(f"   High Prediction: {pred_high_accuracy:.1f}% accuracy")
        except Exception:
            pass
    
    print(f"\n{header_line}")
    print(f"{'Beautiful PHLD Terminal Charts - Predict High Low Direction':^85}")
    print(f"{header_line}\n")


def _calculate_prediction_accuracy(predicted: pd.Series, actual: pd.Series, tolerance: float = 0.001) -> float:
    """Calculate prediction accuracy within tolerance."""
    try:
        pred_clean = predicted.dropna()
        actual_clean = actual.dropna()
        
        if len(pred_clean) == 0 or len(actual_clean) == 0:
            return 0.0
        
        # Align series
        min_len = min(len(pred_clean), len(actual_clean))
        pred_vals = pred_clean.iloc[:min_len]
        actual_vals = actual_clean.iloc[:min_len]
        
        # Calculate accuracy within tolerance
        differences = abs(pred_vals - actual_vals)
        tolerance_range = actual_vals * tolerance  # percentage tolerance

        # Ensure we're dealing with scalar comparisons, not Series comparisons
        accurate_count = 0
        for diff, tol in zip(differences, tolerance_range):
            if diff <= tol:
                accurate_count += 1

        # Calculate percentage
        accuracy_pct = (accurate_count / len(pred_vals)) * 100 if len(pred_vals) > 0 else 0.0
        return accuracy_pct
    except Exception as e:
        logger.print_warning(f"Error calculating prediction accuracy: {e}")
        return 0.0


# Additional utility functions for PHLD plotting
def plot_phld_comparison(df: pd.DataFrame, title: str = "PHLD Comparison") -> None:
    """Compare predicted vs actual high/low prices."""
    try:
        logger.print_info("Creating PHLD prediction comparison plot...")
        
        plt.clear_data()
        plt.clear_figure()
        plt.theme('matrix')
        plt.plot_size(120, 30)
        
        x_values = list(range(len(df)))
        
        # Plot actual vs predicted
        if 'High' in df.columns and 'PPrice2' in df.columns:
            actual_high = df['High'].ffill().tolist()
            predicted_high = df['PPrice2'].ffill().tolist()
            
            plt.plot(x_values, actual_high, color="red+", label="Actual High", marker="^")
            plt.plot(x_values, predicted_high, color="yellow+", label="Predicted High", marker="D")
        
        if 'Low' in df.columns and 'PPrice1' in df.columns:
            actual_low = df['Low'].ffill().tolist()
            predicted_low = df['PPrice1'].ffill().tolist()
            
            plt.plot(x_values, actual_low, color="blue+", label="Actual Low", marker="v")
            plt.plot(x_values, predicted_low, color="cyan+", label="Predicted Low", marker="D")
        
        plt.title(f"{title}")
        plt.xlabel("Time / Bar Index")
        plt.ylabel("Price Levels")
        plt.show()
        
        logger.print_success("PHLD comparison plot generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating PHLD comparison plot: {e}")


def plot_phld_signals_only(df: pd.DataFrame, title: str = "PHLD Signals") -> None:
    """Plot only trading signals from PHLD analysis."""
    try:
        logger.print_info("Creating PHLD signals-only plot...")
        
        plt.clear_data()
        plt.clear_figure()
        plt.theme('matrix')
        plt.plot_size(120, 20)
        
        x_values = list(range(len(df)))
        
        # Find signal columns
        signal_cols = [col for col in df.columns if 'signal' in col.lower() or 'direction' in col.lower()]
        
        colors = ["red+", "green+", "blue+", "yellow+", "magenta+"]
        
        for i, col in enumerate(signal_cols):
            if i < len(colors):
                values = df[col].fillna(0).tolist()
                
                # Convert to buy/sell/hold visualization
                buy_indices = [j for j, v in enumerate(values) if v == 1]
                sell_indices = [j for j, v in enumerate(values) if v == -1]
                
                if buy_indices:
                    buy_x = [x_values[j] for j in buy_indices]
                    buy_y = [1] * len(buy_x)
                    plt.scatter(buy_x, buy_y, color="green+", label=f"{col} Buy", marker="^")
                
                if sell_indices:
                    sell_x = [x_values[j] for j in sell_indices]
                    sell_y = [-1] * len(sell_x)
                    plt.scatter(sell_x, sell_y, color="red+", label=f"{col} Sell", marker="v")
        
        plt.title(f"{title}")
        plt.xlabel("Time / Bar Index")
        plt.ylabel("Signal Type (1=Buy, -1=Sell)")
        plt.show()
        
        logger.print_success("PHLD signals plot generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating PHLD signals plot: {e}")
