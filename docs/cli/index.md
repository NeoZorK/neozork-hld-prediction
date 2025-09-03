# Command Line Interface (CLI)

The Neozork HLD Prediction system provides a comprehensive command-line interface for all system operations.

> **📖 Complete CLI Guide**: For comprehensive CLI usage, see [CLI_GUIDE.md](CLI_GUIDE.md)

## Overview

The CLI is designed to be intuitive, powerful, and extensible. It provides access to all major system functionality through a unified interface.

## Quick Start

```bash
# Get help
neozork --help

# Get version
neozork --version

# Enable verbose output
neozork --verbose --help
```

## Available Commands

### Analysis Commands

#### `analyze` - Financial Data Analysis

Analyze financial data using various technical indicators and analysis methods.

```bash
# Basic analysis
neozork analyze --data data.csv

# Analysis with specific indicators
neozork analyze --data data.csv --indicators sma,rsi,bb

# Analysis with output file
neozork analyze --data data.csv --indicators sma,rsi --output results.json

# Analysis with custom parameters
neozork analyze --data data.csv --indicators sma --parameters '{"period": 20}'
```

**Options:**
- `--data, -d`: Path to data file (required)
- `--indicators, -i`: Comma-separated list of indicators
- `--output, -o`: Output file path
- `--parameters`: JSON string of indicator parameters

**Supported Indicators:**
- `sma`: Simple Moving Average
- `ema`: Exponential Moving Average
- `rsi`: Relative Strength Index
- `bb`: Bollinger Bands
- `macd`: MACD
- `stoch`: Stochastic Oscillator

#### `train` - Machine Learning Model Training

Train machine learning models on financial data.

```bash
# Train Random Forest model
neozork train --model random_forest --data train.csv

# Train with custom parameters
neozork train --model random_forest --data train.csv --parameters '{"n_estimators": 100}'

# Train with output path
neozork train --model random_forest --data train.csv --output models/rf_model.joblib
```

**Options:**
- `--model, -m`: Model type to train (required)
- `--data, -d`: Path to training data (required)
- `--output, -o`: Output model path
- `--parameters`: JSON string of model parameters

**Supported Models:**
- `random_forest`: Random Forest Classifier
- `xgboost`: XGBoost Classifier
- `lightgbm`: LightGBM Classifier
- `neural_network`: Neural Network Classifier

#### `predict` - Model Predictions

Make predictions using trained machine learning models.

```bash
# Make predictions
neozork predict --model model.joblib --data test.csv

# Predictions with output
neozork predict --model model.joblib --data test.csv --output predictions.csv

# Predictions with confidence
neozork predict --model model.joblib --data test.csv --confidence
```

**Options:**
- `--model, -m`: Path to trained model (required)
- `--data, -d`: Path to prediction data (required)
- `--output, -o`: Output predictions path
- `--confidence`: Include confidence scores

### Data Management Commands

#### `data` - Data Operations

Perform various data management operations.

```bash
# Fetch data from source
neozork data fetch --source api --symbol AAPL

# Process data
neozork data process --input raw.csv --output processed.csv

# Validate data
neozork data validate --data data.csv

# Export data
neozork data export --data results.json --format csv
```

**Operations:**
- `fetch`: Retrieve data from external sources
- `process`: Transform and clean data
- `validate`: Check data quality and integrity
- `export`: Convert data to different formats

**Options:**
- `--source, -s`: Data source identifier
- `--input`: Input file path
- `--output, -o`: Output file path
- `--format`: Export format (csv, json, parquet)

### Help Commands

#### `help` - Detailed Help

Get detailed help for specific topics.

```bash
# General help
neozork help

# Help for specific topic
neozork help analysis
neozork help indicators
neozork help ml
neozork help data
```

## Global Options

All commands support these global options:

- `--version`: Show version information
- `--verbose, -v`: Enable verbose output
- `--config`: Path to configuration file
- `--help, -h`: Show help information

## Configuration

The CLI can be configured using a configuration file:

```json
{
  "data": {
    "cache_dir": "data/cache",
    "raw_dir": "data/raw",
    "processed_dir": "data/processed"
  },
  "analysis": {
    "default_timeframe": "1H",
    "max_lookback_periods": 1000
  },
  "ml": {
    "model_dir": "models",
    "default_algorithm": "random_forest"
  },
  "export": {
    "default_format": "csv",
    "output_dir": "results"
  }
}
```

## Examples

### Complete Analysis Workflow

```bash
# 1. Fetch data
neozork data fetch --source yfinance --symbol AAPL --timeframe 1D

# 2. Process data
neozork data process --input raw_aapl.csv --output processed_aapl.csv

# 3. Analyze data
neozork analyze --data processed_aapl.csv --indicators sma,rsi,bb --output analysis.json

# 4. Train model
neozork train --model random_forest --data processed_aapl.csv --output aapl_model.joblib

# 5. Make predictions
neozork predict --model aapl_model.joblib --data new_data.csv --output predictions.csv
```

### Batch Processing

```bash
# Process multiple symbols
for symbol in AAPL MSFT GOOGL; do
  neozork data fetch --source yfinance --symbol $symbol
  neozork analyze --data ${symbol}.csv --indicators sma,rsi --output ${symbol}_analysis.json
done
```

### Custom Analysis

```bash
# Custom moving average analysis
neozork analyze --data data.csv --indicators sma \
  --parameters '{"sma": {"period": 50}, "rsi": {"period": 14}}' \
  --output custom_analysis.json
```

## Error Handling

The CLI provides comprehensive error handling:

- **Validation Errors**: Clear messages for invalid inputs
- **File Errors**: Helpful messages for file operations
- **Network Errors**: Retry logic for external API calls
- **Model Errors**: Detailed error messages for ML operations

## Exit Codes

- `0`: Success
- `1`: General error
- `130`: User interruption (Ctrl+C)

## Logging

The CLI provides structured logging:

```bash
# Enable debug logging
neozork --verbose analyze --data data.csv

# Log file location
# Default: logs/cli.log
# Configurable via config file
```

## Extending the CLI

### Adding New Commands

1. Create command implementation in `src/cli/commands/`
2. Register command in `src/cli/core/command_manager.py`
3. Add help documentation
4. Write comprehensive tests

### Custom Indicators

1. Implement indicator in `src/analysis/indicators/`
2. Register in indicator registry
3. Add CLI support in analyze command

### Custom Models

1. Implement model in `src/ml/models/`
2. Register in model registry
3. Add CLI support in train command

## Best Practices

### Command Design

- Use descriptive command names
- Provide clear help text
- Use consistent option naming
- Support both short and long options

### Error Handling

- Validate inputs early
- Provide helpful error messages
- Use appropriate exit codes
- Log errors for debugging

### Performance

- Use efficient data processing
- Support parallel execution
- Implement caching where appropriate
- Monitor resource usage

## Troubleshooting

### Common Issues

1. **Command not found**: Ensure proper installation
2. **Permission denied**: Check file permissions
3. **Data format error**: Verify input data format
4. **Model loading error**: Check model file integrity

### Debug Mode

```bash
# Enable debug output
neozork --verbose --debug analyze --data data.csv

# Check configuration
neozork --config-debug analyze --data data.csv
```

### Getting Help

```bash
# Command help
neozork <command> --help

# General help
neozork --help

# Topic help
neozork help <topic>
```

## Related Documentation

- [Analysis Guide](../analysis/index.md)
- [Machine Learning Guide](../ml/index.md)
- [Data Management Guide](../data/index.md)
- [Configuration Guide](../configuration/index.md)
