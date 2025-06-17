# CI/CD Pipeline

Continuous Integration and Deployment workflows using GitHub Actions and local testing tools.

## Overview

The project uses GitHub Actions for automated Docker building and testing. The workflow is currently focused on containerization with optional Docker Hub publishing.

## GitHub Actions Workflow

### Main Workflow File
**Location:** `.github/workflows/docker-build.yml`

**Current Triggers:**
- Push to main/master branches
- Manual workflow dispatch (workflow_dispatch)
- Pull requests (currently commented out but available)

### Actual Workflow Configuration

The workflow performs the following steps:

```yaml
name: Build and Test Docker Image

on:
  push:
    branches: [ main, master ]
  # pull_request:  # Currently commented out
  #   branches: [ main, master ]
  workflow_dispatch:  # Manual trigger

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Build Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: false
          load: true
          tags: neozork-hld-prediction:latest
          cache-from: type=gha  # GitHub Actions cache
          cache-to: type=gha,mode=max
          outputs: type=docker

      - name: Display Docker image size
        run: |
          docker images neozork-hld-prediction:latest --format "{{.Repository}}:{{.Tag}} - Size: {{.Size}}"
          docker history neozork-hld-prediction:latest

      - name: Test Docker image
        run: |
          docker run --rm neozork-hld-prediction:latest python -c "import sys; print(f'Python {sys.version} is working in the container')"

      - name: Check disk usage
        run: df -h
```

### Workflow Features

1. **Code Checkout:** Downloads repository code using `actions/checkout@v3`
2. **Docker Buildx Setup:** Configures advanced Docker build features
3. **Docker Build:** 
   - Builds image with tag `neozork-hld-prediction:latest`
   - Uses GitHub Actions cache for optimization
   - Loads image locally for testing
4. **Image Analysis:** Displays image size and layer breakdown
5. **Container Testing:** Tests Python environment functionality
6. **Resource Monitoring:** Checks disk usage after build

### Optional Docker Hub Publishing

The workflow includes a commented-out publishing job that can be enabled:

```yaml
# Uncomment to enable Docker Hub publishing
# publish:
#   needs: build
#   if: github.event_name != 'pull_request'
#   runs-on: ubuntu-latest
#   steps:
#     - name: Login to Docker Hub
#       uses: docker/login-action@v2
#       with:
#         username: ${{ secrets.DOCKER_HUB_USERNAME }}
#         password: ${{ secrets.DOCKER_HUB_TOKEN }}
#
#     - name: Build and push
#       uses: docker/build-push-action@v4
#       with:
#         context: .
#         push: true
#         tags: your-dockerhub-username/neozork-hld-prediction:latest
```

**To enable Docker Hub publishing:**
1. Set up GitHub secrets: `DOCKER_HUB_USERNAME` and `DOCKER_HUB_TOKEN`
2. Uncomment the publish job
3. Update the Docker Hub username in the tags field

## Local Testing with Act

### Testing Script

Use `test-workflow.sh` for automated local testing:

```bash
chmod +x test-workflow.sh
./test-workflow.sh
```

**What the script does:**
1. Detects system architecture (handles Apple Silicon compatibility)
2. Creates temporary `.actrc` configuration if needed
3. Runs the GitHub Actions workflow locally using act
4. Cleans up configuration afterwards

**For Apple Silicon Macs:**
- Uses `ghcr.io/catthehacker/ubuntu:act-22.04` image
- Sets `--container-architecture linux/amd64` for compatibility
- Automatically handles configuration and cleanup

**For other systems:**
- Uses standard configuration
- Runs with `ghcr.io/catthehacker/ubuntu:act-22.04` image

### Manual Act Usage

```bash
# Install act (macOS)
brew install act

# Install act (Linux)
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# List available workflows
act -l

# Run the build job
act -j build

# Run with specific runner image
act -j build -P ubuntu-latest=ghcr.io/catthehacker/ubuntu:act-22.04

# Dry run (show what would be executed)
act -n
```

## Caching Strategy

The workflow uses GitHub Actions cache (`type=gha`) to:
- Speed up Docker builds between runs
- Reduce resource usage and build times
- Cache Docker layers efficiently

## Monitoring and Debugging

### Build Information
The workflow provides monitoring through:
- Docker image size reporting
- Layer-by-layer breakdown with `docker history`
- Basic Python functionality testing
- Disk usage monitoring

### Build Status
Add build status badge to README:
```markdown
![Build Status](https://github.com/username/neozork-hld-prediction/workflows/Build%20and%20Test%20Docker%20Image/badge.svg)
```

## Performance Metrics

### Typical Execution Times

**Local Testing (Act):**
- Setup: 30-60 seconds
- Build: 2-4 minutes
- Tests: 30 seconds
- **Total: 3-5 minutes**

