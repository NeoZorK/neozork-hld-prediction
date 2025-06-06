# -*- coding: utf-8 -*-
# src/plotting/term_phld_plot.py

"""
Specialized terminal plotting for PHLD (Predict High Low Direction) indicators using plotext.
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
    Plot PHLD (Predict High Low Direction) indicators in terminal using beautiful candlestick charts.
    Specialized for displaying pressure, PV, HL, predicted prices, and trading signals.
    
    Args:
        df (pd.DataFrame): DataFrame with PHLD calculation results
        rule (TradingRule | str): Trading rule (should be PHLD-related)
        title (str): Title for the plot
        output_path (str, optional): Not used for terminal plots, kept for compatibility
    """
    try:
        logger.print_info("Generating beautiful PHLD terminal plot with candlestick charts...")
        
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
        has_volume = 'Volume' in df.columns and not df['Volume'].isna().all()
        
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
        plt.theme('matrix')  # Matrix theme for PHLD (high-tech trading feel)
        
        # Create time axis
        x_values = list(range(len(df)))
        
        # Convert rule to string
        rule_str = rule.name if hasattr(rule, 'name') else str(rule)
        
        # MAIN PANEL: Beautiful Candlestick Chart with PHLD overlays
        if has_ohlc:
            logger.print_info("Creating beautiful PHLD candlestick chart...")
            
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
            plt.title(f"🎯 {title} - Beautiful PHLD Candlestick Chart")
            
            if not has_volume:
                plt.xlabel("Time / Bar Index")
            plt.ylabel("Price")
            
            # Add PHLD-specific overlays
            _add_phld_overlays(df, x_values)
            
        else:
            logger.print_info("Creating beautiful PHLD indicators chart...")
            plt.title(f"🎯 {title} - Beautiful PHLD Indicators")
            plt.xlabel("Time / Bar Index")
            plt.ylabel("Values")
            
            # Plot PHLD indicators without OHLC base
            _add_phld_overlays(df, x_values, plot_base_indicators=True)
        
        # VOLUME PANEL (if available)
        if has_volume:
            logger.print_info("Creating beautiful PHLD volume panel...")
            plt.subplot(2, 1)  # Bottom panel
            
            volume_values = df['Volume'].fillna(0).tolist()
            plt.bar(x_values, volume_values, color="cyan+", label="📊 Volume")
            
            plt.title("📊 PHLD Trading Volume")
            plt.xlabel("Time / Bar Index")
            plt.ylabel("Volume")
        
        # Display the plot
        logger.print_info("Displaying beautiful PHLD terminal plot...")
        plt.show()
        
        # Show enhanced PHLD statistics
        _show_phld_statistics(df, rule_str)
        
        logger.print_success("Beautiful PHLD terminal plot generated successfully!")
        
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


def _plot_ohlc_base_phld(df: pd.DataFrame, x_values: list) -> None:
    """Plot base OHLC data for PHLD visualization."""
    
    # Plot with more subdued colors to make predicted prices stand out
    open_values = df['Open'].fillna(method='ffill').fillna(0).tolist()
    high_values = df['High'].fillna(method='ffill').fillna(0).tolist()
    low_values = df['Low'].fillna(method='ffill').fillna(0).tolist()
    close_values = df['Close'].fillna(method='ffill').fillna(0).tolist()
    
    plt.plot(x_values, open_values, color="green", label="Open", marker="o")
    plt.plot(x_values, high_values, color="gray", label="High", marker="^")
    plt.plot(x_values, low_values, color="gray", label="Low", marker="v")
    plt.plot(x_values, close_values, color="red", label="Close", marker="s")


