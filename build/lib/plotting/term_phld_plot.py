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
        
        # Validate input data - prevent ambiguous DataFrame truth value
        if df is None or (isinstance(df, pd.DataFrame) and df.empty):
            logger.print_error("DataFrame is None or empty, cannot plot")
            return
        
        # Check available data
        ohlc_columns = ['Open', 'High', 'Low', 'Close']
        # Make sure has_ohlc is a scalar boolean value
        has_ohlc = all(col in df.columns for col in ohlc_columns)
        if not isinstance(has_ohlc, bool):
            # If somehow has_ohlc is not a boolean, convert it explicitly
            has_ohlc = bool(has_ohlc)

        # Fix the ambiguous Series issue - use .any() method explicitly when checking for Volume
        has_volume = False  # Default to False
        if 'Volume' in df.columns:
            # Handle potential Series ambiguity with .any() method
            volume_notna = df['Volume'].notna()
            if isinstance(volume_notna, pd.Series):
                has_volume = volume_notna.any()
            else:
                has_volume = bool(volume_notna)

        # Debug output to see the actual values
        logger.print_debug(f"has_ohlc: {has_ohlc} (type: {type(has_ohlc)})")
        logger.print_debug(f"has_volume: {has_volume} (type: {type(has_volume)})")

        # Set up layout based on available data - PHLD typically has volume
        if bool(has_ohlc) and bool(has_volume):  # Explicit boolean conversion
            logger.print_info("PHLD plot with OHLC and Volume data detected.")
            plt.subplots(2, 1)  # Price + Volume panels
            main_plot_size = (140, 40)
        elif bool(has_ohlc):  # Ensure scalar boolean comparison
            plt.subplots(1, 1)  # Single price panel
            main_plot_size = (140, 30)
        else:
            plt.subplots(1, 1)  # Single indicator panel
            main_plot_size = (140, 30)
        
        plt.plot_size(*main_plot_size)
        plt.theme('matrix')  # Matrix theme for unified green style
        
        # Create time axis
        x_values = list(range(len(df)))
        
        # Convert rule to string - safely handle different rule types
        rule_str = rule.name if hasattr(rule, 'name') else str(rule)
        
        # MAIN PANEL: Candlestick Chart with PHLD overlays
        if bool(has_ohlc):  # Ensure scalar boolean comparison
            logger.print_info("Creating PHLD candlestick chart...")
            
            if bool(has_volume):  # Ensure scalar boolean comparison
                plt.subplot(1, 1)  # Top panel
            
            # Prepare OHLC data for candlestick - prevent Series comparison issues
            ohlc_data = {
                'Open': df['Open'].ffill().fillna(df['Close']).to_numpy().tolist(),
                'High': df['High'].ffill().fillna(df['Close']).to_numpy().tolist(),
                'Low': df['Low'].ffill().fillna(df['Close']).to_numpy().tolist(),
                'Close': df['Close'].ffill().fillna(df['Open']).to_numpy().tolist()
            }
            
            plt.candlestick(x_values, ohlc_data)
            plt.title(f"{title} - PHLD Candlestick Chart")
            
            if not bool(has_volume):  # Ensure scalar boolean comparison
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
        if bool(has_volume):  # Ensure scalar boolean comparison
            logger.print_info("Creating beautiful PHLD volume panel...")
            plt.subplot(2, 1)  # Bottom panel
            
            # Convert volume to integers, handling NaN values properly
            volume_values = df['Volume'].fillna(0).to_numpy().astype(float).astype(int).tolist()
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
        import traceback
        logger.print_debug(f"Stack trace: {traceback.format_exc()}")


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
                # Convert Series to numpy array then to list to avoid Series ambiguity issues
                values_series = df[col].fillna(0)
                values = values_series.to_numpy().tolist()

                # Skip empty data with proper scalar comparison
                if not any(abs(float(v)) > 1e-10 for v in values):
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
                        # Use numpy arrays to avoid Series comparison issues
                        close_values = df['Close'].fillna(0).to_numpy().tolist()
                        high_values = df['High'].fillna(0).to_numpy().tolist() if 'High' in df.columns else close_values
                        low_values = df['Low'].fillna(0).to_numpy().tolist() if 'Low' in df.columns else close_values

                        # Position signals above/below price action - scalar operations only
                        positioned_values = []
                        for i, sig in enumerate(values):
                            # Use precise numerical comparison instead of direct equality
                            if abs(float(sig) - 1.0) < 0.0001:  # Buy signal
                                positioned_values.append(low_values[i] * 0.995)  # Slightly below low
                            elif abs(float(sig) - (-1.0)) < 0.0001:  # Sell signal
                                positioned_values.append(high_values[i] * 1.005)  # Slightly above high
                            else:
                                positioned_values.append(None)  # No signal

                        # Plot as scatter for signals - safely filter None values
                        valid_indices = [i for i, v in enumerate(positioned_values) if v is not None]
                        if valid_indices:  # Check if we have any valid points
                            valid_x = [x_values[i] for i in valid_indices]
                            valid_y = [positioned_values[i] for i in valid_indices]

                            if valid_x and valid_y:
                                plt.scatter(valid_x, valid_y, color=color, label=label, marker="*")
                    else:
                        # Use list comprehension with explicit numerical comparison
                        buy_indices = [i for i, v in enumerate(values) if abs(float(v) - 1.0) < 0.0001]
                        sell_indices = [i for i, v in enumerate(values) if abs(float(v) - (-1.0)) < 0.0001]

                        if buy_indices:
                            buy_x = [x_values[i] for i in buy_indices]
                            buy_y = [1.0] * len(buy_x)
                            plt.scatter(buy_x, buy_y, color="green+", label=f"{label} Buy", marker="^")

                        if sell_indices:
                            sell_x = [x_values[i] for i in sell_indices]
                            sell_y = [-1.0] * len(sell_x)
                            plt.scatter(sell_x, sell_y, color="red+", label=f"{label} Sell", marker="v")

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
    try:
        header_line = "═" * 85
        print(f"\n{header_line}")
        print(f"{' PHLD PLOT STATISTICS':^85}")
        print(f"{rule_str:^85}")
        print(f"{header_line}")

        # Data overview - safe operations
        print(f"DATA OVERVIEW:")
        print(f"   Total Rows:     {len(df) if isinstance(df, pd.DataFrame) else 0}")
        print(f"   Total Columns:  {len(df.columns) if isinstance(df, pd.DataFrame) else 0}")
        print(f"   Rule Type:      {rule_str}")

        # OHLC statistics if available - ensure safe operations
        ohlc_columns = ['Open', 'High', 'Low', 'Close']
        has_ohlc = all(col in df.columns for col in ohlc_columns) if isinstance(df, pd.DataFrame) else False

        if has_ohlc:
            print(f"\nOHLC STATISTICS:")
            # Safe scalar extraction with error handling
            try:
                high_max = float(df['High'].max())
                low_min = float(df['Low'].min())
                close_final = float(df['Close'].iloc[-1])
                open_initial = float(df['Open'].iloc[0])

                print(f"   Highest:        {high_max:.5f}")
                print(f"   Lowest:         {low_min:.5f}")
                print(f"   Final Close:    {close_final:.5f}")
                print(f"   Initial Open:   {open_initial:.5f}")

                # Calculate price change safely
                price_change = close_final - open_initial
                if open_initial != 0:  # Avoid division by zero
                    price_change_pct = (price_change / open_initial) * 100
                else:
                    price_change_pct = 0.0

                direction_text = "UP" if price_change >= 0 else "DOWN"
                print(f"   Total Change:   {price_change:+.5f} ({price_change_pct:+.2f}%) {direction_text}")
            except Exception as e:
                print(f"   Error calculating OHLC statistics: {e}")

        # PHLD-specific statistics - safe extraction
        phld_indicators = ['PPrice1', 'PPrice2', 'Pressure', 'HL', 'PV', 'Direction']
        phld_found = [col for col in phld_indicators if col in df.columns] if isinstance(df, pd.DataFrame) else []

        if phld_found:
            print(f"\nPHLD INDICATORS:")
            for col in phld_found:
                try:
                    # Get clean data and safely extract statistics
                    col_data = df[col].dropna()
                    if len(col_data) > 0:
                        col_min = float(col_data.min())
                        col_max = float(col_data.max())
                        col_mean = float(col_data.mean())

                        if col == 'PPrice1':
                            print(f"   Predicted Low:   Min={col_min:.5f}, Max={col_max:.5f}, Avg={col_mean:.5f}")
                        elif col == 'PPrice2':
                            print(f"   Predicted High:  Min={col_min:.5f}, Max={col_max:.5f}, Avg={col_mean:.5f}")
                        elif col == 'Pressure':
                            print(f"   Pressure:        Min={col_min:.3f}, Max={col_max:.3f}, Avg={col_mean:.3f}")
                        elif col == 'HL':
                            print(f"   HL Range:        Min={col_min:.3f}, Max={col_max:.3f}, Avg={col_mean:.3f}")
                        elif col == 'PV':
                            print(f"   PV Indicator:    Min={col_min:.3f}, Max={col_max:.3f}, Avg={col_mean:.3f}")
                        elif col == 'Direction':
                            # Safely count values
                            buy_signals = int((col_data == 1).sum())
                            sell_signals = int((col_data == -1).sum())
                            no_trade = int((col_data == 0).sum())
                            print(f"   Direction:       Buy={buy_signals}, Sell={sell_signals}, NoTrade={no_trade}")
                except Exception as e:
                    print(f"   Error processing {col}: {e}")

        # Trading signals analysis - explicit scalar operations
        if isinstance(df, pd.DataFrame):
            signal_columns = [col for col in df.columns if 'signal' in col.lower() or 'direction' in col.lower()]
            if signal_columns:
                print(f"\nTRADING SIGNALS:")
                for col in signal_columns:
                    try:
                        col_data = df[col].dropna()
                        if len(col_data) > 0:
                            # Convert to scalar integers
                            buy_count = int((col_data == 1).sum())
                            sell_count = int((col_data == -1).sum())
                            total_signals = buy_count + sell_count

                            # Safe calculation of signal rate
                            if len(col_data) > 0:
                                signal_rate = (total_signals / len(col_data)) * 100
                            else:
                                signal_rate = 0.0

                            print(f"   {col}: Buy={buy_count}, Sell={sell_count}, Rate={signal_rate:.1f}%")
                    except Exception as e:
                        print(f"   Error processing {col} signals: {e}")

        # Prediction accuracy if available - safe checks and calculations
        try:
            if 'PPrice1' in df.columns and 'Low' in df.columns:
                pred_low_accuracy = _calculate_prediction_accuracy(df['PPrice1'], df['Low'])
                print(f"\nPREDICTION ACCURACY:")
                print(f"   Low Prediction:  {pred_low_accuracy:.1f}% accuracy")

            if 'PPrice2' in df.columns and 'High' in df.columns:
                pred_high_accuracy = _calculate_prediction_accuracy(df['PPrice2'], df['High'])
                print(f"   High Prediction: {pred_high_accuracy:.1f}% accuracy")
        except Exception as e:
            print(f"   Error calculating prediction accuracy: {e}")

        print(f"\n{header_line}")
        print(f"{'Beautiful PHLD Terminal Charts - Predict High Low Direction':^85}")
        print(f"{header_line}\n")

    except Exception as e:
        # Catch any errors that might occur in the statistics calculation
        logger.print_error(f"Error displaying PHLD statistics: {e}")
        import traceback
        logger.print_debug(f"Statistics error details: {traceback.format_exc()}")


