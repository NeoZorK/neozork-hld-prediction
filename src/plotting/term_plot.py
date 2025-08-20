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
    from src.common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    # Fallback to relative imports when run as module
    from src.common import logger
    from src.common.constants import TradingRule, BUY, SELL, NOTRADE

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
                plt.plot_size(140, 30)  # Reduced height for better text visibility
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
        plt.title(title)
        
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
            plt.plot(x_values, pprice1_values, color="green+", label="Predicted Low")

        if 'PPrice2' in df.columns:  # Predicted High
            pprice2_values = df['PPrice2'].fillna(0).tolist()
            plt.plot(x_values, pprice2_values, color="red+", label="Predicted High")

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
        
        # === After plt.show() ===
        # Display metrics in a separate block with color coding
        metrics = calculate_trading_metrics(df_results)
        print("\n=== Trading Metrics ===")
        _print_colored_metrics(metrics)
        
        logger.print_success("Terminal plot generated successfully!")
        
    except Exception as e:
        logger.print_error(f"Error generating terminal plot: {e}")
        logger.print_debug(f"Exception details: {type(e).__name__}: {e}")


def _add_phld_indicators_term(df: pd.DataFrame, x_values: list) -> None:
    """Add PHLD-specific indicators to terminal plot with green square markers."""

    # Add HL (High-Low range in points)
    if 'HL' in df.columns:
        hl_values = df['HL'].fillna(0).tolist()
        plt.plot(x_values, hl_values, color="green+", label="HL Range")

    # Add Pressure
    if 'Pressure' in df.columns:
        pressure_values = df['Pressure'].fillna(0).tolist()
        plt.plot(x_values, pressure_values, color="blue+", label="Pressure")

    # Add Pressure Vector (PV)
    if 'PV' in df.columns:
        pv_values = df['PV'].fillna(0).tolist()
        plt.plot(x_values, pv_values, color="yellow+", label="PV")


def _add_pv_indicators_term(df: pd.DataFrame, x_values: list) -> None:
    """Add Pressure Vector specific indicators to terminal plot with green square markers."""

    if 'PV' in df.columns:
        pv_values = df['PV'].fillna(0).tolist()
        plt.plot(x_values, pv_values, color="yellow+", label="Pressure Vector")

    if 'Pressure' in df.columns:
        pressure_values = df['Pressure'].fillna(0).tolist()
        plt.plot(x_values, pressure_values, color="blue+", label="Pressure Force")


def _add_auto_indicators_term(df: pd.DataFrame, x_values: list) -> None:
    """Add all available indicators for AUTO mode with unique colors for each field."""
    
    # Import the color function from term_chunked_plot
    try:
        from src.plotting.term_chunked_plot import _get_field_color
    except ImportError:
        # Fallback color function if import fails
        def _get_field_color(field_name: str) -> str:
            colors = ["green+", "blue+", "red+", "yellow+", "magenta+", "cyan+", "white+", "orange+", "purple+", "pink+"]
            import hashlib
            hash_value = int(hashlib.md5(field_name.encode()).hexdigest(), 16)
            return colors[hash_value % len(colors)]
    
    # Use bold lines without markers for clean visualization
    marker = ""  # No markers, use bold lines instead

    # Standard columns to skip
    skip_columns = {
        'Open', 'High', 'Low', 'Close', 'Volume', 'DateTime', 'Timestamp', 
        'Date', 'Time', 'Index', 'index'
    }

    for col in df.columns:
        if col not in skip_columns and pd.api.types.is_numeric_dtype(df[col]):
            try:
                # Clean data for plotting
                values = df[col].fillna(0).tolist()

                # Only plot if we have valid data
                if any(v != 0 for v in values):
                    # Get unique color for this field
                    color = _get_field_color(col)

                    # Simple label without emojis
                    label = col
                    plt.plot(x_values, values, color=color, label=label, marker=marker)

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


