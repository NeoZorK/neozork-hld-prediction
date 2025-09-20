# Gaps Analysis Module

## Overview

The Gaps Analysis module provides comprehensive time series gaps detection and fixing capabilities for MTF (Multi-Timeframe) data in the NeoZork Interactive ML Trading Strategy Development system.

## Features

- **Fast Gap Detection**: Vectorized algorithms for efficient gap detection across multiple timeframes
- **Multiple Fixing Strategies**: Various interpolation and filling methods
- **Progress Tracking**: Real-time progress bars with percentage and ETA
- **Backup Management**: Automatic backup creation and restoration
- **Comprehensive Reporting**: Detailed statistics and analysis results

## Architecture

### Core Components

1. **GapsDetector**: Fast gap detection using vectorized operations
2. **GapsFixer**: Multiple gap filling strategies
3. **ProgressTracker**: Real-time progress tracking with ETA
4. **BackupManager**: Backup creation, restoration, and management
5. **GapsAnalyzer**: Main orchestrator combining all components

### File Structure

```
src/interactive/eda_analysis/gaps_analysis/
├── __init__.py              # Module exports
├── gaps_detector.py         # Gap detection algorithms
├── gaps_fixer.py           # Gap fixing strategies
├── progress_tracker.py     # Progress tracking utilities
├── backup_manager.py       # Backup management
└── gaps_analyzer.py        # Main analyzer class
```

## Usage

### Basic Usage

```python
from src.interactive.eda_analysis.gaps_analysis import GapsAnalyzer

# Initialize analyzer
analyzer = GapsAnalyzer()

# Analyze and fix gaps
result = analyzer.analyze_and_fix_gaps(
    mtf_data=mtf_data,
    symbol='BTCUSD',
    strategy='auto',
    create_backup=True
)
```

### Available Strategies

1. **auto** 🤖: **Auto-select best strategy** based on data characteristics (default)
2. **forward_fill**: Fill gaps with last known value
3. **backward_fill**: Fill gaps with next known value
4. **linear_interpolation**: Linear interpolation between values
5. **spline_interpolation**: Spline interpolation (smooth curves)
6. **mean_fill**: Fill gaps with mean value
7. **median_fill**: Fill gaps with median value

### Progress Tracking

```python
from src.interactive.eda_analysis.gaps_analysis import ProgressTracker

# Create progress tracker
tracker = ProgressTracker(total_items=100, description="Processing")

# Start tracking
tracker.start()

# Update progress
tracker.update(current_item=50, custom_message="Halfway done")

# Finish
tracker.finish("Completed successfully")
```

### Backup Management

```python
# Create backup
backup_result = analyzer.backup_manager.create_backup(
    mtf_data, 'BTCUSD', 'Pre-gap-fixing backup'
)

# List backups
backups = analyzer.list_backups()

# Restore from backup
restore_result = analyzer.restore_from_backup('backup_name')
```

## Integration with EDA Menu

The gaps analysis is integrated into the EDA Analysis menu:

1. **Load Data** → **4. Cleaned Data** (load MTF data)
2. **EDA Analysis** → **1. Time Series Gaps Analysis**
3. Choose from submenu options:
   - Detect Gaps Only
   - Detect & Fix Gaps
   - Show Available Strategies
   - List Backups
   - Restore from Backup
   - Cleanup Backups

## Algorithm Details

### Gap Detection

The gap detection algorithm uses vectorized operations for efficiency:

1. Calculate differences between consecutive timestamps
2. Identify gaps where differences exceed expected interval threshold
3. Calculate gap statistics (duration, missing points, etc.)
4. Generate comprehensive gap reports

### Gap Fixing

Multiple strategies are available for filling gaps:

- **Auto Selection** 🤖: **Intelligent strategy selection** based on data analysis
- **Interpolation Methods**: Linear and spline interpolation for smooth data
- **Forward/Backward Fill**: Simple filling with adjacent values
- **Statistical Methods**: Mean and median filling for robust estimates

#### Auto Selection Algorithm

The auto selection feature analyzes both data and gap characteristics to choose the optimal strategy:

**Data Analysis:**
- **Trend Detection**: Identifies trending vs stationary data
- **Volatility Assessment**: Measures price volatility
- **Trend Strength**: Calculates directional bias strength

**Gap Analysis:**
- **Gap Size**: Average and maximum gap sizes
- **Gap Distribution**: Number and pattern of gaps

**Decision Tree:**
- **Trending + Small Gaps (<5)**: Linear interpolation
- **Volatile + Very Small Gaps (<3)**: Spline interpolation  
- **Strong Trend + Medium Gaps (<10)**: Forward fill
- **Stationary + Medium Gaps (<7)**: Mean fill
- **Very Large Gaps (>20)**: Median fill (robust)
- **Default**: Linear interpolation

### Performance Optimizations

- Vectorized operations for gap detection
- Efficient memory usage with progress tracking
- Parallel processing capabilities
- Caching of intermediate results

## Testing

Comprehensive test suite with 100% coverage:

```bash
# Run all tests
uv run pytest tests/test_gaps_analysis.py -v

# Run specific test class
uv run pytest tests/test_gaps_analysis.py::TestGapsDetector -v
```

## Error Handling

The module includes robust error handling:

- Graceful degradation on errors
- Detailed error messages and logging
- Fallback strategies for critical operations
- Validation of input data structures

## Configuration

### Gap Thresholds

Default gap thresholds for different timeframes:

```python
gap_thresholds = {
    'M1': timedelta(minutes=1),
    'M5': timedelta(minutes=5),
    'M15': timedelta(minutes=15),
    'M30': timedelta(minutes=30),
    'H1': timedelta(hours=1),
    'H4': timedelta(hours=4),
    'D1': timedelta(days=1),
    'W1': timedelta(weeks=1),
    'MN1': timedelta(days=30)
}
```

### Progress Update Interval

Default progress update interval: 100ms (configurable)

## Future Enhancements

- Machine learning-based gap filling
- Real-time gap monitoring
- Advanced visualization tools
- Integration with external data sources
- Custom gap detection rules

## Dependencies

- pandas: Data manipulation and analysis
- numpy: Numerical operations
- datetime: Time handling
- pathlib: File system operations
- pickle: Data serialization
- json: Metadata storage

## License

This module is part of the NeoZork Interactive ML Trading Strategy Development system.
