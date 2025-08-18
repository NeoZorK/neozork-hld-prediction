# Adding Custom Indicators to neozork-hld-prediction

## Overview

This comprehensive tutorial will guide you through the process of adding your own custom indicators to the neozork-hld-prediction platform. We'll use the **SMA (Simple Moving Average)** indicator as a practical example to demonstrate the complete workflow.

## What You'll Learn

- ✅ How to create a new indicator module
- ✅ How to integrate it into the platform architecture
- ✅ How to add help and documentation
- ✅ How to write comprehensive tests
- ✅ How to test your indicator in real scenarios

## Prerequisites

- Basic understanding of Python
- Familiarity with pandas and numpy
- Access to the neozork-hld-prediction codebase

## Step-by-Step Guide

### Step 1: Create the Indicator Module

First, create a new file in the appropriate category directory. For SMA, we'll place it in the trend indicators:

**File:** `src/calculation/indicators/trend/sma_ind.py`

```python
# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/sma_ind.py

"""
INDICATOR INFO:
Name: SMA
Category: Trend
Description: Simple Moving Average. A type of moving average that gives equal weight to all prices in the calculation period.
Usage: --rule sma:20,close or --rule sma:20,open
Parameters: period, price_type
Pros: + Simple and easy to understand, + Smooths out price noise, + Good for trend identification
Cons: - Can lag behind price changes, - May give false signals in volatile markets, - Equal weight may not reflect recent market conditions

SMA (Simple Moving Average) indicator calculation module.
"""

import pandas as pd
import numpy as np
from ....common import logger
from ....common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType


def calculate_sma(price_series: pd.Series, period: int = 20) -> pd.Series:
    """
    Calculates the Simple Moving Average (SMA).
    
    Args:
        price_series (pd.Series): Series of prices (Open or Close)
        period (int): SMA calculation period (default: 20)
    
    Returns:
        pd.Series: SMA values
    """
    if period <= 0:
        raise ValueError("SMA period must be positive")
    
    if len(price_series) < period:
        logger.print_warning(f"Not enough data for SMA calculation. Need at least {period} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float)
    
    # Calculate SMA using pandas rolling mean
    sma = price_series.rolling(window=period, min_periods=period).mean()
    
    return sma


def calculate_sma_signals(price_series: pd.Series, sma_values: pd.Series) -> pd.Series:
    """
    Calculate trading signals based on price vs SMA.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        sma_values (pd.Series): SMA values
    
    Returns:
        pd.Series: Trading signals (BUY, SELL, NOTRADE)
    """
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Price crosses above SMA
    buy_condition = (price_series > sma_values) & (price_series.shift(1) <= sma_values.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Price crosses below SMA
    sell_condition = (price_series < sma_values) & (price_series.shift(1) >= sma_values.shift(1))
    signals[sell_condition] = SELL
    
    return signals


def apply_rule_sma(df: pd.DataFrame, point: float, 
                   sma_period: int = 20, price_type: PriceType = PriceType.CLOSE):
    """
    Applies SMA rule logic to calculate trading signals and price levels.
    
    Args:
        df (pd.DataFrame): Input DataFrame with OHLCV data
        point (float): Instrument point size
        sma_period (int): SMA calculation period
        price_type (PriceType): Price type to use for SMA calculation (OPEN or CLOSE)
    
    Returns:
        pd.DataFrame: DataFrame with SMA calculations and signals
    """
    open_prices = df['Open']
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:  # PriceType.CLOSE
        price_series = df['Close']
        price_name = "Close"
    
    # Calculate SMA
    df['SMA'] = calculate_sma(price_series, sma_period)
    
    # Add price type info to column name
    df['SMA_Price_Type'] = price_name
    
    # Calculate SMA signals
    df['SMA_Signal'] = calculate_sma_signals(price_series, df['SMA'])
    
    # Calculate support and resistance levels based on SMA
    # Use SMA as dynamic support/resistance
    sma_values = df['SMA']
    
    # Support level: SMA with small buffer
    support_levels = sma_values * 0.995  # 0.5% below SMA
    
    # Resistance level: SMA with small buffer
    resistance_levels = sma_values * 1.005  # 0.5% above SMA
    
    # Set output columns
    df['PPrice1'] = support_levels  # Support level
    df['PColor1'] = BUY
    df['PPrice2'] = resistance_levels  # Resistance level
    df['PColor2'] = SELL
    df['Direction'] = df['SMA_Signal']
    df['Diff'] = price_series - sma_values  # Use price - SMA as difference indicator
    
    return df
```

