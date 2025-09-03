# CLI Guide

## Overview

The Neozork HLD Prediction system provides a comprehensive command-line interface (CLI) for financial analysis, machine learning, and data processing operations.

## Quick Start

### Basic Usage
```bash
# Get help
neozork --help

# Get version
neozork --version

# Run with verbose output
neozork --verbose
```

### Main Commands
```bash
# Analyze financial data
neozork analyze --data data.csv --indicators sma,rsi

# Train ML model
neozork train --model random_forest --data data.csv

# Make predictions
neozork predict --model model.joblib --data test_data.csv

# Data operations
neozork data --action clean --input raw_data.csv --output clean_data.csv

# Get help for specific command
neozork analyze --help
```

## Command Reference

### Global Options
```bash
--help, -h          Show help message and exit
--version, -v       Show version and exit
--verbose           Enable verbose output
--config PATH       Path to configuration file
--log-level LEVEL   Set logging level (DEBUG, INFO, WARNING, ERROR)
--output-dir DIR    Output directory for results
```

### Analyze Command
```bash
neozork analyze [OPTIONS]

Options:
  --data PATH              Input data file (CSV, JSON, Parquet)
  --indicators LIST        Comma-separated list of indicators
  --timeframe STR          Timeframe for analysis (1m, 5m, 15m, 1h, 4h, 1d, 1w)
  --period INT             Period for indicators
  --output PATH            Output file path
  --format STR             Output format (csv, json, parquet, html)
  --plot                   Generate plots
  --save-plots             Save plots to files

Examples:
  neozork analyze --data ohlcv.csv --indicators sma,rsi --timeframe 1h
  neozork analyze --data data.csv --indicators bollinger_bands --period 20 --plot
  neozork analyze --data prices.csv --indicators macd,stoch --output results.json
```

### Train Command
```bash
neozork train [OPTIONS]

Options:
  --model STR              ML algorithm (random_forest, xgboost, lstm)
  --data PATH              Training data file
  --target STR             Target column name
  --features LIST          Comma-separated list of feature columns
  --test-size FLOAT        Test set size (0.0-1.0)
  --random-state INT       Random seed for reproducibility
  --output PATH            Model output path
  --config PATH            Model configuration file

Examples:
  neozork train --model random_forest --data features.csv --target price
  neozork train --model xgboost --data data.csv --target target --test-size 0.2
  neozork train --model lstm --data time_series.csv --target next_price --output model.h5
```

### Predict Command
```bash
neozork predict [OPTIONS]

Options:
  --model PATH             Path to trained model file
  --data PATH              Input data for prediction
  --output PATH            Output file path
  --format STR             Output format (csv, json, parquet)
  --confidence             Include confidence intervals
  --explain                Generate feature importance/explanation

Examples:
  neozork predict --model model.joblib --data test_data.csv
  neozork predict --model model.h5 --data new_data.csv --confidence
  neozork predict --model model.pkl --data data.csv --explain --output predictions.json
```

### Data Command
```bash
neozork data [OPTIONS]

Options:
  --action STR             Action to perform (clean, validate, convert, merge)
  --input PATH             Input data file
  --output PATH            Output data file
  --format STR             Output format
  --config PATH            Data processing configuration

Examples:
  neozork data --action clean --input raw.csv --output clean.csv
  neozork data --action convert --input data.csv --output data.parquet
  neozork data --action validate --input data.csv --config validation.json
```

### Help Command
```bash
neozork help [COMMAND]

Examples:
  neozork help              # Show general help
  neozork help analyze      # Show help for analyze command
  neozork help train        # Show help for train command
```

## Configuration

### Configuration File
```json
{
  "cli": {
    "default_command": "help",
    "verbose": false,
    "colors": true,
    "progress_bars": true,
    "commands": {
      "analyze": {
        "default_indicators": ["sma", "rsi"],
        "max_indicators": 10
      },
      "train": {
        "default_algorithm": "random_forest",
        "test_size": 0.2
      }
    }
  }
}
```

### Environment Variables
```bash
# CLI configuration
export NEOZORK_CLI_VERBOSE=true
export NEOZORK_CLI_COLORS=true
export NEOZORK_CLI_OUTPUT_DIR=/path/to/output

# Command-specific configuration
export NEOZORK_ANALYSIS_DEFAULT_TIMEFRAME=1H
export NEOZORK_ML_DEFAULT_ALGORITHM=xgboost
```

## Usage Examples

### Financial Analysis Workflow
```bash
# 1. Clean and prepare data
neozork data --action clean --input raw_ohlcv.csv --output clean_ohlcv.csv

# 2. Analyze with technical indicators
neozork analyze \
  --data clean_ohlcv.csv \
  --indicators sma,rsi,bollinger_bands,macd \
  --timeframe 1h \
  --period 20 \
  --plot \
  --save-plots \
  --output analysis_results.json

# 3. Train ML model
neozork train \
  --model random_forest \
  --data clean_ohlcv.csv \
  --target next_close \
  --features open,high,low,close,volume \
  --test-size 0.2 \
  --output price_predictor.joblib

# 4. Make predictions
neozork predict \
  --model price_predictor.joblib \
  --data new_data.csv \
  --confidence \
  --output predictions.csv
```

