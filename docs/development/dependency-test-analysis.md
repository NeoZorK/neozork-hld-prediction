# Dependency Test Analysis

## Overview

The Dependency Test Analyzer is a powerful tool that automatically tests dependencies by temporarily disabling them and running tests to determine which packages are actually needed. This provides the most accurate way to identify truly unused dependencies.

## 🚀 How It Works

### The Testing Process
1. **Backup Creation**: Creates a backup of `requirements.txt`
2. **Package Disabling**: Temporarily comments out each package
3. **Test Execution**: Runs tests (pytest, MCP, or both)
4. **Error Analysis**: Analyzes test output for import errors
5. **Package Re-enabling**: Re-enables the package
6. **Result Reporting**: Reports which packages are required vs unused

### Test Environments
- **Native**: Local environment with `uv`
- **Docker**: Docker container environment
- **Container**: Podman container environment

### Test Types
- **pytest**: Run pytest tests only
- **mcp**: Run MCP server tests only
- **all**: Run both pytest and MCP tests (default)

## 🛠️ Tools

### 1. Dependency Test Analyzer (`scripts/analysis/dead-code/dependency_test_analyzer.py`)
The core analysis engine that performs the actual testing.

**Key Features:**
- Automatic package disabling/enabling
- Multi-environment support (native, docker, container)
- Multiple test types (pytest, MCP, all)
- Comprehensive error analysis
- Safe backup and restore mechanism
- Progress tracking with tqdm

### 2. Dependency Test Runner (`scripts/analysis/dead-code/run_dependency_test.sh`)
User-friendly bash script with interactive menu.

**Key Features:**
- Interactive menu for configuration
- Environment auto-detection
- Colored output for better readability
- Safety warnings for real execution
- Flexible output options (text/JSON)

## 📋 Usage

### Quick Start

```bash
# Interactive menu (recommended)
./scripts/analysis/dead-code/run_dependency_test.sh --interactive

# Dry run to see what would be tested
./scripts/analysis/dead-code/run_dependency_test.sh --dry-run

# Test specific packages
./scripts/analysis/dead-code/run_dependency_test.sh --packages numpy pandas --dry-run
```

### Command Line Options

```bash
./scripts/analysis/dead-code/run_dependency_test.sh [OPTIONS]

Options:
  --environment ENV     Test environment (native, docker, container)
  --test-type TYPE      Type of tests (pytest, mcp, all)
  --packages PKG1 PKG2  Specific packages to test
  --dry-run             Show what would be tested without running
  --verbose             Verbose output
  --json                Output in JSON format
  --output-file FILE    Output file path
  --help                Show this help message
```

### Direct Python Usage

```bash
# Run analyzer directly
uv run python scripts/analysis/dead-code/dependency_test_analyzer.py --dry-run

# Test specific packages
uv run python scripts/analysis/dead-code/dependency_test_analyzer.py --packages numpy pandas --test-type pytest

# Full analysis with JSON output
uv run python scripts/analysis/dead-code/dependency_test_analyzer.py --test-type all --output-format json --output-file results.json
```

## 📊 Understanding Results

### Test Summary
```
📊 SUMMARY
------------------------------------------------------------
Environment: native
Test Type: all
Total Packages: 115
Required Packages: 45
Unused Packages: 70
Test Duration: 1800.5 seconds
```

### Required Packages
```
✅ REQUIRED PACKAGES (45)
------------------------------------------------------------
  - numpy
    Error: ModuleNotFoundError
  - pandas
    Error: ImportError: No module named 'pandas'
```

### Unused Packages
```
❌ UNUSED PACKAGES (70)
------------------------------------------------------------
  - beautifulsoup4
  - requests
  - matplotlib
```

## 🔧 Advanced Configuration

### Excluded Packages
The analyzer automatically excludes certain packages from testing:

```python
exclude_packages = {
    'uv',  # Package manager itself
    'pytest',  # Testing framework
    'pytest-xdist',  # Parallel testing
    'pytest-cov',  # Coverage
    'coverage',  # Coverage
    'black',  # Code formatting
    'flake8',  # Linting
    'mypy',  # Type checking
    # ... more development/testing packages
}
```

### Test Configurations
```python
test_configs = {
    TestEnvironment.NATIVE: {
        'pytest_cmd': ['uv', 'run', 'pytest', 'tests', '-n', 'auto'],
        'mcp_cmd': ['uv', 'run', 'python', 'scripts/mcp/check_mcp_status.py'],
        'install_cmd': ['uv', 'pip', 'install', '-r', 'requirements.txt']
    },
    TestEnvironment.DOCKER: {
        'pytest_cmd': ['docker', 'exec', 'neozork-container', 'uv', 'run', 'pytest', 'tests', '-n', 'auto'],
        'mcp_cmd': ['docker', 'exec', 'neozork-container', 'uv', 'run', 'python', 'scripts/mcp/check_mcp_status.py'],
        'install_cmd': ['docker', 'exec', 'neozork-container', 'uv', 'pip', 'install', '-r', 'requirements.txt']
    }
}
```

## 📈 Workflow Examples

### 1. Initial Assessment
```bash
# Start with dry run to see what would be tested
./scripts/analysis/dead-code/run_dependency_test.sh --dry-run

# Review the list of packages that would be tested
# This helps understand the scope of the analysis
```

