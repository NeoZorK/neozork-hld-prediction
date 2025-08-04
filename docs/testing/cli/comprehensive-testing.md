# Comprehensive CLI Testing Suite

This directory contains comprehensive automated tests for the `run_analysis.py` command line interface. The testing system automatically validates all possible flag combinations and ensures CLI functionality works correctly.

## 🚀 Quick Start

```bash
# Run all CLI tests
python run_all_cli_tests.py

# Run specific test types
python run_all_cli_tests.py --pytest --comprehensive

# Run with verbose output
python run_all_cli_tests.py --verbose

# Run in parallel
python run_all_cli_tests.py --parallel
```

## 📁 File Structure

```
tests/cli/comprehensive/
├── __init__.py                           # Package initialization
├── README.md                            # This file
├── pytest.ini                          # Pytest configuration
├── run_all_cli_tests.py                # Main test runner script
├── test_all_flags.py                   # Comprehensive test suite
├── test_all_flags_pytest.py            # Pytest-based test suite
├── test_auto_run_all_commands.py       # Auto command runner
└── test_flag_generator.py              # Flag combination generator
```

## 🧪 Test Types

### 1. Basic Flag Tests
Tests for fundamental CLI flags:
- `--version`, `--help`, `--examples`
- `--indicators`, `--interactive`
- Basic functionality validation

### 2. Mode Tests
Tests for all operating modes:
- `demo`, `yfinance`, `csv`, `polygon`, `binance`, `exrate`, `show`, `interactive`
- Mode-specific parameter validation
- Required parameter checking

### 3. Flag Combination Tests
Tests for flag interactions:
- Rule + draw mode combinations
- Export flag combinations
- Price type combinations
- Multiple flag scenarios

### 4. Error Case Tests
Tests for error conditions:
- Invalid modes and parameters
- Missing required parameters
- Conflicting flag combinations
- Invalid flag values

### 5. Performance Tests
Tests for performance characteristics:
- Execution time validation
- Resource usage monitoring
- Timeout detection
- Performance regression detection

### 6. Integration Tests
Tests for end-to-end scenarios:
- Full workflow validation
- Export functionality
- Data processing pipelines

## 🎯 Test Coverage

### Flags Covered
- **Basic**: `--version`, `--help`, `--examples`, `--indicators`, `--interactive`, `-i`
- **Data Source**: `--csv-file`, `--ticker`, `--interval`, `--point`, `--period`, `--start`, `--end`
- **Indicator**: `--rule`, `--price-type`
- **Show Mode**: `--source`, `--keywords`, `--show-start`, `--show-end`, `--show-rule`
- **Plotting**: `-d`, `--draw`
- **Export**: `--export-parquet`, `--export-csv`, `--export-json`, `--export-indicators-info`

### Modes Covered
- `demo` - Demo data analysis
- `yfinance/yf` - Yahoo Finance data
- `csv` - CSV file analysis
- `polygon` - Polygon.io data
- `binance` - Binance data
- `exrate` - Exchange rate data
- `show` - Data display mode
- `interactive` - Interactive mode

## 📊 Test Results

### Output Formats
- **Console**: Real-time progress and results
- **JSON**: Detailed test results
- **CSV**: Tabular test data
- **HTML**: Visual reports with charts

### Report Locations
All reports are saved to `logs/cli_tests/` with timestamps:
```
logs/cli_tests/
├── cli_test_results_YYYYMMDD_HHMMSS.json
├── cli_test_details_YYYYMMDD_HHMMSS.csv
├── cli_test_report_YYYYMMDD_HHMMSS.html
└── cli_auto_tests/
    ├── cli_test_detailed_YYYYMMDD_HHMMSS.log
    └── cli_test_summary_YYYYMMDD_HHMMSS.json
```

## 🔧 Usage Examples

### Run All Tests
```bash
python run_all_cli_tests.py
```

### Run Specific Test Types
```bash
# Pytest-based tests only
python run_all_cli_tests.py --pytest

# Comprehensive test suite only
python run_all_cli_tests.py --comprehensive

# Auto-generated tests only
python run_all_cli_tests.py --auto-generator

# Auto command runner only
python run_all_cli_tests.py --auto-runner
```

### Run Test Categories
```bash
# Basic functionality tests
python run_all_cli_tests.py --basic

# Performance tests
python run_all_cli_tests.py --performance

# Error case tests
python run_all_cli_tests.py --error-cases

# Flag combination tests
python run_all_cli_tests.py --flag-combinations
```

### Execution Options
```bash
# Run in parallel (faster execution)
python run_all_cli_tests.py --parallel

# Verbose output (detailed information)
python run_all_cli_tests.py --verbose

# Generate HTML report
python run_all_cli_tests.py --html-report

# Generate JSON report
python run_all_cli_tests.py --json-report
```

### Pytest Direct Usage
```bash
# Run pytest tests directly
pytest test_all_flags_pytest.py -v

# Run with specific markers
pytest test_all_flags_pytest.py -m basic
pytest test_all_flags_pytest.py -m performance
pytest test_all_flags_pytest.py -m error
pytest test_all_flags_pytest.py -m integration

# Exclude slow tests
pytest test_all_flags_pytest.py -m "not slow"

# Run in parallel
pytest test_all_flags_pytest.py -n auto
```

