#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Детальное тестирование соединения с MCP сервером для GitHub Copilot
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def check_environment():
    """Проверка окружения и зависимостей"""
    print("===== Проверка окружения =====")
    print(f"Python версия: {sys.version}")
    print(f"Текущая директория: {os.getcwd()}")
    print(f"PYTHONPATH: {sys.path}")

    # Проверка наличия необходимых пакетов
    try:
        import typing
        import dataclasses
        print("✓ Пакеты typing и dataclasses установлены")
    except ImportError as e:
        print(f"✗ Ошибка импорта: {e}")
        print("Попробуйте выполнить: pip install typing-extensions dataclasses")

def check_project_structure():
    """Проверка структуры проекта"""
    print("\n===== Проверка структуры проекта =====")
    root_dir = Path(os.getcwd())

    # Проверка наличия ключевых директорий
    for dir_name in ['mcp', 'src', 'scripts']:
        dir_path = root_dir / dir_name
        if dir_path.exists() and dir_path.is_dir():
            print(f"✓ Директория {dir_name} существует")
        else:
            print(f"✗ Директория {dir_name} не найдена")

    # Проверка наличия ключевых файлов
    mcp_server = root_dir / 'mcp' / 'mcp_server.py'
    if mcp_server.exists():
        print(f"✓ Файл mcp_server.py найден")
        # Проверка прав доступа
        if os.access(mcp_server, os.X_OK):
            print("✓ Файл mcp_server.py имеет права на выполнение")
        else:
            print("✗ Файл mcp_server.py не имеет прав на выполнение")
            print(f"  Выполните: chmod +x {mcp_server}")
    else:
        print("✗ Файл mcp_server.py не найден")

def test_mcp_connection():
    """Тестирование соединения с MCP сервером"""
    print("\n===== Тестирование соединения с MCP сервером =====")

    # Формирование тестового запроса
    test_request = {
        "method": "initialize",
        "params": {}
    }

    # Сохранение запроса во временный файл
    with open('test_request.json', 'w') as f:
        json.dump(test_request, f)

    try:
        # Установка переменных окружения
        env = os.environ.copy()
        env['PYTHONPATH'] = './src:.'
        env['PROJECT_ROOT'] = '.'

        # Запуск MCP сервера с тестовым запросом
        print("Отправка тестового запроса initialize...")
        result = subprocess.run(
            f'cat test_request.json | python3 mcp/mcp_server.py',
            shell=True,
            env=env,
            capture_output=True,
            text=True
        )

        # Очистка временного файла
        os.remove('test_request.json')

        # Анализ результата
        if result.returncode != 0:
            print(f"✗ Ошибка выполнения MCP сервера (код {result.returncode})")
            if result.stderr:
                print("Ошибка:")
                print(result.stderr)
        else:
            print("✓ MCP сервер запущен успешно")

            if result.stdout:
                try:
                    response = json.loads(result.stdout)
                    print("Ответ сервера:")
                    print(json.dumps(response, indent=2))

                    # Проверка ответа
                    if "protocolVersion" in response:
                        print(f"✓ Получен корректный ответ с protocolVersion: {response['protocolVersion']}")
                    else:
                        print("✗ Ответ не содержит обязательного поля protocolVersion")
                except json.JSONDecodeError:
                    print("✗ Ответ не является корректным JSON:")
                    print(result.stdout)
            else:
                print("✗ Пустой ответ от сервера")

    except Exception as e:
        print(f"✗ Ошибка при тестировании: {e}")

def generate_fix_recommendations():
    """Генерация рекомендаций по исправлению проблем"""
    print("\n===== Рекомендации по исправлению =====")
    print("1. Убедитесь, что все зависимости установлены:")
    print("   pip install typing-extensions dataclasses")
    print("")
    print("2. Убедитесь, что файлы имеют правильные права доступа:")
    print("   chmod +x mcp/mcp_server.py")
    print("   chmod +x scripts/start_mcp_server.sh")
    print("   chmod +x scripts/test_mcp_connection.sh")
    print("")
    print("3. Проверьте пути в MCP сервере:")
    print("   - В mcp_server.py корректно ли добавляется путь к src")
    print("   - Корректно ли задана переменная PROJECT_ROOT")
    print("")
    print("4. Перезапустите IDE после исправлений")
    print("")
    print("5. Проверьте логи PyCharm/IDEA в:")
    print("   - ~/Library/Logs/JetBrains/PyCharmXXXX.X/")
    print("   - ~/Library/Application Support/JetBrains/PyCharmXXXX.X/log/")
    print("   (где XXXX.X - версия PyCharm)")

if __name__ == "__main__":
    print("===== Детальное тестирование MCP сервера для GitHub Copilot =====")
    print("Этот скрипт поможет определить проблемы с подключением MCP сервера\n")

    check_environment()
    check_project_structure()
    test_mcp_connection()
    generate_fix_recommendations()

    print("\n===== Тестирование завершено =====")
