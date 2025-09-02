# CI/CD Guide

## Overview

This guide covers Continuous Integration and Continuous Deployment (CI/CD) setup for the NeoZork HLD Prediction project using GitHub Actions and automated testing.

> ⚠️ **Version Information**: v0.5.2 is the last version that supports Docker and Apple Container. Current version: v0.5.3

## GitHub Actions Workflows

### Available Workflows

The project includes several GitHub Actions workflows for automated testing and deployment:

- **Docker Build** (`.github/workflows/docker-build.yml`) - Container building and testing
- **MCP Integration** (`.github/workflows/mcp-integration.yml`) - MCP server testing
- **MCP Servers CI** (`.github/workflows/mcp-servers-ci.yml`) - Comprehensive MCP testing
- **Python Testing** (`.github/workflows/python-testing.yml`) - Python environment testing

## Local CI/CD Testing

### Using Act Tool

Test GitHub Actions workflows locally without downloading Docker images:

```bash
# Install act tool
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash  # Linux

# Test all workflows (dry run - no Docker downloads)
act -n

# Test specific workflows
act -n -W .github/workflows/docker-build.yml
act -n -W .github/workflows/mcp-integration.yml

# List available workflows
act -l
```

**Benefits:**
- **No Docker Downloads**: Prevents downloading large Docker images
- **Fast Validation**: Quickly validates workflow syntax and structure
- **MCP Server Testing**: Verify MCP server communication protocols
- **Resource Efficient**: Uses minimal system resources

## Docker Workflow

> **Note**: Docker workflow support is limited to v0.5.2 and earlier versions.

### Docker Build Workflow

The Docker build workflow (`.github/workflows/docker-build.yml`) includes:

```yaml
name: Docker Build and Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
      
    - name: Build Docker image
      run: docker build -t neozork-hld-prediction .
      
    - name: Test Docker container
      run: |
        docker run --rm neozork-hld-prediction:latest \
          python -c "import sys; print(f'Python {sys.version} is working in the container')"
```

### Docker Testing

```bash
# Test Docker workflow locally
act -n -W .github/workflows/docker-build.yml

# Test Docker build
docker build -t neozork-hld-prediction .

# Test container functionality
docker run --rm neozork-hld-prediction:latest python -c "print('Container working')"
```

## MCP Server Testing

### MCP Integration Workflow

The MCP integration workflow (`.github/workflows/mcp-integration.yml`) tests:

- **Server Communication**: MCP server startup and shutdown
- **Protocol Compliance**: JSON-RPC 2.0 protocol validation
- **IDE Integration**: Cursor, VS Code, PyCharm configurations
- **Error Handling**: Robust error handling and recovery

### Local MCP Testing

```bash
# Test MCP server locally
python neozork_mcp_server.py

# Test MCP server status
python scripts/check_mcp_status.py

# Test MCP server with pytest
pytest tests/mcp/ -v
```

## Python Testing Workflow

### Python Environment Testing

The Python testing workflow (`.github/workflows/python-testing.yml`) includes:

```yaml
name: Python Testing

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
        
    steps:
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Run tests
      run: |
        pytest tests/ -v
```

### Local Python Testing

```bash
# Test with multiple Python versions
python3.8 -m pytest tests/ -v
python3.9 -m pytest tests/ -v
python3.10 -m pytest tests/ -v
python3.11 -m pytest tests/ -v

# Test with UV (recommended)
uv run pytest tests -n auto
```

## UV Package Manager Integration

### UV-Only Mode Testing

> **Note**: Docker UV testing is limited to v0.5.2 and earlier versions.

```bash
# Test UV-only mode locally
python scripts/check_uv_mode.py --verbose

# Test UV package installation
uv pip install -r requirements.txt

# Test UV testing
uv run pytest tests -n auto
```

### UV in CI/CD

```yaml
# Example UV integration in workflow
- name: Install UV
  run: |
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "$HOME/.local/bin" >> $GITHUB_PATH
    
- name: Install dependencies with UV
  run: |
    uv pip install -r requirements.txt
    
- name: Run tests with UV
  run: |
    uv run pytest tests -n auto
```

## Testing Strategies

### Adaptive Testing

The project uses adaptive testing that works in both local and container environments:

```python
# Example adaptive test
def test_uv_functionality():
    """Test UV functionality in current environment"""
    if is_running_in_docker():
        # Docker-specific tests (limited to v0.5.2 and earlier)
        test_docker_uv()
    else:
        # Local environment tests
        test_local_uv()
```

### Test Categories

- **Unit Tests**: Individual function and class testing
- **Integration Tests**: End-to-end workflow testing
- **Environment Tests**: Docker vs local detection
- **Performance Tests**: UV vs pip comparison
- **MCP Tests**: Model Context Protocol validation

## Deployment

### Production Deployment

> **Note**: Container deployment is limited to v0.5.2 and earlier versions.

```yaml
# Example deployment workflow
name: Deploy to Production

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - name: Deploy to production
      run: |
        # Production deployment logic
        echo "Deploying version ${{ github.ref_name }}"
```

### Local Deployment Testing

```bash
# Test deployment locally
./scripts/production/test.sh

# Test production configuration
pytest tests/production/ -v

# Test deployment scripts
./scripts/production/setup.sh
```

## Monitoring and Logging

### CI/CD Monitoring

```yaml
# Example monitoring in workflow
- name: Monitor workflow
  run: |
    echo "Workflow completed successfully"
    echo "Tests passed: ${{ steps.test.outputs.result }}"
    echo "Coverage: ${{ steps.coverage.outputs.result }}"
```

### Local Monitoring

```bash
# Check workflow status
act -l

# View workflow logs
act -W .github/workflows/docker-build.yml -v

# Test specific workflow steps
act -W .github/workflows/mcp-integration.yml --list
```

## Troubleshooting

### Common CI/CD Issues

**Workflow Failures:**
```bash
# Check workflow syntax
act -n -W .github/workflows/docker-build.yml

# Validate YAML syntax
yamllint .github/workflows/*.yml

# Test locally
act -W .github/workflows/docker-build.yml
```

**Docker Issues:**
```bash
# Test Docker locally
docker build -t test-image .

# Check Docker logs
docker logs <container_id>

# Verify Docker configuration
docker-compose config
```

**MCP Server Issues:**
```bash
# Test MCP server locally
python neozork_mcp_server.py

# Check MCP server status
python scripts/check_mcp_status.py

# Test MCP server with pytest
pytest tests/mcp/ -v
```

## Best Practices

1. **Test Locally First**: Use `act` tool to test workflows locally
2. **UV Package Manager**: Use UV for consistent dependency management
3. **Adaptive Testing**: Write tests that work in both environments
4. **Version Compatibility**: Note that Docker support is limited to v0.5.2
5. **Regular Updates**: Keep workflows and dependencies updated

## Related Documentation

- **[Testing Guide](testing.md)** - Testing framework and guidelines
- **[Docker Setup](docker-setup.md)** - Docker container setup
- **[Local Setup](local-setup.md)** - Local development setup
- **[UV Package Management](uv-package-management.md)** - UV usage guide
- **[MCP Server Integration](mcp-server-docker-integration.md)** - MCP server setup
- **[Development](../development/)** - Development workflow
