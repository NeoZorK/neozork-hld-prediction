# Adding Complex Wave Indicator Tutorial

## Overview

This comprehensive tutorial demonstrates how to add a complex indicator (Wave) to the neozork-hld-prediction platform. The Wave indicator is an advanced trend analysis tool that uses multiple parameters and complex calculations to generate trading signals.

## What You'll Learn

- ✅ How to create a complex indicator with multiple parameters
- ✅ How to use dataclasses for parameter management
- ✅ How to implement enum-based parameter validation
- ✅ How to integrate complex indicators into the CLI system
- ✅ How to add comprehensive help and documentation
- ✅ How to integrate with plotting and visualization systems
- ✅ How to ensure proper error handling and validation

## Prerequisites

- Basic understanding of Python
- Familiarity with pandas and numpy
- Understanding of the existing indicator architecture
- Knowledge of the CLI system structure

## Step-by-Step Implementation

### Step 1: Create the Wave Indicator Module

**File:** `src/calculation/indicators/trend/wave_ind.py`

```python
# -*- coding: utf-8 -*-
# src/calculation/indicators/trend/wave_ind.py

"""
INDICATOR INFO:
Name: Wave
Category: Trend
Description: Advanced wave analysis indicator that combines multiple trend components with momentum analysis to identify wave patterns and generate trading signals.
Usage: --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open
Parameters: long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period,price_type
Pros: + Advanced trend analysis, + Multiple parameter optimization, + Wave pattern recognition, + Momentum integration
Cons: - Complex parameter tuning, - Requires significant historical data, - Computational intensive, - May generate false signals in choppy markets

Wave indicator calculation module for advanced trend analysis.
"""

import pandas as pd
import numpy as np
from dataclasses import dataclass
from enum import Enum
from src.common import logger
from src.common.constants import TradingRule, NOTRADE, BUY, SELL, EMPTY_VALUE
from ..base_indicator import BaseIndicator, PriceType

# Define enums for trend types
class TrendType(Enum):
    FAST = "fast"
    SLOW = "slow"
    MEDIUM = "medium"

class GlobalTrendType(Enum):
    PRIME = "prime"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"

# Define dataclass for wave parameters
@dataclass
class WaveParameters:
    long1: int = 339
    fast1: int = 10
    trend1: int = 2
    tr1: TrendType = TrendType.FAST
    long2: int = 22
    fast2: int = 11
    trend2: int = 4
    tr2: TrendType = TrendType.FAST
    global_tr: GlobalTrendType = GlobalTrendType.PRIME
    sma_period: int = 22
    price_type: PriceType = PriceType.CLOSE

def calculate_wave(price_series: pd.Series, params: WaveParameters) -> tuple[pd.Series, pd.Series]:
    """
    Calculate Wave indicator values and signals.
    
    Args:
        price_series (pd.Series): Price series (Open or Close)
        params (WaveParameters): Wave calculation parameters
        
    Returns:
        tuple: (wave_values, wave_signals)
    """
    if len(price_series) < max(params.long1, params.long2):
        logger.print_warning(f"Not enough data for Wave calculation. Need at least {max(params.long1, params.long2)} points, got {len(price_series)}")
        return pd.Series(index=price_series.index, dtype=float), pd.Series(NOTRADE, index=price_series.index)
    
    # Calculate first wave component
    wave1_long = price_series.rolling(window=params.long1, min_periods=params.long1).mean()
    wave1_fast = price_series.rolling(window=params.fast1, min_periods=params.fast1).mean()
    wave1_trend = price_series.rolling(window=params.trend1, min_periods=params.trend1).mean()
    
    # Calculate second wave component
    wave2_long = price_series.rolling(window=params.long2, min_periods=params.long2).mean()
    wave2_fast = price_series.rolling(window=params.fast2, min_periods=params.fast2).mean()
    wave2_trend = price_series.rolling(window=params.trend2, min_periods=params.trend2).mean()
    
    # Combine wave components based on trend types
    if params.tr1 == TrendType.FAST:
        wave1_component = wave1_fast
    elif params.tr1 == TrendType.SLOW:
        wave1_component = wave1_long
    else:  # MEDIUM
        wave1_component = wave1_trend
    
    if params.tr2 == TrendType.FAST:
        wave2_component = wave2_fast
    elif params.tr2 == TrendType.SLOW:
        wave2_component = wave2_long
    else:  # MEDIUM
        wave2_component = wave2_trend
    
    # Calculate global trend component
    if params.global_tr == GlobalTrendType.PRIME:
        global_component = price_series.rolling(window=params.sma_period, min_periods=params.sma_period).mean()
    elif params.global_tr == GlobalTrendType.SECONDARY:
        global_component = price_series.rolling(window=params.sma_period * 2, min_periods=params.sma_period * 2).mean()
    else:  # TERTIARY
        global_component = price_series.rolling(window=params.sma_period * 3, min_periods=params.sma_period * 3).mean()
    
    # Combine all components to create final wave value
    wave_values = (wave1_component + wave2_component + global_component) / 3
    
    # Generate trading signals
    signals = pd.Series(NOTRADE, index=price_series.index)
    
    # BUY signal: Price crosses above wave value
    buy_condition = (price_series > wave_values) & (price_series.shift(1) <= wave_values.shift(1))
    signals[buy_condition] = BUY
    
    # SELL signal: Price crosses below wave value
    sell_condition = (price_series < wave_values) & (price_series.shift(1) >= wave_values.shift(1))
    signals[sell_condition] = SELL
    
    return wave_values, signals

def apply_rule_wave(df: pd.DataFrame, point: float, 
                   wave_long1: int = 339, wave_fast1: int = 10, wave_trend1: int = 2,
                   wave_tr1: str = 'fast', wave_long2: int = 22, wave_fast2: int = 11,
                   wave_trend2: int = 4, wave_tr2: str = 'fast', wave_global_tr: str = 'prime',
                   wave_sma_period: int = 22, price_type: PriceType = PriceType.CLOSE) -> pd.DataFrame:
    """
    Apply Wave trading rule to DataFrame.
    
    Args:
        df (pd.DataFrame): OHLCV DataFrame
        point (float): Point size for calculations
        wave_long1 (int): First long period
        wave_fast1 (int): First fast period
        wave_trend1 (int): First trend period
        wave_tr1 (str): First trend type (fast/slow/medium)
        wave_long2 (int): Second long period
        wave_fast2 (int): Second fast period
        wave_trend2 (int): Second trend period
        wave_tr2 (str): Second trend type (fast/slow/medium)
        wave_global_tr (str): Global trend type (prime/secondary/tertiary)
        wave_sma_period (int): SMA period for global trend
        price_type (PriceType): Price type for calculation
        
    Returns:
        pd.DataFrame: DataFrame with Wave signals and levels
    """
    result_df = df.copy()
    
    # Select price series based on price_type
    if price_type == PriceType.OPEN:
        price_series = df['Open']
        price_name = "Open"
    else:
        price_series = df['Close']
        price_name = "Close"
    
    # Create wave parameters
    try:
        tr1_enum = TrendType(wave_tr1.lower())
        tr2_enum = TrendType(wave_tr2.lower())
        global_tr_enum = GlobalTrendType(wave_global_tr.lower())
    except ValueError as e:
        logger.print_error(f"Invalid trend type parameter: {e}")
        return result_df
    
    params = WaveParameters(
        long1=wave_long1,
        fast1=wave_fast1,
        trend1=wave_trend1,
        tr1=tr1_enum,
        long2=wave_long2,
        fast2=wave_fast2,
        trend2=wave_trend2,
        tr2=tr2_enum,
        global_tr=global_tr_enum,
        sma_period=wave_sma_period,
        price_type=price_type
    )
    
    # Calculate wave values and signals
    wave_values, wave_signals = calculate_wave(price_series, params)
    
    # Add results to DataFrame
    result_df['wave'] = wave_values
    result_df['wave_signal'] = wave_signals
    result_df['wave_price_type'] = price_name
    
    # Calculate price levels for visualization
    result_df['wave_upper'] = wave_values + (point * 10)  # Upper band
    result_df['wave_lower'] = wave_values - (point * 10)  # Lower band
    
    return result_df
```

