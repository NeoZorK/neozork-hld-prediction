# Deployment Documentation

This section covers all aspects of deploying the NeoZork HLD Prediction system, from local development to production environments.

## 🚀 Quick Start

### Docker Deployment (Recommended)
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

### [Docker Setup](docker-setup.md)
Complete guide for containerized deployment using Docker and Docker Compose.

**Key Features:**
- Multi-stage builds for optimized images
- Environment variable management
- Volume mounting for data persistence
- Health checks and monitoring
- **UV-Only Mode**: Exclusive UV package manager usage

### [UV-Only Mode](uv-only-mode.md) ⭐ **NEW**
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

### Environment Variables
```bash
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
pytest tests/docker/ -v -s

# Check environment detection
python scripts/check_uv_mode.py --debug

# Test specific environment
python scripts/check_uv_mode.py --docker-only
```

## 📈 Monitoring & Logging

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