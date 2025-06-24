# -*- coding: utf-8 -*-
# src/plotting/term_plot.py

"""
Terminal-based plotting using plotext for ASCII charts in terminal/SSH environments.
"""

import pandas as pd
import numpy as np
import plotext as plt
from typing import Optional, Union
from datetime import datetime

# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    # Fallback to relative imports when run as module
    from ..common import logger
    from ..common.constants import TradingRule, BUY, SELL, NOTRADE

from src.calculation.trading_metrics import calculate_trading_metrics


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
        
        # Convert rule to string - safely handle different rule types
        rule_str = rule.name if hasattr(rule, 'name') else str(rule)
        
        # Check if we have original rule with parameters for display
        if hasattr(rule, 'original_rule_with_params'):
            display_rule = rule.original_rule_with_params
        else:
            display_rule = rule_str
        
        # Check if rule is AUTO - use separate field plotting with dots style
        if rule_str.upper() in ['AUTO', 'AUTO_DISPLAY_ALL']:
            logger.print_info("AUTO rule detected, using separate field plotting with 'dots' style...")

            # Check for OHLC columns first
            ohlc_columns = ['Open', 'High', 'Low', 'Close']
            has_ohlc = all(col in df_results.columns for col in ohlc_columns)

            if has_ohlc:
                # First show the main OHLC chart as candlestick
                logger.print_info("Plotting main OHLC candlestick chart first...")

                # Create time axis
                x_values = list(range(len(df_results)))

                # Set up plot
                plt.plot_size(140, 35)
                plt.theme('matrix')  # Matrix green theme

                # Prepare OHLC data for candlestick chart
                ohlc_data = {
                    'Open': df_results['Open'].ffill().fillna(df_results['Close']).tolist(),
                    'High': df_results['High'].ffill().fillna(df_results['Close']).tolist(),
                    'Low': df_results['Low'].ffill().fillna(df_results['Close']).tolist(),
                    'Close': df_results['Close'].ffill().fillna(df_results['Open']).tolist()
                }

                # Create the candlestick chart
                plt.candlestick(x_values, ohlc_data)
                plt.title(f"{title} - OHLC Chart (Matrix Green Theme)")
                plt.xlabel("Time / Bar Index")
                plt.ylabel("Price")
                plt.show()

            # Then use separate field plotting for all numeric fields
            try:
                from src.plotting.term_separate_plots import plot_separate_fields_terminal
                # Plot each additional numeric field as a separate chart with dots style
                plot_separate_fields_terminal(df_results, rule, f"{title} - Fields", style="dots")
                logger.print_success("Successfully plotted all fields as separate terminal charts with 'dots' style")
            except ImportError as e:
                logger.print_warning(f"Could not import separate field plotting: {e}")

            return

        # Check for required OHLC columns
        required_columns = ['Open', 'High', 'Low', 'Close']
        missing_columns = [col for col in required_columns if col not in df_results.columns]
        if missing_columns:
            logger.print_error(f"Missing required columns: {missing_columns}")
            return
        
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
            # For AUTO rule, show the main OHLC chart first, then separate field plots
            logger.print_info("AUTO rule detected in Python API, using 'dots' style for separate field plotting...")
            _add_auto_indicators_term(df, x_values)  # Add overlays to main chart
            
            # Show the main chart first
            plt.show()
            
            # Then show separate field plots with dots style
            try:
                from src.plotting.term_separate_plots import plot_separate_fields_terminal
                plot_separate_fields_terminal(df, rule_str, f"{title} - Separate Fields", style="dots")
                logger.print_success("Successfully displayed main OHLC chart and separate field plots with 'dots' style.")
                return  # Early return to avoid showing main chart twice
            except ImportError as e:
                logger.print_warning(f"Could not import separate field plotting: {e}. Showing main chart with overlays only.")
            except Exception as e:
                logger.print_warning(f"Error in separate field plotting: {e}. Continuing with main chart.")
        
        # Add predicted price lines if available
        if 'PPrice1' in df.columns:  # Predicted Low
            pprice1_values = df['PPrice1'].fillna(0).tolist()
            plt.plot(x_values, pprice1_values, color="green+", label="Predicted Low", marker="s")

        if 'PPrice2' in df.columns:  # Predicted High
            pprice2_values = df['PPrice2'].fillna(0).tolist()
            plt.plot(x_values, pprice2_values, color="green+", label="Predicted High", marker="s")

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
        _show_terminal_statistics(df, display_rule)
        
        # === После plt.show() ===
        # Вывести метрики отдельным блоком
        metrics = calculate_trading_metrics(df_results)
        print("\n=== Trading Metrics ===")
        for k, v in metrics.items():
            print(f"{k}: {v}")
        
        logger.print_success("Terminal plot generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating terminal plot: {e}")
        logger.print_debug(f"Exception details: {type(e).__name__}: {e}")


def _add_phld_indicators_term(df: pd.DataFrame, x_values: list) -> None:
    """Add PHLD-specific indicators to terminal plot with green square markers."""

    # Add HL (High-Low range in points)
    if 'HL' in df.columns:
        hl_values = df['HL'].fillna(0).tolist()
        plt.plot(x_values, hl_values, color="green+", label="HL Range", marker="s")

    # Add Pressure
    if 'Pressure' in df.columns:
        pressure_values = df['Pressure'].fillna(0).tolist()
        plt.plot(x_values, pressure_values, color="green+", label="Pressure", marker="s")

    # Add Pressure Vector (PV)
    if 'PV' in df.columns:
        pv_values = df['PV'].fillna(0).tolist()
        plt.plot(x_values, pv_values, color="green+", label="PV", marker="s")