**GitHub Actions:**
- Queue time: 0-2 minutes
- Setup: 1-2 minutes
- Build: 3-5 minutes
- Tests: 30 seconds
- **Total: 4-9 minutes**

## Best Practices

### Current Implementation
1. **Efficient caching** - Uses GitHub Actions cache for Docker layers
2. **Basic testing** - Validates Python environment in container
3. **Resource monitoring** - Tracks disk usage and image size
4. **Manual triggers** - Supports workflow_dispatch for manual runs

### Recommended Enhancements
1. **Enable pull request testing** - Uncomment PR triggers for better CI
2. **Add comprehensive testing** - Include unit tests, linting, type checking
3. **Implement Docker Hub publishing** - Enable automatic image publishing
4. **Add notification systems** - Slack or email notifications for failures

## Troubleshooting

### Common Issues

**Act not working on Apple Silicon:**
```bash
# Use the provided test script which handles this automatically
./test-workflow.sh
```

**Docker build failures:**
```bash
# Test build locally first
docker build -t neozork-hld-prediction:latest .

# Check if dependencies are properly installed
docker run --rm neozork-hld-prediction:latest pip list
```

**Workflow not triggering:**
- Check branch names match (main/master)
- Verify workflow file syntax
- Ensure proper Git push to correct branch

### Debug Mode

```bash
# Verbose act output
act -v -j build

# Test specific step
act -j build --step
```

For more Docker details, see [Docker Setup](docker.md).
For local testing setup, see [Testing Guide](testing.md).
```bash
# Using Chocolatey
choco install act-cli

# Using Scoop
scoop install act
```

### Local Testing Script

**`test-workflow.sh`** - Automated local testing:
```bash
chmod +x test-workflow.sh
./test-workflow.sh
```

**What the script does:**
1. Checks if Act is installed
2. Validates Docker is running
3. Simulates GitHub Actions environment
4. Runs the complete workflow locally
5. Reports results and timing

**Expected execution time:** 2-5 minutes depending on hardware

### Manual Act Usage
```bash
# List available workflows
act -l

# Run default workflow
act

# Run specific workflow
act push

# Run with specific event
act pull_request

# Dry run (show what would be executed)
act -n

# Verbose output
act -v
```

## CI/CD Pipeline Components

### 1. Code Quality Checks

**Linting and Formatting:**
```yaml
- name: Code Quality
  run: |
    flake8 src/ tests/
    black --check src/ tests/
    isort --check-only src/ tests/
```

**Type Checking:**
```yaml
- name: Type Check
  run: mypy src/
```

### 2. Testing Framework

**Unit Tests:**
```yaml
- name: Unit Tests
  run: pytest tests/unit/ -v --junitxml=unit-results.xml
```

**Integration Tests:**
```yaml
- name: Integration Tests
  run: pytest tests/integration/ -v --junitxml=integration-results.xml
```

**API Tests:**
```yaml
- name: API Tests
  run: |
    python scripts/debug_scripts/debug_yfinance.py
    python scripts/debug_scripts/debug_polygon_connection.py
  env:
    POLYGON_API_KEY: ${{ secrets.POLYGON_API_KEY }}
```

### 3. Docker Build and Test

**Multi-stage Build:**
```yaml
- name: Build Docker Image
  run: |
    docker compose build
    docker compose run --rm neozork-hld python --version
```

**Container Testing:**
```yaml
- name: Test Container
  run: |
    docker compose run --rm neozork-hld python run_analysis.py demo
    docker compose run --rm neozork-hld pytest tests/ --maxfail=3
```

### 4. Performance Testing

**Benchmark Tests:**
```yaml
- name: Performance Tests
  run: |
    docker compose run --rm neozork-hld python tests/performance/benchmark.py
    docker compose run --rm neozork-hld python -m memory_profiler tests/performance/memory_test.py
```

## Environment Configuration

### Secrets Management

**GitHub Repository Secrets:**
```
Settings > Secrets and variables > Actions

Required secrets:
- POLYGON_API_KEY
- BINANCE_API_KEY
- BINANCE_API_SECRET
- DOCKER_HUB_USERNAME (if pushing images)
- DOCKER_HUB_TOKEN (if pushing images)
```

**Environment Variables:**
```yaml
env:
  TESTING: true
  LOG_LEVEL: DEBUG
  CACHE_DISABLED: true
```

### Matrix Testing

**Multiple Python Versions:**
```yaml
strategy:
  matrix:
    python-version: [3.11, 3.12]
    os: [ubuntu-latest, windows-latest, macos-latest]

steps:
- name: Set up Python ${{ matrix.python-version }}
  uses: actions/setup-python@v4
  with:
    python-version: ${{ matrix.python-version }}
```

## Workflow Optimization

### Caching Strategies

