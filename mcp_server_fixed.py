#!/usr/bin/env python3
# mcp_server_fixed.py
# Улучшенная версия MCP сервера с исправлениями для проблемы с "undefined" аргументами

import os
import asyncio
import anyio
import json
import time
import datetime
import sys
import traceback

# Путь к рабочей директории
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
# Путь к файлу конфигурации
CONFIG_FILE = os.path.expanduser('~/.config/github-copilot/intellij/mcp.json')

# Функция для логирования с временной меткой
def log_message(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    print(f"{timestamp} [{level:8}] - {message}", flush=True)

# Логирование попыток соединения
def log_connection_attempt(addr, success=True, error=None):
    status = "успешна" if success else "неудачна"
    log_message(f"### СОЕДИНЕНИЕ ### Попытка соединения от {addr} {status}", "INFO" if success else "ERROR")
    if error:
        log_message(f"Причина ошибки: {error}", "ERROR")
        log_message(f"Трассировка:\n{traceback.format_exc()}", "DEBUG")

# Базовый класс сервера, заменяющий класс из модуля mcp.server
class Server:
    def __init__(self, name):
        self.name = name
        log_message(f"Создан сервер с именем: {name}")

    def on_connect(self, client):
        log_message(f"Клиент подключен: {client}")

    def on_disconnect(self, client):
        log_message(f"Клиент отключен: {client}")

# Сервер для доступа к файлам
class FileAccessServer(Server):
    def __init__(self):
        # Загружаем конфигурацию
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
                log_message(f"Конфигурация загружена из {CONFIG_FILE}")
            else:
                config = {}
                os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
                log_message(f"Файл конфигурации не найден, используем пустую конфигурацию", "WARN")
        except Exception as e:
            log_message(f"Ошибка при чтении конфигурации: {e}", "ERROR")
            config = {}

        super().__init__("mcp_server")
        self.config = config

    # Обработчик запросов инициализации
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

    # Обработчик запросов на чтение файла с явной поддержкой Copilot запросов
    def handle_read_file(self, client, path=None, file=None):
        # Защитная проверка: преобразуем undefined в None
        if path == "undefined":
            path = None
        if file == "undefined":
            file = None

        log_message(f"Запрос на чтение файла от {client['addr']}, path={path}, file={file}")

        # Специальная обработка запросов от GitHub Copilot
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

    # Обработчик запросов на проверку существования файла
    def handle_check_file(self, client, path):
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
        # Создаем асинхронный сервер на localhost:8765
        host, port = "127.0.0.1", 8765

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
                    try:
                        # Проверяем, что длина сообщения в разумных пределах
                        if message_length > 10485760:  # 10 МБ
                            log_message(f"Слишком большая длина сообщения: {message_length} байт от {addr}", "WARN")
                            error_response = json.dumps({"error": "Message too large"}).encode('utf-8')
                            writer.write(len(error_response).to_bytes(4, byteorder='big'))
                            writer.write(error_response)
                            await writer.drain()
                            continue

                        message_bytes = await asyncio.wait_for(reader.read(message_length), timeout=5.0)
                        if not message_bytes:
                            log_message(f"Пустое сообщение от клиента {addr}", "WARN")
                            break
                    except asyncio.TimeoutError:
                        log_message(f"Таймаут при чтении сообщения от клиента {addr}", "WARN")
                        error_response = json.dumps({"error": "Read timeout"}).encode('utf-8')
                        writer.write(len(error_response).to_bytes(4, byteorder='big'))
                        writer.write(error_response)
                        await writer.drain()
                        continue
                    except Exception as e:
                        log_message(f"Ошибка при чтении сообщения от клиента {addr}: {e}", "ERROR")
                        error_response = json.dumps({"error": f"Read error: {str(e)}"}).encode('utf-8')
                        writer.write(len(error_response).to_bytes(4, byteorder='big'))
                        writer.write(error_response)
                        await writer.drain()
                        continue

                    # Декодируем и парсим JSON-сообщение
                    try:
                        message_str = message_bytes.decode('utf-8')
                        log_message(f"Получено сообщение от {addr}: {message_str[:200]}..." if len(message_str) > 200 else message_str)
                    except UnicodeDecodeError:
                        log_message(f"Ошибка декодирования UTF-8 от клиента {addr}", "ERROR")
                        log_message(f"Первые 100 байт сообщения: {message_bytes[:100]}", "DEBUG")
                        error_response = json.dumps({"error": "Invalid UTF-8 encoding"}).encode('utf-8')
                        writer.write(len(error_response).to_bytes(4, byteorder='big'))
                        writer.write(error_response)
                        await writer.drain()
                        continue

                    try:
                        message = json.loads(message_str)

                        # Обрабатываем запрос в зависимости от типа
                        response = {"status": "error", "message": "Unknown request type"}

                        if "type" in message:
                            if message["type"] == "read_file":
                                path = message.get("path")
                                file = message.get("file")

                                # Обработка "undefined" значений как строк
                                if path == "undefined":
                                    path = None
                                if file == "undefined":
                                    file = None

                                # Подробное логирование для отладки проблемы с "file" аргументом
                                log_message(f"Тип аргумента path: {type(path)}, значение: {path}", "DEBUG")
                                log_message(f"Тип аргумента file: {type(file)}, значение: {file}", "DEBUG")

                                # Улучшенная обработка параметров
                                if path is None and file is None:
                                    log_message(f"Ошибка: аргументы path и file отсутствуют в запросе", "ERROR")
                                    response = {"error": "Path or file argument is missing"}
                                elif path is not None and not isinstance(path, str):
                                    log_message(f"Ошибка: аргумент path не является строкой", "ERROR")
                                    response = {"error": "Path must be a string"}
                                elif file is not None and not isinstance(file, str):
                                    log_message(f"Ошибка: аргумент file не является строкой", "ERROR")
                                    response = {"error": "File must be a string"}
                                else:
                                    # Если path отсутствует, используем file
                                    # Если file отсутствует, используем path
                                    # Если оба присутствуют, используем path
                                    actual_path = path if path is not None else file
                                    response = server.handle_read_file(client, path=actual_path, file=actual_path)
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
