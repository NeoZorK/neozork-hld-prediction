# mcp_server.py
# MCP server stub for local file access

# Проверяем наличие модуля mcp
try:
    from mcp.server import Server
except ImportError:
    print("ОШИБКА: Модуль mcp не найден. Установите его с помощью pip install mcp")
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
        return {"status": "success", "message": "MCP server initialized"}

    # Handler for file read request
    def handle_read_file(self, client, path=None, file=None):
        # Поддержка обоих параметров: path и file (для совместимости с GitHub Copilot)
        actual_path = path if path is not None else file
        log_message(f"Запрос на чтение файла: {actual_path} от клиента {client['addr']}")

        if actual_path is None or not isinstance(actual_path, str):
            log_message(f"Ошибка: путь должен быть строкой, получено: {type(actual_path)}", "ERROR")
            return {"error": "Path must be a string"}

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

    async def main():
        # Создаем асинхронный сервер на localhost:8765
        host, port = "127.0.0.1", 8765

        # Используем стандартный asyncio для создания сервера
        server_coro = await asyncio.start_server(
            lambda r, w: handle_client(server, r, w),
            host, port
        )

        log_message(f"Сервер запущен на {host}:{port}")

        # Держим сервер запущенным
        async with server_coro:
            await server_coro.serve_forever()

    # Функция для обработки подключений клиентов
    async def handle_client(server, reader, writer):
        addr = writer.get_extra_info('peername')
        log_message(f"Новое подключение: {addr}")
        client = {"addr": addr, "writer": writer}

        try:
            log_connection_attempt(addr, success=True)
            server.on_connect(client)

            while True:
                try:
                    # Читаем длину сообщения (4 байта)
                    length_bytes = await reader.read(4)
                    if not length_bytes:
                        log_message(f"Соединение закрыто клиентом {addr}")
                        break

                    # Преобразуем байты в целое число
                    message_length = int.from_bytes(length_bytes, byteorder='big')
                    log_message(f"Получено сообщение длиной {message_length} байт от {addr}")

                    # Читаем сообщение указанной длины
                    message_bytes = await reader.read(message_length)
                    if not message_bytes:
                        log_message(f"Пустое сообщение от клиента {addr}", "WARN")
                        break

                    # Декодируем и парсим JSON-сообщение
                    message_str = message_bytes.decode('utf-8')
                    log_message(f"Получено сообщение от {addr}: {message_str}")

                    try:
                        message = json.loads(message_str)

                        # Обрабатываем запрос в зависимости от типа
                        response = {"status": "error", "message": "Unknown request type"}

                        if "type" in message:
                            if message["type"] == "read_file":
                                path = message.get("path")
                                file = message.get("file")
                                # Подробное логирование для отладки проблемы с "file" аргументом
                                log_message(f"Тип аргумента path: {type(path)}, значение: {path}", "DEBUG")
                                log_message(f"Тип аргумента file: {type(file)}, значение: {file}", "DEBUG")
                                if path is None and file is None:
                                    log_message(f"Ошибка: аргументы path и file отсутствуют в запросе", "ERROR")
                                    response = {"error": "Path or file argument is missing"}
                                else:
                                    response = server.handle_read_file(client, path=path, file=file)
                            elif message["type"] == "init":
                                options = message.get("options")
                                # Подробное логирование параметров инициализации
                                log_message(f"Параметры инициализации: {options}", "DEBUG")
                                response = server.handle_init(client, options)
                            elif message["type"] == "check_file":
                                path = message.get("path")
                                # Подробное логирование аргумента path
                                log_message(f"Тип аргумента path: {type(path)}, значение: {path}", "DEBUG")
                                if path is None:
                                    log_message(f"Ошибка: аргумент path отсутствует в запросе", "ERROR")
                                    response = {"error": "Path argument is missing"}
                                else:
                                    response = server.handle_check_file(client, path)
                            else:
                                log_message(f"Неизвестный тип запроса: {message['type']}", "WARN")
                        else:
                            log_message(f"Отсутствует поле 'type' в сообщении", "WARN")

                        # Сериализуем ответ
                        response_str = json.dumps(response)
                        log_message(f"Отправка ответа клиенту {addr}: {response_str}")
                        response_bytes = response_str.encode('utf-8')

                        # Отправляем длину и сам ответ
                        writer.write(len(response_bytes).to_bytes(4, byteorder='big'))
                        writer.write(response_bytes)
                        await writer.drain()
                        log_message(f"Ответ успешно отправлен клиенту {addr}")

                    except json.JSONDecodeError as e:
                        log_message(f"Ошибка декодирования JSON от клиента {addr}: {e}", "ERROR")
                        log_message(f"Исходное сообщение: {message_str}", "ERROR")
                        error_response = json.dumps({"error": "Invalid JSON format"}).encode('utf-8')
                        writer.write(len(error_response).to_bytes(4, byteorder='big'))
                        writer.write(error_response)
                        await writer.drain()
                except Exception as e:
                    log_message(f"Ошибка при обработке сообщения от клиента {addr}: {e}", "ERROR")
                    log_message(f"Трассировка: {traceback.format_exc()}", "ERROR")
                    # Отправляем сообщение об ошибке клиенту
                    try:
                        error_response = json.dumps({"error": str(e)}).encode('utf-8')
                        writer.write(len(error_response).to_bytes(4, byteorder='big'))
                        writer.write(error_response)
                        await writer.drain()
                    except:
                        log_message(f"Не удалось отправить сообщение об ошибке клиенту {addr}", "ERROR")
                    # Не прерываем соединение, продолжаем обработку следующих сообщений

        except Exception as e:
            log_message(f"Ошибка обработки клиента {addr}: {e}", "ERROR")
            log_connection_attempt(addr, success=False, error=e)
        finally:
            server.on_disconnect(client)
            writer.close()
            await writer.wait_closed()
            log_message(f"Соединение закрыто: {addr}")

    anyio.run(main, backend="asyncio")
