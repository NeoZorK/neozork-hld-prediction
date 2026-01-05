# Terminal Chunked Plot Modules Reference

## Module Overview

The terminal chunked plotting functionality has been organized into the following modules:

## Base Module: `term_chunked_plot_base.py`

Contains fundamental utility functions used across all plotting modules.

### Functions

- **`get_terminal_plot_size() -> Tuple[int, int]`**
  - Determines the plot size for terminal mode
  - Returns: (width, height) tuple

- **`calculate_optimal_chunk_size(total_rows: int, target_chunks: int = 10, min_chunk_size: int = 50, max_chunk_size: int = 200) -> int`**
  - Calculates optimal chunk size based on data length
  - Parameters:
    - `total_rows`: Total number of data rows
    - `target_chunks`: Target number of chunks (default: 10)
    - `min_chunk_size`: Minimum chunk size (default: 50)
    - `max_chunk_size`: Maximum chunk size (default: 200)
  - Returns: Optimal chunk size

- **`split_dataframe_into_chunks(df: pd.DataFrame, chunk_size: int) -> List[pd.DataFrame]`**
  - Splits a DataFrame into chunks of specified size
  - Returns: List of DataFrame chunks

- **`parse_rsi_rule(rule: str) -> Tuple[str, Dict[str, Any]]`**
  - Parses RSI rule string to extract parameters
  - Returns: (rule_type, params) tuple

- **`draw_ohlc_candles(chunk: pd.DataFrame, x_values: List) -> None`**
  - Draws OHLC candlestick chart using plotext
  - Parameters:
    - `chunk`: DataFrame with OHLC data
    - `x_values`: X-axis values

## Helpers Module: `term_chunked_plot_helpers.py`

Contains helper functions for colors, field plotting, signals, and statistics.

### Functions

- **`_get_field_color(field_name: str) -> str`**
  - Returns color for a field based on its name
  - Uses hash-based color assignment for consistency

- **`_plot_single_field_chunk(chunk: pd.DataFrame, field: str, title: str, style: str) -> None`**
  - Plots a single field from a chunk
  - Parameters:
    - `chunk`: DataFrame chunk
    - `field`: Field name to plot
    - `title`: Plot title
    - `style`: Plot style

- **`_has_trading_signals(chunk: pd.DataFrame) -> bool`**
  - Checks if chunk has trading signals (Direction column)
  - Returns: True if signals exist

- **`_add_trading_signals_to_chunk(chunk: pd.DataFrame, x_values: List) -> None`**
  - Adds trading signals (BUY/SELL) to the plot
  - Parameters:
    - `chunk`: DataFrame chunk with Direction column
    - `x_values`: X-axis values

- **`_show_chunk_statistics(chunk: pd.DataFrame, title: str, start_idx: int, end_idx: int) -> None`**
  - Displays statistics for a chunk
  - Parameters:
    - `chunk`: DataFrame chunk
    - `title`: Statistics title
    - `start_idx`: Start index
    - `end_idx`: End index

- **`_show_field_statistics(chunk: pd.DataFrame, field: str) -> None`**
  - Displays statistics for a specific field
  - Parameters:
    - `chunk`: DataFrame chunk
    - `field`: Field name

## Overlays Module: `term_chunked_plot_overlays.py`

Contains functions to add specific overlays to chunk plots.

### Functions

- **`_add_pv_overlays_to_chunk(chunk: pd.DataFrame, x_values: List) -> None`**
  - Adds PV-specific overlays (buy/sell signals only)
  - Parameters:
    - `chunk`: DataFrame chunk with PV data
    - `x_values`: X-axis values

- **`_add_sr_overlays_to_chunk(chunk: pd.DataFrame, x_values: List) -> None`**
  - Adds SR-specific overlays (support/resistance lines)
  - Parameters:
    - `chunk`: DataFrame chunk with SR data
    - `x_values`: X-axis values

- **`_add_phld_overlays_to_chunk(chunk: pd.DataFrame, x_values: List) -> None`**
  - Adds PHLD-specific overlays (two channels and signals)
  - Parameters:
    - `chunk`: DataFrame chunk with PHLD data
    - `x_values`: X-axis values

- **`_add_rsi_overlays_to_chunk(chunk: pd.DataFrame, x_values: List, rule_type: str, params: Dict) -> None`**
  - Adds RSI-specific overlays based on rule type
  - Parameters:
    - `chunk`: DataFrame chunk with RSI data
    - `x_values`: X-axis values
    - `rule_type`: RSI rule type (rsi, rsi_mom, rsi_div)
    - `params`: RSI parameters

