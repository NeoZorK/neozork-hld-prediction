# mcp_server.py
# MCP server stub for local file access

from mcp.server import Server
import os
import sys
import asyncio
import anyio
import aioconsole
import socket

# Specify the directory to allow access
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

class FileAccessServer(Server):
    def __init__(self):
        super().__init__("mcp_server")

    def on_connect(self, client):
        print(f"Client connected: {client}")

    def on_disconnect(self, client):
        print(f"Client disconnected: {client}")

    # Example handler for file read request
    def handle_read_file(self, client, path):
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

        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break

                # Обработка полученных данных
                response = "Получено: " + data.decode()
                writer.write(response.encode())
                await writer.drain()
        except Exception as e:
            print(f"Ошибка обработки клиента: {e}")
        finally:
            writer.close()
            await writer.wait_closed()
            print(f"Соединение закрыто: {addr}")

    anyio.run(main)
