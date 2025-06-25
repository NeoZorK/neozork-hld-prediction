# Docker Examples

Examples for using Docker with the project.

## Overview

The project includes Docker support for:

- **Containerized Development** - Consistent development environment
- **Production Deployment** - Scalable deployment options
- **Data Mounting** - Persistent data storage
- **Multi-stage Builds** - Optimized container images
- **Service Orchestration** - Docker Compose integration

## Basic Docker Commands

### Build and Run
```bash
# Build and run container
docker compose up --build

# Build without cache
docker compose build --no-cache

# Run in detached mode
docker compose up -d

# Stop containers
docker compose down

# View logs
docker compose logs neozork-hld
```

### Interactive Sessions
```bash
# Interactive session in container
docker compose run --rm neozork-hld bash

# Run with specific user
docker compose run --rm -u $(id -u):$(id -g) neozork-hld bash

# Run with environment variables
docker compose run --rm -e DEBUG=1 neozork-hld bash

# Run with working directory
docker compose run --rm -w /app/src neozork-hld bash
```

## Data Analysis in Docker

### Demo Analysis
```bash
# Run demo in container
docker compose run --rm neozork-hld python run_analysis.py demo

# Demo with specific indicator
docker compose run --rm neozork-hld python run_analysis.py demo --rule RSI

# Demo with different backends
docker compose run --rm neozork-hld python run_analysis.py demo -d plotly
docker compose run --rm neozork-hld python run_analysis.py demo -d seaborn
docker compose run --rm neozork-hld python run_analysis.py demo -d term
```

### Real Data Analysis
```bash
# Yahoo Finance analysis
docker compose run --rm neozork-hld python run_analysis.py yf -t AAPL --period 1mo --point 0.01

# CSV analysis
docker compose run --rm neozork-hld python run_analysis.py csv --csv-file data.csv --point 0.01

# Binance analysis
docker compose run --rm neozork-hld python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01
```

### Interactive Mode
```bash
# Interactive mode in container
docker compose run --rm neozork-hld python run_analysis.py --interactive

# Interactive mode with alias
docker compose run --rm neozork-hld nz --interactive
```

## Data Mounting

### Mount Data Directory
```bash
# Mount data directory
docker compose run --rm -v $(pwd)/data:/app/data neozork-hld python run_analysis.py csv --csv-file data.csv

# Mount with read-only
docker compose run --rm -v $(pwd)/data:/app/data:ro neozork-hld python run_analysis.py csv --csv-file data.csv

# Mount specific files
docker compose run --rm -v $(pwd)/data/file.csv:/app/data/file.csv neozork-hld python run_analysis.py csv --csv-file data/file.csv
```

### Mount Results Directory
```bash
# Mount results directory
docker compose run --rm -v $(pwd)/results:/app/results neozork-hld python run_analysis.py demo --export-parquet

# Mount with custom permissions
docker compose run --rm -v $(pwd)/results:/app/results:rw neozork-hld python run_analysis.py demo --export-parquet

# Mount multiple directories
docker compose run --rm -v $(pwd)/data:/app/data -v $(pwd)/results:/app/results neozork-hld python run_analysis.py demo --export-parquet
```

### Mount Configuration
```bash
# Mount configuration files
docker compose run --rm -v $(pwd)/config:/app/config neozork-hld python run_analysis.py demo

# Mount with environment variables
docker compose run --rm -v $(pwd)/config:/app/config -e CONFIG_PATH=/app/config neozork-hld python run_analysis.py demo
```

## Testing in Docker

### Run Tests
```bash
# Run all tests in container
docker compose run --rm neozork-hld python -m pytest tests/

# Run specific test categories
docker compose run --rm neozork-hld python -m pytest tests/calculation/ -v
docker compose run --rm neozork-hld python -m pytest tests/cli/ -v
docker compose run --rm neozork-hld python -m pytest tests/data/ -v

# Run with coverage
docker compose run --rm neozork-hld python -m pytest tests/ --cov=src --cov-report=html
```

