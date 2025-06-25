# Core Calculation Reference

Core calculation components for technical indicators and analysis.

## Overview

The core calculation module provides the foundation for all technical indicator calculations and analysis workflows.

## Components

### Core Calculations (`core_calculations.py`)

Fundamental mathematical calculations used across all indicators.

#### Functions

- **`calculate_ema(data, period)`** - Exponential Moving Average calculation
- **`calculate_sma(data, period)`** - Simple Moving Average calculation
- **`calculate_std(data, period)`** - Standard Deviation calculation
- **`calculate_atr(high, low, close, period)`** - Average True Range calculation

#### Usage Example

```python
from src.calculation.core_calculations import calculate_ema, calculate_sma

# Calculate EMA for price data
ema_values = calculate_ema(price_data, period=14)

# Calculate SMA for volume data
sma_values = calculate_sma(volume_data, period=20)
```

### Indicator Calculation (`indicator_calculation.py`)

Main orchestrator for indicator calculations and data processing.

#### Key Features

- **Multi-indicator processing** - Calculate multiple indicators simultaneously
- **Data validation** - Ensure data quality before calculations
- **Performance optimization** - Efficient calculation algorithms
- **Error handling** - Robust error management

#### Main Classes

##### `IndicatorCalculator`

Primary class for indicator calculations.

```python
from src.calculation.indicator_calculation import IndicatorCalculator

# Initialize calculator
calculator = IndicatorCalculator()

# Calculate indicators
results = calculator.calculate_indicators(
    data=price_data,
    indicators=['rsi', 'macd', 'bollinger_bands'],
    params={'rsi_period': 14, 'macd_fast': 12, 'macd_slow': 26}
)
```

#### Methods

- **`calculate_indicators(data, indicators, params)`** - Calculate multiple indicators
- **`validate_data(data)`** - Validate input data quality
- **`process_results(results)`** - Process and format calculation results

### Rules Engine (`rules.py`)

Trading rules and signal generation system.

#### Trading Rules

##### PHLD (Price High Low Direction)
- **Purpose**: Predict price direction based on high-low patterns
- **Parameters**: Lookback period, threshold values
- **Output**: Buy/Sell signals with confidence levels

##### PV (Pressure Vector)
- **Purpose**: Measure market pressure and momentum
- **Parameters**: Pressure calculation period, vector components
- **Output**: Pressure direction and magnitude

##### SR (Support Resistance)
- **Purpose**: Identify support and resistance levels
- **Parameters**: Level detection sensitivity, confirmation periods
- **Output**: Support/resistance levels with strength indicators

#### Usage Example

```python
from src.calculation.rules import PHLDRule, PressureVectorRule

# Initialize rules
phld_rule = PHLDRule(lookback_period=20, threshold=0.02)
pv_rule = PressureVectorRule(period=14)

# Apply rules to data
phld_signals = phld_rule.apply(price_data)
pv_signals = pv_rule.apply(price_data)
```

### Base Indicator (`base_indicator.py`)

Abstract base class for all technical indicators.

#### Abstract Methods

- **`calculate(data, **params)`** - Main calculation method
- **`validate_params(params)`** - Parameter validation
- **`get_name()`** - Indicator name
- **`get_description()`** - Indicator description

#### Implementation Example

```python
from src.calculation.indicators.base_indicator import BaseIndicator

class CustomIndicator(BaseIndicator):
    def __init__(self, period=14):
        self.period = period
    
    def calculate(self, data, **params):
        # Implementation here
        pass
    
    def validate_params(self, params):
        # Validation logic
        pass
    
    def get_name(self):
        return "Custom Indicator"
    
    def get_description(self):
        return "Custom technical indicator"
```

## Data Requirements

### Input Data Format

All calculations expect OHLCV (Open, High, Low, Close, Volume) data in pandas DataFrame format:

```python
import pandas as pd

# Required columns
data = pd.DataFrame({
    'open': [...],
    'high': [...],
    'low': [...],
    'close': [...],
    'volume': [...],
    'timestamp': [...]  # Optional, for time-based calculations
})
```

### Data Quality Requirements

- **No missing values** in OHLC data
- **Positive values** for all price data
- **Non-negative values** for volume data
- **Chronological order** for time series data
- **Minimum data points** based on indicator requirements

## Performance Considerations

### Optimization Features

- **Vectorized calculations** using NumPy and Pandas
- **Lazy evaluation** for complex indicators
- **Memory efficient** processing for large datasets
- **Caching** for repeated calculations

### Performance Tips

1. **Batch processing** - Calculate multiple indicators together
2. **Data preprocessing** - Clean data before calculations
3. **Parameter optimization** - Use appropriate parameter values
4. **Memory management** - Process data in chunks for large datasets

## Error Handling

### Common Errors

- **Insufficient data** - Not enough data points for calculation
- **Invalid parameters** - Parameters outside valid ranges
- **Data type errors** - Incorrect data types
- **Missing columns** - Required OHLCV columns not present

### Error Recovery

```python
from src.calculation.indicator_calculation import IndicatorCalculator

try:
    calculator = IndicatorCalculator()
    results = calculator.calculate_indicators(data, indicators=['rsi'])
except ValueError as e:
    print(f"Parameter error: {e}")
except RuntimeError as e:
    print(f"Calculation error: {e}")
```

## Testing

### Unit Tests

```bash
# Run core calculation tests
pytest tests/calculation/test_core_calculations.py -v

# Run indicator calculation tests
pytest tests/calculation/test_indicator_calculation.py -v

# Run rules tests
pytest tests/calculation/test_rules.py -v
```

### Integration Tests

```bash
# Run integration tests
pytest tests/calculation/integration/ -v

# Run performance tests
pytest tests/calculation/performance/ -v
```

## Related Documentation

- **[Technical Indicators](indicators/)** - Individual indicator documentation
- **[Data Acquisition](../api/data-sources.md)** - Data source integration
- **[CLI Interface](../guides/cli-interface.md)** - Command-line usage
- **[Export Functions](../guides/export-functions.md)** - Data export capabilities 