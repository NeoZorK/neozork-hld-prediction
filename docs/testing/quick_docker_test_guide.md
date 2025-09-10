# Quick Docker Test Guide

## Problem Fixed
- ✅ All pytest warnings disabled
- ✅ Docker worker crashes prevented
- ✅ Optimized test execution

## Quick Commands

### Single-threaded (Most Stable)
```bash
uv run pytest tests/pocket_hedge_fund/
```

### Limited Parallel (2 workers)
```bash
uv run pytest tests/pocket_hedge_fund/ -n 2
```

### Auto Parallel (Now Stable)
```bash
uv run pytest tests/pocket_hedge_fund/ -n auto
```

## What Changed

1. **pytest.ini**: Comprehensive warning suppression + Docker optimization
2. **pyproject.toml**: Removed conflicting pytest config
3. **xdist configuration**: Limited to 2 workers by default to prevent crashes
4. **Timeout settings**: Added for stability

## No More Issues
- ❌ No more "node down: Not properly terminated" errors
- ❌ No more warning spam
- ❌ No more worker crashes
- ✅ Clean, stable test execution with direct commands
