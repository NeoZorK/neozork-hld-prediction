# NeoZork HLD Prediction - Полное руководство по запуску и тестированию

## 🚀 Обзор системы

Ваша система NeoZork HLD Prediction включает в себя множество компонентов:

1. **Основной анализ** (`run_analysis.py`) - Ручное построение графиков и индикаторов
2. **Интерактивная система** (`src/interactive/`) - ML торговые стратегии
3. **SaaS платформа** (`src/saas/`) - Облачная платформа
4. **Pocket Hedge Fund** (`src/pocket_hedge_fund/`) - Хедж-фонд
5. **Мобильное приложение** (`src/mobile_app/`) - React Native приложение
6. **Админ панель** (`src/admin_panel/`) - Vue.js админка
7. **Мониторинг** (`src/monitoring/`) - Система мониторинга
8. **Развертывание** (`deployment/`) - Docker и K8s конфигурации

## 📋 Требования к системе

### Минимальные требования
- **Python**: 3.11+
- **Node.js**: 18+
- **Docker**: 20.10+ (опционально)
- **UV**: Последняя версия
- **Память**: 4GB RAM
- **Диск**: 10GB свободного места

### Рекомендуемые требования
- **Python**: 3.12+
- **Node.js**: 20+
- **Docker**: 24+
- **Память**: 8GB RAM
- **Диск**: 20GB свободного места

## 🔧 Установка и настройка

### 1. Клонирование репозитория
```bash
git clone https://github.com/username/neozork-hld-prediction.git
cd neozork-hld-prediction
```

### 2. Установка UV (если не установлен)
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Проверка установки
uv --version
```

### 3. Установка зависимостей Python
```bash
# Установка всех зависимостей
uv pip install -r requirements.txt

# Установка зависимостей для разработки
uv pip install -e ".[dev]"

# Проверка установки
uv pip list
```

### 4. Установка зависимостей Node.js

#### Мобильное приложение
```bash
cd src/mobile_app
npm install
cd ..
```

#### Админ панель
```bash
cd src/admin_panel
npm install
cd ../..
```

### 5. Настройка окружения
```bash
# Копирование файла окружения
cp env.example .env

# Редактирование переменных окружения
nano .env
```

## 🚀 Запуск компонентов

### Основной анализ (run_analysis.py)

#### Демо анализ
```bash
# Простой демо анализ
uv run run_analysis.py demo --rule PHLD

# Демо с различными индикаторами
uv run run_analysis.py demo --rule RSI,MACD,SMA:20,close

# Демо с различными режимами отображения
uv run run_analysis.py demo --rule PHLD -d plotly
uv run run_analysis.py demo --rule PHLD -d fastest
uv run run_analysis.py demo --rule PHLD -d mpl
```

#### Анализ с реальными данными
```bash
# Yahoo Finance данные
uv run run_analysis.py yfinance AAPL --rule RSI
uv run run_analysis.py yfinance MSFT --period 1y --rule MACD

# Binance данные
uv run run_analysis.py binance BTCUSDT --interval 1h --rule PHLD

# Polygon данные
uv run run_analysis.py polygon AAPL --interval 1 --rule SMA:20,close

# CSV данные
uv run run_analysis.py show csv mn1 --rule RSI -d fastest
```

#### Интерактивный режим
```bash
# Запуск интерактивного режима
uv run run_analysis.py interactive

# Интерактивный режим с предустановленными параметрами
uv run run_analysis.py interactive --input-file data/mn1.csv
```

### Интерактивная система

#### Запуск через Python
```bash
# Прямой запуск
uv run python src/interactive/neozork.py

# Запуск с отладкой
uv run python -u src/interactive/neozork.py
```

#### Запуск через скрипт nz
```bash
# Интерактивный режим
./nz interactive

# Демо режим
./nz demo

# Анализ данных
./nz analyze --csv-file data/mn1.csv --rule RSI
```

### SaaS платформа

#### Запуск SaaS платформы
```bash
# Запуск с настройками по умолчанию
uv run python run_saas.py

