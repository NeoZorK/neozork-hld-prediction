#!/bin/bash
# Скрипт для обновления зависимостей с помощью uv

# Проверка, установлен ли uv
if ! command -v uv &> /dev/null; then
    echo "uv не установлен. Запускаем скрипт установки..."
    ./scripts/setup_uv.sh
    if [ $? -ne 0 ]; then
        echo "Не удалось установить uv. Пожалуйста, установите его вручную."
        exit 1
    fi
fi

# Функция вывода с цветом
info() {
    echo -e "\033[0;34m[INFO]\033[0m $1"
}

success() {
    echo -e "\033[0;32m[SUCCESS]\033[0m $1"
}

warn() {
    echo -e "\033[0;33m[WARNING]\033[0m $1"
}

error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1"
}

# Активация виртуального окружения
if [ -d ".venv" ]; then
    info "Активация виртуального окружения..."
    source .venv/bin/activate
else
    info "Создание виртуального окружения..."
    uv venv
    source .venv/bin/activate
fi

# Обновление зависимостей
info "Обновление зависимостей с помощью uv..."
uv pip install --upgrade -r requirements.txt

if [ $? -eq 0 ]; then
    success "Зависимости успешно обновлены!"

    # Генерация lock-файла
    info "Генерация lock-файла для фиксации версий..."
    uv pip freeze > requirements-lock.txt
    success "Lock-файл сгенерирован: requirements-lock.txt"

    # Вывод списка установленных пакетов
    info "Установленные пакеты:"
    uv pip list
else
    error "Ошибка при обновлении зависимостей"
    exit 1
fi

# Проверка наличия docker-compose
if command -v docker-compose &> /dev/null || command -v docker &> /dev/null; then
    echo ""
    read -p "Пересобрать Docker-образ с обновленными зависимостями? (y/n): " rebuild
    if [[ $rebuild == "y" || $rebuild == "Y" ]]; then
        info "Пересборка Docker-образа..."
        if command -v docker-compose &> /dev/null; then
            docker-compose build
        else
            docker compose build
        fi

        if [ $? -eq 0 ]; then
            success "Docker-образ успешно пересобран!"
        else
            error "Ошибка при пересборке Docker-образа"
        fi
    else
        warn "Пропуск пересборки Docker-образа"
    fi
fi

echo ""
success "Процесс обновления зависимостей завершен!"
