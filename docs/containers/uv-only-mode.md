# UV-Only Mode in Docker

This document describes the implementation and usage of UV-only mode in the NeoZork HLD Prediction Docker container.

> ⚠️ **Version Information**: v0.5.2 is the last version that supports Docker and Apple Container. Current version: v0.5.3

## Overview

The project has been configured to use **UV package manager exclusively** within Docker containers, providing faster dependency resolution, better caching, and improved reliability compared to traditional pip.

> **Note**: Docker container support is limited to v0.5.2 and earlier versions.

## Key Features

- **Exclusive UV Usage**: No fallback to pip - all package management is handled by UV
- **Optimized Caching**: Persistent UV cache mounted as Docker volume
- **MCP Integration**: MCP server configured to work with UV-only mode
- **Environment Validation**: Comprehensive checks ensure UV-only mode is properly configured
- **Command Wrappers**: Convenient shortcuts for common UV operations

## Configuration Files

### 1. Docker Environment (`docker.env`)

```bash
# UV-only mode enforcement
USE_UV=true
UV_ONLY=true
UV_CACHE_DIR=/app/.uv_cache
UV_VENV_DIR=/app/.venv
```

### 2. Docker Compose (`docker-compose.yml`)

```yaml
services:
  neozork-hld:
    build:
      args:
        USE_UV: ${USE_UV:-true}
        UV_ONLY: ${UV_ONLY:-true}
    volumes:
      - uv_cache:/app/.uv_cache
    environment:
      - USE_UV=true
      - UV_ONLY=true
      - UV_CACHE_DIR=/app/.uv_cache
      - UV_VENV_DIR=/app/.venv

volumes:
  uv_cache:
    driver: local
```

### 3. MCP Configuration (`cursor_mcp_config.json`)

```json
{
  "serverSettings": {
    "neozork": {
      "features": {
        "uv_integration": true,
        "uv_only_mode": true
      }
    }
  },
  "cursor": {
    "python": {
      "packageManager": "uv",
      "uvOnly": true
    }
  }
}
```

## Dockerfile Changes

The Dockerfile has been updated to:

1. **Force UV Installation**: UV is always installed, no conditional logic
2. **Remove Pip Fallback**: All package installation uses UV exclusively
3. **UV Environment Variables**: Set UV-specific environment variables
4. **Cache Directory Creation**: Create and configure UV cache directories

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

## Available Commands

### UV Package Management

```bash
# Install dependencies
uv-install

# Update dependencies
uv-update

# Install specific package
uv pip install <package>

# List installed packages
uv pip list

# Check UV version
uv --version
```

### Analysis Commands

```bash
# Run analysis
nz

# Run EDA
eda

# Direct Python execution
python run_analysis.py demo --rule PHLD
```

## Validation and Testing

### UV Mode Checker

Run the UV mode validation script:

```bash
python scripts/check_uv_mode.py
```

This script checks:
- UV installation and version
- Environment variables
- Directory permissions
- MCP configuration
- Package installation status

### Test Suite

Run the UV-only mode tests:

```bash
pytest tests/docker/test_uv_only_mode.py -v
```

Tests validate:
- UV installation
- Environment configuration
- Directory setup
- Package management
- MCP integration

## Benefits of UV-Only Mode

### 1. Performance
- **Faster Installation**: UV is significantly faster than pip
- **Better Caching**: Intelligent caching reduces download times
- **Parallel Downloads**: Concurrent package downloads

### 2. Reliability
- **Deterministic Builds**: Consistent dependency resolution
- **Better Error Handling**: More informative error messages
- **Lock File Support**: Precise dependency pinning

### 3. Security
- **Vulnerability Scanning**: Built-in security checks
- **Package Verification**: Enhanced package integrity checks
- **Isolated Environments**: Better environment isolation

### 4. Developer Experience
- **Simplified Workflow**: Single package manager
- **Better Tooling**: Enhanced IDE integration
- **Consistent Behavior**: Same behavior across environments

## Troubleshooting

### Common Issues

#### 1. UV Not Available
```bash
Error: UV is not available - this is required for UV-only mode
```

**Solution**: Ensure the Docker image is built with UV installation enabled.

#### 2. Cache Directory Issues
```bash
Error: Cannot write to UV cache directory
```

**Solution**: Check Docker volume permissions and ensure the cache volume is properly mounted.

#### 3. Package Installation Failures
```bash
Error: Failed to install packages via UV
```

**Solution**: 
- Check network connectivity
- Verify package names and versions
- Review UV cache for corrupted files

### Debug Commands

```bash
# Check UV status
python scripts/check_uv_mode.py --verbose

# Validate environment
env | grep UV

# Check cache directory
ls -la /app/.uv_cache

# Test UV functionality
uv pip install --dry-run requests
```

## Migration from Pip

If migrating from a pip-based setup:

1. **Update Configuration**: Ensure all config files use UV settings
2. **Rebuild Container**: Build new Docker image with UV-only mode
3. **Test Dependencies**: Verify all packages install correctly via UV
4. **Update Scripts**: Modify any scripts that use pip commands
5. **Validate MCP**: Ensure MCP server works with UV configuration

## Best Practices

### 1. Cache Management
- Use persistent Docker volumes for UV cache
- Regularly clean old cache entries
- Monitor cache size and performance

### 2. Dependency Management
- Use `requirements.txt` for reproducible builds
- Consider using UV lock files for exact versions
- Regularly update dependencies

### 3. Environment Consistency
- Always use UV-only mode in containers
- Validate environment on container startup
- Monitor for any pip fallback attempts

### 4. Testing
- Run UV validation tests regularly
- Test package installation in clean environments
- Validate MCP server functionality

## Monitoring and Logging

### UV Activity Logs
UV operations are logged to:
- Container stdout/stderr
- Application logs (`/app/logs/`)
- Docker logs

### Health Checks
The container includes health checks for:
- UV availability
- Package installation status
- Cache directory accessibility
- MCP server functionality

## Future Enhancements

### Planned Improvements
1. **UV Lock Files**: Implement lock file support for exact dependency versions
2. **Multi-Stage Builds**: Optimize Docker builds with UV-specific stages
3. **Advanced Caching**: Implement more sophisticated caching strategies
4. **Security Scanning**: Integrate UV's security scanning capabilities

### Integration Opportunities
1. **CI/CD Pipelines**: Use UV in automated testing and deployment
2. **Development Tools**: Enhanced IDE integration with UV
3. **Monitoring**: Advanced monitoring and alerting for UV operations

## Conclusion

UV-only mode provides a modern, efficient, and reliable package management solution for the NeoZork HLD Prediction project. The implementation ensures consistent behavior across all environments while providing significant performance and security benefits.

For questions or issues related to UV-only mode, refer to the troubleshooting section or contact the development team. 