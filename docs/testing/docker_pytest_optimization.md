# Docker Pytest Optimization

This document describes the optimizations made to prevent pytest worker crashes in Docker environments.

## Problem

When running pytest with parallel execution (`-n auto`) in Docker containers, workers were crashing with the error:
```
[gw1] node down: Not properly terminated
F
replacing crashed worker gw1
```

## Solution

### 1. Comprehensive Warning Suppression

Updated `pytest.ini` to suppress ALL warnings:
- All standard Python warnings (DeprecationWarning, UserWarning, etc.)
- All pytest-specific warnings
- All third-party library warnings (pandas, matplotlib, numpy, etc.)

### 2. Optimized Configuration

- Added timeout settings for stability
- Reduced logging verbosity
- Configured xdist for stable parallel execution
- Set maximum worker count to 2 to prevent crashes

## Usage

### Direct Command Line Usage

**Single-threaded execution (most stable):**
```bash
uv run pytest tests/pocket_hedge_fund/
```

**Limited parallel execution (2 workers):**
```bash
uv run pytest tests/pocket_hedge_fund/ -n 2
```

**Auto parallel execution (now stable with optimizations):**
```bash
uv run pytest tests/pocket_hedge_fund/ -n auto
```

### Environment Variables (Optional)

For optimal Docker performance, you can set these environment variables:
- `PYTHONUNBUFFERED=1` - Immediate output
- `PYTHONDONTWRITEBYTECODE=1` - No .pyc files
- `PYTHONIOENCODING=utf-8` - Proper encoding
- `PYTHONHASHSEED=0` - Reproducible hashing
- `PYTHON_MULTIPROCESSING_START_METHOD=fork` - Stable multiprocessing

## Configuration Files

### pytest.ini
- Comprehensive warning suppression
- Docker-optimized settings
- Timeout configuration
- Minimal logging

### pyproject.toml
- Removed conflicting pytest configuration
- Kept only dependency management

## Troubleshooting

If you still experience worker crashes:

1. Use the single-threaded script: `./scripts/run_docker_tests.sh`
2. Check Docker memory limits
3. Ensure proper environment variables are set
4. Consider reducing the number of parallel workers further

## Performance Notes

- Single-threaded execution is slower but most stable
- Limited parallel execution (2 workers) provides a good balance
- Full parallel execution (`-n auto`) is not recommended in Docker