# Запуск с кастомными настройками
SAAS_HOST=0.0.0.0 SAAS_PORT=8080 uv run python run_saas.py

# Запуск в фоновом режиме
nohup uv run python run_saas.py > logs/saas.log 2>&1 &
```

#### Доступ к SaaS платформе
- **Основной интерфейс**: http://localhost:8080
- **API документация**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **Health Check**: http://localhost:8080/health

### Pocket Hedge Fund

#### Запуск хедж-фонда
```bash
# Запуск с настройками по умолчанию
uv run python run_pocket_hedge_fund.py

# Запуск с кастомными настройками
HOST=0.0.0.0 PORT=8080 DEBUG=true uv run python run_pocket_hedge_fund.py

# Запуск в фоновом режиме
nohup uv run python run_pocket_hedge_fund.py > logs/pocket_hedge_fund.log 2>&1 &
```

#### Доступ к Pocket Hedge Fund
- **Основной интерфейс**: http://localhost:8080
- **API документация**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc
- **Health Check**: http://localhost:8080/health

### Мобильное приложение

#### Запуск React Native приложения
```bash
cd src/mobile_app

# Установка зависимостей
npm install

# Запуск Metro bundler
npm start

# Запуск на iOS (требует Xcode)
npm run ios

# Запуск на Android (требует Android Studio)
npm run android

# Запуск в веб-браузере
npm run web
```

#### Доступ к мобильному приложению
- **Metro Bundler**: http://localhost:8081
- **iOS Simulator**: Автоматически открывается
- **Android Emulator**: Автоматически открывается
- **Web Browser**: http://localhost:19006

### Админ панель

#### Запуск Vue.js админки
```bash
cd src/admin_panel

# Установка зависимостей
npm install

# Запуск в режиме разработки
npm run dev

# Сборка для продакшна
npm run build

# Предварительный просмотр продакшн сборки
npm run preview
```

#### Доступ к админ панели
- **Режим разработки**: http://localhost:3000
- **Продакшн сборка**: http://localhost:4173

### Система мониторинга

#### Запуск мониторинга
```bash
# Запуск системы мониторинга
uv run python -m src.monitoring.system_monitor

# Запуск с кастомными настройками
MONITORING_PORT=9090 uv run python -m src.monitoring.system_monitor

# Запуск в фоновом режиме
nohup uv run python -m src.monitoring.system_monitor > logs/monitoring.log 2>&1 &
```

#### Доступ к мониторингу
- **Prometheus метрики**: http://localhost:9090/metrics
- **Health Check**: http://localhost:9090/health
- **Grafana Dashboard**: http://localhost:3001 (если настроен)

## 🧪 Тестирование

### Запуск всех тестов

#### Многопоточное тестирование
```bash
# Все тесты с автоматическим определением количества потоков
uv run pytest tests -n auto

# Все тесты с определенным количеством потоков
uv run pytest tests -n 4

# Все тесты с подробным выводом
uv run pytest tests -n auto -v
```

#### Безопасное тестирование
```bash
# Безопасный режим (ограниченное количество потоков)
./scripts/run_tests_safe.sh

# Безопасный режим с конкретными тестами
./scripts/run_tests_safe.sh tests/calculation/

# Безопасный режим с таймаутом
./scripts/run_tests_with_timeout.sh
```

#### Автоматическое определение окружения
```bash
# Автоматическое определение Docker/Local окружения
./scripts/run_all_tests.sh

# Запуск с логированием
./scripts/run_all_tests.sh 2>&1 | tee test_results.log
```

### Тестирование по категориям

#### Основные тесты
```bash
# Тесты расчетов
uv run pytest tests/calculation/ -n auto -v

# Тесты CLI
uv run pytest tests/cli/ -n auto -v

# Тесты данных
uv run pytest tests/data/ -n auto -v