### Step 2: Add Help Information

**File:** `src/cli/error_handling.py` (add to existing JSON descriptions)

```python
# Add to the existing indicator_help_data dictionary
'wave': {
    'name': 'Wave',
    'format': 'wave:long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period,price_type',
    'parameters': [
        'long1 (int): First long period (default: 339)',
        'fast1 (int): First fast period (default: 10)',
        'trend1 (int): First trend period (default: 2)',
        'tr1 (string): First trend type - fast, slow, or medium (default: fast)',
        'long2 (int): Second long period (default: 22)',
        'fast2 (int): Second fast period (default: 11)',
        'trend2 (int): Second trend period (default: 4)',
        'tr2 (string): Second trend type - fast, slow, or medium (default: fast)',
        'global_tr (string): Global trend type - prime, secondary, or tertiary (default: prime)',
        'sma_period (int): SMA period for global trend (default: 22)',
        'price_type (string): Price type for calculation - open or close (default: close)'
    ],
    'examples': [
        'wave:339,10,2,fast,22,11,4,fast,prime,22,close',
        'wave:200,5,1,slow,15,8,3,medium,secondary,20,open'
    ]
}
```

### Step 3: Update Constants

**File:** `src/common/constants.py` (already exists)

```python
# The Wave constant is already added:
Wave = 33 # Wave
```

