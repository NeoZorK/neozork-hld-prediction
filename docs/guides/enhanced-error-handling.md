# Enhanced CLI Error Handling

## Overview

The enhanced CLI error handling system provides beautiful, colorful help with icons for all indicators when errors occur. This system automatically detects the type of error and provides comprehensive help information to guide users to the correct usage.

## Features

### 🎨 Visual Enhancements
- **Colorful output** with different colors for different types of information
- **Icons** for better visual identification of help sections
- **Structured layout** with clear sections and separators
- **Professional appearance** that makes errors less frustrating

### 📊 Comprehensive Help
- **Indicator descriptions** explaining what each indicator does
- **Parameter details** with types, descriptions, and default values
- **Usage examples** showing correct command formats
- **Tips and best practices** for optimal usage
- **Common errors** and how to fix them
- **Command usage examples** with real commands

### 🔍 Smart Error Detection
- **Automatic indicator detection** from error messages
- **Parameter validation** with specific error messages
- **Fallback help** for unknown indicators
- **Context-aware suggestions** based on the error type

## How It Works

### Error Flow
1. **Error occurs** during indicator calculation or parameter parsing
2. **Error message analyzed** to extract indicator name and error type
3. **Help data retrieved** for the specific indicator
4. **Enhanced help displayed** with colors, icons, and comprehensive information
5. **Additional resources** provided for further assistance

### Error Types Handled
- **Invalid price_type**: Wrong price type (e.g., "clo" instead of "close")
- **Wrong parameter count**: Too few or too many parameters
- **Invalid parameter values**: Out of range or wrong type
- **Unknown indicators**: Non-existent indicator names
- **General errors**: Any other calculation or parsing errors

## Examples

### COT Indicator Error
```bash
uv run python run_analysis.py show csv mn1 -d fastest --rule cot:20,clo
```

**Output:**
```
❌ ERROR: COT price_type must be 'open' or 'close', got: clo
============================================================

📊 COT (Commitment of Traders) Help:
Analyzes futures market positioning to gauge institutional sentiment.

⚙️ Format:
⚙️ cot:period,price_type

⚙️ Parameters:
  ⚙️ period (int) [default: 20]
     COT calculation period
  ⚙️ price_type (string) [default: close]
     Price type for calculation

💻 Examples:
  💻 cot:20,close # Standard COT with close prices
  💻 cot:14,open # Short-term COT with open prices
  💻 cot:30,close # Long-term COT with close prices

💡 Tips:
  💡 Standard period: 20 for balanced analysis
  💡 Short-term: 14 for quick sentiment changes
  💡 Long-term: 30 for major sentiment trends

⚠️ Common Errors:
  🔧 Invalid price_type: Use "open" or "close" only
  🔧 Invalid period: Must be a positive integer

💻 Command Usage:
  💻 python run_analysis.py show csv mn1 -d fastest --rule cot:20,close
  💻 python run_analysis.py show csv mn1 -d fastest --rule cot:14,open

────────────────────────────────────────────────────────────

💡 Need more help?
  💻 python run_analysis.py --indicators # List all indicators
  💻 python run_analysis.py --examples # Show usage examples
  💻 python run_analysis.py --help # Show general help
```

### RSI Indicator Error
```bash
uv run python run_analysis.py show csv mn1 -d fastest --rule rsi:14,30,70,invalid
```

**Output:**
```
❌ ERROR: RSI price_type must be 'open' or 'close', got: invalid
============================================================

📊 RSI (Relative Strength Index) Help:
Measures the speed and magnitude of price changes to identify overbought/oversold conditions.

⚙️ Format:
⚙️ rsi:period,oversold,overbought,price_type

⚙️ Parameters:
  ⚙️ period (int) [default: 14]
     RSI calculation period
  ⚙️ oversold (float) [default: 30]
     Oversold threshold (0-100)
  ⚙️ overbought (float) [default: 70]
     Overbought threshold (0-100)
  ⚙️ price_type (string) [default: close]
     Price type for calculation

💻 Examples:
  💻 rsi:14,30,70,open # Standard RSI with open prices
  💻 rsi:21,25,75,close # Custom RSI with close prices
  💻 rsi:14,10,90,open # Wide range RSI with open prices

💡 Tips:
  💡 Use period 14 for standard analysis
  💡 Oversold/overbought levels can be adjusted based on market conditions
  💡 Open prices are more volatile, close prices are more stable

⚠️ Common Errors:
  🔧 Invalid price_type: Use "open" or "close" only
  🔧 Invalid period: Must be a positive integer
  🔧 Invalid thresholds: Must be between 0 and 100

💻 Command Usage:
  💻 python run_analysis.py show csv mn1 -d fastest --rule rsi:14,30,70,open
  💻 python run_analysis.py show csv mn1 -d fastest --rule rsi:21,25,75,close

────────────────────────────────────────────────────────────

💡 Need more help?
  💻 python run_analysis.py --indicators # List all indicators
  💻 python run_analysis.py --examples # Show usage examples
  💻 python run_analysis.py --help # Show general help
```

