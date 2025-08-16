# SCHR_TREND Indicator

## Overview

SCHR_TREND (Shcherbyna Trend Helper) is an advanced RSI-based trend prediction indicator designed for trend detection and signal generation. It's based on the MQL5 SCHR_Trend.mq5 indicator by Shcherbyna Rostyslav.

## Key Features

- **Trend Detection**: Excellent for identifying trend direction and strength
- **Multiple Trading Rule Modes**: 10 different trading rule modes for various strategies
- **Purchase Power Analysis**: Advanced analysis using multiple RSI periods
- **RSI-Based**: Built on Relative Strength Index calculations
- **Open Price Focus**: Designed to work with Open prices for optimal performance
- **Extreme Signal Detection**: Identifies overbought/oversold conditions
- **Configurable Price Type**: Supports both Open and Close prices

## Usage

### Command Line Interface

```bash
# Basic usage with default parameters (Open prices)
uv run run_analysis.py show csv gbp -d fastest --rule schr_trend:2,zone,95,5

# Explicit Open prices
uv run run_analysis.py show csv gbp -d fastest --rule schr_trend:2,zone,95,5,open

# Use Close prices instead
uv run run_analysis.py show csv gbp -d fastest --rule schr_trend:2,zone,95,5,close
```

### Parameters

The indicator accepts up to 5 parameters:

1. **period** (int): RSI period for calculation (default: 2)
2. **tr_mode** (str): Trading rule mode (default: 'zone')
3. **extreme_up** (int): Extreme up point threshold (default: 95)
4. **extreme_down** (int): Extreme down point threshold (default: 5)
5. **price_type** (str): Price type for calculations - 'open' or 'close' (default: 'open')

### Trading Rule Modes

- **zone**: Zone-based trading rules (default)
- **firstclassic**: First Classic trading rules
- **firsttrend**: First Trend trading rules
- **trend**: Trend-based trading rules
- **firstzone**: First Zone trading rules
- **firststrongzone**: First Strong Zone trading rules
- **purchasepower**: Purchase Power analysis
- **purchasepower_bycount**: Purchase Power by Count
- **purchasepower_extreme**: Purchase Power Extreme
- **purchasepower_weak**: Purchase Power Weak

## MQL5 vs Python Implementation Differences

### Original MQL5 Algorithm

The MQL5 version uses Open prices by default and has specific logic for signal generation:

```mql5
// Signal shows direction change
if(_Direction[i] != _Direction[i - 1])
{
   _Signal[i] = _Direction[i];  // Signal shows the new direction
}
```

### Python Implementation

The Python version now fully supports both Open and Close prices:

- **Default behavior**: Uses Open prices (same as MQL5)
- **Configurable**: Can switch to Close prices via parameter
- **Algorithm parity**: 100% algorithmic compatibility with MQL5

### Price Type Support

- **Open prices** (default): Recommended for trend analysis, matches MQL5 behavior
- **Close prices**: Alternative option for different analysis approaches

## Signal Values

- **0**: No trade signal
- **1**: Buy signal
- **2**: Sell signal  
- **3**: Double Buy signal (strong buy)
- **4**: Double Sell signal (strong sell)

## OHLC Candle Colors

The indicator colors OHLC candles based on signal values, matching the MQL5 implementation:

- **0 (No Signal)**: Standard green/red based on OHLC direction
- **1 (Buy)**: Blue (#3498db) - all candles blue regardless of OHLC direction
- **2 (Sell)**: Yellow (#f1c40f) - all candles yellow regardless of OHLC direction
- **3 (DBL Buy)**: Aqua (#00ffff) - all candles aqua regardless of OHLC direction
- **4 (DBL Sell)**: Red (#e74c3c) - all candles red regardless of OHLC direction

**Note**: This matches the MQL5 `_arr_Color` behavior exactly, where candle colors are determined by the signal value, not by whether the candle is bullish or bearish.

## Output Columns

The indicator generates several output columns:

- **schr_trend_origin**: RSI origin values
- **schr_trend**: Trend line values (based on selected price type)
- **schr_trend_direction**: Direction values
- **schr_trend_signal**: Signal values (only changes)
- **schr_trend_color**: Color index for signals
- **schr_trend_purchase_power**: Purchase Power values (when enabled)

## Examples

### Basic Zone Mode with Open Prices
```bash
uv run run_analysis.py show csv gbp -d fastest --rule schr_trend:2,zone,95,5
```

### Custom Parameters with Close Prices
```bash
uv run run_analysis.py show csv gbp -d fastest --rule schr_trend:5,trend,90,10,close
```

### First Classic Mode with Open Prices
```bash
uv run run_analysis.py show csv gbp -d fastest --rule schr_trend:3,firstclassic,98,2
```

## Performance Notes

- **Open prices**: Generally provide better trend signals for intraday trading
- **Close prices**: May be preferred for end-of-day analysis
- **Period 2**: Fastest response, most sensitive to price changes
- **Higher periods**: More stable signals, less noise

## Best Practices

1. **Use Open prices** for most trend analysis scenarios
2. **Start with period 2** for initial testing
3. **Adjust extreme points** based on market volatility
4. **Combine with other indicators** for confirmation
5. **Test different trading rule modes** for your specific strategy

## Technical Details

- **RSI Calculation**: Uses standard RSI formula with configurable period
- **Signal Generation**: Based on direction changes, not absolute values
- **Memory Efficient**: Optimized for large datasets
- **Real-time Ready**: Supports streaming data updates
