# Deployment Documentation

This section covers all aspects of deploying the NeoZork HLD Prediction system, from local development to production environments.

## 🚀 Quick Start

### Native Apple Silicon Container (Recommended for macOS 26+)
```bash
# Setup and run native container
./scripts/native-container/setup.sh
./scripts/native-container/run.sh

# Execute commands
./scripts/native-container/exec.sh --analysis 'nz demo --rule PHLD'
```

### Docker Deployment (Cross-platform)
```bash
# Build and start
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Local Deployment
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -r requirements.txt

# Run application
python run_analysis.py
```

## 📚 Deployment Guides

### [Native Apple Silicon Container](native-container-setup.md) ⭐ **NEW & RECOMMENDED**
Complete guide for native Apple Silicon container deployment on macOS 26+ (Tahoe).

**Key Features:**
- **30-50% performance improvement** over Docker
- **Native Apple Silicon optimization** with ARM64 architecture
- **Lower resource usage** and faster startup times
- **Simplified setup** with single configuration file
- **UV-Only Mode**: Exclusive UV package manager usage
- **Native macOS integration** with system-level optimizations

### [Native vs Docker Comparison](native-vs-docker-comparison.md) ⭐ **NEW**
Comprehensive comparison between native containers and Docker.

**Highlights:**
- **Performance benchmarks** and resource usage analysis
- **Platform compatibility** and use case recommendations
- **Migration guide** from Docker to native containers
- **Cost analysis** and development time savings

### [Docker Setup](docker-setup.md)
Complete guide for containerized deployment using Docker and Docker Compose.

**Key Features:**
- Multi-stage builds for optimized images
- Environment variable management
- Volume mounting for data persistence
- Health checks and monitoring
- **UV-Only Mode**: Exclusive UV package manager usage
- **Cross-platform compatibility**

### [UV-Only Mode](uv-only-mode.md)
Comprehensive guide for UV package manager configuration and usage.

**Highlights:**
- **Exclusive UV Usage**: No fallback to pip
- **Docker Integration**: Seamless UV in containers
- **Local Development**: UV support for local environments
- **Adaptive Testing**: Tests that work in both Docker and local
- **Performance**: 10-100x faster than traditional pip

### [Production Deployment](production.md)
Production-ready deployment configurations and best practices.

### [Monitoring](monitoring.md)
System monitoring, logging, and health check configurations.

## 🔧 Configuration

### Native Container Configuration
```yaml
# container.yaml
apiVersion: v1
kind: Container
metadata:
  name: neozork-hld-prediction
  labels:
    platform: apple-silicon
spec:
  image: python:3.11-slim
  architecture: arm64
  resources:
    memory: "4Gi"
    cpu: "2"
  environment:
    - USE_UV=true
    - UV_ONLY=true
    - NATIVE_CONTAINER=true
```

### Environment Variables
```bash
# Native container environment
USE_UV=true
UV_ONLY=true
UV_CACHE_DIR=/app/.uv_cache
UV_VENV_DIR=/app/.venv
NATIVE_CONTAINER=true
DOCKER_CONTAINER=false

# Docker environment
UV_ONLY_MODE=true
UV_CACHE_DIR=/app/.uv_cache
UV_VENV_DIR=/app/.venv

# Local environment
export UV_ONLY_MODE=true
export UV_CACHE_DIR=./.uv_cache
export UV_VENV_DIR=./.venv
```

### Docker Compose
```yaml
version: '3.8'
services:
  neozork:
    build: .
    environment:
      - UV_ONLY_MODE=true
      - UV_CACHE_DIR=/app/.uv_cache
    volumes:
      - ./.uv_cache:/app/.uv_cache
```

## 🧪 Testing Deployment

### Native Container Environment
```bash
# Test native container setup
pytest tests/native-container/test_container_setup.py -v

# Test container configuration
pytest tests/native-container/ -v

# Run integration tests
./scripts/native-container/exec.sh --test
```

### Docker Environment
```bash
# Test UV-only mode
pytest tests/docker/test_uv_only_mode.py -v

# Test basic functionality
pytest tests/docker/test_uv_simple.py -v

# Test commands
pytest tests/docker/test_uv_commands.py -v
```

### Local Environment
```bash
# Test adaptive functionality
pytest tests/docker/test_uv_simple.py -v

# Check UV status
python scripts/check_uv_mode.py --verbose
```

## 📊 Performance Metrics

### Native Apple Silicon Container
- **Performance**: 30-50% faster than Docker
- **Memory Usage**: 2-3GB (vs 4-6GB in Docker)
- **Startup Time**: 5-10 seconds (vs 15-30 seconds in Docker)
- **Resource Overhead**: 10-20% (vs 20-30% in Docker)
- **Native Integration**: Optimized for Apple Silicon

### UV Package Manager
- **Installation Speed**: 10-100x faster than pip
- **Dependency Resolution**: Intelligent conflict resolution
- **Caching**: Persistent package cache
- **Virtual Environments**: Fast environment creation

### Docker Optimization
- **Multi-stage Builds**: Reduced image size
- **Layer Caching**: Faster rebuilds
- **Volume Mounting**: Persistent data storage
- **Health Checks**: Automatic service monitoring

