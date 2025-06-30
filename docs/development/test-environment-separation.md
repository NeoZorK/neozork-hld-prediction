# Test Environment Separation

This document describes how tests are automatically separated and skipped based on the environment type to prevent conflicts between Docker and native container tests.

## Problem

Docker tests expect the environment variable `DOCKER_CONTAINER=true`, but in native container environments, this variable is set to `false`. This causes test failures when running Docker tests in native containers.

## Solution

The test framework automatically detects the environment type and skips incompatible tests:

- **Native Container**: Docker tests are automatically skipped
- **Docker Container**: Native container tests are automatically skipped
- **Local Environment**: All tests run normally

## Environment Detection

The system uses the following logic to determine the environment:

```python
def get_environment_type():
    """Determine the current environment type"""
    if os.environ.get('NATIVE_CONTAINER') == 'true':
        return 'native_container'
    elif os.environ.get('DOCKER_CONTAINER') == 'true':
        return 'docker'
    elif os.path.exists('/.dockerenv'):
        return 'docker'
    else:
        return 'local'
```

## Test Markers

Tests are automatically marked based on their location:

- `tests/docker/` → `@pytest.mark.docker`
- `tests/native-container/` → `@pytest.mark.native_container`

## Automatic Test Skipping

In `tests/conftest.py`, the `pytest_collection_modifyitems` function automatically:

1. Detects the environment type
2. Adds appropriate markers to tests
3. Skips incompatible tests with descriptive messages

## Running Tests

### All Tests (Recommended)
```bash
# Automatically skips incompatible tests
./scripts/run_all_tests.sh
```

### Native Container Only
```bash
# Explicitly excludes Docker tests
./scripts/run_tests_native_container.sh
```

### Manual Control
```bash
# Run only non-Docker tests
uv run pytest tests -m "not docker"

# Run only Docker tests
uv run pytest tests -m "docker"

# Run only native container tests
uv run pytest tests -m "native_container"
```

## Environment Variables

### Native Container
```yaml
environment:
  - NATIVE_CONTAINER=true
  - DOCKER_CONTAINER=false
  - USE_UV=true
  - UV_ONLY=true
```

### Docker Container
```yaml
environment:
  - DOCKER_CONTAINER=true
  - USE_UV=true
  - UV_ONLY=true
```

## Test Output

When running tests, you'll see messages like:

```
🔍 Environment detected: native_container
⏭️  Docker tests will be skipped
⏭️  Skipping Docker test: tests/docker/test_uv_commands.py::test_uv_environment
```

## Benefits

1. **No Manual Configuration**: Tests are automatically skipped based on environment
2. **Clear Feedback**: Users see which tests are being skipped and why
3. **Flexible**: Can still run specific test categories manually
4. **Maintainable**: Centralized logic in `conftest.py`

## Troubleshooting

### Tests Still Running When They Should Be Skipped

1. Check environment variables are set correctly
2. Verify test file paths contain the expected keywords
3. Ensure `conftest.py` is being loaded

### Tests Being Skipped Unexpectedly

1. Check the environment detection logic
2. Verify file paths don't contain unexpected keywords
3. Review the skip conditions in `pytest_collection_modifyitems`

## Future Enhancements

- Add more granular environment detection
- Support for custom test categories
- Integration with CI/CD pipeline environment detection 