# NeoZork HLD Prediction - Complete Run and Test Manual

## 🚀 System Overview

Your NeoZork HLD Prediction system includes multiple components:

1. **Main Analysis** (`run_analysis.py`) - Manual charting and indicator visualization
2. **Interactive System** (`src/interactive/`) - ML trading strategies
3. **SaaS Platform** (`src/saas/`) - Cloud platform
4. **Pocket Hedge Fund** (`src/pocket_hedge_fund/`) - Hedge fund
5. **Mobile Application** (`src/mobile_app/`) - React Native app
6. **Admin Panel** (`src/admin_panel/`) - Vue.js admin interface
7. **Monitoring** (`src/monitoring/`) - Monitoring system
8. **Deployment** (`deployment/`) - Docker and K8s configurations

## 📋 System Requirements

### Minimum Requirements
- **Python**: 3.11+
- **Node.js**: 18+
- **Docker**: 20.10+ (optional)
- **UV**: Latest version
- **Memory**: 4GB RAM
- **Disk**: 10GB free space

### Recommended Requirements
- **Python**: 3.12+
- **Node.js**: 20+
- **Docker**: 24+
- **Memory**: 8GB RAM
- **Disk**: 20GB free space

## 🔧 Installation and Setup

### 1. Clone Repository
```bash
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction
```

### 2. Install UV (if not installed)
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### 3. Install Python Dependencies
```bash
# Install all dependencies
uv pip install -r requirements.txt

# Install development dependencies
uv pip install -e ".[dev]"

# Verify installation
uv pip list
```

### 4. Install Node.js Dependencies

#### Mobile Application
```bash
cd src/mobile_app
npm install
cd ..
```

#### Admin Panel
```bash
cd src/admin_panel
npm install
cd ../..
```

### 5. Environment Setup
```bash
# Copy environment file
cp env.example .env

# Edit environment variables
nano .env
```

## 🚀 Running Components

### Main Analysis (run_analysis.py)

#### Demo Analysis
```bash
# Simple demo analysis
uv run run_analysis.py demo --rule PHLD

# Demo with various indicators
uv run run_analysis.py demo --rule RSI,MACD,SMA:20,close

# Demo with different display modes
uv run run_analysis.py demo --rule PHLD -d plotly
uv run run_analysis.py demo --rule PHLD -d fastest
uv run run_analysis.py demo --rule PHLD -d mpl
```

#### Real Data Analysis
```bash
# Yahoo Finance data
uv run run_analysis.py yfinance AAPL --rule RSI
uv run run_analysis.py yfinance MSFT --period 1y --rule MACD

# Binance data
uv run run_analysis.py binance BTCUSDT --interval 1h --rule PHLD

# Polygon data
uv run run_analysis.py polygon AAPL --interval 1 --rule SMA:20,close

# CSV data
uv run run_analysis.py show csv mn1 --rule RSI -d fastest
```

#### Interactive Mode
```bash
# Launch interactive mode
uv run run_analysis.py interactive

# Interactive mode with preset parameters
uv run run_analysis.py interactive --input-file data/mn1.csv
```

### Interactive System

#### Run via Python
```bash
# Direct run
uv run python src/interactive/neozork.py

# Run with debugging
uv run python -u src/interactive/neozork.py
```

#### Run via nz Script
```bash
# Interactive mode
./nz interactive

# Demo mode
./nz demo

# Data analysis
./nz analyze --csv-file data/mn1.csv --rule RSI
```

### SaaS Platform

#### Launch SaaS Platform
```bash
# Run with default settings
uv run python run_saas.py

# Run with custom settings
SAAS_HOST=0.0.0.0 SAAS_PORT=8080 uv run python run_saas.py

# Run in background
nohup uv run python run_saas.py > logs/saas.log 2>&1 &
```

#### Access SaaS Platform
- **Main Interface**: http://localhost:8080
- **API Documentation**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **Health Check**: http://localhost:8080/health

### Pocket Hedge Fund

#### Launch Hedge Fund
```bash
# Run with default settings
uv run python run_pocket_hedge_fund.py

# Run with custom settings
HOST=0.0.0.0 PORT=8080 DEBUG=true uv run python run_pocket_hedge_fund.py

# Run in background
nohup uv run python run_pocket_hedge_fund.py > logs/pocket_hedge_fund.log 2>&1 &
```

