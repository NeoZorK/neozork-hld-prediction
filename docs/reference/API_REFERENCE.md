# API Reference

## Overview

The Neozork HLD Prediction system provides a comprehensive API for financial analysis, machine learning, and data processing operations.

## Core Modules

### Core Module (`src.core`)

#### Base Classes
```python
from src.core.base import BaseComponent, DataProcessor, AnalysisEngine, MLModel

# BaseComponent - Foundation for all system components
class MyComponent(BaseComponent):
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
    
    def process(self, data):
        # Implementation
        pass

# DataProcessor - For data transformation operations
class MyDataProcessor(DataProcessor):
    def process_data(self, data):
        # Transform data
        return transformed_data

# AnalysisEngine - For analytical operations
class MyAnalysisEngine(AnalysisEngine):
    def analyze(self, data):
        # Perform analysis
        return analysis_result

# MLModel - For machine learning operations
class MyMLModel(MLModel):
    def train(self, data):
        # Train model
        pass
    
    def predict(self, data):
        # Make predictions
        return predictions
```

#### Configuration Management
```python
from src.core.config import Config

# Initialize configuration
config = Config()

# Get configuration values
cache_dir = config.get("data.cache_dir")
timeframe = config.get("analysis.default_timeframe", "1H")

# Set configuration values
config.set("data.cache_dir", "/new/cache/dir")
config.save()

# Access nested configuration
sma_period = config.get("analysis.indicators.sma.default_period")
```

#### Exception Handling
```python
from src.core.exceptions import (
    NeozorkError, DataError, ValidationError, 
    MLError, CLIError, ConfigError
)

try:
    # Operation that might fail
    result = process_data(data)
except DataError as e:
    logger.error(f"Data processing failed: {e}")
    # Handle data-specific error
except ValidationError as e:
    logger.error(f"Validation failed: {e}")
    # Handle validation error
except NeozorkError as e:
    logger.error(f"System error: {e}")
    # Handle general system error
```

#### Interfaces
```python
from src.core.interfaces import DataSource, DataSink, DataPipeline

# DataSource - For data retrieval
class MyDataSource(DataSource):
    def fetch_data(self, **kwargs):
        # Fetch data from source
        return data
    
    def is_available(self) -> bool:
        # Check if source is available
        return True
    
    def get_metadata(self) -> dict:
        # Return source metadata
        return {"type": "custom", "format": "csv"}

# DataSink - For data storage
class MyDataSink(DataSink):
    def store_data(self, data, **kwargs):
        # Store data to destination
        pass
    
    def is_writable(self) -> bool:
        # Check if sink is writable
        return True

# DataPipeline - For data processing workflows
class MyDataPipeline(DataPipeline):
    def __init__(self, steps: List[AnalysisStep]):
        self.steps = steps
    
    def execute(self, data):
        # Execute pipeline steps
        result = data
        for step in self.steps:
            result = step.process(result)
        return result
```

### Data Module (`src.data`)

#### Data Sources
```python
from src.data.sources.base import BaseDataSource, TimeSeriesDataSource

# BaseDataSource - Generic data source
class CSVDataSource(BaseDataSource):
    def __init__(self, file_path: str, config: dict):
        super().__init__("csv_source", config)
        self.file_path = file_path
    
    def fetch_data(self, **kwargs):
        import pandas as pd
        return pd.read_csv(self.file_path, **kwargs)
    
    def is_available(self) -> bool:
        import os
        return os.path.exists(self.file_path)

# TimeSeriesDataSource - For time-series data
class FinancialDataSource(TimeSeriesDataSource):
    def __init__(self, symbol: str, timeframe: str, config: dict):
        super().__init__("financial_source", config)
        self.symbol = symbol
        self.timeframe = timeframe
    
    def fetch_data(self, start_date=None, end_date=None, **kwargs):
        # Fetch financial data
        return self._fetch_ohlcv(start_date, end_date)
    
    def validate_timeframe(self, timeframe: str) -> bool:
        valid_timeframes = ["1m", "5m", "15m", "1h", "4h", "1d", "1w"]
        return timeframe in valid_timeframes
```