**Dependencies Caching:**
```yaml
- name: Cache pip dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

**Docker Layer Caching:**
```yaml
- name: Build with cache
  uses: docker/build-push-action@v4
  with:
    context: .
    push: false
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### Parallel Execution

**Job Parallelization:**
```yaml
jobs:
  test:
    strategy:
      matrix:
        test-type: [unit, integration, api]
    steps:
    - name: Run ${{ matrix.test-type }} tests
      run: pytest tests/${{ matrix.test-type }}/ -v
```

## Deployment Strategies

### Staging Deployment
```yaml
deploy-staging:
  needs: build-and-test
  if: github.ref == 'refs/heads/develop'
  runs-on: ubuntu-latest
  steps:
  - name: Deploy to Staging
    run: |
      docker tag neozork-hld:latest neozork-hld:staging
      # Deploy to staging environment
```

### Production Deployment
```yaml
deploy-production:
  needs: build-and-test
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  steps:
  - name: Deploy to Production
    run: |
      docker tag neozork-hld:latest neozork-hld:production
      # Deploy to production environment
```

## Monitoring and Notifications

### Build Status Badges
Add to README.md:
```markdown
![Build Status](https://github.com/username/neozork-hld-prediction/workflows/Docker%20Build%20and%20Test/badge.svg)
```

### Slack Notifications
```yaml
- name: Notify Slack
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: failure
    channel: '#ci-cd'
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### Email Notifications
Configured in repository settings under "Notifications"

## Performance Metrics

### GitHub Actions Limits

**Free Tier:**
- 2,000 minutes/month for public repositories
- 2,000 minutes/month for private repositories (GitHub Free)
- 2-core CPU, 8 GB RAM, 14 GB SSD
- 6 hours maximum job runtime

**Paid Plans:**
- 3,000-50,000 minutes depending on plan
- Larger runners available (up to 64-core, 256 GB RAM)
- Self-hosted runners option

### Typical Execution Times

**Local Testing (Act):**
- Setup: 30-60 seconds
- Build: 2-4 minutes
- Tests: 1-3 minutes
- **Total: 3-7 minutes**

**GitHub Actions:**
- Queue time: 0-2 minutes
- Setup: 1-2 minutes
- Build: 3-5 minutes
- Tests: 2-4 minutes
- **Total: 6-13 minutes**

## Best Practices

### Workflow Design
1. **Keep jobs focused** - Single responsibility per job
2. **Use matrix strategies** for multi-environment testing
3. **Implement proper caching** to reduce build times
4. **Set appropriate timeouts** to prevent runaway jobs
5. **Use conditional execution** to optimize resource usage

### Testing Strategy
1. **Fast feedback loop** - Run quick tests first
2. **Comprehensive coverage** - Include unit, integration, and e2e tests
3. **Environment parity** - Test in production-like conditions
4. **Fail fast** - Stop on first critical failure

### Security Practices
1. **Use secrets** for sensitive data
2. **Limit permissions** with least privilege principle
3. **Audit dependencies** regularly
4. **Scan for vulnerabilities** in Docker images

## Troubleshooting

### Common Issues

**Workflow not triggering:**
```bash
# Check workflow file syntax
act -n

# Validate YAML syntax
yamllint .github/workflows/
```

**Test failures:**
```bash
# Run tests locally first
pytest tests/ -v

# Check specific test
act -j test --artifact-server-path /tmp/artifacts
```

**Docker build issues:**
```bash
# Test build locally
docker compose build

# Check Act runner
act --list
act --pull=false  # Use local images
```

**Resource limits:**
```bash
# Monitor resource usage
docker stats

# Optimize Docker build
docker compose build --build-arg USE_UV=true
```

### Debug Mode
```bash
# Verbose Act output
act -v

# Step-by-step execution
act --step

# Interactive debugging
act -P ubuntu-latest=nektos/act-environments-ubuntu:18.04 -s GITHUB_TOKEN="$(gh auth token)"
```

## Advanced Configuration

### Custom Runners
```yaml
runs-on: self-hosted  # Use self-hosted runner
# or
runs-on: [self-hosted, linux, x64]  # Specific labels
```

### Conditional Workflows
```yaml
if: |
  github.event_name == 'push' ||
  (github.event_name == 'pull_request' && contains(github.head_ref, 'feature/'))
```

### Workflow Dependencies
```yaml
jobs:
  test:
    # ... test configuration
    
  deploy:
    needs: test
    if: success()
    # ... deploy configuration
```

### Custom Actions
Create reusable actions in `.github/actions/`:
```yaml
# .github/actions/setup-project/action.yml
name: 'Setup Project'
description: 'Setup Python environment and dependencies'
inputs:
  python-version:
    description: 'Python version'
    required: false
    default: '3.12'
runs:
  using: 'composite'
  steps:
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ inputs.python-version }}
    - name: Install dependencies
      shell: bash
      run: pip install -r requirements.txt
```
