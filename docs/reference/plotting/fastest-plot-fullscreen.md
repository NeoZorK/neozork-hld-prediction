# Fastest Plot Fullscreen

## Overview

The `fastest_plot_fullscreen` module provides dynamic fullscreen height functionality specifically optimized for the command:

```bash
uv run run_analysis.py show csv mn1 -d fastest --rule OHLCV
```

This module automatically detects the screen height and calculates an optimal chart height to utilize the full screen space for better visualization of OHLCV data.

## Features

- **Dynamic Height Calculation**: Automatically detects screen resolution and calculates optimal chart height
- **Fullscreen Optimization**: Uses 90% of screen height for OHLCV rule to maximize chart visibility
- **Fallback Support**: Gracefully falls back to standard plotting if fullscreen mode is unavailable
- **Cross-Platform**: Works on Windows, macOS, and Linux systems
- **Performance Optimized**: Uses Dask and Datashader for efficient handling of large datasets

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
- **OHLCV Rule**: Uses 90% of screen height (bounded between 800-2000px)
- **Other Rules**: Uses standard height of 1100px

### `plot_indicator_results_fastest_fullscreen(df, rule, title='', output_path="results/plots/fastest_plot_fullscreen.html", width=1800, height=None, mode="fastest", data_source="demo", **kwargs)`

Creates a fullscreen-optimized chart using Plotly with dynamic height calculation.

**Parameters:**
- `df` (pd.DataFrame): DataFrame with OHLCV data
- `rule` (TradingRule): Trading rule object or string
- `title` (str): Chart title
- `output_path` (str): Output HTML file path
- `width` (int): Chart width in pixels (default: 1800)
- `height` (int, optional): Chart height in pixels (if None, calculated dynamically)
- `mode` (str): Plotting mode (default: "fastest")
- `data_source` (str): Data source identifier
- `**kwargs`: Additional arguments

**Returns:**
- `go.Figure`: Plotly figure object

## Usage Examples

### Basic Usage

```python
from src.plotting.fastest_plot_fullscreen import plot_indicator_results_fastest_fullscreen

# Create chart with dynamic height
fig = plot_indicator_results_fastest_fullscreen(
    df=ohlcv_data,
    rule="OHLCV",
    title="Fullscreen OHLCV Chart"
)
```

### Custom Height

```python
# Use custom height instead of dynamic calculation
fig = plot_indicator_results_fastest_fullscreen(
    df=ohlcv_data,
    rule="OHLCV",
    title="Custom Height Chart",
    height=1500
)
```

### Screen Height Detection

```python
from src.plotting.fastest_plot_fullscreen import get_screen_height, calculate_dynamic_height

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
uv run run_analysis.py show csv mn1 -d fastest --rule OHLCV
```

The system detects this specific combination and:
1. Sets the `display_candlestick_only` flag
2. Calls the fullscreen plotting function
3. Falls back to standard plotting if fullscreen mode fails

## Error Handling

The module includes comprehensive error handling:

- **Import Errors**: Falls back to standard plotting if dependencies are missing
- **Screen Detection Failures**: Uses default height values
- **Invalid Data**: Returns None and logs appropriate error messages
- **File System Errors**: Handles permission and path issues gracefully

## Performance Considerations

- **Memory Usage**: Uses Dask for lazy data processing to minimize memory footprint
- **Rendering**: Leverages Datashader for efficient downsampling of large datasets
- **Browser Performance**: Optimized HTML output for smooth browser rendering

## Browser Compatibility

The generated HTML files are compatible with:
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## File Output

The module generates HTML files with:
- Interactive Plotly charts
- Responsive design
- Hover tooltips
- Zoom and pan capabilities
- Automatic browser opening

## Configuration

### Height Bounds

The dynamic height calculation respects these bounds:
- **Minimum**: 800px
- **Maximum**: 2000px
- **OHLCV Rule**: 90% of screen height (within bounds)

### Output Directory

Default output path: `results/plots/fastest_plot_fullscreen.html`

## Testing

Run the test suite:

```bash
uv run pytest tests/plotting/test_fastest_plot_fullscreen.py -v
```

## Dependencies

- `pandas`: Data manipulation
- `plotly`: Interactive plotting
- `dask`: Lazy data processing
- `datashader`: Large dataset rendering
- `tkinter`: Screen height detection (optional)
- `subprocess`: Platform-specific screen detection

## Troubleshooting

### Screen Height Detection Issues

If screen height detection fails:
1. Check if tkinter is available
2. Verify platform-specific commands (`wmic` on Windows, `xrandr` on Linux)
3. The system will use default height (1080px)

### Import Errors

If the fullscreen module cannot be imported:
1. Check that all dependencies are installed
2. Verify the module path is correct
3. The system will fall back to standard plotting

### Performance Issues

For large datasets:
1. Ensure sufficient RAM is available
2. Consider reducing data size for testing
3. Monitor system resources during plotting

## Related Modules

- `fastest_plot.py`: Standard fastest plotting functionality
- `plotting_generation.py`: Plot generation orchestration
- `cli_show_mode.py`: CLI integration for show mode 