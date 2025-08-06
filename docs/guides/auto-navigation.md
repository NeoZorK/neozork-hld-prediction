# AUTO Mode Navigation with Field Switching

Complete guide to the enhanced navigation system for AUTO mode in terminal plotting (`-d term`).

## Overview

The AUTO mode navigation system provides **extended interactive navigation** that allows switching between different field arrays (pressure_high, pressure_low, pressure_vector, predicted_high, predicted_low, etc.) in addition to standard chunk navigation.

## Enhanced Navigation Features

### Field Array Switching

AUTO mode now supports switching between different field arrays:

1. **OHLC Group** - Price and Volume Data
2. **Pressure Group** - Pressure Indicators (pressure_high, pressure_low, pressure_vector)
3. **Predicted Group** - Predicted Values (predicted_high, predicted_low)
4. **Other Group** - Additional Indicators (HL, Pressure, PV, etc.)

### Navigation Commands

#### Chunk Navigation (Standard)
- **`n`** - Next chunk
- **`p`** - Previous chunk  
- **`s`** - Start (first chunk)
- **`e`** - End (last chunk)
- **`c`** - Choose chunk by number
- **`d`** - Choose chunk by date (YYYY-MM-DD or YYYY-MM-DD HH:MM)

#### Field Navigation (New)
- **`f`** - Next field within current group
- **`b`** - Previous field within current group
- **`g`** - Next field group
- **`h`** - Previous field group

#### System Commands
- **`?`** - Show help
- **`q`** - Quit navigation
- **Enter** - Continue to next chunk (original behavior)

## Usage Examples

### Basic AUTO Navigation

```bash
# Start AUTO mode with enhanced navigation
uv run run_analysis.py show csv gbp -d term --rule AUTO
```

**Navigation Prompt**:
```
[AUTO Navigation: n/p/s/e/c/d for chunks, f/b/g/h for fields, ? for help, q to quit]
Chunk: 1/4 (2024-01-01 to 2024-01-20)
Field: Pressure - Pressure Indicators
Current: pressure_high (1/3)
Press Enter to continue or type navigation command:
```

### Field Navigation Examples

```bash
# Navigate to next field
f

# Navigate to previous field
b

# Switch to next field group
g

# Switch to previous field group
h
```

### Complete Navigation Flow

1. **Start with OHLC Group** - View candlestick charts
2. **Switch to Pressure Group** - Navigate through pressure_high, pressure_low, pressure_vector
3. **Switch to Predicted Group** - Navigate through predicted_high, predicted_low
4. **Switch to Other Group** - Navigate through additional indicators

## Field Groups

### OHLC Group
- **Description**: Price and Volume Data
- **Fields**: Open, High, Low, Close, Volume
- **Display**: Candlestick charts

### Pressure Group
- **Description**: Pressure Indicators
- **Fields**: pressure_high, pressure_low, pressure_vector
- **Display**: Individual field plots

### Predicted Group
- **Description**: Predicted Values
- **Fields**: predicted_high, predicted_low
- **Display**: Individual field plots

### Other Group
- **Description**: Additional Indicators
- **Fields**: HL, Pressure, PV, and other indicators
- **Display**: Individual field plots

## Navigation Flow

### Chunk Navigation
```
Chunk 1/4 → Chunk 2/4 → Chunk 3/4 → Chunk 4/4
```

### Field Navigation within Group
```
pressure_high → pressure_low → pressure_vector
```

### Group Navigation
```
OHLC Group → Pressure Group → Predicted Group → Other Group
```

### Combined Navigation
```
Chunk 1, OHLC → Chunk 1, Pressure → Chunk 1, Predicted → Chunk 2, OHLC → ...
```

## Technical Implementation

### AutoTerminalNavigator Class

The enhanced navigation is implemented in the `AutoTerminalNavigator` class:

```python
class AutoTerminalNavigator(TerminalNavigator):
    """
    Extended terminal navigator for AUTO mode with field array switching.
    Supports switching between different field arrays.
    """
    
    def __init__(self, chunks, title, field_columns):
        # Initialize field navigation state
        self.current_field_index = 0
        self.field_columns = field_columns
        self.field_groups = self._organize_field_groups()
        self.current_group_index = 0
```

### Field Group Organization

Fields are automatically organized into logical groups:

