# Docker Setup Guide

## Overview

This guide covers setting up and running the NeoZork HLD Prediction project using Docker containers for cross-platform development and deployment.

> ⚠️ **Version Information**: v0.5.2 is the last version that supports Docker and Apple Container. Current version: v0.5.3

## Prerequisites

> **Note**: Docker support is limited to v0.5.2 and earlier versions.

- **Docker Desktop** installed and running
- **Docker Compose** (included with Docker Desktop)
- **At least 4GB of available RAM**
- **10GB of available disk space**

## Quick Start

### 1. Build the Docker Image

```bash
# Build with UV package manager (recommended)
docker compose build --build-arg USE_UV=true

# Or build with pip package manager
docker compose build --build-arg USE_UV=false
```

### 2. Run the Container

```bash
# Start interactive container
docker compose run --rm neozork-hld

# Or start in background
docker compose up -d
```

## Configuration

### Environment Variables

The project uses `docker.env` file for configuration. Key variables:

```bash
# Package manager selection
USE_UV=true

# Python configuration
PYTHONPATH=/app
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1

# MCP Server configuration
MCP_SERVER_TYPE=pycharm_copilot

# Logging
LOG_LEVEL=INFO
LOG_FILE=/app/logs/docker.log
```

### Volume Mounts

The following directories are mounted from host to container:

- `./data` → `/app/data` - Data files and cache
- `./logs` → `/app/logs` - Log files
- `./mql5_feed` → `/app/mql5_feed` - MQL5 data feed
- `./results` → `/app/results` - Analysis results and plots
- `./tests` → `/app/tests` - Test files

## Usage

### Interactive Mode

When you start the container, you'll be prompted to:

1. **Run external data feed tests** - Tests connectivity to Polygon, YFinance, Binance
2. **Start MCP server** - Enables enhanced LLM support

### Available Commands

Inside the container, you can use:

```bash
# Main analysis command
nz demo --rule PHLD
nz yfinance AAPL --rule PHLD
nz mql5 BTCUSD --interval H4 --rule PHLD

# EDA analysis
eda

# Direct Python execution
python run_analysis.py demo --rule PHLD

# Run tests
pytest

# View generated plots
ls results/plots/
```

### Viewing Results

Generated HTML plots are saved to `results/plots/`. To view them:

1. **Docker Desktop**: 
   - Open Docker Desktop
   - Navigate to the container
   - Access the files through the file browser

2. **Host System**:
   - Results are automatically synced to `./results/plots/` on your host system
   - Open the HTML files in your web browser

## UV Package Management

### UV-Only Mode

The Docker container is configured to use **UV package manager exclusively**:

```dockerfile
# Force UV usage - no fallback to pip
ARG USE_UV=true
ARG UV_ONLY=true

# Install uv - required for UV-only mode
RUN mkdir -p /tmp/uv-installer \
    && curl -sSL https://github.com/astral-sh/uv/releases/latest/download/uv-installer.sh -o /tmp/uv-installer/installer.sh \
    && chmod +x /tmp/uv-installer/installer.sh \
    && /tmp/uv-installer/installer.sh \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv

# Install dependencies using UV only - no pip fallback
RUN uv pip install --no-cache -r requirements.txt
```

### UV Commands in Container

```bash
# Install dependencies
uv-install

# Update dependencies
uv-update

# Test UV environment
uv-test

# Run tests with UV
uv-pytest
```

## Testing

### Docker Environment Tests

> **Note**: Docker testing is limited to v0.5.2 and earlier versions.

```bash
# Run all tests
pytest tests/ -v

# Run Docker-specific tests
pytest tests/docker/ -v

# Run UV-only mode tests
pytest tests/docker/test_uv_only_mode.py -v
```

### Test Categories

- **UV-Specific Tests**: Package manager validation
- **Environment Tests**: Docker vs local detection
- **Integration Tests**: End-to-end functionality
- **Performance Tests**: UV vs pip comparison

## Troubleshooting

### Common Issues

**Build Issues:**
```bash
# Clean build
docker compose build --no-cache

# Check Docker logs
docker compose logs
```

**Permission Errors:**
```bash
# Fix file permissions
chmod +x docker-entrypoint.sh
chmod +x scripts/*.sh
```

**Container Won't Start:**
```bash
# Check container status
docker compose ps

# View logs
docker compose logs -f

# Clean restart
docker compose down -v
docker system prune -a
docker compose up --build
```

### Performance Issues

**Memory Issues:**
```bash
# Increase Docker memory limit in Docker Desktop
# Recommended: 4GB minimum, 8GB preferred
```

**Disk Space:**
```bash
# Clean up Docker system
docker system prune -a
docker volume prune
```

## Advanced Configuration

### Custom Dockerfile

You can create a custom Dockerfile for specific requirements:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set environment variables
ENV USE_UV=true
ENV UV_ONLY=true

# Copy project files
COPY . /app
WORKDIR /app

# Install dependencies
RUN uv pip install -r requirements.txt

# Expose port (if needed)
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["./docker-entrypoint.sh"]
```

### Docker Compose Override

Create `docker-compose.override.yml` for development:

```yaml
version: '3.8'
services:
  neozork-hld:
    volumes:
      - .:/app
      - /app/.venv  # Exclude virtual environment
    environment:
      - PYTHONPATH=/app
      - LOG_LEVEL=DEBUG
    ports:
      - "8000:8000"  # Expose port for development
```

## Comparison with Local Setup

| Aspect | Docker Setup | Local Setup |
|--------|--------------|-------------|
| **Performance** | Container overhead | Native performance |
| **Setup Time** | 15-30 minutes | 5-10 minutes |
| **Resource Usage** | Higher | Lower |
| **Platform Support** | Cross-platform | All platforms |
| **Maintenance** | More complex | Easier |
| **Version Support** | Limited to v0.5.2 | Current version |

> **Note**: Docker setup is limited to v0.5.2 and earlier versions. Local setup is currently recommended for all users.

## Related Documentation

- **[Getting Started](../getting-started/)** - Basic setup
- **[Local Setup](local-setup.md)** - Local development setup
- **[UV Package Management](uv-package-management.md)** - UV usage guide
- **[Testing](../testing/)** - Testing framework
- **[Containers](../containers/)** - Container documentation
- **[MCP Server Integration](mcp-server-docker-integration.md)** - MCP server setup
