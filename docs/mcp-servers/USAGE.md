# MCP Servers Usage Guide

📖 **Usage Examples and API Documentation**

## 🚀 Basic Examples

### Financial Data Analysis

```python
# Autocompletion for financial symbols and timeframes
def analyze_market_data():
    symbol = "BTCUSD"  # Available symbols: BTCUSD, GBPUSD, EURUSD, USDJPY
    timeframe = "D1"   # Available timeframes: D1, H1, M15, M5, M1
    
    # Load data with autocompletion
    data = load_financial_data(symbol, timeframe)
    
    # Calculate indicators with autocompletion
    sma_20 = calculate_sma(data, period=20)
    ema_50 = calculate_ema(data, period=50)
    rsi_14 = calculate_rsi(data, period=14)
    
    return data, sma_20, ema_50, rsi_14
```

### Technical Indicators

```python
# GitHub Copilot will suggest based on project context
def calculate_technical_indicators(data):
    """
    Calculate comprehensive technical indicators
    Copilot will suggest: SMA, EMA, RSI, MACD, Bollinger Bands, ATR
    """
    indicators = {}
    
    # Simple moving averages
    indicators['sma_20'] = data['close'].rolling(window=20).mean()
    indicators['sma_50'] = data['close'].rolling(window=50).mean()
    
    # Exponential moving averages
    indicators['ema_12'] = data['close'].ewm(span=12, adjust=False).mean()
    indicators['ema_26'] = data['close'].ewm(span=26, adjust=False).mean()
    
    # RSI
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    indicators['rsi'] = 100 - (100 / (1 + rs))
    
    # MACD
    indicators['macd'] = indicators['ema_12'] - indicators['ema_26']
    indicators['macd_signal'] = indicators['macd'].ewm(span=9, adjust=False).mean()
    indicators['macd_histogram'] = indicators['macd'] - indicators['macd_signal']
    
    return indicators
```

### Code Snippets

```python
# Type 'load_data' and get autocompletion
load_financial_data  # Expands to: load_financial_data(symbol, timeframe)

# Type 'calculate_indicators' and get autocompletion
calculate_indicators  # Expands to: calculate_indicators(data)

# Type 'plot_analysis' and get autocompletion
plot_analysis  # Expands to: plot_analysis(data, indicators)

# Type 'backtest_strategy' and get autocompletion
backtest_strategy  # Expands to: backtest_strategy(data, strategy_params)
```

### GitHub Copilot Integration

```python
# Copilot will suggest based on project context
def create_trading_strategy():
    """
    Create a complete trading strategy
    Copilot will suggest: data loading, indicator calculation, signal generation
    """
    # Load data (Copilot will suggest: BTCUSD, D1)
    data = load_financial_data("BTCUSD", "D1")
    
    # Calculate indicators (Copilot will suggest: SMA, RSI, MACD)
    indicators = calculate_technical_indicators(data)
    
    # Generate signals (Copilot will suggest: crossover logic)
    signals = generate_trading_signals(data, indicators)
    
    # Backtest strategy (Copilot will suggest: performance metrics)
    results = backtest_strategy(data, signals)
    
    return results
```

## 🔄 Usage Patterns

### Data Loading Pattern

```python
def load_and_prepare_data(symbol: str, timeframe: str):
    """
    Standard pattern for loading and preparing financial data
    """
    # 1. Load raw data
    raw_data = load_financial_data(symbol, timeframe)
    
    # 2. Check data quality
    if not check_data_quality(raw_data):
        raise ValueError(f"Poor data quality for {symbol} {timeframe}")
    
    # 3. Preprocess data
    processed_data = preprocess_data(raw_data)
    
    # 4. Feature engineering
    features = engineer_features(processed_data)
    
    return processed_data, features
```

### Indicator Calculation Pattern

```python
def calculate_all_indicators(data):
    """
    Standard pattern for calculating technical indicators
    """
    indicators = {}
    
    # Trend indicators
    indicators.update(calculate_trend_indicators(data))
    
    # Momentum indicators
    indicators.update(calculate_momentum_indicators(data))
    
    # Volatility indicators
    indicators.update(calculate_volatility_indicators(data))
    
    # Volume indicators
    indicators.update(calculate_volume_indicators(data))
    
    return indicators
```