```python
def _organize_field_groups(self):
    groups = []
    
    # Group 1: OHLC
    ohlc_fields = [col for col in self.field_columns 
                   if col.lower() in ['open', 'high', 'low', 'close', 'volume']]
    
    # Group 2: Pressure indicators
    pressure_fields = [col for col in self.field_columns 
                      if 'pressure' in col.lower()]
    
    # Group 3: Predicted values
    predicted_fields = [col for col in self.field_columns 
                       if 'predicted' in col.lower()]
    
    # Group 4: Other indicators
    other_fields = [col for col in self.field_columns 
                   if col not in ohlc_fields and 
                   col not in pressure_fields and 
                   col not in predicted_fields]
    
    return groups
```

## Integration with Existing Commands

### Show Mode Integration

The enhanced navigation is automatically enabled for AUTO mode:

```bash
# CSV files with AUTO navigation
uv run run_analysis.py show csv gbp -d term --rule AUTO

# Parquet files with AUTO navigation
uv run run_analysis.py show ind parquet -d term --rule AUTO
```

### Backward Compatibility

- Original navigation commands still work
- Non-AUTO rules use standard navigation
- AUTO mode automatically uses enhanced navigation

## Error Handling

### Boundary Conditions
- **First field**: `b` command shows warning
- **Last field**: `f` command moves to next group
- **First group**: `h` command shows warning
- **Last group**: `g` command shows warning

### Invalid Commands
- Unknown commands show warning and continue navigation
- Invalid chunk numbers show error and continue
- Invalid dates show error and continue

## Testing

### Run AUTO Navigation Tests
```bash
# Run AUTO navigation tests
uv run pytest tests/plotting/test_auto_navigation.py -v

# Run all navigation tests
uv run pytest tests/plotting/ -v
```

### Manual Testing
```bash
# Test with sample data
uv run run_analysis.py show csv gbp -d term --rule AUTO

# Test navigation commands:
# n, p, s, e, c, d (chunk navigation)
# f, b, g, h (field navigation)
# ?, q (system commands)
```

## Troubleshooting

### Common Issues

#### Navigation Not Working
```bash
# Check if AUTO mode is active
uv run run_analysis.py show csv gbp -d term --rule AUTO

# Verify enhanced navigation prompt appears
```

#### Field Groups Not Showing
```bash
# Check available fields in data
# Ensure data contains pressure_high, pressure_low, etc.
```

#### Navigation Commands Not Responding
```bash
# Use '?' to see available commands
# Check if you're in the correct mode
```

### Debug Mode
```bash
# Enable debug logging
export DEBUG_NAVIGATION=1
uv run run_analysis.py show csv gbp -d term --rule AUTO
```

## Performance Considerations

### Memory Usage
- Field groups are organized once at initialization
- Navigation state is maintained efficiently
- Large datasets may require more memory for field organization

### Response Time
- Field switching is instant
- Group switching is instant
- Chunk navigation performance unchanged

## Future Enhancements

### Planned Features
1. **Field Bookmarks** - Save favorite fields
2. **Custom Field Groups** - User-defined field organization
3. **Field Search** - Find specific fields by name
4. **Field Comparison** - Compare multiple fields side-by-side

### Potential Improvements
- **Field Filtering** - Filter fields by type
- **Field Statistics** - Show field statistics during navigation
- **Field Export** - Export current field data
- **Field Annotations** - Add notes to specific fields

## Migration from Standard Navigation

### For Existing Users
- All existing navigation commands work unchanged
- New field navigation commands are optional
- Enhanced navigation is automatically enabled for AUTO mode

### For New Users
- Start with standard chunk navigation (`n`, `p`, `s`, `e`)
- Learn field navigation (`f`, `b`, `g`, `h`)
- Use help command (`?`) for guidance

## Summary

The enhanced AUTO mode navigation provides:

✅ **Extended Navigation** - Switch between field arrays  
✅ **Logical Grouping** - Fields organized by type  
✅ **Backward Compatibility** - Existing commands still work  
✅ **Intuitive Interface** - Clear navigation prompts  
✅ **Comprehensive Testing** - Full test coverage  
✅ **Error Handling** - Graceful error management  

This enhancement specifically addresses the user requirement to switch between different field arrays (pressure_high, pressure_low, pressure_vector, predicted_high, predicted_low, etc.) in AUTO mode navigation. 