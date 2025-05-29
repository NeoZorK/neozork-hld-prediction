# mcp_server.py
# MCP server stub for local file access

from mcp.server import Server
import os
import sys
import asyncio
import anyio
import json

# Specify the directory to allow access
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

class FileAccessServer(Server):
    def __init__(self):
        super().__init__("mcp_server")

    def on_connect(self, client):
        print(f"Client connected: {client}")

    def on_disconnect(self, client):
        print(f"Client disconnected: {client}")

    # Handler for file read request
    def handle_read_file(self, client, path):
        if path is None or not isinstance(path, str):
            return {"error": "Path must be a string"}

        abs_path = os.path.abspath(os.path.join(WORKSPACE_DIR, path))
        if not abs_path.startswith(WORKSPACE_DIR):
            return {"error": "Access denied"}
        try:
            with open(abs_path, 'r') as f:
                content = f.read()
            return {"content": content}
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    server = FileAccessServer()
    print("MCP server started...")

    async def main():
        # Создаем асинхронный сервер на localhost:8765
        host, port = "127.0.0.1", 8765

        # Используем стандартный asyncio для создания сервера
        server_coro = await asyncio.start_server(
            lambda r, w: handle_client(server, r, w),
            host, port
        )

        print(f"Сервер запущен на {host}:{port}")

        # Держим сервер запущенным
        async with server_coro:
            await server_coro.serve_forever()

    # Функция для обработки подключений клиентов
    async def handle_client(server, reader, writer):
        addr = writer.get_extra_info('peername')
        print(f"Новое подключение: {addr}")
        client = {"addr": addr, "writer": writer}

        try:
            server.on_connect(client)

            while True:
                # Читаем длину сообщения (4 байта)
                length_bytes = await reader.read(4)
                if not length_bytes:
                    break

                # Преобразуем байты в целое число
                message_length = int.from_bytes(length_bytes, byteorder='big')

                # Читаем сообщение указанной длины
                message_bytes = await reader.read(message_length)
                if not message_bytes:
                    break

                # Декодируем и парсим JSON-сообщение
                message_str = message_bytes.decode('utf-8')
                try:
                    message = json.loads(message_str)

                    # Обрабатываем запрос в зависимости от типа
                    response = {"status": "error", "message": "Unknown request type"}

                    if "type" in message:
                        if message["type"] == "read_file":
                            path = message.get("path")
                            response = server.handle_read_file(client, path)

                    # Сериализуем ответ
                    response_str = json.dumps(response)
                    response_bytes = response_str.encode('utf-8')

                    # Отправляем длину и сам ответ
                    writer.write(len(response_bytes).to_bytes(4, byteorder='big'))
                    writer.write(response_bytes)
                    await writer.drain()

                except json.JSONDecodeError:
                    print(f"Ошибка декодирования JSON: {message_str}")
                    writer.write(b'\x00\x00\x00\x1f{"error": "Invalid JSON format"}')
                    await writer.drain()

        except Exception as e:
            print(f"Ошибка обработки клиента: {e}")
        finally:
            server.on_disconnect(client)
            writer.close()
            await writer.wait_closed()
            print(f"Соединение закрыто: {addr}")

    anyio.run(main)
