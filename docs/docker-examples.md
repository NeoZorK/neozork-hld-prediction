# Docker Examples

Примеры использования Docker для развертывания и разработки проекта.

## 🐳 Быстрый старт с Docker

### Первый запуск
```bash
# Сборка и запуск контейнера
docker compose up --build

# Запуск в фоновом режиме
docker compose up -d --build

# Запуск только сервиса
docker compose up --build neozork-hld
```

### Базовые команды
```bash
# Запуск демо анализа в контейнере
docker compose run --rm neozork-hld python run_analysis.py demo

# Интерактивная сессия
docker compose run --rm neozork-hld bash

# Запуск с конкретными параметрами
docker compose run --rm neozork-hld python run_analysis.py demo --rule RSI -d plotly
```

## 🔧 Управление контейнерами

### Сборка и пересборка
```bash
# Сборка без кэша
docker compose build --no-cache

# Сборка конкретного сервиса
docker compose build neozork-hld

# Принудительная пересборка
docker compose build --force-rm --no-cache
```

### Запуск и остановка
```bash
# Запуск всех сервисов
docker compose up

# Запуск в фоновом режиме
docker compose up -d

# Остановка всех сервисов
docker compose down

# Остановка с удалением volumes
docker compose down -v
```

### Статус и логи
```bash
# Просмотр статуса
docker compose ps

# Просмотр логов
docker compose logs

# Просмотр логов конкретного сервиса
docker compose logs neozork-hld

# Просмотр логов в реальном времени
docker compose logs -f neozork-hld
```

## 📊 Анализ данных в Docker

### Демо анализ
```bash
# Базовый демо
docker compose run --rm neozork-hld python run_analysis.py demo

# Демо с конкретным индикатором
docker compose run --rm neozork-hld python run_analysis.py demo --rule RSI

# Демо с разными бэкендами
docker compose run --rm neozork-hld python run_analysis.py demo -d plotly
docker compose run --rm neozork-hld python run_analysis.py demo -d seaborn
docker compose run --rm neozork-hld python run_analysis.py demo -d term
```

### Реальные данные
```bash
# Yahoo Finance
docker compose run --rm neozork-hld python run_analysis.py yf -t AAPL --period 1mo --point 0.01 --rule RSI

# Binance
docker compose run --rm neozork-hld python run_analysis.py binance -t BTCUSDT --interval D1 --point 0.01 --rule MACD

# CSV файлы
docker compose run --rm -v $(pwd)/data:/app/data neozork-hld python run_analysis.py csv --csv-file data.csv --point 0.01 --rule EMA

# Exchange Rate API
docker compose run --rm neozork-hld python run_analysis.py exrate -t EURUSD --interval D1 --point 0.00001 --rule BB
```

### Интерактивный режим
```bash
# Запуск интерактивного режима
docker compose run --rm neozork-hld python run_analysis.py interactive

# Интерактивный режим с TTY
docker compose run --rm -it neozork-hld python run_analysis.py interactive
```

## 🧪 Тестирование в Docker

### Запуск тестов
```bash
# Все тесты
docker compose run --rm neozork-hld python -m pytest tests/

# Тесты с подробным выводом
docker compose run --rm neozork-hld python -m pytest tests/ -v

# Тесты с покрытием
docker compose run --rm neozork-hld python -m pytest tests/ --cov=src --cov-report=html
```

### Конкретные тесты
```bash
# Тест stdio режима
docker compose run --rm neozork-hld python tests/test_stdio.py

# Тест MCP серверов
docker compose run --rm neozork-hld python -m pytest tests/mcp/ -v

# Тест индикаторов
docker compose run --rm neozork-hld python -m pytest tests/calculation/indicators/ -v
```

### Анализ покрытия
```bash
# Анализ покрытия
docker compose run --rm neozork-hld python tests/zzz_analyze_test_coverage.py

# Анализ с подробным отчетом
docker compose run --rm neozork-hld python tests/zzz_analyze_test_coverage.py --verbose
```

## 🔧 MCP серверы в Docker