def _plot_predicted_prices_phld(df: pd.DataFrame, x_values: list) -> None:
    """Plot predicted high and low prices - the main PHLD feature."""
    
    # Predicted Low (PPrice1)
    if 'PPrice1' in df.columns:
        pprice1_values = df['PPrice1'].fillna(method='ffill').fillna(0).tolist()
        plt.plot(x_values, pprice1_values, color="green+", label="🎯 Predicted Low", 
                marker="D")
        logger.print_debug("Added Predicted Low (PPrice1) to plot")
    
    # Predicted High (PPrice2)
    if 'PPrice2' in df.columns:
        pprice2_values = df['PPrice2'].fillna(method='ffill').fillna(0).tolist()
        plt.plot(x_values, pprice2_values, color="red+", label="🎯 Predicted High", 
                marker="D")
        logger.print_debug("Added Predicted High (PPrice2) to plot")
    
    # Alternative column names for predicted prices
    if 'predicted_low' in df.columns:
        pred_low_values = df['predicted_low'].fillna(method='ffill').fillna(0).tolist()
        plt.plot(x_values, pred_low_values, color="green+", label="🎯 Predicted Low", 
                marker="D")
    
    if 'predicted_high' in df.columns:
        pred_high_values = df['predicted_high'].fillna(method='ffill').fillna(0).tolist()
        plt.plot(x_values, pred_high_values, color="red+", label="🎯 Predicted High", 
                marker="D")


def _plot_pressure_indicators_phld(df: pd.DataFrame, x_values: list) -> None:
    """Plot pressure-related indicators for PHLD."""
    
    # Pressure
    if 'Pressure' in df.columns:
        pressure_values = df['Pressure'].fillna(0).tolist()
        # Normalize pressure to fit with price scale for better visualization
        if pressure_values and max(abs(p) for p in pressure_values) > 0:
            plt.plot(x_values, pressure_values, color="blue+", label="💨 Pressure", 
                    marker="x")
            logger.print_debug("Added Pressure indicator to plot")
    
    # Pressure Vector (PV)
    if 'PV' in df.columns:
        pv_values = df['PV'].fillna(0).tolist()
        plt.plot(x_values, pv_values, color="orange+", label="🎯 Pressure Vector", 
                marker="+")
        logger.print_debug("Added Pressure Vector (PV) to plot")
    
    # Alternative column names
    if 'pressure_vector' in df.columns:
        pv_alt_values = df['pressure_vector'].fillna(0).tolist()
        plt.plot(x_values, pv_alt_values, color="yellow", label="🎯 PV", marker="+")
    
    if 'pressure' in df.columns and 'Pressure' not in df.columns:
        pressure_alt_values = df['pressure'].fillna(0).tolist()
        plt.plot(x_values, pressure_alt_values, color="blue", label="💨 Press", marker="x")


def _plot_hl_indicator_phld(df: pd.DataFrame, x_values: list) -> None:
    """Plot HL (High-Low range in points) indicator."""
    
    if 'HL' in df.columns:
        hl_values = df['HL'].fillna(0).tolist()
        plt.plot(x_values, hl_values, color="brown+", label="📏 HL Points", 
                marker=".")
        logger.print_debug("Added HL (High-Low points) to plot")
    
    # Alternative column names
    if 'hl' in df.columns and 'HL' not in df.columns:
        hl_alt_values = df['hl'].fillna(0).tolist()
        plt.plot(x_values, hl_alt_values, color="brown", label="📏 HL", marker=".")


def _plot_trading_signals_phld(df: pd.DataFrame, x_values: list) -> None:
    """Plot trading signals for PHLD."""
    
    if 'Direction' in df.columns:
        direction_values = df['Direction'].fillna(NOTRADE).tolist()
        
        # Create signal markers
        buy_indices = [i for i, d in enumerate(direction_values) if d == BUY]
        sell_indices = [i for i, d in enumerate(direction_values) if d == SELL]
        
        if buy_indices:
            buy_x = [x_values[i] for i in buy_indices]
            # Use a fixed signal level for better visibility
            buy_y = [1] * len(buy_indices)  # Fixed level for signals
            plt.scatter(buy_x, buy_y, color="green+", marker="▲", label="🔼 BUY Signal")
            logger.print_debug(f"Added {len(buy_indices)} BUY signals to plot")
        
        if sell_indices:
            sell_x = [x_values[i] for i in sell_indices]
            sell_y = [-1] * len(sell_indices)  # Fixed level for signals
            plt.scatter(sell_x, sell_y, color="red+", marker="▼", label="🔽 SELL Signal")
            logger.print_debug(f"Added {len(sell_indices)} SELL signals to plot")
    
    # Alternative column names
    if 'direction' in df.columns and 'Direction' not in df.columns:
        direction_alt = df['direction'].fillna(NOTRADE).tolist()
        buy_alt = [i for i, d in enumerate(direction_alt) if d == BUY]
        sell_alt = [i for i, d in enumerate(direction_alt) if d == SELL]
        
        if buy_alt:
            plt.scatter([x_values[i] for i in buy_alt], [1] * len(buy_alt), 
                       color="green", marker="^", label="🔼 BUY")
        if sell_alt:
            plt.scatter([x_values[i] for i in sell_alt], [-1] * len(sell_alt), 
                       color="red", marker="v", label="🔽 SELL")


