# SMA Indicator Testing Guide

## Overview

This guide covers comprehensive testing of the SMA (Simple Moving Average) indicator across all display modes and scenarios.

## Automated Testing

### 1. Run All Tests

```bash
# Run all tests with UV
uv run pytest tests/ -n auto

# Run with verbose output
uv run pytest tests/ -n auto -v

# Run with coverage
uv run pytest tests/ -n auto --cov=src --cov-report=html
```

### 2. SMA-Specific Tests

```bash
# Test SMA calculation module
uv run pytest tests/calculation/indicators/trend/test_sma_indicator.py -v

# Test CLI integration
uv run pytest tests/cli/ -k "sma" -v

# Test plotting modes
uv run pytest tests/plotting/ -k "sma" -v

# Test all SMA-related tests
uv run pytest tests/ -k "sma" -v
```

### 3. Test Categories

#### Unit Tests
```bash
# Core SMA calculation
uv run pytest tests/calculation/indicators/trend/test_sma_indicator.py::TestSMAIndicator::test_calculate_sma_basic -v

# Parameter validation
uv run pytest tests/calculation/indicators/trend/test_sma_indicator.py::TestSMAIndicator::test_calculate_sma_invalid_period -v

# Edge cases
uv run pytest tests/calculation/indicators/trend/test_sma_indicator.py::TestSMAIndicator::test_calculate_sma_insufficient_data -v
```

#### Integration Tests
```bash
# CLI parameter parsing
uv run pytest tests/cli/ -k "parse_sma" -v

# Rule application
uv run pytest tests/calculation/ -k "apply_rule_sma" -v

# Help system
uv run pytest tests/cli/ -k "sma_help" -v
```

#### Plotting Tests
```bash
# Fastest mode
uv run pytest tests/plotting/ -k "fastest_sma" -v

# Fast mode
uv run pytest tests/plotting/ -k "fast_sma" -v

# Plotly mode
uv run pytest tests/plotting/ -k "plotly_sma" -v

# MPL mode
uv run pytest tests/plotting/ -k "mpl_sma" -v

# Seaborn mode
uv run pytest tests/plotting/ -k "seaborn_sma" -v

# Terminal mode
uv run pytest tests/plotting/ -k "term_sma" -v
```

## Manual Testing

### 1. Test All Display Modes

```bash
# Test script for all modes
for mode in fastest fast plotly mpl seaborn term; do
    echo "Testing SMA in $mode mode..."
    uv run run_analysis.py demo --rule sma:20,close -d $mode
    echo "Completed $mode mode test"
    echo "----------------------------------------"
done
```

### 2. Test Different Parameters

```bash
# Test different periods
for period in 5 10 20 50 100; do
    echo "Testing SMA period $period..."
    uv run run_analysis.py demo --rule sma:$period,close -d fastest
done

# Test different price types
uv run run_analysis.py demo --rule sma:20,close -d fastest
uv run run_analysis.py demo --rule sma:20,open -d fastest

# Test multiple SMAs
uv run run_analysis.py demo --rule sma:10,close,sma:20,close,sma:50,close -d plotly
```

### 3. Test with Real Data

```bash
# Test with different assets
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:20,close -d fastest
uv run run_analysis.py yfinance --ticker BTC-USD --period 6mo --point 0.01 --rule sma:20,close -d plotly
uv run run_analysis.py yfinance --ticker EURUSD=X --period 1y --point 0.00001 --rule sma:20,close -d mpl

# Test with different timeframes
uv run run_analysis.py yfinance --ticker AAPL --period 1mo --point 0.01 --rule sma:5,close -d fastest
uv run run_analysis.py yfinance --ticker AAPL --period 2y --point 0.01 --rule sma:100,close -d plotly
```

## Performance Testing

### 1. Large Dataset Testing

```bash
# Test with large datasets
uv run run_analysis.py yfinance --ticker SPY --period 5y --point 0.01 --rule sma:20,close -d fastest

# Test multiple indicators
uv run run_analysis.py yfinance --ticker SPY --period 2y --point 0.01 --rule sma:20,close,sma:50,close,rsi:14,macd:12,26,9 -d fastest
```

### 2. Memory Usage Testing

```bash
# Monitor memory usage
python -m memory_profiler scripts/test_sma_performance.py

# Test with different data sizes
for period in 1mo 3mo 6mo 1y 2y 5y; do
    echo "Testing $period period..."
    uv run run_analysis.py yfinance --ticker AAPL --period $period --point 0.01 --rule sma:20,close -d fastest
done
```

## Error Testing

### 1. Invalid Parameters

```bash
# Test invalid period
uv run run_analysis.py demo --rule sma:0,close -d fastest

# Test invalid price type
uv run run_analysis.py demo --rule sma:20,invalid -d fastest

# Test missing parameters
uv run run_analysis.py demo --rule sma:20 -d fastest

# Test too many parameters
uv run run_analysis.py demo --rule sma:20,close,extra -d fastest
```

### 2. Edge Cases

```bash
# Test with minimal data
uv run run_analysis.py yfinance --ticker AAPL --period 1d --point 0.01 --rule sma:20,close -d fastest

# Test with very long period
uv run run_analysis.py yfinance --ticker AAPL --period 1y --point 0.01 --rule sma:1000,close -d fastest

# Test with zero data
uv run run_analysis.py yfinance --ticker INVALID --period 1y --point 0.01 --rule sma:20,close -d fastest
```

## Regression Testing

### 1. Compare Results

```bash
# Test consistency across modes
for mode in fastest fast plotly mpl seaborn term; do
    echo "Testing $mode mode consistency..."
    uv run run_analysis.py demo --rule sma:20,close -d $mode --export-csv
done

# Compare exported files
python scripts/compare_sma_results.py
```