### Запуск MCP серверов
```bash
# Автозапуск MCP серверов
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py

# Запуск с конфигурацией
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py --config mcp_auto_config.json

# Запуск в режиме отладки
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py --debug
```

### Тестирование MCP
```bash
# Тест stdio режима
docker compose run --rm neozork-hld python tests/test_stdio.py

# Тест MCP функциональности
docker compose run --rm neozork-hld python -m pytest tests/mcp/ -v

# Тест интеграции
docker compose run --rm neozork-hld python scripts/run_cursor_mcp.py --test
```

## 🛠️ Утилитарные скрипты в Docker

### Исправление импортов
```bash
# Исправление импортов
docker compose run --rm neozork-hld python scripts/fix_imports.py

# Исправление с подробным выводом
docker compose run --rm neozork-hld python scripts/fix_imports.py --verbose
```

### Отладочные скрипты
```bash
# Отладка Binance соединения
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_binance_connection.py

# Проверка parquet файлов
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_check_parquet.py

# Отладка индикаторов
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_indicators.py
```

### Создание тестовых данных
```bash
# Создание тестового parquet файла
docker compose run --rm neozork-hld python scripts/create_test_parquet.py

# Создание с параметрами
docker compose run --rm neozork-hld python scripts/create_test_parquet.py --rows 1000 --symbol TEST
```

## 📁 Работа с данными

### Монтирование volumes
```bash
# Монтирование локальной папки data
docker compose run --rm -v $(pwd)/data:/app/data neozork-hld python run_analysis.py csv --csv-file data.csv

# Монтирование результатов
docker compose run --rm -v $(pwd)/results:/app/results neozork-hld python run_analysis.py demo --export-parquet

# Монтирование логов
docker compose run --rm -v $(pwd)/logs:/app/logs neozork-hld python run_analysis.py demo
```

### Копирование файлов
```bash
# Копирование файла в контейнер
docker cp data.csv $(docker compose ps -q neozork-hld):/app/data.csv

# Копирование файла из контейнера
docker cp $(docker compose ps -q neozork-hld):/app/results/ ./local_results/
```

### Работа с кэшем
```bash
# Очистка кэша в контейнере
docker compose run --rm neozork-hld rm -rf data/cache/*

# Принудительное обновление данных
docker compose run --rm neozork-hld python run_analysis.py yf -t AAPL --force-refresh
```

## 🔄 Рабочие процессы

### Полный пайплайн анализа
```bash
# 1. Загрузка данных
docker compose run --rm neozork-hld python run_analysis.py yf -t AAPL --period 1y --point 0.01

# 2. Анализ с индикаторами
docker compose run --rm neozork-hld python run_analysis.py show yf AAPL --rule RSI --export-parquet
docker compose run --rm neozork-hld python run_analysis.py show yf AAPL --rule MACD --export-parquet

# 3. Просмотр результатов
docker compose run --rm neozork-hld python run_analysis.py show ind parquet
```

### Разработка в контейнере
```bash
# 1. Запуск интерактивной сессии
docker compose run --rm -it neozork-hld bash

# 2. Исправление импортов
python scripts/fix_imports.py

# 3. Запуск тестов
python -m pytest tests/ -v

# 4. Анализ покрытия
python tests/zzz_analyze_test_coverage.py

# 5. Запуск MCP серверов
python scripts/auto_start_mcp.py
```

### Отладка в контейнере
```bash
# 1. Проверка данных
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_check_parquet.py

# 2. Проверка соединений
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_binance_connection.py

# 3. Проверка индикаторов
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_indicators.py

# 4. Проверка CLI
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_cli.py
```

## 🎯 Специализированные сценарии

### Продакшн развертывание
```bash
# Сборка для продакшна
docker compose -f docker-compose.prod.yml build

# Запуск в продакшне
docker compose -f docker-compose.prod.yml up -d

# Мониторинг
docker compose -f docker-compose.prod.yml logs -f
```

### Разработка с hot reload
```bash
# Запуск с монтированием исходного кода
docker compose -f docker-compose.dev.yml up

# Изменения в коде автоматически отражаются в контейнере
```