def _plot_volume_phld(df: pd.DataFrame, x_values: list) -> None:
    """Plot volume data for PHLD (normalized to fit with other indicators)."""
    
    volume_col = 'Volume' if 'Volume' in df.columns else 'TickVolume'
    volume_values = df[volume_col].fillna(0).tolist()
    
    if volume_values and max(volume_values) > 0:
        # Normalize volume to a small scale to not overwhelm other indicators
        max_vol = max(volume_values)
        volume_normalized = [v / max_vol * 0.5 for v in volume_values]  # Scale to 0-0.5 range
        
        plt.bar(x_values, volume_normalized, color="gray", 
               label=f"📊 {volume_col} (norm)")
        logger.print_debug(f"Added normalized {volume_col} to plot")


def _show_phld_statistics(df: pd.DataFrame, rule_str: str) -> None:
    """Display detailed PHLD statistics in terminal."""
    
    print("\n" + "="*80)
    print(f"🎯 PHLD TERMINAL PLOT STATISTICS - {rule_str.upper()}")
    print("="*80)
    
    # Basic data info
    print(f"📊 DATA OVERVIEW:")
    print(f"   Total Bars:        {len(df)}")
    print(f"   Columns Available: {len(df.columns)}")
    print(f"   Data Range:        Bar 0 to {len(df)-1}")
    
    # OHLC statistics
    if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
        print(f"\n📈 OHLC STATISTICS:")
        print(f"   Highest Price:     {df['High'].max():.5f}")
        print(f"   Lowest Price:      {df['Low'].min():.5f}")
        print(f"   Opening Price:     {df['Open'].iloc[0]:.5f}")
        print(f"   Closing Price:     {df['Close'].iloc[-1]:.5f}")
        print(f"   Total Price Range: {df['High'].max() - df['Low'].min():.5f}")
        
        # Calculate price movement
        price_change = df['Close'].iloc[-1] - df['Open'].iloc[0]
        price_change_pct = (price_change / df['Open'].iloc[0]) * 100 if df['Open'].iloc[0] != 0 else 0
        print(f"   Total Price Change: {price_change:+.5f} ({price_change_pct:+.2f}%)")
    
    # Predicted prices statistics
    predicted_cols = [col for col in ['PPrice1', 'PPrice2', 'predicted_low', 'predicted_high'] 
                     if col in df.columns]
    if predicted_cols:
        print(f"\n🎯 PREDICTED PRICES STATISTICS:")
        for col in predicted_cols:
            valid_data = df[col].dropna()
            if len(valid_data) > 0:
                print(f"   {col:<15}: Min={valid_data.min():.5f}, Max={valid_data.max():.5f}, "
                      f"Avg={valid_data.mean():.5f}, Count={len(valid_data)}")
            else:
                print(f"   {col:<15}: No valid predictions")
    
    # Pressure indicators statistics
    pressure_cols = [col for col in ['Pressure', 'PV', 'pressure', 'pressure_vector'] 
                    if col in df.columns]
    if pressure_cols:
        print(f"\n💨 PRESSURE INDICATORS STATISTICS:")
        for col in pressure_cols:
            valid_data = df[col].dropna()
            if len(valid_data) > 0:
                print(f"   {col:<15}: Min={valid_data.min():.3f}, Max={valid_data.max():.3f}, "
                      f"Avg={valid_data.mean():.3f}, Std={valid_data.std():.3f}")
    
    # HL statistics
    hl_cols = [col for col in ['HL', 'hl'] if col in df.columns]
    if hl_cols:
        print(f"\n📏 HIGH-LOW RANGE STATISTICS:")
        for col in hl_cols:
            valid_data = df[col].dropna()
            if len(valid_data) > 0:
                print(f"   {col:<15}: Min={valid_data.min():.3f}, Max={valid_data.max():.3f}, "
                      f"Avg={valid_data.mean():.3f} points")
    
    # Trading signals statistics
    direction_cols = [col for col in ['Direction', 'direction'] if col in df.columns]
    if direction_cols:
        print(f"\n🎯 TRADING SIGNALS STATISTICS:")
        for col in direction_cols:
            direction_data = df[col].fillna(NOTRADE)
            buy_count = (direction_data == BUY).sum()
            sell_count = (direction_data == SELL).sum()
            notrade_count = (direction_data == NOTRADE).sum()
            
            print(f"   {col} Signals:")
            print(f"      🔼 BUY:       {buy_count:>6} ({buy_count/len(df)*100:.1f}%)")
            print(f"      🔽 SELL:      {sell_count:>6} ({sell_count/len(df)*100:.1f}%)")
            print(f"      ⏸️  NO TRADE:  {notrade_count:>6} ({notrade_count/len(df)*100:.1f}%)")
            print(f"      📊 Total:     {len(df):>6}")
    
    # Volume statistics
    volume_cols = [col for col in ['Volume', 'TickVolume'] if col in df.columns]
    if volume_cols:
        print(f"\n📊 VOLUME STATISTICS:")
        for col in volume_cols:
            valid_data = df[col].dropna()
            if len(valid_data) > 0:
                print(f"   {col}:")
                print(f"      Total:      {valid_data.sum():>15,.0f}")
                print(f"      Average:    {valid_data.mean():>15,.0f}")
                print(f"      Maximum:    {valid_data.max():>15,.0f}")
                print(f"      Minimum:    {valid_data.min():>15,.0f}")
    
    # Prediction accuracy (if we have both actual and predicted data)
    _analyze_prediction_accuracy(df)
    
    print("\n" + "="*80)
    print("💡 PHLD (Predict High Low Direction) Terminal Visualization")
    print("   🎯 Predicted prices shown with dashed lines and diamond markers")
    print("   💨 Pressure indicators help predict market direction")
    print("   📏 HL (High-Low range) indicates market volatility in points")
    print("   🔼🔽 Trading signals based on pressure vector analysis")
    print("="*80 + "\n")


