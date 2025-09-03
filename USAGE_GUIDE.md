# Usage Guide

## Overview

This guide provides comprehensive usage instructions for the Neozork HLD Prediction system, covering data analysis, machine learning, and data processing workflows.

## Quick Start

### Basic Analysis
```bash
# Analyze financial data with basic indicators
neozork analyze --data ohlcv.csv --indicators sma,rsi

# Train a simple ML model
neozork train --model random_forest --data features.csv --target price

# Make predictions
neozork predict --model model.joblib --data new_data.csv
```

### Data Processing
```bash
# Clean raw data
neozork data --action clean --input raw_data.csv --output clean_data.csv

# Convert data format
neozork data --action convert --input data.csv --output data.parquet

# Validate data quality
neozork data --action validate --input data.csv --config validation.json
```

## Financial Analysis

### Technical Indicators

#### Moving Averages
```bash
# Simple Moving Average (SMA)
neozork analyze \
  --data ohlcv.csv \
  --indicators sma \
  --period 20 \
  --output sma_analysis.json

# Exponential Moving Average (EMA)
neozork analyze \
  --data ohlcv.csv \
  --indicators ema \
  --period 12 \
  --output ema_analysis.json

# Multiple moving averages
neozork analyze \
  --data ohlcv.csv \
  --indicators sma,ema \
  --period 20,12 \
  --output moving_averages.json
```

#### Oscillators
```bash
# Relative Strength Index (RSI)
neozork analyze \
  --data ohlcv.csv \
  --indicators rsi \
  --period 14 \
  --output rsi_analysis.json

# Stochastic Oscillator
neozork analyze \
  --data ohlcv.csv \
  --indicators stoch \
  --period 14 \
  --output stoch_analysis.json

# MACD
neozork analyze \
  --data ohlcv.csv \
  --indicators macd \
  --period 12,26,9 \
  --output macd_analysis.json
```

#### Volatility Indicators
```bash
# Bollinger Bands
neozork analyze \
  --data ohlcv.csv \
  --indicators bollinger_bands \
  --period 20 \
  --output bollinger_analysis.json

# Average True Range (ATR)
neozork analyze \
  --data ohlcv.csv \
  --indicators atr \
  --period 14 \
  --output atr_analysis.json
```

### Pattern Recognition
```bash
# Candlestick patterns
neozork analyze \
  --data ohlcv.csv \
  --indicators candlestick_patterns \
  --output patterns.json

# Support and resistance levels
neozork analyze \
  --data ohlcv.csv \
  --indicators support_resistance \
  --period 20 \
  --output levels.json

# Trend analysis
neozork analyze \
  --data ohlcv.csv \
  --indicators trend_analysis \
  --period 50 \
  --output trend.json
```

### Statistical Analysis
```bash
# Descriptive statistics
neozork analyze \
  --data ohlcv.csv \
  --indicators descriptive_stats \
  --output stats.json

# Correlation analysis
neozork analyze \
  --data ohlcv.csv \
  --indicators correlation \
  --output correlation.json

# Volatility analysis
neozork analyze \
  --data ohlcv.csv \
  --indicators volatility \
  --period 20 \
  --output volatility.json
```

## Machine Learning

### Model Training

#### Regression Models
```bash
# Random Forest
neozork train \
  --model random_forest \
  --data training_data.csv \
  --target next_close \
  --features open,high,low,close,volume \
  --test-size 0.2 \
  --output rf_model.joblib

# XGBoost
neozork train \
  --model xgboost \
  --data training_data.csv \
  --target next_close \
  --features open,high,low,close,volume \
  --test-size 0.2 \
  --output xgb_model.joblib

# LSTM Neural Network
neozork train \
  --model lstm \
  --data time_series_data.csv \
  --target next_price \
  --features price,volume,technical_indicators \
  --test-size 0.2 \
  --output lstm_model.h5
```

