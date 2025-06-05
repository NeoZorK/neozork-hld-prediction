# src/plotting/term_plot.py
"""
Terminal plotting using plotext for OHLCV and indicator panels.
Supports line charts, bars, and multi-panel indicators in the terminal.
"""
import plotext as plt
import pandas as pd
import numpy as np
from src.common import logger
from src.common.constants import TradingRule

def _plot_financial_indicators_panels(df: pd.DataFrame, x_data: list, x_labels: list, step: int, rule=None):
    """
    Plot financial indicators in separate panels for better visualization.

    Args:
        df: DataFrame with financial data
        x_data: list of x positions
        x_labels: list of x-axis labels
        step: step size for x-ticks
        rule: Trading rule being applied, if None or OHLCV only price data is shown
    """
    # Skip indicator panels if rule is None or OHLCV
    if rule is None or (hasattr(rule, 'name') and rule.name == 'OHLCV'):
        return

    # Define indicator categories and their colors
    momentum_indicators = {
        'RSI': 'green+',
        'MACD': 'red+', 
        'Signal': 'orange+',
        'Stochastic': 'yellow+'
    }
    
    trend_indicators = {
        'MA': 'blue+',
        'SMA': 'blue+',
        'EMA': 'cyan+',
        'BB_Upper': 'gray+',
        'BB_Lower': 'gray+',
        'BB_Middle': 'white+'
    }
    
    volume_indicators = {
        'PV': 'red+',
        'Volume_MA': 'purple+'
    }
    
    custom_indicators = {
        'HL': 'yellow+',
        'Pressure': 'magenta+',
        'PPrice1': 'lime+',
        'PPrice2': 'red+'
    }
    
    # Panel 1: Momentum Indicators
    momentum_cols = [col for col in df.columns if col in momentum_indicators and not df[col].isna().all()]
    if momentum_cols:
        plt.clear_data()
        print("\n📊 MOMENTUM INDICATORS")
        
        for col in momentum_cols:
            color = momentum_indicators[col]
            data = df[col].tolist()
            plt.plot(x_data, data, label=col, color=color)

            # Add reference lines for RSI
            if col == 'RSI':
                plt.plot(x_data, [70] * len(x_data), label="Overbought (70)", color="red")
                plt.plot(x_data, [30] * len(x_data), label="Oversold (30)", color="green")
        
        plt.title("Momentum Indicators")
        plt.xlabel("Time")
        plt.ylabel("Values")
        plt.xticks(x_data[::step], x_labels[::step])
        plt.show()
    
    # Panel 2: Trend Indicators  
    trend_cols = [col for col in df.columns if col in trend_indicators and not df[col].isna().all()]
    if trend_cols:
        plt.clear_data()
        print("\n📈 TREND INDICATORS")
        
        for col in trend_cols:
            color = trend_indicators[col]
            data = df[col].tolist()
            plt.plot(x_data, data, label=col, color=color)

        plt.title("Trend Indicators")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.xticks(x_data[::step], x_labels[::step])
        plt.show()
    
    # Panel 3: Volume Indicators
    volume_cols = [col for col in df.columns if col in volume_indicators and not df[col].isna().all()]
    if volume_cols:
        plt.clear_data()
        print("\n📊 VOLUME INDICATORS")
        
        for col in volume_cols:
            color = volume_indicators[col]
            data = df[col].tolist()
            
            if col == 'PV':
                # PV can be positive/negative, add zero line
                plt.plot(x_data, data, label=col, color=color)
                plt.plot(x_data, [0] * len(x_data), label="Zero Line", color="gray")
            else:
                plt.plot(x_data, data, label=col, color=color)

        plt.title("Volume Indicators")
        plt.xlabel("Time")
        plt.ylabel("Volume")
        plt.xticks(x_data[::step], x_labels[::step])
        plt.show()
    
    # Panel 4: Custom Indicators (HL, Pressure, etc.)
    custom_cols = [col for col in df.columns if col in custom_indicators and not df[col].isna().all()]
    if custom_cols:
        plt.clear_data()
        print("\n🔧 CUSTOM INDICATORS")
        
        for col in custom_cols:
            color = custom_indicators[col]
            data = df[col].tolist()
            
            if col in ['Pressure', 'HL']:
                # These can have positive/negative values
                plt.plot(x_data, data, label=col, color=color)
                plt.plot(x_data, [0] * len(x_data), label="Zero Line", color="gray")
            else:
                plt.plot(x_data, data, label=col, color=color)

        plt.title("Custom Indicators")
        plt.xlabel("Time")
        plt.ylabel("Values")
        plt.xticks(x_data[::step], x_labels[::step])
        plt.show()


