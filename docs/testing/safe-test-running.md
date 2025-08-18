# Safe Test Running Guide

This guide explains how to run tests safely to prevent freezing issues in both Docker and native environments.

## Problem

When running `uv run pytest tests -n auto`, tests may freeze at around 90% completion, especially in native environments. This is typically caused by:

1. **Multithreading issues** with matplotlib in plotting tests
2. **Resource exhaustion** with too many workers
3. **Deadlocks** in test execution

## Solutions

### 1. Safe Test Runner Scripts

We provide several scripts for safe test execution:

#### `scripts/run_tests_safe.sh`
Runs tests with limited workers (4) to prevent freezing:
```bash
./scripts/run_tests_safe.sh [pytest_args...]
```

#### `scripts/run_all_tests_safe.sh`
Runs all tests with timeout protection:
```bash
./scripts/run_all_tests_safe.sh [timeout_seconds]
```

#### `scripts/run_tests_with_timeout.sh`
Runs tests with custom timeout:
```bash
./scripts/run_tests_with_timeout.sh [timeout_seconds] [pytest_args...]
```

### 2. Manual Safe Commands

#### Limited Workers
```bash
uv run pytest tests -n 4 --dist=worksteal --max-worker-restart=3
```

#### Single Thread (Safest)
```bash
uv run pytest tests -n 0
```

#### Specific Test Categories
```bash
# Only unit tests
uv run pytest tests/calculation/ -n 4

# Only CLI tests
uv run pytest tests/cli/ -n 4

# Skip plotting tests
uv run pytest tests -m "not plotting" -n auto
```

### 3. Environment-Specific Solutions

#### Docker Environment
Tests automatically skip problematic plotting tests in Docker:
```bash
docker exec container-name uv run pytest tests -n auto
```

#### Native Environment
Use safe scripts or limited workers:
```bash
./scripts/run_tests_safe.sh
```

## Test Categories and Recommendations

### Fast Tests (Safe with auto workers)
- Unit tests (`tests/calculation/`)
- CLI tests (`tests/cli/`)
- Data tests (`tests/data/`)

### Medium Risk Tests (Use 4 workers)
- Integration tests
- Export tests
- Some plotting tests

### High Risk Tests (Use single thread)
- Complex plotting tests
- Tests with large datasets
- Tests with matplotlib operations

## Configuration

### pytest.ini Settings
```ini
# Safe settings
addopts = 
    -n auto
    --dist=worksteal
    --max-worker-restart=5
    --maxfail=10
```

### Environment Variables
```bash
# Force single thread
export PYTEST_XDIST_WORKER_COUNT=1

# Limit workers
export PYTEST_XDIST_WORKER_COUNT=4
```

## Troubleshooting

### Tests Still Freeze
1. Use single thread: `uv run pytest tests -n 0`
2. Skip plotting tests: `uv run pytest tests -m "not plotting"`
3. Use safe script: `./scripts/run_all_tests_safe.sh`

### Memory Issues
1. Reduce worker count: `-n 2`
2. Skip heavy tests: `-m "not slow"`
3. Use timeout: `./scripts/run_tests_with_timeout.sh 300`

### Performance Issues
1. Use more workers: `-n 8` (if stable)
2. Run specific test categories
3. Use parallel execution for fast tests only

## Best Practices

1. **Always use safe scripts** for full test runs
2. **Monitor resource usage** during test execution
3. **Use appropriate worker count** for your system
4. **Skip problematic tests** when needed
5. **Use timeouts** for long-running tests

## Quick Reference

```bash
# Safe full test run
./scripts/run_all_tests_safe.sh

# Fast test run (limited scope)
./scripts/run_tests_safe.sh tests/calculation/

# Emergency stop
pkill -f "uv run pytest"
```