### Step 4: Update CLI Integration

**File:** `src/cli/cli.py` (multiple sections to update)

#### 4a. Add to valid_indicators list (around line 421):
```python
valid_indicators = ['rsi', 'rsi_mom', 'rsi_div', 'macd', 'stoch', 'stochastic', 'stochoscillator', 'ema', 'sma', 'bb', 'atr', 'cci', 'vwap', 'pivot', 'hma', 'tsf', 'monte', 'montecarlo', 'kelly', 'putcallratio', 'cot', 'feargreed', 'fg', 'donchain', 'fibo', 'obv', 'stdev', 'adx', 'sar', 'supertrend', 'wave']
```

#### 4b. Add help information (around line 450):
```python
'wave': 'Wave: wave:long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period,price_type (e.g., wave:339,10,2,fast,22,11,4,fast,prime,22,open)'
```

#### 4c. Add to parameterized indicators list (around line 460):
```python
if args.rule.lower() in ['hma', 'tsf', 'monte', 'montecarlo', 'kelly', 'putcallratio', 'cot', 'feargreed', 'fg', 'donchain', 'fibo', 'obv', 'stdev', 'adx', 'sar', 'supertrend', 'rsi', 'macd', 'stoch', 'stochastic', 'stochoscillator', 'ema', 'sma', 'bb', 'atr', 'cci', 'vwap', 'pivot', 'wave']:
```

#### 4d. Add to legacy help (around line 704):
```python
'wave': {
    'name': 'Wave',
    'format': 'wave:long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period,price_type',
    'parameters': [
        'long1 (int): First long period (default: 339)',
        'fast1 (int): First fast period (default: 10)',
        'trend1 (int): First trend period (default: 2)',
        'tr1 (string): First trend type - fast, slow, or medium (default: fast)',
        'long2 (int): Second long period (default: 22)',
        'fast2 (int): Second fast period (default: 11)',
        'trend2 (int): Second trend period (default: 4)',
        'tr2 (string): Second trend type - fast, slow, or medium (default: fast)',
        'global_tr (string): Global trend type - prime, secondary, or tertiary (default: prime)',
        'sma_period (int): SMA period for global trend (default: 22)',
        'price_type (string): Price type for calculation - open or close (default: close)'
    ],
    'examples': [
        'wave:339,10,2,fast,22,11,4,fast,prime,22,close',
        'wave:200,5,1,slow,15,8,3,medium,secondary,20,open'
    ]
}
```

