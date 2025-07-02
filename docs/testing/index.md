# Testing Documentation

This section contains comprehensive documentation for testing the NeoZork HLD Prediction project.

## Testing Categories

### Docker Testing
- [UV-Only Mode Tests](docker/uv-only-mode-tests.md) - Comprehensive testing for UV package manager in Docker environments

### CLI Testing
- [Comprehensive CLI Testing](cli/comprehensive-testing.md) - Automated testing suite for command-line interface

### Test Structure
```
tests/
├── docker/                    # Docker-specific tests
│   ├── test_uv_only_mode.py  # UV-only mode validation
│   ├── test_uv_commands.py   # UV command functionality
│   └── test_uv_simple.py     # Basic UV tests
├── cli/                       # CLI testing
│   └── comprehensive/         # Comprehensive CLI test suite
├── calculation/               # Calculation and indicator tests
├── data/                      # Data acquisition tests
├── eda/                       # EDA functionality tests
└── plotting/                  # Visualization tests
```

## Running Tests

### Docker Environment
```bash
# Run all tests
pytest tests/ -v

# Run Docker-specific tests
pytest tests/docker/ -v

# Run UV-only mode tests
pytest tests/docker/test_uv_only_mode.py -v
```

### Local Environment
```bash
# Run adaptive tests (work in both environments)
pytest tests/docker/test_uv_simple.py -v

# Run comprehensive CLI tests
python tests/cli/comprehensive/run_all_cli_tests.py

# Run with UV
uv run pytest tests -n auto
```

### CI/CD Testing with Act
```bash
# Install act tool
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash  # Linux

# Test GitHub Actions workflows (dry run - no Docker downloads)
act -n

# Test specific workflow
act -n -W .github/workflows/docker-build.yml

# Test MCP server integration
act -n -W .github/workflows/mcp-integration.yml

# List all available workflows
act -l
```

### Test Categories
- **UV-Specific Tests**: Package manager validation
- **Environment Tests**: Docker vs local detection
- **Integration Tests**: End-to-end functionality
- **Performance Tests**: UV vs pip comparison
- **CLI Tests**: Command-line interface validation
- **Native Container Tests**: Full functionality validation
- **CI/CD Tests**: GitHub Actions workflow validation
- **MCP Server Tests**: Model Context Protocol integration testing

## Test Coverage

The project maintains 100% test coverage with:
- Unit tests for all modules
- Integration tests for workflows
- Performance tests for optimization
- Environment-specific tests for Docker and local
- Comprehensive CLI testing for all commands 