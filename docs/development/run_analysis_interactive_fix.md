# Run Analysis Interactive Mode Fix

## Overview

This document describes the fixes applied to the `run_analysis.py` script to properly handle the `--interactive` flag.

## Problem Description

The original `run_analysis.py` script had the following issues:

1. The `--interactive` flag was defined in CLI but not properly handled in the workflow
2. The script would always run in interactive mode regardless of command line arguments
3. The `mode` argument was required even when using `--interactive` flag

## Fixes Applied

### 1. CLI Module Updates (`src/cli/cli.py`)

- Made the `mode` argument optional (`nargs='?'`) to support `--interactive` flag usage
- Added automatic mode setting logic: when `--interactive` is used without a mode, it automatically sets `mode = 'interactive'`
- Updated help text to clarify that mode is not required when using `--interactive`

### 2. Workflow Module Updates (`src/workflow/workflow.py`)

- Added import for `InteractiveSystem` from `src.interactive.core`
- Added special case handling for interactive mode at the beginning of `run_indicator_workflow()`
- Interactive mode now properly creates and runs the `InteractiveSystem` instance
- Added proper error handling and result structure for interactive mode

### 3. Test Coverage

- Created comprehensive tests in `tests/test_run_analysis_interactive.py`
- Tests cover both successful and error scenarios for interactive mode
- Tests verify proper argument parsing and workflow execution

## Usage Examples

### Interactive Mode
```bash
# Start interactive mode (mode automatically set to 'interactive')
uv run run_analysis.py --interactive

# Start interactive mode with explicit mode
uv run run_analysis.py --interactive demo
```

### Non-Interactive Mode
```bash
# Run with demo data and EMA indicator
uv run run_analysis.py demo --rule EMA

# Run with CSV file
uv run run_analysis.py csv --csv-file data.csv --rule RSI
```

## Technical Details

### Argument Parsing Flow

1. User provides `--interactive` flag
2. CLI parser processes the flag and sets `args.interactive = True`
3. If no mode is specified, `args.mode` is automatically set to `'interactive'`
4. Workflow detects interactive mode and bypasses normal data processing
5. `InteractiveSystem` is instantiated and run

### Result Structure

Interactive mode returns a standardized result structure:

```python
{
    "success": True,
    "effective_mode": "interactive",
    "data_source_label": "Interactive mode",
    "error_message": None,
    "error_traceback": None,
    "data_fetch_duration": 0,
    "calc_duration": 0,
    "plot_duration": 0,
    "rows_count": 0,
    "columns_count": 0,
    "data_size_mb": 0,
    "data_size_bytes": 0
}
```

## Testing

Run the interactive mode tests:

```bash
uv run pytest tests/test_run_analysis_interactive.py -v
```

## Files Modified

- `src/cli/cli.py` - CLI argument handling
- `src/workflow/workflow.py` - Workflow execution logic
- `tests/test_run_analysis_interactive.py` - Test coverage (new file)

## Dependencies

- `src.interactive.core.InteractiveSystem` - Interactive system implementation
- Standard Python libraries: `argparse`, `sys`, `traceback`

## Future Improvements

1. Add more granular control over interactive mode behavior
2. Consider adding configuration options for interactive mode
3. Implement interactive mode for specific data sources
4. Add progress indicators for long-running interactive operations
