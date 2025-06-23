# Docker Troubleshooting Guide

This guide helps you resolve common Docker issues when working with the NeoZork HLD Prediction project.

## Common Issues and Solutions

### 1. Build Errors

#### Error: "COPY run_analysis.py mcp_server.py mcp.json ./"

**Problem**: Missing files in Dockerfile COPY commands.

**Solution**: 
- Ensure all required files exist in project root
- Check that `pycharm_github_copilot_mcp.py` is present
- Verify `cursor_mcp_config.json` and `mcp_auto_config.json` exist

**Files Required**:
```
run_analysis.py
pycharm_github_copilot_mcp.py
cursor_mcp_config.json
mcp_auto_config.json
requirements.txt
uv.toml
```

#### Error: "No module named 'pytest'"

**Problem**: Missing dependencies in container.

**Solution**:
```bash
# Rebuild with UV package manager
docker compose build --build-arg USE_UV=true

# Or rebuild with pip
docker compose build --build-arg USE_UV=false
```

### 2. Permission Errors

#### Error: "Permission denied" when accessing files

**Problem**: Container runs as non-root user but files have wrong permissions.

**Solution**:
```bash
# Fix permissions on host
chmod -R 755 data/ logs/ results/

# Or run container with proper user mapping
docker compose run --rm --user $(id -u):$(id -g) neozork-hld
```

### 3. Volume Mount Issues

#### Error: "Cannot access mounted volumes"

**Problem**: Volume mounts not working correctly.

**Solution**:
```bash
# Check volume mounts in docker-compose.yml
docker compose config

# Verify directories exist
ls -la data/ logs/ results/

# Create missing directories
mkdir -p data/ logs/ results/
```

### 4. MCP Server Issues

#### Error: "MCP server failed to start"

**Problem**: MCP server configuration issues.

**Solution**:
```bash
# Check MCP server configuration
cat docker.env | grep MCP

# Run with debug logging
docker compose run --rm -e LOG_LEVEL=DEBUG neozork-hld

# Check logs
docker logs <container_id>
```

### 5. Memory Issues

#### Error: "Out of memory" during build

**Problem**: Insufficient memory for Docker build.

**Solution**:
```bash
# Increase Docker memory limit in Docker Desktop
# Settings → Resources → Memory: 8GB+

# Or build with reduced parallelism
docker compose build --build-arg USE_UV=true --parallel 1
```

### 6. Network Issues

#### Error: "Cannot connect to external APIs"

**Problem**: Network connectivity issues in container.

**Solution**:
```bash
# Check network connectivity
docker compose run --rm neozork-hld ping google.com

# Use host networking (Linux only)
docker compose run --rm --network=host neozork-hld

# Check DNS resolution
docker compose run --rm neozork-hld nslookup api.polygon.io
```

## Debug Commands

### Check Container Status
```bash
# List running containers
docker ps

# Check container logs
docker logs <container_id>

# Execute commands in running container
docker exec -it <container_id> bash
```

### Inspect Configuration
```bash
# Validate docker-compose configuration
docker compose config

# Check environment variables
docker compose run --rm neozork-hld env

# Test file permissions
docker compose run --rm neozork-hld ls -la /app/
```

### Clean Up
```bash
# Remove all containers and images
docker compose down --rmi all

# Clean up volumes (WARNING: removes all data)
docker volume prune

# Remove unused images
docker image prune -a
```

## Performance Optimization

### Build Optimization
```bash
# Use build cache
docker compose build --build-arg USE_UV=true --no-cache

# Build with specific platform
docker compose build --platform linux/amd64

# Use multi-stage build (already configured)
```

### Runtime Optimization
```bash
# Increase memory limit
docker compose run --rm --memory=8g neozork-hld

# Use host networking (Linux only)
docker compose run --rm --network=host neozork-hld

# Mount source code for development
docker compose run --rm -v $(pwd)/src:/app/src neozork-hld
```

## Environment-Specific Issues

### macOS Issues
```bash
# File permission issues
chmod -R 755 data/ logs/ results/

# Docker Desktop resource limits
# Increase memory to 8GB+ in Docker Desktop settings
```

### Linux Issues
```bash
# SELinux issues
setsebool -P container_manage_cgroup 1

# AppArmor issues
sudo aa-complain docker-default
```

### Windows Issues
```bash
# WSL2 backend issues
wsl --shutdown
wsl --start

# File sharing issues
# Ensure project is in WSL2 filesystem, not Windows filesystem
```

## Getting Help

### Check Logs
```bash
# Container logs
docker logs <container_id>

# Application logs
docker compose run --rm neozork-hld cat /app/logs/docker.log

# System logs
docker system info
```

### Run Tests
```bash
# Test Docker configuration
python -m pytest tests/docker/test_docker_config.py -v

# Test in container
docker compose run --rm neozork-hld python -m pytest tests/ -v
```

### Documentation
- [Docker Setup Guide](docker-setup.md)
- [Main README](../../README.md)
- [Project Documentation](../index.md)

### Support
1. Check this troubleshooting guide
2. Review Docker setup documentation
3. Check project logs in `logs/` directory
4. Open an issue on GitHub with:
   - Error message
   - Docker version
   - Operating system
   - Steps to reproduce 