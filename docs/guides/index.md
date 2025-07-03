# Guides

This section provides step-by-step guides and tutorials for using the NeoZork HLD Prediction project, including UV package management and adaptive testing.

## 🚀 Quick Start Guides

### [Getting Started Guide](getting-started.md)
Complete step-by-step guide for setting up the project.

**Covers:**
- System requirements and prerequisites
- Installation methods (Docker and local)
- Initial configuration
- First analysis run
- Troubleshooting common issues

### [UV Package Management Guide](uv-package-management.md) ⭐ **NEW**
Comprehensive guide for UV package manager usage.

**Highlights:**
- **UV Installation**: Installing and configuring UV
- **Docker Integration**: UV usage in containers
- **Local Development**: UV for local environments
- **Adaptive Testing**: Tests that work in both environments
- **Performance Optimization**: UV vs traditional pip

## 🔧 Setup and Configuration

### [Docker Setup](docker-setup.md)
Complete guide for containerized development and deployment.

**Features:**
- Docker installation and configuration
- Container management
- UV integration in Docker
- Environment variables
- Service orchestration

### [Local Development Setup](local-setup.md)
Setting up a local development environment.

**Includes:**
- Python environment setup
- UV package manager installation
- Virtual environment configuration
- Development tools setup
- Testing environment

### [IDE Configuration](ide-configuration.md)
Configuring your IDE for optimal development experience.

**Covers:**
- VS Code configuration
- PyCharm setup
- Vim/Neovim configuration
- MCP server integration
- Debugging setup

## 🧪 Testing and Quality Assurance

### [Testing Guide](testing-guide.md)
Comprehensive testing framework and guidelines.

**Includes:**
- Test structure and organization
- Running tests in different environments
- UV-specific testing
- Adaptive testing patterns
- Test coverage and quality

### [UV Testing Guide](uv-testing-guide.md) ⭐ **NEW**
Specialized guide for UV package manager testing.

**Highlights:**
- **Docker Testing**: UV tests in containers
- **Local Testing**: UV tests in local environment
- **Adaptive Testing**: Environment-aware tests
- **Performance Testing**: UV vs pip comparison
- **Integration Testing**: End-to-end UV validation

### [Code Quality Guide](code-quality.md)
Maintaining high code quality standards.

**Covers:**
- Linting and formatting
- Type checking
- Security scanning
- Code review process
- Best practices

## 📊 Analysis and Data

### [Data Sources Guide](data-sources.md)
Working with different financial data sources.

**Includes:**
- Polygon API integration
- YFinance data access
- Binance cryptocurrency data
- MQL5 MetaTrader data
- Data quality assessment

### [Technical Indicators Guide](indicators.md)
Using technical indicators for analysis.

**Covers:**
- Momentum indicators
- Oscillators
- Trend indicators
- Volatility indicators
- Volume indicators
- Support & Resistance
- Predictive indicators
- Probability indicators
- Sentiment indicators

### [Analysis Tools Guide](analysis-tools.md)
Using analysis and visualization tools.

**Features:**
- Exploratory Data Analysis (EDA)
- Data visualization
- Statistical analysis
- Pattern recognition
- Result interpretation

### [Vertical Scrollbar for AUTO Mode](vertical-scrollbar-auto-mode.md) ⭐ **NEW**
Enhanced AUTO mode with vertical scrollbar functionality.

**Highlights:**
- **Vertical Scrolling**: Navigate through all charts without overlapping
- **Custom CSS**: Beautiful scrollbar with hover effects
- **Information Panel**: Built-in statistics and chart details
- **Responsive Design**: Works on different screen sizes
- **Browser Compatibility**: Cross-browser support

## 🔧 Development and Automation

### [CLI Interface Guide](cli-interface.md)
Using the command-line interface.

**Covers:**
- Basic commands
- Data source options
- Analysis parameters
- Output formats
- Automation scripts

### [Scripts Guide](scripts.md)
Using utility scripts and automation tools.

**Includes:**
- Data processing scripts
- Analysis automation
- UV management scripts
- Environment setup scripts
- Debugging utilities

### [Debug Scripts Guide](debug-scripts.md)
Troubleshooting and debugging tools.

**Features:**
- Common issue diagnosis
- Debug scripts usage
- Log analysis
- Performance profiling
- Error resolution

## 🐳 Docker and Deployment

### [Docker Guide](docker-guide.md)
Complete Docker usage guide.

**Covers:**
- Container management
- Service orchestration
- Environment configuration
- Volume management
- Network setup

### [UV in Docker Guide](uv-docker-guide.md) ⭐ **NEW**
Specialized guide for UV package manager in Docker.

**Highlights:**
- **UV Installation**: Installing UV in containers
- **Dependency Management**: UV vs pip in Docker
- **Cache Optimization**: UV cache in containers
- **Performance**: UV performance in Docker
- **Troubleshooting**: Common UV Docker issues

### [Deployment Guide](deployment-guide.md)
Production deployment guidelines.

**Includes:**
- Production environment setup
- Configuration management
- Monitoring and logging
- Security considerations
- Performance optimization

## 🔍 Advanced Topics

### [MCP Server Guide](mcp-server-guide.md)
Model Context Protocol server configuration.

**Covers:**
- MCP server setup
- IDE integration
- Environment detection
- Server configuration
- Usage examples

### [Performance Optimization Guide](performance-optimization.md)
Optimizing application performance.

**Features:**
- UV package manager optimization
- Docker performance tuning
- Memory and CPU optimization
- Caching strategies
- Profiling tools

