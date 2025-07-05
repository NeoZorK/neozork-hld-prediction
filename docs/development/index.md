# Development Documentation

This section covers development setup, testing, and contribution guidelines for the NeoZork HLD Prediction project.

## 🚀 Quick Start

### Development Environment Setup
```bash
# Clone repository
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction

# Install UV package manager
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

### Docker Development
```bash
# Start development container
docker-compose up -d

# Enter container
docker-compose exec neozork bash

# Run tests inside container
pytest tests/ -v
```

## 📚 Development Guides

### [Setup](setup.md)
Complete development environment setup guide.

### [Testing](testing.md)
Comprehensive testing framework and guidelines.

### [Code Style](code-style.md)
Coding standards and conventions.

### [Debugging](debugging.md)
Debugging tools and techniques.

### [Contributing](contributing.md)
Contribution guidelines and workflow.

### [Refactoring](REFACTORING_SUMMARY.md)
Code refactoring guidelines and recent improvements.

## 🔧 UV Package Management

### UV-Only Mode
The project uses UV package manager exclusively for dependency management.

**Key Features:**
- **Exclusive UV Usage**: No fallback to pip
- **Docker Integration**: Seamless UV in containers
- **Local Development**: UV support for local environments
- **Performance**: 10-100x faster than traditional pip

### UV Commands
```bash
# Install dependencies
uv pip install -r requirements.txt

# Install development dependencies
uv pip install -r requirements-dev.txt

# Add new dependency
uv pip install package-name

# Update dependencies
uv pip install --upgrade -r requirements.txt

# List installed packages
uv pip list
```

### Environment Configuration
```bash
# Set UV-only mode
export UV_ONLY_MODE=true

# Configure cache directory
export UV_CACHE_DIR=./.uv_cache

# Configure virtual environment
export UV_VENV_DIR=./.venv
```

## 🧪 Testing Framework

### Test Structure
```
tests/
├── docker/                 # Docker-specific tests
│   ├── test_uv_only_mode.py    # Comprehensive UV tests
│   ├── test_uv_simple.py       # Simple UV tests
│   ├── test_uv_commands.py     # UV command tests
│   └── test_uv_docker.py       # Docker UV tests
├── calculation/            # Calculation tests
├── cli/                   # CLI tests
├── data/                  # Data acquisition tests
├── eda/                   # EDA tests
├── plotting/              # Plotting tests
└── utils/                 # Utility tests
```

### Running Tests

#### All Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific category
pytest tests/calculation/ -v
```

#### UV-Specific Tests
```bash
# Docker environment
pytest tests/docker/test_uv_only_mode.py -v
pytest tests/docker/test_uv_simple.py -v
pytest tests/docker/test_uv_commands.py -v

# Local environment (adaptive tests)
pytest tests/docker/test_uv_simple.py -v
python scripts/check_uv_mode.py --verbose
```

#### Adaptive Testing
Tests in `tests/docker/` are designed to work in both Docker and local environments:

- **Docker Environment**: Full validation of UV variables, paths, and commands
- **Local Environment**: Basic UV availability and local directory creation
- **Environment Detection**: Automatic detection of running environment

### Test Categories

#### Unit Tests
- Individual component testing
- Isolated functionality validation
- Mock and stub usage

#### Integration Tests
- End-to-end functionality
- Component interaction testing
- Real data processing

#### Environment Tests
- Docker vs host detection
- UV package manager validation
- Environment-specific configurations

#### Performance Tests
- Speed and efficiency validation
- Resource usage monitoring
- Scalability testing

## 🔍 Code Quality

### Linting
```bash
# Run flake8
flake8 src/ tests/

# Run black formatting
black src/ tests/

# Run isort
isort src/ tests/
```

### Type Checking
```bash
# Run mypy
mypy src/

# Run with strict mode
mypy src/ --strict
```

### Security Scanning
```bash
# Run bandit
bandit -r src/

# Run safety
safety check
```

## 🐳 Docker Development

### Development Container
```bash
# Build development image
docker-compose build

# Start development environment
docker-compose up -d

# Access container
docker-compose exec neozork bash

# Run tests in container
pytest tests/ -v
```

### UV in Docker
```bash
# Install dependencies
uv-install

# Update dependencies
uv-update

# Test UV functionality
uv-test

# Check UV status
python scripts/check_uv_mode.py
```

### Environment Variables
```bash
# Docker environment
UV_ONLY_MODE=true
UV_CACHE_DIR=/app/.uv_cache
UV_VENV_DIR=/app/.venv
PYTHONPATH=/app/src
```

## 🔧 Development Tools

### IDE Configuration
- **VS Code**: Python extension with UV support
- **PyCharm**: UV interpreter configuration
- **Vim/Neovim**: Python LSP with UV

### Debugging
```bash
# Run with debugger
python -m pdb run_analysis.py

# Use ipdb for better debugging
ipdb run_analysis.py

# Debug tests
pytest tests/ -s --pdb
```

### Profiling
```bash
# Profile with cProfile
python -m cProfile -o profile.stats run_analysis.py

# Analyze profile
python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(20)"
```

## 📊 Performance Monitoring

### Memory Usage
```bash
# Monitor memory
python -m memory_profiler run_analysis.py

# Profile specific functions
@profile
def my_function():
    pass
```

### CPU Profiling
```bash
# Profile CPU usage
python -m cProfile -o cpu_profile.stats run_analysis.py

# Visualize with snakeviz
snakeviz cpu_profile.stats
```

## 🔄 Continuous Integration

### GitHub Actions
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
      - name: Install dependencies
        run: uv pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ -v
```

### Pre-commit Hooks
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

## 🚨 Troubleshooting

### Common Issues

#### UV Installation Problems
```bash
# Check UV installation
uv --version

# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clear cache
rm -rf ~/.cache/uv
```

#### Test Failures
```bash
# Run with verbose output
pytest tests/ -v -s

# Check environment
python scripts/check_uv_mode.py --debug

# Test specific environment
python scripts/check_uv_mode.py --docker-only
```

#### Import Errors
```bash
# Check Python path
echo $PYTHONPATH

# Add src to path
export PYTHONPATH=$PYTHONPATH:./src

# Install in development mode
uv pip install -e .
```

## 📚 Additional Resources

- [UV Documentation](https://docs.astral.sh/uv/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing](https://docs.python.org/3/library/unittest.html)
- [Docker Development](https://docs.docker.com/develop/)

---

**Last Updated**: 2025-07-05
**Version**: 2.1.0 (UV-Only Mode + Refactored Plotting) 