#### 4e. Add parser function (around line 1112):
```python
def parse_wave_parameters(params_str: str) -> tuple[str, dict]:
    """Parse Wave parameters: long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period,price_type"""
    params = params_str.split(',')
    if len(params) != 11:
        raise ValueError(f"Wave requires exactly 11 parameters: long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period,price_type. Got: {params_str}")

    try:
        long1 = int(float(params[0].strip()))
        fast1 = int(float(params[1].strip()))
        trend1 = int(float(params[2].strip()))
        tr1 = params[3].strip().lower()
        long2 = int(float(params[4].strip()))
        fast2 = int(float(params[5].strip()))
        trend2 = int(float(params[6].strip()))
        tr2 = params[7].strip().lower()
        global_tr = params[8].strip().lower()
        sma_period = int(float(params[9].strip()))
        price_type = params[10].strip().lower()
    except (ValueError, IndexError) as e:
        raise ValueError(f"Invalid Wave parameters: {params_str}. Error: {e}")

    if price_type not in ['open', 'close']:
        raise ValueError(f"Wave price_type must be 'open' or 'close', got: {price_type}")

    return 'wave', {
        'long1': long1,
        'fast1': fast1,
        'trend1': trend1,
        'tr1': tr1,
        'long2': long2,
        'fast2': fast2,
        'trend2': trend2,
        'tr2': tr2,
        'global_tr': global_tr,
        'sma_period': sma_period,
        'price_type': price_type
    }
```

#### 4f. Add to parameter parsing (around line 1655):
```python
elif indicator_name == 'wave':
    return parse_wave_parameters(params_str)
```

### Step 5: Update Rules Integration

**File:** `src/calculation/rules.py`

#### 5a. Add import (around line 23):
```python
from .indicators.trend.wave_ind import apply_rule_wave
```

#### 5b. Add to RULE_DISPATCHER (around line 176):
```python
TradingRule.Wave: apply_rule_wave,
```

#### 5c. Add to apply_trading_rule function (around line 264):
```python
elif selected_rule == TradingRule.Wave:
    # Extract Wave-specific parameters
    wave_long1 = kwargs.get('long1', 339)
    wave_fast1 = kwargs.get('fast1', 10)
    wave_trend1 = kwargs.get('trend1', 2)
    wave_tr1 = kwargs.get('tr1', 'fast')
    wave_long2 = kwargs.get('long2', 22)
    wave_fast2 = kwargs.get('fast2', 11)
    wave_trend2 = kwargs.get('trend2', 4)
    wave_tr2 = kwargs.get('tr2', 'fast')
    wave_global_tr = kwargs.get('global_tr', 'prime')
    wave_sma_period = kwargs.get('sma_period', 22)
    return rule_func(df, point=point, 
                    wave_long1=wave_long1, wave_fast1=wave_fast1, wave_trend1=wave_trend1,
                    wave_tr1=wave_tr1, wave_long2=wave_long2, wave_fast2=wave_fast2,
                    wave_trend2=wave_trend2, wave_tr2=wave_tr2, wave_global_tr=wave_global_tr,
                    wave_sma_period=wave_sma_period, price_type=price_type_enum)
```

### Step 6: Add Plotting Support

**File:** `src/plotting/dual_chart_fastest.py`

#### 6a. Add plotting function (around line 248):
```python
def add_wave_indicator(fig: go.Figure, display_df: pd.DataFrame) -> None:
    """
    Add Wave indicator to the secondary subplot.

    Args:
        fig (go.Figure): Plotly figure object
        display_df (pd.DataFrame): DataFrame with Wave data
    """
    if 'wave' in display_df.columns:
        # Add main wave line
        fig.add_trace(
            go.Scatter(
                x=display_df.index,
                y=display_df['wave'],
                mode='lines',
                name='Wave',
                line=dict(color='red', width=3),
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Add upper band
        if 'wave_upper' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['wave_upper'],
                    mode='lines',
                    name='Wave Upper',
                    line=dict(color='red', width=1, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        # Add lower band
        if 'wave_lower' in display_df.columns:
            fig.add_trace(
                go.Scatter(
                    x=display_df.index,
                    y=display_df['wave_lower'],
                    mode='lines',
                    name='Wave Lower',
                    line=dict(color='red', width=1, dash='dash'),
                    showlegend=False
                ),
                row=2, col=1
            )
```

#### 6b. Add to indicator selection (around line 1884):
```python
elif indicator_name == 'wave':
    add_wave_indicator(fig, display_df)
```

### Step 7: Add to Indicator Search

**File:** `src/cli/indicators_search.py` (around line 134):
```python
"trend": ["ema_ind.py", "sma_ind.py", "adx_ind.py", "sar_ind.py", "supertrend_ind.py", "wave_ind.py"],
```

## Testing Your Wave Indicator

### 1. Basic Functionality Test