#### Classification Models
```bash
# Binary classification (up/down)
neozork train \
  --model random_forest \
  --data classification_data.csv \
  --target direction \
  --features technical_indicators \
  --test-size 0.2 \
  --output direction_model.joblib

# Multi-class classification
neozork train \
  --model xgboost \
  --data multi_class_data.csv \
  --target category \
  --features features \
  --test-size 0.2 \
  --output category_model.joblib
```

### Feature Engineering
```bash
# Create technical features
neozork features \
  --action create \
  --input ohlcv.csv \
  --features sma,rsi,macd,volume_ma \
  --output features.csv

# Feature selection
neozork features \
  --action select \
  --input features.csv \
  --method correlation \
  --threshold 0.8 \
  --output selected_features.csv

# Feature scaling
neozork features \
  --action scale \
  --input features.csv \
  --method standard \
  --output scaled_features.csv
```

### Model Evaluation
```bash
# Evaluate model performance
neozork evaluate \
  --model model.joblib \
  --data test_data.csv \
  --target actual_values \
  --output evaluation.json

# Cross-validation
neozork evaluate \
  --model model.joblib \
  --data data.csv \
  --target target \
  --cv-folds 5 \
  --output cv_results.json

# Feature importance
neozork evaluate \
  --model model.joblib \
  --data data.csv \
  --target target \
  --feature-importance \
  --output importance.json
```

### Predictions
```bash
# Basic predictions
neozork predict \
  --model model.joblib \
  --data new_data.csv \
  --output predictions.csv

# Predictions with confidence
neozork predict \
  --model model.joblib \
  --data new_data.csv \
  --confidence \
  --output predictions_with_ci.csv

# Feature importance for predictions
neozork predict \
  --model model.joblib \
  --data new_data.csv \
  --explain \
  --output predictions_explained.json
```

## Data Processing

### Data Cleaning
```bash
# Remove duplicates
neozork data \
  --action clean \
  --input raw_data.csv \
  --clean-duplicates \
  --output clean_data.csv

# Handle missing values
neozork data \
  --action clean \
  --input raw_data.csv \
  --handle-missing forward_fill \
  --output clean_data.csv

# Remove outliers
neozork data \
  --action clean \
  --input raw_data.csv \
  --remove-outliers iqr \
  --output clean_data.csv

# Comprehensive cleaning
neozork data \
  --action clean \
  --input raw_data.csv \
  --clean-duplicates \
  --handle-missing forward_fill \
  --remove-outliers iqr \
  --output clean_data.csv
```

### Data Validation
```bash
# Schema validation
neozork data \
  --action validate \
  --input data.csv \
  --schema schema.json \
  --output validation_report.json

# Quality checks
neozork data \
  --action validate \
  --input data.csv \
  --quality-checks \
  --output quality_report.json

# Custom validation rules
neozork data \
  --action validate \
  --input data.csv \
  --rules validation_rules.json \
  --output validation_report.json
```

### Data Transformation
```bash
# Convert timezone
neozork data \
  --action transform \
  --input data.csv \
  --timezone UTC \
  --output utc_data.csv

# Resample data
neozork data \
  --action transform \
  --input data.csv \
  --resample 1H \
  --output hourly_data.csv

# Normalize data
neozork data \
  --action transform \
  --input data.csv \
  --normalize minmax \
  --output normalized_data.csv
```

### Data Export
```bash
# Export to CSV
neozork export \
  --data results.json \
  --format csv \
  --output results.csv

# Export to Parquet
neozork export \
  --data results.json \
  --format parquet \
  --output results.parquet

# Export to Excel
neozork export \
  --data results.json \
  --format xlsx \
  --output results.xlsx

# Export with custom formatting
neozork export \
  --data results.json \
  --format html \
  --template custom_template.html \
  --output results.html
```

## Advanced Workflows

