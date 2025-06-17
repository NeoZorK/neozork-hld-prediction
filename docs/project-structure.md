# Project Structure

Key directories and files in the NeoZork HLD Prediction project.

## Core Directories

```
src/                    # Main source code
├── calculation/        # Core calculations and indicators
├── cli/               # Command-line interface
├── data/              # Data acquisition and fetchers
├── eda/               # Exploratory data analysis
├── plotting/          # Visualization tools
└── utils/             # Utility functions

scripts/               # Automation and setup scripts
├── debug_scripts/     # Debugging and testing tools
└── *.py              # Setup and utility scripts

tests/                 # Test suite
data/                  # Data storage
├── cache/            # Cached data
├── raw_parquet/      # Raw Parquet files
└── *.csv, *.parquet  # Data files

docs/                  # Documentation
```

## Key Files

- `run_analysis.py` - Main analysis entry point
- `nz` - Universal command shortcut
- `docker-compose.yml` - Docker configuration
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Project configuration
- `.github/workflows/` - CI/CD pipelines

## Module Organization

**Core Analysis:**
- `src/calculation/` - Mathematical calculations
- `src/data/` - Data acquisition
- `src/plotting/` - Visualization

**Tools:**
- `src/cli/` - Command-line tools
- `src/eda/` - Data analysis
- `src/utils/` - Helper functions

**External:**
- `scripts/` - Automation tools
- `tests/` - Test suite
- `docs/` - Documentation

For usage examples: [Getting Started](getting-started.md)