def _add_pv_indicators_term(df: pd.DataFrame, x_values: list) -> None:
    """Add Pressure Vector specific indicators to terminal plot with green square markers."""

    if 'PV' in df.columns:
        pv_values = df['PV'].fillna(0).tolist()
        plt.plot(x_values, pv_values, color="green+", label="Pressure Vector", marker="s")

    if 'Pressure' in df.columns:
        pressure_values = df['Pressure'].fillna(0).tolist()
        plt.plot(x_values, pressure_values, color="green+", label="Pressure Force", marker="s")


def _add_auto_indicators_term(df: pd.DataFrame, x_values: list) -> None:
    """Add all available indicators for AUTO mode with beautiful color scheme."""
    
    # Always use green+ as the primary color
    colors = [
        "green+", "green+", "green+", "green+", "green+", "green+",
        "green+", "green+", "green+", "green+"
    ]
    
    # Use square markers for all plots
    marker = "s"  # Always use square marker for all modes

    # Standard columns to skip
    skip_columns = {
        'Open', 'High', 'Low', 'Close', 'Volume', 'DateTime', 'Timestamp', 
        'Date', 'Time', 'Index', 'index'
    }
    
    color_index = 0

    for col in df.columns:
        if col not in skip_columns and pd.api.types.is_numeric_dtype(df[col]):
            try:
                # Clean data for plotting
                values = df[col].fillna(0).tolist()

                # Only plot if we have valid data
                if any(v != 0 for v in values):
                    color = colors[color_index % len(colors)]

                    # Simple label without emojis
                    label = col
                    plt.plot(x_values, values, color=color, label=label, marker=marker)

                    color_index += 1

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
        plt.scatter(buy_x, buy_y, color="green+", marker="s", label="BUY Signal")

    if sell_indices:
        sell_x = [x_values[i] for i in sell_indices]
        sell_y = [high_values[i] * 1.005 for i in sell_indices]  # Place above High
        plt.scatter(sell_x, sell_y, color="green+", marker="s", label="SELL Signal")


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
    
    # Trading Performance Metrics
    if 'Direction' in df.columns and total_signals > 0:
        try:
            print(f"\n📊 TRADING PERFORMANCE METRICS:")
            print(f"{'─' * 50}")
            
            # Calculate trading metrics
            metrics = calculate_trading_metrics(df)
            
            # Display key metrics with emojis and formatting
            print(f"🎯 Win Ratio:           {metrics['win_ratio']:.1f}%")
            print(f"⚖️  Risk/Reward Ratio:   {metrics['risk_reward_ratio']:.2f}")
            print(f"💰 Profit Factor:        {metrics['profit_factor']:.2f}")
            print(f"📈 Total Return:         {metrics['total_return']:.1f}%")
            print(f"📉 Max Drawdown:         {metrics['max_drawdown']:.1f}%")
            print(f"📊 Sharpe Ratio:         {metrics['sharpe_ratio']:.2f}")
            print(f"🛡️  Sortino Ratio:       {metrics['sortino_ratio']:.2f}")
            print(f"🎲 Probability Risk:     {metrics['probability_risk_ratio']:.2f}")
            print(f"📈 Volatility:           {metrics['volatility']:.1f}%")
            print(f"⚡ Calmar Ratio:         {metrics['calmar_ratio']:.2f}")
            
            # Add volume-weighted metrics if available
            if 'volume_weighted_return' in metrics and metrics['volume_weighted_return'] != 0:
                print(f"📊 Vol Weighted Return: {metrics['volume_weighted_return']:.2f}%")
                print(f"📊 Vol Win Ratio:       {metrics['volume_win_ratio']:.1f}%")
            
            # Performance summary
            print(f"\n📋 PERFORMANCE SUMMARY:")
            if metrics['win_ratio'] >= 50:
                print(f"✅ Good win rate ({metrics['win_ratio']:.1f}%)")
            else:
                print(f"⚠️  Low win rate ({metrics['win_ratio']:.1f}%)")
            
            if metrics['risk_reward_ratio'] >= 1.5:
                print(f"✅ Good risk/reward ratio ({metrics['risk_reward_ratio']:.2f})")
            else:
                print(f"⚠️  Poor risk/reward ratio ({metrics['risk_reward_ratio']:.2f})")
            
            if metrics['sharpe_ratio'] >= 1.0:
                print(f"✅ Good Sharpe ratio ({metrics['sharpe_ratio']:.2f})")
            else:
                print(f"⚠️  Low Sharpe ratio ({metrics['sharpe_ratio']:.2f})")
            
            if metrics['max_drawdown'] <= 20:
                print(f"✅ Acceptable max drawdown ({metrics['max_drawdown']:.1f}%)")
            else:
                print(f"⚠️  High max drawdown ({metrics['max_drawdown']:.1f}%)")
                
        except Exception as e:
            logger.print_warning(f"Could not calculate trading metrics: {e}")
            print(f"⚠️  Trading metrics calculation failed: {e}")
    
    # Footer
    print(f"\n{header_line}")
    print(f"{'END OF STATISTICS':^80}")
    print(f"{header_line}")


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