#### Data Processors
```python
from src.data.processors.base import BaseDataProcessor

class DataCleaner(BaseDataProcessor):
    def __init__(self, config: dict):
        super().__init__("data_cleaner", config)
    
    def process_data(self, data):
        # Remove duplicates
        data = data.drop_duplicates()
        
        # Handle missing values
        data = data.fillna(method='ffill')
        
        # Remove outliers
        data = self._remove_outliers(data)
        
        return data
    
    def _remove_outliers(self, data, threshold=3):
        # Remove outliers using IQR method
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR
        
        return data[(data >= lower_bound) & (data <= upper_bound)]
```

### Analysis Module (`src.analysis`)

#### Technical Indicators
```python
from src.analysis.indicators.base import BaseIndicator, TrendIndicator

# BaseIndicator - Foundation for all indicators
class CustomIndicator(BaseIndicator):
    def __init__(self, period: int, config: dict):
        super().__init__("custom_indicator", config)
        self.period = period
        self._validate_parameters()
    
    def _validate_parameters(self):
        if self.period < 2:
            raise ValueError("Period must be at least 2")
    
    def calculate(self, data):
        # Calculate indicator values
        return self._compute_indicator(data)
    
    def _compute_indicator(self, data):
        # Implementation
        pass

# TrendIndicator - For trend analysis
class MovingAverage(TrendIndicator):
    def __init__(self, period: int, config: dict):
        super().__init__("moving_average", config)
        self.period = period
    
    def calculate(self, data):
        return data.rolling(window=self.period).mean()
    
    def get_trend_direction(self, data) -> str:
        ma = self.calculate(data)
        current = ma.iloc[-1]
        previous = ma.iloc[-2]
        
        if current > previous:
            return "uptrend"
        elif current < previous:
            return "downtrend"
        else:
            return "sideways"
```

#### Statistical Analysis
```python
from src.analysis.statistics.base import StatisticalAnalyzer

class DescriptiveStats(StatisticalAnalyzer):
    def __init__(self, config: dict):
        super().__init__("descriptive_stats", config)
    
    def analyze(self, data):
        return {
            "mean": data.mean(),
            "median": data.median(),
            "std": data.std(),
            "min": data.min(),
            "max": data.max(),
            "skewness": data.skew(),
            "kurtosis": data.kurtosis()
        }
    
    def get_summary(self, data):
        stats = self.analyze(data)
        return f"Mean: {stats['mean']:.2f}, Std: {stats['std']:.2f}"
```

### ML Module (`src.ml`)

#### Machine Learning Models
```python
from src.ml.models.base import BaseMLModel
import joblib

class RandomForestModel(BaseMLModel):
    def __init__(self, config: dict):
        super().__init__("random_forest", config)
        self.model = None
        self.is_trained = False
    
    def _create_model(self):
        from sklearn.ensemble import RandomForestRegressor
        return RandomForestRegressor(
            n_estimators=self.config.get("n_estimators", 100),
            max_depth=self.config.get("max_depth", 10),
            random_state=self.config.get("random_state", 42)
        )
    
    def train(self, X, y):
        self.model = self._create_model()
        self.model.fit(X, y)
        self.is_trained = True
        return self.model
    
    def predict(self, X):
        if not self.is_trained:
            raise RuntimeError("Model must be trained before prediction")
        return self.model.predict(X)
    
    def evaluate(self, X, y):
        if not self.is_trained:
            raise RuntimeError("Model must be trained before evaluation")
        
        from sklearn.metrics import mean_squared_error, r2_score
        predictions = self.predict(X)
        
        return {
            "mse": mean_squared_error(y, predictions),
            "rmse": mean_squared_error(y, predictions, squared=False),
            "r2": r2_score(y, predictions)
        }
    
    def save_model(self, filepath: str):
        if self.model is not None:
            joblib.dump(self.model, filepath)
    
    def load_model(self, filepath: str):
        self.model = joblib.load(filepath)
        self.is_trained = True
```

#### Feature Engineering
```python
from src.ml.features.base import FeatureEngineer

class TechnicalFeatures(FeatureEngineer):
    def __init__(self, config: dict):
        super().__init__("technical_features", config)
    
    def create_features(self, data):
        features = {}
        
        # Price-based features
        features['returns'] = data['close'].pct_change()
        features['log_returns'] = np.log(data['close'] / data['close'].shift(1))
        
        # Volume features
        features['volume_ma'] = data['volume'].rolling(window=20).mean()
        features['volume_ratio'] = data['volume'] / features['volume_ma']
        
        # Technical indicators
        features['sma_20'] = data['close'].rolling(window=20).mean()
        features['sma_50'] = data['close'].rolling(window=50).mean()
        features['rsi'] = self._calculate_rsi(data['close'])
        
        return pd.DataFrame(features)
    
    def _calculate_rsi(self, prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
```