#### Access Pocket Hedge Fund
- **Main Interface**: http://localhost:8080
- **API Documentation**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **Health Check**: http://localhost:8080/health

### Mobile Application

#### Launch React Native Application
```bash
cd src/mobile_app

# Install dependencies
npm install

# Start Metro bundler
npm start

# Run on iOS (requires Xcode)
npm run ios

# Run on Android (requires Android Studio)
npm run android

# Run in web browser
npm run web
```

#### Access Mobile Application
- **Metro Bundler**: http://localhost:8081
- **iOS Simulator**: Opens automatically
- **Android Emulator**: Opens automatically
- **Web Browser**: http://localhost:19006

### Admin Panel

#### Launch Vue.js Admin Panel
```bash
cd src/admin_panel

# Install dependencies
npm install

# Run in development mode
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

#### Access Admin Panel
- **Development Mode**: http://localhost:3000
- **Production Build**: http://localhost:4173

### Monitoring System

#### Launch Monitoring
```bash
# Launch monitoring system
uv run python -m src.monitoring.system_monitor

# Run with custom settings
MONITORING_PORT=9090 uv run python -m src.monitoring.system_monitor

# Run in background
nohup uv run python -m src.monitoring.system_monitor > logs/monitoring.log 2>&1 &
```

#### Access Monitoring
- **Prometheus Metrics**: http://localhost:9090/metrics
- **Health Check**: http://localhost:9090/health
- **Grafana Dashboard**: http://localhost:3001 (if configured)

## 🧪 Testing

### Running All Tests

#### Multithreaded Testing
```bash
# All tests with automatic thread detection
uv run pytest tests -n auto

# All tests with specific thread count
uv run pytest tests -n 4

# All tests with verbose output
uv run pytest tests -n auto -v
```

#### Safe Testing
```bash
# Safe mode (limited threads)
./scripts/run_tests_safe.sh

# Safe mode with specific tests
./scripts/run_tests_safe.sh tests/calculation/

# Safe mode with timeout
./scripts/run_tests_with_timeout.sh
```

#### Automatic Environment Detection
```bash
# Automatic Docker/Local environment detection
./scripts/run_all_tests.sh

# Run with logging
./scripts/run_all_tests.sh 2>&1 | tee test_results.log
```

### Testing by Categories

#### Core Tests
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

#### Component Tests
```bash
# SaaS platform tests
uv run pytest tests/saas/ -n auto -v

# Pocket Hedge Fund tests
uv run pytest tests/pocket_hedge_fund/ -n auto -v

# Interactive system tests
uv run pytest tests/interactive/ -n auto -v

# Monitoring tests
uv run pytest tests/monitoring/ -n auto -v
```

#### Deployment Tests
```bash
# Docker tests
uv run pytest tests/docker/ -n auto -v

# Native container tests
uv run pytest tests/native-container/ -n auto -v

# Integration tests
uv run pytest tests/integration/ -n auto -v
```

### Testing with Coverage

#### Basic Coverage
```bash
# Tests with code coverage
uv run pytest tests/ --cov=src -n auto

# Coverage with HTML report
uv run pytest tests/ --cov=src --cov-report=html -n auto

# Coverage with XML report
uv run pytest tests/ --cov=src --cov-report=xml -n auto
```

#### Detailed Coverage
```bash
# Coverage with missing lines
uv run pytest tests/ --cov=src --cov-report=html --cov-report=term-missing -n auto

# Coverage for specific modules
uv run pytest tests/ --cov=src.calculation --cov=src.cli -n auto

# Coverage with minimum threshold
uv run pytest tests/ --cov=src --cov-fail-under=80 -n auto
```

### Specialized Testing

#### Performance Tests
```bash
# Performance tests
uv run pytest tests/ -m performance -n auto

# Tests with profiling
uv run pytest tests/ --profile -n auto
```

#### Security Tests
```bash
# Security tests
uv run pytest tests/ -m security -n auto

# Authentication tests
uv run pytest tests/pocket_hedge_fund/test_auth_system.py -v
```

#### API Tests
```bash
# API endpoint tests
uv run pytest tests/pocket_hedge_fund/test_api_endpoints.py -v

