# Quick Start - Memory Optimization v2

## Problem Solved

The original system would get "Killed" when loading large EURUSD datasets in Docker containers due to memory exhaustion. The new v2 system solves this with aggressive memory optimization.

## Quick Fix

### 1. Update Environment Variables

```bash
# In docker.env
MAX_MEMORY_MB=512                    # Reduced from 2048
CHUNK_SIZE=25000                     # Reduced from 100000
SAMPLE_SIZE=5000                     # New setting
MAX_FILE_SIZE_MB=25                  # New setting
ENABLE_MEMORY_OPTIMIZATION=true      # Ensure enabled
```

### 2. Update Docker Memory Limits

```yaml
# In docker-compose.yml
deploy:
  resources:
    limits:
      memory: 8G                      # Increased from 6G
      cpus: '4.0'                     # Increased from 2.0
    reservations:
      memory: 4G                      # Increased from 2G
      cpus: '1.0'                     # Increased from 0.5
```

### 3. Restart Container

```bash
# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

## Test the Fix

### 1. Run Interactive System

```bash
docker-compose exec neozork-hld ./interactive_system.py
```

### 2. Load EURUSD Data

```
Menu: 1 (Load Data)
Enter: 3 eurusd
```

### Expected Behavior

**Before (v1)**:
```
✅ Loaded: CSVExport_EURUSD_PERIOD_M1.parquet (9523445 rows)
Killed
```

**After (v2)**:
```
🔄 Loading CSVExport_EURUSD_PERIOD_M1.parquet in chunks of 25,000 rows...
   📈 Progress: 10.0% (250,000/9,523,445 rows)
   📈 Progress: 20.0% (500,000/9,523,445 rows)
   ...
✅ Loaded: CSVExport_EURUSD_PERIOD_M1.parquet (9,523,445 rows, ~847MB)
📊 Memory Summary:
   Total files loaded: 10
   Total rows: 12,456,123
   Estimated memory usage: 1,847 MB
```

## Key Features

### 1. Automatic Chunked Loading

- Files >25MB are automatically loaded in chunks
- Progress indicators show loading status
- Memory is cleaned up after each chunk

### 2. Intelligent Datetime Parsing

- Automatically detects datetime columns
- Parses datetime during chunked loading
- No manual configuration required

### 3. Aggressive Data Quality Checks

- Large datasets use sampling instead of full processing
- Extremely large datasets use aggressive sampling (2%)
- Prevents memory exhaustion during analysis

### 4. Real-time Memory Monitoring

- Continuous memory usage tracking
- Automatic throttling when memory is low
- Graceful degradation for large datasets

## Configuration Options

### Conservative Settings (Default)

```bash
MAX_MEMORY_MB=512
CHUNK_SIZE=25000
SAMPLE_SIZE=5000
```

### Aggressive Settings (More Memory)

```bash
MAX_MEMORY_MB=1024
CHUNK_SIZE=50000
SAMPLE_SIZE=10000
```

### Very Conservative Settings (Limited Memory)

```bash
MAX_MEMORY_MB=256
CHUNK_SIZE=10000
SAMPLE_SIZE=1000
```

## Troubleshooting

### Still Getting "Killed"

1. **Increase Docker Memory**:
   ```yaml
   limits:
     memory: 12G  # Increase further
   ```

2. **Reduce Chunk Size**:
   ```bash
   CHUNK_SIZE=10000  # Smaller chunks
   ```

3. **Reduce Memory Limit**:
   ```bash
   MAX_MEMORY_MB=256  # More conservative
   ```

### Slow Processing

1. **Increase Chunk Size**:
   ```bash
   CHUNK_SIZE=50000  # Larger chunks
   ```

2. **Increase Memory Limit**:
   ```bash
   MAX_MEMORY_MB=1024  # More memory
   ```

### Datetime Columns Not Parsed

1. **Check Column Names**: Ensure columns contain 'date', 'time', 'datetime', or 'timestamp'
2. **Check CSV Format**: Verify CSV is properly formatted
3. **Check Encoding**: Ensure UTF-8 encoding

## Monitoring

### Health Check

The container includes a health check that monitors memory usage:

```bash
# Check container health
docker-compose ps

# View health check logs
docker-compose logs neozork-hld
```

### Memory Usage

Monitor memory usage in real-time:

```bash
# Inside container
docker-compose exec neozork-hld python -c "import psutil; print('Memory:', psutil.virtual_memory().percent, '%')"
```

## Testing

### Run Memory Tests

```bash
# Test memory optimization features
uv run pytest tests/interactive/test_data_manager_memory_optimization.py -v
```

### Expected Output

```
✅ Passed: 16
❌ Failed: 0
⏭️  Skipped: 0
💥 Errors: 0
📈 Total: 16
```

## Migration from v1

### Automatic Migration

The new system is backward compatible. Existing configurations will work, but you may want to:

1. **Update Environment Variables**: Use the new conservative defaults
2. **Increase Docker Memory**: Give more memory to the container
3. **Test with Your Data**: Verify it works with your specific datasets

### Behavior Changes

- **More Conservative**: Uses less memory by default
- **Better Progress**: Shows loading progress for large files
- **Automatic Parsing**: Detects and parses datetime columns automatically
- **Graceful Degradation**: Handles large datasets better

## Support

### Debug Mode

Enable debug logging for detailed information:

```bash
LOG_LEVEL=DEBUG
```

### Common Commands

```bash
# Check memory usage
docker-compose exec neozork-hld python -c "import psutil; m=psutil.virtual_memory(); print(f'Total: {m.total//1024//1024}MB, Available: {m.available//1024//1024}MB, Used: {m.percent}%')"

# Test file loading
docker-compose exec neozork-hld python -c "from src.interactive.data_manager import DataManager; dm=DataManager(); print('DataManager initialized successfully')"

# Check environment variables
docker-compose exec neozork-hld env | grep -E "(MAX_MEMORY|CHUNK_SIZE|SAMPLE_SIZE)"
```

## Success Indicators

✅ **Container doesn't get killed** when loading large datasets
✅ **Progress indicators** show during file loading
✅ **Memory usage** stays within limits
✅ **Datetime columns** are automatically parsed
✅ **Data quality checks** complete without memory issues
✅ **All tests pass** for memory optimization features
