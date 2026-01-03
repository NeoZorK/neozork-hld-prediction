# Project Structure / Project Structure

## 📁 Main structure / Main Structure

```
neozork-hld-Prediction/
├── src/ # Main code Python / Main Python code
│ ├── saas/ # SaaS platform / SaaS platform
│ ├── pocket_hedge_fund/ # Hedge fund / Hedge fund
│ ├── monitoring/ # Monitoring / Monitoring
│ ├── calculation/ # Расчеты / Calculations
│ ├── cli/ # CLI интерфейс / CLI interface
│ ├── data/ # Работа with data / Data handling
│ ├── plotting/ # Построение графиков / Plotting
│ └── ...
├── src/interactive/ # Интерактивная система / Interactive system
├── src/mobile_app/ # Mobile application / Mobile application
├── src/admin_panel/ # Админ панель / Admin panel
├── tests/ # Тесты / Tests
├── scripts/ # Скрипты Launchа / Launch scripts
├── docs/ # documentation / Documentation
├── data/ # Данные / Data
├── logs/ # Логи / Logs
└── deployment/ # Развертывание / Deployment
```

## 🚀 Основные скрипты Launchа / Main Launch Scripts

### Python скрипты / Python Scripts
- `run_analysis.py` - Основной анализ / Main analysis
- `run_saas.py` - SaaS platform / SaaS platform
- `run_pocket_hedge_fund.py` - Hedge fund / Hedge fund
- `start_mcp_server.py` - MCP сервер / MCP server

### Bash скрипты / Bash Scripts
- `nz` - Универсальный скрипт / Universal script
- `eda` - EDA анализ / EDA analysis
- `scripts/run_all_tests.sh` - Launch всех тестов / Run all tests
- `scripts/run_tests_safe.sh` - Безопасное тестирование / Safe testing

## 🧪 Структура тестов / Test Structure

```
tests/
├── calculation/ # Тесты расчетов / Calculation tests
├── cli/ # Тесты CLI / CLI tests
├── data/ # Тесты данных / Data tests
├── saas/ # Тесты SaaS / SaaS tests
├── pocket_hedge_fund/ # Тесты Hedge fundа / Hedge fund tests
├── interactive/ # Тесты интерактивной системы / Interactive system tests
├── monitoring/ # Тесты Monitoringа / Monitoring tests
├── docker/ # Тесты Docker / Docker tests
├── native-container/ # Тесты нативного контейнера / Native container tests
└── integration/ # Интеграционные тесты / Integration tests
```

## 📊 Компоненты системы / System Components

### Backend компоненты / Backend Components
- **SaaS Platform** (`src/saas/`) - Облачная platform / Cloud platform
- **Pocket Hedge Fund** (`src/pocket_hedge_fund/`) - Hedge fund / Hedge fund
- **Monitoring** (`src/monitoring/`) - Система Monitoringа / Monitoring system
- **Interactive System** (`src/interactive/`) - Интерактивная система / Interactive system

### Frontend компоненты / Frontend Components
- **Mobile App** (`src/mobile_app/`) - React Native application / React Native app
- **Admin Panel** (`src/admin_panel/`) - Vue.js админка / Vue.js admin panel

### Инфраструктура / Infrastructure
- **Docker** (`docker-compose.yml`) - Контейнеризация / Containerization
- **Kubernetes** (`k8s/`) - Оркестрация / Orchestration
- **Deployment** (`deployment/`) - Развертывание / Deployment

## 🔧 Конфигурационные файлы / Configuration Files

### Python configuration / Python Configuration
- `pyproject.toml` - configuration проекта / Project configuration
- `requirements.txt` - dependencies / Dependencies
- `pytest.ini` - configuration тестов / Test configuration

### Node.js configuration / Node.js Configuration
- `src/mobile_app/package.json` - Mobile application / Mobile app
- `src/admin_panel/package.json` - Админ панель / Admin panel

### Docker configuration / Docker Configuration
- `docker-compose.yml` - Основные сервисы / Main services
- `docker-compose.prod.yml` - Продакшн сервисы / Production services
- `docker-compose.apple.yml` - Apple Silicon сервисы / Apple Silicon services

## 📚 documentation / Documentation

### Run and Test Guides / Run and Test Guides
- `docs/run-and-test-guides/` - Полные руководства / Complete guides
- `docs/run-and-test-guides/russian/` - Russian Version / Russian Version
- `docs/run-and-test-guides/english/` - English Version / English Version

### Другие руководства / Other Guides
- `docs/guides/` - Пошаговые руководства / Step-by-step guides
- `docs/examples/` - examples использования / Usage examples
- `docs/reference/` - Справочная documentation / Reference documentation
