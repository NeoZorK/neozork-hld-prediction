# NeoZork HLD Scripts Documentation

## Overview

The NeoZork HLD project provides two main command-line scripts for analysis and data exploration:

- **`nz`** - Main analysis script for running indicator calculations and generating plots
- **`eda`** - Data exploration and analysis script for quality checks and statistical analysis

Both scripts are designed to work seamlessly in both Docker and native environments.

## Scripts

### nz - Main Analysis Script

The `nz` script is the primary interface for running indicator analysis and generating visualizations.

#### Usage

```bash
# Basic usage
./nz [options]

# With uv (recommended for native environment)
uv run ./nz [options]

# Direct execution
./nz [options]
```

#### Environment Detection

The script automatically detects whether it's running in a Docker container or native environment:

- **Docker Environment**: Uses `python run_analysis.py` directly
- **Native Environment**: Uses `uv run python run_analysis.py` (with fallback to direct Python)

#### Examples

```bash
# Show version
./nz --version

# Show help
./nz --help

# Run demo analysis
./nz demo --rule PHLD

# Analyze YFinance data
./nz yfinance MSFT --rule PHLD

# Analyze MQL5 data
./nz mql5 EURUSD --interval H4 --rule PHLD

# Run with specific parameters
./nz --input-file data.csv --output-dir ./results --plot-type detailed
```

### eda - Data Exploration Script

The `eda` script provides comprehensive data quality checks and statistical analysis capabilities.

#### Usage

```bash
# Basic usage
./eda [options]

# With uv (recommended for native environment)
uv run ./eda [options]

# Direct execution
./eda [options]
```

#### Environment Detection

Similar to `nz`, the script automatically detects the environment:

- **Docker Environment**: Uses `python src/eda/eda_batch_check.py` directly
- **Native Environment**: Uses `uv run python src/eda/eda_batch_check.py` (with fallback to direct Python)

#### Examples

```bash
# Show help
./eda --help

# Run data quality checks
./eda --data-quality-checks

# Check for specific issues
./eda --nan-check --duplicate-check

# Fix data quality issues
./eda --fix-files --fix-all

# Run statistical analysis
./eda --descriptive-stats

# Analyze specific file
./eda --file mydata.parquet --nan-check

# Clean up logs and reports
./eda --clean-stats-logs --clean-reports
```

## Environment Setup

### Native Environment

1. **Install uv** (recommended):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**:
   ```bash
   uv sync
   ```

3. **Add scripts to PATH** (optional):
   ```bash
   export PATH="/path/to/neozork-hld-prediction:$PATH"
   ```

### Docker Environment

1. **Build and run container**:
   ```bash
   docker-compose up -d
   ```

2. **Access container**:
   ```bash
   docker exec -it <container_name> bash
   ```

3. **Use scripts directly**:
   ```bash
   nz --version
   eda --help
   ```

## Script Behavior

### Environment Detection Logic

Both scripts use the following logic to determine the execution environment:

```bash
# Check if running inside a Docker container
IN_DOCKER=false
if [ -f /.dockerenv ] || grep -q docker /proc/1/cgroup 2>/dev/null; then
    IN_DOCKER=true
fi
```

### Execution Path

1. **Docker Environment**:
   - Direct Python execution
   - No dependency management needed (pre-installed)

2. **Native Environment**:
   - Try `uv run` first (recommended)
   - Fallback to direct Python if `uv` unavailable

### Error Handling

- Graceful fallback from `uv run` to direct Python
- Clear environment detection messages
- Proper error reporting for missing dependencies

## Integration with Docker

### Docker Entrypoint

The `docker-entrypoint.sh` creates wrapper scripts in `/tmp/bin/`:

```bash
# nz wrapper
python /app/run_analysis.py "$@"

# eda wrapper  
python /app/src/eda/eda_batch_check.py "$@"
```

### Container Usage

Inside Docker containers, scripts work seamlessly:

```bash
# Direct execution
nz --version
eda --help

# Full analysis workflow
nz demo --rule PHLD
eda --data-quality-checks
```

## Best Practices

### Native Development

1. **Use uv for dependency management**:
   ```bash
   uv run ./nz --version
   ```

2. **Keep scripts in PATH**:
   ```bash
   export PATH="/path/to/project:$PATH"
   nz --help
   ```

3. **Use virtual environment**:
   ```bash
   uv venv
   source .venv/bin/activate
   ./nz --version
   ```

### Docker Development

1. **Use container scripts directly**:
   ```bash
   docker exec -it <container> nz --version
   ```

2. **Interactive development**:
   ```bash
   docker exec -it <container> bash
   nz demo --rule PHLD
   ```

3. **Volume mounting for results**:
   ```bash
   docker run -v $(pwd)/results:/app/results <image> nz demo --rule PHLD
   ```

## Troubleshooting

### Common Issues

1. **uv not found**:
   - Script falls back to direct Python
   - Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

2. **Permission denied**:
   - Make scripts executable: `chmod +x nz eda`

3. **Docker not running**:
   - Scripts work in native mode automatically
   - No Docker required for basic functionality

4. **Python path issues**:
   - Use `uv run` for proper environment isolation
   - Check `PYTHONPATH` in Docker containers

### Debug Information

Enable debug output:

```bash
# Check environment detection
./nz --version  # Shows "Running in native environment with uv" or "Running in Docker environment"

# Check uv availability
which uv

# Check Python path
python -c "import sys; print(sys.path)"
```

## File Structure

```
neozork-hld-prediction/
├── nz                    # Main analysis script
├── eda                   # Data exploration script
├── run_analysis.py       # Main analysis entry point
├── src/
│   └── eda/
│       └── eda_batch_check.py  # EDA functionality
├── docker-entrypoint.sh  # Docker container setup
└── docs/
    └── scripts.md        # This documentation
```

## Main Scripts

### `run_analysis.py`