### Visualization Pattern

```python
def create_comprehensive_chart(data, indicators):
    """
    Standard pattern for creating comprehensive charts
    """
    # Create figure with subplots
    fig, axes = plt.subplots(3, 1, figsize=(15, 12))
    
    # Price chart with indicators
    plot_price_chart(axes[0], data, indicators)
    
    # Volume chart
    plot_volume_chart(axes[1], data)
    
    # Indicator charts
    plot_indicator_charts(axes[2], indicators)
    
    plt.tight_layout()
    return fig
```

### Backtesting Pattern

```python
def backtest_trading_strategy(data, strategy_params):
    """
    Standard pattern for backtesting trading strategies
    """
    # 1. Generate signals
    signals = generate_signals(data, strategy_params)
    
    # 2. Calculate positions
    positions = calculate_positions(signals)
    
    # 3. Calculate returns
    returns = calculate_returns(data, positions)
    
    # 4. Calculate performance metrics
    metrics = calculate_performance_metrics(returns)
    
    # 5. Generate report
    report = generate_backtest_report(metrics, strategy_params)
    
    return report
```

## 🧪 Testing

### Unit Tests

```python
import pytest
from pycharm_github_copilot_mcp import PyCharmGitHubCopilotMCPServer

class TestPyCharmMCPServer:
    def test_initialization(self):
        """Test server initialization"""
        server = PyCharmGitHubCopilotMCPServer()
        assert server.running == True
        assert len(server.handlers) > 0
    
    def test_completion(self):
        """Test code autocompletion"""
        server = PyCharmGitHubCopilotMCPServer()
        
        # Test financial data autocompletion
        completions = server._get_financial_completions()
        assert len(completions) > 0
        
        # Test indicator autocompletion
        indicator_completions = server._get_indicator_completions()
        assert len(indicator_completions) > 0
    
    def test_github_copilot_integration(self):
        """Test GitHub Copilot integration"""
        server = PyCharmGitHubCopilotMCPServer()
        
        # Test Copilot suggestions
        context = "financial data analysis"
        suggestions = server._handle_copilot_suggestions(None, {"context": context})
        assert "suggestions" in suggestions
```

### Integration Tests

```python
def test_full_workflow():
    """Test complete workflow"""
    # 1. Start server
    server = PyCharmGitHubCopilotMCPServer()
    
    # 2. Load data
    data = load_financial_data("BTCUSD", "D1")
    assert data is not None
    
    # 3. Calculate indicators
    indicators = calculate_technical_indicators(data)
    assert len(indicators) > 0
    
    # 4. Generate signals
    signals = generate_trading_signals(data, indicators)
    assert signals is not None
    
    # 5. Backtest
    results = backtest_strategy(data, signals)
    assert results is not None
```

## 📊 Performance

### Benchmarking

```python
import time
import psutil

def benchmark_server_performance():
    """Benchmark MCP server performance"""
    start_time = time.time()
    
    # Start server
    server = PyCharmGitHubCopilotMCPServer()
    startup_time = time.time() - start_time
    
    # Test autocompletion speed
    completion_start = time.time()
    completions = server._get_project_completions()
    completion_time = time.time() - completion_start
    
    # Memory usage
    process = psutil.Process()
    memory_usage = process.memory_info().rss / 1024 / 1024  # MB
    
    return {
        "startup_time": startup_time,
        "completion_time": completion_time,
        "memory_usage_mb": memory_usage,
        "completions_count": len(completions)
    }
```

### Load Testing

```python
def load_test_server():
    """Load testing MCP server"""
    server = PyCharmGitHubCopilotMCPServer()
    
    # Simulate multiple concurrent requests
    import threading
    import queue
    
    results = queue.Queue()
    
    def make_request():
        start = time.time()
        completions = server._get_project_completions()
        end = time.time()
        results.put(end - start)
    
    # Create multiple threads
    threads = []
    for i in range(10):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()
    
    # Wait for completion
    for thread in threads:
        thread.join()
    
    # Collect results
    response_times = []
    while not results.empty():
        response_times.append(results.get())
    
    return {
        "avg_response_time": sum(response_times) / len(response_times),
        "max_response_time": max(response_times),
        "min_response_time": min(response_times)
    }
```