### [Security Guide](security-guide.md)
Security best practices and considerations.

**Includes:**
- Container security
- Package verification
- Environment isolation
- Input validation
- Access control

## 📚 UV Package Management

### UV Commands Reference
```bash
# Basic UV commands
uv --version                    # Check UV version
uv pip install package          # Install package
uv pip install -r requirements.txt  # Install from requirements
uv pip list                     # List installed packages
uv pip uninstall package        # Uninstall package

# Virtual environment management
uv venv                         # Create virtual environment
uv venv --python 3.11           # Create with specific Python version
source .venv/bin/activate       # Activate virtual environment

# Cache management
uv cache clean                  # Clean cache
uv cache info                   # Cache information

# Performance commands
uv pip install --no-cache       # Install without cache
uv pip install --upgrade        # Upgrade packages
```

### UV Environment Variables
```bash
# UV configuration
export UV_ONLY_MODE=true        # Enable UV-only mode
export UV_CACHE_DIR=./.uv_cache # Set cache directory
export UV_VENV_DIR=./.venv      # Set virtual environment directory
export UV_PYTHON=python3.11     # Set Python version

# Docker environment
UV_ONLY_MODE=true
UV_CACHE_DIR=/app/.uv_cache
UV_VENV_DIR=/app/.venv
PYTHONPATH=/app/src
```

### UV Testing Commands
```bash
# Test UV functionality
python scripts/check_uv_mode.py --verbose

# Run UV-specific tests
pytest tests/docker/test_uv_simple.py -v
pytest tests/docker/test_uv_commands.py -v
pytest tests/docker/test_uv_only_mode.py -v

# Test in Docker
docker-compose exec neozork uv-test
docker-compose exec neozork pytest tests/docker/ -v
```

## 🧪 Adaptive Testing

### Environment Detection
```python
# Example: Adaptive test structure
def test_uv_functionality():
    """Test UV functionality based on environment."""
    if is_docker_environment():
        # Full validation in Docker
        assert check_uv_variables()
        assert check_uv_paths()
        assert check_uv_commands()
        assert check_uv_packages()
    else:
        # Basic validation in local environment
        assert check_uv_installation()
        assert check_local_directories()
        assert check_uv_basic_commands()
```

### Test Categories

#### Docker Environment Tests
- **Full UV Validation**: All UV variables, paths, and commands
- **Container Integration**: UV integration with Docker
- **Service Orchestration**: Multi-service testing
- **Performance Testing**: UV performance in containers

#### Local Environment Tests
- **Basic UV Validation**: UV installation and basic commands
- **Local Directory Creation**: Cache and virtual environment setup
- **Package Management**: Basic package operations
- **Development Tools**: Local development workflow

#### Adaptive Tests
- **Environment Detection**: Automatic environment identification
- **Conditional Testing**: Environment-specific test execution
- **Cross-Platform**: Tests that work on different platforms
- **Fallback Behavior**: Graceful degradation for missing features

## 📊 Real-World Workflows

### Development Workflow
```bash
# 1. Setup development environment
git clone <repository>
cd neozork-hld-prediction

# 2. Install UV and dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
uv pip install -r requirements.txt
uv pip install -r requirements-dev.txt

# 3. Run tests
pytest tests/ -v

# 4. Check code quality
python scripts/check_uv_mode.py --verbose

# 5. Docker testing
docker-compose up -d
docker-compose exec neozork pytest tests/docker/ -v
```

### Analysis Workflow
```bash
# 1. Start Docker environment
docker-compose up -d

# 2. Install dependencies
docker-compose exec neozork uv-install

# 3. Run analysis
docker-compose exec neozork nz yfinance AAPL --rule PHLD

# 4. Generate visualizations
docker-compose exec neozork python -m src.plotting.fast_plot

# 5. Export results
docker-compose exec neozork python -m src.export.csv_export
```

### UV Package Management Workflow
```bash
# 1. Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Configure environment
export UV_ONLY_MODE=true
export UV_CACHE_DIR=./.uv_cache

# 3. Install dependencies
uv pip install -r requirements.txt

# 4. Create virtual environment
uv venv

# 5. Activate environment
source .venv/bin/activate

# 6. Verify installation
python scripts/check_uv_mode.py

# 7. Run tests
pytest tests/docker/test_uv_simple.py -v
```

## 🚨 Troubleshooting

### Common UV Issues
```bash
# Issue: UV not found
# Solution: Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Issue: Cache directory not accessible
# Solution: Create cache directory
mkdir -p ./.uv_cache

# Issue: Virtual environment not found
# Solution: Create virtual environment
uv venv

# Issue: Package installation fails
# Solution: Check network and try again
uv pip install --upgrade pip
uv pip install package-name
```

### Common Test Issues
```bash
# Issue: Tests fail in local environment
# Solution: Check environment detection
python scripts/check_uv_mode.py --debug

# Issue: Docker tests fail
# Solution: Check container environment
docker-compose exec neozork env | grep UV

# Issue: Import errors
# Solution: Check Python path
export PYTHONPATH=$PYTHONPATH:./src
```

## 📚 Additional Resources

### Documentation
- **Getting Started**: Basic setup and installation
- **Examples**: Practical usage examples
- **Reference**: Technical documentation
- **API Documentation**: External API references

### Community
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: Community discussions
- **Documentation**: Comprehensive guides and references

### Tools
- **UV Documentation**: Official UV documentation
- **Docker Documentation**: Docker usage guides
- **Pytest Documentation**: Testing framework guides

---

**Last Updated**: 2024
**Version**: 2.0.0 (UV-Only Mode) 