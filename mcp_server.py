# mcp_server.py
# MCP server stub for local file access

# Проверяем наличие модуля mcp
try:
    from mcp.server import Server
except ImportError:
    print("ОШИБКА: Модуль мcp не найден. Установите его с помощью pip install mcp")
    import sys
    sys.exit(1)

import os
import asyncio
import anyio
import json
import time
import datetime
import sys
import traceback

# Specify the directory to allow access
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
# Path to config file
CONFIG_FILE = os.path.expanduser('~/.config/github-copilot/intellij/mcp.json')

# Функция для логирования с временной меткой
def log_message(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    print(f"{timestamp} [{level:8}] - {message}", flush=True)  # Добавлен flush=True для немедленного вывода

# Логирование попыток соединения
def log_connection_attempt(addr, success=True, error=None):
    status = "успешна" if success else "неудачна"
    log_message(f"### СОЕДИНЕНИЕ ### Попытка соединения от {addr} {status}", "INFO" if success else "ERROR")
    if error:
        log_message(f"Причина ошибки: {error}", "ERROR")
        log_message(f"Трассировка:\n{traceback.format_exc()}", "DEBUG")

class FileAccessServer(Server):
    def __init__(self):
        # Загружаем конфигурацию из файла
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                log_message(f"Конфигурация загружена из {CONFIG_FILE}")
            else:
                config = {}
                os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
                log_message(f"Файл конфигурации {CONFIG_FILE} не найден, используем пустую конфигурацию", "WARN")
        except Exception as e:
            log_message(f"Ошибка при чтении конфигурации: {e}", "ERROR")
            config = {}
        # Передаем имя сервера
        super().__init__("mcp_server")
        # Сохраняем конфигурацию для дальнейшего использования
        self.config = config

    def on_connect(self, client):
        log_message(f"Client connected: {client}")

    def on_disconnect(self, client):
        log_message(f"Client disconnected: {client}")

    # Handler for initialization request from clients
    def handle_init(self, client, options=None):
        log_message(f"Инициализация клиента: {client['addr']}, options: {options}")

        # Специальная обработка для GitHub Copilot
        if options and isinstance(options, dict):
            client_name = options.get("client", "unknown")
            log_message(f"Клиент {client_name} запрашивает инициализацию", "INFO")

            # Формируем ответ, соответствующий ожиданиям GitHub Copilot
            response = {
                "status": "success",
                "message": "MCP server initialized",
                "serverName": "mcp_server",
                "serverVersion": "1.0.0",
                "capabilities": {
                    "fileAccess": True,
                    "checkFile": True,
                    "readFile": True
                }
            }
            return response

        # Стандартный ответ для других клиентов
        return {"status": "success", "message": "MCP server initialized"}

    # Handler for file read request with explicit support for Copilot requests
    def handle_read_file(self, client, path=None, file=None):
        log_message(f"Запрос на чтение файла от {client['addr']}, path={path}, file={file}")

        # Специальная обработка запросов от GitHub Copilot
        # Копилот иногда отправляет null вместо undefined для отсутствующих параметров
        if path is None and file is None:
            log_message(f"Оба параметра path и file отсутствуют в запросе", "ERROR")
            return {"error": "Path or file argument is missing"}

        # Определяем, какой параметр использовать
        if path is not None and isinstance(path, str):
            actual_path = path
        elif file is not None and isinstance(file, str):
            actual_path = file
        else:
            # Проверяем на значения null/None
            err_msg = f"Ошибка в параметрах: path={type(path)}, file={type(file)}"
            log_message(err_msg, "ERROR")
            return {"error": err_msg}

        log_message(f"Чтение файла: {actual_path}")

        abs_path = os.path.abspath(os.path.join(WORKSPACE_DIR, actual_path))
        if not abs_path.startswith(WORKSPACE_DIR):
            log_message(f"Доступ запрещен: {abs_path}", "WARN")
            return {"error": "Access denied"}
        try:
            with open(abs_path, 'r') as f:
                content = f.read()
            log_message(f"Файл успешно прочитан: {abs_path}")
            return {"content": content}
        except Exception as e:
            log_message(f"Ошибка при чтении файла {abs_path}: {e}", "ERROR")
            return {"error": str(e)}

    # Handler for checking if a file exists
    def handle_check_file(self, client, path):
        log_message(f"Проверка существования файла: {path} от клиента {client['addr']}")

        if path is None or not isinstance(path, str):
            log_message(f"Ошибка: путь должен быть строкой, получено: {type(path)}", "ERROR")
            return {"error": "Path must be a string"}

        abs_path = os.path.abspath(os.path.join(WORKSPACE_DIR, path))
        if not abs_path.startswith(WORKSPACE_DIR):
            log_message(f"Доступ запрещен: {abs_path}", "WARN")
            return {"error": "Access denied"}

        exists = os.path.exists(abs_path)
        log_message(f"Файл {path} {'существует' if exists else 'не существует'}")
        return {"exists": exists, "path": path}

if __name__ == "__main__":
    server = FileAccessServer()
    log_message("MCP server started...")

    # Выводим информацию о конфигурации сервера
    log_message(f"Имя сервера: {server.name}")
    log_message(f"Рабочая директория: {WORKSPACE_DIR}")
    log_message(f"Конфигурация: {server.config}")

    async def main():
        # Создаем асинхронный сервер на localhost:8765 или на другом порту из переменной окружения
        host = "127.0.0.1"

        # Получаем порт из переменной окружения или используем порт по умолчанию
        port = int(os.environ.get("MCP_PORT", "8765"))

        log_message(f"Запуск сервера на {host}:{port}...")

        # Используем стандартный asyncio для создания сервера
        try:
            server_coro = await asyncio.start_server(
                lambda r, w: handle_client(server, r, w),
                host, port
            )

            log_message(f"Сервер успешно запущен на {host}:{port}")
            log_message("Ожидание подключений...")

            # Держим сервер запущенным
            async with server_coro:
                await server_coro.serve_forever()
        except Exception as e:
            log_message(f"Ошибка при запуске сервера: {e}", "ERROR")
            log_message(f"Трассировка: {traceback.format_exc()}", "ERROR")
            sys.exit(1)

