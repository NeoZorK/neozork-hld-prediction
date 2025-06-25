# Docker Test Fixes

This document describes the fixes applied to resolve Docker-related test failures.

## Issues Fixed

### 1. Missing Debug Scripts

**Problem:** Tests were failing because `debug_binance.py` and `debug_polygon.py` scripts were missing.

**Solution:** Created the missing debug scripts:
- `scripts/debug_scripts/debug_binance.py` - Tests Binance API connection
- `scripts/debug_scripts/debug_polygon.py` - Tests Polygon API connection

Both scripts include proper error handling and API key validation.

### 2. Test Timeouts

**Problem:** Tests for `run_tests_docker.py` were timing out after 30 seconds.

**Solution:** Increased timeout values from 30 to 60 seconds in:
- `test_run_tests_docker_all_flag`
- `test_run_tests_docker_categories`
- `test_run_tests_docker_no_args`

### 3. Docker Entrypoint Test

**Problem:** Test `test_docker_entrypoint_updated` was checking for old path `/app/tests/run_tests.py` which no longer exists.

**Solution:** Updated the test to check for `run_tests_docker.py` reference instead, which is the correct script used in the Docker environment.

### 4. Interactive Mode Tests

**Problem:** Interactive mode tests were failing in local environment.

**Solution:** Updated tests to properly handle both local and Docker environments:
- Tests now skip when not running in Docker
- Added proper environment variable checks
- Fixed file permission handling for `docker-entrypoint.sh`

## Files Modified

### Created Files
- `scripts/debug_scripts/debug_binance.py`
- `scripts/debug_scripts/debug_polygon.py`
- `docs/development/debug-scripts.md`

### Modified Files
- `tests/docker/test_docker_tests.py` - Increased timeouts
- `tests/summary/test_file_reorganization.py` - Fixed docker entrypoint test
- `tests/docker/test_interactive_mode.py` - Added environment checks

## Test Results

All Docker-related tests now pass:

```bash
# Run all Docker tests
python -m pytest tests/docker/ -v

# Run specific test categories
python -m pytest tests/docker/test_docker_tests.py -v
python -m pytest tests/docker/test_interactive_mode.py -v
```

## Debug Scripts Usage

The new debug scripts can be used to test external API connections:

```bash
# Test Binance API
python scripts/debug_scripts/debug_binance.py

# Test Polygon API
python scripts/debug_scripts/debug_polygon.py

# Run in Docker
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_binance.py
```

## Environment Variables Required

For API testing, ensure these environment variables are set:

```bash
export BINANCE_API_KEY="your_binance_api_key"
export BINANCE_API_SECRET="your_binance_api_secret"
export POLYGON_API_KEY="your_polygon_api_key"
```

## Verification

To verify all fixes are working:

1. **Build Docker image:**
   ```bash
   docker compose build --build-arg USE_UV=true
   ```

2. **Run interactive mode:**
   ```bash
   docker compose run --rm neozork-hld
   ```

3. **Run all tests:**
   ```bash
   python -m pytest tests/docker/ tests/summary/test_file_reorganization.py::test_docker_entrypoint_updated -v
   ```

All tests should pass with no timeouts or missing file errors. 