# Script Examples

Примеры использования утилитарных и отладочных скриптов.

## 🛠️ Утилитарные скрипты

### Инициализация проекта
```bash
# Инициализация директорий проекта
bash scripts/init_dirs.sh

# Проверка структуры проекта
ls -la data/
ls -la logs/
ls -la results/
```

### Исправление импортов
```bash
# Автоматическое исправление импортов
python scripts/fix_imports.py

# Исправление с подробным выводом
python scripts/fix_imports.py --verbose

# Исправление конкретного файла
python scripts/fix_imports.py --file src/calculation/indicators/rsi_ind.py
```

### Анализ зависимостей
```bash
# Анализ requirements.txt
python scripts/analyze_requirements.py

# Анализ с подробным отчетом
python scripts/analyze_requirements.py --verbose

# Анализ с экспортом в файл
python scripts/analyze_requirements.py --output requirements_analysis.txt
```

### Создание тестовых данных
```bash
# Создание тестового parquet файла
python scripts/create_test_parquet.py

# Создание с конкретными параметрами
python scripts/create_test_parquet.py --rows 1000 --symbol TEST

# Создание с экспортом в CSV
python scripts/create_test_parquet.py --export-csv
```

### Воссоздание CSV из parquet
```bash
# Воссоздание CSV из parquet файла
python scripts/recreate_csv.py

# Воссоздание конкретного файла
python scripts/recreate_csv.py --input data/test.parquet --output data/test.csv

# Воссоздание с фильтрацией
python scripts/recreate_csv.py --filter "2024-01-01"
```

## 🔍 Отладочные скрипты

### Отладка Binance соединения
```bash
# Проверка соединения с Binance
python scripts/debug_scripts/debug_binance_connection.py

# Проверка с конкретным символом
python scripts/debug_scripts/debug_binance_connection.py --symbol BTCUSDT

# Проверка с историческими данными
python scripts/debug_scripts/debug_binance_connection.py --historical --start 2024-01-01
```

### Проверка parquet файлов
```bash
# Проверка parquet файлов
python scripts/debug_scripts/debug_check_parquet.py

# Проверка конкретного файла
python scripts/debug_scripts/debug_check_parquet.py --file data/test.parquet

# Проверка с детальным анализом
python scripts/debug_scripts/debug_check_parquet.py --verbose
```

### Отладка обработки данных
```bash
# Отладка обработки данных
python scripts/debug_scripts/debug_data_processing.py

# Отладка с конкретным файлом
python scripts/debug_scripts/debug_data_processing.py --input data/test.csv

# Отладка с экспортом результатов
python scripts/debug_scripts/debug_data_processing.py --export-results
```

### Отладка построения графиков
```bash
# Отладка построения графиков
python scripts/debug_scripts/debug_plotting.py

# Отладка конкретного бэкенда
python scripts/debug_scripts/debug_plotting.py --backend plotly

# Отладка с тестовыми данными
python scripts/debug_scripts/debug_plotting.py --test-data
```

### Отладка индикаторов
```bash
# Отладка индикаторов
python scripts/debug_scripts/debug_indicators.py

# Отладка конкретного индикатора
python scripts/debug_scripts/debug_indicators.py --indicator RSI

# Отладка с тестовыми данными
python scripts/debug_scripts/debug_indicators.py --test-data
```

### Отладка CLI
```bash
# Отладка CLI
python scripts/debug_scripts/debug_cli.py

# Отладка конкретной команды
python scripts/debug_scripts/debug_cli.py --command "demo --rule RSI"

# Отладка с подробным выводом
python scripts/debug_scripts/debug_cli.py --verbose
```

### Отладка MCP серверов
```bash
# Отладка MCP серверов
python scripts/debug_scripts/debug_mcp_servers.py

# Отладка конкретного сервера
python scripts/debug_scripts/debug_mcp_servers.py --server pycharm_copilot

# Отладка с проверкой соединений
python scripts/debug_scripts/debug_mcp_servers.py --check-connections
```

## 🔧 Автоматизация

### Автозапуск MCP серверов
```bash
# Запуск автозапуска
python scripts/auto_start_mcp.py

# Запуск с конфигурацией
python scripts/auto_start_mcp.py --config mcp_auto_config.json

# Запуск в режиме отладки
python scripts/auto_start_mcp.py --debug

# Показать статус
python scripts/auto_start_mcp.py --status

# Остановить серверы
python scripts/auto_start_mcp.py --stop
```

### Запуск Cursor MCP
```bash
# Запуск Cursor MCP
python scripts/run_cursor_mcp.py

# Запуск с тестированием
python scripts/run_cursor_mcp.py --test

# Запуск с отчетом
python scripts/run_cursor_mcp.py --test --report

# Запуск с бенчмаркингом
python scripts/run_cursor_mcp.py --test --benchmark
```

## 📊 EDA и анализ

### EDA скрипт
```bash
# Запуск EDA анализа
bash eda

# EDA с помощью
bash eda -h

# EDA с конкретными параметрами
bash eda --verbose --export-results
```

### Автоматический анализ
```bash
# Автоматический анализ с разными бэкендами
python run_analysis.py demo -d fastest
python run_analysis.py demo -d plotly
python run_analysis.py demo -d seaborn
python run_analysis.py demo -d term
```

## 🐳 Docker интеграция

### Запуск скриптов в Docker
```bash
# Запуск утилитарных скриптов в Docker
docker compose run --rm neozork-hld python scripts/fix_imports.py

# Запуск отладочных скриптов в Docker
docker compose run --rm neozork-hld python scripts/debug_scripts/debug_binance_connection.py

# Запуск MCP серверов в Docker
docker compose run --rm neozork-hld python scripts/auto_start_mcp.py
```

