# Project Structure / Project Structure

## 📁 main Structure / main Structure

```
neozork-hld-Prediction/
├── src/ # main code Python / main Python code
│ ├── saas/ # SaaS platform / SaaS platform
│ ├── pocket_hedge_fund/ # Hedge fund / Hedge fund
│ ├── Monitoring/ # Monitoring / Monitoring
│ ├── calculation/ # Calculations / Calculations
│ ├── cli/ # CLI interface / CLI interface
│ ├── data/ # Working with data / data handling
│ ├── plotting/ # Построение графиков / Plotting
│ └── ...
├── src/interactive/ # Интерактивная система / Interactive system
├── src/mobile_app/ # mobile application / mobile application
├── src/admin_panel/ # Админ панель / Admin panel
├── tests/ # Тесты / Tests
├── scripts/ # Скрипты Launchа / Launch scripts
├── docs/ # documentation / Documentation
├── data/ # data / data
├── logs/ # Логи / Logs
└── deployment/ # Развертывание / deployment
```

## 🚀 Основные скрипты Launchа / main Launch Scripts

### Python скрипты / Python Scripts
- `run_Analysis.py` - Основной анализ / main Analysis
- `run_saas.py` - SaaS platform / SaaS platform
- `run_pocket_hedge_fund.py` - Hedge fund / Hedge fund
- `start_mcp_server.py` - MCP сервер / MCP server

### Bash скрипты / Bash Scripts
- `nz` - Универсальный скрипт / Universal script
- `eda` - EDA анализ / EDA Analysis
- `scripts/run_all_tests.sh` - Run all tests / Run all tests
- `scripts/run_tests_safe.sh` - Безопасное тестирование / Safe testing

## 🧪 Structure тестов / Test Structure

```
tests/
├── calculation/ # Тесты расчетов / Calculation tests
├── cli/ # Тесты CLI / CLI tests
├── data/ # Тесты данных / data tests
├── saas/ # Тесты SaaS / SaaS tests
├── pocket_hedge_fund/ # Тесты Hedge fundа / Hedge fund tests
├── interactive/ # Тесты интерактивной системы / Interactive system tests
├── Monitoring/ # Тесты Monitoringа / Monitoring tests
├── docker/ # Тесты Docker / Docker tests
├── native-container/ # Тесты нативного контейнера / Native container tests
└── integration/ # Интеграционные тесты / integration tests
```

## 📊 components системы / system components

### Backend components / Backend components
- **SaaS platform** (`src/saas/`) - Облачная platform / Cloud platform
- **Pocket Hedge fund** (`src/pocket_hedge_fund/`) - Hedge fund / Hedge fund
- **Monitoring** (`src/Monitoring/`) - Система Monitoringа / Monitoring system
- **Interactive system** (`src/interactive/`) - Интерактивная система / Interactive system

### Frontend components / Frontend components
- **mobile App** (`src/mobile_app/`) - React Native application / React Native app
- **Admin Panel** (`src/admin_panel/`) - Vue.js админка / Vue.js admin panel

### ИнфраStructure / InfraStructure
- **Docker** (`docker-compose.yml`) - Контейнеризация / Containerization
- **Kubernetes** (`k8s/`) - Оркестрация / Orchestration
- **deployment** (`deployment/`) - Развертывание / deployment

## 🔧 Конфигурационные файлы / Configuration Files

### Python configuration / Python Configuration
- `pyproject.toml` - configuration проекта / Project configuration
- `requirements.txt` - dependencies / Dependencies
- `pytest.ini` - configuration тестов / Test configuration

### Node.js configuration / Node.js Configuration
- `src/mobile_app/package.json` - mobile application / mobile app
- `src/admin_panel/package.json` - Админ панель / Admin panel

### Docker configuration / Docker Configuration
- `docker-compose.yml` - Основные Services / main Services
- `docker-compose.prod.yml` - Продакшн Services / Production Services
- `docker-compose.apple.yml` - Apple Silicon Services / Apple Silicon Services

## 📚 documentation / Documentation

### Run and Test Guides / Run and Test Guides
- `docs/run-and-test-guides/` - Полные руководства / Complete guides
- `docs/run-and-test-guides/russian/` - Russian Version / Russian Version
- `docs/run-and-test-guides/english/` - English Version / English Version

### Другие руководства / Other Guides
- `docs/guides/` - Пошаговые руководства / Step-by-step guides
- `docs/examples/` - examples использования / Usage examples
- `docs/reference/` - Справочная documentation / Reference documentation
