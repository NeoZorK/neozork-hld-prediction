# Container Startup Fixes

## Problem Description

The container was stopping during package installation with the following error:
```
[INFO] Executing enhanced shell script...
=== NeoZork HLD Prediction Container Shell ===
Setting up environment...
Installing essential tools...
debconf: delaying package configuration, since apt-utils is not installed
```

The container was failing because:
1. Interactive prompts were being shown in non-interactive mode
2. Package installation was not configured for non-interactive mode
3. Error handling was not properly implemented for container startup

## Fixes Applied

### 1. Non-Interactive Mode Configuration

Added environment variables for non-interactive package installation:

```bash
# Non-interactive mode for package installation
export DEBIAN_FRONTEND=noninteractive
export APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
```

### 2. Interactive Prompt Handling

Modified functions to skip interactive prompts in non-interactive mode:

#### `run_data_feed_tests()` function:
```bash
# Skip interactive prompts in non-interactive mode
if [ ! -t 0 ]; then
    echo -e "\033[1;33mNon-interactive mode - skipping external data feed tests\033[0m\n"
    return 0
fi
```

#### `start_mcp_server()` function:
```bash
# Skip interactive prompts in non-interactive mode
if [ ! -t 0 ]; then
    echo -e "\033[1;33mNon-interactive mode - skipping MCP server startup\033[0m\n"
    return 0
fi
```

### 3. Error Handling Improvements

Added proper error handling to prevent container from stopping:

#### `verify_uv()` function:
```bash
# Install UV using pip (don't fail on error)
if pip install uv; then
    echo -e "\033[1;32m✅ UV installed successfully: $(uv --version)\033[0m"
else
    echo -e "\033[1;31m❌ Failed to install UV - this is required for UV-only mode\033[0m"
    echo -e "\033[1;33m⚠️  Container will continue without UV-only mode\033[0m"
    export UV_ONLY=false
fi
```

#### `install_dependencies()` function:
```bash
# Set non-interactive mode for package installation
export DEBIAN_FRONTEND=noninteractive
export APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1

# Install dependencies (don't fail on error)
if uv pip install --no-cache -r /app/requirements.txt; then
    echo -e "\033[1;32m✅ Dependencies installed successfully\033[0m"
    return 0
else
    echo -e "\033[1;31m❌ Failed to install dependencies\033[0m"
    echo -e "\033[1;33m⚠️  You can try manual installation with: uv-install\033[0m"
    echo -e "\033[1;33m⚠️  Continuing without dependencies - they can be installed later\033[0m"
    return 0
fi
```

### 4. Main Function Error Handling

Added error handling to main initialization steps:

```bash
# Step 2: Verify UV (don't fail on error)
verify_uv || true

# Step 3: Setup UV environment and install dependencies (don't fail on error)
setup_uv_environment || true
```

### 5. Container Startup Test Script

Created a comprehensive test script to verify container startup:

- **File**: `scripts/debug/test_container_startup.py`
- **Tests**: `tests/scripts/test_container_startup.py`

The test script checks:
- Environment variables
- UV package manager availability
- Python environment
- Virtual environment status
- Key directories and files
- Basic Python imports

## Testing

### Run Container Startup Tests

```bash
# Run the container startup test script
python scripts/debug/test_container_startup.py

# Run the test suite
uv run pytest tests/scripts/test_container_startup.py -v
```

### Expected Behavior

After fixes, the container should:
1. Start without stopping during package installation
2. Skip interactive prompts in non-interactive mode
3. Continue running even if some dependencies fail to install
4. Provide clear error messages and recovery options
5. Maintain full functionality in interactive mode

## Recovery Commands

If dependencies fail to install during startup, you can manually install them:

```bash
# Install dependencies manually
uv-install

# Update dependencies
uv-update

# Check UV environment
uv-test

# Run tests
uv-pytest
```

## Environment Variables

The following environment variables are now set for proper container operation:

```bash
# UV-only mode enforcement
export USE_UV=true
export UV_ONLY=true
export UV_CACHE_DIR=/app/.uv_cache
export UV_VENV_DIR=/app/.venv
export NATIVE_CONTAINER=true
export DOCKER_CONTAINER=false

# Non-interactive mode for package installation
export DEBIAN_FRONTEND=noninteractive
export APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1

# Python configuration
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export MPLCONFIGDIR=/tmp/matplotlib-cache
```

## Files Modified

1. `container-entrypoint.sh` - Main container startup script
2. `scripts/debug/test_container_startup.py` - Container startup test script
3. `tests/scripts/test_container_startup.py` - Tests for container startup functionality

## Verification

To verify the fixes work:

1. **Local Testing**: Run the container startup test script
2. **Container Testing**: Build and run the container to ensure it starts properly
3. **Interactive Mode**: Test that interactive prompts work when running in interactive mode
4. **Non-Interactive Mode**: Test that the container starts without prompts in non-interactive mode

## Future Improvements

1. Add more comprehensive error logging
2. Implement automatic retry mechanisms for failed installations
3. Add health checks for container startup
4. Create container-specific test suites
5. Add monitoring and alerting for container startup issues 