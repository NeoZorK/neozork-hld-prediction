# Fast Plot Fullscreen

## Overview

The `fast_plot_fullscreen` module provides dynamic fullscreen height functionality specifically optimized for the command:

```bash
uv run run_analysis.py show csv mn1 -d fast --rule OHLCV
```

This module automatically detects the screen height and calculates an optimal chart height to utilize the full screen space for better visualization of OHLCV data, making it visually identical to the `-d fastest` mode.

## Features

- **Dynamic Height Calculation**: Automatically detects screen resolution and calculates optimal chart height
- **Fullscreen Optimization**: Uses 85% of screen height for OHLCV rule to maximize chart visibility
- **Fallback Support**: Gracefully falls back to standard plotting if fullscreen mode is unavailable
- **Cross-Platform**: Works on Windows, macOS, and Linux systems
- **Bokeh-Based**: Uses Bokeh for interactive web-based visualization
- **Visual Parity**: Provides identical visual experience to `-d fastest` mode

## Functions

### `get_screen_height()`

Detects the screen height in pixels using platform-specific methods.

**Returns:**
- `int`: Screen height in pixels (defaults to 1080 if detection fails)

**Platform Support:**
- **Windows**: Uses `wmic` command
- **Unix/Linux**: Uses `xrandr` command
- **Fallback**: Uses tkinter for cross-platform detection

### `calculate_dynamic_height(screen_height=None, rule_str=None)`

Calculates the optimal chart height based on screen height and trading rule.

**Parameters:**
- `screen_height` (int, optional): Screen height in pixels
- `rule_str` (str, optional): Trading rule string (e.g., 'OHLCV', 'AUTO')

**Returns:**
- `int`: Calculated chart height in pixels

**Height Calculation Logic:**
- **OHLCV Rule**: Uses 85% of screen height (bounded between 400-2000px)
- **Other Rules**: Uses standard height of 1100px

### `plot_indicator_results_fast_fullscreen(df, rule, title='', output_path="results/plots/fast_plot_fullscreen.html", width=1800, height=None, mode="fast", data_source="demo", **kwargs)`

Creates a fullscreen-optimized chart using Bokeh with dynamic height calculation.

**Parameters:**
- `df` (pd.DataFrame): DataFrame with OHLCV data
- `rule` (TradingRule): Trading rule object or string
- `title` (str): Chart title
- `output_path` (str): Output HTML file path
- `width` (int): Chart width in pixels (default: 1800)
- `height` (int, optional): Chart height in pixels (if None, calculated dynamically)
- `mode` (str): Plotting mode (default: "fast")
- `data_source` (str): Data source identifier
- `**kwargs`: Additional arguments

**Returns:**
- `bokeh.layouts.column`: Bokeh layout object

## Usage Examples

### Basic Usage

```python
from src.plotting.fast_plot_fullscreen import plot_indicator_results_fast_fullscreen

# Create chart with dynamic height
layout = plot_indicator_results_fast_fullscreen(
    df=ohlcv_data,
    rule="OHLCV",
    title="Fullscreen OHLCV Chart"
)
```

### Custom Height

```python
# Use custom height instead of dynamic calculation
layout = plot_indicator_results_fast_fullscreen(
    df=ohlcv_data,
    rule="OHLCV",
    title="Custom Height Chart",
    height=1500
)
```

### Screen Height Detection

```python
from src.plotting.fast_plot_fullscreen import get_screen_height, calculate_dynamic_height

# Get screen height
screen_height = get_screen_height()
print(f"Screen height: {screen_height}px")

# Calculate optimal chart height for OHLCV
chart_height = calculate_dynamic_height(screen_height=screen_height, rule_str="OHLCV")
print(f"Optimal chart height: {chart_height}px")
```

## Integration with CLI

The fullscreen functionality is automatically triggered when using:

```bash
uv run run_analysis.py show csv mn1 -d fast --rule OHLCV
```

The system detects this specific combination and:
1. Sets the `display_candlestick_only` flag
2. Calls the fullscreen plotting function
3. Falls back to standard plotting if fullscreen mode fails

## Comparison with Fastest Mode

Both `-d fast` and `-d fastest` modes now provide identical fullscreen functionality:

| Feature | `-d fast` | `-d fastest` |
|---------|-----------|--------------|
| **Backend** | Bokeh | Plotly + Dask + Datashader |
| **Dynamic Height** | ✅ Yes | ✅ Yes |
| **Fullscreen Support** | ✅ Yes | ✅ Yes |
| **OHLCV Rule** | ✅ Fullscreen | ✅ Fullscreen |
| **Other Rules** | Standard height | Standard height |
| **Performance** | Fast | Fastest |
| **Visual Experience** | Identical | Identical |

## Error Handling

The module includes comprehensive error handling:

1. **Screen Height Detection**: Falls back to default 1080px if detection fails
2. **Import Errors**: Gracefully falls back to standard fast plotting
3. **Missing Columns**: Returns None for invalid data
4. **File System Errors**: Handles directory creation and file saving errors

## Testing

Run the test suite to verify functionality:

```bash
uv run pytest tests/plotting/test_fast_plot_fullscreen.py -v
```

## Related Modules

- `fastest_plot_fullscreen.py`: Plotly-based fullscreen functionality
- `fast_plot.py`: Standard fast plotting functionality
- `plotting_generation.py`: Plot generation orchestration
- `cli_show_mode.py`: CLI integration for show mode

## Performance Considerations

- **Memory Usage**: Bokeh-based plotting is memory efficient
- **Rendering Speed**: Optimized for interactive web-based visualization
- **Large Datasets**: Handles datasets with thousands of data points efficiently
- **Browser Compatibility**: Works in all modern web browsers

## Troubleshooting

### Common Issues

1. **Screen Height Not Detected**: Check if tkinter is available or use platform-specific commands
2. **Import Errors**: Ensure all required dependencies are installed
3. **File Permission Errors**: Check write permissions for the results directory
4. **Browser Not Opening**: Verify default browser is set correctly

### Debug Mode

Enable debug logging to see detailed information:

```python
import logging
logging.getLogger('src.plotting.fast_plot_fullscreen').setLevel(logging.DEBUG)
```

## Future Enhancements

- **Custom Height Calculation**: Allow user-defined height calculation formulas
- **Multiple Monitor Support**: Detect and use primary monitor dimensions
- **Responsive Design**: Adapt to browser window resizing
- **Theme Support**: Customizable chart themes and colors 