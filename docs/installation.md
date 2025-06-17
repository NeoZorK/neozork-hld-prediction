# Installation Guide

Quick setup instructions for the NeoZork HLD Prediction project.

## Prerequisites

- **Python 3.12+**
- **Git**
- **Docker** (optional, for containerized usage)

## Quick Install

```bash
# Clone repository
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction

# Install with UV (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync

# Or install with pip
pip install -r requirements.txt
```

## Usage

```bash
# Run analysis
python run_analysis.py demo

# Run EDA
python -m src.eda.eda_batch_check

# Run with Docker
docker compose up --build
```

## API Keys (Optional)

For data fetching, set environment variables:

```bash
export POLYGON_API_KEY="your_key_here"
export BINANCE_API_KEY="your_key_here"
export BINANCE_API_SECRET="your_secret_here"
```

## Troubleshooting

**ImportError issues:**
```bash
pip install --upgrade -r requirements.txt
```

**Permission errors:**
```bash
chmod +x scripts/*.sh
```

For Docker setup: [Docker Guide](docker.md)
For UV package manager: [UV Setup](uv-setup.md)