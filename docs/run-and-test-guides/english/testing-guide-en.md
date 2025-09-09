# Testing Guide - NeoZork HLD Prediction

## 🧪 Testing Overview

The NeoZork HLD Prediction system includes a comprehensive testing framework with support for:
- Multithreaded testing
- Automatic environment detection
- Code coverage
- Specialized tests

## 🚀 Quick Testing Start

### Run All Tests
```bash
# All tests (multithreaded)
uv run pytest tests -n auto

# Safe mode
./scripts/run_tests_safe.sh

# Automatic environment detection
./scripts/run_all_tests.sh
```

### Testing with Coverage
```bash
# Code coverage
uv run pytest tests/ --cov=src -n auto

# HTML report
uv run pytest tests/ --cov=src --cov-report=html -n auto
```

## 📋 Test Categories

### Core Tests
```bash
# Calculation tests
uv run pytest tests/calculation/ -n auto -v

# CLI tests
uv run pytest tests/cli/ -n auto -v

# Data tests
uv run pytest tests/data/ -n auto -v

# EDA tests
uv run pytest tests/eda/ -n auto -v
```

### Component Tests
```bash
# SaaS tests
uv run pytest tests/saas/ -n auto -v

# Pocket Hedge Fund tests
uv run pytest tests/pocket_hedge_fund/ -n auto -v

# Interactive system tests
uv run pytest tests/interactive/ -n auto -v

# Monitoring tests
uv run pytest tests/monitoring/ -n auto -v
```

### Deployment Tests
```bash
# Docker tests
uv run pytest tests/docker/ -n auto -v

# Native container tests
uv run pytest tests/native-container/ -n auto -v

# Integration tests
uv run pytest tests/integration/ -n auto -v
```

## 🔧 Specialized Testing

### Performance Tests
```bash
# Performance tests
uv run pytest tests/ -m performance -n auto

# Tests with profiling
uv run pytest tests/ --profile -n auto
```

### Security Tests
```bash
# Security tests
uv run pytest tests/ -m security -n auto

# Authentication tests
uv run pytest tests/pocket_hedge_fund/test_auth_system.py -v
```

### API Tests
```bash
# API endpoint tests
uv run pytest tests/pocket_hedge_fund/test_api_endpoints.py -v

# SaaS API tests
uv run pytest tests/saas/ -v
```

## 🐳 Testing in Docker

### Tests in Docker Container
```bash
# Tests in main container
docker-compose exec neozork-hld uv run pytest tests/ -n auto

# Tests for specific category
docker-compose exec neozork-hld uv run pytest tests/calculation/ -v

# Tests with coverage
docker-compose exec neozork-hld uv run pytest tests/ --cov=src -n auto
```

### Native Container Tests
```bash
# Enter container
./scripts/native-container/exec.sh --shell

# Inside container:
uv run pytest tests/ -n auto
uv run pytest tests/calculation/ -v
uv run pytest tests/ --cov=src -n auto
```

## 📊 Results Analysis

### View Results
```bash
# HTML coverage report
open htmlcov/index.html

# XML report
cat coverage.xml

# Text report
uv run pytest tests/ --cov=src --cov-report=term-missing -n auto
```

### Performance Analysis
```bash
# Test profiling
uv run pytest tests/ --profile --profile-svg

# Execution time analysis
uv run pytest tests/ --durations=10
```

## 🛠️ Test Debugging

### Run with Debugging
```bash
# Verbose output
uv run pytest tests/ -v -s

# Stop on first failure
uv run pytest tests/ -x

# Run specific test
uv run pytest tests/calculation/test_indicators.py::test_rsi -v
```

### Debug Scripts
```bash
# Debug tests
python scripts/debug/debug_test_issues.py

# Coverage analysis
python scripts/analysis/generate_test_coverage.py

# Test results management
python scripts/analysis/manage_test_results.py
```

## 📚 Additional Resources

- [Complete Manual](complete-manual-en.md)
- [Quick Start](quick-start-en.md)
- [Deployment Guide](deployment-guide-en.md)
