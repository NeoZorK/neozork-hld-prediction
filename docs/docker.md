# Docker Guide

Complete Docker setup and usage guide for containerized development and deployment.

## Overview

The project supports Docker for isolated, reproducible environments with all dependencies pre-configured.

## Files Structure

```
docker-compose.yml      # Docker Compose configuration
Dockerfile             # Container image definition
docker-entrypoint.sh   # Container startup script
```

## Quick Start

### Build and Run
```bash
# Build the Docker image
docker compose build

# Run in interactive mode
docker compose run --rm neozork-hld

# Run in background
docker compose up -d
```

### Using UV for Faster Builds
```bash
# Build with UV package manager for faster installation
docker compose build --build-arg USE_UV=true
```

## Container Features

### Automatic Setup
When the container starts, it automatically:
1. Executes all debug scripts from `scripts/debug_scripts/`
2. Starts the MCP server in the background
3. Displays usage help (`run_analysis.py -h`)
4. Provides an interactive shell

### Data Persistence
Local directories are mounted to preserve data:
- `./data` → `/app/data`
- `./logs` → `/app/logs`
- `./results` → `/app/results`

### Environment Variables
Settings from `.env` file are automatically loaded into the container.

## Usage Examples

### Interactive Analysis
```bash
# Enter the container
docker compose run --rm neozork-hld

# Inside container - run analysis
python run_analysis.py demo --rule PHLD
nz yf -t EURUSD=X --period 1mo --point 0.00001
```

### Background Services
```bash
# Start container with services
docker compose up -d

# Execute commands in running container
docker exec -it neozork-hld-prediction-neozork-hld-1 bash

# Inside container
nz demo --rule PV -d term
```

### Direct Command Execution
```bash
# Run single command
docker compose run --rm neozork-hld python run_analysis.py demo

# Run with specific parameters
docker compose run --rm neozork-hld nz yf -t AAPL --period 1mo --point 0.01
```

## Container Management

### Start/Stop Services
```bash
# Start all services
docker compose up -d

# Stop all services
docker compose down

# Restart services
docker compose restart
```

### Container Access
```bash
# Get container name
docker ps

# Access running container
docker exec -it <container_name> bash

# Or use the typical container name
docker exec -it neozork-hld-prediction-neozork-hld-1 bash
```

### Logs and Monitoring
```bash
# View container logs
docker compose logs

# Follow logs in real-time
docker compose logs -f

# View specific service logs
docker compose logs neozork-hld
```

## Configuration Options

### Environment Variables
Create `.env` file in project root:
```env
# API Keys
POLYGON_API_KEY=your_key_here
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here

# Docker specific
USE_UV=true  # Use UV package manager
```

### Docker Compose Override
Create `docker-compose.override.yml` for custom settings:
```yaml
version: '3.8'
services:
  neozork-hld:
    ports:
      - "8080:8080"  # Expose additional ports
    environment:
      - DEBUG=true
```

## Terminal Plotting

In Docker environments, plotting automatically switches to terminal mode:
```bash
# Automatically uses terminal plotting in Docker
nz demo -d term
nz yf -t AAPL --period 1mo --point 0.01 -d term
```

## MCP Server Integration

The container includes MCP server for enhanced GitHub Copilot support:
```bash
# MCP server starts automatically
# When prompted: "Would you like to start the MCP service for enhanced LLM support? [y/N]:"
# Enter "y" to activate
```

## Performance Considerations

### Memory and CPU
- Default: 2-core CPU, 8 GB RAM
- For large datasets, consider increasing resources
- Data processing may be slower than native execution

### Storage
- Container uses bind mounts for data persistence
- Large datasets are stored outside container
- Cache files persist between container restarts

### Network
- API calls work normally from container
- Respect rate limits for external APIs

## Troubleshooting

### Common Issues

**Container won't start:**
```bash
# Check Docker status
docker --version
docker compose --version

# Rebuild image
docker compose build --no-cache
```

**Permission errors:**
```bash
# Fix file permissions
sudo chown -R $USER:$USER data/ logs/ results/
```

**Out of memory:**
```bash
# Increase Docker memory in Docker Desktop settings
# Or use smaller datasets
```

### Debug Commands
```bash
# Check container status
docker ps -a

# Inspect container
docker inspect <container_name>

# View container resource usage
docker stats

# Clean up unused containers/images
docker system prune
```

## Development Workflow

### Code Changes
```bash
# After code changes, rebuild
docker compose build

# Or rebuild specific service
docker compose build neozork-hld
```

### Testing in Container
```bash
# Run tests in container
docker compose run --rm neozork-hld pytest tests/ -v

# Run specific test
docker compose run --rm neozork-hld python -m unittest tests.cli.test_cli_all_commands
```

### CI/CD Integration
```bash
# Test GitHub Actions locally
chmod +x test-workflow.sh
./test-workflow.sh
```

## Best Practices

1. **Use bind mounts** for data directories to persist results
2. **Set resource limits** appropriate for your datasets
3. **Use .dockerignore** to exclude unnecessary files
4. **Build with UV** for faster dependency installation
5. **Clean up regularly** to save disk space:
   ```bash
   docker system prune -f
   ```