### End-to-End Analysis
```bash
#!/bin/bash
# complete_analysis.sh

INPUT_FILE="$1"
OUTPUT_DIR="$2"

if [ -z "$INPUT_FILE" ] || [ -z "$OUTPUT_DIR" ]; then
    echo "Usage: $0 <input_file> <output_dir>"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "Starting complete analysis workflow..."

# 1. Data cleaning
echo "Step 1: Cleaning data..."
neozork data \
    --action clean \
    --input "$INPUT_FILE" \
    --clean-duplicates \
    --handle-missing forward_fill \
    --remove-outliers iqr \
    --output "$OUTPUT_DIR/clean_data.csv"

# 2. Feature engineering
echo "Step 2: Creating features..."
neozork features \
    --action create \
    --input "$OUTPUT_DIR/clean_data.csv" \
    --features sma,rsi,macd,bollinger_bands,volume_ma \
    --output "$OUTPUT_DIR/features.csv"

# 3. Technical analysis
echo "Step 3: Technical analysis..."
neozork analyze \
    --data "$OUTPUT_DIR/features.csv" \
    --indicators sma,rsi,macd,bollinger_bands \
    --timeframe 1H \
    --plot \
    --save-plots \
    --output "$OUTPUT_DIR/technical_analysis.json"

# 4. Train ML model
echo "Step 4: Training ML model..."
neozork train \
    --model random_forest \
    --data "$OUTPUT_DIR/features.csv" \
    --target next_close \
    --features sma_20,rsi_14,macd,bollinger_upper,bollinger_lower,volume_ma_20 \
    --test-size 0.2 \
    --output "$OUTPUT_DIR/price_predictor.joblib"

# 5. Model evaluation
echo "Step 5: Evaluating model..."
neozork evaluate \
    --model "$OUTPUT_DIR/price_predictor.joblib" \
    --data "$OUTPUT_DIR/features.csv" \
    --target next_close \
    --output "$OUTPUT_DIR/model_evaluation.json"

echo "Complete analysis workflow finished!"
echo "Results saved to: $OUTPUT_DIR"
```

### Batch Processing
```bash
#!/bin/bash
# batch_process.sh

DATA_DIR="data/raw"
OUTPUT_DIR="results/batch"
INDICATORS="sma,rsi,macd"

# Process all CSV files in data directory
for file in "$DATA_DIR"/*.csv; do
    if [ -f "$file" ]; then
        filename=$(basename "$file" .csv)
        echo "Processing $filename..."
        
        # Create output subdirectory
        mkdir -p "$OUTPUT_DIR/$filename"
        
        # Run analysis
        neozork analyze \
            --data "$file" \
            --indicators "$INDICATORS" \
            --output "$OUTPUT_DIR/$filename/analysis.json" \
            --plot \
            --save-plots
        
        echo "Completed $filename"
    fi
done

echo "Batch processing completed!"
```

### Real-time Analysis
```bash
#!/bin/bash
# realtime_analysis.sh

WATCH_DIR="data/realtime"
OUTPUT_DIR="results/realtime"
MODEL_PATH="models/price_predictor.joblib"

# Monitor directory for new files
inotifywait -m -e create,moved_to "$WATCH_DIR" |
while read path action file; do
    if [[ "$file" =~ \.csv$ ]]; then
        echo "New file detected: $file"
        
        # Wait for file to be fully written
        sleep 2
        
        # Run real-time analysis
        neozork analyze \
            --data "$path$file" \
            --indicators sma,rsi,macd \
            --output "$OUTPUT_DIR/$(basename "$file" .csv)_analysis.json"
        
        # Make predictions if model exists
        if [ -f "$MODEL_PATH" ]; then
            neozork predict \
                --model "$MODEL_PATH" \
                --data "$path$file" \
                --confidence \
                --output "$OUTPUT_DIR/$(basename "$file" .csv)_predictions.json"
        fi
        
        echo "Analysis completed for $file"
    fi
done
```

## Interactive Mode

### Start Interactive Session
```bash
# Start interactive mode
neozork interactive

# Or start with specific data
neozork interactive --data data.csv
```

