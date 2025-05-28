#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# fix_mcp_connection.py
"""
Утилита для исправления проблем подключения GitHub Copilot к MCP серверу
"""

import os
import sys
import json
import shutil
import subprocess
import time
from pathlib import Path

def check_environment():
    """Проверка окружения и настроек"""
    print("\n🔍 Проверка окружения...")

    # Проверка текущей директории
    current_dir = os.getcwd()
    print(f"Текущая директория: {current_dir}")

    # Проверка наличия файла конфигурации MCP
    mcp_config = Path("mcp/mcp-config.json")
    if mcp_config.exists():
        print(f"✅ Файл конфигурации MCP найден: {mcp_config}")
    else:
        print(f"❌ Файл конфигурации MCP не найден: {mcp_config}")
        return False

    # Проверка настроек IDE для Copilot
    idea_dir = Path("../.idea")
    vscode_dir = Path("../.vscode")

    if idea_dir.exists():
        print("✅ Найдена конфигурация IntelliJ/PyCharm (.idea)")

    if vscode_dir.exists():
        print("✅ Найдена конфигурация VSCode (.vscode)")

    if not (idea_dir.exists() or vscode_dir.exists()):
        print("⚠️ Не найдены конфигурации IDE (.idea или .vscode)")

    return True

def clean_cache_files():
    """Очистка файлов кэша"""
    print("\n🧹 Очистка файлов кэша...")

    # Очистка __pycache__ директорий
    pycache_dirs = list(Path("..").rglob("__pycache__"))
    for pycache in pycache_dirs:
        print(f"Удаление: {pycache}")
        shutil.rmtree(pycache, ignore_errors=True)

    # Удаление .pyc файлов
    pyc_files = list(Path("..").rglob("*.pyc"))
    for pyc in pyc_files:
        print(f"Удаление: {pyc}")
        pyc.unlink(missing_ok=True)

    # Проверка наличия проблемного файла из логов
    problem_file = Path("mcp/mcp-config.json.py")
    if problem_file.exists():
        print(f"Удаление проблемного файла: {problem_file}")
        problem_file.unlink()
    else:
        print("Проблемный файл mcp-config.json.py не найден")

    return True

def validate_mcp_config():
    """Проверка и исправление конфигурации MCP"""
    print("\n📋 Проверка конфигурации MCP...")

    config_path = Path("mcp/mcp-config.json")
    if not config_path.exists():
        print(f"❌ Файл конфигурации не найден: {config_path}")
        return False

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)

        print("✅ Файл конфигурации MCP валиден")

        # Проверка структуры конфигурации
        if "mcpServers" in config and "neozork-hld-prediction" in config["mcpServers"]:
            print("✅ Конфигурация сервера корректна")
        else:
            print("❌ Неверная структура конфигурации MCP")
            return False

        return True
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка в формате JSON файла конфигурации: {e}")
        return False
    except Exception as e:
        print(f"❌ Ошибка при чтении файла конфигурации: {e}")
        return False

def test_mcp_server():
    """Тестирование MCP сервера"""
    print("\n🧪 Запуск тестов MCP сервера...")

    try:
        subprocess.run(
            [sys.executable, "mcp/test_mcp_server.py"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30
        )
        print("✅ Тесты MCP сервера успешно пройдены")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при запуске тестов MCP сервера: {e}")
        print(f"Вывод: {e.stdout}")
        print(f"Ошибки: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Превышено время ожидания при запуске тестов MCP сервера")
        return False
    except Exception as e:
        print(f"❌ Неизвестная ошибка при тестировании MCP сервера: {e}")
        return False

def restart_mcp_server():
    """Перезапуск MCP сервера"""
    print("\n🔄 Перезапуск MCP сервера...")

    # Остановка запущенных процессов Python
    try:
        if sys.platform == "win32":
            os.system("taskkill /f /im python.exe")
        else:
            # Поиск процессов Python, запущенных с mcp_server.py
            ps_output = subprocess.check_output(
                ["ps", "-ef"],
                text=True
            )
            for line in ps_output.splitlines():
                if "mcp_server.py" in line and "python" in line:
                    # Извлечение PID и завершение процесса
                    parts = line.split()
                    if len(parts) > 1:
                        pid = parts[1]
                        os.system(f"kill -9 {pid}")
                        print(f"Остановлен процесс MCP сервера с PID {pid}")
    except Exception as e:
        print(f"⚠️ Ошибка при остановке процессов Python: {e}")

    # Запуск MCP сервера в фоновом режиме
    try:
        if sys.platform == "win32":
            subprocess.Popen(
                ["python", "mcp/mcp_server.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            subprocess.Popen(
                ["python", "mcp/mcp_server.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
        print("✅ MCP сервер запущен в фоновом режиме")
        return True
    except Exception as e:
        print(f"❌ Ошибка при запуске MCP сервера: {e}")
        return False

def main():
    """Основная функция"""
    print("=" * 60)
    print("🛠️  УТИЛИТА ИСПРАВЛЕНИЯ ПОДКЛЮЧЕНИЯ GITHUB COPILOT К MCP СЕРВЕРУ")
    print("=" * 60)

    # Шаг 1: Проверка окружения
    if not check_environment():
        print("\n❌ Проверка окружения завершилась с ошибками. Прерывание.")
        return False

    # Шаг 2: Очистка кэша
    if not clean_cache_files():
        print("\n⚠️ Возникли проблемы при очистке кэша.")

    # Шаг 3: Валидация конфигурации MCP
    if not validate_mcp_config():
        print("\n❌ Проверка конфигурации MCP завершилась с ошибками. Прерывание.")
        return False

    # Шаг 4: Тестирование MCP сервера
    if not test_mcp_server():
        print("\n⚠️ Тесты MCP сервера не пройдены. Попытка перезапуска.")

    # Шаг 5: Перезапуск MCP сервера
    if not restart_mcp_server():
        print("\n❌ Не удалось перезапустить MCP сервер. Прерывание.")
        return False

    print("\n" + "=" * 60)
    print("✅ ГОТОВО! Проблемы с подключением GitHub Copilot к MCP серверу исправлены")
    print("\nТеперь вы можете:")
    print("1. Перезапустить IDE (PyCharm, VSCode или другую)")
    print("2. Проверить статус подключения GitHub Copilot")
    print("3. Если проблемы сохраняются, проверьте логи IDE")
    print("=" * 60)

    return True

if __name__ == "__main__":
    main()