# SaaS API tests
uv run pytest tests/saas/ -v
```

## 🐳 Docker and Containers

### Docker Compose

#### Launch All Services
```bash
# Run in background
docker-compose up -d

# Run with logging
docker-compose up

# Run specific services
docker-compose up neozork-hld
```

#### Service Management
```bash
# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f neozork-hld

# Execute commands in container
docker-compose exec neozork-hld bash
```

### Apple Silicon Containers

#### Native Container
```bash
# Interactive launch
./scripts/native-container/native-container.sh

# Quick launch
./scripts/native-container/setup.sh && ./scripts/native-container/run.sh

# Check status
./scripts/native-container/run.sh --status

# Execute commands
./scripts/native-container/exec.sh --shell
```

#### Native Container Management
```bash
# Stop
./scripts/native-container/stop.sh

# Force restart
./scripts/native-container/force_restart.sh

# Cleanup
./scripts/native-container/cleanup.sh --all --force

# View logs
./scripts/native-container/logs.sh
```

### Testing in Docker

#### Tests in Docker Container
```bash
# Tests in main container
docker-compose exec neozork-hld uv run pytest tests/ -n auto

# Tests for specific category
docker-compose exec neozork-hld uv run pytest tests/calculation/ -v

# Tests with coverage
docker-compose exec neozork-hld uv run pytest tests/ --cov=src -n auto
```

#### Native Container Tests
```bash
# Enter container
./scripts/native-container/exec.sh --shell

# Inside container:
uv run pytest tests/ -n auto
uv run pytest tests/calculation/ -v
uv run pytest tests/ --cov=src -n auto
```

## 📊 Monitoring and Logs

### Viewing Logs

#### Main Logs
```bash
# Pocket Hedge Fund logs
tail -f logs/pocket_hedge_fund.log

# SaaS platform logs
tail -f logs/saas_platform.log

# Monitoring logs
tail -f logs/monitoring.log

