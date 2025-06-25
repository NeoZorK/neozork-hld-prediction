# RSI (Relative Strength Index) Indicator

## Overview

The RSI (Relative Strength Index) indicator has been successfully integrated into the neozork-hld-prediction system. It provides three different calculation modes, each offering unique insights into market momentum and potential reversal points.

## Available RSI Rules

### 1. RSI (Basic)
- **Rule Name**: `RSI`
- **Alias**: `RSI`
- **Description**: Standard RSI calculation with overbought/oversold signals

**Features:**
- Calculates RSI values between 0 and 100
- Generates BUY signals when RSI ≤ 30 (oversold)
- Generates SELL signals when RSI ≥ 70 (overbought)
- Provides support and resistance levels based on RSI extremes
- Uses RSI value as the difference indicator

**Output Columns:**
- `RSI`: RSI values (0-100)
- `RSI_Signal`: Trading signals (BUY/SELL/NOTRADE)
- `PPrice1`: Support level
- `PPrice2`: Resistance level
- `Direction`: Trading direction
- `Diff`: RSI value

### 2. RSI Momentum
- **Rule Name**: `RSI_Momentum`
- **Alias**: `RSI_MOM`
- **Description**: RSI with momentum-based signals

**Features:**
- Calculates RSI momentum (change in RSI)
- Generates BUY signals when RSI rises from oversold levels
- Generates SELL signals when RSI falls from overbought levels
- Dynamic volatility calculation based on momentum strength
- Uses RSI momentum as the difference indicator

**Output Columns:**
- `RSI`: RSI values (0-100)
- `RSI_Momentum`: Change in RSI values
- `RSI_Signal`: Trading signals (BUY/SELL/NOTRADE)
- `PPrice1`: Dynamic support level
- `PPrice2`: Dynamic resistance level
- `Direction`: Trading direction
- `Diff`: RSI momentum

### 3. RSI Divergence
- **Rule Name**: `RSI_Divergence`
- **Alias**: `RSI_DIV`
- **Description**: RSI with divergence detection

**Features:**
- Detects bullish and bearish divergences
- Bearish divergence: Price making higher highs, RSI making lower highs
- Bullish divergence: Price making lower lows, RSI making higher lows
- Calculates divergence strength based on RSI distance from neutral (50)
- Uses divergence strength as the difference indicator

**Output Columns:**
- `RSI`: RSI values (0-100)
- `RSI_Signal`: Trading signals based on divergence
- `PPrice1`: Support level based on divergence strength
- `PPrice2`: Resistance level based on divergence strength
- `Direction`: Trading direction
- `Diff`: Divergence strength (0-1)

## Usage Examples

### Command Line Interface

```bash
# Basic RSI calculation
python -m src.cli.cli demo --rule RSI

# RSI Momentum calculation
python -m src.cli.cli demo --rule RSI_MOM

# RSI Divergence calculation
python -m src.cli.cli demo --rule RSI_DIV

# Using with real data
python -m src.cli.cli yfinance --ticker AAPL --rule RSI --period 1mo
```

### Programmatic Usage

```python
import pandas as pd
from src.calculation.indicator import calculate_pressure_vector
from src.common.constants import TradingRule

# Load your OHLCV data
df = pd.DataFrame({
    'Open': [...],
    'High': [...],
    'Low': [...],
    'Close': [...],
    'TickVolume': [...]
})

# Calculate RSI
point_size = 0.01  # Adjust based on your instrument
result = calculate_pressure_vector(df, point_size, TradingRule.RSI)

# Access RSI values
rsi_values = result['RSI']
trading_signals = result['Direction']
```

## Technical Implementation

### Core Functions

1. **`calculate_rsi(close_prices, period=14)`**
   - Calculates RSI using exponential moving average
   - Handles edge cases and insufficient data
   - Returns RSI values between 0 and 100

2. **`calculate_rsi_signals(rsi_values, overbought=70, oversold=30)`**
   - Generates trading signals based on overbought/oversold levels
   - Returns BUY, SELL, or NOTRADE signals

3. **`calculate_rsi_levels(open_prices, rsi_values, overbought=70, oversold=30)`**
   - Calculates support and resistance levels
   - Uses volatility-based approach

### Rule Functions

1. **`apply_rule_rsi(df, point, rsi_period=14, overbought=70, oversold=30)`**
   - Applies basic RSI rule logic
   - Sets all required output columns

2. **`apply_rule_rsi_momentum(df, point, rsi_period=14, overbought=70, oversold=30)`**
   - Applies RSI momentum rule logic
   - Calculates momentum and dynamic levels

3. **`apply_rule_rsi_divergence(df, point, rsi_period=14, overbought=70, oversold=30)`**
   - Applies RSI divergence rule logic
   - Detects price/RSI divergences

## Integration with Existing System

The RSI indicator is fully integrated with the existing system:

- **Constants**: Added to `TradingRule` enum
- **Rules**: Integrated into rule dispatcher
- **CLI**: Added aliases and help text
- **Indicator Module**: Properly handles RSI rules without calculating unnecessary intermediate values
- **Tests**: Comprehensive test coverage for all RSI functionality

## Key Features

1. **No Breaking Changes**: RSI implementation doesn't affect existing indicators
2. **Consistent Interface**: Uses same output format as other indicators
3. **Configurable Parameters**: Period, overbought, and oversold levels can be adjusted
4. **Robust Error Handling**: Handles edge cases and insufficient data gracefully
5. **Comprehensive Testing**: Full test coverage for all RSI functionality

## Performance Considerations

- RSI calculation is efficient using pandas operations
- No unnecessary intermediate calculations for RSI rules
- Memory usage is optimized for large datasets
- Calculation time scales linearly with data size

## Future Enhancements

Potential improvements for the RSI indicator:

1. **Custom Periods**: Allow user-defined RSI periods via CLI
2. **Multiple Timeframes**: Support for different RSI periods simultaneously
3. **Advanced Divergence**: More sophisticated divergence detection algorithms
4. **RSI Filters**: Additional filters for signal quality
5. **Backtesting**: Integration with backtesting framework

## Troubleshooting

### Common Issues

1. **No RSI values calculated**: Ensure sufficient data points (at least period + 1)
2. **All NaN values**: Check for constant price data or insufficient volatility
3. **Unexpected signals**: Verify overbought/oversold threshold settings

### Debug Mode

Use the debug script to test RSI functionality:

```bash
python test_rsi_debug.py
```

This will show detailed information about RSI calculations and help identify any issues. 