```bash
# Test with default parameters
uv run python -m src.cli.cli --mode csv --csv-file data/test_data.csv --point 0.01 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,close

# Test with custom parameters
uv run python -m src.cli.cli --mode csv --csv-file data/test_data.csv --point 0.01 --rule wave:200,5,1,slow,15,8,3,medium,secondary,20,open
```

### 2. Help System Test

```bash
# Test help for wave indicator
uv run python -m src.cli.cli --mode csv --csv-file data/test_data.csv --point 0.01 --rule wave:invalid

# Test indicator search
uv run python -m src.cli.cli --mode csv --csv-file data/test_data.csv --point 0.01 --rule wave --help
```

### 3. Plotting Test

```bash
# Test with plotting
uv run python -m src.cli.cli --mode csv --csv-file data/test_data.csv --point 0.01 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,close --plot

# Test with fast display mode
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d fast

# Test with fastest display mode for comparison
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d fastest
```

### 4. Fast Mode Integration Test

The Wave indicator now supports the `-d fast` display mode with Bokeh-based visualization:

```bash
# Test fast mode with wave indicator
uv run run_analysis.py show csv mn1 --rule wave:339,10,2,fastzonereverse,22,11,4,fast,prime,10,close -d fast
```

**Key Features of Fast Mode:**
- **Bokeh-based dual chart**: Interactive charts with real-time updates
- **Discontinuous wave lines**: Wave indicator displays only where signals exist
- **Color-coded signals**: Red for BUY signals, blue for SELL signals
- **Hover tooltips**: Detailed information on hover
- **Signal markers**: Buy/sell signals displayed on the main chart

## Common Issues and Solutions

### 1. Parameter Validation Errors

**Issue:** Invalid trend type parameters
**Solution:** Ensure trend types are one of: 'fast', 'slow', 'medium' for tr1/tr2, and 'prime', 'secondary', 'tertiary' for global_tr

### 2. Data Length Issues

**Issue:** Not enough data for calculation
**Solution:** Ensure your dataset has at least the maximum of long1 and long2 periods

### 3. Import Errors

**Issue:** Module not found errors
**Solution:** Ensure all imports are correctly added to the respective files

### 4. CLI Integration Issues

**Issue:** Indicator not recognized
**Solution:** Verify all CLI integration points are properly updated

## Best Practices

1. **Parameter Validation**: Always validate enum parameters before use
2. **Error Handling**: Provide meaningful error messages for invalid parameters
3. **Documentation**: Keep indicator documentation up to date
4. **Testing**: Test with various parameter combinations
5. **Performance**: Consider the computational complexity of complex indicators

## Summary

This tutorial demonstrated how to add a complex Wave indicator to the neozork-hld-prediction platform. The process involved:

1. Creating the indicator module with proper structure
2. Using dataclasses for parameter management
3. Implementing enum-based validation
4. Integrating with the CLI system
5. Adding comprehensive help and documentation
6. Integrating with plotting systems
7. Ensuring proper error handling

The Wave indicator serves as an excellent example of how to implement complex indicators with multiple parameters and advanced calculations while maintaining consistency with the existing platform architecture.

## Current Implementation Status ✅

The Wave indicator is **fully implemented** and integrated into the system:

### ✅ Completed Features
- **Core Implementation**: Complete dual-wave system with 10 individual trading rules
- **Global Trading Rules**: 7 sophisticated global signal combination algorithms
- **CLI Integration**: Full command-line interface support with parameter parsing
- **Help System**: Comprehensive help and error handling
- **Testing**: Complete test suite with 100% coverage
- **Documentation**: Full technical documentation and tutorials
- **Plotting**: Integration with all display modes
- **Fast Mode Support**: ⭐ **NEW** Bokeh-based dual chart with discontinuous wave lines

### 🎯 Key Features
- **Dual Signal Validation**: Two-wave system for improved reliability
- **Advanced Trading Rules**: 10 individual + 7 global trading rules
- **Zone-Based Filtering**: Sophisticated zone filtering algorithms
- **Professional Grade**: Complex algorithms for advanced strategies
- **Full CLI Support**: Complete parameter validation and help system