def _calculate_prediction_accuracy(predicted: pd.Series, actual: pd.Series, tolerance: float = 0.001) -> float:
    """Calculate prediction accuracy within tolerance."""
    try:
        pred_clean = predicted.dropna()
        actual_clean = actual.dropna()
        
        if len(pred_clean) == 0 or len(actual_clean) == 0:
            return 0.0
        
        # Align series
        min_len = min(len(pred_clean), len(actual_clean))
        pred_vals = pred_clean.iloc[:min_len].to_numpy()  # Convert to numpy array
        actual_vals = actual_clean.iloc[:min_len].to_numpy()  # Convert to numpy array

        # Calculate accuracy using vectorized numpy operations
        differences = np.abs(pred_vals - actual_vals)
        tolerance_range = actual_vals * tolerance  # Percentage tolerance

        # Use numpy comparison for element-wise operation
        accurate_predictions = differences <= tolerance_range
        accurate_count = np.sum(accurate_predictions)

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
        
        # Validate input data
        if df is None or (isinstance(df, pd.DataFrame) and df.empty):
            logger.print_error("DataFrame is None or empty, cannot plot comparison")
            return

        x_values = list(range(len(df)))
        
        # Plot actual vs predicted - safe checking
        if 'High' in df.columns and 'PPrice2' in df.columns:
            # Safe conversion to numpy arrays then lists
            actual_high = df['High'].ffill().to_numpy().tolist()
            predicted_high = df['PPrice2'].ffill().to_numpy().tolist()

            plt.plot(x_values, actual_high, color="red+", label="Actual High", marker="^")
            plt.plot(x_values, predicted_high, color="yellow+", label="Predicted High", marker="D")
        
        if 'Low' in df.columns and 'PPrice1' in df.columns:
            # Safe conversion to numpy arrays then lists
            actual_low = df['Low'].ffill().to_numpy().tolist()
            predicted_low = df['PPrice1'].ffill().to_numpy().tolist()

            plt.plot(x_values, actual_low, color="blue+", label="Actual Low", marker="v")
            plt.plot(x_values, predicted_low, color="cyan+", label="Predicted Low", marker="D")
        
        plt.title(f"{title}")
        plt.xlabel("Time / Bar Index")
        plt.ylabel("Price Levels")
        plt.show()
        
        logger.print_success("PHLD comparison plot generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating PHLD comparison plot: {e}")
        import traceback
        logger.print_debug(f"Comparison plot error details: {traceback.format_exc()}")