### Step 2: Add to Constants

Add your indicator to the `TradingRule` enum in `src/common/constants.py`:

```python
class TradingRule(Enum):
    # ... existing rules ...
    SMA = 12  # Simple Moving Average
    # ... rest of rules ...
```

**Note:** Make sure to update the numbering of subsequent rules accordingly.

### Step 3: Register in Rules System

Add your indicator to the rules dispatcher in `src/calculation/rules.py`:

```python
# Import your indicator
from .indicators.trend.sma_ind import apply_rule_sma

# Add to RULE_DISPATCHER
RULE_DISPATCHER = {
    # ... existing rules ...
    TradingRule.SMA: apply_rule_sma,
    # ... rest of rules ...
}

# Add parameter handling in apply_trading_rule function
elif selected_rule == TradingRule.SMA:
    # Extract SMA-specific parameters
    sma_period = kwargs.get('sma_period', 20)
    return rule_func(df, point=point, sma_period=sma_period, price_type=price_type_enum)
```

### Step 4: Add to CLI System

Add your indicator to the CLI parsing system in `src/cli/cli.py`:

```python
# Add to valid_indicators list
valid_indicators = ['rsi', 'rsi_mom', 'rsi_div', 'macd', 'stoch', 'stochastic', 'stochoscillator', 'ema', 'sma', 'bb', ...]

# Add parameter parsing function
def parse_sma_parameters(params_str: str) -> tuple[str, dict]:
    """Parse SMA parameters: period,price_type"""
    params = params_str.split(',')
    if len(params) != 2:
        raise ValueError(f"SMA requires exactly 2 parameters: period,price_type. Got: {params_str}")
    
    try:
        period = int(float(params[0].strip()))  # Handle float values
        price_type = params[1].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid SMA parameters: {params_str}. Error: {e}")
    
    if price_type not in ['open', 'close']:
        raise ValueError(f"SMA price_type must be 'open' or 'close', got: {price_type}")
    
    return 'sma', {
        'sma_period': period,
        'price_type': price_type
    }

# Add to parse_indicator_parameters function
elif indicator_name == 'sma':
    return parse_sma_parameters(params_str)

# Add to help_info dictionary
'sma': {
    'name': 'SMA (Simple Moving Average)',
    'format': 'sma:period,price_type',
    'parameters': [
        'period (int): SMA period (default: 20)',
        'price_type (string): Price type for calculation - open or close (default: close)'
    ],
    'examples': [
        'sma:20,close',
        'sma:50,open'
    ]
},
```

### Step 5: Add to Enhanced Help System

Add comprehensive help information in `src/cli/error_handling.py`:

```python
'sma': {
    'name': 'SMA (Simple Moving Average)',
    'description': 'Simple moving average that gives equal weight to all prices in the calculation period.',
    'format': 'sma:period,price_type',
    'parameters': [
        ('period', 'int', 'SMA period', '20'),
        ('price_type', 'string', 'Price type for calculation', 'close')
    ],
    'examples': [
        ('sma:20,close', 'Standard SMA with close prices'),
        ('sma:50,open', 'Long-term SMA with open prices'),
        ('sma:10,close', 'Short-term SMA with close prices')
    ],
    'tips': [
        'Use period 20 for standard analysis',
        'Shorter periods are more responsive to price changes',
        'Longer periods provide smoother signals',
        'SMA is less responsive than EMA but more stable',
        'Open prices are more volatile, close prices are more stable'
    ],
    'common_errors': [
        'Invalid price_type: Use "open" or "close" only',
        'Invalid period: Must be a positive integer',
        'Period too short may give unreliable results'
    ]
},
```

