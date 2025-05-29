#!/usr/bin/env python3
# mcp_test_client.py - тестовый клиент для MCP сервера

import asyncio
import json
import sys
import traceback

async def test_mcp_connection():
    try:
        # Подключаемся к серверу
        host, port = "127.0.0.1", 8765
        print(f"Подключение к MCP серверу {host}:{port}...")

        reader, writer = await asyncio.open_connection(host, port)
        print(f"Соединение установлено")

        # Отправляем запрос инициализации
        init_request = {
            "type": "init",
            "options": {
                "client": "mcp_test_client",
                "version": "1.0.0"
            }
        }

        await send_message(writer, init_request)
        response = await receive_message(reader)
        print(f"Ответ на init: {response}")

        # Отправляем запрос на проверку файла
        check_file_request = {
            "type": "check_file",
            "path": "mcp_server.py"
        }

        await send_message(writer, check_file_request)
        response = await receive_message(reader)
        print(f"Ответ на check_file: {response}")

        # Отправляем запрос на чтение файла
        read_file_request = {
            "type": "read_file",
            "path": "mcp_server.py"
        }

        await send_message(writer, read_file_request)
        response = await receive_message(reader)

        # Корректный вывод длинного ответа
        response_str = str(response)
        if len(response_str) > 100:
            print(f"Ответ на read_file: {response_str[:100]}...")
        else:
            print(f"Ответ на read_file: {response}")

        # Проверка наличия ключевых полей в ответе
        if isinstance(response, dict):
            if "content" in response:
                print("Файл успешно прочитан!")
            elif "error" in response:
                print(f"Ошибка при чтении файла: {response['error']}")
            else:
                print(f"Неожиданный формат ответа: {response.keys()}")
        else:
            print(f"Ответ не является словарем, тип: {type(response)}")

        # Закрываем соединение
        writer.close()
        await writer.wait_closed()
        print("Соединение закрыто")

    except Exception as e:
        print(f"Ошибка при тестировании MCP соединения: {e}")
        print(traceback.format_exc())
        return False

    return True

async def send_message(writer, message):
    """Отправляет сообщение серверу в формате MCP протокола"""
    message_json = json.dumps(message)
    message_bytes = message_json.encode('utf-8')
    length_bytes = len(message_bytes).to_bytes(4, byteorder='big')

    print(f"Отправка сообщения ({len(message_bytes)} байт): {message_json[:100]}..." if len(message_json) > 100 else f"Отправка сообщения ({len(message_bytes)} байт): {message_json}")

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
    print("MCP Test Client")
    result = asyncio.run(test_mcp_connection())
    if result:
        print("Тест успешно завершен")
        sys.exit(0)
    else:
        print("Тест завершился с ошибкой")
        sys.exit(1)