# All logs
tail -f logs/*.log
```

#### Docker Logs
```bash
# Docker container logs
docker-compose logs -f neozork-hld

# All services logs
docker-compose logs -f

# Logs with timestamps
docker-compose logs -f -t neozork-hld
```

#### Native Container Logs
```bash
# View native container logs
./scripts/native-container/logs.sh

# Analyze all logs
./scripts/native-container/analyze_all_logs.sh
```

### System Monitoring

#### Launch Monitoring
```bash
# System monitoring
uv run python -m src.monitoring.system_monitor

# Monitoring with custom settings
MONITORING_PORT=9090 uv run python -m src.monitoring.system_monitor
```

#### Status Checks
```bash
# Health check
curl http://localhost:9090/health

# Prometheus metrics
curl http://localhost:9090/metrics

# Service status
curl http://localhost:8080/health  # SaaS/Pocket Hedge Fund
```

## 🚀 Deployment

### Production Deployment

#### Setup Production Environment
```bash
# Setup production configuration
python deploy/production_setup.py

# Validate configuration
python deploy/production_setup.py --validate

# Create production environment
python deploy/production_setup.py --create
```

#### Launch Production Containers
```bash
# Launch production services
docker-compose -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.prod.yml ps

# View logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Kubernetes Deployment

#### Apply Manifests
```bash
# Apply all manifests
kubectl apply -f k8s/

# Apply specific manifest
kubectl apply -f k8s/neozork-apple-deployment.yaml

# Check status
kubectl get pods
kubectl get services
kubectl get deployments
```

#### Deployment Management
```bash
# Scaling
kubectl scale deployment neozork-app --replicas=3

# Update image
kubectl set image deployment/neozork-app neozork-app=neozork:latest

# Rollback
kubectl rollout undo deployment/neozork-app
```

## 🛠️ Useful Commands

### System Cleanup

#### Cache Cleanup
```bash
# Clean UV cache
uv cache clean

# Clean pip cache
pip cache purge

# Clean npm cache
cd src/mobile_app && npm cache clean --force
cd src/admin_panel && npm cache clean --force
```

#### Docker Cleanup
```bash
# Clean unused containers
docker container prune

# Clean unused images
docker image prune

# Full Docker cleanup
docker system prune -a

# Clean volumes
docker volume prune
```

#### Native Container Cleanup
```bash
# Clean native container
./scripts/native-container/cleanup.sh --all --force

# Clean only logs
./scripts/native-container/cleanup.sh --logs

# Clean only cache
./scripts/native-container/cleanup.sh --cache
```

### Status Checks

#### UV Check
```bash
# Check UV mode
python scripts/utilities/check_uv_mode.py --verbose

# Check installed packages
uv pip list

# Check dependencies
uv pip check
```

#### MCP Check
```bash
# Check MCP server status
python scripts/check_mcp_status.py

# Launch MCP server
python start_mcp_server.py

# Check MCP configuration
python scripts/mcp/check_mcp_status.py
```

#### Docker Check
```bash
# Container status
docker-compose ps

# Image status
docker images

# Volume status
docker volume ls

# Network status
docker network ls
```

### Dependency Updates

#### Python Dependencies
```bash
# Update all dependencies
uv pip install --upgrade -r requirements.txt

# Update specific package
uv pip install --upgrade pandas

# Update development dependencies
uv pip install --upgrade -e ".[dev]"
```

#### Node.js Dependencies
```bash
# Update mobile app
cd src/mobile_app
npm update
npm audit fix
cd ..

# Update admin panel
cd src/admin_panel
npm update
npm audit fix
cd ..
```

## 🆘 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Check PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# Check package installation
uv pip list | grep neozork

# Reinstall package
uv pip install -e .
```

#### UV Issues
```bash
# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clean UV cache
uv cache clean

# Check UV configuration
uv --version
```

#### Docker Issues
```bash
# Rebuild containers
docker-compose build --no-cache

# Restart Docker
sudo systemctl restart docker

# Clean Docker
docker system prune -a
```

#### Test Issues
```bash
# Run tests in safe mode
./scripts/run_tests_safe.sh

# Run tests with debugging
uv run pytest tests/ -v -s

# Run specific test
uv run pytest tests/calculation/test_indicators.py::test_rsi -v
```

### Debug Scripts

#### Data Debugging
```bash
# Debug Yahoo Finance
python scripts/debug/debug_yfinance.py

# Debug Binance
python scripts/debug/debug_binance.py

# Debug Polygon
python scripts/debug/debug_polygon.py

# Debug CSV data
python scripts/debug/debug_csv_reader.py
```

#### Indicator Debugging
```bash
# Debug RSI signals
python scripts/debug/debug_rsi_signals.py

# Debug Wave indicator
python scripts/debug/debug_wave_indicator.py

# Debug signals
python scripts/debug/debug_signals_analysis.py
```

#### System Debugging
```bash
# Debug Docker processes
python scripts/debug_docker_processes.py

# Debug MCP server
python scripts/mcp/debug_mcp_detection.py

# Debug terminal
python scripts/demo_terminal_chunked.py
```

### Getting Help

#### Command Help
```bash
# Main script help
./nz --help

# Analysis help
uv run run_analysis.py --help

# Test help
uv run pytest --help

# Docker help
docker-compose --help
```

#### Logs and Diagnostics
```bash
# View all logs
find logs/ -name "*.log" -exec tail -f {} \;

# Search for errors
grep -r "ERROR" logs/

# Search for warnings
grep -r "WARNING" logs/

# Analyze performance
grep -r "performance" logs/
```

## 📚 Additional Resources

### Documentation
- [API Documentation](docs/api/)
- [Guides](docs/guides/)
- [Examples](docs/examples/)
- [Architecture](docs/architecture/)

### Useful Links
- [UV Documentation](https://docs.astral.sh/uv/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Docker Documentation](https://docs.docker.com/)
- [React Native Documentation](https://reactnative.dev/)
- [Vue.js Documentation](https://vuejs.org/)

### Community
- [GitHub Issues](https://github.com/username/neozork-hld-prediction/issues)
- [Discord Server](https://discord.gg/neozork)
- [Telegram Channel](https://t.me/neozork_hld)

---

**Note**: All commands should be executed from the project root directory (`neozork-hld-prediction/`).

**Documentation Version**: 1.0.0  
**Last Updated**: $(date)  
**Author**: NeoZork Development Team
