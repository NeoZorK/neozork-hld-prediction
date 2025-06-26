# UV-Only Mode Docker Tests

This directory contains tests for validating UV-only mode functionality in both Docker containers and local environments.

## Test Files

### 1. `test_uv_only_mode.py`
Comprehensive test suite for UV-only mode validation:
- UV installation and version
- Environment variables (Docker-specific and local)
- Directory permissions
- Package management
- MCP configuration
- Integration tests
- **Adaptive**: Works in both Docker and local environments

### 2. `test_uv_commands.py`
Basic UV command functionality tests:
- UV availability
- Basic commands (help, version)
- Package listing
- Environment validation
- **Adaptive**: Works in both Docker and local environments

### 3. `test_uv_simple.py`
Very simple tests that should work in any environment:
- UV existence check
- Help command
- Environment variables
- Package listing fallback
- **Adaptive**: Works in both Docker and local environments

## Running Tests

### Inside Docker Container

1. **Start the container**:
   ```bash
   docker-compose up
   ```

2. **Run comprehensive tests**:
   ```bash
   pytest tests/docker/test_uv_only_mode.py -v
   ```

3. **Run basic command tests**:
   ```bash
   pytest tests/docker/test_uv_commands.py -v
   ```

4. **Run simple tests**:
   ```bash
   pytest tests/docker/test_uv_simple.py -v
   ```

5. **Run all Docker tests**:
   ```bash
   pytest tests/docker/ -v
   ```

### Outside Docker (Local Environment)

1. **Ensure UV is installed locally**:
   ```bash
   # Install UV if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # or
   pip install uv
   ```

2. **Run simple tests** (recommended for local testing):
   ```bash
   pytest tests/docker/test_uv_simple.py -v
   ```

3. **Run basic command tests**:
   ```bash
   pytest tests/docker/test_uv_commands.py -v
   ```

4. **Run comprehensive tests** (will skip Docker-specific checks):
   ```bash
   pytest tests/docker/test_uv_only_mode.py -v
   ```

5. **Run all tests**:
   ```bash
   pytest tests/docker/ -v
   ```

### Using UV Test Script

The container includes a UV test script that can be run in both environments:

```bash
# Run the UV environment test
python scripts/test_uv_docker.py

# Or use the wrapper command (Docker only)
uv-test
```

### Manual Testing

You can also test UV functionality manually:

```bash
# Check UV version
uv --version

# Check UV help
uv --help

# List packages (try different methods)
uv pip list
pip list
python -m pip list

# Check environment variables
env | grep UV
```

## Environment Detection

The tests automatically detect whether they're running in Docker or locally:

### Docker Environment Detection
- `DOCKER_CONTAINER=true` environment variable
- Presence of `/.dockerenv` file
- Presence of `/app` directory

### Local Environment Behavior
- Skips Docker-specific environment variable checks
- Uses local paths instead of `/app` paths
- Creates temporary test directories locally
- Checks for local MCP configuration files

## Test Behavior by Environment

### Inside Docker
- **Strict checks**: All Docker-specific environment variables must be set
- **Docker paths**: Uses `/app` directory structure
- **MCP config**: Checks `/app/cursor_mcp_config.json`
- **UV-only mode**: Enforces UV-only mode requirements

### Outside Docker
- **Flexible checks**: Only requires UV to be available
- **Local paths**: Uses current directory and local paths
- **Optional MCP**: Checks for local MCP config if available
- **Basic validation**: Focuses on UV availability and basic functionality

## Troubleshooting

### Common Issues

1. **UV not available**:
   ```bash
   # Install UV locally
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # or
   pip install uv
   ```

2. **Environment variables not set** (Docker only):
   - Ensure `docker.env` has correct UV settings
   - Check `docker-compose.yml` environment section
   - Verify Dockerfile sets UV environment variables

3. **Directory permissions** (Docker only):
   - UV cache and venv directories should be writable
   - Check Docker volume permissions
   - Ensure non-root user has access

4. **Local testing issues**:
   - Ensure UV is in PATH
   - Check Python environment
   - Verify package installation

### Debug Commands

#### Docker Environment
```bash
# Check UV installation
which uv
uv --version

# Check environment
env | grep UV

# Check directories
ls -la /app/.uv_cache
ls -la /app/.venv

# Test package management
uv pip list
pip list

# Run UV test script with verbose output
python scripts/test_uv_docker.py
```

#### Local Environment
```bash
# Check UV installation
which uv
uv --version

# Check environment
env | grep UV

# Check local directories
ls -la .uv_cache
ls -la .venv

# Test package management
uv pip list
pip list

# Run UV test script
python scripts/check_uv_mode.py --verbose
```

## Test Results

### Expected Output (Docker)

Successful tests should show:
```
✅ UV version: uv 0.x.x
✅ UV help command works
✅ Package listing works with: uv pip list
✅ Docker environment variables are set correctly
✅ Docker UV directories are accessible
```

### Expected Output (Local)

Successful tests should show:
```
✅ UV version: uv 0.x.x
✅ UV help command works
✅ Package listing works with: uv pip list
ℹ️  Running outside Docker - UV environment variables not required
✅ UV is available in local environment
```

### Failed Tests

If tests fail, check:
1. UV installation in both environments
2. Environment variable configuration (Docker)
3. Directory permissions (Docker)
4. Package installation status
5. Python environment setup

## Integration with CI/CD

These tests can be integrated into CI/CD pipelines for both environments:

```yaml
# Example GitHub Actions step
- name: Test UV mode (Docker)
  run: |
    docker-compose up -d
    docker-compose exec neozork-hld pytest tests/docker/test_uv_simple.py -v

- name: Test UV mode (Local)
  run: |
    pytest tests/docker/test_uv_simple.py -v
```

## Notes

- Tests are designed to be robust and handle different UV versions
- Fallback to regular pip is accepted for package management
- Environment validation adapts based on detection
- Directory tests check for parent directory existence
- MCP configuration tests validate UV integration settings
- Local testing focuses on UV availability and basic functionality
- Docker testing enforces full UV-only mode requirements 