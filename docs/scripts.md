# Scripts Overview

Complete guide to all available scripts and automation tools.

## Core Scripts

### `nz` - Main Command Tool
**Location:** `./nz`
**Purpose:** Universal command shortcut for all analysis operations

```bash
# Basic usage
nz demo
nz demo --rule PHLD

# Data analysis
nz yf -t AAPL --period 1mo --point 0.01
nz csv --csv-file data.csv --point 0.01

# Show cached data
nz show yf aapl
```

**Features:**
- Smart environment detection (Docker/local)
- PATH integration for global access
- All parameters compatible with `run_analysis.py`

### `run_analysis.py` - Main Analysis Engine
**Location:** `./run_analysis.py`
**Purpose:** Core analysis and prediction pipeline

```bash
# Direct usage
python run_analysis.py demo
python run_analysis.py --examples
python run_analysis.py --help
```

## Setup and Initialization

### `scripts/init_dirs.sh` - Project Setup
**Purpose:** Initialize project directory structure and environment

```bash
# Run from project root
./scripts/init_dirs.sh
```

**What it does:**
- Creates data directories (`data/cache/`, `data/raw_parquet/`, etc.)
- Creates log and results directories
- Generates `.env` file template
- Sets up source directories

**Testing:**
```bash
# Test the script
bats tests/scripts/test_init_dirs.bats
```

### `scripts/run_tests.py` - Test Runner
**Purpose:** Unified test execution and reporting

```bash
# Run all tests
python scripts/run_tests.py

# Specific test categories
python scripts/run_tests.py --unit
python scripts/run_tests.py --integration
python scripts/run_tests.py --cli
```

## Requirements Management

### `scripts/analyze_requirements.py` - Dependency Analyzer
**Purpose:** Analyze project imports and detect unused dependencies

```bash
# Basic analysis
python scripts/analyze_requirements.py

# Detailed report
python scripts/analyze_requirements.py --detailed

# Show unused packages
python scripts/analyze_requirements.py --unused-only
```

**Features:**
- Scans all Python files for imports
- Compares with `requirements.txt`
- Identifies unused dependencies
- Generates cleanup recommendations
- Uses grep for efficient processing

**Output Example:**
```
📊 Requirements Analysis Report
============================

✅ Used packages (45):
  - pandas: 23 imports across 15 files
  - numpy: 18 imports across 12 files
  - matplotlib: 8 imports across 5 files

⚠️  Unused packages (3):
  - some-unused-package
  - another-package
  - old-dependency

💡 Recommendations:
  - Remove unused packages to reduce size
  - Update package versions
  - Consider consolidating similar packages
```

### `scripts/auto_pyproject_from_requirements.py` - Project File Generator
**Purpose:** Generate `pyproject.toml` from `requirements.txt`

```bash
# Generate pyproject.toml
python scripts/auto_pyproject_from_requirements.py

# Custom template
python scripts/auto_pyproject_from_requirements.py --template custom.toml
```

**Features:**
- Converts requirements.txt to modern pyproject.toml
- Includes project metadata
- Sets up build system configuration
- Handles version constraints

## UV Package Manager Scripts

### `uv_setup/setup_uv.sh` - UV Installation
**Purpose:** Automated UV package manager setup

```bash
# Make executable and run
chmod +x uv_setup/setup_uv.sh
./uv_setup/setup_uv.sh
```

**What it does:**
- Downloads and installs UV safely
- Creates virtual environment
- Installs project dependencies
- Configures environment variables

### `uv_setup/update_deps.sh` - Dependency Updates
**Purpose:** Update all project dependencies using UV

```bash
# Update dependencies
chmod +x uv_setup/update_deps.sh
./uv_setup/update_deps.sh
```

**Features:**
- Checks UV installation
- Activates virtual environment
- Updates to latest package versions
- Colored output for readability

## CI/CD and Testing

### `test-workflow.sh` - GitHub Actions Local Testing
**Purpose:** Test GitHub Actions workflows locally using Act

```bash
# Make executable and run
chmod +x test-workflow.sh
./test-workflow.sh
```

**What it does:**
- Simulates GitHub Actions environment
- Tests Docker build process
- Validates workflow configuration
- Provides early feedback before pushing

