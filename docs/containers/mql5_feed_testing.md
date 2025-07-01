# Testing mql5_feed Folder Access in Docker Container

This document explains how to test the `mql5_feed` folder access in Docker container and troubleshoot any issues.

## Overview

The `mql5_feed` folder contains MQL5 indicators and is mounted into the Docker container at `/app/mql5_feed`. The tests verify that this folder is accessible and contains the expected files.

## Running Tests

### 1. Start the Docker Container

```bash
# Start the container
docker-compose up -d

# Or run interactively
docker-compose run --rm neozork-hld bash
```

### 2. Run the Diagnostic Script

Inside the container, run the diagnostic script:

```bash
# Run the bash diagnostic script
./scripts/docker/test_mql5_feed_in_container.sh

# Or run the Python diagnostic test
python -m pytest tests/docker/test_container_mql5_feed_paths.py::TestContainerMQL5FeedPaths::test_list_possible_paths -v -s
```

### 3. Run All MQL5 Feed Tests

```bash
# Run all mql5_feed tests
python -m pytest tests/docker/test_mql5_feed_access.py -v

# Run specific test
python -m pytest tests/docker/test_mql5_feed_access.py::TestMQL5FeedAccess::test_mql5_feed_folder_exists -v
```

## Expected Results

When everything is working correctly, you should see:

```
✅ Found directory: /app
   Contents: data logs mql5_feed results tests ...
   🎯 Found mql5_feed subdirectory at: /app/mql5_feed
   mql5_feed contents: indicators
   📁 Found indicators directory
   indicators contents: SCHR_VWAP.mq5
```

## Troubleshooting

### Problem: "mql5_feed folder not found"

**Possible causes:**
1. The folder is not mounted correctly
2. The folder doesn't exist on the host
3. Permission issues

**Solutions:**
1. Check if the folder exists on the host:
   ```bash
   ls -la mql5_feed/
   ```

2. Verify Docker volume mount:
   ```bash
   docker-compose config
   ```

3. Check container logs:
   ```bash
   docker-compose logs neozork-hld
   ```

### Problem: "Permission denied"

**Solutions:**
1. Check file permissions on the host:
   ```bash
   ls -la mql5_feed/
   chmod -R 755 mql5_feed/
   ```

2. Run container with proper user:
   ```bash
   docker-compose run --rm --user root neozork-hld bash
   ```

### Problem: "SCHR_VWAP.mq5 not found"

**Solutions:**
1. Verify the file exists:
   ```bash
   ls -la mql5_feed/indicators/
   ```

2. Check file encoding:
   ```bash
   file mql5_feed/indicators/SCHR_VWAP.mq5
   ```

## Test Structure

The tests check:

1. **Folder Existence**: `mql5_feed` folder exists in container
2. **Subfolder Structure**: `indicators` subfolder exists
3. **File Presence**: `SCHR_VWAP.mq5` file exists
4. **File Content**: File contains expected MQL5 code
5. **Permissions**: Folders and files are readable
6. **Mount Point**: Volume is properly mounted

## Manual Verification

You can manually verify the setup:

```bash
# Enter the container
docker-compose run --rm neozork-hld bash

# Check the folder structure
ls -la /app/mql5_feed/
ls -la /app/mql5_feed/indicators/

# Check file content
head -20 /app/mql5_feed/indicators/SCHR_VWAP.mq5

# Run a simple test
python -c "
from pathlib import Path
mql5_path = Path('/app/mql5_feed')
print(f'mql5_feed exists: {mql5_path.exists()}')
print(f'indicators exists: {(mql5_path / \"indicators\").exists()}')
print(f'VWAP file exists: {(mql5_path / \"indicators\" / \"SCHR_VWAP.mq5\").exists()}')
"
```

## Configuration Files

The following files are involved in the setup:

- `docker-compose.yml`: Volume mount configuration
- `Dockerfile`: Container build configuration
- `.dockerignore`: Files to exclude from build
- `tests/docker/test_mql5_feed_access.py`: Main test file
- `tests/docker/test_container_mql5_feed_paths.py`: Diagnostic test file
- `scripts/docker/test_mql5_feed_in_container.sh`: Bash diagnostic script 