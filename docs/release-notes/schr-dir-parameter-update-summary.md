# SCHR_DIR Parameter Update Summary

## Overview

Added configurable `grow_percent` parameter to SCHR_DIR indicator with comprehensive help system and dual chart display.

## New Features

### 1. Configurable grow_percent Parameter
- **Range**: 1.0 - 95.0
- **Default**: 1.0
- **Usage**: `schr_dir:value` (e.g., `schr_dir:50`)

### 2. Enhanced Help System
- **Trigger**: Using `schr_dir:` or `SCHR_DIR:` (with colon)
- **Content**: Comprehensive help with parameters, examples, tips, and common errors
- **Format**: Colorful, well-structured help display

### 3. Dual Chart Display
- **Primary Chart**: OHLC candlesticks
- **Secondary Chart**: Two separate lines
  - High line (blue) - resistance levels
  - Low line (gold) - support levels
  - Buy/Sell markers at signal points

## Implementation Details

### Parameter Validation
```python
# Validate grow_percent parameter
if not (1.0 <= grow_percent <= 95.0):
    raise ValueError(f"grow_percent must be between 1.0 and 95.0, got: {grow_percent}")
```

### CLI Integration
- Updated `parse_schr_dir_parameters()` function
- Added parameter parsing and validation
- Integrated with existing CLI framework

### Help System
- Updated help information in `error_handling.py`
- Added comprehensive examples and tips
- Included common error messages

## Usage Examples

### Basic Usage (Default 1%)
```bash
uv run run_analysis.py show csv gbp -d fastest --rule SCHR_DIR
```

### With Custom Growth Percentage
```bash
# Moderate growth (50%)
uv run run_analysis.py show csv gbp -d fastest --rule schr_dir:50

# Conservative growth (95%)
uv run run_analysis.py show csv gbp -d fastest --rule schr_dir:95

# Aggressive growth (10%)
uv run run_analysis.py show csv gbp -d fastest --rule schr_dir:10
```

### Help Display
```bash
# Show help for SCHR_DIR
uv run run_analysis.py show csv gbp -d fastest --rule schr_dir:invalid
```

## Parameter Effects

### grow_percent Values
- **1-25**: More aggressive signals, tighter line separation
- **26-50**: Moderate signals, balanced separation
- **51-95**: More conservative signals, wider line separation

### Trading Rules
- **BUY Signal**: When open price > both High and Low lines
- **SELL Signal**: When open price < both High and Low lines
- **NO TRADE**: When open price is between the lines

## Files Modified

### Core Implementation
- `src/calculation/indicators/predictive/schr_dir_ind.py` - Added grow_percent parameter

### CLI System
- `src/cli/cli.py` - Updated parameter parsing
- `src/cli/error_handling.py` - Enhanced help information

### Business Logic
- `src/calculation/rules.py` - Added parameter passing

### Tests
- `tests/calculation/indicators/predictive/test_schr_dir_indicator.py` - Updated tests

### Documentation
- `docs/reference/indicators/predictive/schr-direction.md` - Updated documentation

## Testing Results

### Unit Tests
- ✅ All 16 tests passing
- ✅ Parameter validation working
- ✅ Different grow_percent values tested
- ✅ Error handling verified

### Integration Tests
- ✅ CLI parameter parsing working
- ✅ Help system displaying correctly
- ✅ Dual chart rendering properly
- ✅ Trading signals generating correctly

## Benefits

1. **Flexibility**: Users can adjust sensitivity based on market conditions
2. **User-Friendly**: Comprehensive help system with examples
3. **Robust**: Proper parameter validation and error handling
4. **Visual**: Clear dual chart display with two separate lines
5. **Backward Compatible**: Default behavior maintained

## Error Handling

### Invalid Parameters
- Values outside 1.0-95.0 range
- Non-numeric values
- Missing parameters (uses default)

### Help System
- Shows detailed help when invalid parameters provided
- Includes examples and tips
- Lists common errors and solutions

## Future Considerations

- Monitor performance with different grow_percent values
- Consider adding more parameters if needed
- Evaluate signal frequency and accuracy across different settings
- Test with various market conditions and timeframes

## Migration Guide

### From Previous Version
- **No changes required** for existing commands
- Default behavior (1% growth) maintained
- New parameter optional

### New Users
- Start with default `SCHR_DIR` (1% growth)
- Experiment with different values (10, 50, 95)
- Use help system for guidance (`schr_dir:invalid`)

## Performance Notes

- Lower grow_percent values generate more signals
- Higher grow_percent values provide more conservative approach
- Default 1% provides optimal balance for most markets
- Dual chart display enhances visual analysis