## 🔒 Security Considerations

### Native Container Security
- **Native macOS Security**: System-level isolation
- **Minimal Attack Surface**: Native containerization
- **System-level Permissions**: Apple's security model
- **Non-root Execution**: Secure container operation

### Container Security
- **Non-root Execution**: Secure container operation
- **Package Verification**: UV's built-in security checks
- **Environment Isolation**: Proper environment separation
- **Input Validation**: Comprehensive input sanitization

### Network Security
- **Internal Communication**: Secure inter-service communication
- **External APIs**: Secure API key management
- **Data Encryption**: Encrypted data transmission

## 🚨 Troubleshooting

### Native Container Issues

#### Native Container Application Not Found
```bash
# Install from Apple Developer Beta
# Download from: https://developer.apple.com/download/all/

# Check installation
container --version
```

#### macOS Version Incompatibility
```bash
# Check macOS version
sw_vers -productVersion

# Update to macOS 26+ (Tahoe) for optimal performance
```

#### Container Build Failures
```bash
# Check available disk space (minimum 10GB)
df -h

# Clean up and retry
./scripts/native-container/cleanup.sh --all
./scripts/native-container/setup.sh
```

### Common Issues

#### UV Installation Problems
```bash
# Check UV installation
uv --version

# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clear UV cache
rm -rf ~/.cache/uv
```

#### Docker Build Issues
```bash
# Clean build
docker-compose build --no-cache

# Check logs
docker-compose logs build

# Verify environment
docker-compose exec neozork env | grep UV
```

#### Test Failures
```bash
# Run with verbose output
pytest tests/native-container/ -v -s
pytest tests/docker/ -v -s

# Check environment detection
python scripts/check_uv_mode.py --debug

# Test specific environment
python scripts/check_uv_mode.py --docker-only
```

## 📈 Monitoring & Logging

### Native Container Monitoring
```bash
# Check container status
./scripts/native-container/run.sh --status

# View container logs
./scripts/native-container/logs.sh --follow

# Monitor system resources
./scripts/native-container/logs.sh system
```

### Health Checks
```bash
# Check service health
docker-compose ps

# View service logs
docker-compose logs -f neozork

# Monitor resource usage
docker stats
```

### Log Management
```bash
# View application logs
tail -f logs/app.log

# Check error logs
tail -f logs/error.log

# Monitor UV operations
tail -f logs/uv.log
```

## 🎯 Deployment Recommendations

### Choose Native Container When
- **Developing on macOS 26+** with Apple Silicon
- **Performance is critical** for analysis tasks
- **Resource efficiency** is important
- **Native macOS integration** is desired
- **Fast development iteration** is needed

### Choose Docker When
- **Cross-platform compatibility** is required
- **Team uses different platforms** (Windows, Linux)
- **CI/CD pipelines** need universal support
- **Legacy macOS versions** are in use
- **Docker ecosystem** integration is needed

### Migration Path
```bash
# From Docker to Native Container
docker-compose down
./scripts/native-container/setup.sh
./scripts/native-container/run.sh

# Rollback to Docker if needed
./scripts/native-container/cleanup.sh --all
docker-compose up -d
```

## 🔄 Updates & Maintenance

### Updating Dependencies
```bash
# Docker environment
docker-compose exec neozork uv-update

# Local environment
uv pip install --upgrade -r requirements.txt
```

### System Updates
```bash
# Update Docker images
docker-compose pull
docker-compose up -d

# Update UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [UV Documentation](https://docs.astral.sh/uv/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Project Issues](https://github.com/username/neozork-hld-prediction/issues)

---

**Last Updated**: 2024
**Version**: 2.0.0 (UV-Only Mode)

# Deployment

This section covers deployment options and configurations for the NeoZork HLD Prediction project.

## Container Options

### Docker Deployment
- **[Docker Setup](docker-setup.md)** - Standard Docker container setup
- **[Docker Examples](docker-examples.md)** - Docker usage examples
- **[Docker Testing](docker-testing.md)** - Testing in Docker environment

### Native Apple Silicon Container (macOS 26+)
- **[Native Container Setup](native-container-setup.md)** - Complete setup guide for Apple Silicon
- **[Native vs Docker Comparison](native-vs-docker-comparison.md)** - Performance comparison
- **[Implementation Summary](NATIVE_CONTAINER_IMPLEMENTATION_SUMMARY.md)** - Complete implementation overview

## Configuration

- **[Environment Configuration](environment-config.md)** - Environment variables and settings
- **[UV Package Management](uv-only-mode.md)** - UV package manager configuration
- **[MCP Server Setup](mcp-server-setup.md)** - Model Context Protocol server configuration

## Testing

- **[Test Environment Setup](test-environment.md)** - Setting up test environments
- **[CI/CD Integration](ci-cd.md)** - Continuous integration and deployment
- **[Performance Testing](performance-testing.md)** - Performance benchmarks and testing

## Monitoring and Logging

- **[Logging Configuration](logging-config.md)** - Log management and configuration
- **[Monitoring Setup](monitoring-setup.md)** - System monitoring and alerts
- **[Debugging Tools](debugging-tools.md)** - Debugging and troubleshooting tools 