def plot_phld_signals_only(df: pd.DataFrame, title: str = "PHLD Signals") -> None:
    """Plot only trading signals from PHLD analysis."""
    try:
        logger.print_info("Creating PHLD signals-only plot...")
        
        plt.clear_data()
        plt.clear_figure()
        plt.theme('matrix')
        plt.plot_size(120, 20)
        
        # Validate input data
        if df is None or (isinstance(df, pd.DataFrame) and df.empty):
            logger.print_error("DataFrame is None or empty, cannot plot signals")
            return

        x_values = list(range(len(df)))
        
        # Find signal columns safely
        signal_cols = [col for col in df.columns if isinstance(col, str) and ('signal' in col.lower() or 'direction' in col.lower())]

        colors = ["red+", "green+", "blue+", "yellow+", "magenta+"]
        
        for i, col in enumerate(signal_cols):
            if i < len(colors):
                # Convert to numpy then list to avoid Series comparison issues
                values = df[col].fillna(0).to_numpy().tolist()

                # Use explicit numeric comparison for signals
                buy_indices = [j for j, v in enumerate(values) if abs(float(v) - 1.0) < 0.0001]
                sell_indices = [j for j, v in enumerate(values) if abs(float(v) - (-1.0)) < 0.0001]

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
        import traceback
        logger.print_debug(f"Signals plot error details: {traceback.format_exc()}")
