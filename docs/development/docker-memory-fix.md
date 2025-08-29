# Docker Memory Fix - Quick Guide

## Problem
When running `./interactive_system.py` in Docker and loading EURUSD data with `3 eurusd`, the container gets killed due to memory exhaustion.

## Solution Implemented

### 1. Memory Optimization in DataManager
- **Chunked Loading**: Large files (>100MB) are loaded in chunks
- **Memory Monitoring**: Real-time memory usage tracking
- **Automatic Cleanup**: Garbage collection after each chunk
- **Progress Indicators**: Shows loading progress for large files

### 2. Docker Resource Limits
Added to `docker-compose.yml`:
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

### 3. Environment Variables
Added to `docker.env`:
```bash
MAX_MEMORY_MB=4096
CHUNK_SIZE=50000
ENABLE_MEMORY_OPTIMIZATION=true
```

## Quick Test

### Run Memory Optimization Test
```bash
# Test locally
uv run pytest tests/interactive/test_data_manager_memory.py -v

# Test in Docker
./scripts/docker/test_memory_docker.sh
```

### Test Interactive System
```bash
# Start container
docker-compose up -d

# Run interactive system
docker-compose exec neozork-hld ./interactive_system.py

# Load EURUSD data (should work without being killed)
Menu Load Data -> Enter: 3 eurusd
```

## Expected Behavior

### Before Fix
```
✅ Loaded: CSVExport_EURUSD_PERIOD_M1.parquet (9523445 rows)
Killed
```

### After Fix
```
🔄 Loading CSVExport_EURUSD_PERIOD_M1.parquet in chunks of 50,000 rows...
   📊 Progress: 10.0% (500,000/9,523,445 rows)
   📊 Progress: 20.0% (1,000,000/9,523,445 rows)
   ...
✅ Loaded: CSVExport_EURUSD_PERIOD_M1.parquet (9,523,445 rows, ~847MB)
📊 Memory Summary:
   Total files loaded: 10
   Total rows: 12,456,123
   Estimated memory usage: 1,847 MB
```

## Configuration Options

### Increase Memory Limit
```bash
# In docker.env
MAX_MEMORY_MB=8192  # 8GB
```

### Reduce Chunk Size (for better memory management)
```bash
# In docker.env
CHUNK_SIZE=25000  # Smaller chunks
```

### Disable Memory Optimization (not recommended)
```bash
# In docker.env
ENABLE_MEMORY_OPTIMIZATION=false
```

## Troubleshooting

### Container Still Getting Killed
1. Increase Docker memory limit in `docker-compose.yml`
2. Reduce chunk size in `docker.env`
3. Check available system memory

### Performance Issues
1. Increase chunk size for faster loading
2. Increase memory limit
3. Monitor memory usage with test script

## Files Modified
- `src/interactive/data_manager.py` - Memory optimization logic
- `docker-compose.yml` - Resource limits
- `docker.env` - Memory configuration
- `tests/interactive/test_data_manager_memory.py` - Memory tests
- `scripts/debug/test_memory_optimization.py` - Memory test script
- `scripts/docker/test_memory_docker.sh` - Docker test script

## Documentation
- Full documentation: `docs/development/memory-optimization.md`
- Implementation details and best practices included
