# Docker Testing Guide

## Overview

This guide provides instructions for running tests in Docker containers, including solutions for common issues with parallel test execution.

## Running Tests in Docker

### Basic Test Execution

```bash
# Run all integration tests (single-threaded - recommended for Docker)
docker-compose exec neozork-hld uv run pytest tests/integration/ -v --tb=short

# Run specific test file
docker-compose exec neozork-hld uv run pytest tests/integration/test_investment_flow.py -v

# Run specific test
docker-compose exec neozork-hld uv run pytest tests/integration/test_investment_flow.py::TestInvestmentFlow::test_authentication_flow -v
```

### Parallel Test Execution (Use with Caution)

**⚠️ Warning**: Parallel test execution (`-n auto`) in Docker containers can cause worker crashes and BrokenPipeError due to resource limitations.

```bash
# NOT RECOMMENDED in Docker - may cause worker crashes
docker-compose exec neozork-hld uv run pytest tests/integration/ -n auto

# If you must use parallel execution, limit workers
docker-compose exec neozork-hld uv run pytest tests/integration/ -n 2 -v
```

## Common Issues and Solutions

### 1. Worker Crashes with `-n auto`

**Problem**: 
```
worker 'gw0' crashed while running 'test_name'
BrokenPipeError: [Errno 32] Broken pipe
```

**Solution**: 
- Use single-threaded execution (default configuration)
- If parallel execution is needed, limit workers: `-n 2` or `-n 4`

### 2. Database Connection Issues

**Problem**: 
```
ERROR: Failed to initialize database connections: [Errno -2] Name or service not known
```

**Solution**: 
- Ensure PostgreSQL container is running: `docker-compose ps`
- Check network connectivity: `docker-compose exec neozork-hld ping postgres`
- Verify DATABASE_URL in docker-compose.yml

### 3. Authentication Test Failures

**Problem**: 
```
assert 401 == 200  # Authentication failures
```

**Solution**: 
- Tests are designed to handle existing users in database
- Registration may fail if user already exists (expected behavior)
- Login should work with existing users

## Configuration

### pytest.ini Settings for Docker

The project includes Docker-optimized pytest configuration:

```ini
[tool:pytest]
# Single-threaded execution by default (stable in Docker)
addopts = -v --tb=short --disable-warnings

# Docker-specific settings
maxfail = 1
timeout = 300
timeout_method = thread

# Markers for test organization
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    # ... other markers
```

### Environment Variables

Key environment variables for Docker testing:

```bash
# Database connection
DATABASE_URL=postgresql://neozork_user:neozork_password@postgres:5432/neozork_fund

# Test environment
DOCKER_CONTAINER=true
NEOZORK_TEST=1
MPLBACKEND=Agg  # Non-interactive backend for plotting
```

## Best Practices

### 1. Test Execution Order

1. **Single-threaded first**: Always test with single-threaded execution first
2. **Parallel testing**: Only use parallel execution if single-threaded works
3. **Resource monitoring**: Monitor Docker container resources during parallel execution

### 2. Test Data Management

- Tests use unique identifiers to avoid conflicts
- Existing users in database are handled gracefully
- Test data is isolated per test run

### 3. Error Handling

- Tests are designed to be resilient to database issues
- Authentication tests handle both new and existing users
- API tests accept various valid status codes

## Troubleshooting

### Check Container Status

```bash
# Check if containers are running
docker-compose ps

# Check container logs
docker-compose logs neozork-hld
docker-compose logs postgres
```

### Verify Database Connection

```bash
# Test database connection
docker-compose exec neozork-hld python -c "
import psycopg2
conn = psycopg2.connect('postgresql://neozork_user:neozork_password@postgres:5432/neozork_fund')
print('Database connection successful')
"
```

### Check Test Configuration

```bash
# Verify pytest configuration
docker-compose exec neozork-hld cat /app/pytest.ini
```

## Performance Considerations

### Single-threaded vs Parallel

| Execution Type | Pros | Cons | Recommended For |
|----------------|------|------|-----------------|
| Single-threaded | Stable, reliable | Slower | Docker containers, CI/CD |
| Parallel (2-4 workers) | Faster | May crash | Local development |
| Parallel (auto) | Fastest | Unstable in Docker | Local development only |

### Resource Requirements

- **Single-threaded**: ~2GB RAM, 1 CPU core
- **Parallel (2 workers)**: ~4GB RAM, 2 CPU cores
- **Parallel (auto)**: Variable, often unstable in Docker

## Examples

### Running All Integration Tests

```bash
# Recommended approach
docker-compose exec neozork-hld uv run pytest tests/integration/ -v --tb=short

# With specific markers
docker-compose exec neozork-hld uv run pytest tests/integration/ -m "not slow" -v
```

### Running Investment Flow Tests

```bash
# All investment flow tests
docker-compose exec neozork-hld uv run pytest tests/integration/test_investment_flow.py -v

# Specific test
docker-compose exec neozork-hld uv run pytest tests/integration/test_investment_flow.py::TestInvestmentFlow::test_authentication_flow -v
```

### Running Wave Analysis Tests

```bash
# All wave analysis tests
docker-compose exec neozork-hld uv run pytest tests/integration/test_wave_run_analysis_integration.py -v

# Performance tests only
docker-compose exec neozork-hld uv run pytest tests/integration/test_wave_run_analysis_integration.py -k "performance" -v
```

## Conclusion

For reliable test execution in Docker containers:

1. **Use single-threaded execution by default**
2. **Avoid `-n auto` in Docker environments**
3. **Monitor container resources**
4. **Handle database connectivity issues gracefully**
5. **Use appropriate timeouts and error handling**

This approach ensures stable, reliable test execution in containerized environments while maintaining good performance for development workflows.
