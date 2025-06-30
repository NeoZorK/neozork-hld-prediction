# Docker Setup and Usage

This document provides comprehensive instructions for setting up and running the NeoZork HLD Prediction project using Docker.

## Prerequisites

- Docker Desktop installed and running
- At least 4GB of available RAM
- 10GB of available disk space

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
   - Select your running container
   - Go to "Press ... → View Files → Bind Mounts"
   - Navigate to the volume mapped to `/app/results`
   - Open HTML files in the `plots` folder

2. **Host System**: 
   - Plots are automatically available in `./results/plots/` on your host
   - Open HTML files with any web browser

## Troubleshooting

### Common Issues

1. **Build fails with missing files**
   - Ensure all required files are present in the project root
   - Check that `pycharm_github_copilot_mcp.py` exists

2. **Permission errors**
   - The container runs as non-root user `neozork`
   - All necessary directories have proper permissions

3. **MCP server issues**
   - Check logs in `/app/logs/`
   - Ensure `MCP_SERVER_TYPE` is set correctly

### Debug Mode

To run in debug mode with more verbose output:

```bash
docker compose run --rm -e LOG_LEVEL=DEBUG neozork-hld
```

### Cleanup

```bash
# Remove all containers and images
docker compose down --rmi all

# Clean up volumes (WARNING: removes all data)
docker volume prune
```

## Advanced Configuration

### Custom Environment

Create a custom `docker.env` file:

```bash
cp docker.env docker.env.local
# Edit docker.env.local with your settings
```

Then run with:

```bash
docker compose --env-file docker.env.local run --rm neozork-hld
```

### Development Mode

For development with live code changes:

```bash
# Mount source code for live reloading
docker compose run --rm -v $(pwd)/src:/app/src neozork-hld
```

### Performance Optimization

For better performance:

```bash
# Increase memory limit
docker compose run --rm --memory=8g neozork-hld

# Use host networking (Linux only)
docker compose run --rm --network=host neozork-hld
```

## Docker Scripts

The project includes several utility scripts in `scripts/docker/` for testing and managing Docker containers:

| Script                    | Purpose                                                                 |
|---------------------------|-------------------------------------------------------------------------|
| test_docker_history.sh    | Test command history functionality in interactive Docker container     |
| test_history_auto.sh      | Automatic verification of history initialization and operation in Docker |
| docker-test-workflows.sh  | Local testing of GitHub Actions workflows using act tool               |

### Using Docker Scripts

```bash
# Test command history in Docker container
./scripts/docker/test_docker_history.sh

# Run automatic history tests
./scripts/docker/test_history_auto.sh

# Test GitHub Actions workflows locally
./scripts/docker/docker-test-workflows.sh
```

## Security Considerations

- Container runs as non-root user
- Minimal system packages installed
- No sensitive data in image layers
- Environment variables for configuration

## Support

For issues and questions:

1. Check the logs in `./logs/`
2. Review this documentation
3. Check the main project README
4. Open an issue on GitHub 