### Test Coverage Analysis
```bash
# Analyze test coverage in container
docker compose run --rm neozork-hld python tests/zzz_analyze_test_coverage.py

# Analyze with verbose output
docker compose run --rm neozork-hld python tests/zzz_analyze_test_coverage.py --verbose
```

### MCP Server Testing
```bash
# Test stdio mode in container
docker compose run --rm neozork-hld python tests/test_stdio.py

# Test MCP functionality
docker compose run --rm neozork-hld python -m pytest tests/mcp/ -v
```

## MCP Servers in Docker

### Auto-start MCP Servers
```bash
# Start MCP servers in container
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py

# Start with configuration
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py --config mcp_auto_config.json

# Start in debug mode
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py --debug

# Show server status
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py --status
```

### Manual MCP Server Management
```bash
# Start PyCharm GitHub Copilot MCP server
docker compose run --rm neozork-hld python pycharm_github_copilot_mcp.py

# Start with stdio mode
docker compose run --rm neozork-hld python pycharm_github_copilot_mcp.py --stdio

# Start with debug logging
docker compose run --rm neozork-hld python pycharm_github_copilot_mcp.py --debug
```

## Scripts in Docker

### Utility Scripts
```bash
# Fix imports in container
docker compose run --rm neozork-hld python scripts/fix_imports.py

# Create test data in container
docker compose run --rm neozork-hld python scripts/create_test_parquet.py

# Analyze requirements in container
docker compose run --rm neozork-hld python scripts/analyze_requirements.py
```

### Debug Scripts
```bash
# Debug Binance connection in container
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_binance_connection.py

# Check Parquet files in container
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_check_parquet.py

# Debug indicators in container
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_indicators.py

# Debug CLI in container
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_cli.py
```

## EDA in Docker

### Basic EDA
```bash
# Run EDA script in container
docker compose run --rm neozork-hld bash eda

# EDA with UV in container
docker compose run --rm neozork-hld uv run ./eda

# EDA with verbose output
docker compose run --rm neozork-hld bash eda --verbose

# EDA with export results
docker compose run --rm neozork-hld bash eda --export-results
```

### EDA with Data Mounting
```bash
# EDA with mounted data
docker compose run --rm -v $(pwd)/data:/app/data neozork-hld bash eda

# EDA with mounted results
docker compose run --rm -v $(pwd)/results:/app/results neozork-hld bash eda --export-results
```

## Performance Optimization

### Resource Limits
```bash
# Run with memory limit
docker compose run --rm --memory=2g neozork-hld python run_analysis.py demo

# Run with CPU limit
docker compose run --rm --cpus=2 neozork-hld python run_analysis.py demo

# Run with both limits
docker compose run --rm --memory=2g --cpus=2 neozork-hld python run_analysis.py demo
```

### Fastest Backend
```bash
# Use fastest backend for large datasets
docker compose run --rm neozork-hld python run_analysis.py demo -d fastest

# Use terminal backend for SSH/Docker
docker compose run --rm neozork-hld python run_analysis.py demo -d term
```

## Multi-stage Builds

### Development Build
```bash
# Build development image
docker build -f Dockerfile.dev -t neozork-hld:dev .

# Run development image
docker run --rm -v $(pwd):/app neozork-hld:dev python run_analysis.py demo
```

### Production Build
```bash
# Build production image
docker build -f Dockerfile.prod -t neozork-hld:prod .

# Run production image
docker run --rm neozork-hld:prod python run_analysis.py demo
```

## Docker Compose Services

### Multiple Services
```yaml
# docker-compose.yml example
version: '3.8'
services:
  neozork-hld:
    build: .
    volumes:
      - ./data:/app/data
      - ./results:/app/results
    environment:
      - DEBUG=0
    ports:
      - "8000:8000"
  
  mcp-server:
    build: .
    command: python scripts/auto_start_mcp.py
    volumes:
      - ./config:/app/config
    environment:
      - MCP_DEBUG=1
```