### CLI Module (`src.cli`)

#### Command Line Interface
```python
from src.cli.core.cli import CLI

# Initialize CLI
cli = CLI()

# Run CLI with arguments
cli.run(['--help'])
cli.run(['analyze', '--data', 'data.csv', '--indicators', 'sma,rsi'])

# Get help for specific command
cli.run(['analyze', '--help'])
```

#### Command Management
```python
from src.cli.core.command_manager import CommandManager

class CustomCommand(CommandManager):
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
    
    def add_arguments(self, parser):
        parser.add_argument('--input', required=True, help='Input file')
        parser.add_argument('--output', required=True, help='Output file')
    
    def execute(self, args):
        # Command implementation
        input_data = self._load_data(args.input)
        result = self._process_data(input_data)
        self._save_data(result, args.output)
    
    def _load_data(self, filepath):
        # Load data implementation
        pass
    
    def _process_data(self, data):
        # Process data implementation
        pass
    
    def _save_data(self, data, filepath):
        # Save data implementation
        pass
```

## Usage Examples

### Basic Data Analysis
```python
from src.data.sources.csv import CSVDataSource
from src.analysis.indicators.trend import MovingAverage
from src.core.config import Config

# Load configuration
config = Config()

# Create data source
data_source = CSVDataSource("data/ohlcv.csv", config._config)

# Fetch data
data = data_source.fetch_data()

# Calculate indicators
sma_20 = MovingAverage(20, config._config)
sma_50 = MovingAverage(50, config._config)

# Get trend analysis
trend_20 = sma_20.get_trend_direction(data['close'])
trend_50 = sma_50.get_trend_direction(data['close'])

print(f"20-period trend: {trend_20}")
print(f"50-period trend: {trend_50}")
```

### Machine Learning Pipeline
```python
from src.ml.models.regression import RandomForestModel
from src.ml.features.technical import TechnicalFeatures
from src.data.processors.cleaner import DataCleaner

# Initialize components
config = Config()
cleaner = DataCleaner(config._config)
feature_engineer = TechnicalFeatures(config._config)
model = RandomForestModel(config._config)

# Load and clean data
raw_data = data_source.fetch_data()
clean_data = cleaner.process_data(raw_data)

# Create features
features = feature_engineer.create_features(clean_data)
target = clean_data['close'].shift(-1).dropna()
features = features.iloc[:-1]  # Align with target

# Split data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    features, target, test_size=0.2, random_state=42
)

# Train model
model.train(X_train, y_train)

# Evaluate model
evaluation = model.evaluate(X_test, y_test)
print(f"Model performance: {evaluation}")

# Save model
model.save_model("models/random_forest.joblib")
```

### Custom Analysis Pipeline
```python
from src.analysis.pipeline import AnalysisPipeline
from src.analysis.steps import DataValidationStep, IndicatorCalculationStep, SignalGenerationStep

# Create analysis steps
validation_step = DataValidationStep(config._config)
indicator_step = IndicatorCalculationStep(config._config)
signal_step = SignalGenerationStep(config._config)

# Create pipeline
pipeline = AnalysisPipeline([validation_step, indicator_step, signal_step])

# Execute pipeline
result = pipeline.execute(data)

# Access results
signals = result['signals']
indicators = result['indicators']
validation_report = result['validation_report']
```

## Error Handling

### Custom Exceptions
```python
from src.core.exceptions import NeozorkError, DataError

class CustomAnalysisError(NeozorkError):
    """Custom error for analysis operations"""
    pass

class InsufficientDataError(DataError):
    """Error when insufficient data is available"""
    pass

# Usage
def analyze_data(data, min_periods=100):
    if len(data) < min_periods:
        raise InsufficientDataError(
            f"Need at least {min_periods} periods, got {len(data)}"
        )
    
    try:
        # Analysis logic
        result = perform_analysis(data)
        return result
    except Exception as e:
        raise CustomAnalysisError(f"Analysis failed: {e}") from e
```