def _print_colored_metrics(metrics: dict) -> None:
    """
    Print trading metrics with color coding for strategy quality assessment.
    Red = bad, Yellow = average, Green = good for profitable strategy.
    """
    # ANSI color codes
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    BLUE = '\033[94m'
    
    def get_metric_icon_color_and_description(metric_name: str, value) -> tuple[str, str, str]:
        """Determine icon, color and description based on metric name and value for profitable strategy."""
        try:
            value = float(str(value).replace('%', '').replace(',', ''))
        except:
            return "📊", YELLOW, "Non-numeric value - check data quality."
        
        # Win Rate: Green > 60%, Yellow 40-60%, Red < 40%
        if 'win' in metric_name.lower() or 'win_rate' in metric_name.lower():
            if value >= 60: 
                return "🏆", GREEN, f"Excellent win rate! Strategy is highly profitable. Keep current approach."
            elif value >= 40: 
                return "🎯", YELLOW, f"Acceptable win rate. Consider improving entry/exit timing or risk management."
            else: 
                return "💔", RED, f"Low win rate indicates strategy needs major improvement. Review entry criteria and market conditions."
        
        # Profit Factor: Green > 1.5, Yellow 1.0-1.5, Red < 1.0
        elif 'profit_factor' in metric_name.lower():
            if value >= 1.5: 
                return "💰", GREEN, f"Strong profit factor! Strategy generates good profits vs losses. Optimize position sizing."
            elif value >= 1.0: 
                return "💵", YELLOW, f"Moderate profit factor. Focus on improving win rate or average win size."
            else: 
                return "📉", RED, f"Poor profit factor. Strategy loses more than it gains. Major revision needed."
        
        # Total Return: Green > 20%, Yellow 5-20%, Red < 5%
        elif 'total_return' in metric_name.lower():
            if value >= 20: 
                return "🚀", GREEN, f"Outstanding returns! Strategy is highly effective. Consider scaling up carefully."
            elif value >= 5: 
                return "📈", YELLOW, f"Good returns. Strategy is profitable but could be optimized further."
            else: 
                return "📊", RED, f"Low returns. Strategy needs significant improvement or market conditions are unfavorable."
        
        # Sharpe Ratio: Green > 1.0, Yellow 0.5-1.0, Red < 0.5
        elif 'sharpe_ratio' in metric_name.lower():
            if value >= 1.0: 
                return "⭐", GREEN, f"Excellent risk-adjusted returns! Strategy is very efficient."
            elif value >= 0.5: 
                return "✨", YELLOW, f"Good risk-adjusted returns. Consider reducing volatility or increasing returns."
            else: 
                return "💫", RED, f"Poor risk-adjusted returns. High volatility relative to returns."
        
        # Max Drawdown: Green < 10%, Yellow 10-20%, Red > 20%
        elif 'max_drawdown' in metric_name.lower():
            if value <= 10: 
                return "🛡️", GREEN, f"Excellent risk management! Very low drawdown indicates good capital preservation."
            elif value <= 20: 
                return "⚠️", YELLOW, f"Acceptable drawdown. Consider improving stop-loss or position sizing."
            else: 
                return "💥", RED, f"High drawdown! Risk management needs immediate attention."
        
        # Number of Trades: Green 20-100, Yellow 10-20 or 100-200, Red < 10 or > 200
        elif 'total_trades' in metric_name.lower() or 'buy_count' in metric_name.lower() or 'sell_count' in metric_name.lower():
            if 20 <= value <= 100: 
                return "🎲", GREEN, f"Optimal number of trades. Good balance between activity and quality."
            elif 10 <= value <= 20 or 100 <= value <= 200: 
                return "🎪", YELLOW, f"Trade frequency needs adjustment. Too few or too many trades."
            else: 
                return "🎭", RED, f"Extreme trade frequency. Strategy may be over-trading or under-trading."
        
        # Average Trade: Green > 2%, Yellow 0.5-2%, Red < 0.5%
        elif 'average_trade' in metric_name.lower():
            if value >= 2: 
                return "💎", GREEN, f"Excellent average trade size! Strategy captures significant moves."
            elif value >= 0.5: 
                return "🔮", YELLOW, f"Moderate average trade size. Consider improving entry/exit timing."
            else: 
                return "💍", RED, f"Small average trade size. Strategy may be taking profits too early."
        
        # Risk/Reward Ratio: Green > 2.0, Yellow 1.5-2.0, Red < 1.5
        elif 'risk_reward_ratio' in metric_name.lower():
            if value >= 2.0: 
                return "⚖️", GREEN, f"Excellent risk/reward ratio! Strategy has strong asymmetric returns."
            elif value >= 1.5: 
                return "🎪", YELLOW, f"Good risk/reward ratio. Consider improving target/stop placement."
            else: 
                return "🎭", RED, f"Poor risk/reward ratio. Strategy risks more than it gains."
        
        # Sortino Ratio: Green > 1.0, Yellow 0.5-1.0, Red < 0.5
        elif 'sortino_ratio' in metric_name.lower():
            if value >= 1.0: 
                return "🛡️", GREEN, f"Excellent downside risk management! Strategy handles losses well."
            elif value >= 0.5: 
                return "⚔️", YELLOW, f"Good downside risk management. Consider improving loss control."
            else: 
                return "🗡️", RED, f"Poor downside risk management. Strategy has excessive losses."
        
        # Volatility: Green < 15%, Yellow 15-25%, Red > 25%
        elif 'volatility' in metric_name.lower():
            if value <= 15: 
                return "🎯", GREEN, f"Low volatility! Strategy is very stable and predictable."
            elif value <= 25: 
                return "🎪", YELLOW, f"Moderate volatility. Consider risk management improvements."
            else: 
                return "🎭", RED, f"High volatility! Strategy is very risky and unpredictable."
        
        # Calmar Ratio: Green > 1.0, Yellow 0.5-1.0, Red < 0.5
        elif 'calmar_ratio' in metric_name.lower():
            if value >= 1.0: 
                return "🏆", GREEN, f"Excellent return vs drawdown ratio! Strategy is very efficient."
            elif value >= 0.5: 
                return "🎯", YELLOW, f"Good return vs drawdown ratio. Consider improving risk management."
            else: 
                return "💔", RED, f"Poor return vs drawdown ratio. Strategy has high risk for low returns."
        
        # Kelly Fraction: Green 0.1-0.3, Yellow 0.05-0.1 or 0.3-0.5, Red < 0.05 or > 0.5
        elif 'kelly_fraction' in metric_name.lower():
            if 0.1 <= value <= 0.3: 
                return "🎯", GREEN, f"Optimal position sizing! Kelly criterion suggests good risk management."
            elif 0.05 <= value <= 0.1 or 0.3 <= value <= 0.5: 
                return "⚖️", YELLOW, f"Position sizing needs adjustment. Consider Kelly criterion optimization."
            else: 
                return "🎪", RED, f"Poor position sizing! Kelly criterion suggests major risk management issues."
        
        # Strategy Efficiency: Green > 80%, Yellow 60-80%, Red < 60%
        elif 'strategy_efficiency' in metric_name.lower():
            if value >= 80: 
                return "⚡", GREEN, f"Excellent strategy efficiency! Low fees and high net returns."
            elif value >= 60: 
                return "🔋", YELLOW, f"Good strategy efficiency. Consider reducing trading costs."
            else: 
                return "🔌", RED, f"Poor strategy efficiency. High fees eating into profits."
        
        # Monte Carlo Expected Return: Green > 15%, Yellow 5-15%, Red < 5%
        elif 'mc_expected_return' in metric_name.lower():
            if value >= 15: 
                return "🎲", GREEN, f"Strong expected returns from Monte Carlo simulation! Strategy is robust."
            elif value >= 5: 
                return "🎪", YELLOW, f"Moderate expected returns. Strategy shows some promise."
            else: 
                return "🎭", RED, f"Low expected returns. Strategy may not be profitable long-term."
        
        # Monte Carlo Probability of Profit: Green > 70%, Yellow 50-70%, Red < 50%
        elif 'mc_probability_profit' in metric_name.lower():
            if value >= 70: 
                return "🎯", GREEN, f"High probability of profit! Monte Carlo shows strategy is very reliable."
            elif value >= 50: 
                return "🎪", YELLOW, f"Moderate probability of profit. Strategy has some reliability."
            else: 
                return "🎭", RED, f"Low probability of profit. Strategy may not be reliable long-term."
        
        # Strategy Robustness: Green > 80%, Yellow 60-80%, Red < 60%
        elif 'strategy_robustness' in metric_name.lower():
            if value >= 80: 
                return "🛡️", GREEN, f"Excellent strategy robustness! Very consistent across different scenarios."
            elif value >= 60: 
                return "⚔️", YELLOW, f"Good strategy robustness. Some consistency but room for improvement."
            else: 
                return "🗡️", RED, f"Poor strategy robustness. Inconsistent results across scenarios."
        
        # Risk of Ruin: Green < 10%, Yellow 10-30%, Red > 30%
        elif 'risk_of_ruin' in metric_name.lower():
            if value <= 10: 
                return "🛡️", GREEN, f"Very low risk of ruin! Strategy is very safe for capital preservation."
            elif value <= 30: 
                return "⚠️", YELLOW, f"Moderate risk of ruin. Consider improving risk management."
            else: 
                return "💥", RED, f"High risk of ruin! Strategy is very dangerous for capital."
        
        # Signal Accuracy: Green > 70%, Yellow 50-70%, Red < 50%
        elif 'signal_accuracy' in metric_name.lower():
            if value >= 70: 
                return "🎯", GREEN, f"Excellent signal accuracy! Trading signals are very reliable."
            elif value >= 50: 
                return "🎪", YELLOW, f"Moderate signal accuracy. Consider improving signal generation."
            else: 
                return "🎭", RED, f"Poor signal accuracy. Trading signals are unreliable."
        
        # Signal Frequency: Green 0.1-0.3, Yellow 0.05-0.1 or 0.3-0.5, Red < 0.05 or > 0.5
        elif 'signal_frequency' in metric_name.lower():
            if 0.1 <= value <= 0.3: 
                return "⚡", GREEN, f"Optimal signal frequency! Good balance between activity and quality."
            elif 0.05 <= value <= 0.1 or 0.3 <= value <= 0.5: 
                return "🔋", YELLOW, f"Signal frequency needs adjustment. Too few or too many signals."
            else: 
                return "🔌", RED, f"Extreme signal frequency. Strategy may be over-trading or under-trading."
        
        # Signal Stability: Green > 80%, Yellow 60-80%, Red < 60%
        elif 'signal_stability' in metric_name.lower():
            if value >= 80: 
                return "🛡️", GREEN, f"Excellent signal stability! Strategy is very consistent."
            elif value >= 60: 
                return "⚔️", YELLOW, f"Good signal stability. Some consistency but room for improvement."
            else: 
                return "🗡️", RED, f"Poor signal stability. Strategy is very inconsistent."
        
        # Pattern Consistency: Green > 70%, Yellow 50-70%, Red < 50%
        elif 'pattern_consistency' in metric_name.lower():
            if value >= 70: 
                return "🎯", GREEN, f"Excellent pattern consistency! Strategy follows reliable patterns."
            elif value >= 50: 
                return "🎪", YELLOW, f"Moderate pattern consistency. Some patterns but room for improvement."
            else: 
                return "🎭", RED, f"Poor pattern consistency. Strategy lacks reliable patterns."
        
        # Signal Clustering: Green > 70%, Yellow 50-70%, Red < 50%
        elif 'signal_clustering' in metric_name.lower():
            if value >= 70: 
                return "🎯", GREEN, f"Excellent signal clustering! Strategy has good market timing."
            elif value >= 50: 
                return "🎪", YELLOW, f"Moderate signal clustering. Some market timing but room for improvement."
            else: 
                return "🎭", RED, f"Poor signal clustering. Strategy lacks good market timing."
        
        # Volume Weighted Return: Green > 2%, Yellow 0.5-2%, Red < 0.5%
        elif 'volume_weighted_return' in metric_name.lower():
            if value >= 2: 
                return "📊", GREEN, f"Excellent volume-weighted returns! Strategy performs well on high volume."
            elif value >= 0.5: 
                return "📈", YELLOW, f"Good volume-weighted returns. Consider volume analysis."
            else: 
                return "📉", RED, f"Poor volume-weighted returns. Strategy struggles on high volume."
        
        # Volume Win Ratio: Green > 70%, Yellow 50-70%, Red < 50%
        elif 'volume_win_ratio' in metric_name.lower():
            if value >= 70: 
                return "📊", GREEN, f"Excellent volume win ratio! Strategy wins on high volume periods."
            elif value >= 50: 
                return "📈", YELLOW, f"Good volume win ratio. Consider volume-based filtering."
            else: 
                return "📉", RED, f"Poor volume win ratio. Strategy loses on high volume periods."
        
        # Fee Impact: Green < 10%, Yellow 10-25%, Red > 25%
        elif 'fee_impact' in metric_name.lower():
            if value <= 10: 
                return "💰", GREEN, f"Low fee impact! Trading costs are well managed."
            elif value <= 25: 
                return "💵", YELLOW, f"Moderate fee impact. Consider reducing trading frequency."
            else: 
                return "📉", RED, f"High fee impact! Trading costs are eating into profits significantly."
        
        # Strategy Sustainability: Green > 80%, Yellow 60-80%, Red < 60%
        elif 'strategy_sustainability' in metric_name.lower():
            if value >= 80: 
                return "🌱", GREEN, f"Excellent strategy sustainability! Strategy is well-designed for long-term success."
            elif value >= 60: 
                return "🌿", YELLOW, f"Good strategy sustainability. Some improvements needed for long-term success."
            else: 
                return "🍂", RED, f"Poor strategy sustainability. Strategy may not be viable long-term."
        
        # Break Even Win Rate: Green < 40%, Yellow 40-50%, Red > 50%
        elif 'break_even_win_rate' in metric_name.lower():
            if value <= 40: 
                return "🎯", GREEN, f"Low break-even win rate! Strategy is very efficient."
            elif value <= 50: 
                return "🎪", YELLOW, f"Moderate break-even win rate. Strategy efficiency needs improvement."
            else: 
                return "🎭", RED, f"High break-even win rate! Strategy is very inefficient."
        
        # Minimum Win Rate for Profit: Green < 40%, Yellow 40-50%, Red > 50%
        elif 'min_win_rate_for_profit' in metric_name.lower():
            if value <= 40: 
                return "🎯", GREEN, f"Low minimum win rate needed! Strategy is very forgiving."
            elif value <= 50: 
                return "🎪", YELLOW, f"Moderate minimum win rate needed. Strategy requires good execution."
            else: 
                return "🎭", RED, f"High minimum win rate needed! Strategy is very demanding."
        
        # Risk Adjusted Return with Fees: Green > 2.0, Yellow 1.0-2.0, Red < 1.0
        elif 'risk_adjusted_return_with_fees' in metric_name.lower():
            if value >= 2.0: 
                return "⚡", GREEN, f"Excellent risk-adjusted returns with fees! Strategy is very efficient."
            elif value >= 1.0: 
                return "🔋", YELLOW, f"Good risk-adjusted returns with fees. Some efficiency improvements possible."
            else: 
                return "🔌", RED, f"Poor risk-adjusted returns with fees. Strategy efficiency needs major improvement."
        
        # Monte Carlo VaR 95%: Green > -10%, Yellow -10% to -20%, Red < -20%
        elif 'mc_var_95' in metric_name.lower():
            if value >= -10: 
                return "🛡️", GREEN, f"Low Value at Risk! Strategy has good downside protection."
            elif value >= -20: 
                return "⚠️", YELLOW, f"Moderate Value at Risk. Consider improving risk management."
            else: 
                return "💥", RED, f"High Value at Risk! Strategy has poor downside protection."
        
        # Monte Carlo CVaR 95%: Green > -15%, Yellow -15% to -25%, Red < -25%
        elif 'mc_cvar_95' in metric_name.lower():
            if value >= -15: 
                return "🛡️", GREEN, f"Low Conditional Value at Risk! Strategy handles extreme losses well."
            elif value >= -25: 
                return "⚠️", YELLOW, f"Moderate Conditional Value at Risk. Consider improving extreme loss management."
            else: 
                return "💥", RED, f"High Conditional Value at Risk! Strategy handles extreme losses poorly."
        
        # Monte Carlo Max Loss: Green > -20%, Yellow -20% to -40%, Red < -40%
        elif 'mc_max_loss' in metric_name.lower():
            if value >= -20: 
                return "🛡️", GREEN, f"Low maximum loss! Strategy has excellent capital preservation."
            elif value >= -40: 
                return "⚠️", YELLOW, f"Moderate maximum loss. Consider improving worst-case scenario management."
            else: 
                return "💥", RED, f"High maximum loss! Strategy has poor capital preservation."
        
        # Monte Carlo Max Gain: Green > 50%, Yellow 25-50%, Red < 25%
        elif 'mc_max_gain' in metric_name.lower():
            if value >= 50: 
                return "🚀", GREEN, f"High maximum gain potential! Strategy can achieve excellent returns."
            elif value >= 25: 
                return "📈", YELLOW, f"Moderate maximum gain potential. Some upside but room for improvement."
            else: 
                return "📊", RED, f"Low maximum gain potential. Strategy has limited upside."
        
        # Monte Carlo Sharpe Ratio: Green > 1.0, Yellow 0.5-1.0, Red < 0.5
        elif 'mc_sharpe_ratio' in metric_name.lower():
            if value >= 1.0: 
                return "⭐", GREEN, f"Excellent Monte Carlo Sharpe ratio! Strategy is very efficient across scenarios."
            elif value >= 0.5: 
                return "✨", YELLOW, f"Good Monte Carlo Sharpe ratio. Some efficiency across scenarios."
            else: 
                return "💫", RED, f"Poor Monte Carlo Sharpe ratio. Strategy is inefficient across scenarios."
        
        # Correlation metrics: Green > 0.3, Yellow 0.1-0.3, Red < 0.1
        elif 'correlation' in metric_name.lower():
            if value >= 0.3: 
                return "🔗", GREEN, f"Strong correlation! This factor is well-aligned with strategy performance."
            elif value >= 0.1: 
                return "🔗", YELLOW, f"Moderate correlation. This factor has some relationship with strategy."
            else: 
                return "🔗", RED, f"Weak correlation. This factor has little relationship with strategy."
        
        # Probability Risk Ratio: Green > 2.0, Yellow 1.0-2.0, Red < 1.0
        elif 'probability_risk_ratio' in metric_name.lower():
            if value >= 2.0: 
                return "🎯", GREEN, f"Excellent probability ratio! Strategy has much higher profit probability than loss."
            elif value >= 1.0: 
                return "🎪", YELLOW, f"Good probability ratio. Strategy has balanced profit/loss probability."
            else: 
                return "🎭", RED, f"Poor probability ratio. Strategy has higher loss probability than profit."
        
        # Position Size: Green 0.5-2.0, Yellow 0.1-0.5 or 2.0-5.0, Red < 0.1 or > 5.0
        elif 'position_size' in metric_name.lower():
            if 0.5 <= value <= 2.0: 
                return "⚖️", GREEN, f"Optimal position size! Good balance between risk and reward."
            elif 0.1 <= value <= 0.5 or 2.0 <= value <= 5.0: 
                return "🎪", YELLOW, f"Position size needs adjustment. Consider risk management optimization."
            else: 
                return "🎭", RED, f"Extreme position size! Very risky or too conservative approach."
        
        # Optimal Position Size: Green 0.1-0.5, Yellow 0.05-0.1 or 0.5-1.0, Red < 0.05 or > 1.0
        elif 'optimal_position_size' in metric_name.lower():
            if 0.1 <= value <= 0.5: 
                return "🎯", GREEN, f"Optimal position sizing! Kelly criterion suggests excellent risk management."
            elif 0.05 <= value <= 0.1 or 0.5 <= value <= 1.0: 
                return "🎪", YELLOW, f"Position sizing needs fine-tuning. Consider Kelly criterion optimization."
            else: 
                return "🎭", RED, f"Poor position sizing! Kelly criterion suggests major risk management issues."
        
        # Net Return: Green > 10%, Yellow 2-10%, Red < 2%
        elif 'net_return' in metric_name.lower():
            if value >= 10: 
                return "💰", GREEN, f"Excellent net returns! Strategy is highly profitable after fees."
            elif value >= 2: 
                return "💵", YELLOW, f"Good net returns. Strategy is profitable but could be optimized."
            else: 
                return "📉", RED, f"Poor net returns. Strategy may not be profitable after fees."
        
        # Max Risk Per Trade: Green < 1%, Yellow 1-3%, Red > 3%
        elif 'max_risk_per_trade' in metric_name.lower():
            if value <= 1: 
                return "🛡️", GREEN, f"Excellent risk per trade! Very conservative and safe approach."
            elif value <= 3: 
                return "⚠️", YELLOW, f"Moderate risk per trade. Consider position sizing optimization."
            else: 
                return "💥", RED, f"High risk per trade! Very dangerous approach to risk management."
        
        # Expected Risk Per Trade: Green < 0.5%, Yellow 0.5-1.5%, Red > 1.5%
        elif 'expected_risk_per_trade' in metric_name.lower():
            if value <= 0.5: 
                return "🛡️", GREEN, f"Excellent expected risk! Strategy has very low expected losses."
            elif value <= 1.5: 
                return "⚠️", YELLOW, f"Moderate expected risk. Consider improving risk management."
            else: 
                return "💥", RED, f"High expected risk! Strategy has significant expected losses."
        
        # Expected Reward Per Trade: Green > 2%, Yellow 0.5-2%, Red < 0.5%
        elif 'expected_reward_per_trade' in metric_name.lower():
            if value >= 2: 
                return "💰", GREEN, f"Excellent expected reward! Strategy has high expected profits."
            elif value >= 0.5: 
                return "💵", YELLOW, f"Good expected reward. Consider improving profit potential."
            else: 
                return "📉", RED, f"Low expected reward. Strategy has limited profit potential."
        
        # Signal Timing Score: Green > 1%, Yellow 0.1-1%, Red < 0.1%
        elif 'signal_timing_score' in metric_name.lower():
            if value >= 1: 
                return "🎯", GREEN, f"Excellent signal timing! Strategy has very good market timing."
            elif value >= 0.1: 
                return "🎪", YELLOW, f"Good signal timing. Consider improving entry/exit timing."
            else: 
                return "🎭", RED, f"Poor signal timing. Strategy has poor market timing."
        
        # Momentum Correlation: Green > 0.3, Yellow 0.1-0.3, Red < 0.1
        elif 'momentum_correlation' in metric_name.lower():
            if value >= 0.3: 
                return "📈", GREEN, f"Strong momentum correlation! Strategy follows price momentum well."
            elif value >= 0.1: 
                return "📊", YELLOW, f"Moderate momentum correlation. Some momentum following but room for improvement."
            else: 
                return "📉", RED, f"Weak momentum correlation. Strategy doesn't follow price momentum well."
        
        # Volatility Correlation: Green > 0.3, Yellow 0.1-0.3, Red < 0.1
        elif 'volatility_correlation' in metric_name.lower():
            if value >= 0.3: 
                return "📊", GREEN, f"Strong volatility correlation! Strategy adapts well to market volatility."
            elif value >= 0.1: 
                return "📈", YELLOW, f"Moderate volatility correlation. Some volatility adaptation but room for improvement."
            else: 
                return "📉", RED, f"Weak volatility correlation. Strategy doesn't adapt well to market volatility."
        
        # Trend Correlation: Green > 0.3, Yellow 0.1-0.3, Red < 0.1
        elif 'trend_correlation' in metric_name.lower():
            if value >= 0.3: 
                return "📈", GREEN, f"Strong trend correlation! Strategy follows market trends well."
            elif value >= 0.1: 
                return "📊", YELLOW, f"Moderate trend correlation. Some trend following but room for improvement."
            else: 
                return "📉", RED, f"Weak trend correlation. Strategy doesn't follow market trends well."
        
        # Risk Adjusted Momentum: Green > 1.0, Yellow 0.5-1.0, Red < 0.5
        elif 'risk_adjusted_momentum' in metric_name.lower():
            if value >= 1.0: 
                return "📈", GREEN, f"Excellent risk-adjusted momentum! Strategy captures momentum efficiently."
            elif value >= 0.5: 
                return "📊", YELLOW, f"Good risk-adjusted momentum. Some momentum capture but room for improvement."
            else: 
                return "📉", RED, f"Poor risk-adjusted momentum. Strategy doesn't capture momentum efficiently."
        
        # Risk Adjusted Trend: Green > 1.0, Yellow 0.5-1.0, Red < 0.5
        elif 'risk_adjusted_trend' in metric_name.lower():
            if value >= 1.0: 
                return "📈", GREEN, f"Excellent risk-adjusted trend! Strategy follows trends efficiently."
            elif value >= 0.5: 
                return "📊", YELLOW, f"Good risk-adjusted trend. Some trend following but room for improvement."
            else: 
                return "📉", RED, f"Poor risk-adjusted trend. Strategy doesn't follow trends efficiently."
        
        # Monte Carlo Standard Deviation: Green < 10%, Yellow 10-20%, Red > 20%
        elif 'mc_std_deviation' in metric_name.lower():
            if value <= 10: 
                return "🛡️", GREEN, f"Low Monte Carlo deviation! Strategy is very consistent across scenarios."
            elif value <= 20: 
                return "⚠️", YELLOW, f"Moderate Monte Carlo deviation. Some consistency but room for improvement."
            else: 
                return "💥", RED, f"High Monte Carlo deviation! Strategy is very inconsistent across scenarios."
        
        # Risk Reward Setting: Green 1.5-3.0, Yellow 1.0-1.5 or 3.0-5.0, Red < 1.0 or > 5.0
        elif 'risk_reward_setting' in metric_name.lower():
            if 1.5 <= value <= 3.0: 
                return "⚖️", GREEN, f"Optimal risk/reward setting! Good balance between risk and reward."
            elif 1.0 <= value <= 1.5 or 3.0 <= value <= 5.0: 
                return "🎪", YELLOW, f"Risk/reward setting needs adjustment. Consider optimization."
            else: 
                return "🎭", RED, f"Extreme risk/reward setting! Very aggressive or too conservative."
        
        # Fee Per Trade: Green < 0.05%, Yellow 0.05-0.15%, Red > 0.15%
        elif 'fee_per_trade' in metric_name.lower():
            if value <= 0.05: 
                return "💰", GREEN, f"Low trading fees! Excellent cost management."
            elif value <= 0.15: 
                return "💵", YELLOW, f"Moderate trading fees. Consider reducing costs."
            else: 
                return "📉", RED, f"High trading fees! Costs are eating into profits significantly."
        
        # Default for unknown metrics
        else:
            return "📊", YELLOW, f"Unknown metric '{metric_name}'. Consider reviewing strategy documentation."
    
    # Group metrics by quality
    good_metrics = []
    average_metrics = []
    bad_metrics = []
    
    def format_metric_name(metric_name: str) -> str:
        """Convert technical metric names to more readable and visually appealing names."""
        # Special cases for better readability
        name_mapping = {
            'buy_count': 'Buy Signals',
            'sell_count': 'Sell Signals', 
            'total_trades': 'Total Trades',
            'win_ratio': 'Win Rate',
            'risk_reward_ratio': 'Risk/Reward Ratio',
            'profit_factor': 'Profit Factor',
            'sharpe_ratio': 'Sharpe Ratio',
            'sortino_ratio': 'Sortino Ratio',
            'probability_risk_ratio': 'Probability Ratio',
            'max_drawdown': 'Max Drawdown',
            'total_return': 'Total Return',
            'volatility': 'Volatility',
            'calmar_ratio': 'Calmar Ratio',
            'volume_weighted_return': 'Volume-Weighted Return',
            'volume_win_ratio': 'Volume Win Rate',
            'kelly_fraction': 'Kelly Fraction',
            'strategy_efficiency': 'Strategy Efficiency',
            'mc_expected_return': 'MC Expected Return',
            'mc_probability_profit': 'MC Profit Probability',
            'strategy_robustness': 'Strategy Robustness',
            'risk_of_ruin': 'Risk of Ruin',
            'signal_accuracy': 'Signal Accuracy',
            'signal_frequency': 'Signal Frequency',
            'signal_stability': 'Signal Stability',
            'pattern_consistency': 'Pattern Consistency',
            'signal_clustering': 'Signal Clustering',
            'fee_impact': 'Fee Impact',
            'strategy_sustainability': 'Strategy Sustainability',
            'break_even_win_rate': 'Break-Even Win Rate',
            'min_win_rate_for_profit': 'Min Win Rate for Profit',
            'risk_adjusted_return_with_fees': 'Risk-Adjusted Return (with Fees)',
            'mc_var_95': 'MC Value at Risk (95%)',
            'mc_cvar_95': 'MC Conditional VaR (95%)',
            'mc_max_loss': 'MC Max Loss',
            'mc_max_gain': 'MC Max Gain',
            'mc_sharpe_ratio': 'MC Sharpe Ratio',
            'mc_std_deviation': 'MC Standard Deviation',
            'position_size': 'Position Size',
            'optimal_position_size': 'Optimal Position Size',
            'net_return': 'Net Return',
            'max_risk_per_trade': 'Max Risk per Trade',
            'expected_risk_per_trade': 'Expected Risk per Trade',
            'expected_reward_per_trade': 'Expected Reward per Trade',
            'signal_timing_score': 'Signal Timing Score',
            'momentum_correlation': 'Momentum Correlation',
            'volatility_correlation': 'Volatility Correlation',
            'trend_correlation': 'Trend Correlation',
            'risk_adjusted_momentum': 'Risk-Adjusted Momentum',
            'risk_adjusted_trend': 'Risk-Adjusted Trend',
            'risk_reward_setting': 'Risk/Reward Setting',
            'fee_per_trade': 'Fee per Trade'
        }
        
        # Check if we have a special mapping
        if metric_name.lower() in name_mapping:
            return name_mapping[metric_name.lower()]
        
        # Default formatting: convert snake_case to Title Case
        return metric_name.replace('_', ' ').title()
    
    for metric_name, value in metrics.items():
        icon, color, description = get_metric_icon_color_and_description(metric_name, value)
        readable_name = format_metric_name(metric_name)
        
        if color == GREEN:
            good_metrics.append((readable_name, value, icon, description))
        elif color == YELLOW:
            average_metrics.append((readable_name, value, icon, description))
        elif color == RED:
            bad_metrics.append((readable_name, value, icon, description))
    
    # Sort each group alphabetically by metric name
    good_metrics.sort(key=lambda x: x[0])
    average_metrics.sort(key=lambda x: x[0])
    bad_metrics.sort(key=lambda x: x[0])
    
    # Print grouped results
    if good_metrics:
        print(f"\n{BOLD}{GREEN}✅ EXCELLENT METRICS ({len(good_metrics)}):{RESET}")
        print(f"{GREEN}{'='*50}{RESET}")
        for metric_name, value, icon, description in good_metrics:
            # Format value to 2 decimal places
            formatted_value = f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
            print(f"{icon} {BOLD}{metric_name}:{RESET} {GREEN}{formatted_value}{RESET}")
            print(f"   {BLUE}💡 {description}{RESET}")
            print()
    
    if average_metrics:
        print(f"\n{BOLD}{YELLOW}⚠️  AVERAGE METRICS ({len(average_metrics)}):{RESET}")
        print(f"{YELLOW}{'='*50}{RESET}")
        for metric_name, value, icon, description in average_metrics:
            # Format value to 2 decimal places
            formatted_value = f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
            print(f"{icon} {BOLD}{metric_name}:{RESET} {YELLOW}{formatted_value}{RESET}")
            print(f"   {BLUE}💡 {description}{RESET}")
            print()
    
    if bad_metrics:
        print(f"\n{BOLD}{RED}❌ POOR METRICS ({len(bad_metrics)}):{RESET}")
        print(f"{RED}{'='*50}{RESET}")
        for metric_name, value, icon, description in bad_metrics:
            # Format value to 2 decimal places
            formatted_value = f"{value:.2f}" if isinstance(value, (int, float)) else str(value)
            print(f"{icon} {BOLD}{metric_name}:{RESET} {RED}{formatted_value}{RESET}")
            print(f"   {BLUE}💡 {description}{RESET}")
            print()
    
    # Print summary
    total_metrics = len(metrics)
    good_percentage = (len(good_metrics) / total_metrics * 100) if total_metrics > 0 else 0
    average_percentage = (len(average_metrics) / total_metrics * 100) if total_metrics > 0 else 0
    bad_percentage = (len(bad_metrics) / total_metrics * 100) if total_metrics > 0 else 0
    
    print(f"\n{BOLD}📊 STRATEGY QUALITY SUMMARY:{RESET}")
    print(f"{'='*50}")
    print(f"{GREEN}✅ Excellent: {len(good_metrics)} metrics ({good_percentage:.1f}%){RESET}")
    print(f"{YELLOW}⚠️  Average: {len(average_metrics)} metrics ({average_percentage:.1f}%){RESET}")
    print(f"{RED}❌ Poor: {len(bad_metrics)} metrics ({bad_percentage:.1f}%){RESET}")
    
    # Overall assessment
    if good_percentage >= 60:
        overall_color = GREEN
        overall_icon = "🏆"
        overall_assessment = "EXCELLENT"
        overall_description = "Strategy shows outstanding performance across most metrics!"
    elif good_percentage >= 40:
        overall_color = YELLOW
        overall_icon = "🎯"
        overall_assessment = "GOOD"
        overall_description = "Strategy shows good performance with room for improvement."
    else:
        overall_color = RED
        overall_icon = "💔"
        overall_assessment = "NEEDS IMPROVEMENT"
        overall_description = "Strategy needs significant optimization across multiple areas."
    
    print(f"\n{overall_color}{overall_icon} OVERALL ASSESSMENT: {overall_assessment}{RESET}")
    print(f"{overall_color}{overall_description}{RESET}")