def _plot_predicted_prices(df: pd.DataFrame, x_data: list, x_labels: list, step: int, rule=None):
    """
    Plot predicted price levels if available.

    Args:
        df: DataFrame with financial data
        x_data: list of x positions
        x_labels: list of x-axis labels
        step: step size for x-ticks
        rule: Trading rule being applied, if None or OHLCV predicted prices aren't shown
    """
    # Skip predicted prices if rule is None or OHLCV
    if rule is None or (hasattr(rule, 'name') and rule.name == 'OHLCV'):
        return

    predicted_cols = [col for col in df.columns if 'predicted' in col.lower() or 'pprice' in col.lower()]
    predicted_cols = [col for col in predicted_cols if not df[col].isna().all()]
    
    if predicted_cols:
        plt.clear_data()
        print("\n🎯 PREDICTED PRICES")
        
        # Plot actual close price for reference
        if 'Close' in df.columns:
            plt.plot(x_data, df['Close'].tolist(), label="Close Price", color="cyan+")

        # Plot predicted prices
        colors = ['lime+', 'red+', 'yellow+', 'magenta+', 'orange+']
        for i, col in enumerate(predicted_cols[:5]):
            color = colors[i % len(colors)]
            data = df[col].tolist()
            plt.plot(x_data, data, label=col, color=color)

        plt.title("Price Predictions")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.xticks(x_data[::step], x_labels[::step])
        plt.show()


def _plot_trading_signals(df: pd.DataFrame, x_data: list, x_labels: list, step: int, rule=None):
    """
    Plot trading signals and direction indicators.

    Args:
        df: DataFrame with financial data
        x_data: list of x positions
        x_labels: list of x-axis labels
        step: step size for x-ticks
        rule: Trading rule being applied, if None or OHLCV trading signals aren't shown
    """
    # Skip trading signals if rule is None or OHLCV
    if rule is None or (hasattr(rule, 'name') and rule.name == 'OHLCV'):
        return

    signal_cols = [col for col in df.columns if col.lower() in ['direction', 'signal', 'buy_signal', 'sell_signal']]
    signal_cols = [col for col in signal_cols if not df[col].isna().all()]
    
    if signal_cols:
        plt.clear_data()
        print("\n🚦 TRADING SIGNALS")
        
        for col in signal_cols:
            data = df[col].tolist()
            
            if col.lower() == 'direction':
                # Direction: 1=Buy, -1/2=Sell, 0=Hold
                buy_points = [1 if val == 1 else 0 for val in data]
                sell_points = [1 if val in [-1, 2] else 0 for val in data]
                
                plt.bar(x_data, buy_points, label="Buy Signal", color="green+")
                plt.bar(x_data, [-val for val in sell_points], label="Sell Signal", color="red+")
            else:
                # Generic signal plotting
                plt.plot(x_data, data, label=col, color="orange+", marker="circle")
        
        plt.title("Trading Signals")
        plt.xlabel("Time")
        plt.ylabel("Signal Strength")
        plt.xticks(x_data[::step], x_labels[::step])
        plt.show()