### Interactive Commands
```python
# In interactive mode
>>> help()
Available commands:
  analyze(data, indicators, **kwargs) - Run technical analysis
  train(model, data, target, **kwargs) - Train ML model
  predict(model, data, **kwargs) - Make predictions
  clean(data, **kwargs) - Clean data
  features(data, **kwargs) - Create features

>>> # Load data
>>> data = load_data('ohlcv.csv')

>>> # Run analysis
>>> results = analyze(data, indicators=['sma', 'rsi'], period=20)

>>> # View results
>>> print(results)

>>> # Plot results
>>> plot_results(results)

>>> # Save results
>>> save_results(results, 'analysis_results.json')
```

## Configuration

### Custom Configuration
```json
{
  "analysis": {
    "default_timeframe": "1H",
    "max_lookback_periods": 1000,
    "confidence_threshold": 0.8,
    "indicators": {
      "sma": {
        "default_period": 20,
        "min_period": 2,
        "max_period": 500
      },
      "rsi": {
        "default_period": 14,
        "overbought_threshold": 70,
        "oversold_threshold": 30
      }
    }
  },
  "ml": {
    "default_algorithm": "random_forest",
    "cross_validation_folds": 5,
    "test_size": 0.2,
    "random_state": 42
  }
}
```

### Environment-Specific Configuration
```bash
# Development environment
export NEOZORK_ENV=development
export NEOZORK_LOG_LEVEL=DEBUG
export NEOZORK_DEBUG_MODE=true

# Production environment
export NEOZORK_ENV=production
export NEOZORK_LOG_LEVEL=WARNING
export NEOZORK_DEBUG_MODE=false

# Testing environment
export NEOZORK_ENV=testing
export NEOZORK_LOG_LEVEL=INFO
export NEOZORK_TEST_MODE=true
```

## Performance Optimization

### Parallel Processing
```bash
# Enable parallel processing
export NEOZORK_PARALLEL_WORKERS=4

# Process large datasets in parallel
neozork analyze \
    --data large_dataset.csv \
    --indicators sma,rsi,macd \
    --parallel \
    --chunk-size 10000 \
    --output parallel_results.json
```

### Caching
```bash
# Enable caching
export NEOZORK_CACHE_ENABLED=true
export NEOZORK_CACHE_DIR=/tmp/neozork_cache

# Use cached results
neozork analyze \
    --data data.csv \
    --indicators sma,rsi \
    --use-cache \
    --output cached_results.json
```

### Memory Management
```bash
# Set memory limits
export NEOZORK_MEMORY_LIMIT_MB=2048

# Process in chunks
neozork analyze \
    --data large_file.csv \
    --chunk-size 5000 \
    --memory-efficient \
    --output chunked_results.json
```

## Output and Visualization

### Plot Generation
```bash
# Generate plots
neozork analyze \
    --data data.csv \
    --indicators sma,rsi \
    --plot \
    --output analysis.json

# Save plots to files
neozork analyze \
    --data data.csv \
    --indicators sma,rsi \
    --plot \
    --save-plots \
    --plot-dir plots/ \
    --output analysis.json
```

### Report Generation
```bash
# Generate HTML report
neozork report \
    --data analysis.json \
    --template default \
    --output report.html

# Generate PDF report
neozork report \
    --data analysis.json \
    --template custom \
    --format pdf \
    --output report.pdf

# Generate custom report
neozork report \
    --data analysis.json \
    --template custom_template.html \
    --config report_config.json \
    --output custom_report.html
```

## Integration Examples

### Python Script Integration
```python
import subprocess
import json
import pandas as pd

def run_neozork_analysis(data_file, indicators, output_file):
    """Run Neozork analysis from Python."""
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

def run_neozork_training(data_file, model_type, target, features, output_file):
    """Run Neozork training from Python."""
    cmd = [
        'neozork', 'train',
        '--model', model_type,
        '--data', data_file,
        '--target', target,
        '--features', features,
        '--output', output_file
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"Training failed: {result.stderr}")

# Usage example
if __name__ == "__main__":
    # Run analysis
    results = run_neozork_analysis(
        'ohlcv.csv', 
        'sma,rsi,macd', 
        'analysis_results.json'
    )
    print(f"Analysis completed: {len(results)} indicators calculated")
    
    # Run training
    run_neozork_training(
        'features.csv',
        'random_forest',
        'next_close',
        'sma_20,rsi_14,macd',
        'price_model.joblib'
    )
    print("Training completed")
```