### Error Recovery
```python
from src.core.exceptions import ValidationError, DataError

def robust_analysis(data):
    try:
        # Attempt analysis
        result = analyze_data(data)
        return result
    except ValidationError as e:
        logger.warning(f"Validation failed, attempting recovery: {e}")
        # Attempt to fix validation issues
        fixed_data = fix_validation_issues(data)
        return analyze_data(fixed_data)
    except DataError as e:
        logger.error(f"Data error, cannot recover: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise CustomAnalysisError(f"Analysis failed: {e}") from e
```

## Configuration Examples

### Environment-Specific Configuration
```python
import os
from src.core.config import Config

# Load base configuration
config = Config()

# Override based on environment
env = os.getenv("NEOZORK_ENV", "development")
if env == "production":
    config.set("logging.level", "WARNING")
    config.set("performance.caching.enabled", True)
    config.set("security.strict_mode", True)
elif env == "development":
    config.set("logging.level", "DEBUG")
    config.set("development.debug_mode", True)
    config.set("performance.caching.enabled", False)

# Save configuration
config.save()
```

### Dynamic Configuration Updates
```python
from src.core.config import Config

config = Config()

# Update configuration at runtime
config.set("analysis.default_timeframe", "4H")
config.set("ml.default_algorithm", "xgboost")

# Save changes
config.save()

# Reload configuration
config.reload()
```

## Best Practices

### 1. Component Design
- Inherit from appropriate base classes
- Implement all required abstract methods
- Use dependency injection for configuration
- Follow single responsibility principle

### 2. Error Handling
- Use specific exception types
- Provide meaningful error messages
- Implement proper error recovery
- Log errors with context

### 3. Configuration Management
- Use hierarchical configuration structure
- Provide sensible defaults
- Validate configuration values
- Support environment-specific overrides

### 4. Testing
- Write unit tests for all components
- Use mocking for external dependencies
- Test error conditions
- Maintain high test coverage

### 5. Performance
- Use lazy loading where appropriate
- Implement caching for expensive operations
- Use parallel processing for large datasets
- Monitor memory usage

## Integration Examples

### External Data Sources
```python
import yfinance as yf
from src.data.sources.base import BaseDataSource

class YahooFinanceSource(BaseDataSource):
    def __init__(self, symbol: str, config: dict):
        super().__init__("yahoo_finance", config)
        self.symbol = symbol
        self.ticker = yf.Ticker(symbol)
    
    def fetch_data(self, start_date=None, end_date=None, **kwargs):
        return self.ticker.history(
            start=start_date, 
            end=end_date, 
            **kwargs
        )
    
    def is_available(self) -> bool:
        try:
            info = self.ticker.info
            return info is not None
        except:
            return False
```

### Database Integration
```python
import sqlite3
from src.data.sources.base import BaseDataSource

class SQLiteSource(BaseDataSource):
    def __init__(self, db_path: str, table: str, config: dict):
        super().__init__("sqlite_source", config)
        self.db_path = db_path
        self.table = table
    
    def fetch_data(self, query=None, **kwargs):
        conn = sqlite3.connect(self.db_path)
        if query is None:
            query = f"SELECT * FROM {self.table}"
        
        data = pd.read_sql_query(query, conn)
        conn.close()
        return data
    
    def is_available(self) -> bool:
        try:
            conn = sqlite3.connect(self.db_path)
            conn.close()
            return True
        except:
            return False
```

## Troubleshooting

### Common Issues

#### 1. Import Errors
```python
# Check module structure
import sys
print(sys.path)

# Verify package installation
import src
print(src.__file__)
```

#### 2. Configuration Issues
```python
# Check configuration loading
from src.core.config import Config
config = Config()
print(f"Config loaded: {config._config}")
print(f"Config path: {config.config_path}")
```

#### 3. Data Processing Issues
```python
# Validate data structure
print(f"Data shape: {data.shape}")
print(f"Data columns: {data.columns}")
print(f"Data types: {data.dtypes}")
print(f"Missing values: {data.isnull().sum()}")
```

### Debug Mode
```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Enable component debug mode
config.set("development.debug_mode", True)
config.set("logging.level", "DEBUG")
```

## Support and Documentation

### Getting Help
- **API Documentation**: This reference guide
- **Code Examples**: Check `examples/` directory
- **Unit Tests**: Review test files for usage patterns
- **Issues**: GitHub Issues for bug reports

### Contributing
- **Code Standards**: Follow project coding standards
- **Documentation**: Update API documentation
- **Testing**: Add tests for new features
- **Examples**: Provide usage examples