## 🔧 Advanced Usage

### Custom Indicators

```python
# Define custom indicator
def calculate_custom_indicator(data, params):
    """
    Custom technical indicator
    """
    # Implementation
    result = custom_calculation(data, params)
    return result

# Register with MCP server
CUSTOM_INDICATORS = {
    "custom_indicator": {
        "function": calculate_custom_indicator,
        "parameters": ["data", "param1", "param2"],
        "description": "Custom technical indicator"
    }
}
```

### Custom Snippets

```python
# Define custom snippets
CUSTOM_SNIPPETS = {
    "ml_pipeline": {
        "prefix": "ml_pipeline",
        "body": [
            "def create_ml_pipeline():",
            "    # Load data",
            "    data = load_financial_data(symbol, timeframe)",
            "    ",
            "    # Feature engineering",
            "    features = engineer_features(data)",
            "    ",
            "    # Train model",
            "    model = train_model(features, target)",
            "    ",
            "    # Evaluate model",
            "    score = evaluate_model(model, test_features, test_target)",
            "    ",
            "    return model, score"
        ],
        "description": "Complete ML pipeline"
    }
}
```

### External API Integration

```python
def integrate_external_data():
    """
    Integration with external financial data APIs
    """
    # Alpha Vantage API
    alpha_vantage_data = fetch_alpha_vantage_data(symbol, api_key)
    
    # Yahoo Finance API
    yahoo_data = fetch_yahoo_finance_data(symbol)
    
    # Polygon API
    polygon_data = fetch_polygon_data(symbol, api_key)
    
    # Combine data sources
    combined_data = combine_data_sources([
        alpha_vantage_data,
        yahoo_data,
        polygon_data
    ])
    
    return combined_data
```

### Real-time Data Processing

```python
def real_time_analysis():
    """
    Real-time financial data analysis
    """
    # Setup real-time data stream
    stream = setup_real_time_stream(symbols)
    
    # Process incoming data
    for data_point in stream:
        # Update indicators
        updated_indicators = update_indicators(data_point)
        
        # Generate signals
        signals = generate_real_time_signals(updated_indicators)
        
        # Execute trades if needed
        if signals['action'] == 'buy':
            execute_buy_order(signals['symbol'], signals['quantity'])
        elif signals['action'] == 'sell':
            execute_sell_order(signals['symbol'], signals['quantity'])
```

### Machine Learning Integration

```python
def ml_prediction_pipeline():
    """
    Machine learning prediction pipeline
    """
    # Load historical data
    historical_data = load_historical_data(symbol, timeframe)
    
    # Feature engineering
    features = create_ml_features(historical_data)
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(features)
    
    # Train multiple models
    models = {
        'random_forest': train_random_forest(X_train, y_train),
        'xgboost': train_xgboost(X_train, y_train),
        'lstm': train_lstm(X_train, y_train),
        'transformer': train_transformer(X_train, y_train)
    }
    
    # Ensemble predictions
    predictions = ensemble_predict(models, X_test)
    
    # Evaluate performance
    performance = evaluate_predictions(predictions, y_test)
    
    return models, predictions, performance
```

## 📚 API Reference

### Core Methods

- `initialize(request_id, params)`: Server initialization
- `handle_completion(request_id, params)`: Handle autocompletion
- `handle_copilot_suggestions(request_id, params)`: Handle Copilot suggestions
- `handle_financial_data(request_id, params)`: Handle financial data requests

### Data Structures

- `CompletionItem`: Code autocompletion item
- `ProjectFile`: Project file information
- `FinancialData`: Financial data metadata

## 🔍 Debug Commands

```bash
# Run with debugging
LOG_LEVEL=DEBUG python pycharm_github_copilot_mcp.py

# Test functionality
python scripts/run_cursor_mcp.py --test

# Check performance
python scripts/run_cursor_mcp.py --performance

# Generate report
python scripts/run_cursor_mcp.py --test --performance --report
```

## 📚 Additional Resources

- [README.md](README.md) - Main documentation
- [SETUP.md](SETUP.md) - Setup and configuration
- [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) - Change history

---

**Usage Guide** - Complete guide to using MCP servers 