### EDA в Docker
```bash
# Запуск EDA в Docker
docker compose run --rm neozork-hld bash eda

# EDA с UV
uv run ./eda
```

## 🔄 Рабочие процессы

### Полная инициализация проекта
```bash
# 1. Инициализация директорий
bash scripts/init_dirs.sh

# 2. Исправление импортов
python scripts/fix_imports.py

# 3. Анализ зависимостей
python scripts/analyze_requirements.py

# 4. Создание тестовых данных
python scripts/create_test_parquet.py

# 5. Запуск MCP серверов
python scripts/auto_start_mcp.py
```

### Отладка проблем
```bash
# 1. Проверка данных
python scripts/debug_scripts/debug_check_parquet.py

# 2. Проверка соединений
python scripts/debug_scripts/debug_binance_connection.py

# 3. Проверка индикаторов
python scripts/debug_scripts/debug_indicators.py

# 4. Проверка CLI
python scripts/debug_scripts/debug_cli.py

# 5. Проверка MCP серверов
python scripts/debug_scripts/debug_mcp_servers.py
```

### Подготовка к разработке
```bash
# 1. Исправление импортов
python scripts/fix_imports.py

# 2. Создание тестовых данных
python scripts/create_test_parquet.py

# 3. Запуск тестов
python -m pytest tests/ -v

# 4. Анализ покрытия
python tests/zzz_analyze_test_coverage.py

# 5. Запуск MCP серверов
python scripts/auto_start_mcp.py
```

## 📈 Мониторинг и логирование

### Просмотр логов
```bash
# Просмотр логов MCP серверов
tail -f logs/mcp_server.log

# Просмотр логов приложения
tail -f logs/app.log

# Просмотр логов ошибок
tail -f logs/error.log
```

### Анализ логов
```bash
# Анализ логов
python scripts/log_analysis/analyze_logs.py

# Анализ с фильтрацией
python scripts/log_analysis/analyze_logs.py --filter "ERROR"

# Анализ с экспортом
python scripts/log_analysis/analyze_logs.py --export results/log_analysis.txt
```

## 🎯 Специализированные скрипты

### Анализ производительности
```bash
# Анализ производительности
python scripts/performance_analysis.py

# Анализ с бенчмаркингом
python scripts/performance_analysis.py --benchmark

# Анализ с профилированием
python scripts/performance_analysis.py --profile
```

### Валидация данных
```bash
# Валидация данных
python scripts/data_validation.py

# Валидация с правилами
python scripts/data_validation.py --rules strict

# Валидация с отчетом
python scripts/data_validation.py --report
```

### Очистка кэша
```bash
# Очистка кэша
python scripts/clear_cache.py

# Очистка конкретного типа кэша
python scripts/clear_cache.py --type parquet

# Очистка с подтверждением
python scripts/clear_cache.py --confirm
```

## 🔧 Настройка и конфигурация

### Настройка UV
```bash
# Настройка UV
bash uv_setup/setup_uv.sh

# Обновление зависимостей
bash uv_setup/update_deps.sh

# Проверка конфигурации
cat uv_setup/uv.toml
```

### Настройка MCP
```bash
# Создание конфигурации MCP
python scripts/create_mcp_config.py

# Проверка конфигурации MCP
python scripts/validate_mcp_config.py

# Обновление конфигурации MCP
python scripts/update_mcp_config.py
```

## 🚨 Устранение неполадок

### Общие проблемы
```bash
# Проблема с импортами
python scripts/fix_imports.py --verbose

# Проблема с данными
python scripts/debug_scripts/debug_check_parquet.py --file data/problematic.parquet

# Проблема с соединениями
python scripts/debug_scripts/debug_binance_connection.py --verbose

# Проблема с MCP серверами
python scripts/debug_scripts/debug_mcp_servers.py --check-all
```

### Проблемы с производительностью
```bash
# Анализ производительности
python scripts/performance_analysis.py --full

# Очистка кэша
python scripts/clear_cache.py --all

# Проверка ресурсов
python scripts/debug_scripts/debug_system_resources.py
```

### Проблемы с Docker
```bash
# Пересборка контейнера
docker compose build --no-cache

# Проверка логов контейнера
docker compose logs neozork-hld

# Запуск в интерактивном режиме
docker compose run --rm neozork-hld bash
```

## 💡 Советы по использованию

### Лучшие практики
```bash
# Регулярно запускайте исправление импортов
python scripts/fix_imports.py

# Проверяйте данные перед анализом
python scripts/debug_scripts/debug_check_parquet.py

# Мониторьте MCP серверы
python scripts/auto_start_mcp.py --status

# Анализируйте логи регулярно
python scripts/log_analysis/analyze_logs.py
```

### Автоматизация
```bash
# Создайте alias для часто используемых команд
alias fix-imports="python scripts/fix_imports.py"
alias debug-data="python scripts/debug_scripts/debug_check_parquet.py"
alias mcp-status="python scripts/auto_start_mcp.py --status"

# Используйте в crontab для регулярных задач
# 0 2 * * * cd /path/to/project && python scripts/clear_cache.py
```

---

📚 **Дополнительные ресурсы:**
- **[Документация по скриптам](scripts.md)** - Подробная документация
- **[Полные примеры использования](usage-examples.md)** - Комплексные примеры
- **[Быстрые примеры](quick-examples.md)** - Быстрый старт
- **[Отладочные скрипты](debug-scripts.md)** - Специализированные скрипты отладки 