#!/bin/bash
# Скрипт для установки uv в локальную среду разработки

echo "Установка uv - быстрого пакетного менеджера Python..."

# Проверка наличия curl
if ! command -v curl &> /dev/null; then
    echo "curl не найден, пожалуйста, установите его"
    exit 1
fi

# Установка uv
curl -sSf https://astral.sh/uv/install.sh | sh

# Проверка успешности установки
if command -v uv &> /dev/null; then
    echo "uv успешно установлен!"
    echo "Для активации добавьте следующую строку в ваш ~/.bashrc или ~/.zshrc:"
    echo 'export PATH="$HOME/.cargo/bin:$PATH"'

    # Создание виртуального окружения с помощью uv, если его еще нет
    if [ ! -d ".venv" ]; then
        echo "Создание виртуального окружения с помощью uv..."
        ~/.cargo/bin/uv venv
        echo "Виртуальное окружение создано в директории .venv"
        echo "Активируйте его командой: source .venv/bin/activate"
    fi

    echo "Установка зависимостей из requirements.txt..."
    if [ -f "requirements.txt" ]; then
        if [ -d ".venv" ]; then
            source .venv/bin/activate
            ~/.cargo/bin/uv pip install -r requirements.txt
            echo "Зависимости успешно установлены в виртуальное окружение!"
        else
            echo "Ошибка: виртуальное окружение не найдено"
        fi
    else
        echo "Ошибка: файл requirements.txt не найден"
    fi
else
    echo "Ошибка: uv не удалось установить"
    exit 1
fi

echo "Готово! Теперь вы можете использовать uv вместо pip."
