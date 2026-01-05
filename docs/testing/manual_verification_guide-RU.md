# Руководство по ручной проверке проекта

## Обзор

Это руководство содержит пошаговые инструкции для ручной проверки всех компонентов проекта после обновления до Python 3.14.

---

## 1. Проверка нативной среды

### 1.1 Проверка окружения

```bash
# Проверить версию Python
python3.14 --version
# Ожидается: Python 3.14.2

# Проверить uv
uv --version
# Ожидается: uv 0.9.21 или выше

# Проверить установленные зависимости
source .venv314/bin/activate  # или ваше виртуальное окружение
uv pip list | head -20
```

### 1.2 Проверка ключевых зависимостей

```bash
source .venv314/bin/activate

# Проверить основные библиотеки
python -c "import pydantic; print(f'pydantic {pydantic.__version__}')"
python -c "import fastapi; print(f'fastapi {fastapi.__version__}')"
python -c "import pyparsing; print(f'pyparsing {pyparsing.__version__}')"
python -c "import pandas, numpy, sklearn; print('ML libraries OK')"
```

**Ожидаемые версии:**
- pydantic >= 2.12.0
- fastapi >= 0.115.0
- pyparsing >= 3.3.1

### 1.3 Запуск тестов нативно

```bash
source .venv314/bin/activate

# Все тесты
uv run pytest tests -n auto -v

# По категориям
uv run pytest tests/common/ -v
uv run pytest tests/unit/ -v
uv run pytest tests/data/ -v
uv run pytest tests/calculation/ -v
uv run pytest tests/cli/ -v
uv run pytest tests/plotting/ -v
uv run pytest tests/integration/ -v
```

### 1.4 Проверка основных программ

```bash
source .venv314/bin/activate

# Основной анализ
python run_analysis.py --help
python run_analysis.py demo --rule PHLD

# Интерактивная система
python src/interactive/neozork.py --help

# MCP сервер (если доступен)
python neozork_mcp_server.py --help
```

---

## 2. Проверка Docker окружения

### 2.1 Подготовка Docker

```bash
# Остановить существующие контейнеры
docker-compose down

# Пересобрать образы
docker-compose build --no-cache

# Проверить успешность сборки
docker images | grep neozork
```

### 2.2 Запуск контейнеров

```bash
# Запустить все сервисы
docker-compose up -d

# Проверить статус
docker-compose ps

# Проверить логи
docker-compose logs --tail=50
```

### 2.3 Проверка окружения в Docker

```bash
# Проверить версию Python
docker-compose exec neozork-hld python --version
# Ожидается: Python 3.14.x

# Проверить uv
docker-compose exec neozork-hld uv --version

# Проверить зависимости
docker-compose exec neozork-hld uv pip list | head -20

# Проверить переменные окружения
docker-compose exec neozork-hld env | grep -E "(PYTHON|UV|DOCKER)"
```

### 2.4 Запуск тестов в Docker

```bash
# Последовательные тесты (рекомендуется)
docker-compose exec neozork-hld python scripts/run_sequential_tests_docker.py

# Прямой запуск всех тестов
docker-compose exec neozork-hld uv run pytest tests -c pytest-docker.ini -n auto

# Docker-специфичные тесты
docker-compose exec neozork-hld uv run pytest tests/docker/ -v
```

### 2.5 Проверка программ в Docker

```bash
# Основной анализ
docker-compose exec neozork-hld python run_analysis.py --help
docker-compose exec neozork-hld python run_analysis.py demo --rule PHLD

# Интерактивная система
docker-compose exec neozork-hld python src/interactive/neozork.py --help

# MCP сервер
docker-compose exec neozork-hld python scripts/mcp/check_mcp_status.py

# Подключение к БД
docker-compose exec neozork-hld python -c "import psycopg2; conn = psycopg2.connect('postgresql://neozork_user:neozork_password@postgres:5432/neozork_fund'); print('DB OK'); conn.close()"
```

---

## 3. Проверка Apple Container

### 3.1 Подготовка Apple Container

```bash
# Проверить доступность инструментов
container list --all

# Проверить конфигурацию
cat container.yaml | grep python
# Ожидается: python:3.14-slim
```

### 3.2 Запуск Apple Container

```bash
# Использовать интерактивный скрипт
./scripts/native-container/native-container.sh

# Или вручную
./scripts/native-container/setup.sh
./scripts/native-container/run.sh
./scripts/native-container/exec.sh --shell
```

### 3.3 Проверка окружения в Apple Container

```bash
# Внутри контейнера
python --version
# Ожидается: Python 3.14.x

uv --version
uv pip list | head -20
```

### 3.4 Запуск тестов в Apple Container

```bash
# Внутри контейнера
uv run pytest tests -n auto

# Последовательные тесты
python scripts/run_sequential_tests_docker.py

# Native-container тесты
uv run pytest tests/native-container/ -v
```

### 3.5 Проверка программ в Apple Container

```bash
# Внутри контейнера
python run_analysis.py --help
python run_analysis.py demo --rule PHLD
python src/interactive/neozork.py --help
```

---

## 4. Быстрая проверка (чеклист)

### Минимальный набор команд

```bash
# 1. Нативная среда
source .venv314/bin/activate
python --version
python -c "import pydantic, fastapi; print('OK')"
uv run pytest tests/common/ -v

# 2. Docker
docker-compose up -d
docker-compose exec neozork-hld python --version
docker-compose exec neozork-hld uv run pytest tests/common/ -v

# 3. Программы
python run_analysis.py --help
docker-compose exec neozork-hld python run_analysis.py --help
```

### Детальная проверка

```bash
# Все тесты нативно
uv run pytest tests -n auto

# Все тесты в Docker
docker-compose exec neozork-hld python scripts/run_sequential_tests_docker.py

# Все программы
python run_analysis.py demo --rule PHLD
python src/interactive/neozork.py --help
docker-compose exec neozork-hld python run_analysis.py demo --rule PHLD
```

---

## 5. Проверка производительности

### Сравнение времени выполнения

```bash
# Нативно
time uv run pytest tests/common/ -v

# В Docker
time docker-compose exec neozork-hld uv run pytest tests/common/ -v
```

### Проверка использования памяти

```bash
# Нативно
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"

# В Docker
docker stats neozork-hld-prediction-neozork-hld-1 --no-stream
```

---

## 6. Устранение проблем

### Проблема: Зависимости не устанавливаются

```bash
# Очистить кэш
uv cache clean

# Переустановить
uv pip install -r requirements.txt --upgrade --force-reinstall
```

### Проблема: Docker не собирается

```bash
# Очистить Docker
docker system prune -a

# Пересобрать
docker-compose build --no-cache --pull
```

### Проблема: Тесты не проходят

```bash
# Запустить с подробным выводом
uv run pytest tests/ -v --tb=long

# Запустить только упавшие тесты
uv run pytest tests/ --lf
```

---

## 7. Критерии успеха

✅ Python 3.14 установлен и работает  
✅ Все ключевые зависимости установлены  
✅ Тесты проходят нативно  
✅ Docker образы собираются  
✅ Тесты проходят в Docker  
✅ Все программы запускаются  
✅ Apple Container работает (если доступен)  

---

## 8. Контакты и поддержка

При возникновении проблем:
1. Проверьте логи: `docker-compose logs`
2. Проверьте отчет: `docs/testing/python-3.14-upgrade-report.md`
3. Проверьте резервную копию: `docs/testing/pre-python-3.14-dependencies-backup.txt`