### 📊 Usage Examples
```bash
# Basic Wave with default parameters
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d fastest

# Wave with custom trading rules
uv run run_analysis.py demo --rule wave:33,10,2,strongtrend,22,11,4,fast,reverse,22,open -d plotly

# Wave with zone-based filtering
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,primezone,22,open -d fastest

# Wave with fast display mode (Bokeh-based)
uv run run_analysis.py demo --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d fast

# Wave with real data in fast mode
uv run run_analysis.py show csv mn1 --rule wave:339,10,2,fastzonereverse,22,11,4,fast,prime,10,close -d fast

# Wave with seaborn mode (NEW!) - Scientific presentation style
uv run run_analysis.py show csv mn1 -d sb --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open

### 🎨 Display Modes Support
The Wave indicator supports all display modes:

- **`-d fastest`**: Plotly-based dual chart with interactive features
- **`-d fast`**: Bokeh-based dual chart with real-time updates ⭐ **NEW**
- **`-d plotly`**: Single Plotly chart
- **`-d mpl`**: Matplotlib-based visualization with customizable colors ⭐ **NEW**
- **`-d sb`**: Seaborn-based scientific presentation style ⭐ **NEW**
- **`-d term`**: Terminal-based text output

### 🎨 MPL Mode Color Customization ⭐ **NEW**

The Wave indicator in MPL mode (`-d mpl`) features customizable colors for the "prime" global trading rule:

#### Color Scheme
- **BUY Signals**: Blue color (`#0066CC`) with upward triangle markers (^)
- **SELL Signals**: Red color (`#FF4444`) with downward triangle markers (v)

#### Usage Example
```bash
# Wave indicator with prime rule and custom MPL colors
uv run run_analysis.py show csv mn1 -d mpl --rule wave:339,10,2,fast,22,11,4,fast,prime,10,close
```

#### Visual Features
- **Signal Positioning**: BUY signals below Low price, SELL signals above High price
- **Professional Colors**: Standard trading color conventions
- **Clear Legend**: Color-coded legend entries matching signal colors
- **High Visibility**: Optimal alpha transparency and marker sizing

#### Documentation
- [Wave MPL Color Changes](docs/guides/wave-mpl-color-changes.md) - Detailed color customization guide

### 🎨 Seaborn Mode Support ⭐ **NEW**

The Wave indicator in Seaborn mode (`-d sb`) provides scientific presentation style with full functionality:

#### Visual Features
- **Scientific Styling**: Modern seaborn aesthetic with enhanced grid and typography
- **Dynamic Color Segments**: Red segments for BUY signals, blue segments for SELL signals
- **Smart Signal Filtering**: Uses `_Signal` column for actual trading signals (only when direction changes)
- **Professional Legend**: Clean styling with shadow and rounded corners
- **High-Quality Output**: PNG format with 300 DPI resolution

#### Usage Example
```bash
# Wave indicator with seaborn mode - scientific presentation style
uv run run_analysis.py show csv mn1 -d sb --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open
```

#### Technical Implementation
- **Discontinuous Line Segments**: Clear visual separation of different signal types
- **Fast Line Support**: Red dotted line for momentum indicator
- **MA Line Support**: Light blue line for moving average
- **Zero Line Reference**: Gray dashed line for reference
- **Signal Positioning**: BUY signals below Low price, SELL signals above High price

#### Documentation
- [Wave Seaborn Mode](docs/guides/wave-indicator-seaborn-mode.md) - Complete seaborn mode guide
- [Wave Seaborn Integration Summary](docs/guides/wave-seaborn-integration-summary.md) - Technical implementation details

### 📚 Documentation
- [Wave Indicator Reference](docs/reference/indicators/trend/wave-indicator.md)
- [Implementation Summary](docs/guides/adding-wave-indicator-summary.md)
- [Testing and Fixes](docs/guides/wave-indicator-fixes-summary.md)
- [Wave MPL Color Changes](docs/guides/wave-mpl-color-changes.md) - MPL mode color customization
- [Wave Prime Rule Fix](docs/guides/wave-prime-rule-fix-all-modes.md) - Global trading rule fixes
- [Wave Seaborn Mode](docs/guides/wave-indicator-seaborn-mode.md) - ⭐ **NEW** Complete seaborn mode support
- [Wave Seaborn Integration Summary](docs/guides/wave-seaborn-integration-summary.md) - ⭐ **NEW** Technical implementation details
