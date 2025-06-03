# Переход с pip на uv

## Что такое uv?

[uv](https://github.com/astral-sh/uv) - это новый, быстрый пакетный менеджер Python, который может заменить pip. 

**Преимущества uv:**
- В 10-100 раз быстрее pip при установке пакетов
- Параллельная установка зависимостей
- Улучшенное разрешение зависимостей
- Меньший размер Docker-контейнеров
- Лучшее кэширование пакетов

## Установка uv

### Локальная установка

Для локальной установки можно использовать предоставленный скрипт:

```bash
chmod +x scripts/setup_uv.sh
./scripts/setup_uv.sh
```

Или установить вручную:

```bash
# Установка uv
curl -sSf https://astral.sh/uv/install.sh | sh

# Добавление в PATH (добавьте в ваш .bashrc или .zshrc)
export PATH="$HOME/.cargo/bin:$PATH"
```

### Проверка установки

```bash
uv --version
```

## Команды uv (замена pip)

| pip                            | uv                        | Описание                                  |
|--------------------------------|---------------------------|-------------------------------------------|
| `pip install package`          | `uv pip install package`  | Установка пакета                          |
| `pip install -r requirements.txt` | `uv pip install -r requirements.txt` | Установка из файла требований |
| `pip uninstall package`        | `uv pip uninstall package` | Удаление пакета                         |
| `pip freeze > requirements.txt`| `uv pip freeze > requirements.txt` | Сохранение текущих зависимостей   |
| `python -m venv .venv`         | `uv venv`                 | Создание виртуального окружения           |
| -                              | `uv pip compile requirements.txt` | Компиляция requirements.txt в lock-файл |

## Виртуальные окружения с uv

```bash
# Создание виртуального окружения
uv venv

# Активация (так же, как и с обычным venv)
source .venv/bin/activate
```

## Docker

В Dockerfile уже настроено использование uv для установки зависимостей.

## CI/CD

Для GitHub Actions вы можете использовать кэширование для ускорения установки зависимостей:

```yaml
- name: Install uv
  run: |
    curl -sSf https://astral.sh/uv/install.sh | sh
    echo "$HOME/.cargo/bin" >> $GITHUB_PATH

- name: Install dependencies
  run: |
    uv venv
    source .venv/bin/activate
    uv pip install -r requirements.txt
```
