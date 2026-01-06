# Frequently Asked Questions / Frequently Asked Questions

## 🚀 General questions / General questions

### Q: How to quickly Launch the system? / How to quickly Launch the system?
**A:** Use Quick start:
```bash
# installation dependencies / install dependencies
uv pip install -r requirements.txt

# Launch main Analysis / Launch main Analysis
uv run run_Analysis.py demo --rule PHLD

# Run all tests / Run all tests
uv run pytest tests -n auto
```

### Q: What components are included in the system? / What components are included in the system?
**A:** System consists of:
- ** Basic analysis** ( `run_Analis.py') - Manual graphics/Manual charting
- ** Interactive system** (`interactive/') - ML trade strategies / ML trading strategies
- **SaaaS platform** (`src/sas/') - Cloud tableform / Cloud tableform
- **Pocket Hedge fund** (`src/pocket_hedge_fund/`) - Hedge fund / Hedge fund
- **mobile application** (`src/mobile_app/`) - React Native application / React Native app
- **Admin panel** ('src/admin_panel/') - Vue.js admin / Vue.js admin penel
- **Monitoring** (`src/Monitoring/') - Monitoring system

## Q: What system requirements?
**A:** Minimum requirements:
- **Python**: 3.11+
- **Node.js**: 18+
- **Docker**: 20.10+
- **UV**: Last version / Latest version
- ** Memory/Memorial**: 4GB RAM
- ** Disk / Disk**: 10GB available space / free space

## ♪ Questions on testing / testing Quests

### Q: How do you run all the tests?
**A:** Use multi-track test:
```bash
# All tests / all tests
uv run pytest tests -n auto

# Safe mode / Safe mode
./scripts/run_tests_safe.sh

# with coverage / With coverage
uv run pytest tests/ --cov=src -n auto
```

### Q: How to run tests on a specific component?
**A:** Start tests on categories:
```bash
# Calculation tests / Calculation tests
uv run pytest tests/calculation/ -n auto

# SaaS / SaaS tests
uv run pytest tests/saas/ -n auto

# Pocket Hedge fund / Pocket Hedge fund test
uv run pytest tests/pocket_hedge_fund/ -n auto
```

### Q: What if tests do not stand?
**A:** Try Safe Mode:
```bash
# Safe mode / Safe mode
./scripts/run_tests_safe.sh

# with debugging / with debugging
uv run pytest tests/ -v -s

# Specific test / special test
uv run pytest tests/calculation/test_indicators.py::test_rsi -v
```

## ♪ Questions on Docker / Docker Quests

## Q: How is Launch the system in Docker?
**A:** Use Docker Compose:
```bash
# Launch all services / Launch all services
docker-compose up -d

# Launch with Logsting / Launch with Logging
docker-compose up

# Stop / Stop
docker-compose down
```

## Q: How to run tests in Docker?
**A:** execute team in container:
```bash
# Test in container / test in container
docker-compose exec neozork-hld uv run pytest tests/ -n auto

# Specific tests / special tests
docker-compose exec neozork-hld uv run pytest tests/calculation/ -v
```

### Q: What if Docker not Launch?
**A:** Try the bulkhead:
```bash
# Rebuild containers / Rebuild containers
docker-compose build --no-cache

# clean Docker / clean Docker
docker system prune -a

# Restart Docker / Restart Docker
sudo systemctl Restart Docker
```

## ♪ Questions on Apple Silicon / Apple Silicon Quests

### Q: How do you start a portable container?
**A:** Use scripts of a nick container:
```bash
# Interactive Launch / Interactive Launch
./scripts/native-container/native-container.sh

# Fast Launch / Quick Launch
./scripts/native-container/setup.sh && ./scripts/native-container/run.sh

# Check status / sheck status
./scripts/native-container/run.sh --status
```

### Q: How do you control a native container?
**A:** Use team control:
```bash
# Stop / Stop
./scripts/native-container/stop.sh

# OverLaunch / Restart
./scripts/native-container/force_restart.sh

# clean / cleanup
./scripts/native-container/cleanup.sh --all --force
```

## ♪ Questions on development / development regulations

### Q: How do you turn a system into a product?
**A:** Use production configuration:
```bash
# Configuring Production / Setup Production
python deploy/production_setup.py

# Launch production services / Launch production services
docker-compose -f docker-compose.prod.yml up -d
```

### Q: How to open in Kubernets?
**A:** Apply manifestos:
```bash
# Application of manifestos / Apply manifests
kubectl apply -f k8s/

# Check status / sheck status
kubectl get pods
kubectl get services
```

## ♪ Questions on setting / configuring Quesions

### Q: How do you set the variables of the environment?
**A:** Edit file .env:
```bash
# Copying an example / Copy example
cp env.example .env

# Editing / Edition
nano .env
```

### Q: How do you set up the database?
**A:** install PostgreSQL and set the variables:
```bash
# installation PostgreSQL / install PostgreSQL
sudo apt-get install postgresql postgresql-contrib

# of the database/Create database
createdb neozork_fund

# configuration User / Configure User
createUser neozork_User
```

## ♪ Questions on Monitoring ♪

## Q: How to View Logs?
**A:** Use Team View log:
```bash
# Logs application / application Logs
tail -f Logs/pocket_hedge_fund.log

# Docker Logs / Docker Logs
docker-compose Logs -f neozork-hld

# All Logs / All Logs
tail -f Logs/*.log
```

### Q: How do you check the status of the system?
**A:** Use team check:
```bash
# health check / health check
curl http://localhost:8080/health

# Prometheus metrics / Prometheus metrics
curl http://localhost:9090/metrics

# Docker status / Docker status
docker-compose ps
```

## ♪ Questions on how to fix troubles / Troubleshooting Quesions

### Q: What if Import Errors arise?
**A:** Check PYTHONPATH:
```bash
# installation PYTHONPATH / Set PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# installation check / installation check
uv pip List | grep neozork
```

### Q: What if the tests are slowly Working?
**A:** Use optimized team:
```bash
# Safe mode / Safe mode
./scripts/run_tests_safe.sh

# Limited flows / Limited outs
uv run pytest tests/ -n 2

# Specific tests / special tests
uv run pytest tests/calculation/ -v
```

### Q: How do you get help?
**A:** Use available resources:
- **documentation / Documentation**: [docs/run-and-test-guides/](.)
- **GitHub Issues**: https://github.com/Username/neozork-hld-Prediction/issues
- **Discord**: https://discord.gg/neozork
- **Telegram**: https://t.me/neozork_hld

## * Additional resources/Additional resources

- [Complete guide / Complete Manual](russian/complete-manual-ru.md)
- [Quick start / Quick start](russian/quick-start-ru.md)
- [guide on testing / testing Guide](russian/testing-guide-ru.md)
- [guide on deployment / deployment Guide](russian/deployment-guide-ru.md)
- [Troubleshooting / Troubleshooting](Troubleshooting.md)