### Batch Processing
```bash
# Process multiple files
for file in data/*.csv; do
  neozork analyze \
    --data "$file" \
    --indicators sma,rsi \
    --output "results/$(basename "$file" .csv)_analysis.json"
done

# Train multiple models
for model in random_forest xgboost lstm; do
  neozork train \
    --model "$model" \
    --data training_data.csv \
    --target target \
    --output "models/${model}_model.joblib"
done
```

### Interactive Mode
```bash
# Start interactive session
neozork interactive

# Or run specific analysis interactively
neozork analyze --interactive --data data.csv
```

## Output Formats

### CSV Output
```bash
neozork analyze --data data.csv --format csv --output results.csv
```

### JSON Output
```bash
neozork analyze --data data.csv --format json --output results.json
```

### Parquet Output
```bash
neozork analyze --data data.csv --format parquet --output results.parquet
```

### HTML Output
```bash
neozork analyze --data data.csv --format html --output results.html
```

## Error Handling

### Common Errors
```bash
# File not found
Error: Input file 'nonexistent.csv' not found

# Invalid format
Error: Unsupported file format '.txt'. Supported formats: csv, json, parquet

# Insufficient data
Error: Insufficient data for analysis. Need at least 100 rows, got 50

# Invalid parameters
Error: Invalid period value '0'. Period must be at least 2
```

### Debug Mode
```bash
# Enable debug logging
export NEOZORK_LOG_LEVEL=DEBUG

# Run with verbose output
neozork analyze --data data.csv --verbose

# Check configuration
neozork --config-debug analyze --data data.csv
```

## Performance Optimization

### Parallel Processing
```bash
# Enable parallel processing
export NEOZORK_PARALLEL_WORKERS=4

# Process large datasets
neozork analyze --data large_dataset.csv --parallel --chunk-size 10000
```

### Caching
```bash
# Enable caching
export NEOZORK_CACHE_ENABLED=true
export NEOZORK_CACHE_DIR=/tmp/neozork_cache

# Use cached results
neozork analyze --data data.csv --use-cache
```

## Integration

### Shell Scripts
```bash
#!/bin/bash
# analyze_and_train.sh

INPUT_FILE="$1"
OUTPUT_DIR="$2"

if [ -z "$INPUT_FILE" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: $0 <input_file> <output_dir>"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Run analysis
neozork analyze \
    --data "$INPUT_FILE" \
    --indicators sma,rsi,macd \
    --output "$OUTPUT_DIR/analysis.json" \
    --plot \
    --save-plots

# Train model
neozork train \
    --model random_forest \
    --data "$INPUT_FILE" \
    --target target \
    --output "$OUTPUT_DIR/model.joblib"

echo "Analysis and training completed. Results saved to $OUTPUT_DIR"
```

### Python Integration
```python
import subprocess
import json

def run_analysis(data_file, indicators, output_file):
    """Run analysis using CLI."""
    cmd = [
        'neozork', 'analyze',
        '--data', data_file,
        '--indicators', indicators,
        '--output', output_file,
        '--format', 'json'
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        with open(output_file, 'r') as f:
            return json.load(f)
    else:
        raise RuntimeError(f"Analysis failed: {result.stderr}")

# Usage
results = run_analysis('data.csv', 'sma,rsi', 'results.json')
print(f"Analysis completed: {len(results)} indicators calculated")
```

## Troubleshooting

### Common Issues

#### Command Not Found
```bash
# Check if neozork is installed
which neozork

# Check PATH
echo $PATH

# Reinstall if needed
uv run pip install -e .
```

#### Permission Errors
```bash
# Check file permissions
ls -la data.csv

# Fix permissions if needed
chmod 644 data.csv

# Check directory permissions
ls -la output_dir/
```

#### Memory Issues
```bash
# Check available memory
free -h

# Use smaller chunk sizes
neozork analyze --data large_file.csv --chunk-size 5000

# Process in batches
split -l 10000 large_file.csv chunk_
for chunk in chunk_*; do
    neozork analyze --data "$chunk" --output "results_${chunk}.json"
done
```

### Getting Help
```bash
# General help
neozork --help

# Command-specific help
neozork analyze --help
neozork train --help

# Verbose help
neozork --help --verbose

# Check version
neozork --version
```

## Best Practices

### Command Organization
1. **Logical Order**: Group related operations together
2. **Consistent Naming**: Use consistent naming conventions
3. **Clear Options**: Provide clear, descriptive option names
4. **Helpful Messages**: Include helpful error and success messages

### Performance
1. **Batch Processing**: Process multiple files in batches
2. **Caching**: Use caching for repeated operations
3. **Parallel Processing**: Enable parallel processing for large datasets
4. **Chunking**: Process large files in chunks

### Error Handling
1. **Validation**: Validate inputs before processing
2. **Clear Messages**: Provide clear error messages
3. **Recovery**: Suggest recovery actions when possible
4. **Logging**: Log all operations for debugging

### Configuration
1. **Defaults**: Provide sensible defaults for all options
2. **Environment Variables**: Support environment variable overrides
3. **Configuration Files**: Use configuration files for complex settings
4. **Validation**: Validate configuration values

## Support

### Documentation
- **CLI Reference**: This guide
- **API Documentation**: Check `docs/api/` directory
- **Examples**: Review `examples/` directory
- **Configuration**: See `config.json` and `CONFIGURATION.md`

### Getting Help
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Ask questions on GitHub Discussions
- **Wiki**: Check project wiki for common problems
- **Community**: Engage with the development community
