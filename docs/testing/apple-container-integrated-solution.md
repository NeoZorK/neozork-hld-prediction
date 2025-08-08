# Apple Native Container - Integrated Solution

## Overview

This document describes the integrated solution for Apple native container management and testing, which combines all functionality into a single script: `./scripts/native-container/native-container.sh`.

## 🎯 Key Features

### Container Management
- **Full Container Lifecycle**: Setup, start, stop, and cleanup
- **Emergency Recovery**: Automatic service restart and stuck container handling
- **Status Monitoring**: Real-time container status and health checks
- **Interactive Shell**: Enhanced shell with UV environment and aliases

### Integrated Testing
- **Safe Test Execution**: Memory management and thread limits for container stability
- **Staged Testing**: Tests run in safe stages to prevent resource exhaustion
- **Multiple Test Categories**: Basic, indicators, plotting, CLI, and comprehensive tests
- **Automatic Cleanup**: Environment cleanup between test stages
- **Result Reporting**: JUnit XML reports and detailed test analysis

## 🚀 Quick Start

### Interactive Mode
```bash
# Start the integrated container manager
./scripts/native-container/native-container.sh
```

### Direct Commands
```bash
# Start container and shell
./scripts/native-container/setup.sh && ./scripts/native-container/run.sh

# Run all tests safely
uv run pytest tests -n 2 --maxfail=10 --disable-warnings

# Stop container and cleanup
./scripts/native-container/stop.sh && ./scripts/native-container/cleanup.sh --all --force
```

## 📋 Menu Options

### Container Management (1-4)
1. **Start Container** - Full setup sequence with interactive shell
2. **Stop Container** - Complete cleanup with emergency recovery
3. **Show Status** - Current container status and health
4. **Restart Service** - Emergency container service management

### Testing Features (5-12)
5. **Run All Tests** - Complete test suite with safety measures
6. **Run Staged Tests** - Tests in safe, sequential stages
7. **Run Basic Tests** - Core functionality tests
8. **Run Indicator Tests** - Technical indicator calculations
9. **Run Plotting Tests** - Visualization and charting tests
10. **Run CLI Tests** - Command line interface tests
11. **Show Test Results** - Display test outcomes and reports
12. **Cleanup Test Environment** - Reset test state and cleanup

## 🔧 Technical Implementation

### Environment Management
```bash
# Thread limits for stability
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export PYTHONMALLOC=malloc

# Python environment
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export MPLCONFIGDIR=/tmp/matplotlib-cache
```

### Safe Test Execution
```bash
# Container-aware worker count
get_safe_worker_count() {
    if is_container; then
        # In container, use fewer workers for stability
        local cpu_count=$(nproc 2>/dev/null || echo 2)
        local safe_workers=$((cpu_count > 2 ? 2 : cpu_count))
        echo $safe_workers
    else
        # On host, use more workers
        local cpu_count=$(nproc 2>/dev/null || echo 4)
        echo $cpu_count
    fi
}
```

### Staged Test Execution
```bash
# Test stages for safe execution
TEST_STAGES=("basic:unit" "indicators:data:export" "plotting" "cli")

# Each stage runs with single worker and cleanup
for stage in "${TEST_STAGES[@]}"; do
    uv run pytest tests -m '$stage' -n 1 --maxfail=5
    # Cleanup between stages
    uv run python -c "import matplotlib.pyplot as plt; plt.close('all')"
done
```

## 🛡️ Safety Features

### Memory Management
- **Thread Limits**: Restrict OpenMP, MKL, and OpenBLAS threads
- **Worker Count**: Adaptive worker count based on environment
- **Memory Allocation**: Use `PYTHONMALLOC=malloc` for better memory management
- **Timeout Protection**: 5-minute timeout for test execution

### Error Recovery
- **Graceful Degradation**: Fallback options when commands fail
- **Emergency Restart**: Automatic container service restart on failures
- **Stuck Container Detection**: Identify and handle stuck containers
- **Resource Cleanup**: Automatic cleanup of temporary files and matplotlib figures

### Test Stability
- **Container-Safe Markers**: Exclude slow and performance tests in container
- **Single Worker for Plotting**: Prevent matplotlib conflicts
- **Automatic Cleanup**: Clear cache and temporary files between stages
- **Error Isolation**: Fail fast with `--maxfail` to prevent cascading failures

## 📊 Test Categories

### Basic Tests (`-m basic or unit`)
- Core functionality tests
- Essential module tests
- Basic validation tests

### Indicator Tests (`-m indicators`)
- Technical indicator calculations
- Mathematical computations
- Statistical analysis

### Plotting Tests (`-m plotting`)
- Visualization tests
- Chart generation
- Matplotlib integration