### Shell Script Integration
```bash
#!/bin/bash
# trading_strategy.sh

# Configuration
DATA_FILE="data/ohlcv.csv"
MODEL_FILE="models/price_predictor.joblib"
OUTPUT_DIR="results/trading"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# 1. Technical Analysis
echo "Running technical analysis..."
neozork analyze \
    --data "$DATA_FILE" \
    --indicators sma,rsi,macd,bollinger_bands \
    --timeframe 1H \
    --plot \
    --save-plots \
    --output "$OUTPUT_DIR/technical_analysis.json"

# 2. Generate Trading Signals
echo "Generating trading signals..."
neozork signals \
    --data "$OUTPUT_DIR/technical_analysis.json" \
    --strategy crossover \
    --indicators sma_20,sma_50 \
    --output "$OUTPUT_DIR/signals.json"

# 3. Make Price Predictions
echo "Making price predictions..."
neozork predict \
    --model "$MODEL_FILE" \
    --data "$DATA_FILE" \
    --confidence \
    --output "$OUTPUT_DIR/predictions.json"

# 4. Generate Trading Report
echo "Generating trading report..."
neozork report \
    --data "$OUTPUT_DIR/technical_analysis.json" \
    --signals "$OUTPUT_DIR/signals.json" \
    --predictions "$OUTPUT_DIR/predictions.json" \
    --template trading \
    --output "$OUTPUT_DIR/trading_report.html"

echo "Trading strategy analysis completed!"
echo "Results saved to: $OUTPUT_DIR"
```

## Best Practices

### Data Management
1. **Backup Data**: Always backup original data before processing
2. **Version Control**: Use version control for configuration files
3. **Data Validation**: Validate data before analysis
4. **Clean Data**: Clean data thoroughly before ML training

### Analysis Workflow
1. **Start Simple**: Begin with basic indicators before complex analysis
2. **Validate Results**: Always validate analysis results
3. **Document Process**: Document your analysis workflow
4. **Iterate**: Refine analysis based on results

### Machine Learning
1. **Feature Engineering**: Create meaningful features
2. **Cross-Validation**: Use cross-validation for reliable results
3. **Hyperparameter Tuning**: Optimize model parameters
4. **Model Validation**: Validate models on unseen data

### Performance
1. **Use Caching**: Enable caching for repeated operations
2. **Parallel Processing**: Use parallel processing for large datasets
3. **Memory Management**: Monitor memory usage
4. **Batch Processing**: Process data in batches when possible

## Troubleshooting

### Common Issues

#### Analysis Errors
```bash
# Check data format
file data.csv

# Validate data structure
neozork data --action validate --input data.csv

# Check for missing values
neozork data --action inspect --input data.csv
```

#### Training Errors
```bash
# Check feature columns
head -1 features.csv

# Verify target column exists
grep "target_column" features.csv

# Check data quality
neozork data --action validate --input features.csv
```

#### Performance Issues
```bash
# Check system resources
free -h
df -h

# Use smaller datasets for testing
neozork analyze --data small_sample.csv --indicators sma

# Enable verbose output for debugging
neozork analyze --data data.csv --indicators sma --verbose
```

### Getting Help
```bash
# General help
neozork --help

# Command-specific help
neozork analyze --help
neozork train --help

# Check version
neozork --version

# Enable debug mode
export NEOZORK_LOG_LEVEL=DEBUG
neozork analyze --data data.csv --indicators sma
```

## Support and Resources

### Documentation
- **Usage Guide**: This guide
- **CLI Reference**: Check `CLI_GUIDE.md`
- **API Documentation**: Check `API_REFERENCE.md`
- **Examples**: Review `examples/` directory

### Getting Help
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Ask questions on GitHub Discussions
- **Wiki**: Check project wiki for common problems
- **Community**: Engage with the development community
