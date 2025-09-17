# Quick Start - NeoZork HLD Prediction

## 🚀 Get Running in 5 Minutes

### 1. Install Dependencies
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python dependencies
uv pip install -r requirements.txt

# Install Node.js dependencies
cd src/mobile_app && npm install && cd ..
cd src/admin_panel && npm install && cd ../..
```

### 2. Launch Main Components

#### Main Analysis
```bash
# Demo analysis
uv run run_analysis.py demo --rule PHLD

# Real data analysis
uv run run_analysis.py yfinance AAPL --rule RSI
```

#### Interactive System
```bash
# Launch interactive system
uv run python src/interactive/neozork.py
```

#### SaaS Platform
```bash
# Launch SaaS
uv run python run_saas.py
# Access: http://localhost:8080
```

#### Pocket Hedge Fund
```bash
# Launch hedge fund
uv run python run_pocket_hedge_fund.py
# Access: http://localhost:8080
```

#### Mobile Application
```bash
cd src/mobile_app
npm start
```

#### Admin Panel
```bash
cd src/admin_panel
npm run dev
# Access: http://localhost:3000
```

### 3. Testing
```bash
# All tests
uv run pytest tests -n auto

# Safe mode
./scripts/run_tests_safe.sh
```

### 4. Docker (Optional)
```bash
# Launch all services
docker-compose up -d

# Stop
docker-compose down
```

## 🔧 Useful Commands

### Status Checks
```bash
# Check UV
python scripts/utilities/check_uv_mode.py --verbose

# Check MCP
python scripts/check_mcp_status.py

# Check Docker
docker-compose ps
```

### Cleanup
```bash
# Clean UV cache
uv cache clean

# Clean Docker
docker system prune -a
```

## 🆘 Troubleshooting

### Common Issues
1. **Import errors**: `export PYTHONPATH="${PWD}:${PYTHONPATH}"`
2. **UV issues**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. **Docker issues**: `docker-compose build --no-cache`
4. **Test issues**: `./scripts/run_tests_safe.sh`

### Getting Help
```bash
# Main script help
./nz --help

# Analysis help
uv run run_analysis.py --help
```

---

**Complete Manual**: [complete-manual-en.md](complete-manual-en.md)
