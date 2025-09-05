#!/bin/bash
# Script to run problematic tests that fail with -n auto

echo "Running problematic tests without parallel execution..."

# Run tests that have race conditions with parallel execution
uv run pytest tests/test_run_analysis.py::test_run_analysis_basic_functionality -v
uv run pytest tests/src/plotting/test_term_chunked_plot.py::TestTermChunkedPlot::test_plot_chunked_terminal_with_invalid_input -v
uv run pytest tests/src/plotting/test_term_chunked_plot.py::TestTermChunkedPlot::test_plot_chunked_terminal_with_navigation -v

echo "Problematic tests completed."
