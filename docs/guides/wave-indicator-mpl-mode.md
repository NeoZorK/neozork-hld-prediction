# Wave Indicator with MPL Mode

## Overview

The Wave indicator is now fully supported in MPL (matplotlib) mode using the `-d mpl` option. This provides a high-quality, static visualization of the Wave indicator with dual charts showing both price action and indicator values.

## Usage

### Basic Command

```bash
uv run python -m src.cli.cli csv --csv-file <data_file> --point <points> --rule wave:<parameters> -d mpl
```

### Example

```bash
uv run python -m src.cli.cli csv --csv-file data/test_wave_mpl.csv --point 20 --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open -d mpl
```

## Parameters

The Wave indicator requires exactly 11 parameters in the following format:

```
wave:long1,fast1,trend1,tr1,long2,fast2,trend2,tr2,global_tr,sma_period,price_type
```

### Parameter Details

| Parameter | Description | Default | Range |
|-----------|-------------|---------|-------|
| `long1` | First long period | 339 | > 0 |
| `fast1` | First fast period | 10 | > 0 |
| `trend1` | First trend period | 2 | > 0 |
| `tr1` | First trading rule | fast | See Trading Rules |
| `long2` | Second long period | 22 | > 0 |
| `fast2` | Second fast period | 11 | > 0 |
| `trend2` | Second trend period | 4 | > 0 |
| `tr2` | Second trading rule | fast | See Trading Rules |
| `global_tr` | Global trading rule | prime | See Global Rules |
| `sma_period` | SMA calculation period | 22 | > 0 |
| `price_type` | Price type for calculation | open | open/close |

## Trading Rules (tr1, tr2)

| Rule | Description |
|------|-------------|
| `fast` | Basic momentum comparison |
| `zone` | Simple zone-based signals |
| `strongtrend` | Strong trend confirmation |
| `weaktrend` | Weak trend signals |
| `fastzonereverse` | Reverse signals in zones |
| `bettertrend` | Enhanced trend signals |
| `betterfast` | Improved fast trading |
| `rost` | Reverse momentum signals |
| `trendrost` | Trend-based reverse signals |
| `bettertrendrost` | Enhanced trend reverse signals |

## Global Trading Rules (global_tr)

| Rule | Description |
|------|-------------|
| `prime` | Prime rule - generates signals when both wave indicators agree |
| `reverse` | Reverse rule - reverses signals when both wave indicators agree |
| `primezone` | Prime Zone rule - BUY only in negative zone, SELL only in positive zone |
| `reversezone` | Reverse Zone rule - reverses zone-filtered signals |
| `newzone` | New Zone rule - generates signals when wave indicators disagree |
| `longzone` | Long Zone rule - always generates opposite signal to last signal |
| `longzonereverse` | Long Zone Reverse rule - always uses the last signal |

## MPL Mode Features

### Dual Chart Layout

The MPL mode creates a dual chart layout with:

1. **Main Chart (Top)**: OHLC candlesticks with support/resistance lines
2. **Indicator Chart (Bottom)**: Wave indicator values with multiple components

### Wave Indicator Components

The indicator chart displays:

- **Wave Line**: Main indicator line with dynamic colors
  - Red segments: BUY signals (value = 1)
  - Blue segments: SELL signals (value = 2)
  - No segments: No trade signals (value = 0)
- **Fast Line**: Thin red dotted line showing fast momentum
- **MA Line**: Light blue line showing moving average
- **Zero Line**: Gray dashed reference line

### Visual Features

- **Discontinuous Line Segments**: Wave line is displayed as separate segments for different signal types
- **Color Coding**: Clear visual distinction between BUY and SELL signals
- **Support Lines**: Additional indicator lines for comprehensive analysis
- **Professional Styling**: High-quality matplotlib rendering

## Example Output

When you run the command, the MPL mode will:

1. Calculate the Wave indicator using the specified parameters
2. Create a dual chart visualization
3. Display the chart in a matplotlib window
4. Show both price action and indicator values

## Error Handling

The MPL mode includes comprehensive error handling:

- **Parameter Validation**: Ensures all 11 parameters are provided and valid
- **Data Validation**: Checks for sufficient data points for calculation
- **Rule Validation**: Validates trading rules and global rules
- **Price Type Validation**: Ensures price type is 'open' or 'close'

## Performance

MPL mode provides:

- **Fast Rendering**: Efficient matplotlib-based visualization
- **High Quality**: Professional-grade chart output
- **Memory Efficient**: Optimized for large datasets
- **Cross-Platform**: Works on all operating systems

## Comparison with Other Modes

| Mode | Speed | Quality | Interactivity | File Size |
|------|-------|---------|---------------|-----------|
| `-d fastest` | Fastest | Good | High | Large |
| `-d fast` | Fast | Good | High | Large |
| `-d mpl` | Medium | Excellent | Low | Small |
| `-d plotly` | Medium | Excellent | High | Large |

## Best Practices

1. **Parameter Testing**: Test different parameter combinations to find optimal settings
2. **Data Quality**: Ensure your data has sufficient points for the longest period used
3. **Rule Selection**: Choose trading rules based on your market conditions
4. **Global Rule**: Select global rules that match your trading strategy
5. **Price Type**: Use 'open' for opening price analysis, 'close' for closing price analysis

## Troubleshooting

### Common Issues

1. **"Wave requires exactly 11 parameters"**: Ensure you provide all required parameters
2. **"Invalid tr1 value"**: Check that trading rule names are correct
3. **"Invalid global_tr value"**: Verify global rule names
4. **"Not enough data"**: Increase your data points or reduce period values

### Solutions

- Use the `--help` option to see parameter details
- Check the indicator documentation for valid rule names
- Ensure your CSV file has sufficient data rows
- Verify parameter values are within valid ranges

## Integration

The Wave indicator with MPL mode integrates seamlessly with:

- **Data Sources**: CSV, yfinance, polygon, binance, exrate
- **Export Options**: Parquet, CSV, JSON formats
- **Other Indicators**: Can be combined with other technical indicators
- **Analysis Tools**: Compatible with all analysis workflows
