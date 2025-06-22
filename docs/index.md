# Documentation Index

Complete guide to NeoZork HLD Prediction project.

## Quick Start

- **[Getting Started](getting-started.md)** - Project overview, installation, and quick setup
- **[Usage Examples](usage-examples.md)** - Common commands and use cases

## Core Documentation

- **[Docker](docker.md)** - Containerized development
- **[Exchange Rate API](exchange-rate-api-complete.md)** - Real-time forex data integration
- **[Indicator Export](indicator-export.md)** - New export feature for calculated indicators
- **[MCP Server](mcp-servers/mcp-server.md)** - Model Context Protocol server
- **[UV Setup](uv-setup.md)** - Fast package manager

## Tools & Analysis

- **[Analysis & EDA](analysis-eda.md)** - Data analysis and exploration tools
- **[Scripts](scripts.md)** - Available scripts and automation
- **[Utility Scripts](utility-scripts.md)** - Data conversion and test file management utilities
- **[Debug Scripts](debug-scripts.md)** - Testing and debugging tools

## Development

- **[Testing](testing.md)** - Testing framework and validation
- **[CI/CD](ci-cd.md)** - GitHub Actions and local testing
- **[Project Structure](project-structure.md)** - Directory organization

## Export Flags: Allowed Modes

Export flags (`--export-parquet`, `--export-csv`, `--export-json`) are only available in `demo` mode. They are not allowed in `show ind`, `yfinance`, `csv`, `polygon`, `binance`, or `exrate` modes.

### Example Workflow

1. **Download or Convert Data**
   - Download with yfinance:
     ```bash
     python run_analysis.py yfinance --ticker EURUSD=X --period 1y --point 0.00001
     ```
   - Or convert from CSV:
     ```bash
     python run_analysis.py csv --csv-file mydata.csv --point 0.01
     ```
2. **Apply Indicator and Export**
   - Use show mode with a rule and export flags:
     ```bash
     python run_analysis.py show yfinance EURUSD=X --rule PHLD --export-parquet --export-csv --export-json
     ```
3. **View Exported Indicators**
   - Use show ind to view the exported files:
     ```bash
     python run_analysis.py show ind parquet
     python run_analysis.py show ind csv
     python run_analysis.py show ind json
     ```

> Export flags are not available in `show ind`, `yfinance`, `csv`, `polygon`, `binance`, or `exrate` modes. Use `demo` for direct export, or the above workflow for real data.

## Navigation by Role

### New Users
1. [Getting Started](getting-started.md)
2. [Usage Examples](usage-examples.md)

### Developers
1. [Project Structure](project-structure.md)
2. [Testing](testing.md)
3. [CI/CD](ci-cd.md)
4. [Debug Scripts](debug-scripts.md)

### Data Scientists
1. [Exchange Rate API](exchange-rate-api-complete.md)
2. [Analysis & EDA](analysis-eda.md)
3. [Usage Examples](usage-examples.md)
4. [Scripts](scripts.md)

### DevOps
1. [Docker](docker.md)
2. [CI/CD](ci-cd.md)
3. [UV Setup](uv-setup.md)

## By Task

**Setup:**
- [Getting Started](getting-started.md) (includes installation)

**Usage:**
- [Usage Examples](usage-examples.md) → [Exchange Rate API](exchange-rate-api-complete.md) → [Analysis & EDA](analysis-eda.md)

**Development:**
- [Project Structure](project-structure.md) → [Testing](testing.md) → [CI/CD](ci-cd.md)

**Deployment:**
- [Docker](docker.md) → [CI/CD](ci-cd.md) → [MCP Server](mcp-servers/mcp-server.md)