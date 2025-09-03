# Plot Display Fix

## Overview

This document describes the fixes applied to resolve the issue where charts were closing instantly when using `-d mpl` and `-d sb` flags.

## Problem Description

The original issue was that when using commands like:
```bash
uv run run_analysis.py show csv gbp mn1 -d mpl --rule AUTO
uv run run_analysis.py show csv gbp mn1 -d sb --rule AUTO
```

The charts would open and immediately close, making it impossible to view the generated plots.

## Root Cause

The problem was in the matplotlib backend configuration and interactive mode handling:

1. **Backend Issues**: The matplotlib backend was not properly configured for macOS
2. **Interactive Mode**: Interactive mode was disabled, causing plots to close immediately
3. **Blocking Display**: The `plt.show()` calls were not properly blocking execution

## Fixes Applied

### 1. Enhanced `smart_plot_display` Function (`src/plotting/plot_utils.py`)

- Added automatic backend setup call at the beginning
- Implemented proper blocking mode with double `plt.show()` calls
- Added `force_interactive_mode()` call for blocking displays
- Increased default pause time from 5 to 10 seconds

### 2. Improved `setup_interactive_backend` Function

- Added platform detection for macOS vs other systems
- Automatically sets `macosx` backend on macOS
- Falls back to `TkAgg` on other systems
- Enables interactive mode with `plt.ion()`
- Added informative logging for backend configuration

### 3. New `force_interactive_mode` Function

- Forces matplotlib into interactive mode
- Validates backend compatibility
- Provides warnings for unsupported backends
- Ensures blocking plots work correctly

## Technical Details

### Backend Selection Logic

```python
def setup_interactive_backend():
    if not is_test_environment():
        try:
            import platform
            if platform.system() == 'Darwin':  # macOS
                matplotlib.use('macosx')
            else:
                matplotlib.use('TkAgg')
            plt.ion()
        except Exception as e:
            print(f"Warning: Could not set interactive backend: {e}")
```

### Blocking Mode Implementation

```python
def smart_plot_display(show_plot=True, block=None, pause_time=None):
    setup_interactive_backend()
    
    if show_plot and should_show_plot():
        if block:
            force_interactive_mode()
            plt.show(block=True)
            plt.show()  # Keep plot open until user closes it
        else:
            plt.show(block=False)
            time.sleep(pause_time)
            plt.close()
```

## Environment Variables

The following environment variables can be used to control plot behavior:

- `PLOT_BLOCK_MODE`: Set to `true` (default) for blocking plots, `false` for auto-close
- `PLOT_PAUSE_TIME`: Time in seconds to pause before auto-closing (default: 10.0)

## Testing

Comprehensive tests were created in `tests/test_plot_display_fix.py`:

- ✅ `force_interactive_mode` functionality
- ✅ Blocking mode display
- ✅ Non-blocking mode display
- ✅ Environment variable handling
- ✅ Test environment detection

## Usage Examples

### Blocking Mode (Default)
```bash
# Charts stay open until manually closed
uv run run_analysis.py show csv gbp mn1 -d mpl --rule AUTO
uv run run_analysis.py show csv gbp mn1 -d sb --rule AUTO
```

### Non-blocking Mode
```bash
# Set environment variable for auto-close behavior
export PLOT_BLOCK_MODE=false
export PLOT_PAUSE_TIME=15.0

uv run run_analysis.py show csv gbp mn1 -d mpl --rule AUTO
```

## Files Modified

- `src/plotting/plot_utils.py` - Core plotting utilities and display logic

## Dependencies

- `matplotlib` - Core plotting library
- `platform` - System platform detection
- Standard Python libraries: `os`, `sys`, `time`

## Verification

The fixes have been verified with:

1. **Functional Testing**: Both `-d mpl` and `-d sb` flags now work correctly
2. **Backend Verification**: macOS backend is properly set to `macosx`
3. **Interactive Mode**: Interactive mode is enabled for blocking displays
4. **Test Coverage**: Comprehensive test suite covers all scenarios

## Future Improvements

1. Add support for more matplotlib backends
2. Implement configurable plot window management
3. Add progress indicators for long-running plot operations
4. Consider adding plot export options for non-interactive environments
