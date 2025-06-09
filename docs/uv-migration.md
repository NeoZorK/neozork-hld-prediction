# Миграция с pip на uv

## Что такое uv?

uv — это быстрый пакетный менеджер для Python, написанный на Rust. Он совместим с pip, но предлагает:
- Значительное ускорение установки пакетов
- Улучшенную стратегию разрешения зависимостей
- Лучшую работу с кешем

## Установка uv

```bash
# Установка с помощью официального скрипта
curl -LsSf https://astral.sh/uv/install.sh | sh

# Или с помощью pip
pip install uv
```

## Основные команды

### Создание виртуального окружения
```bash
uv venv
source .venv/bin/activate  # для macOS/Linux
```

### Установка зависимостей
```bash
# Установка основных зависимостей
uv pip install -e .

# Установка с дополнительными группами зависимостей
uv pip install -e ".[dev,jupyter]"
```

### Управление зависимостями
```bash
# Добавление новой зависимости
uv pip install package_name

# Обновление lock-файла
uv pip compile pyproject.toml -o requirements-lock.txt
```

## Сравнение с pip

| Команда pip | Эквивалент в uv |
|-------------|-----------------|
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` |
| `pip install package` | `uv pip install package` |
| `pip freeze > requirements.txt` | `uv pip freeze > requirements.txt` |
| `pip install -e .` | `uv pip install -e .` |

## Примечания по миграции

1. uv использует тот же формат файлов зависимостей, что и pip, поэтому существующие файлы requirements.txt будут работать.
2. Для современных проектов рекомендуется использовать pyproject.toml.
3. Для воспроизводимых установок используйте lock-файлы: `uv pip compile pyproject.toml -o requirements-lock.txt`
