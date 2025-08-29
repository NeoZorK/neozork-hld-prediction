# Memory Optimization v2 - Aggressive Memory Management

## Overview

This document describes the enhanced memory optimization features implemented in version 2 of the NeoZorK HLD Prediction system. The new implementation provides aggressive memory management to handle extremely large datasets in Docker containers without causing "Killed" errors.

## Key Improvements

### 1. Aggressive Memory Optimization

The new system implements multiple layers of memory optimization:

- **Conservative Defaults**: Reduced memory limits and chunk sizes for better stability
- **Multi-level Processing**: Different strategies for small, large, and extremely large datasets
- **Real-time Monitoring**: Continuous memory usage tracking with automatic throttling
- **Graceful Degradation**: Automatic fallback to sampling for extremely large datasets

### 2. Enhanced DataManager

The `DataManager` class has been completely rewritten with:

- **Intelligent Chunking**: Automatic detection of file sizes and appropriate loading strategies
- **Datetime Handling**: Proper parsing of datetime columns during chunked loading
- **Memory Thresholds**: Multiple thresholds for different processing strategies
- **Progress Indicators**: Real-time progress reporting for large file operations

### 3. Improved Data Quality Checks

The data quality functions now support:

- **Aggressive Sampling**: For datasets >2GB, uses very small samples (2% or 5k rows)
- **Chunked Processing**: For datasets 0.5-2GB, processes in chunks with memory cleanup
- **Direct Processing**: For datasets <0.5GB, processes normally
- **Automatic Skipping**: Skips certain checks for extremely large datasets to prevent OOM

## Configuration

### Environment Variables

```bash
# Memory management configuration - Conservative settings for Docker stability
MAX_MEMORY_MB=512                    # 512MB default (reduced from 2GB)
CHUNK_SIZE=25000                     # 25k rows per chunk (reduced from 100k)
SAMPLE_SIZE=5000                     # 5k rows for sampling (reduced from 10k)
MAX_FILE_SIZE_MB=25                  # 25MB threshold for chunked loading
ENABLE_MEMORY_OPTIMIZATION=true      # Enable all optimizations
ENABLE_STREAMING=true                # Enable streaming operations

# Aggressive memory optimization for large datasets
MEMORY_WARNING_THRESHOLD=0.7         # 70% memory usage warning
MEMORY_CRITICAL_THRESHOLD=0.9        # 90% memory usage critical
```

### Docker Configuration

```yaml
# docker-compose.yml
services:
  neozork-hld:
    deploy:
      resources:
        limits:
          memory: 8G                  # Increased from 6G
          cpus: '4.0'                 # Increased from 2.0
        reservations:
          memory: 4G                  # Increased from 2G
          cpus: '1.0'                 # Increased from 0.5
    healthcheck:
      test: ["CMD", "python", "-c", "import psutil; print('Memory:', psutil.virtual_memory().percent, '%')"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## Processing Strategies

### 1. File Loading Strategy

```python
def _should_use_chunked_loading(self, file_path: Path) -> bool:
    """Determine if file should be loaded in chunks."""
    file_size_mb = self._get_file_size_mb(file_path)
    return file_size_mb > self.max_file_size_mb  # 25MB threshold