### 2. Version Comparison

```bash
# Test against previous version
git checkout main
uv run run_analysis.py demo --rule sma:20,close -d fastest --export-csv
git checkout feature/sma-enhancement
uv run run_analysis.py demo --rule sma:20,close -d fastest --export-csv
python scripts/compare_versions.py
```

## Integration Testing

### 1. CLI Integration

```bash
# Test help system
uv run run_analysis.py demo --rule sma --help

# Test parameter parsing
uv run run_analysis.py demo --rule sma:20,close -d fastest --verbose

# Test error handling
uv run run_analysis.py demo --rule sma:invalid -d fastest
```

### 2. Export Testing

```bash
# Test all export formats
uv run run_analysis.py demo --rule sma:20,close -d fastest --export-parquet
uv run run_analysis.py demo --rule sma:20,close -d fastest --export-csv
uv run run_analysis.py demo --rule sma:20,close -d fastest --export-json

# Verify exported files
python scripts/verify_exports.py
```

## Load Testing

### 1. Concurrent Usage

```bash
# Test multiple concurrent requests
for i in {1..5}; do
    uv run run_analysis.py demo --rule sma:20,close -d fastest &
done
wait

# Test with different parameters
for period in 10 20 50; do
    for price_type in open close; do
        uv run run_analysis.py demo --rule sma:$period,$price_type -d fastest &
    done
done
wait
```

### 2. Stress Testing

```bash
# Test with maximum data
uv run run_analysis.py yfinance --ticker SPY --period max --point 0.01 --rule sma:20,close -d fastest

# Test multiple indicators
uv run run_analysis.py demo --rule sma:20,close,sma:50,close,rsi:14,macd:12,26,9,bb:20,2,atr:14 -d fastest
```

## Browser Testing (for Web-based modes)

### 1. Plotly Mode Testing

```bash
# Test plotly interactivity
uv run run_analysis.py demo --rule sma:20,close -d plotly

# Test in different browsers
# - Chrome
# - Firefox
# - Safari
# - Edge
```

### 2. Responsive Design Testing

```bash
# Test different screen sizes
# - Desktop (1920x1080)
# - Tablet (768x1024)
# - Mobile (375x667)
```

## Continuous Integration Testing

### 1. Automated Test Suite

```yaml
# .github/workflows/sma-testing.yml
name: SMA Testing

on: [push, pull_request]

jobs:
  test-sma:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install UV
        run: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Run SMA tests
        run: |
          uv run pytest tests/ -k "sma" -v
      - name: Test all display modes
        run: |
          for mode in fastest fast plotly mpl seaborn term; do
            uv run run_analysis.py demo --rule sma:20,close -d $mode
          done
```

### 2. Performance Regression Testing

```bash
# Automated performance test
python scripts/performance_test_sma.py

# Compare with baseline
python scripts/compare_performance.py baseline.json current_results.json
```

## Test Data Management

### 1. Test Data Creation

```bash
# Create test datasets
python scripts/create_test_data.py --periods 1000 --indicators sma

# Create edge case data
python scripts/create_edge_case_data.py --minimal --large-period
```

### 2. Test Data Validation

```bash
# Validate test data
python scripts/validate_test_data.py

# Check data integrity
python scripts/check_data_integrity.py
```

## Reporting

### 1. Test Results Summary

```bash
# Generate test report
uv run pytest tests/ -k "sma" --html=reports/sma_test_report.html --self-contained-html

# Generate coverage report
uv run pytest tests/ -k "sma" --cov=src --cov-report=html --cov-report=term
```

### 2. Performance Report

```bash
# Generate performance report
python scripts/generate_performance_report.py

# Compare performance across modes
python scripts/compare_mode_performance.py
```

## Best Practices

### 1. Test Organization
- Group related tests together
- Use descriptive test names
- Include both positive and negative test cases
- Test edge cases and error conditions

### 2. Test Data
- Use consistent test data across tests
- Include edge cases (minimal data, large periods)
- Test with real market data
- Validate data integrity

### 3. Performance Testing
- Test with realistic data sizes
- Monitor memory and CPU usage
- Compare performance across modes
- Set performance baselines

### 4. Continuous Testing
- Run tests on every code change
- Include automated regression testing
- Monitor test coverage
- Maintain test documentation

## Troubleshooting

### Common Test Issues

1. **Test failures due to data changes**
   ```bash
   # Regenerate test data
   python scripts/regenerate_test_data.py
   ```

2. **Performance test failures**
   ```bash
   # Check system resources
   python scripts/check_system_resources.py
   ```

3. **Display mode test failures**
   ```bash
   # Check display dependencies
   python scripts/check_display_dependencies.py
   ```

### Debug Commands

```bash
# Debug test failures
uv run pytest tests/ -k "sma" -v --tb=short

# Debug specific test
uv run pytest tests/calculation/indicators/trend/test_sma_indicator.py::TestSMAIndicator::test_calculate_sma_basic -v -s

# Profile test performance
python -m cProfile -o profile.stats scripts/run_sma_tests.py
```

## Next Steps

1. **Run comprehensive tests** using the commands above
2. **Set up continuous integration** for automated testing
3. **Create custom test scenarios** for your specific use cases
4. **Monitor test performance** and optimize as needed
5. **Contribute test improvements** to the project

For more information, see:
- [Complete SMA Tutorial](adding-sma-indicator-tutorial.md)
- [Quick Start Guide](sma-quick-start-guide.md)
- [Practical Examples](sma-practical-examples.md)
- [Testing Guide](testing.md)
