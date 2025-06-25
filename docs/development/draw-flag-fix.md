# Draw Flag Fix Documentation

## Problem Description

The CLI was experiencing an error when using the `-d` flag for plotting:
```
Error calculating indicator: 'Namespace' object has no attribute 'draw'
```

This error occurred because the argument parser was defining the `-d` flag without specifying a `dest` attribute, which meant the value was stored as `args.d` instead of `args.draw`. However, the code throughout the application was expecting `args.draw`.

## Root Cause

In `src/cli/cli.py`, the argument definition was:
```python
plotting_group.add_argument(
    '-d',
    choices=['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term'],
    default='fastest',
    help="Plot method: fastest, fast, plotly, mplfinance, seaborn, term"
)
```

This meant that when users used `-d fastest`, the value was stored as `args.d = 'fastest'`, but the code was trying to access `args.draw`.

## Solution

The argument definition was updated to include both short and long forms with proper destination:

```python
plotting_group.add_argument(
    '-d', '--draw',
    dest='draw',
    choices=['fastest', 'fast', 'plotly', 'plt', 'mplfinance', 'mpl', 'seaborn', 'sb', 'term'],
    default='fastest',
    help="Plot method: fastest, fast, plotly, mplfinance, seaborn, term"
)
```

## Changes Made

1. **Added long form flag**: `--draw` alongside `-d`
2. **Added dest parameter**: `dest='draw'` to ensure the value is stored as `args.draw`
3. **Maintained backward compatibility**: Both `-d` and `--draw` work identically

## Testing

### Manual Testing
- ✅ `python run_analysis.py demo -d fastest` - works correctly
- ✅ `python run_analysis.py demo --draw fastest` - works correctly  
- ✅ `python run_analysis.py demo -d term` - works correctly
- ✅ `python run_analysis.py demo -d mpl` - works correctly

### Automated Testing
Created comprehensive test suite in `tests/cli/test_draw_flag_fix.py` that covers:
- Short form flag (`-d`)
- Long form flag (`--draw`)
- Default value
- All valid draw modes
- Invalid draw modes (error handling)
- Combination with other arguments
- Show mode compatibility

All tests pass successfully.

## Affected Files

### Modified Files
- `src/cli/cli.py` - Fixed argument definition

### New Files
- `tests/cli/test_draw_flag_fix.py` - Comprehensive test suite

### Files That Use args.draw (Now Working)
- `src/plotting/plotting_generation.py`
- `src/cli/cli_show_mode.py`

## Impact

This fix resolves the error across all plotting types:
- fastest
- fast  
- mpl (matplotlib)
- sb (seaborn)
- plt (plotly)
- term (terminal)

## Backward Compatibility

The fix maintains full backward compatibility:
- Existing `-d` flag continues to work
- New `--draw` flag provides explicit long form
- All existing code using `args.draw` now works correctly

## Verification

To verify the fix works:
```bash
# Test short form
python run_analysis.py demo -d fastest

# Test long form  
python run_analysis.py demo --draw fastest

# Run automated tests
python -m pytest tests/cli/test_draw_flag_fix.py -v
```

All commands should execute successfully without the "Namespace object has no attribute 'draw'" error. 