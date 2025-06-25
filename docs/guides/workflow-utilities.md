# Workflow and Utilities Guide

Complete guide to workflow management and utility functions in the Neozork HLD Prediction project.

## Overview

The workflow and utilities modules provide automation, workflow management, and utility functions for data processing, analysis, and system operations.

## Workflow Management

### 1. Workflow Engine (`workflow.py`)

Automated workflow orchestration and management.

#### Features
- **Pipeline orchestration** - Automated data processing pipelines
- **Task scheduling** - Scheduled task execution
- **Error handling** - Robust error management and recovery
- **Progress tracking** - Real-time progress monitoring
- **Dependency management** - Task dependency resolution
- **Parallel execution** - Multi-threaded task execution

#### Usage Example

```python
from src.workflow.workflow import WorkflowEngine

# Initialize workflow engine
workflow = WorkflowEngine()

# Define workflow steps
workflow.add_step(
    name='data_fetch',
    function=fetch_data,
    params={'symbol': 'AAPL', 'period': '1y'},
    dependencies=[]
)

workflow.add_step(
    name='indicator_calculation',
    function=calculate_indicators,
    params={'indicators': ['rsi', 'macd']},
    dependencies=['data_fetch']
)

workflow.add_step(
    name='analysis',
    function=run_analysis,
    params={'analysis_type': 'comprehensive'},
    dependencies=['indicator_calculation']
)

workflow.add_step(
    name='export',
    function=export_results,
    params={'formats': ['csv', 'json']},
    dependencies=['analysis']
)

# Execute workflow
results = workflow.execute(parallel=True, max_workers=4)
```

#### Workflow Configuration

```python
# Workflow configuration
config = {
    'parallel': True,
    'max_workers': 4,
    'retry_attempts': 3,
    'retry_delay': 5,
    'timeout': 300,
    'log_level': 'INFO',
    'save_intermediate': True
}

workflow = WorkflowEngine(config=config)
```

### 2. Reporting System (`reporting.py`)

Automated report generation and distribution.

#### Features
- **Automated reporting** - Scheduled report generation
- **Multiple formats** - HTML, PDF, email reports
- **Customizable templates** - Custom report templates
- **Distribution** - Email, web, file system distribution
- **Alerting** - Automated alerts and notifications
- **Archiving** - Report archiving and versioning

#### Usage Example

```python
from src.workflow.reporting import ReportingSystem

# Initialize reporting system
reporter = ReportingSystem()

# Generate daily report
daily_report = reporter.generate_daily_report(
    symbols=['AAPL', 'GOOGL', 'MSFT'],
    analysis_types=['technical', 'fundamental', 'sentiment'],
    template='daily_summary',
    output_formats=['html', 'pdf']
)

# Schedule weekly report
reporter.schedule_report(
    name='weekly_analysis',
    schedule='weekly',
    day_of_week='friday',
    time='09:00',
    symbols=['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'],
    template='weekly_comprehensive'
)

# Send alert report
reporter.send_alert_report(
    condition='price_change > 0.05',
    symbols=['AAPL'],
    template='alert_notification',
    recipients=['analyst@company.com']
)
```

## Utility Functions

### 1. Point Size Determination (`point_size_determination.py`)

Automatic point size calculation for different instruments.

#### Features
- **Automatic detection** - Detect appropriate point size
- **Instrument-specific** - Different rules for different instruments
- **Market-aware** - Consider market conditions
- **Validation** - Validate calculated point sizes
- **Caching** - Cache results for performance

#### Usage Example

```python
from src.utils.point_size_determination import PointSizeDeterminer

# Initialize determiner
determiner = PointSizeDeterminer()

# Determine point size for stock
point_size = determiner.determine_point_size(
    symbol='AAPL',
    instrument_type='stock',
    price_range=(100, 200)
)

# Determine point size for forex
forex_point_size = determiner.determine_point_size(
    symbol='EURUSD',
    instrument_type='forex',
    price_range=(1.0, 1.5)
)

# Determine point size for crypto
crypto_point_size = determiner.determine_point_size(
    symbol='BTCUSDT',
    instrument_type='crypto',
    price_range=(40000, 50000)
)
```

#### Point Size Rules

```python
# Point size rules by instrument type
point_size_rules = {
    'stock': {
        'price_0_10': 0.01,
        'price_10_100': 0.01,
        'price_100_1000': 0.01,
        'price_1000_plus': 0.01
    },
    'forex': {
        'default': 0.00001
    },
    'crypto': {
        'price_0_1': 0.00001,
        'price_1_100': 0.01,
        'price_100_10000': 0.01,
        'price_10000_plus': 0.1
    }
}
```

### 2. Docker Browser (`docker_browser.py`)

Docker container management and browser automation.