- **`_add_macd_overlays_to_chunk(chunk: pd.DataFrame, x_values: List) -> None`**
  - Adds MACD-specific overlays
  - Parameters:
    - `chunk`: DataFrame chunk with MACD data
    - `x_values`: X-axis values

## Indicators Module: `term_chunked_plot_indicators.py`

Contains all indicator functions for subplots.

### Main Functions

- **`_add_macd_chart_to_subplot(chunk: pd.DataFrame, x_values: List) -> None`**
  - Adds MACD chart to a subplot
  - Parameters:
    - `chunk`: DataFrame chunk with MACD data
    - `x_values`: X-axis values

- **`_add_indicator_chart_to_subplot(chunk: pd.DataFrame, x_values: List, indicator_name: str, rule: str = "") -> None`**
  - Generic function to add indicator chart to subplot
  - Routes to specific indicator functions based on indicator name
  - Parameters:
    - `chunk`: DataFrame chunk
    - `x_values`: X-axis values
    - `indicator_name`: Name of the indicator
    - `rule`: Original rule string for parameter extraction

### Specific Indicator Functions

All `_add_*_indicator_to_subplot()` functions follow the same pattern:
- Take `chunk: pd.DataFrame` and `x_values: List` as parameters
- Add indicator-specific plots to the subplot
- Handle missing columns gracefully

Supported indicators:
- RSI (`_add_rsi_indicator_to_subplot`)
- Stochastic (`_add_stochastic_indicator_to_subplot`)
- CCI (`_add_cci_indicator_to_subplot`)
- Bollinger Bands (`_add_bollinger_bands_to_subplot`)
- EMA (`_add_ema_indicator_to_subplot`)
- SMA (`_add_sma_indicator_to_subplot`)
- ADX (`_add_adx_indicator_to_subplot`)
- SAR (`_add_sar_indicator_to_subplot`)
- SuperTrend (`_add_supertrend_indicator_to_subplot`)
- ATR (`_add_atr_indicator_to_subplot`)
- Standard Deviation (`_add_std_indicator_to_subplot`)
- OBV (`_add_obv_indicator_to_subplot`)
- VWAP (`_add_vwap_indicator_to_subplot`)
- HMA (`_add_hma_indicator_to_subplot`)
- Time Series Forecast (`_add_tsf_indicator_to_subplot`)
- Monte Carlo (`_add_monte_carlo_indicator_to_subplot`)
- Kelly Criterion (`_add_kelly_indicator_to_subplot`)
- Put/Call Ratio (`_add_putcall_indicator_to_subplot`)
- COT (`_add_cot_indicator_to_subplot`)
- Fear & Greed (`_add_fear_greed_indicator_to_subplot`)
- Pivot Points (`_add_pivot_points_to_subplot`)
- Fibonacci Retracement (`_add_fibonacci_indicator_to_subplot`)
- Donchian Channel (`_add_donchian_indicator_to_subplot`)
- Wave (`_add_wave_indicator_to_subplot`)
- Generic (`_add_generic_indicator_to_subplot`)

## Plotting Function Modules

Each plotting function has its own module with a single main function.

### `term_chunked_plot_ohlcv.py`

- **`plot_ohlcv_chunks(df: pd.DataFrame, title: str = "OHLC Chunks", style: str = "matrix", Use_Navigation: bool = False) -> None`**
  - Plots OHLC data in chunks (no volume charts)
  - Parameters:
    - `df`: DataFrame with OHLC data
    - `title`: Base title for plots
    - `style`: Plot style
    - `Use_Navigation`: Whether to use interactive navigation

### `term_chunked_plot_auto.py`

- **`plot_auto_chunks(df: pd.DataFrame, title: str = "AUTO Chunks", style: str = "matrix", Use_Navigation: bool = False) -> None`**
  - Plots all fields in chunks with separate charts for each field
  - Uses AutoTerminalNavigator for field switching

### `term_chunked_plot_pv.py`

- **`plot_pv_chunks(df: pd.DataFrame, title: str = "PV Chunks", style: str = "matrix", Use_Navigation: bool = False) -> None`**
  - Plots PV (Pressure Vector) data with channels and signals
  - OHLC candles are always shown as the base layer

### `term_chunked_plot_sr.py`

- **`plot_sr_chunks(df: pd.DataFrame, title: str = "SR Chunks", style: str = "matrix", Use_Navigation: bool = False) -> None`**
  - Plots SR (Support/Resistance) data with support/resistance lines
  - OHLC candles are always shown as the base layer