### CLI Tests (`-m cli`)
- Command line interface
- Argument parsing
- User interaction

### Data Tests (`-m data`)
- Data processing
- File I/O operations
- Data validation

### Export Tests (`-m export`)
- Data export functionality
- Format conversion
- Output validation

## 🔍 Monitoring and Debugging

### Test Results
- **JUnit XML Reports**: `logs/test-results-*.xml`
- **Console Output**: Real-time test progress
- **Error Logs**: Detailed failure information
- **Performance Metrics**: Test duration and resource usage

### Container Status
- **Health Checks**: Container running status
- **Resource Usage**: CPU and memory monitoring
- **Service Status**: Container service health
- **Error Recovery**: Automatic problem detection and resolution

### Debugging Features
- **Verbose Output**: Detailed execution information
- **Error Tracing**: Stack traces for failures
- **Environment Inspection**: Container environment verification
- **Log Analysis**: Comprehensive logging for troubleshooting

## 🚨 Troubleshooting

### Common Issues

#### Segmentation Faults
```bash
# Solution: Use safe worker count and thread limits
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
uv run pytest tests -n 1 --maxfail=5
```

#### Memory Exhaustion
```bash
# Solution: Run tests in stages with cleanup
./scripts/native-container/native-container.sh
# Choose option 6: Run Staged Tests
```

#### Container Service Issues
```bash
# Solution: Emergency service restart
./scripts/native-container/native-container.sh
# Choose option 4: Restart Service
```

#### Test Failures
```bash
# Solution: Check specific test categories
./scripts/native-container/native-container.sh
# Choose options 7-10 for specific test types
```

### Recovery Procedures

#### Stuck Container
1. Choose "Stop Container" (option 2)
2. If normal stop fails, choose "Restart Service" (option 4)
3. Retry stop operation
4. Clean up resources

#### Test Failures
1. Run "Cleanup Test Environment" (option 12)
2. Try "Run Staged Tests" (option 6)
3. Check specific test categories (options 7-10)
4. Review test results (option 11)

#### Service Issues
1. Choose "Restart Service" (option 4)
2. Wait for service to stabilize
3. Retry container operations
4. Check container status (option 3)

## 📈 Performance Optimization

### Container Environment
- **Resource Limits**: 2 CPUs, 4GB RAM
- **Thread Optimization**: Single-threaded operations where possible
- **Memory Management**: Aggressive cleanup and garbage collection
- **Cache Management**: UV cache optimization and cleanup

### Test Execution
- **Parallel Safety**: Limited parallel execution in container
- **Stage Isolation**: Independent test stages with cleanup
- **Timeout Protection**: Prevent hanging tests
- **Resource Monitoring**: Track memory and CPU usage

### Environment Variables
```bash
# Performance optimization
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
export MPLCONFIGDIR=/tmp/matplotlib-cache
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export PYTHONMALLOC=malloc
```

## 🔄 Integration with Existing Workflow

### Development Workflow
1. **Start Container**: Option 1 for development environment
2. **Run Tests**: Options 5-10 for different test categories
3. **Check Results**: Option 11 for test analysis
4. **Cleanup**: Option 12 for environment reset
5. **Stop Container**: Option 2 for cleanup

### CI/CD Integration
```bash
# Automated test execution
./scripts/native-container/native-container.sh <<< "6"
# Run staged tests non-interactively
```

### Documentation Integration
- **Setup Guides**: Native container setup documentation
- **Troubleshooting**: Comprehensive error resolution
- **Best Practices**: Container testing guidelines
- **Performance Tips**: Optimization recommendations

## 🎉 Benefits

### Unified Interface
- **Single Script**: All functionality in one place
- **Interactive Menu**: User-friendly interface
- **Consistent Experience**: Same interface for all operations
- **Error Handling**: Comprehensive error management

### Enhanced Stability
- **Memory Safety**: Prevent memory exhaustion
- **Thread Safety**: Avoid threading conflicts
- **Resource Management**: Proper cleanup and limits
- **Error Recovery**: Automatic problem resolution

### Improved Testing
- **Safe Execution**: Container-optimized test runs
- **Staged Testing**: Sequential test execution
- **Result Analysis**: Comprehensive reporting
- **Debugging Support**: Detailed error information

### Developer Experience
- **Easy Setup**: One-command container management
- **Quick Testing**: Multiple test execution options
- **Clear Feedback**: Detailed status and progress information
- **Troubleshooting**: Built-in diagnostic tools

This integrated solution provides a comprehensive, stable, and user-friendly approach to Apple native container management and testing, addressing all the issues identified in the original problem while maintaining full functionality and adding significant improvements.