def _analyze_prediction_accuracy(df: pd.DataFrame) -> None:
    """Analyze prediction accuracy if both actual and predicted data are available."""
    
    try:
        # Check if we have both actual High/Low and predicted High/Low
        has_actual_hl = 'High' in df.columns and 'Low' in df.columns
        has_pred_high = 'PPrice2' in df.columns or 'predicted_high' in df.columns
        has_pred_low = 'PPrice1' in df.columns or 'predicted_low' in df.columns
        
        if has_actual_hl and (has_pred_high or has_pred_low):
            print(f"\n🎯 PREDICTION ACCURACY ANALYSIS:")
            
            # Analyze predicted high accuracy
            if has_pred_high:
                pred_high_col = 'PPrice2' if 'PPrice2' in df.columns else 'predicted_high'
                pred_high = df[pred_high_col].dropna()
                actual_high = df.loc[pred_high.index, 'High']
                
                if len(pred_high) > 0:
                    errors = abs(pred_high - actual_high)
                    mae_high = errors.mean()
                    rmse_high = np.sqrt((errors ** 2).mean())
                    print(f"   Predicted High:")
                    print(f"      Mean Abs Error:  {mae_high:.5f}")
                    print(f"      RMSE:            {rmse_high:.5f}")
                    print(f"      Predictions:     {len(pred_high)}")
            
            # Analyze predicted low accuracy
            if has_pred_low:
                pred_low_col = 'PPrice1' if 'PPrice1' in df.columns else 'predicted_low'
                pred_low = df[pred_low_col].dropna()
                actual_low = df.loc[pred_low.index, 'Low']
                
                if len(pred_low) > 0:
                    errors = abs(pred_low - actual_low)
                    mae_low = errors.mean()
                    rmse_low = np.sqrt((errors ** 2).mean())
                    print(f"   Predicted Low:")
                    print(f"      Mean Abs Error:  {mae_low:.5f}")
                    print(f"      RMSE:            {rmse_low:.5f}")
                    print(f"      Predictions:     {len(pred_low)}")
            
            # Analyze direction prediction accuracy
            if 'Direction' in df.columns and len(df) > 1:
                direction = df['Direction'].fillna(NOTRADE)
                # Calculate actual direction based on close prices
                actual_direction = []
                for i in range(1, len(df)):
                    if df['Close'].iloc[i] > df['Close'].iloc[i-1]:
                        actual_direction.append(BUY)
                    elif df['Close'].iloc[i] < df['Close'].iloc[i-1]:
                        actual_direction.append(SELL)
                    else:
                        actual_direction.append(NOTRADE)
                
                if len(actual_direction) > 0:
                    predicted_dir = direction.iloc[1:].tolist()  # Skip first bar
                    correct_predictions = sum(1 for p, a in zip(predicted_dir, actual_direction) 
                                            if p == a and p != NOTRADE)
                    total_predictions = sum(1 for p in predicted_dir if p != NOTRADE)
                    
                    if total_predictions > 0:
                        accuracy = correct_predictions / total_predictions * 100
                        print(f"   Direction Accuracy:")
                        print(f"      Correct:         {correct_predictions}/{total_predictions}")
                        print(f"      Accuracy:        {accuracy:.1f}%")
    
    except Exception as e:
        logger.print_debug(f"Could not analyze prediction accuracy: {e}")


