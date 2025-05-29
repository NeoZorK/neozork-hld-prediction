#!/usr/bin/env python3
# copilot_emulator.py - эмулятор GitHub Copilot MCP клиента

import asyncio
import json
import sys
import traceback

async def test_copilot_behavior():
    try:
        print("Эмулятор клиента GitHub Copilot MCP")

        # Проверяем каждый сервер из конфигурации
        servers = [
            {"name": "copilot-mcp-server", "host": "127.0.0.1", "port": 9999},
            {"name": "mcp_server", "host": "127.0.0.1", "port": 8765},
            {"name": "mcp_server_alt", "host": "127.0.0.1", "port": 5000}
        ]

        for server in servers:
            print(f"\n=== Тестирование сервера {server['name']} ({server['host']}:{server['port']}) ===")

            try:
                # Подключаемся к серверу
                reader, writer = await asyncio.open_connection(server['host'], server['port'])
                print(f"Соединение установлено с {server['name']}")

                # Отправляем запрос инициализации в стиле GitHub Copilot
                init_request = {
                    "type": "init",
                    "options": {
                        "client": "github.copilot",
                        "version": "1.0.0",
                        "capabilities": {
                            "file_access": True
                        }
                    }
                }

                await send_message(writer, init_request)
                response = await receive_message(reader)
                print(f"Ответ на init: {response}")

                # Важно: отправляем запрос чтения файла с undefined для file
                # Точно эмулируем проблемный запрос GitHub Copilot
                problem_request = {
                    "type": "read_file",
                    "path": "README.md",
                    "file": "undefined"  # Вот это ключевая проблема!
                }

                await send_message(writer, problem_request)
                response = await receive_message(reader)
                print(f"Ответ на проблемный запрос: {str(response)[:100]}..." if len(str(response)) > 100 else f"Ответ на проблемный запрос: {response}")

                # Закрываем соединение
                writer.close()
                await writer.wait_closed()
                print(f"Соединение с {server['name']} закрыто")

            except Exception as e:
                print(f"Ошибка при тестировании {server['name']}: {e}")
                print(traceback.format_exc())

    except Exception as e:
        print(f"Общая ошибка: {e}")
        print(traceback.format_exc())
        return False

    return True

async def send_message(writer, message):
    """Отправляет сообщение серверу в формате MCP протокола"""
    message_json = json.dumps(message)
    message_bytes = message_json.encode('utf-8')
    length_bytes = len(message_bytes).to_bytes(4, byteorder='big')

    print(f"Отправка: {message_json[:100]}..." if len(message_json) > 100 else f"Отправка: {message_json}")

    writer.write(length_bytes)
    writer.write(message_bytes)
    await writer.drain()

async def receive_message(reader):
    """Получает сообщение от сервера в формате MCP протокола"""
    length_bytes = await reader.read(4)
    if not length_bytes:
        raise ConnectionError("Соединение закрыто сервером")

    message_length = int.from_bytes(length_bytes, byteorder='big')
    print(f"Получено сообщение длиной {message_length} байт")

    message_bytes = await reader.read(message_length)
    if not message_bytes:
        raise ConnectionError("Получено пустое сообщение")

    message_str = message_bytes.decode('utf-8')
    return json.loads(message_str)

if __name__ == "__main__":
    print("Запуск эмулятора GitHub Copilot MCP клиента")
    result = asyncio.run(test_copilot_behavior())
    if result:
        print("\nТест успешно завершен")
        sys.exit(0)
    else:
        print("\nТест завершился с ошибкой")
        sys.exit(1)