#### Features
- **Container management** - Start, stop, monitor containers
- **Browser automation** - Automated browser operations
- **Screenshot capture** - Automated screenshot capture
- **Web scraping** - Automated web data extraction
- **Container orchestration** - Multi-container management

#### Usage Example

```python
from src.utils.docker_browser import DockerBrowser

# Initialize browser
browser = DockerBrowser()

# Start container
container = browser.start_container(
    image='selenium/standalone-chrome',
    ports={'4444': 4444, '7900': 7900},
    environment={'SE_NODE_MAX_SESSIONS': 4}
)

# Navigate and capture screenshot
browser.navigate('https://finance.yahoo.com/quote/AAPL')
screenshot = browser.capture_screenshot('aapl_chart.png')

# Extract data
data = browser.extract_data(
    selectors={
        'price': '.Fw(b).Fz(36px)',
        'change': '.Fw(500).Pstart(10px).Fz(24px)',
        'volume': '[data-test="qsp-volume"]'
    }
)

# Stop container
browser.stop_container(container)
```

### 3. General Utilities (`utils.py`)

General utility functions for common operations.

#### Features
- **File operations** - File handling utilities
- **Data validation** - Data validation functions
- **Format conversion** - Data format conversion
- **Time utilities** - Time and date utilities
- **Configuration management** - Configuration utilities

#### Usage Example

```python
from src.utils.utils import (
    validate_data, convert_format, 
    get_timestamp, load_config, save_config
)

# Validate data
is_valid = validate_data(
    data=price_data,
    required_columns=['open', 'high', 'low', 'close', 'volume'],
    data_types={'open': float, 'volume': int}
)

# Convert data format
converted_data = convert_format(
    data=price_data,
    from_format='csv',
    to_format='parquet',
    compression='snappy'
)

# Get timestamp
timestamp = get_timestamp(format='%Y%m%d_%H%M%S')

# Load configuration
config = load_config('config.yaml')

# Save configuration
save_config(config, 'config_backup.yaml')
```

## Common Utilities

### 1. File Operations

```python
from src.utils.utils import (
    ensure_directory, safe_filename, 
    backup_file, cleanup_old_files
)

# Ensure directory exists
ensure_directory('data/export/')

# Create safe filename
safe_name = safe_filename('AAPL Analysis Report (2024).csv')
# Result: 'AAPL_Analysis_Report_2024.csv'

# Backup file
backup_file('data/important.csv', backup_dir='backups/')

# Cleanup old files
cleanup_old_files(
    directory='logs/',
    pattern='*.log',
    days_old=30
)
```

### 2. Data Validation

```python
from src.utils.utils import (
    validate_ohlcv, validate_timestamp, 
    validate_numeric_range, validate_file_exists
)

# Validate OHLCV data
ohlcv_valid = validate_ohlcv(
    data=price_data,
    required_columns=['open', 'high', 'low', 'close', 'volume']
)

# Validate timestamp
timestamp_valid = validate_timestamp(
    timestamp='2024-12-01 09:30:00',
    format='%Y-%m-%d %H:%M:%S'
)

# Validate numeric range
range_valid = validate_numeric_range(
    value=150.25,
    min_value=0,
    max_value=1000
)

# Validate file exists
file_exists = validate_file_exists('data/aapl.csv')
```

### 3. Configuration Management

```python
from src.utils.utils import (
    load_yaml_config, save_yaml_config,
    load_env_config, merge_configs
)

# Load YAML configuration
config = load_yaml_config('config.yaml')

# Save YAML configuration
save_yaml_config(config, 'config_updated.yaml')

# Load environment configuration
env_config = load_env_config(prefix='APP_')

# Merge configurations
merged_config = merge_configs(
    base_config=config,
    override_config=env_config
)
```

## CLI Integration

### Workflow Commands

```bash
# Run workflow
python -m src.workflow.workflow --config workflow_config.yaml

# Generate report
python -m src.workflow.reporting --template daily_summary --symbols AAPL,GOOGL

# Schedule workflow
python -m src.workflow.workflow --schedule daily --time 09:00 --config daily_workflow.yaml

# Run utility functions
python -m src.utils.point_size_determination --symbol AAPL --instrument stock

# Docker operations
python -m src.utils.docker_browser --action start --image selenium/standalone-chrome
```

### CLI Options

- **`--config`** - Configuration file path
- **`--schedule`** - Schedule type (daily, weekly, monthly)
- **`--time`** - Execution time
- **`--symbols`** - Comma-separated symbols
- **`--template`** - Report template
- **`--action`** - Action to perform

## Workflow Examples

### 1. Daily Analysis Workflow

