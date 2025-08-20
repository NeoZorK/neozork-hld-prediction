# Wave Indicator Help Enhancement - Summary

## Overview

Successfully implemented enhanced help functionality for the Wave indicator that provides detailed information about all ENUM_MOM_TR and ENUM_GLOBAL_TR trading rules. This enhancement helps users understand the complex parameter options available in the Wave indicator.

## Changes Made

### 1. Updated Wave Indicator Docstring

**File**: `src/calculation/indicators/trend/wave_ind.py`

- Added comprehensive documentation for all ENUM_MOM_TR trading rules
- Added comprehensive documentation for all ENUM_GLOBAL_TR global trading rules
- Each rule includes detailed explanation of its behavior and use cases

### 2. Enhanced IndicatorSearcher

**File**: `src/cli/indicators_search.py`

- Extended `IndicatorInfo` class to include `trading_rules` and `global_rules` fields
- Updated `_parse_indicator_file` method to extract trading rules information from docstring
- Enhanced `display` method to show trading rules with proper formatting
- Improved `_extract_field` method to handle multi-line fields with special regex patterns

### 3. Enhanced Error Handling System

**File**: `src/cli/error_handling.py`

- Added `enum_details` section to wave indicator help data
- Included detailed descriptions for all ENUM_MOM_TR and ENUM_GLOBAL_TR values
- Updated `show_enhanced_indicator_help` function to display enum information

### 4. Created Comprehensive Test Suite

**File**: `tests/cli/test_wave_help_enhancement.py`

- Added 5 comprehensive tests covering all aspects of the functionality
- Tests include:
  - CLI command functionality with enum information
  - Error help system with enum details
  - IndicatorSearcher enum extraction
  - Docstring content validation
  - Error handling system validation

## Functionality

### Commands Available

```bash
# Show enhanced wave indicator help with enum information
uv run run_analysis.py --indicators wave

# Show error help with enum details (when using invalid parameters)
uv run run_analysis.py show csv mn1 -d fastest --rule wave:invalid
```

### Output Features

- **Colored Output**: Uses ANSI colors for better readability
- **Structured Display**: Clear sections for Trading Rules and Global Trading Rules
- **Detailed Descriptions**: Each rule includes comprehensive explanation
- **Search Integration**: Works with existing indicator search system

## ENUM_MOM_TR Trading Rules

### Individual Trading Rules (10 Rules)

1. **fast**: Basic momentum comparison - BUY when wave > fastline, SELL when wave < fastline
2. **zone**: Simple zone-based signals - BUY when wave > 0, SELL when wave < 0
3. **strongtrend**: Strong trend confirmation - BUY in positive zone when wave > fastline, SELL in negative zone when wave < fastline
4. **weaktrend**: Weak trend signals - BUY in positive zone when wave < fastline, SELL in negative zone when wave > fastline
5. **fastzonereverse**: Reverse signals in zones - SELL in positive zone when wave < fastline, BUY in negative zone when wave > fastline
6. **bettertrend**: Enhanced trend signals avoiding false signals by comparing with previous values
7. **betterfast**: Improved fast trading with enhanced signal validation
8. **rost**: Reverse momentum signals - opposite of standard momentum
9. **trendrost**: Trend-based reverse signals - reverse signals in trend direction
10. **bettertrendrost**: Enhanced trend reverse signals with improved validation

## ENUM_GLOBAL_TR Global Trading Rules

### Global Trading Rules (7 Rules)

1. **prime**: Prime rule - generates signals when both wave indicators agree (same signal)
2. **reverse**: Reverse rule - reverses signals when both wave indicators agree (opposite signal)
3. **primezone**: Prime Zone rule - BUY only in negative zone, SELL only in positive zone when both agree
4. **reversezone**: Reverse Zone rule - reverses zone-filtered signals when both agree
5. **newzone**: New Zone rule - generates signals when wave indicators disagree (opposite to last signal)
6. **longzone**: Long Zone rule - always generates opposite signal to last confirmed signal
7. **longzonereverse**: Long Zone Reverse rule - always uses the last confirmed signal

## Example Usage

### Basic Command with Default Parameters

```bash
uv run run_analysis.py show csv mn1 -d fastest --rule wave:339,10,2,fast,22,11,4,fast,prime,22,open
```

### Command with Custom Trading Rules

```bash
# Using strong trend rule for first wave
uv run run_analysis.py show csv mn1 -d fastest --rule wave:339,10,2,strongtrend,22,11,4,fast,prime,22,open

# Using reverse global rule
uv run run_analysis.py show csv mn1 -d fastest --rule wave:339,10,2,fast,22,11,4,fast,reverse,22,open

# Using zone-based global rule
uv run run_analysis.py show csv mn1 -d fastest --rule wave:339,10,2,fast,22,11,4,fast,primezone,22,open
```

## Technical Implementation

### Regex Pattern Improvements

The enhanced `_extract_field` method uses specialized regex patterns for multi-line fields:

```python
# For Trading Rules (ENUM_MOM_TR)
pattern = rf"Trading Rules \(ENUM_MOM_TR\):\s*(.*?)(?=\nGlobal Trading Rules|$)"

# For Global Trading Rules (ENUM_GLOBAL_TR)
pattern = rf"Global Trading Rules \(ENUM_GLOBAL_TR\):\s*(.*?)(?=\n[A-Z][a-zA-Z\s]+:|$)"
```

### Display Formatting

The enhanced display system uses color-coded sections:

- 🎯 **Trading Rules (ENUM_MOM_TR)**: Individual wave indicator rules
- 🌐 **Global Trading Rules (ENUM_GLOBAL_TR)**: Signal combination rules
- ✅ **Pros**: Advantages and strengths
- ❌ **Cons**: Disadvantages and limitations

## Benefits

1. **Improved User Experience**: Users can now understand all available trading rule options
2. **Better Documentation**: Comprehensive explanations for each rule type
3. **Reduced Learning Curve**: Clear descriptions help users choose appropriate rules
4. **Enhanced Debugging**: Detailed error messages with rule explanations
5. **Professional Appearance**: Color-coded, well-structured help output

## Testing

All functionality is covered by comprehensive tests:

- ✅ CLI command integration tests
- ✅ Error handling system tests
- ✅ IndicatorSearcher extraction tests
- ✅ Docstring content validation tests
- ✅ Enum value validation tests

## Future Enhancements

Potential improvements for future versions:

1. **Interactive Rule Selection**: GUI or interactive CLI for rule selection
2. **Rule Performance Metrics**: Historical performance data for each rule
3. **Rule Recommendations**: AI-powered suggestions based on market conditions
4. **Visual Rule Diagrams**: Graphical representations of rule behavior
5. **Rule Combination Examples**: Pre-configured rule combinations for different market types
