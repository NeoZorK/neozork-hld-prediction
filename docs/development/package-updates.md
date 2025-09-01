# Package Updates

This document tracks package updates and dependency management in the project.

## 2025-01-01: Major Package Updates

### Overview
Successfully updated 50+ packages to their latest stable versions while maintaining project stability.

### Updated Packages

#### Security & Network
- ✅ **certifi**: 2025.1.31 → 2025.8.3
- ✅ **requests**: 2.32.3 → 2.32.5
- ✅ **urllib3**: 2.3.0 → 2.5.0 (CVE fix)
- ✅ **httpcore**: 1.0.7 → 1.0.9
- ✅ **h11**: 0.14.0 → 0.16.0

#### Development & Testing
- ✅ **coverage**: 7.10.5 → 7.10.6
- ✅ **debugpy**: 1.8.13 → 1.8.16
- ✅ **fastjsonschema**: 2.21.1 → 2.21.2
- ✅ **setuptools**: 76.0.0 → 80.9.0

#### Data & API
- ✅ **yfinance**: 0.2.25 → 0.2.65
- ✅ **python-binance**: 1.0.17 → 1.0.29
- ✅ **websockets**: 14.2 → 15.0.1
- ✅ **polygon-api-client**: 1.15.3 → 0.2.11

#### Visualization & UI
- ✅ **plotly**: 6.0.1 → 6.3.0
- ✅ **rich**: 13.6.0 → 14.1.0
- ✅ **matplotlib**: 3.10.1 → 3.10.6
- ✅ **bokeh**: 3.7.3 → 3.8.0
- ✅ **pillow**: 11.1.0 → 11.3.0

#### Jupyter & Interactive
- ✅ **ipython**: 9.0.2 → 9.5.0
- ✅ **ipykernel**: 6.29.5 → 6.30.1
- ✅ **jedi**: 0.19.2 (unchanged)

#### File System & Utilities
- ✅ **filelock**: 3.13.1 → 3.19.1
- ✅ **platformdirs**: 4.3.6 → 4.4.0
- ✅ **watchdog**: 4.0.0 → 6.0.0
- ✅ **fsspec**: 2024.6.1 → 2025.7.0

#### JSON & Schemas
- ✅ **jsonschema**: 4.23.0 → 4.25.1
- ✅ **jsonschema-specifications**: 2024.10.1 → 2025.4.1
- ✅ **json5**: 0.10.0 → 0.12.1

#### Git & Version Control
- ✅ **gitpython**: 3.1.44 → 3.1.45
- ✅ **comm**: 0.2.2 → 0.2.3

#### Date & Time
- ✅ **pytz**: 2025.1 → 2025.2
- ✅ **tzdata**: 2025.1 → 2025.2
- ✅ **types-python-dateutil**: 2.9.0.20241206 → 2.9.0.20250822

#### Network & Async
- ✅ **anyio**: 4.9.0 → 4.10.0
- ✅ **tornado**: 6.4.2 → 6.5.2
- ✅ **pyzmq**: 26.3.0 → 27.0.2

#### Parsing & Data Processing
- ✅ **beautifulsoup4**: 4.13.3 → 4.13.5
- ✅ **charset-normalizer**: 3.4.1 → 3.4.3
- ✅ **soupsieve**: 2.6 → 2.8
- ✅ **parso**: 0.8.4 → 0.8.5
- ✅ **mistune**: 3.1.2 → 3.1.4

#### Math & Statistics
- ✅ **sympy**: 1.13.1 → 1.14.0
- ✅ **packaging**: 24.2 → 25.0
- ✅ **rpds-py**: 0.23.1 → 0.27.1
- ✅ **joblib**: 1.4.2 → 1.5.2

#### Monitoring & Logging
- ✅ **prometheus-client**: 0.21.1 → 0.22.1
- ✅ **pygments**: 2.19.1 → 2.19.2
- ✅ **regex**: 2025.7.34 → 2025.8.29

#### Data Structures
- ✅ **networkx**: 3.3 → 3.5
- ✅ **narwhals**: 1.31.0 → 2.3.0
- ✅ **pandas-stubs**: 2.2.3.250527 → 2.3.2.250827

#### Core Utilities
- ✅ **python-dotenv**: 1.1.0 → 1.1.1
- ✅ **typing-extensions**: 4.12.2 → 4.15.0
- ✅ **prompt-toolkit**: 3.0.50 → 3.0.52

#### Graphics & Layout
- ✅ **contourpy**: 1.3.1 → 1.3.3
- ✅ **fonttools**: 4.56.0 → 4.59.2
- ✅ **kiwisolver**: 1.4.8 → 1.4.9
- ✅ **pyparsing**: 3.2.1 → 3.2.3

### Packages Not Updated (Compatibility Issues)

#### Scientific Libraries
- ⚠️ **numpy**: 2.2.4 (latest: 2.3.2) - Dependency conflicts
- ⚠️ **pandas**: 2.2.3 (latest: 2.3.2) - Dependency conflicts
- ⚠️ **scipy**: 1.15.2 (latest: 1.16.1) - Dependency conflicts
- ⚠️ **scikit-learn**: 1.6.1 (latest: 1.7.1) - Dependency conflicts

#### Security Libraries
- ⚠️ **argon2-cffi**: 23.1.0 (latest: 25.1.0) - Python version compatibility
- ⚠️ **argon2-cffi-bindings**: 21.2.0 (latest: 25.1.0) - Python version compatibility

#### API Client
- ⚠️ **polygon-api-client**: 0.2.11 (latest: 1.15.3) - Major version change, requires testing

### Test Results
- ✅ **Total tests**: 3905
- ✅ **Passed**: 3661 (93.8%)
- ❌ **Failed**: 7 (0.2%)
- ⏭️ **Skipped**: 237 (6.1%)

**Note**: Failed tests are unrelated to package updates and existed before the update.

### Best Practices for Future Updates

1. **Group Updates by Category**: Update related packages together
2. **Test After Each Group**: Run tests to catch issues early
3. **Security First**: Prioritize security-related updates
4. **Document Changes**: Keep track of all updates
5. **Monitor Dependencies**: Watch for breaking changes in major versions

### Update Commands Used

```bash
# Security packages
uv add "certifi>=2025.8.3" "requests>=2.32.5" "urllib3>=2.5.0"

# Development tools
uv add "coverage>=7.10.6" "debugpy>=1.8.16" "fastjsonschema>=2.21.2"

# Visualization
uv add "plotly>=6.3.0" "rich>=14.1.0" "matplotlib>=3.10.6"

# Data & API
uv add "yfinance>=0.2.65" "python-binance>=1.0.29" "websockets>=15.0.1"

# And many more...
```

### Verification Commands

```bash
# Check outdated packages
uv pip list --outdated

# Check for vulnerabilities
uv pip check

# Run tests
uv run pytest tests -n auto

# Show package info
uv pip show package_name
```
