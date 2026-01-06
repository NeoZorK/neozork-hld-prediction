# Manual Verification Guide

## Overview

This guide contains step-by-step instructions for manually verifying all project components after upgrading to Python 3.14.

---

## 1. Native Environment Verification

### 1.1 Environment Check

```bash
# Check Python version
python3.14 --version
# Expected: Python 3.14.2

# Check uv
uv --version
# Expected: uv 0.9.21 or higher

# Check installed dependencies
source .venv/bin/activate  # or your virtual environment
uv pip list | head -20
```

### 1.2 Key Dependencies Check

```bash
source .venv/bin/activate

# Check core libraries
python -c "import pydantic; print(f'pydantic {pydantic.__version__}')"
python -c "import fastapi; print(f'fastapi {fastapi.__version__}')"
python -c "import pyparsing; print(f'pyparsing {pyparsing.__version__}')"
python -c "import pandas, numpy, sklearn; print('ML libraries OK')"
```

**Expected versions:**
- pydantic >= 2.12.0
- fastapi >= 0.115.0
- pyparsing >= 3.3.1

### 1.3 Running Tests Natively

```bash
source .venv/bin/activate

# All tests
uv run pytest tests -n auto -v

# By category
uv run pytest tests/common/ -v
uv run pytest tests/unit/ -v
uv run pytest tests/data/ -v
uv run pytest tests/calculation/ -v
uv run pytest tests/cli/ -v
uv run pytest tests/plotting/ -v
uv run pytest tests/integration/ -v
```

### 1.4 Main Programs Check

```bash
source .venv/bin/activate

# Main analysis
python run_analysis.py --help
python run_analysis.py demo --rule PHLD

# Interactive system
python src/interactive/neozork.py --help

# MCP server (if available)
python neozork_mcp_server.py --help
```

---

## 2. Docker Environment Verification

### 2.1 Docker Preparation

```bash
# Stop existing containers
docker-compose down

# Rebuild images
docker-compose build --no-cache

# Check build success
docker images | grep neozork
```

### 2.2 Starting Containers

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# Check logs
docker-compose logs --tail=50
```

### 2.3 Docker Environment Check

```bash
# Check Python version
docker-compose exec neozork-hld python --version
# Expected: Python 3.14.x

# Check uv
docker-compose exec neozork-hld uv --version

# Check dependencies
docker-compose exec neozork-hld uv pip list | head -20

# Check environment variables
docker-compose exec neozork-hld env | grep -E "(PYTHON|UV|DOCKER)"
```

### 2.4 Running Tests in Docker

```bash
# Sequential tests (recommended)
docker-compose exec neozork-hld python scripts/run_sequential_tests_docker.py

# Direct run of all tests
docker-compose exec neozork-hld uv run pytest tests -c pytest-docker.ini -n auto

# Docker-specific tests
docker-compose exec neozork-hld uv run pytest tests/docker/ -v
```

### 2.5 Programs Check in Docker

```bash
# Main analysis
docker-compose exec neozork-hld python run_analysis.py --help
docker-compose exec neozork-hld python run_analysis.py demo --rule PHLD

# Interactive system
docker-compose exec neozork-hld python src/interactive/neozork.py --help

# MCP server
docker-compose exec neozork-hld python scripts/mcp/check_mcp_status.py

# Database connection
docker-compose exec neozork-hld python -c "import psycopg2; conn = psycopg2.connect('postgresql://neozork_user:neozork_password@postgres:5432/neozork_fund'); print('DB OK'); conn.close()"
```

---

## 3. Apple Container Verification

### 3.1 Apple Container Preparation

```bash
# Check tool availability
container list --all

# Check configuration
cat container.yaml | grep python
# Expected: python:3.14-slim
```

### 3.2 Starting Apple Container

```bash
# Use interactive script
./scripts/native-container/native-container.sh

# Or manually
./scripts/native-container/setup.sh
./scripts/native-container/run.sh
./scripts/native-container/exec.sh --shell
```

### 3.3 Apple Container Environment Check

```bash
# Inside container
python --version
# Expected: Python 3.14.x

uv --version
uv pip list | head -20
```

### 3.4 Running Tests in Apple Container

```bash
# Inside container
uv run pytest tests -n auto

# Sequential tests
python scripts/run_sequential_tests_docker.py

# Native-container tests
uv run pytest tests/native-container/ -v
```

### 3.5 Programs Check in Apple Container

```bash
# Inside container
python run_analysis.py --help
python run_analysis.py demo --rule PHLD
python src/interactive/neozork.py --help
```

---

## 4. Quick Verification (Checklist)

### Minimal Command Set

```bash
# 1. Native environment
source .venv/bin/activate
python --version
python -c "import pydantic, fastapi; print('OK')"
uv run pytest tests/common/ -v

# 2. Docker
docker-compose up -d
docker-compose exec neozork-hld python --version
docker-compose exec neozork-hld uv run pytest tests/common/ -v

# 3. Programs
python run_analysis.py --help
docker-compose exec neozork-hld python run_analysis.py --help
```

### Detailed Verification

```bash
# All tests natively
uv run pytest tests -n auto

# All tests in Docker
docker-compose exec neozork-hld python scripts/run_sequential_tests_docker.py

# All programs
python run_analysis.py demo --rule PHLD
python src/interactive/neozork.py --help
docker-compose exec neozork-hld python run_analysis.py demo --rule PHLD
```

---

## 5. Performance Verification

### Execution Time Comparison

```bash
# Native
time uv run pytest tests/common/ -v

# Docker
time docker-compose exec neozork-hld uv run pytest tests/common/ -v
```

### Memory Usage Check

```bash
# Native
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"

# Docker
docker stats neozork-hld-prediction-neozork-hld-1 --no-stream
```

---

## 6. Troubleshooting

### Issue: Dependencies Not Installing

```bash
# Clear cache
uv cache clean

# Reinstall
uv pip install -r requirements.txt --upgrade --force-reinstall
```

### Issue: Docker Not Building

```bash
# Clean Docker
docker system prune -a

# Rebuild
docker-compose build --no-cache --pull
```

### Issue: Tests Not Passing

```bash
# Run with verbose output
uv run pytest tests/ -v --tb=long

# Run only failed tests
uv run pytest tests/ --lf
```

---

## 7. Success Criteria

✅ Python 3.14 installed and working  
✅ All key dependencies installed  
✅ Tests pass natively  
✅ Docker images build  
✅ Tests pass in Docker  
✅ All programs start  
✅ Apple Container works (if available)  

---

## 8. Contacts and Support

If you encounter problems:
1. Check logs: `docker-compose logs`
2. Check report: `docs/testing/python-3.14-upgrade-report-EN.md`
3. Check backup: `docs/testing/pre-python-3.14-dependencies-backup.txt`

