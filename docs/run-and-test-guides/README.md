# Run and Test Guides / Run and Test Guides

## 📁 Structure / Structure

```
docs/run-and-test-guides/
├── index.md # main page / main page
├── project-Structure.md # Project Structure / Project Structure
├── Troubleshooting.md # Troubleshooting / Troubleshooting
├── faq.md # Frequently Asked Questions / FAQ
├── russian/ # Russian Version / Russian Version
│ ├── complete-manual-ru.md # Complete guide / Complete manual
│ ├── quick-start-ru.md # Quick start / Quick start
│ ├── testing-guide-ru.md # guide on testing / testing guide
│ └── deployment-guide-ru.md # guide on deployment / deployment guide
└── english/ # English Version / English Version
 ├── complete-manual-en.md # Complete manual
 ├── quick-start-en.md # Quick start
 ├── testing-guide-en.md # testing guide
 └── deployment-guide-en.md # deployment guide
```

## ♪ Quick access / Quick Access

### Russian Version / Russian Version
- [Complete guide](russian/complete-manual-ru.md) - Detailed guide on all components
- [Quick Start] (Russian/Quick-start-ru.md) - Launch for 5 minutes
- [Guide on test] (russian/testing-guide-ru.md) - All about testing
- [Guide on release] (russian/development-guid-ru.md) - Deployment in sales

### English Version
- [Complete Manual](english/complete-manual-en.md) - Comprehensive guide for all components
- [Quick start](english/quick-start-en.md) - Get running in 5 minutes
- [testing Guide](english/testing-guide-en.md) - Everything about testing
- [deployment Guide](english/deployment-guide-en.md) - Production deployment

## ♪ components of the system / system components

### Basic components / Main components
1. ** Basic analysis** ( `run_Analis.py') - Manual charting / Manual charting
2. ** Interactive system** (`interactive/') - ML trade strategies / ML trading strategies
3. **Saaas platform** (`src/saas/') - Cloud tableform / Cloud tableform
4. **Pocket Hedge fund** (`src/pocket_hedge_fund/`) - Hedge fund / Hedge fund
5. **mobile application** (`src/mobile_app/`) - React Native application / React Native app
6. **Admin panel** (`src/admin_panel/') - Vue.js admin / Vue.js admin penel
7. **Monitoring** (`src/Monitoring/') - Monitoring system

### Test / Testing
- ** Multiple test** / Multihreaded test
- **Automatic environmental definition**/Automatic environmental release
- ** Code cover**/ Code control
- **Specialized tests** / Specialized tests

### Deploy/deployment
- ** Local deployment**/ Local release
- **Docker containers**
- **Apple Silicon fixed containers** / Apple Silicon native containers
- **Kubernetes clusters** / Kubernetes clusters
- ** Production deployment**/ Production release

## ♪ Useful team / Useful Commands

### Launch / Launch
```bash
# Basic analysis / Main Analysis
uv run run_Analysis.py demo --rule PHLD

# Interactive system / Interactive system
uv run python interactive/neozork.py

# SaaS platform / SaaS platform
uv run python run_saas.py

# Pocket Hedge fund
uv run python run_pocket_hedge_fund.py
```

### Test / Testing
```bash
# All tests / all tests
uv run pytest tests -n auto

# Safe mode / Safe mode
./scripts/run_tests_safe.sh

# with coverage / With coverage
uv run pytest tests/ --cov=src -n auto
```

### Docker / Docker
```bash
# Launch services / Launch services
docker-compose up -d

# Stop / Stop
docker-compose down

# Tests in Docker / tests in Docker
docker-compose exec neozork-hld uv run pytest tests/ -n auto
```

## Support / Support

### Troubleshooting / Troubleshooting
- [Troubleshooting] (Troubleshooting.md) - Common Issues and Decisions
- [FAQ](faq.md) - Frequently Asked Questions

### Additional resources / Additional Resources
- [Project Structure] (project-Structure.md) - Detailed Project Structure
- [Main documentation](../index.md) - main page documentation

---

** Version / Version**: 1.0.
** Last update / Last Update**: $(data)
**Author**: NeoZork Development Team
