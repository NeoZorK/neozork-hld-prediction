# UV-Only Mode Docker Tests

This directory contains tests for validating UV-only mode functionality in Docker containers.

## Test Files

### 1. `test_uv_only_mode.py`
Comprehensive test suite for UV-only mode validation:
- UV installation and version
- Environment variables
- Directory permissions
- Package management
- MCP configuration
- Integration tests

### 2. `test_uv_commands.py`
Basic UV command functionality tests:
- UV availability
- Basic commands (help, version)
- Package listing
- Environment validation

### 3. `test_uv_simple.py`
Very simple tests that should work in any Docker environment:
- UV existence check
- Help command
- Environment variables
- Package listing fallback

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

### Using UV Test Script

The container includes a UV test script that can be run directly:

```bash
# Run the UV environment test
python scripts/test_uv_docker.py

# Or use the wrapper command
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

## Troubleshooting

### Common Issues

1. **UV pip not available**:
   - The test now accepts regular pip as fallback
   - Check if UV is properly installed in Dockerfile
   - Verify PATH includes UV binary

2. **Environment variables not set**:
   - Ensure `docker.env` has correct UV settings
   - Check `docker-compose.yml` environment section
   - Verify Dockerfile sets UV environment variables

3. **Directory permissions**:
   - UV cache and venv directories should be writable
   - Check Docker volume permissions
   - Ensure non-root user has access

### Debug Commands

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

## Test Results

### Expected Output

Successful tests should show:
```
✅ UV version: uv 0.x.x
✅ UV help command works
✅ Package listing works with: uv pip list
✅ UV environment variables are set correctly
✅ UV directories are accessible
```

### Failed Tests

If tests fail, check:
1. UV installation in Dockerfile
2. Environment variable configuration
3. Directory permissions
4. Package installation status

## Integration with CI/CD

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions step
- name: Test UV-only mode
  run: |
    docker-compose up -d
    docker-compose exec neozork-hld pytest tests/docker/test_uv_simple.py -v
```

## Notes

- Tests are designed to be robust and handle different UV versions
- Fallback to regular pip is accepted for package management
- Environment validation is strict for UV-only mode
- Directory tests check for parent directory existence
- MCP configuration tests validate UV integration settings 