**Requirements:**
- [Act](https://github.com/nektos/act) installed
- Docker running

### `eda` - EDA Batch Processing
**Purpose:** Shortcut for exploratory data analysis

```bash
# Run EDA checks
./eda

# Equivalent to:
python src/eda/eda_batch_check.py --data-quality-checks
```

## Debug Scripts Collection

**Location:** `scripts/debug_scripts/`

### Connection Testing Scripts

#### `debug_yfinance.py` - Yahoo Finance Testing
```bash
python scripts/debug_scripts/debug_yfinance.py
```
Tests Yahoo Finance API connectivity and data fetching.

#### `debug_polygon_connection.py` - Polygon.io Testing
```bash
python scripts/debug_scripts/debug_polygon_connection.py
```
Tests Polygon.io API connection and authentication.

#### `debug_binance_connection.py` - Binance Testing
```bash
python scripts/debug_scripts/debug_binance_connection.py
```
Tests Binance API connectivity and permissions.

### Data Validation Scripts

#### `debug_csv_reader.py` - CSV Processing Testing
```bash
python scripts/debug_scripts/debug_csv_reader.py
```
Validates CSV file reading and processing logic.

#### `debug_check_parquet.py` - Parquet File Validation
```bash
python scripts/debug_scripts/debug_check_parquet.py
```
Checks integrity of cached Parquet files.

### Data Examination Scripts

#### `examine_parquet.py` - Parquet File Inspector
```bash
python scripts/debug_scripts/examine_parquet.py data/file.parquet
```
Detailed examination of Parquet file structure and content.

#### `examine_binance_parquet.py` - Binance Data Inspector
```bash
python scripts/debug_scripts/examine_binance_parquet.py
```
Specialized examination of Binance-sourced data files.

## Docker Integration Scripts

### `docker-entrypoint.sh` - Container Startup
**Purpose:** Container initialization and service startup

**Automatic actions:**
1. Run all debug scripts
2. Start MCP server (optional)
3. Display help information
4. Provide interactive shell

**Usage:** Automatically executed in Docker containers

## Script Usage Patterns

### Common Workflows

**Initial Project Setup:**
```bash
./scripts/init_dirs.sh
./uv_setup/setup_uv.sh
python scripts/run_tests.py
```

**Development Workflow:**
```bash
# Make changes
git add .
git commit -m "Changes"

# Test before push
./test-workflow.sh
python scripts/run_tests.py
```

**Dependency Management:**
```bash
# Check for unused packages
python scripts/analyze_requirements.py

# Update dependencies
./uv_setup/update_deps.sh

# Generate modern config
python scripts/auto_pyproject_from_requirements.py
```

**Debugging Issues:**
```bash
# Test API connections
python scripts/debug_scripts/debug_yfinance.py
python scripts/debug_scripts/debug_polygon_connection.py

# Check data integrity
python scripts/debug_scripts/debug_check_parquet.py
./eda
```

### Script Permissions

Make scripts executable:
```bash
chmod +x scripts/init_dirs.sh
chmod +x uv_setup/*.sh
chmod +x test-workflow.sh
chmod +x nz
chmod +x eda
```

## Custom Script Development

### Adding New Scripts

1. **Create script file:**
```bash
touch scripts/my_custom_script.py
chmod +x scripts/my_custom_script.py
```

2. **Add shebang and documentation:**
```python
#!/usr/bin/env python3
"""
Custom Script

Description of what the script does.
"""
```

3. **Add to test suite:**
```bash
# Create test file
touch tests/scripts/test_my_custom_script.py
```

### Script Best Practices

1. **Use proper shebangs:** `#!/usr/bin/env python3` or `#!/bin/bash`
2. **Include documentation:** Docstrings and comments
3. **Handle errors gracefully:** Try/except blocks and exit codes
4. **Make scripts executable:** `chmod +x`
5. **Add help options:** `--help` flag
6. **Use consistent naming:** Descriptive, lowercase with underscores
7. **Test thoroughly:** Unit tests and integration tests

### Script Templates

**Python script template:**
```python
#!/usr/bin/env python3
"""
Script Name

Brief description of functionality.
"""

import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Script description")
    parser.add_argument("--option", help="Option description")
    args = parser.parse_args()
    
    # Script logic here
    print("Script executed successfully")

if __name__ == "__main__":
    main()
```

**Shell script template:**
```bash
#!/bin/bash
set -euo pipefail

# Script Name
# Brief description

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Functions
usage() {
    echo "Usage: $0 [options]"
    echo "  -h, --help    Show this help"
}

# Main logic
main() {
    echo "Script executed successfully"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

main "$@"
```
