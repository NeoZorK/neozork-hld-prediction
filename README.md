# NeoZork HLD Prediction

A professional trading indicator enhancement system using Machine Learning techniques to improve High, Low, and Direction (HLD) predictions for financial instruments.

## 📚 Documentation

**📋 [Complete Documentation Index](docs/index.md)** - All documentation organized by category and role

### Core Documentation
- [📋 Project Overview](docs/overview.md) - Core goals, features and methodology
- [⚙️ Installation Guide](docs/installation.md) - Complete setup instructions
- [🚀 Quick Start](docs/quick-start.md) - Get started fast
- [💻 Usage Examples](docs/usage-examples.md) - Comprehensive command examples

### Technical Documentation
- [🐳 Docker Guide](docs/docker.md) - Docker setup and configuration
- [🤖 MCP Server](docs/mcp-server.md) - GitHub Copilot integration
- [⚡ UV Package Manager](docs/uv-setup.md) - Fast Python package management
- [🧪 Testing](docs/testing.md) - Running tests and validation

### Tools & Scripts
- [🔧 Scripts Overview](docs/scripts.md) - All available scripts and tools
- [📊 EDA Tools](docs/eda-tools.md) - Exploratory Data Analysis utilities
- [🔍 Debug Scripts](docs/debug-scripts.md) - Connection and data debugging
- [📈 Analysis Tools](docs/analysis-tools.md) - Core analysis workflow

### Workflow & Development
- [📅 Project Workflow](docs/workflow.md) - Development phases and status
- [🔄 CI/CD](docs/ci-cd.md) - GitHub Actions and testing workflow
- [📁 Project Structure](docs/project-structure.md) - Code organization

## Quick Reference

```bash
# Install and setup
./scripts/init_dirs.sh
pip install -r requirements.txt

# Run demo analysis
python run_analysis.py demo

# Or use the nz shortcut
nz demo --rule PHLD
```

For detailed usage, see [Usage Examples](docs/usage-examples.md).

## Tech Stack

- **Language:** Python 3.12+
- **ML Libraries:** scikit-learn, xgboost, lightgbm
- **Data Sources:** Yahoo Finance, Polygon.io, Binance, CSV
- **Visualization:** matplotlib, plotly, seaborn
- **Environment:** Docker, uv package manager

## License

This project is part of proprietary trading indicator development.