### Step 6: Add to Calculation System

Add your indicator to the calculation system in `src/calculation/indicator_calculation.py`:

```python
# Add to rule_aliases_map
'SMA': 'SMA',
```

### Step 7: Create Comprehensive Tests

Create a test file for your indicator:

**File:** `tests/calculation/indicators/trend/test_sma_indicator.py`

```python
# -*- coding: utf-8 -*-
# tests/calculation/indicators/trend/test_sma_indicator.py

"""
Tests for SMA (Simple Moving Average) indicator.
"""

import pytest
import pandas as pd
import numpy as np
from src.calculation.indicators.trend.sma_ind import calculate_sma, apply_rule_sma
from src.calculation.indicators.base_indicator import PriceType


class TestSMAIndicator:
    """Test class for SMA indicator calculations."""
    
    def setup_method(self):
        """Set up test data."""
        # Create sample OHLCV data
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        np.random.seed(42)  # For reproducible tests
        
        # Generate realistic price data
        base_price = 100.0
        price_changes = np.random.normal(0, 1, 50)  # Random price changes
        prices = [base_price]
        
        for change in price_changes[1:]:
            new_price = prices[-1] + change
            prices.append(max(new_price, 1.0))  # Ensure positive prices
        
        self.sample_data = pd.DataFrame({
            'Open': prices,
            'High': [p * 1.02 for p in prices],  # High is 2% above open
            'Low': [p * 0.98 for p in prices],   # Low is 2% below open
            'Close': [p * 1.01 for p in prices], # Close is 1% above open
            'Volume': np.random.randint(1000, 10000, 50)
        }, index=dates)
        
        self.point = 0.01  # Point size for testing
    
    def test_calculate_sma_basic(self):
        """Test basic SMA calculation."""
        period = 10
        close_prices = self.sample_data['Close']
        sma_values = calculate_sma(close_prices, period)
        
        # Check that SMA is calculated
        assert len(sma_values) == len(close_prices)
        assert not sma_values.isna().all()
        
        # Check that first (period-1) values are NaN
        assert sma_values.iloc[:period-1].isna().all()
        
        # Check that period-th value is not NaN
        assert not pd.isna(sma_values.iloc[period-1])
        
        # Check that SMA is reasonable (within price range)
        assert sma_values.iloc[period-1] > 0
        assert sma_values.iloc[period-1] < close_prices.max() * 1.1
    
    def test_calculate_sma_different_periods(self):
        """Test SMA calculation with different periods."""
        close_prices = self.sample_data['Close']
        
        for period in [5, 10, 20]:
            sma_values = calculate_sma(close_prices, period)
            
            # Check that first (period-1) values are NaN
            assert sma_values.iloc[:period-1].isna().all()
            
            # Check that period-th value is not NaN
            assert not pd.isna(sma_values.iloc[period-1])
            
            # Check that SMA values are reasonable
            assert sma_values.iloc[period-1] > 0
    
    def test_calculate_sma_invalid_period(self):
        """Test SMA calculation with invalid period."""
        close_prices = self.sample_data['Close']
        
        # Test with zero period
        with pytest.raises(ValueError, match="SMA period must be positive"):
            calculate_sma(close_prices, 0)
        
        # Test with negative period
        with pytest.raises(ValueError, match="SMA period must be positive"):
            calculate_sma(close_prices, -5)
    
    def test_calculate_sma_insufficient_data(self):
        """Test SMA calculation with insufficient data."""
        short_data = self.sample_data.head(5)
        close_prices = short_data['Close']
        
        # Should not raise error, but return NaN values
        sma_values = calculate_sma(close_prices, 10)
        assert sma_values.isna().all()
    
    def test_apply_rule_sma_close_prices(self):
        """Test SMA rule application with close prices."""
        result = apply_rule_sma(self.sample_data, point=self.point, 
                               sma_period=10, price_type=PriceType.CLOSE)
        
        # Check that required columns are added
        assert 'SMA' in result.columns
        assert 'SMA_Price_Type' in result.columns
        assert 'SMA_Signal' in result.columns
        
        # Check that output columns are present
        assert 'PPrice1' in result.columns
        assert 'PPrice2' in result.columns
        assert 'PColor1' in result.columns
        assert 'PColor2' in result.columns
        assert 'Direction' in result.columns
        assert 'Diff' in result.columns
        
        # Check price type
        assert result['SMA_Price_Type'].iloc[0] == 'Close'
        
        # Check that SMA values are calculated
        assert not result['SMA'].isna().all()
        
        # Check that signals are calculated
        assert 'SMA_Signal' in result.columns
    
    def test_apply_rule_sma_open_prices(self):
        """Test SMA rule application with open prices."""
        result = apply_rule_sma(self.sample_data, point=self.point, 
                               sma_period=10, price_type=PriceType.OPEN)
        
        # Check price type
        assert result['SMA_Price_Type'].iloc[0] == 'Open'
        
        # Check that SMA values are calculated
        assert not result['SMA'].isna().all()
    
    def test_apply_rule_sma_default_parameters(self):
        """Test SMA rule application with default parameters."""
        result = apply_rule_sma(self.sample_data, point=self.point)
        
        # Should use default period (20) and close prices
        assert result['SMA_Price_Type'].iloc[0] == 'Close'
        
        # Check that SMA values are calculated
        assert not result['SMA'].isna().all()
    
    def test_apply_rule_sma_support_resistance_levels(self):
        """Test that SMA rule calculates support and resistance levels."""
        result = apply_rule_sma(self.sample_data, point=self.point, 
                               sma_period=10, price_type=PriceType.CLOSE)
        
        # Check that support and resistance levels are calculated
        assert not result['PPrice1'].isna().all()  # Support levels
        assert not result['PPrice2'].isna().all()  # Resistance levels
        
        # Check that support is below resistance
        valid_mask = ~(result['PPrice1'].isna() | result['PPrice2'].isna())
        if valid_mask.any():
            assert (result.loc[valid_mask, 'PPrice1'] <= result.loc[valid_mask, 'PPrice2']).all()
    
    def test_apply_rule_sma_signals(self):
        """Test that SMA rule generates trading signals."""
        result = apply_rule_sma(self.sample_data, point=self.point, 
                               sma_period=10, price_type=PriceType.CLOSE)
        
        # Check that signals are generated
        assert 'SMA_Signal' in result.columns
        assert not result['SMA_Signal'].isna().all()
        
        # Check that signals are valid values (0, 1, 2)
        valid_signals = result['SMA_Signal'].dropna()
        assert all(signal in [0, 1, 2] for signal in valid_signals)
    
    def test_apply_rule_sma_difference_calculation(self):
        """Test that SMA rule calculates price difference."""
        result = apply_rule_sma(self.sample_data, point=self.point, 
                               sma_period=10, price_type=PriceType.CLOSE)
        
        # Check that difference is calculated
        assert 'Diff' in result.columns
        assert not result['Diff'].isna().all()
        
        # Check that difference is price - SMA
        valid_mask = ~(result['SMA'].isna() | result['Close'].isna())
        if valid_mask.any():
            expected_diff = result.loc[valid_mask, 'Close'] - result.loc[valid_mask, 'SMA']
            actual_diff = result.loc[valid_mask, 'Diff']
            pd.testing.assert_series_equal(expected_diff, actual_diff, check_names=False)
```