def _calculate_simple_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Placeholder function that no longer calculates simple indicators.
    According to new requirements, we don't need to show SMA, RSI and other indicators by default.

    Args:
        df: DataFrame with data

    Returns:
        DataFrame without changes
    """
    # According to requirements, we no longer calculate indicators by default
    return df.copy()


def plot_indicator_results_term(df: pd.DataFrame, rule: TradingRule, title: str = "Indicator Results"):
    """
    Plots OHLCV and indicators in the terminal using plotext.
    Uses simple line charts for better compatibility.
    """
    if df is None or df.empty:
        logger.print_warning("No data to plot in terminal mode.")
        return

    try:
        # Clear any previous plots
        plt.clear_data()
        
        # Limit data points for terminal display (last 80 points for better visibility)
        max_points = 80
        if len(df) > max_points:
            df = df.tail(max_points).copy()

        # Prepare x-axis data
        x_data = list(range(len(df)))
        
        # Generate x-axis labels from index
        if isinstance(df.index, pd.DatetimeIndex):
            x_labels = [d.strftime('%m-%d') for d in df.index]
        else:
            x_labels = [f"T{i}" for i in x_data]

        print(f"\n{title}")
        print("=" * 60)
        
        # Plot 1: OHLC Price Chart
        plt.clear_data()
        plt.canvas_color('black')
        plt.axes_color('black')

        # Plot OHLC as simple line charts (avoid candlestick issues)
        if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
            plt.plot(x_data, df['Close'].tolist(), label="Close", color="cyan+")
            plt.plot(x_data, df['High'].tolist(), label="High", color="green+")
            plt.plot(x_data, df['Low'].tolist(), label="Low", color="red+")

            print("\n📈 PRICE CHART")
        else:
            # Fallback to available price columns
            price_cols = [col for col in df.columns if col.lower() in ['price', 'close', 'value', 'adj close']]
            if price_cols:
                plt.plot(x_data, df[price_cols[0]].tolist(), label=price_cols[0], color="cyan+")
                print(f"\n📈 {price_cols[0].upper()} CHART")
            else:
                logger.print_warning("No price data found for plotting.")
                return

        plt.title("Price Movement")
        plt.xlabel("Time")
        plt.ylabel("Price")
        
        # Set readable x-axis labels
        step = max(1, len(x_labels) // 8)
        plt.xticks(x_data[::step], x_labels[::step])
        
        plt.show()
        
        # Plot 2: Volume Chart (if available)
        if 'Volume' in df.columns and df['Volume'].sum() > 0:
            plt.clear_data()
            vol_data = df['Volume'].tolist()
            plt.bar(x_data, vol_data, label="Volume", color="blue+")
            plt.title("Volume")
            plt.xlabel("Time")
            plt.ylabel("Volume")
            plt.xticks(x_data[::step], x_labels[::step])
            print("\n📊 VOLUME CHART")
            plt.show()

        # Calculate additional indicators if needed
        df = _calculate_simple_indicators(df)
        
        # Plot 3: Financial Indicators in Multiple Panels
        _plot_financial_indicators_panels(df, x_data, x_labels, step, rule)

        # Plot 4: Predicted Price Lines (if available)
        _plot_predicted_prices(df, x_data, x_labels, step, rule)

        # Plot 5: Trading Signals (if available)
        _plot_trading_signals(df, x_data, x_labels, step, rule)

        # Print data summary
        print("\n📋 DATA SUMMARY")
        print("-" * 30)
        print(f"Data points: {len(df)}")
        print(f"Rule applied: {rule.name if hasattr(rule, 'name') else str(rule)}")
        
        if 'Close' in df.columns:
            close_prices = df['Close']
            print(f"Price range: ${close_prices.min():.2f} - ${close_prices.max():.2f}")
            
        # Find all indicators for summary
        all_indicators = []
        indicator_types = ['RSI', 'MACD', 'Signal', 'MA', 'SMA', 'EMA', 'PV', 'HL', 'Pressure', 'PPrice1', 'PPrice2']
        for col in df.columns:
            if any(ind in col for ind in indicator_types) and not df[col].isna().all():
                all_indicators.append(col)
        
        if all_indicators:
            print(f"Indicators: {', '.join(all_indicators)}")
            
        logger.print_info(f"Terminal plot completed successfully with {len(df)} data points")
            
    except Exception as e:
        logger.print_error(f"Error in terminal plotting: {str(e)}")
        # Ultra-simple fallback
        try:
            plt.clear_data()
            plt.canvas_color('black')
            plt.axes_color('black')
            if 'Close' in df.columns:
                close_data = df['Close'].tolist()
                plt.plot(range(len(close_data)), close_data, label="Close Price", color="cyan+")
                plt.title(f"{title} - Price Chart")
                plt.xlabel("Time Points")
                plt.ylabel("Price")
                plt.show()
                print(f"\n✅ Simple price chart displayed ({len(close_data)} points)")
            else:
                print(f"❌ Terminal plotting failed: {str(e)}")
        except Exception as fallback_e:
            logger.print_error(f"Even fallback plotting failed: {str(fallback_e)}")
            print(f"❌ Terminal plotting unavailable. Error: {str(e)}")
