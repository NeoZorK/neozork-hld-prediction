# Memory Optimization for Docker Container

## Overview

This document describes the memory optimization features implemented to prevent the "Killed" error when loading large datasets in the Docker container.

## Problem

When running `./interactive_system.py` in Docker and loading large EURUSD datasets (especially `CSVExport_EURUSD_PERIOD_M1.parquet` with 9,523,445 rows), the container would run out of memory and be killed by the system.

## Solution

### 1. Memory Management in DataManager

The `DataManager` class now includes memory optimization features:

- **Chunked Loading**: Large files (>100MB) are loaded in chunks to manage memory usage
- **Memory Monitoring**: Real-time memory usage tracking with `psutil`
- **Automatic Cleanup**: Garbage collection after each chunk
- **Memory Limits**: Configurable memory limits to prevent OOM

### 2. Environment Variables

Configure memory optimization through environment variables:

```bash
# Memory limit in MB (default: 2048)
MAX_MEMORY_MB=4096

# Chunk size for loading large files (default: 100000)
CHUNK_SIZE=50000

# Enable/disable memory optimization (default: true)
ENABLE_MEMORY_OPTIMIZATION=true
```

### 3. Docker Resource Limits

The `docker-compose.yml` now includes resource limits:

```yaml
deploy:
  resources:
    limits:
      memory: 6G
      cpus: '2.0'
    reservations:
      memory: 2G
      cpus: '0.5'
```

## Features

### Chunked Loading

Large files are automatically detected and loaded in chunks:

```python
# For parquet files
import pyarrow.parquet as pq
parquet_file = pq.ParquetFile(file_path)
for chunk in parquet_file.iter_batches(batch_size=chunk_size):
    # Process chunk
    gc.collect()  # Clean up memory
```

### Memory Monitoring

Real-time memory usage tracking:

```python
import psutil
memory = psutil.virtual_memory()
available_memory = memory.available / (1024 * 1024)  # MB
```

### Progress Indicators

During chunked loading, progress is displayed:

```
🔄 Loading CSVExport_EURUSD_PERIOD_M1.parquet in chunks of 50,000 rows...
   📊 Progress: 10.0% (500,000/9,523,445 rows)
   📊 Progress: 20.0% (1,000,000/9,523,445 rows)
```

## Usage

### In Docker Container

1. **Start container with memory limits**:
   ```bash
   docker-compose up -d
   ```

2. **Run interactive system**:
   ```bash
   docker-compose exec neozork-hld ./interactive_system.py
   ```

3. **Load data with memory optimization**:
   ```
   Menu Load Data -> Enter: 3 eurusd
   ```

### Testing Memory Optimization

Run the memory optimization test:

```bash
docker-compose exec neozork-hld python scripts/debug/test_memory_optimization.py
```

### Running Tests

```bash
# Run memory optimization tests
uv run pytest tests/interactive/test_data_manager_memory.py -v

# Run all tests with memory optimization
uv run pytest tests -n auto
```

## Configuration

### Default Settings

- **Max Memory**: 2GB (2048 MB)
- **Chunk Size**: 100,000 rows
- **Large File Threshold**: 100MB
- **Memory Buffer**: 50% of available memory

### Custom Configuration

Set environment variables in `docker.env`:

```bash
# Increase memory limit for large datasets
MAX_MEMORY_MB=8192

# Reduce chunk size for better memory management
CHUNK_SIZE=25000

# Disable optimization if needed
ENABLE_MEMORY_OPTIMIZATION=false
```

## Monitoring

### Memory Usage Display

The system now shows memory usage during data loading:

```
📊 Memory Summary:
   Total files loaded: 10
   Total rows: 12,456,123
   Estimated memory usage: 1,847 MB
   Final memory usage: ~1,847 MB
```

### Progress Tracking

Large file loading shows progress:

```
🔄 Loading file 1/10: CSVExport_EURUSD_PERIOD_M1.parquet
   📊 Progress: 25.0% (2,380,861/9,523,445 rows)
   📊 Progress: 50.0% (4,761,722/9,523,445 rows)
```

## Troubleshooting

### Container Still Getting Killed

1. **Increase memory limits**:
   ```yaml
   deploy:
     resources:
       limits:
         memory: 8G  # Increase from 6G
   ```

2. **Reduce chunk size**:
   ```bash
   CHUNK_SIZE=25000  # Reduce from 50000
   ```

3. **Disable memory optimization** (not recommended):
   ```bash
   ENABLE_MEMORY_OPTIMIZATION=false
   ```

### Performance Issues

1. **Increase chunk size** for faster loading:
   ```bash
   CHUNK_SIZE=100000
   ```

2. **Increase memory limit**:
   ```bash
   MAX_MEMORY_MB=8192
   ```

### Memory Leaks

1. **Enable garbage collection**:
   ```bash
   ENABLE_MEMORY_OPTIMIZATION=true
   ```

2. **Monitor memory usage**:
   ```bash
   python scripts/debug/test_memory_optimization.py
   ```

## Best Practices

1. **Start with conservative settings** and adjust based on your data size
2. **Monitor memory usage** during data loading
3. **Use chunked loading** for files larger than 100MB
4. **Clean up memory** after processing large datasets
5. **Test with your specific data** before production use

## Implementation Details

### Key Classes

- `DataManager`: Main memory optimization logic
- `_load_data_in_chunks()`: Chunked loading implementation
- `_estimate_memory_usage()`: Memory usage estimation
- `_check_memory_available()`: Memory availability check

### Dependencies

- `psutil`: Memory monitoring
- `pyarrow`: Efficient parquet reading
- `pandas`: Data manipulation
- `gc`: Garbage collection

### Error Handling

- Graceful handling of memory exhaustion
- Automatic fallback to standard loading
- Progress indicators for long operations
- Detailed error messages for debugging