### `term_chunked_plot_phld.py`

- **`plot_phld_chunks(df: pd.DataFrame, title: str = "PHLD Chunks", style: str = "matrix", Use_Navigation: bool = False) -> None`**
  - Plots PHLD (Predict High Low Direction) data with two channels and signals
  - OHLC candles are always shown as the base layer

### `term_chunked_plot_rsi.py`

- **`plot_rsi_chunks(df: pd.DataFrame, rule: str, title: str = "RSI Chunks", style: str = "matrix", Use_Navigation: bool = False) -> None`**
  - Plots RSI data based on rule type (rsi, rsi_mom, rsi_div)
  - Parameters:
    - `df`: DataFrame with RSI data
    - `rule`: RSI rule string (e.g., "rsi(14,70,30,close)")
    - `title`: Base title for plots
    - `style`: Plot style
    - `Use_Navigation`: Whether to use interactive navigation

### `term_chunked_plot_macd.py`

- **`plot_macd_chunks(df: pd.DataFrame, title: str = "MACD Chunks", style: str = "matrix", Use_Navigation: bool = False) -> None`**
  - Plots MACD data with MACD lines and trading signals
  - Uses dual subplot: OHLC (50%) and MACD (50%)

### `term_chunked_plot_indicator.py`

- **`plot_indicator_chunks(df: pd.DataFrame, indicator_name: str, title: str = "Indicator Chunks", style: str = "matrix", Use_Navigation: bool = False, rule: str = "") -> None`**
  - Generic function to plot any indicator in chunks
  - Uses dual subplot: OHLC (50%) and Indicator (50%)
  - Parameters:
    - `df`: DataFrame with indicator data
    - `indicator_name`: Name of the indicator
    - `title`: Base title for plots
    - `style`: Plot style
    - `Use_Navigation`: Whether to use interactive navigation
    - `rule`: Original rule string for parameter extraction

## Main Module: `term_chunked_plot.py`

The main entry point that imports and re-exports all functions.

### Main Function

- **`plot_chunked_terminal(df: pd.DataFrame, rule: str, title: str = "Chunked Terminal Plot", style: str = "matrix", Use_Navigation: bool = False) -> None`**
  - Main function to plot data in chunks based on the rule
  - Routes to appropriate plotting function based on rule type
  - Parameters:
    - `df`: DataFrame with data
    - `rule`: Trading rule (OHLCV, AUTO, PV, SR, PHLD, RSI variants, or indicator name)
    - `title`: Plot title
    - `style`: Plot style
    - `Use_Navigation`: Whether to use interactive navigation

### Exported Functions

All functions from the split modules are re-exported for backward compatibility:
- All plotting functions (`plot_*_chunks`)
- Base functions (`calculate_optimal_chunk_size`, `split_dataframe_into_chunks`, `parse_rsi_rule`, etc.)
- Indicator functions (`_add_wave_indicator_to_subplot`)

## Usage Examples

### Basic Usage

```python
from src.plotting.term_chunked_plot import plot_chunked_terminal
import pandas as pd

# Create sample data
df = pd.DataFrame({
    'Open': [100, 101, 102],
    'High': [105, 106, 107],
    'Low': [99, 100, 101],
    'Close': [104, 105, 106],
})

# Plot OHLCV chunks
plot_chunked_terminal(df, rule="OHLCV")
```

### Using Individual Functions

```python
from src.plotting.term_chunked_plot import plot_ohlcv_chunks, calculate_optimal_chunk_size

# Calculate chunk size
chunk_size = calculate_optimal_chunk_size(len(df))

# Plot directly
plot_ohlcv_chunks(df, title="My OHLCV Plot", style="matrix")
```

### With Navigation

```python
from src.plotting.term_chunked_plot import plot_chunked_terminal

# Plot with interactive navigation
plot_chunked_terminal(df, rule="AUTO", Use_Navigation=True)
```

## Dependencies

All modules depend on:
- `pandas` - Data manipulation
- `plotext` - Terminal plotting
- `numpy` - Numerical operations
- `src.common.logger` - Logging
- `src.common.constants` - Trading constants (BUY, SELL, NOTRADE)
- `src.plotting.term_navigation` - Navigation system

## Error Handling

All plotting functions use try-except blocks to handle errors gracefully:
- Missing columns are handled with warnings
- Invalid data is logged and skipped
- Navigation errors are caught and logged

## Performance Considerations

- Chunk size is automatically calculated for optimal performance
- Large datasets are split into manageable chunks
- Each chunk is processed independently
- Memory usage is optimized by processing chunks sequentially

