#!/usr/bin/env python3
# copilot_mcp_server.py
# Специальный MCP сервер для GitHub Copilot

import os
import asyncio
import json
import datetime
import sys
import traceback
import anyio

# Порт по умолчанию для GitHub Copilot
DEFAULT_PORT = 9999

# Рабочая директория
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

def log_message(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    print(f"{timestamp} [{level:8}] - {message}", flush=True)

class CopilotServer:
    def __init__(self, name="copilot-mcp-server"):
        self.name = name
        log_message(f"Сервер {name} создан")

    def on_connect(self, client):
        log_message(f"Клиент подключен: {client['addr']}")

    def on_disconnect(self, client):
        log_message(f"Клиент отключен: {client['addr']}")

    def handle_init(self, client, options=None):
        log_message(f"Инициализация от клиента {client['addr']}, options: {options}")
        return {
            "status": "success",
            "message": "MCP server initialized",
            "serverName": self.name,
            "serverVersion": "1.0.0",
            "capabilities": {
                "fileAccess": True,
                "checkFile": True,
                "readFile": True
            }
        }

    def handle_read_file(self, client, path=None, file=None):
        # Специальная обработка для GitHub Copilot
        if isinstance(path, str) and path.lower() == "undefined":
            path = None
        if isinstance(file, str) and file.lower() == "undefined":
            file = None

        log_message(f"Запрос на чтение файла: path={path}, file={file}")

        # Выбираем, какой параметр использовать
        if path is not None and isinstance(path, str):
            file_path = path
        elif file is not None and isinstance(file, str):
            file_path = file
        else:
            log_message(f"Ошибка: не указан путь к файлу. path={path}, file={file}", "ERROR")
            return {"error": "No valid path provided"}

        abs_path = os.path.abspath(os.path.join(WORKSPACE_DIR, file_path))
        if not abs_path.startswith(WORKSPACE_DIR):
            log_message(f"Попытка доступа за пределы рабочей директории: {abs_path}", "WARN")
            return {"error": "Access denied"}

        try:
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
            log_message(f"Файл {file_path} успешно прочитан")
            return {"content": content}
        except Exception as e:
            log_message(f"Ошибка при чтении файла {file_path}: {e}", "ERROR")
            return {"error": str(e)}

    def handle_check_file(self, client, path):
        log_message(f"Проверка файла: {path}")

        if not isinstance(path, str):
            return {"error": "Path must be a string"}

        abs_path = os.path.abspath(os.path.join(WORKSPACE_DIR, path))
        if not abs_path.startswith(WORKSPACE_DIR):
            return {"error": "Access denied"}

        exists = os.path.exists(abs_path)
        return {"exists": exists, "path": path}

async def handle_client(server, reader, writer):
    addr = writer.get_extra_info('peername')
    client = {"addr": addr, "writer": writer}

    log_message(f"Новое подключение от {addr}")
    server.on_connect(client)

    try:
        while True:
            # Читаем длину сообщения (4 байта)
            length_bytes = await reader.read(4)
            if not length_bytes:
                log_message(f"Клиент {addr} закрыл соединение")
                break

            # Преобразуем байты в целое число
            message_length = int.from_bytes(length_bytes, byteorder='big')
            log_message(f"Получено сообщение длиной {message_length} байт от {addr}")

            # Проверяем разумные пределы длины сообщения
            if message_length > 10 * 1024 * 1024:  # 10 МБ
                log_message(f"Слишком большое сообщение от {addr}: {message_length} байт", "WARN")
                error_response = json.dumps({"error": "Message too large"}).encode('utf-8')
                writer.write(len(error_response).to_bytes(4, byteorder='big'))
                writer.write(error_response)
                await writer.drain()
                continue

            # Читаем само сообщение
            try:
                message_bytes = await asyncio.wait_for(reader.read(message_length), timeout=5.0)
                if not message_bytes:
                    log_message(f"Пустое сообщение от {addr}", "WARN")
                    break

                # Декодируем сообщение
                message_str = message_bytes.decode('utf-8')
                log_message(f"Сообщение от {addr}: {message_str[:100]}..." if len(message_str) > 100 else f"Сообщение от {addr}: {message_str}")

                # Парсим JSON
                message = json.loads(message_str)

                # Обрабатываем запрос
                response = {"status": "error", "message": "Unknown request type"}

                if "type" in message:
                    req_type = message["type"]

                    if req_type == "init":
                        options = message.get("options")
                        response = server.handle_init(client, options)
                    elif req_type == "read_file":
                        path = message.get("path")
                        file = message.get("file")
                        response = server.handle_read_file(client, path, file)
                    elif req_type == "check_file":
                        path = message.get("path")
                        response = server.handle_check_file(client, path)
                    else:
                        log_message(f"Неизвестный тип запроса: {req_type}", "WARN")
                else:
                    log_message(f"Отсутствует поле 'type' в запросе", "WARN")

                # Отправляем ответ
                response_str = json.dumps(response)
                response_bytes = response_str.encode('utf-8')

                writer.write(len(response_bytes).to_bytes(4, byteorder='big'))
                writer.write(response_bytes)
                await writer.drain()
                log_message(f"Ответ отправлен клиенту {addr}")

            except asyncio.TimeoutError:
                log_message(f"Таймаут при чтении сообщения от {addr}", "WARN")
                error_response = json.dumps({"error": "Read timeout"}).encode('utf-8')
                writer.write(len(error_response).to_bytes(4, byteorder='big'))
                writer.write(error_response)
                await writer.drain()
            except json.JSONDecodeError:
                log_message(f"Ошибка декодирования JSON от {addr}", "ERROR")
                error_response = json.dumps({"error": "Invalid JSON"}).encode('utf-8')
                writer.write(len(error_response).to_bytes(4, byteorder='big'))
                writer.write(error_response)
                await writer.drain()
            except Exception as e:
                log_message(f"Ошибка при обработке сообщения от {addr}: {e}", "ERROR")
                log_message(traceback.format_exc(), "ERROR")
                try:
                    error_response = json.dumps({"error": str(e)}).encode('utf-8')
                    writer.write(len(error_response).to_bytes(4, byteorder='big'))
                    writer.write(error_response)
                    await writer.drain()
                except:
                    log_message(f"Не удалось отправить сообщение об ошибке клиенту {addr}", "ERROR")
    except Exception as e:
        log_message(f"Ошибка при обработке клиента {addr}: {e}", "ERROR")
        log_message(traceback.format_exc(), "ERROR")
    finally:
        server.on_disconnect(client)
        writer.close()
        await writer.wait_closed()

async def start_server(server, host, port):
    """Запускает сервер на указанном хосте и порту"""
    try:
        server_instance = await asyncio.start_server(
            lambda r, w: handle_client(server, r, w),
            host, port
        )
        log_message(f"Сервер запущен на {host}:{port}")
        return server_instance
    except OSError as e:
        log_message(f"Не удалось запустить сервер на {host}:{port}: {e}", "ERROR")
        return None

async def main():
    # Создаем сервер
    server = CopilotServer()

    # Порты, на которых пытаемся запустить сервер
    ports = [9999, 8765, 5000]
    host = "127.0.0.1"

    # Запускаем серверы на разных портах и сохраняем ссылки на них
    server_instances = []

    for port in ports:
        log_message(f"Запуск сервера на {host}:{port}...")
        server_instance = await start_server(server, host, port)
        if server_instance:
            server_instances.append(server_instance)

    if not server_instances:
        log_message("Не удалось запустить сервер ни на одном порту", "ERROR")
        return

    # Ожидаем завершения работы серверов
    try:
        # Выбираем первый успешно запущенный сервер и ждем его завершения
        async with server_instances[0]:
            log_message(f"Сервер работает на {len(server_instances)} портах. Нажмите Ctrl+C для завершения.")
            await server_instances[0].serve_forever()
    finally:
        # Закрываем все серверы при выходе
        for server_instance in server_instances:
            server_instance.close()
        log_message("Все серверы остановлены")

if __name__ == "__main__":
    log_message("Запуск MCP сервера для GitHub Copilot...")
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log_message("Сервер остановлен пользователем")
    except Exception as e:
        log_message(f"Ошибка при запуске сервера: {e}", "ERROR")
        log_message(traceback.format_exc(), "ERROR")
