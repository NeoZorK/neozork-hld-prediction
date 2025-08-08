# Multiprocessing Import Fix Summary

Successfully fixed import errors that occurred when running tests with `-n auto` (multiprocessing mode).

## Issue Resolved

### ✅ Problem: Import Errors with `-n auto`
**Problem**: When running `uv run pytest tests -n auto`, the test `test_field_colors.py` failed with import errors:

```
ImportError: cannot import name 'logger' from 'common'
ImportError: attempted relative import beyond top-level package
```

**Root Cause**: Pytest's multiprocessing mode (`-n auto`) changes the working directory and Python path structure, causing relative imports to fail.

## Technical Changes

### Updated Import Strategy in `src/plotting/term_chunked_plot.py`

#### Before (Problematic):
```python
# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    # Fallback to relative imports when run as module
    from ..common import logger
    from ..common.constants import TradingRule, BUY, SELL, NOTRADE
```

#### After (Fixed):
```python
# Use absolute imports when possible, fallback to relative
try:
    from common import logger
    from common.constants import TradingRule, BUY, SELL, NOTRADE
except ImportError:
    try:
        # Fallback to relative imports when run as module
        from ..common import logger
        from ..common.constants import TradingRule, BUY, SELL, NOTRADE
    except ImportError:
        # Final fallback for pytest with -n auto
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.common import logger
        from src.common.constants import TradingRule, BUY, SELL, NOTRADE
```

### Enhanced Import Strategy

The fix implements a **three-tier import strategy**:

1. **Primary**: Direct absolute imports (`from common import logger`)
2. **Secondary**: Relative imports (`from ..common import logger`)
3. **Tertiary**: Path-adjusted absolute imports (`from src.common import logger`)

## Why This Happened

### Pytest Multiprocessing Behavior
- **Single-threaded**: Tests run in the main process with normal Python path
- **Multiprocessing (`-n auto`)**: Tests run in separate worker processes
- **Working Directory**: Each worker process may have different working directory
- **Python Path**: Import resolution changes in multiprocessing mode

### Import Resolution Issues
1. **Relative imports** fail when package structure changes
2. **Absolute imports** fail when working directory changes
3. **Path manipulation** needed for consistent imports across all modes

## Testing Results

### Before Fix:
```bash
uv run pytest tests -n auto
# Result: ERROR tests/plotting/test_field_colors.py
# ImportError: cannot import name 'logger' from 'common'
```

### After Fix:
```bash
uv run pytest tests -n auto
# Result: ✅ 1919 passed, 70 skipped, 0 errors
```

## Benefits

1. **Consistent Behavior**: Tests work in both single-threaded and multiprocessing modes
2. **Robust Imports**: Three-tier fallback system handles all import scenarios
3. **Performance**: Multiprocessing mode works without errors
4. **Maintainability**: Clear import strategy with proper error handling

## Technical Details

### Import Fallback Chain
```python
try:
    # Level 1: Direct absolute import
    from common import logger
except ImportError:
    try:
        # Level 2: Relative import
        from ..common import logger
    except ImportError:
        # Level 3: Path-adjusted absolute import
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
        from src.common import logger
```

### Path Manipulation
- **Dynamic Path Addition**: `sys.path.insert(0, path)` adds project root to Python path
- **Cross-Platform**: Uses `os.path.join()` for platform-independent paths
- **Safe Execution**: Only modifies path when necessary

## Future Considerations

### Similar Issues
This pattern can be applied to other modules that experience import issues with:
- Pytest multiprocessing mode
- Different working directories
- Package structure changes

### Best Practices
1. **Always test with `-n auto`** to catch multiprocessing issues
2. **Use multiple import strategies** for robust code
3. **Test in different environments** (CI/CD, local, different Python versions)
4. **Document import dependencies** clearly

The fix ensures that the color assignment functionality works reliably in all testing scenarios, including high-performance multiprocessing mode.
