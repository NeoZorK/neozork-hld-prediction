# ADX Help Integration

## Overview

This document describes the integration of ADX (Average Directional Index) help functionality into the CLI system, following the same pattern as MACD help.

## Implementation Details

### Files Modified

1. **`src/cli/error_handling.py`**
   - Added ADX help data to the `get_indicator_help_data()` function
   - Follows the same structure as MACD help

### ADX Help Data Structure

```python
'adx': {
    'name': 'ADX (Average Directional Index)',
    'description': 'Trend strength indicator that measures the strength of a trend regardless of its direction. Values above 25 indicate a strong trend, values below 20 indicate a weak trend.',
    'format': 'adx:period',
    'parameters': [
        ('period', 'int', 'ADX calculation period', '14')
    ],
    'examples': [
        ('adx:14', 'Standard ADX with 14-period window'),
        ('adx:21', 'Long-term ADX with 21-period window'),
        ('adx:10', 'Short-term ADX with 10-period window')
    ],
    'tips': [
        'Values 0-20: Weak trend (sideways market)',
        'Values 20-25: Developing trend',
        'Values 25-50: Strong trend',
        'Values 50+: Very strong trend',
        'Use with +DI and -DI for trend direction',
        'ADX alone does not indicate trend direction',
        'Higher ADX values suggest trend-following strategies'
    ],
    'common_errors': [
        'Invalid period: Must be a positive integer',
        'Period too short may give unreliable results',
        'ADX requires only one parameter: period'
    ]
}
```

## Usage Examples

### Getting ADX Help

```bash
# Show ADX help (same style as MACD)
uv run run_analysis.py show csv gbp -d mpl --rule adx:
```

### Using ADX with Parameters

```bash
# Standard ADX with 14-period window
uv run run_analysis.py show csv gbp -d mpl --rule adx:14

# Long-term ADX with 21-period window
uv run run_analysis.py show csv gbp -d mpl --rule adx:21

# Short-term ADX with 10-period window
uv run run_analysis.py show csv gbp -d mpl --rule adx:10
```

## Help Output Format

The ADX help follows the same colorful, icon-based format as MACD:

```
❌ ERROR: Help requested for indicator: adx
============================================================

📊 ADX (Average Directional Index) Help:
Trend strength indicator that measures the strength of a trend regardless of its direction. Values above 25 indicate a strong trend, values below 20 indicate a weak trend.

⚙️ Format:
⚙️ adx:period

⚙️ Parameters:

  ⚙️ period (int) [default: 14]
     ADX calculation period

💻 Examples:

  💻 adx:14 # Standard ADX with 14-period window
  💻 adx:21 # Long-term ADX with 21-period window
  💻 adx:10 # Short-term ADX with 10-period window

💡 Tips:

  💡 Values 0-20: Weak trend (sideways market)
  💡 Values 20-25: Developing trend
  💡 Values 25-50: Strong trend
  💡 Values 50+: Very strong trend
  💡 Use with +DI and -DI for trend direction
  💡 ADX alone does not indicate trend direction
  💡 Higher ADX values suggest trend-following strategies

⚠️ Common Errors:

  🔧 Invalid period: Must be a positive integer
  🔧 Period too short may give unreliable results
  🔧 ADX requires only one parameter: period

💻 Command Usage:

  💻 python run_analysis.py show csv mn1 -d fastest --rule adx:14 # Basic usage with first example
  💻 python run_analysis.py show csv mn1 -d fastest --rule adx:21 # Alternative usage with second example
────────────────────────────────────────────────────────────

💡 Need more help?
  💻 python run_analysis.py --indicators # List all indicators
  💻 python run_analysis.py --examples # Show usage examples
  💻 python run_analysis.py --help # Show general help
```

## Testing

### Test File: `tests/cli/test_adx_help.py`

The implementation includes comprehensive tests that verify:

1. **Data Structure**: ADX help data exists and has correct structure
2. **Content Validation**: ADX help data has correct content and values
3. **Case Insensitivity**: ADX help works with different case variations
4. **Consistency**: ADX help has the same structure as MACD help

### Running Tests

```bash
# Run ADX help tests
uv run pytest tests/cli/test_adx_help.py -v

# Run all CLI tests
uv run pytest tests/cli/ -v
```

## Integration Points

### 1. Error Handling System

ADX help integrates with the existing error handling system in `src/cli/error_handling.py`:

- Uses `get_indicator_help_data()` function
- Follows the same data structure as other indicators
- Integrates with `show_enhanced_indicator_help()` function

### 2. CLI Parser

ADX is already supported in the CLI parser in `src/cli/cli.py`:

- Listed in `valid_indicators` array
- Has parameter parsing function `parse_adx_parameters()`
- Included in help information

### 3. Indicator Calculation

ADX indicator calculation is handled by:

- `src/calculation/indicators/trend/adx_ind.py`
- Integrated with the main calculation workflow
- Supports parameterized usage

## Benefits

1. **Consistency**: ADX help follows the same pattern as MACD help
2. **User Experience**: Provides clear, colorful help with icons and examples
3. **Maintainability**: Uses the same infrastructure as other indicators
4. **Testability**: Comprehensive test coverage ensures reliability

## Future Enhancements

1. **Additional Examples**: Could add more specific use cases
2. **Advanced Tips**: Could include more advanced trading strategies
3. **Integration with Other Indicators**: Could show how ADX works with +DI and -DI
4. **Performance Tips**: Could include optimization suggestions

## Related Documentation

- [CLI Interface Guide](../guides/cli-interface.md)
- [Parameterized Indicators Guide](../guides/parameterized-indicators.md)
- [Error Handling System](../reference/error-handling.md)
- [ADX Indicator Reference](../reference/indicators/trend/adx-indicator.md) 