### 2. Focused Testing
```bash
# Test specific packages that you suspect are unused
./scripts/analysis/dead-code/run_dependency_test.sh --packages beautifulsoup4 requests --test-type pytest

# Test packages in Docker environment
./scripts/analysis/dead-code/run_dependency_test.sh --environment docker --packages numpy pandas
```

### 3. Comprehensive Analysis
```bash
# Run full analysis with all tests
./scripts/analysis/dead-code/run_dependency_test.sh --test-type all --verbose

# Save results to JSON for further analysis
./scripts/analysis/dead-code/run_dependency_test.sh --test-type all --json --output-file dependency_results.json
```

### 4. MCP Server Testing
```bash
# Test dependencies specifically for MCP server functionality
./scripts/analysis/dead-code/run_dependency_test.sh --test-type mcp --verbose

# This is useful for identifying dependencies needed for MCP server operation
```

## ⚠️ Safety Features

### Automatic Backup
- Creates `requirements.txt.backup` before any modifications
- Automatically restores from backup after testing
- Ensures your requirements file is never permanently modified

### Dry Run Mode
- Shows what would be tested without actually running tests
- Lists all packages that would be tested
- Safe way to understand the scope before execution

### Confirmation Prompts
- Warns before real execution
- Requires explicit confirmation for actual testing
- Prevents accidental package disabling

### Error Handling
- Graceful handling of test failures
- Automatic package re-enabling even if tests fail
- Detailed error reporting for troubleshooting

## 🔍 Error Analysis

### Common Error Patterns
The analyzer looks for these patterns to determine if a package is required:

```python
error_patterns = [
    r'ModuleNotFoundError',
    r'ImportError',
    r'No module named',
    r'Failed:',
    r'ERROR:',
    r'FAILED',
    r'Traceback',
    r'Exception:',
]
```

### Success Patterns
```python
success_patterns = [
    r'passed',
    r'PASSED',
    r'✓',
    r'SUCCESS',
]
```

## 🚀 Integration

### CI/CD Pipeline
```yaml
# GitHub Actions example
- name: Run dependency test analysis
  run: |
    ./scripts/analysis/dead-code/run_dependency_test.sh --test-type pytest --json --output-file dependency_results.json
    
    # Fail if too many unused packages found
    python -c "
    import json
    with open('dependency_results.json') as f:
        data = json.load(f)
    if data['unused_packages'] > 20:
        print('Too many unused packages found')
        exit(1)
    "

- name: Upload dependency results
  uses: actions/upload-artifact@v2
  with:
    name: dependency-analysis
    path: dependency_results.json
```

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: dependency-test
        name: Dependency Test Analysis
        entry: ./scripts/analysis/dead-code/run_dependency_test.sh
        args: [--test-type, pytest, --dry-run]
        language: system
        pass_filenames: false
```

## 📚 Comparison with Other Tools

| Feature | Import Analysis | Dependency Test |
|---------|----------------|-----------------|
| **Accuracy** | Medium (static analysis) | High (runtime testing) |
| **False Positives** | High | Low |
| **Dynamic Imports** | Missed | Detected |
| **Conditional Usage** | Missed | Detected |
| **Test Time** | Fast | Slow |
| **Safety** | Safe | Safe (with backup) |

## 🎯 Best Practices

### 1. **Start with Dry Run**
Always use `--dry-run` first to understand the scope:
```bash
./scripts/analysis/dead-code/run_dependency_test.sh --dry-run
```

### 2. **Test in Stages**
Don't test all packages at once:
```bash
# Test suspicious packages first
./scripts/analysis/dead-code/run_dependency_test.sh --packages beautifulsoup4 requests

# Then test core packages
./scripts/analysis/dead-code/run_dependency_test.sh --packages numpy pandas matplotlib
```

### 3. **Use Appropriate Test Types**
- **pytest**: For general functionality
- **mcp**: For MCP server dependencies
- **all**: For comprehensive testing

### 4. **Test in Multiple Environments**
```bash
# Test in native environment
./scripts/analysis/dead-code/run_dependency_test.sh --environment native

# Test in Docker
./scripts/analysis/dead-code/run_dependency_test.sh --environment docker
```

### 5. **Review Results Carefully**
- Check error messages for false positives
- Consider future usage of packages
- Test thoroughly after removing packages

## 🔍 Troubleshooting

### Common Issues

**Tests Fail Even with Package Enabled**
- Check if the package is actually used in the code
- Verify the package name in requirements.txt
- Check for version conflicts

**Package Not Found in Requirements**
- Verify the package name spelling
- Check if the package is in a different requirements file
- Ensure the package is not excluded

**Docker/Container Issues**
- Verify container is running
- Check container name in configuration
- Ensure proper permissions

### Performance Optimization

**For Large Projects**
- Test packages in smaller batches
- Use specific test types instead of 'all'
- Consider running in parallel (future enhancement)

**Timeout Issues**
- Increase timeout values in the analyzer
- Run tests with fewer parallel processes
- Use faster test environments

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the verbose output for details
3. Examine the JSON output for programmatic analysis
4. Consult the project documentation

The Dependency Test Analyzer provides the most accurate way to identify truly unused dependencies by actually testing their removal and observing the results.
