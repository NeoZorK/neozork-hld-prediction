# Terminal Navigation System

Complete guide to the interactive navigation system for terminal plotting mode (`-d term`).

## Overview

The terminal navigation system provides interactive controls for viewing data chunks when using the `-d term` plotting mode. Instead of simply pressing Enter to view the next chunk, users can now navigate freely through the data using keyboard commands.

## Navigation Commands

### Basic Navigation
- **`n`** - Next chunk
- **`p`** - Previous chunk  
- **`s`** - Start (first chunk)
- **`e`** - End (last chunk)

### Advanced Navigation
- **`c`** - Choose chunk by number
- **`d`** - Choose chunk by date (YYYY-MM-DD or YYYY-MM-DD HH:MM)

### System Commands
- **`h`** or **`?`** - Show help
- **`q`** - Quit navigation
- **Enter** - Continue to next chunk (original behavior)

## Usage Examples

### Basic Navigation
```bash
# Start with terminal mode
uv run run_analysis.py show csv gbp -d term

# Navigation prompt will appear:
# [Navigation: type 'n/p/s/e/c/d/h/q' -> next/previous/start/end/choose chunk/choose date/help/quit]
# Current: Chunk 1/5 (2024-01-01 to 2024-01-20)
# Press Enter to continue or type navigation command:
```

### Choose Specific Chunk
```bash
# Type 'c' to choose chunk by number
c
Enter chunk number (1-5): 3
```

### Choose by Date
```bash
# Type 'd' to choose chunk by date
d
Enter date (YYYY-MM-DD or YYYY-MM-DD HH:MM): 2024-01-15
```

### Quick Navigation
```bash
# Jump to start
s

# Jump to end  
e

# Go back one chunk
p

# Go forward one chunk
n
```

## Navigation Features

### Chunk Information Display
The navigation system shows:
- Current chunk number and total chunks
- Date range for current chunk
- Number of rows in current chunk

### Date Selection
Supports multiple date formats:
- `YYYY-MM-DD` (e.g., 2024-01-15)
- `YYYY-MM-DD HH:MM` (e.g., 2024-01-15 14:30)
- `YYYY-MM-DD HH:MM:SS` (e.g., 2024-01-15 14:30:45)

### Error Handling
- Invalid chunk numbers show error message
- Invalid dates show error message
- Unknown commands show warning and help

## Integration with Existing Commands

### Show Mode with Navigation
```bash
# CSV files with navigation
uv run run_analysis.py show csv gbp -d term

# Indicator files with navigation
uv run run_analysis.py show ind parquet -d term

# Auto mode with navigation
uv run run_analysis.py show csv gbp --rule AUTO -d term
```

### All Supported Rules
Navigation works with all trading rules:
- **OHLCV** - Basic candlestick charts
- **AUTO** - All available indicators
- **PV** - Pressure Vector indicators
- **SR** - Support and Resistance
- **PHLD** - Predict High Low Direction
- **RSI** - Relative Strength Index variants

## Technical Implementation

### Navigation System Components
- **TerminalNavigator** - Main navigation controller
- **Chunk Management** - Splits data into optimal chunks
- **Input Processing** - Parses user commands
- **Date Validation** - Validates date inputs

### Integration Points
- **term_chunked_plot.py** - Modified plotting functions
- **plotting_generation.py** - Updated plot generation
- **cli_show_mode.py** - Enhanced show mode handling

### Backward Compatibility
- Original "Press Enter to continue" behavior preserved
- Navigation only enabled for `-d term` mode
- Other plotting modes unchanged

## Error Messages

### Common Error Messages
```
Already at the last chunk
Already at the first chunk
Invalid chunk number. Must be between 1 and 5
Invalid input. Please enter a number.
Invalid date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM
Date 2024-01-15 not found in any chunk
Unknown command 'x'. Type 'h' for help.
```

### Help Display
```
============================================================
TERMINAL NAVIGATION HELP
============================================================
Navigation Commands:
  n - Next chunk
  p - Previous chunk
  s - Start (first chunk)
  e - End (last chunk)
  c - Choose chunk by number
  d - Choose chunk by date (YYYY-MM-DD)
  h/? - Show this help
  q - Quit navigation
  Enter - Continue to next chunk (original behavior)
============================================================
```

## Testing

### Run Navigation Tests
```bash
# Run navigation system tests
uv run pytest tests/plotting/test_term_navigation.py -v

# Run all terminal plotting tests
uv run pytest tests/plotting/ -v
```

### Manual Testing
```bash
# Test with sample data
uv run run_analysis.py show csv gbp -d term

# Test navigation commands:
# n, p, s, e, c, d, h, q
```

## Future Enhancements

### Planned Features
1. **Bookmark System** - Save favorite chunks
2. **Search Functionality** - Find specific patterns
3. **Export Current Chunk** - Save current view
4. **Custom Chunk Size** - User-defined chunk sizes
5. **Keyboard Shortcuts** - Additional navigation keys

### Potential Improvements
- **Mouse Support** - Click navigation
- **Zoom Controls** - In-chunk zooming
- **Filter Options** - Filter data within chunks
- **Annotation System** - Add notes to chunks

## Troubleshooting

### Common Issues

#### Navigation Not Working
```bash
# Check if terminal mode is active
uv run run_analysis.py show csv gbp -d term

# Verify navigation prompt appears
```

#### Date Selection Issues
```bash
# Use correct date format
YYYY-MM-DD
YYYY-MM-DD HH:MM
YYYY-MM-DD HH:MM:SS
```

#### Chunk Selection Issues
```bash
# Check available chunk numbers
# Use 'h' to see help
# Use 'c' then enter valid chunk number
```

### Debug Mode
```bash
# Enable debug logging
export DEBUG_NAVIGATION=1
uv run run_analysis.py show csv gbp -d term
```

## Performance Considerations

### Memory Usage
- Navigation system loads all chunks into memory
- Large datasets may require more memory
- Consider chunk size optimization for very large files

### Response Time
- Navigation commands respond immediately
- Date search may take time for large datasets
- Chunk switching is instant

### Optimization Tips
- Use appropriate chunk sizes for your data
- Consider data filtering before navigation
- Use date selection for large datasets 