### Step 8: Test Your Implementation

Run the tests to ensure everything works correctly:

```bash
# Run tests for your indicator
uv run pytest tests/calculation/indicators/trend/test_sma_indicator.py -v

# Test the indicator with real data
uv run run_analysis.py show csv mn1 -d fastest --rule sma:20,close

# Test help system
uv run run_analysis.py show csv mn1 --rule sma:invalid
```

## Key Components Explained

### 1. Indicator Module Structure

Your indicator module should contain:

- **INDICATOR INFO section**: Metadata about your indicator
- **Calculation functions**: Core mathematical logic
- **Signal generation**: Trading signal logic
- **Main rule function**: Integration point with the platform

### 2. Required Output Columns

Your `apply_rule_*` function must set these columns:

- `PPrice1`: Support level or buy signal price
- `PPrice2`: Resistance level or sell signal price
- `PColor1`: Buy signal color (1.0 for BUY)
- `PColor2`: Sell signal color (2.0 for SELL)
- `Direction`: Trading direction (0=NOTRADE, 1=BUY, 2=SELL)
- `Diff`: Difference indicator (price - indicator value)

### 3. Parameter Handling

- Use the `PriceType` enum for price type selection
- Validate parameters and provide meaningful error messages
- Support default values for better user experience

### 4. Error Handling