## Supported Indicators

The enhanced error handling system provides help for all major indicators:

### Trend Indicators
- **EMA** (Exponential Moving Average)
- **HMA** (Hull Moving Average)
- **TSF** (Time Series Forecast)
- **Supertrend**

### Oscillators
- **RSI** (Relative Strength Index)
- **RSI Momentum**
- **RSI Divergence**
- **Stochastic**
- **CCI** (Commodity Channel Index)

### Momentum Indicators
- **MACD** (Moving Average Convergence Divergence)

### Volatility Indicators
- **Bollinger Bands**
- **ATR** (Average True Range)

### Support/Resistance
- **Pivot Points**
- **VWAP** (Volume Weighted Average Price)
- **Donchian Channels**
- **Fibonacci Retracements**

### Sentiment Indicators
- **COT** (Commitment of Traders)
- **Fear & Greed Index**
- **Put/Call Ratio**

### Volume Indicators
- **OBV** (On-Balance Volume)

### Statistical Indicators
- **Standard Deviation**
- **ADX** (Average Directional Index)
- **SAR** (Parabolic SAR)

### Advanced Indicators
- **Monte Carlo Simulation**
- **Kelly Criterion**

## Technical Implementation

### Files
- **`src/cli/error_handling.py`**: Main error handling module
- **`tests/cli/test_error_handling.py`**: Comprehensive test suite

### Key Components

#### CLIErrorHandler Class
- **Icons**: Unicode icons for different message types
- **Colors**: Colorama color schemes for visual appeal
- **Print methods**: Specialized methods for different content types

#### Error Extraction
- **Pattern matching**: Regex patterns to extract indicator names
- **Case insensitive**: Works with any case combination
- **Fallback handling**: Graceful handling of unknown patterns

#### Help Data System
- **Structured data**: Comprehensive help information for each indicator
- **Parameter validation**: Detailed parameter descriptions and constraints
- **Usage examples**: Real-world command examples
- **Tips and best practices**: Expert advice for optimal usage

### Integration Points
- **CLI show mode**: Integrated into `src/cli/cli_show_mode.py`
- **Parameter parsing**: Integrated into `src/cli/cli.py`
- **Error handling**: Automatic activation on any indicator error

## Benefits

### For Users
- **Immediate help**: No need to search documentation
- **Clear guidance**: Step-by-step instructions
- **Visual appeal**: Less frustrating error experience
- **Learning opportunity**: Educational content in error messages

### For Developers
- **Consistent experience**: Standardized error handling
- **Maintainable code**: Centralized help system
- **Extensible**: Easy to add new indicators
- **Well tested**: Comprehensive test coverage

## Best Practices

### Using the System
1. **Read the error message** carefully to understand the issue
2. **Check the parameters** section for correct format
3. **Use the examples** as templates for your commands
4. **Follow the tips** for optimal results
5. **Use additional help** if needed

### Adding New Indicators
1. **Add help data** to the `get_indicator_help_data()` function
2. **Include all required fields**: name, description, format, parameters, examples, tips, common_errors
3. **Test the help system** with various error scenarios
4. **Update tests** to cover new indicator help

### Error Message Patterns
- **Be specific**: Include the actual value that caused the error
- **Be helpful**: Suggest the correct format
- **Be consistent**: Use the same patterns across all indicators
- **Be educational**: Explain why the error occurred

## Future Enhancements

### Planned Features
- **Interactive help**: Step-by-step parameter input
- **Video tutorials**: Embedded help videos
- **Context-aware suggestions**: Based on user history
- **Multi-language support**: Localized error messages
- **Advanced examples**: More complex usage scenarios

### Integration Opportunities
- **IDE plugins**: Integration with development environments
- **Web interface**: Online help system
- **API documentation**: Automatic API documentation generation
- **Learning system**: Adaptive help based on user skill level

## Conclusion

The enhanced CLI error handling system transforms frustrating error messages into educational opportunities. By providing comprehensive, visually appealing help with every error, users can quickly understand and fix issues while learning about the indicators they're using.

This system demonstrates how good error handling can improve user experience and reduce support burden, making the trading analysis tool more accessible and user-friendly. 