def plot_phld_comparison(df1: pd.DataFrame, df2: pd.DataFrame, 
                        title1: str = "Dataset 1", title2: str = "Dataset 2") -> None:
    """
    Compare PHLD indicators between two datasets.
    
    Args:
        df1 (pd.DataFrame): First dataset
        df2 (pd.DataFrame): Second dataset  
        title1 (str): Title for first dataset
        title2 (str): Title for second dataset
    """
    try:
        logger.print_info(f"Comparing PHLD data: {title1} vs {title2}")
        
        # Clear plots
        plt.clear_data()
        plt.clear_figure()
        
        # Set theme and size
        plt.theme('dark')
        plt.plot_size(130, 35)
        
        # Use shorter dataset length
        min_len = min(len(df1), len(df2))
        x_values = list(range(min_len))
        
        # Compare predicted prices if available
        if 'PPrice1' in df1.columns and 'PPrice1' in df2.columns:
            values1 = df1['PPrice1'].iloc[:min_len].fillna(method='ffill').fillna(0).tolist()
            values2 = df2['PPrice1'].iloc[:min_len].fillna(method='ffill').fillna(0).tolist()
            
            plt.plot(x_values, values1, color="green", label=f"{title1} - Pred Low", marker="o")
            plt.plot(x_values, values2, color="green+", label=f"{title2} - Pred Low", marker="s")
        
        if 'PPrice2' in df1.columns and 'PPrice2' in df2.columns:
            values1 = df1['PPrice2'].iloc[:min_len].fillna(method='ffill').fillna(0).tolist()
            values2 = df2['PPrice2'].iloc[:min_len].fillna(method='ffill').fillna(0).tolist()
            
            plt.plot(x_values, values1, color="red", label=f"{title1} - Pred High", marker="o")
            plt.plot(x_values, values2, color="red+", label=f"{title2} - Pred High", marker="s")
        
        plt.title(f"PHLD Comparison: {title1} vs {title2}")
        plt.xlabel("Time / Bar Index")
        plt.ylabel("Predicted Prices")
        plt.show_legend()
        plt.show()
        
        logger.print_success("PHLD comparison plot generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating PHLD comparison: {e}")