### Service Orchestration
```bash
# Start all services
docker compose up -d

# Start specific service
docker compose up -d neozork-hld

# Scale services
docker compose up -d --scale neozork-hld=3

# View service logs
docker compose logs -f neozork-hld
```

## Environment Variables

### Development Environment
```bash
# Run with development environment
docker compose run --rm -e ENV=development neozork-hld python run_analysis.py demo

# Run with debug mode
docker compose run --rm -e DEBUG=1 neozork-hld python run_analysis.py demo

# Run with custom configuration
docker compose run --rm -e CONFIG_PATH=/app/config neozork-hld python run_analysis.py demo
```

### Production Environment
```bash
# Run with production environment
docker compose run --rm -e ENV=production neozork-hld python run_analysis.py demo

# Run with optimized settings
docker compose run --rm -e OPTIMIZE=1 neozork-hld python run_analysis.py demo

# Run with logging configuration
docker compose run --rm -e LOG_LEVEL=INFO neozork-hld python run_analysis.py demo
```

## Networking

### Port Mapping
```bash
# Map specific port
docker compose run --rm -p 8000:8000 neozork-hld python run_analysis.py demo

# Map multiple ports
docker compose run --rm -p 8000:8000 -p 8080:8080 neozork-hld python run_analysis.py demo
```

### Network Configuration
```bash
# Use specific network
docker compose run --rm --network=host neozork-hld python run_analysis.py demo

# Create custom network
docker network create neozork-network
docker compose run --rm --network=neozork-network neozork-hld python run_analysis.py demo
```

## Troubleshooting

### Common Issues
```bash
# Issue: Permission denied
docker compose run --rm -u $(id -u):$(id -g) neozork-hld python run_analysis.py demo

# Issue: Container not starting
docker compose logs neozork-hld
docker compose run --rm neozork-hld bash

# Issue: Data not persisting
docker compose run --rm -v $(pwd)/data:/app/data:rw neozork-hld python run_analysis.py demo

# Issue: Memory problems
docker compose run --rm --memory=4g neozork-hld python run_analysis.py demo
```

### Debug Mode
```bash
# Run with debug output
docker compose run --rm -e DEBUG=1 neozork-hld python run_analysis.py demo

# Run with verbose logging
docker compose run --rm -e VERBOSE=1 neozork-hld python run_analysis.py demo

# Run with shell access
docker compose run --rm neozork-hld bash
```

### Container Inspection
```bash
# Inspect running container
docker compose ps
docker inspect $(docker compose ps -q neozork-hld)

# Check container resources
docker stats $(docker compose ps -q neozork-hld)

# Check container logs
docker compose logs -f neozork-hld
```

## Advanced Usage

### Custom Dockerfile
```dockerfile
# Custom Dockerfile example
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV DEBUG=0

# Expose port
EXPOSE 8000

# Default command
CMD ["python", "run_analysis.py", "demo"]
```

### Docker Compose Override
```yaml
# docker-compose.override.yml
version: '3.8'
services:
  neozork-hld:
    volumes:
      - ./data:/app/data
      - ./results:/app/results
    environment:
      - DEBUG=1
    ports:
      - "8000:8000"
```

### Health Checks
```yaml
# Health check configuration
services:
  neozork-hld:
    healthcheck:
      test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
      interval: 30s
      timeout: 10s
      retries: 3
```

---

📚 **Additional Resources:**
- **[Usage Examples](usage-examples.md)** - Comprehensive usage examples
- **[Quick Examples](quick-examples.md)** - Fast start examples
- **[Indicator Examples](indicator-examples.md)** - Technical indicator examples
- **[MCP Examples](mcp-examples.md)** - MCP server examples
- **[Testing Examples](testing-examples.md)** - Testing examples
- **[Script Examples](script-examples.md)** - Utility script examples
- **[EDA Examples](eda-examples.md)** - EDA examples 