```

**Small Files (<25MB)**: Load directly with datetime parsing
**Large Files (>25MB)**: Load in chunks with progress indicators

### 2. Data Quality Check Strategy

```python
# Memory thresholds for different processing strategies
if memory_mb > max_memory_mb * 2.0:      # >1GB: Aggressive sampling
    sample_size = min(5000, len(df) // 50)  # 2% or 5k rows
elif memory_mb > max_memory_mb * 1.0:    # >512MB: Sampling
    sample_size = min(5000, len(df) // 20)  # 5% or 5k rows
elif memory_mb > max_memory_mb * 0.5:    # >256MB: Chunked processing
    chunk_size = min(25000, 10000)       # Smaller chunks
else:                                     # <256MB: Direct processing
    # Process normally
```

### 3. Memory Monitoring

```python
def _check_memory_available(self, required_mb: int = None) -> bool:
    """Check if we have enough memory available."""
    memory_info = self._get_memory_info()
    available_mb = memory_info['available_mb']
    
    if required_mb is None:
        required_mb = self.max_memory_mb * 0.3  # Require 30% of max memory
    
    return available_mb > required_mb
```

## Features

### 1. Intelligent Datetime Handling

The system automatically detects and parses datetime columns:

```python
def _load_csv_with_datetime_handling(self, file_path: Path) -> pd.DataFrame:
    # Detect datetime columns
    datetime_columns = []
    sample_df = pd.read_csv(file_path, nrows=1000)
    for col in sample_df.columns:
        if any(keyword in col.lower() for keyword in ['date', 'time', 'datetime', 'timestamp']):
            datetime_columns.append(col)
    
    # Parse datetime columns during loading
    for col in datetime_columns:
        if col in chunk.columns:
            chunk[col] = pd.to_datetime(chunk[col], errors='coerce')
```

### 2. Progress Indicators

Real-time progress reporting for large operations:

```
🔄 Loading CSVExport_EURUSD_PERIOD_M1.parquet in chunks of 25,000 rows...
   📈 Progress: 10.0% (250,000/9,523,445 rows)
   📈 Progress: 20.0% (500,000/9,523,445 rows)
   ...
✅ Loaded: CSVExport_EURUSD_PERIOD_M1.parquet (9,523,445 rows, ~847MB)
```

### 3. Memory Usage Reporting

Detailed memory usage information:

```
📊 Memory Summary:
   Total files loaded: 10
   Total rows: 12,456,123
   Estimated memory usage: 1,847 MB
   Final memory usage: ~1,847MB
```

### 4. Aggressive Data Quality Checks

For extremely large datasets, the system uses aggressive sampling:

```
📊 Extremely large dataset detected (2588MB), using aggressive sampling...
   Column: Open: ~1,234 missing (0.05%) [estimated from sample]
   Column: High: ~2,345 missing (0.09%) [estimated from sample]
```

## Error Handling

### 1. Memory Errors

```python
def load_data_from_file(self, file_path: str) -> pd.DataFrame:
    # Check memory before loading
    if not self._check_memory_available():
        raise MemoryError("Insufficient memory to load file")
```

### 2. Graceful Degradation

```python
# For very large datasets, skip gap analysis to save memory
if memory_mb > max_memory_mb * 1.0:
    print(f"📊 Large dataset detected ({memory_mb}MB), skipping gap analysis to save memory...")
    print(f"⚠️  Gap Check: Skipped for large dataset to prevent memory issues")
    return
```

### 3. Chunked Error Recovery

```python
try:
    chunk_result = operation_func(chunk)
    results.append(chunk_result)
except Exception as e:
    print(f"⚠️  Error processing chunk at rows {start_idx}-{end_idx}: {e}")
    # Continue with next chunk instead of failing completely
    continue
```

## Performance Optimizations

### 1. Memory Cleanup

```python
# Memory management after each chunk
if self.enable_memory_optimization:
    gc.collect()

# Clean up intermediate data
del chunks
gc.collect()
```

### 2. Conservative Chunk Sizes

- **Default**: 25,000 rows per chunk (reduced from 100,000)
- **Large datasets**: 10,000 rows per chunk
- **Extremely large datasets**: 5,000 rows per chunk

### 3. Sampling Strategies

- **Extremely large (>1GB)**: 2% or 5,000 rows
- **Very large (>512MB)**: 5% or 5,000 rows
- **Large (>256MB)**: 10% or 10,000 rows

## Testing

### Test Coverage

The new memory optimization features are fully tested:

```bash
# Run memory optimization tests
uv run pytest tests/interactive/test_data_manager_memory_optimization.py -v

# Expected output: 16 tests passed
```

### Test Scenarios

1. **Memory Settings Initialization**: Verify environment variable overrides
2. **Memory Usage Estimation**: Test memory calculation accuracy
3. **Chunked Loading**: Test large file processing
4. **Datetime Handling**: Test automatic datetime parsing
5. **Error Handling**: Test graceful error recovery
6. **Memory Monitoring**: Test real-time memory tracking

## Migration Guide

### From v1 to v2

1. **Update Environment Variables**:
   ```bash
   # Old settings
   MAX_MEMORY_MB=2048
   CHUNK_SIZE=100000
   
   # New settings
   MAX_MEMORY_MB=512
   CHUNK_SIZE=25000
   SAMPLE_SIZE=5000
   MAX_FILE_SIZE_MB=25
   ```

2. **Update Docker Configuration**:
   ```yaml
   # Increase memory limits
   deploy:
     resources:
       limits:
         memory: 8G  # Increased from 6G
   ```

3. **Behavior Changes**:
   - More conservative memory usage
   - Automatic datetime column detection
   - Aggressive sampling for large datasets
   - Better progress indicators

## Troubleshooting

### Common Issues

1. **Still Getting "Killed" Error**:
   - Increase `MAX_MEMORY_MB` in docker.env
   - Increase Docker memory limits
   - Reduce `CHUNK_SIZE` for more conservative processing

2. **Slow Processing**:
   - Increase `CHUNK_SIZE` for faster processing
   - Increase `SAMPLE_SIZE` for better accuracy
   - Check if memory optimization is enabled

3. **Datetime Columns Not Parsed**:
   - Check column names for datetime keywords
   - Verify CSV format is correct
   - Check for encoding issues

### Debug Information

Enable debug logging to see detailed memory usage:

```bash
LOG_LEVEL=DEBUG
```

This will show:
- Memory usage at each step
- Chunk processing progress
- Sampling decisions
- Error recovery attempts

## Best Practices

1. **Start Conservative**: Begin with default settings and adjust based on your data
2. **Monitor Memory**: Use the health check to monitor container memory usage
3. **Test with Your Data**: Always test with your specific dataset size
4. **Gradual Scaling**: Increase settings gradually to find optimal values
5. **Backup Strategy**: Keep backups before processing large datasets

## Future Enhancements

1. **Adaptive Chunking**: Dynamic chunk size based on available memory
2. **Streaming Processing**: True streaming for extremely large datasets
3. **Memory Prediction**: Predict memory usage before loading
4. **Parallel Processing**: Multi-threaded chunk processing
5. **Compression Support**: Automatic compression for large files
