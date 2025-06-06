# -*- coding: utf-8 -*-
# src/plotting/term_plot.py

"""
Terminal-based plotting using plotext for ASCII charts in terminal/SSH environments.
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


def plot_indicator_results_term(df_results: pd.DataFrame, 
                               rule: Union[TradingRule, str], 
                               title: str = "Terminal Plot",
                               output_path: Optional[str] = None) -> None:
    """
    Plot indicator results in terminal using plotext (ASCII charts).
    
    Args:
        df_results (pd.DataFrame): DataFrame with OHLCV and calculation results
        rule (TradingRule | str): Trading rule enum or string
        title (str): Title for the plot
        output_path (str, optional): Not used for terminal plots, kept for compatibility
    """
    try:
        logger.print_info("Generating terminal-based ASCII plot using plotext...")
        
        # Clear any previous plots
        plt.clear_data()
        plt.clear_figure()
        
        # Validate input data
        if df_results is None or df_results.empty:
            logger.print_error("DataFrame is None or empty, cannot plot")
            return
        
        # Check for required OHLC columns
        required_columns = ['Open', 'High', 'Low', 'Close']
        missing_columns = [col for col in required_columns if col not in df_results.columns]
        if missing_columns:
            logger.print_error(f"Missing required columns: {missing_columns}")
            return
        
        # Convert rule to string for processing
        rule_str = rule.name if hasattr(rule, 'name') else str(rule)
        
        # Prepare data for plotting
        df = df_results.copy()
        
        # Create time axis - use index or create sequential numbers
        if df.index.name == 'DateTime' or 'DateTime' in df.columns:
            time_col = df.index if df.index.name == 'DateTime' else df['DateTime']
            # Convert to numeric for plotext (it doesn't handle datetime well)
            x_values = list(range(len(df)))
            x_labels = [str(t)[:10] if hasattr(t, 'strftime') else str(t) for t in time_col]
        else:
            x_values = list(range(len(df)))
            x_labels = [f"Bar {i}" for i in x_values]
        
        # Determine the best chart layout based on available data
        has_volume = 'Volume' in df.columns and not df['Volume'].isna().all()
        
        # Set up subplots: main chart + volume if available
        if has_volume:
            plt.subplots(2, 1)  # Two panels: price + volume
            main_plot_size = (140, 35)  # Larger size for dual panel
        else:
            plt.subplots(1, 1)  # Single panel
            main_plot_size = (140, 25)  # Standard size for single panel
        
        plt.plot_size(*main_plot_size)
        
        # Use unified matrix green theme for all rules
        plt.theme('matrix')
        
        # MAIN CHART: Beautiful Candlestick Visualization
        logger.print_info("Creating beautiful candlestick chart...")
        
        if has_volume:
            plt.subplot(1, 1)  # Top panel for price
        
        # Prepare OHLC data for candlestick chart
        ohlc_data = {
            'Open': df['Open'].ffill().fillna(df['Close']).tolist(),
            'High': df['High'].ffill().fillna(df['Close']).tolist(),
            'Low': df['Low'].ffill().fillna(df['Close']).tolist(),
            'Close': df['Close'].ffill().fillna(df['Open']).tolist()
        }
        
        # Create the beautiful candlestick chart
        plt.candlestick(x_values, ohlc_data)
        
        # Set price chart title and labels
        price_title = f"{title} - Financial Chart (Matrix Green Theme)"
        plt.title(price_title)
        
        if not has_volume:
            plt.xlabel("Time / Bar Index")
        plt.ylabel("Price")
        
        # Add financial indicators and overlays based on the trading rule
        if rule_str.upper() in ['PHLD', 'PREDICT_HIGH_LOW_DIRECTION']:
            _add_phld_indicators_term(df, x_values)
        elif rule_str.upper() in ['PV', 'PRESSURE_VECTOR']:
            _add_pv_indicators_term(df, x_values)
        elif rule_str.upper() in ['AUTO', 'AUTO_DISPLAY_ALL']:
            _add_auto_indicators_term(df, x_values)
        
        # Add predicted price lines if available
        if 'PPrice1' in df.columns:  # Predicted Low
            pprice1_values = df['PPrice1'].fillna(0).tolist()
            plt.plot(x_values, pprice1_values, color="green+", label="Predicted Low", marker=".")
        
        if 'PPrice2' in df.columns:  # Predicted High
            pprice2_values = df['PPrice2'].fillna(0).tolist()
            plt.plot(x_values, pprice2_values, color="red+", label="Predicted High", marker=".")
        
        # Add trading signals if available
        if 'Direction' in df.columns:
            _add_trading_signals_term(df, x_values, ohlc_data)
        
        # VOLUME PANEL: Beautiful Volume Bars (if volume data exists)
        if has_volume:
            logger.print_info("Creating volume panel...")
            plt.subplot(2, 1)  # Bottom panel for volume
            
            # Convert volume to integers, handling NaN values properly
            volume_values = df['Volume'].fillna(0).astype(float).astype(int).tolist()
            plt.bar(x_values, volume_values, color="cyan+", label="Volume")
            
            plt.title("Trading Volume")
            plt.xlabel("Time / Bar Index")
            plt.ylabel("Volume")
        
        # Display the plot
        logger.print_info("Displaying terminal plot...")
        plt.show()
        
        # Show additional statistics
        _show_terminal_statistics(df, rule_str)
        
        logger.print_success("Terminal plot generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating terminal plot: {e}")
        logger.print_debug(f"Exception details: {type(e).__name__}: {e}")


def _add_phld_indicators_term(df: pd.DataFrame, x_values: list) -> None:
    """Add PHLD-specific indicators to terminal plot with beautiful styling."""
    
    # Add HL (High-Low range in points) with enhanced styling
    if 'HL' in df.columns:
        hl_values = df['HL'].fillna(0).tolist()
        plt.plot(x_values, hl_values, color="orange+", label="HL Range", marker=".")
    
    # Add Pressure with gradient-like effect
    if 'Pressure' in df.columns:
        pressure_values = df['Pressure'].fillna(0).tolist()
        plt.plot(x_values, pressure_values, color="magenta+", label="Pressure", marker="x")
    
    # Add Pressure Vector (PV) with distinct styling
    if 'PV' in df.columns:
        pv_values = df['PV'].fillna(0).tolist()
        plt.plot(x_values, pv_values, color="yellow+", label="PV", marker="*")


def _add_pv_indicators_term(df: pd.DataFrame, x_values: list) -> None:
    """Add Pressure Vector specific indicators to terminal plot with beautiful styling."""
    
    if 'PV' in df.columns:
        pv_values = df['PV'].fillna(0).tolist()
        plt.plot(x_values, pv_values, color="cyan+", label="Pressure Vector", marker="*")
    
    if 'Pressure' in df.columns:
        pressure_values = df['Pressure'].fillna(0).tolist()
        plt.plot(x_values, pressure_values, color="blue+", label="Pressure Force", marker="x")


def _add_auto_indicators_term(df: pd.DataFrame, x_values: list) -> None:
    """Add all available indicators for AUTO mode with beautiful color scheme."""
    
    # Enhanced color palette for better visual distinction
    colors = [
        "yellow+", "magenta+", "cyan+", "green+", "red+", "blue+", 
        "orange", "brown", "white", "gray"
    ]
    
    # Enhanced marker set for variety
    markers = [".", "*", "x", "+", "o", "^", "v", "s", "d"]
    
    color_index = 0
    marker_index = 0
    
    # Standard columns to skip
    skip_columns = {
        'Open', 'High', 'Low', 'Close', 'Volume', 'DateTime', 'Timestamp', 
        'Date', 'Time', 'Index', 'index'
    }
    
    for col in df.columns:
        if col not in skip_columns and pd.api.types.is_numeric_dtype(df[col]):
            try:
                values = df[col].fillna(0).tolist()
                color = colors[color_index % len(colors)]
                marker = markers[marker_index % len(markers)]
                
                # Simple label without emojis
                label = col
                plt.plot(x_values, values, color=color, label=label, marker=marker)
                
                color_index += 1
                marker_index += 1
                
            except Exception as e:
                logger.print_warning(f"Could not plot column {col}: {e}")


def _add_trading_signals_term(df: pd.DataFrame, x_values: list, ohlc_data: dict) -> None:
    """Add trading signal markers to the plot."""
    
    direction_values = df['Direction'].fillna(NOTRADE).tolist()
    
    # Find buy and sell signals
    buy_indices = [i for i, direction in enumerate(direction_values) if direction == BUY]
    sell_indices = [i for i, direction in enumerate(direction_values) if direction == SELL]
    
    # Get high and low values from OHLC data
    high_values = ohlc_data['High']
    low_values = ohlc_data['Low']
    
    if buy_indices:
        buy_x = [x_values[i] for i in buy_indices]
        buy_y = [low_values[i] * 0.995 for i in buy_indices]  # Place below Low
        plt.scatter(buy_x, buy_y, color="green+", marker="^", label="BUY Signal")
    
    if sell_indices:
        sell_x = [x_values[i] for i in sell_indices]
        sell_y = [high_values[i] * 1.005 for i in sell_indices]  # Place above High
        plt.scatter(sell_x, sell_y, color="red+", marker="v", label="SELL Signal")


def _show_terminal_statistics(df: pd.DataFrame, rule_str: str) -> None:
    """Display beautiful summary statistics in terminal."""
    
    # Create a beautiful header
    header_line = "=" * 80
    print(f"\n{header_line}")
    print(f"{'TERMINAL PLOT STATISTICS':^80}")
    print(f"{'Trading Rule: ' + rule_str.upper():^80}")
    print(f"{header_line}")
    
    # Basic OHLC statistics
    if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
        print(f"PRICE STATISTICS:")
        print(f"   Highest Price:  {df['High'].max():.5f}")
        print(f"   Lowest Price:   {df['Low'].min():.5f}")
        print(f"   Close Price:    {df['Close'].iloc[-1]:.5f}")
        print(f"   Open Price:     {df['Open'].iloc[0]:.5f}")
        print(f"   Price Range:    {df['High'].max() - df['Low'].min():.5f}")
        
        # Calculate price movement
        price_change = df['Close'].iloc[-1] - df['Open'].iloc[0]
        price_change_pct = (price_change / df['Open'].iloc[0]) * 100
        direction_symbol = "+" if price_change >= 0 else "-"
        print(f"   Total Change:   {price_change:+.5f} ({price_change_pct:+.2f}%)")
    
    # Volume statistics
    if 'Volume' in df.columns and not df['Volume'].isna().all():
        print(f"\nVOLUME STATISTICS:")
        print(f"   Total Volume:   {df['Volume'].sum():,.0f}")
        print(f"   Avg Volume:     {df['Volume'].mean():.0f}")
        print(f"   Max Volume:     {df['Volume'].max():,.0f}")
        print(f"   Min Volume:     {df['Volume'].min():,.0f}")
    
    # Trading signals statistics
    if 'Direction' in df.columns:
        buy_count = (df['Direction'] == BUY).sum()
        sell_count = (df['Direction'] == SELL).sum()
        notrade_count = (df['Direction'] == NOTRADE).sum()
        
        print(f"\nTRADING SIGNALS:")
        print(f"   BUY Signals:    {buy_count}")
        print(f"   SELL Signals:   {sell_count}")
        print(f"   NO TRADE:       {notrade_count}")
        print(f"   Total Bars:     {len(df)}")
        
        # Signal efficiency
        total_signals = buy_count + sell_count
        if total_signals > 0:
            signal_rate = (total_signals / len(df)) * 100
            print(f"   Signal Rate:     {signal_rate:.1f}%")
    
    # Rule-specific statistics
    if rule_str.upper() in ['PHLD', 'PREDICT_HIGH_LOW_DIRECTION']:
        print(f"\nPHLD INDICATORS:")
        if 'HL' in df.columns:
            print(f"   Avg HL Range:   {df['HL'].mean():.3f} points")
            print(f"   Max HL Range:   {df['HL'].max():.3f} points")
            print(f"   Min HL Range:   {df['HL'].min():.3f} points")
        
        if 'Pressure' in df.columns:
            print(f"   Avg Pressure:   {df['Pressure'].mean():.3f}")
            print(f"   Max Pressure:   {df['Pressure'].max():.3f}")
            print(f"   Min Pressure:   {df['Pressure'].min():.3f}")
        
        if 'PV' in df.columns:
            print(f"   Avg PV:         {df['PV'].mean():.3f}")
            print(f"   Max PV:         {df['PV'].max():.3f}")
            print(f"   Min PV:         {df['PV'].min():.3f}")
    
    # Prediction accuracy (if available)
    if 'PPrice1' in df.columns and 'PPrice2' in df.columns:
        print(f"\nPREDICTION STATISTICS:")
        pprice1_accuracy = _calculate_prediction_accuracy(df, 'PPrice1', 'Low')
        pprice2_accuracy = _calculate_prediction_accuracy(df, 'PPrice2', 'High')
        if pprice1_accuracy is not None:
            print(f"   Low Prediction:  {pprice1_accuracy:.1f}% accuracy")
        if pprice2_accuracy is not None:
            print(f"   High Prediction: {pprice2_accuracy:.1f}% accuracy")
    
    # Footer
    print(f"\n{header_line}")
    print(f"{'Terminal Charts with Plotext Candlesticks':^80}")
    print(f"{'Perfect for SSH/Docker/Terminal Trading Analysis':^80}")
    print(f"{header_line}\n")


def _calculate_prediction_accuracy(df: pd.DataFrame, pred_col: str, actual_col: str) -> Optional[float]:
    """Calculate prediction accuracy percentage."""
    try:
        predictions = df[pred_col].dropna()
        actuals = df[actual_col].dropna()
        
        if len(predictions) == 0 or len(actuals) == 0:
            return None
        
        # Align data by index
        common_idx = predictions.index.intersection(actuals.index)
        if len(common_idx) == 0:
            return None
            
        pred_values = predictions.loc[common_idx]
        actual_values = actuals.loc[common_idx]
        
        # Calculate accuracy as inverse of mean percentage error
        percentage_errors = abs((pred_values - actual_values) / actual_values) * 100
        mean_error = percentage_errors.mean()
        accuracy = max(0, 100 - mean_error)
        
        return accuracy
    except Exception:
        return None