# Тесты EDA
uv run pytest tests/eda/ -n auto -v
```

#### Тесты компонентов
```bash
# Тесты SaaS платформы
uv run pytest tests/saas/ -n auto -v

# Тесты Pocket Hedge Fund
uv run pytest tests/pocket_hedge_fund/ -n auto -v

# Тесты интерактивной системы
uv run pytest tests/interactive/ -n auto -v

# Тесты мониторинга
uv run pytest tests/monitoring/ -n auto -v
```

#### Тесты развертывания
```bash
# Тесты Docker
uv run pytest tests/docker/ -n auto -v

# Тесты нативного контейнера
uv run pytest tests/native-container/ -n auto -v

# Тесты интеграции
uv run pytest tests/integration/ -n auto -v
```

### Тестирование с покрытием

#### Базовое покрытие
```bash
# Тесты с покрытием кода
uv run pytest tests/ --cov=src -n auto

# Покрытие с HTML отчетом
uv run pytest tests/ --cov=src --cov-report=html -n auto

# Покрытие с XML отчетом
uv run pytest tests/ --cov=src --cov-report=xml -n auto
```

#### Детальное покрытие
```bash
# Покрытие с пропуском строк
uv run pytest tests/ --cov=src --cov-report=html --cov-report=term-missing -n auto

# Покрытие конкретных модулей
uv run pytest tests/ --cov=src.calculation --cov=src.cli -n auto

# Покрытие с минимальным порогом
uv run pytest tests/ --cov=src --cov-fail-under=80 -n auto
```

### Специализированное тестирование

#### Тесты производительности
```bash
# Тесты производительности
uv run pytest tests/ -m performance -n auto

# Тесты с профилированием
uv run pytest tests/ --profile -n auto
```

#### Тесты безопасности
```bash
# Тесты безопасности
uv run pytest tests/ -m security -n auto

# Тесты аутентификации
uv run pytest tests/pocket_hedge_fund/test_auth_system.py -v
```

#### Тесты API
```bash
# Тесты API endpoints
uv run pytest tests/pocket_hedge_fund/test_api_endpoints.py -v

# Тесты SaaS API
uv run pytest tests/saas/ -v
```

## 🐳 Docker и контейнеры

### Docker Compose

#### Запуск всех сервисов
```bash
# Запуск в фоновом режиме
docker-compose up -d

# Запуск с логированием
docker-compose up

# Запуск конкретных сервисов
docker-compose up neozork-hld
```

#### Управление сервисами
```bash
# Остановка сервисов
docker-compose down

# Перезапуск сервисов
docker-compose restart

# Просмотр логов
docker-compose logs -f neozork-hld

# Выполнение команд в контейнере
docker-compose exec neozork-hld bash
```

### Apple Silicon контейнеры

#### Нативный контейнер
```bash
# Интерактивный запуск
./scripts/native-container/native-container.sh

# Быстрый запуск
./scripts/native-container/setup.sh && ./scripts/native-container/run.sh

# Проверка статуса
./scripts/native-container/run.sh --status

# Выполнение команд
./scripts/native-container/exec.sh --shell
```

#### Управление нативным контейнером
```bash
# Остановка
./scripts/native-container/stop.sh

# Принудительный перезапуск
./scripts/native-container/force_restart.sh

# Очистка
./scripts/native-container/cleanup.sh --all --force

# Просмотр логов
./scripts/native-container/logs.sh
```

### Тестирование в Docker

#### Тесты в Docker контейнере
```bash
# Тесты в основном контейнере
docker-compose exec neozork-hld uv run pytest tests/ -n auto

# Тесты конкретной категории
docker-compose exec neozork-hld uv run pytest tests/calculation/ -v

# Тесты с покрытием
docker-compose exec neozork-hld uv run pytest tests/ --cov=src -n auto
```

#### Тесты нативного контейнера
```bash
# Вход в контейнер
./scripts/native-container/exec.sh --shell