### Individual Test Files
```bash
# Run comprehensive test suite
python test_all_flags.py

# Run auto-generated tests
python test_flag_generator.py

# Run auto command runner
python test_auto_run_all_commands.py
```

## 📈 Performance Monitoring

### Performance Categories
- **Fast**: < 5 seconds
- **Normal**: 5-30 seconds
- **Slow**: > 30 seconds
- **Timeout**: Exceeded 60-second limit

### Performance Metrics
- Execution time per test
- Success rate by category
- Error distribution
- Resource usage patterns

## 🐛 Troubleshooting

### Common Issues

1. **Timeout Errors**
   ```bash
   # Increase timeout in test configuration
   # Check system resources
   # Verify network connectivity
   ```

2. **Missing Dependencies**
   ```bash
   # Install required packages
   pip install pytest pytest-xdist pytest-timeout
   ```

3. **File Permission Errors**
   ```bash
   # Ensure write permissions for log directories
   chmod -R 755 logs/
   ```

4. **API Rate Limits**
   ```bash
   # Tests handle rate limiting automatically
   # Use test data files for offline testing
   ```

### Debug Mode
```bash
# Enable verbose output for debugging
python run_all_cli_tests.py --verbose
```

## 🔄 Continuous Integration

### CI/CD Integration
```yaml
# Example GitHub Actions workflow
- name: Run CLI Tests
  run: |
    python tests/cli/comprehensive/run_all_cli_tests.py --pytest --comprehensive
    python tests/cli/comprehensive/run_all_cli_tests.py --auto-generator
```

### Testing GitHub Actions with Act

To test GitHub Actions workflows and CI/CD integration without downloading Docker images or installing dependencies:

```bash
# Install act tool
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash  # Linux

# Test all workflows (dry run - no Docker downloads)
act -n

# Test specific workflow
act -n -W .github/workflows/docker-build.yml

# Test MCP server integration workflows
act -n -W .github/workflows/mcp-integration.yml
act -n -W .github/workflows/mcp-servers-ci.yml

# List available workflows
act -l
```

**Benefits of Dry Run Testing:**
- **No Docker Downloads**: Prevents downloading large Docker images
- **Fast Validation**: Quickly validates workflow syntax and structure
- **Resource Efficient**: Uses minimal system resources
- **Safe Testing**: No risk of affecting your local environment
- **Protocol Validation**: Verify MCP server communication protocols
- **Integration Testing**: Test MCP server with various IDEs

### Automated Testing
- Automatic test generation
- Regression detection
- Performance monitoring
- Report generation

## 📚 Documentation

For detailed documentation, see:
- [Comprehensive CLI Testing Documentation](../../../docs/development/cli-comprehensive-testing.md)
- [CLI Interface Guide](../../../docs/guides/cli-interface.md)
- [Development Guide](../../../docs/development/index.md)

## 🤝 Contributing

### Adding New Tests
1. Follow existing test patterns
2. Use appropriate markers
3. Include error cases
4. Document test purpose

### Test Maintenance
1. Regular test updates
2. Flag combination validation
3. Performance monitoring
4. Error case coverage

## 📋 Test Statistics

### Typical Test Results
- **Total Tests**: 500+ test cases
- **Execution Time**: 10-30 minutes (depending on system)
- **Success Rate**: >95% (expected)
- **Coverage**: All CLI flags and modes

### Test Categories Distribution
- Basic Flags: ~10%
- Mode Tests: ~30%
- Flag Combinations: ~25%
- Error Cases: ~20%
- Performance Tests: ~10%
- Integration Tests: ~5%

## 🎯 Best Practices

### Test Development
1. **Modular Design**: Keep tests focused and independent
2. **Clear Naming**: Use descriptive test names
3. **Error Handling**: Include comprehensive error cases
4. **Performance**: Monitor execution times

### Test Execution
1. **Regular Testing**: Run tests before commits
2. **Monitoring**: Track performance trends
3. **Documentation**: Keep test documentation updated
4. **Maintenance**: Regular test updates and cleanup

## 🔮 Future Enhancements

### Planned Features
1. **Enhanced Reporting**: Interactive dashboards, trend analysis
2. **Advanced Testing**: ML-based test generation, fuzz testing
3. **Integration Improvements**: Docker testing, cloud-based execution
4. **Performance Optimization**: Distributed execution, caching

### Roadmap
- [ ] Interactive test dashboard
- [ ] Machine learning test generation
- [ ] Cloud-based test execution
- [ ] Advanced performance analytics
- [ ] Security testing integration

## 📞 Support

For questions or issues:
1. Check test logs in `logs/cli_tests/`
2. Review documentation in `docs/development/`
3. Contact development team
4. Create issue in project repository

---

**Note**: This testing suite is designed to catch regressions and ensure CLI functionality remains stable across development iterations. Regular execution is recommended for maintaining code quality. 