```python
from src.workflow.workflow import WorkflowEngine

# Daily analysis workflow
daily_workflow = WorkflowEngine()

# Define daily steps
daily_workflow.add_step(
    name='market_data_fetch',
    function=fetch_market_data,
    params={'symbols': ['AAPL', 'GOOGL', 'MSFT'], 'period': '1d'},
    dependencies=[]
)

daily_workflow.add_step(
    name='technical_analysis',
    function=run_technical_analysis,
    params={'indicators': ['rsi', 'macd', 'bollinger_bands']},
    dependencies=['market_data_fetch']
)

daily_workflow.add_step(
    name='report_generation',
    function=generate_daily_report,
    params={'template': 'daily_summary'},
    dependencies=['technical_analysis']
)

daily_workflow.add_step(
    name='alert_check',
    function=check_alerts,
    params={'threshold': 0.05},
    dependencies=['technical_analysis']
)

# Execute daily workflow
daily_workflow.execute(parallel=True)
```

### 2. Weekly Research Workflow

```python
# Weekly research workflow
weekly_workflow = WorkflowEngine()

weekly_workflow.add_step(
    name='data_collection',
    function=collect_research_data,
    params={'sources': ['yfinance', 'polygon', 'news']},
    dependencies=[]
)

weekly_workflow.add_step(
    name='comprehensive_analysis',
    function=run_comprehensive_analysis,
    params={'analysis_types': ['technical', 'fundamental', 'sentiment']},
    dependencies=['data_collection']
)

weekly_workflow.add_step(
    name='report_creation',
    function=create_weekly_report,
    params={'template': 'weekly_research'},
    dependencies=['comprehensive_analysis']
)

weekly_workflow.add_step(
    name='distribution',
    function=distribute_report,
    params={'recipients': ['analysts@company.com']},
    dependencies=['report_creation']
)

# Schedule weekly execution
weekly_workflow.schedule('weekly', day_of_week='friday', time='17:00')
```

### 3. Real-time Monitoring Workflow

```python
import time
from src.workflow.workflow import WorkflowEngine

# Real-time monitoring workflow
monitoring_workflow = WorkflowEngine()

monitoring_workflow.add_step(
    name='real_time_data',
    function=fetch_real_time_data,
    params={'symbols': ['AAPL', 'GOOGL'], 'interval': '1m'},
    dependencies=[]
)

monitoring_workflow.add_step(
    name='alert_analysis',
    function=analyze_alerts,
    params={'conditions': ['price_change > 0.02', 'volume_spike > 2.0']},
    dependencies=['real_time_data']
)

monitoring_workflow.add_step(
    name='notification',
    function=send_notifications,
    params={'channels': ['email', 'slack']},
    dependencies=['alert_analysis']
)

# Continuous execution
while True:
    monitoring_workflow.execute()
    time.sleep(60)  # Wait 1 minute
```

## Performance Optimization

### Workflow Performance Tips

1. **Parallel execution** - Use parallel processing for independent tasks
2. **Caching** - Cache intermediate results
3. **Resource management** - Monitor and manage resource usage
4. **Error recovery** - Implement robust error handling

### Performance Configuration

```python
# Performance-optimized workflow
config = {
    'parallel': True,
    'max_workers': 4,
    'cache_results': True,
    'cache_ttl': 3600,
    'timeout': 300,
    'retry_attempts': 3,
    'retry_delay': 5
}

workflow = WorkflowEngine(config=config)
```

## Error Handling

### Workflow Error Recovery

```python
from src.workflow.workflow import WorkflowEngine

try:
    workflow = WorkflowEngine()
    results = workflow.execute()
except WorkflowError as e:
    print(f"Workflow error: {e}")
    # Handle workflow-specific errors
except TimeoutError as e:
    print(f"Timeout error: {e}")
    # Handle timeout errors
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle general errors
```

### Utility Error Handling

```python
from src.utils.utils import safe_execute

# Safe execution with error handling
def safe_operation():
    return safe_execute(
        function=risky_operation,
        fallback=default_value,
        max_retries=3
    )
```

## Testing

### Workflow Testing

```bash
# Run workflow tests
pytest tests/workflow/ -v

# Test specific components
pytest tests/workflow/test_workflow.py -v
pytest tests/workflow/test_reporting.py -v

# Test utilities
pytest tests/utils/ -v
pytest tests/utils/test_point_size_determination.py -v
```

### Integration Testing

```bash
# Test workflow integration
pytest tests/workflow/test_integration.py -v

# Test utility integration
pytest tests/utils/test_integration.py -v
```

## Related Documentation

- **[CLI Interface](cli-interface.md)** - Command-line interface
- **[Data Sources](../api/data-sources.md)** - Data acquisition
- **[Analysis Tools](analysis-tools.md)** - Analysis capabilities
- **[Export Functions](export-functions.md)** - Data export 