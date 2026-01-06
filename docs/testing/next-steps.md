# Следующие шаги после обновления до Python 3.14

## Текущий статус

✅ Конфигурационные файлы обновлены  
✅ Ключевые зависимости обновлены  
✅ Основные программы запускаются  
⚠️ Некоторые пакеты требуют дополнительной настройки  

## Что нужно сделать дальше

### 1. Установить все зависимости

```bash
source .venv/bin/activate
uv pip install -r requirements.txt
```

Если возникают ошибки с конкретными пакетами, установите их отдельно:

```bash
# Проблемные пакеты (если не поддерживают Python 3.14)
uv pip install psycopg2-binary  # Может требовать системные библиотеки
```

### 2. Протестировать нативно

```bash
source .venv/bin/activate

# Базовые тесты
uv run pytest tests/common/ -v

# Все тесты
uv run pytest tests -n auto
```

### 3. Пересобрать Docker

```bash
# Очистить старые образы
docker-compose down
docker system prune -f

# Пересобрать
docker-compose build --no-cache

# Запустить
docker-compose up -d
```

### 4. Проверить в Docker

```bash
# Проверить версию Python
docker-compose exec neozork-hld python --version

# Запустить тесты
docker-compose exec neozork-hld uv run pytest tests/common/ -v
```

### 5. Проверить Apple Container

```bash
./scripts/native-container/native-container.sh
```

## Известные проблемы

1. **psycopg2-binary** - требует libpq-dev в Docker
   - Решение: Добавлено в Dockerfile

2. **ray, torch, numba** - не поддерживают Python 3.14
   - Решение: Сделаны условными в pyproject.toml

3. **datashader** - зависит от numba
   - Решение: Сделан условным

## Рекомендации

- Используйте Python 3.13 для полной совместимости
- Или дождитесь обновления пакетов для Python 3.14
- Тестируйте критичные компоненты отдельно