- Validate input data and parameters
- Provide clear error messages
- Handle edge cases (insufficient data, invalid parameters)

## Best Practices

### 1. Code Organization

- Follow the existing naming conventions
- Use descriptive function and variable names
- Add comprehensive docstrings
- Include type hints

### 2. Testing

- Write unit tests for all functions
- Test edge cases and error conditions
- Ensure 100% test coverage
- Test with real data scenarios

### 3. Documentation

- Provide clear usage examples
- Document all parameters and their effects
- Include tips and common pitfalls
- Add comprehensive help information

### 4. Performance

- Use vectorized operations when possible
- Avoid loops in calculation functions
- Handle large datasets efficiently
- Provide meaningful progress feedback

## Example Usage

Once implemented, your indicator can be used like this:

```bash
# Basic usage with default parameters
uv run run_analysis.py show csv mn1 -d fastest --rule sma

# Custom parameters
uv run run_analysis.py show csv mn1 -d fastest --rule sma:20,close
uv run run_analysis.py show csv mn1 -d fastest --rule sma:50,open

# With different drawing backends
uv run run_analysis.py show csv mn1 -d plotly --rule sma:20,close
uv run run_analysis.py show csv mn1 -d term --rule sma:20,close
```

## Troubleshooting

### Common Issues

1. **Indicator not recognized**: Check that you've added it to all required lists and mappings
2. **Parameter parsing errors**: Ensure your parsing function handles all edge cases
3. **Calculation errors**: Verify your mathematical logic and data validation
4. **Test failures**: Check that your tests cover all scenarios

### Debug Tips

1. Use the debug output to verify data flow
2. Check the generated plots to validate calculations
3. Compare with known indicator values
4. Test with different datasets and parameters

## Next Steps

After successfully adding your first indicator:

1. **Create more complex indicators**: Multi-line indicators, oscillators, etc.
2. **Add advanced features**: Custom signal logic, multiple timeframes
3. **Optimize performance**: Profile and improve calculation speed
4. **Extend testing**: Add integration tests and performance benchmarks

## Conclusion

This tutorial has shown you how to add a custom indicator to the neozork-hld-prediction platform. The SMA example demonstrates all the key components and best practices needed for successful integration.

Remember to:
- ✅ Follow the established patterns and conventions
- ✅ Write comprehensive tests
- ✅ Provide clear documentation and help
- ✅ Test thoroughly with real data
- ✅ Handle errors gracefully

Your custom indicators will now work seamlessly with the platform's analysis, plotting, and reporting features!