# Внутри контейнера:
uv run pytest tests/ -n auto
uv run pytest tests/calculation/ -v
uv run pytest tests/ --cov=src -n auto
```

## 📊 Мониторинг и логи

### Просмотр логов

#### Основные логи
```bash
# Логи Pocket Hedge Fund
tail -f logs/pocket_hedge_fund.log

# Логи SaaS платформы
tail -f logs/saas_platform.log

# Логи мониторинга
tail -f logs/monitoring.log

# Все логи
tail -f logs/*.log
```

#### Docker логи
```bash
# Логи Docker контейнера
docker-compose logs -f neozork-hld

# Логи всех сервисов
docker-compose logs -f

# Логи с временными метками
docker-compose logs -f -t neozork-hld
```

#### Нативный контейнер логи
```bash
# Просмотр логов нативного контейнера
./scripts/native-container/logs.sh

# Анализ всех логов
./scripts/native-container/analyze_all_logs.sh
```

### Мониторинг системы

#### Запуск мониторинга
```bash
# Система мониторинга
uv run python -m src.monitoring.system_monitor

# Мониторинг с кастомными настройками
MONITORING_PORT=9090 uv run python -m src.monitoring.system_monitor
```

#### Проверка статуса
```bash
# Health check
curl http://localhost:9090/health

# Prometheus метрики
curl http://localhost:9090/metrics

# Статус сервисов
curl http://localhost:8080/health  # SaaS/Pocket Hedge Fund
```

## 🚀 Развертывание

### Продакшн развертывание

#### Настройка продакшн окружения
```bash
# Настройка продакшн конфигурации
python deploy/production_setup.py

# Проверка конфигурации
python deploy/production_setup.py --validate

# Создание продакшн окружения
python deploy/production_setup.py --create
```

#### Запуск продакшн контейнеров
```bash
# Запуск продакшн сервисов
docker-compose -f docker-compose.prod.yml up -d

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f
```

### Kubernetes развертывание

#### Применение манифестов
```bash
# Применение всех манифестов
kubectl apply -f k8s/

# Применение конкретного манифеста
kubectl apply -f k8s/neozork-apple-deployment.yaml

# Проверка статуса
kubectl get pods
kubectl get services
kubectl get deployments
```

#### Управление развертыванием
```bash
# Масштабирование
kubectl scale deployment neozork-app --replicas=3

# Обновление образа
kubectl set image deployment/neozork-app neozork-app=neozork:latest

# Откат
kubectl rollout undo deployment/neozork-app
```

## 🛠️ Полезные команды

### Очистка системы

#### Очистка кэша
```bash
# Очистка кэша UV
uv cache clean

# Очистка кэша pip
pip cache purge

# Очистка кэша npm
cd src/mobile_app && npm cache clean --force
cd src/admin_panel && npm cache clean --force
```

#### Очистка Docker
```bash
# Очистка неиспользуемых контейнеров
docker container prune

# Очистка неиспользуемых образов
docker image prune

# Полная очистка Docker
docker system prune -a

# Очистка volumes
docker volume prune
```

#### Очистка нативного контейнера
```bash
# Очистка нативного контейнера
./scripts/native-container/cleanup.sh --all --force

# Очистка только логов
./scripts/native-container/cleanup.sh --logs

# Очистка только кэша
./scripts/native-container/cleanup.sh --cache
```

### Проверка статуса

#### Проверка UV
```bash
# Проверка режима UV
python scripts/utilities/check_uv_mode.py --verbose

# Проверка установленных пакетов
uv pip list

# Проверка зависимостей
uv pip check
```

#### Проверка MCP
```bash
# Проверка статуса MCP сервера
python scripts/check_mcp_status.py

# Запуск MCP сервера
python start_mcp_server.py

# Проверка MCP конфигурации
python scripts/mcp/check_mcp_status.py
```

#### Проверка Docker
```bash
# Статус контейнеров
docker-compose ps

# Статус образов
docker images

# Статус volumes
docker volume ls

# Статус сети
docker network ls
```

### Обновление зависимостей

#### Python зависимости
```bash
# Обновление всех зависимостей
uv pip install --upgrade -r requirements.txt

# Обновление конкретного пакета
uv pip install --upgrade pandas

# Обновление зависимостей для разработки
uv pip install --upgrade -e ".[dev]"
```

#### Node.js зависимости
```bash
# Обновление мобильного приложения
cd src/mobile_app
npm update
npm audit fix
cd ..

# Обновление админ панели
cd src/admin_panel
npm update
npm audit fix
cd ..
```

## 🆘 Решение проблем

### Частые проблемы

#### Ошибки импорта
```bash
# Проверка PYTHONPATH
export PYTHONPATH="${PWD}:${PYTHONPATH}"

# Проверка установки пакетов
uv pip list | grep neozork

# Переустановка пакета
uv pip install -e .
```

#### Проблемы с UV
```bash
# Переустановка UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Очистка кэша UV
uv cache clean

# Проверка конфигурации UV
uv --version
```

#### Проблемы с Docker
```bash
# Пересборка контейнеров
docker-compose build --no-cache

# Перезапуск Docker
sudo systemctl restart docker

# Очистка Docker
docker system prune -a
```

#### Проблемы с тестами
```bash
# Запуск тестов в безопасном режиме
./scripts/run_tests_safe.sh

# Запуск тестов с отладкой
uv run pytest tests/ -v -s

# Запуск конкретного теста
uv run pytest tests/calculation/test_indicators.py::test_rsi -v
```

### Отладочные скрипты

#### Отладка данных
```bash
# Отладка Yahoo Finance
python scripts/debug/debug_yfinance.py

# Отладка Binance
python scripts/debug/debug_binance.py

# Отладка Polygon
python scripts/debug/debug_polygon.py

# Отладка CSV данных
python scripts/debug/debug_csv_reader.py
```

#### Отладка индикаторов
```bash
# Отладка RSI сигналов
python scripts/debug/debug_rsi_signals.py

# Отладка Wave индикатора
python scripts/debug/debug_wave_indicator.py

# Отладка сигналов
python scripts/debug/debug_signals_analysis.py
```

#### Отладка системы
```bash
# Отладка Docker процессов
python scripts/debug_docker_processes.py

# Отладка MCP сервера
python scripts/mcp/debug_mcp_detection.py

# Отладка терминала
python scripts/demo_terminal_chunked.py
```

### Получение помощи

#### Справка по командам
```bash
# Справка по основному скрипту
./nz --help

# Справка по анализу
uv run run_analysis.py --help

# Справка по тестам
uv run pytest --help

# Справка по Docker
docker-compose --help
```

#### Логи и диагностика
```bash
# Просмотр всех логов
find logs/ -name "*.log" -exec tail -f {} \;

# Поиск ошибок в логах
grep -r "ERROR" logs/

# Поиск предупреждений
grep -r "WARNING" logs/

# Анализ производительности
grep -r "performance" logs/
```

## 📚 Дополнительные ресурсы

### Документация
- [Документация API](docs/api/)
- [Руководства](docs/guides/)
- [Примеры](docs/examples/)
- [Архитектура](docs/architecture/)

### Полезные ссылки
- [UV документация](https://docs.astral.sh/uv/)
- [Pytest документация](https://docs.pytest.org/)
- [Docker документация](https://docs.docker.com/)
- [React Native документация](https://reactnative.dev/)
- [Vue.js документация](https://vuejs.org/)

### Сообщество
- [GitHub Issues](https://github.com/username/neozork-hld-prediction/issues)
- [Discord сервер](https://discord.gg/neozork)
- [Telegram канал](https://t.me/neozork_hld)

---

**Примечание**: Все команды должны выполняться из корневой директории проекта (`neozork-hld-prediction/`).

**Версия документации**: 1.0.0  
**Последнее обновление**: $(date)  
**Автор**: NeoZork Development Team