### Масштабирование
```bash
# Запуск нескольких экземпляров
docker compose up --scale neozork-hld=3

# Балансировка нагрузки
docker compose up --scale neozork-hld=3 -d
```

## 🔍 Отладка Docker

### Проблемы с контейнером
```bash
# Проверка статуса контейнера
docker compose ps

# Просмотр логов
docker compose logs neozork-hld

# Вход в контейнер для отладки
docker compose exec neozork-hld bash

# Проверка ресурсов
docker stats
```

### Проблемы с сетью
```bash
# Проверка сети
docker network ls

# Проверка соединений
docker compose exec neozork-hld ping google.com

# Проверка портов
docker compose port neozork-hld 8000
```

### Проблемы с volumes
```bash
# Проверка volumes
docker volume ls

# Проверка монтирования
docker compose exec neozork-hld ls -la /app/data

# Очистка volumes
docker compose down -v
```

## 📊 Мониторинг и метрики

### Мониторинг ресурсов
```bash
# Статистика контейнеров
docker stats

# Использование диска
docker system df

# Использование памяти
docker stats --no-stream
```

### Логирование
```bash
# Централизованное логирование
docker compose logs -f

# Логирование с фильтрацией
docker compose logs -f neozork-hld | grep ERROR

# Экспорт логов
docker compose logs neozork-hld > logs/container.log
```

## 🔧 Настройка и конфигурация

### Переменные окружения
```bash
# Запуск с переменными окружения
docker compose run --rm -e DEBUG=1 -e LOG_LEVEL=DEBUG neozork-hld python run_analysis.py demo

# Использование .env файла
docker compose --env-file .env.prod up
```

### Кастомные конфигурации
```bash
# Использование кастомного docker-compose файла
docker compose -f docker-compose.custom.yml up

# Переопределение сервисов
docker compose -f docker-compose.yml -f docker-compose.override.yml up
```

### Оптимизация образа
```bash
# Многоэтапная сборка
docker build --target production -t neozork-hld:prod .

# Оптимизация размера
docker build --no-cache --compress -t neozork-hld:optimized .
```

## 🚨 Устранение неполадок

### Общие проблемы
```bash
# Проблема: Контейнер не запускается
docker compose logs neozork-hld
docker compose down
docker compose up --build

# Проблема: Нет доступа к данным
docker compose run --rm -v $(pwd)/data:/app/data neozork-hld ls -la /app/data

# Проблема: Высокое потребление ресурсов
docker stats
docker compose restart neozork-hld
```

### Проблемы с зависимостями
```bash
# Пересборка с обновлением зависимостей
docker compose build --no-cache --pull

# Проверка зависимостей в контейнере
docker compose run --rm neozork-hld pip list

# Обновление зависимостей
docker compose run --rm neozork-hld pip install --upgrade -r requirements.txt
```

### Проблемы с сетью
```bash
# Проверка сетевых настроек
docker network inspect neozork-hld-prediction_default

# Сброс сети
docker compose down
docker network prune
docker compose up
```

## 💡 Советы по использованию

### Лучшие практики
```bash
# Используйте --rm для автоматической очистки
docker compose run --rm neozork-hld python run_analysis.py demo

# Монтируйте volumes для данных
docker compose run --rm -v $(pwd)/data:/app/data neozork-hld python run_analysis.py csv --csv-file data.csv

# Используйте .dockerignore для оптимизации
echo "data/cache/" >> .dockerignore
echo "logs/" >> .dockerignore
```

### Оптимизация производительности
```bash
# Используйте кэширование слоев
docker compose build

# Оптимизируйте размер образа
docker build --no-cache --compress .

# Используйте multi-stage builds
docker build --target production .
```

---

📚 **Дополнительные ресурсы:**
- **[Docker документация](docker.md)** - Подробная документация
- **[Полные примеры использования](usage-examples.md)** - Комплексные примеры
- **[Быстрые примеры](quick-examples.md)** - Быстрый старт
- **[MCP примеры](mcp-examples.md)** - Интеграция с AI 