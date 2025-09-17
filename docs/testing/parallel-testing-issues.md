# Parallel Testing Issues and Solutions

## Problem Description

Some tests fail when running with `-n auto` (parallel execution) due to race conditions or shared resource conflicts. These tests work correctly when run individually or with fewer threads.

## Affected Tests

The following tests have been identified as problematic with parallel execution:

1. `tests/test_run_analysis.py::test_run_analysis_basic_functionality`
2. `tests/src/plotting/test_term_chunked_plot.py::TestTermChunkedPlot::test_plot_chunked_terminal_with_invalid_input`
3. `tests/src/plotting/test_term_chunked_plot.py::TestTermChunkedPlot::test_plot_chunked_terminal_with_navigation`

## Root Cause

These tests likely have race conditions due to:
- Shared file system resources
- Subprocess execution conflicts
- Mock/patch conflicts between parallel workers
- Input/output stream conflicts

## Solution

### 1. Mark Tests with `no_parallel` Marker

Tests that cannot run in parallel are marked with `@pytest.mark.no_parallel`:

```python
@pytest.mark.no_parallel
def test_run_analysis_basic_functionality():
    """Test basic run_analysis functionality"""
    # ... test implementation
```

### 2. Run Problematic Tests Separately

For CI/CD or manual testing, run problematic tests without parallel execution:

```bash
# Run all tests with parallel execution (excluding problematic ones)
uv run pytest tests/ -n auto

# Run problematic tests separately without parallel execution
uv run pytest tests/test_run_analysis.py::test_run_analysis_basic_functionality -v
uv run pytest tests/src/plotting/test_term_chunked_plot.py::TestTermChunkedPlot::test_plot_chunked_terminal_with_invalid_input -v
uv run pytest tests/src/plotting/test_term_chunked_plot.py::TestTermChunkedPlot::test_plot_chunked_terminal_with_navigation -v
```

### 3. Alternative: Use Fewer Threads

If you need to run all tests together, use fewer threads:

```bash
uv run pytest tests/ -n 2  # Use 2 threads instead of auto
```

## Configuration

The `pytest.ini` file includes the `no_parallel` marker definition:

```ini
markers =
    no_parallel: marks tests that should not run in parallel (due to shared resources)
```

## Best Practices

1. **Identify Race Conditions**: Look for tests that use:
   - File system operations
   - Subprocess calls
   - Mock/patch with global state
   - Input/output streams

2. **Mark Appropriately**: Use `@pytest.mark.no_parallel` for tests that cannot run in parallel

3. **Test Both Modes**: Ensure tests pass both with and without parallel execution

4. **Document Issues**: Keep this document updated when new problematic tests are found

## Future Improvements

Consider refactoring problematic tests to:
- Use isolated temporary directories
- Avoid global state modifications
- Use proper mocking without conflicts
- Implement proper cleanup mechanisms
