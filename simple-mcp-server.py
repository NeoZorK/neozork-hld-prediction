#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple MCP Server for GitHub Copilot connection
This is a minimal implementation that handles stdio interface for GitHub Copilot
"""

import json
import sys
import traceback
import logging
import threading
from typing import Dict, Any
import os

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Повышаем уровень логирования для отладки
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mcp_server.log"),  # Добавляем запись логов в файл
        logging.StreamHandler(sys.stderr)  # Вывод логов в stderr вместо stdout для stdio протокола
    ]
)
logger = logging.getLogger("simple_mcp")

class SimpleMCPServer:
    """
    Простой MCP сервер для успешного подключения GitHub Copilot через stdio
    """

    def __init__(self):
        self.logger = logger
        self.logger.info("Simple MCP Server initialized with stdio interface")
        # Создаем буфер для входящих данных
        self.buffer = b""
        self.content_length = None

    def run(self):
        """
        Запускает MCP сервер для обработки запросов от GitHub Copilot через stdio
        """
        try:
            self.logger.info("MCP Server started with stdio interface")

            # Основной цикл чтения из stdin и записи в stdout
            self._handle_stdio()

        except Exception as e:
            self.logger.error(f"Ошибка в MCP сервере: {str(e)}")
            self.logger.error(traceback.format_exc())

    def _handle_stdio(self):
        """
        Обрабатывает ввод/вывод через стандартные потоки
        """
        # Устанавливаем двоичный режим для stdin и stdout в Windows
        if os.name == 'nt':
            import msvcrt
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

        # Основной цикл обработки
        while True:
            # Чтение данных из stdin
            try:
                data = sys.stdin.buffer.read1(4096)
                if not data:
                    self.logger.info("End of stdin stream, exiting")
                    break

                self.buffer += data

                # Обрабатываем сообщения, пока они есть в буфере
                self._process_buffer()

            except Exception as e:
                self.logger.error(f"Error reading from stdin: {str(e)}")
                self.logger.error(traceback.format_exc())
                break

    def _process_buffer(self):
        """
        Обрабатывает буфер и извлекает сообщения
        """
        while True:
            # Если мы еще не знаем длину контента, попробуем ее найти
            if self.content_length is None:
                # Ищем двойной перенос строки, отделяющий заголовки от тела
                header_end = self.buffer.find(b"\r\n\r\n")
                if header_end == -1:
                    # Если не найден, ждем больше данных
                    break

                # Извлекаем заголовки
                headers = self.buffer[:header_end].decode('utf-8')

                # Ищем Content-Length
                for line in headers.split("\r\n"):
                    if line.lower().startswith("content-length:"):
                        self.content_length = int(line.split(":", 1)[1].strip())
                        self.logger.debug(f"Found Content-Length: {self.content_length}")
                        break

                # Удаляем заголовки из буфера
                self.buffer = self.buffer[header_end + 4:]  # 4 = len("\r\n\r\n")

            # Если у нас достаточно данных для всего сообщения
            if self.content_length is not None and len(self.buffer) >= self.content_length:
                # Извлекаем тело сообщения
                message_body = self.buffer[:self.content_length].decode('utf-8')
                self.buffer = self.buffer[self.content_length:]

                # Обрабатываем запрос
                try:
                    request = json.loads(message_body)
                    response = self._handle_request(request)

                    # Отправляем ответ
                    if response:
                        self._send_response(response)
                except json.JSONDecodeError:
                    self.logger.error(f"Failed to parse JSON: {message_body}")

                # Сбрасываем content_length для следующего сообщения
                self.content_length = None
            else:
                # Если недостаточно данных, ждем больше
                break

    def _handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка запроса от GitHub Copilot
        """
        if not request:
            return {}

        method = request.get("method", "")
        message_id = request.get("id", 0)

        self.logger.info(f"Received request: {method} (ID: {message_id})")
        self.logger.debug(f"Full request: {json.dumps(request)}")

        # Стандартный ответ на initialize
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "capabilities": {
                        "completionProvider": {
                            "triggerCharacters": [".", " ", "\t", "(", "[", ","]
                        },
                        "textDocumentSync": 1,
                        "hoverProvider": True,
                        "definitionProvider": True,
                        "referencesProvider": True,
                        "documentSymbolProvider": True,
                        "workspaceSymbolProvider": True
                    },
                    "serverInfo": {
                        "name": "NeoZorK HLD Prediction MCP Server",
                        "version": "1.0.0"
                    }
                }
            }

        # Ответ на initialized
        elif method == "initialized":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }

        # Ответ на shutdown
        elif method == "shutdown":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }

        # Ответ на exit
        elif method == "exit":
            self.logger.info("Received exit request, shutting down...")
            # Будем закрывать сервер корректно
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }

        # Обработка других методов для базового функционирования
        elif method == "textDocument/completion":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "isIncomplete": False,
                    "items": []
                }
            }

        # Ответ на текстовые события
        elif method.startswith("textDocument/"):
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }

        # Стандартный ответ для любых других запросов
        self.logger.info(f"Получен неизвестный метод: {method}")
        return {
            "jsonrpc": "2.0",
            "id": message_id,
            "result": None
        }

    def _send_response(self, response: Dict[str, Any]) -> None:
        """
        Отправка ответа через stdout
        """
        if not response:
            return

        response_str = json.dumps(response)
        response_bytes = response_str.encode('utf-8')

        # Формируем полное сообщение с заголовками
        header = f"Content-Length: {len(response_bytes)}\r\n\r\n".encode('utf-8')

        # Отправляем сообщение в stdout
        try:
            sys.stdout.buffer.write(header)
            sys.stdout.buffer.write(response_bytes)
            sys.stdout.buffer.flush()

            self.logger.info(f"Sent response for ID: {response.get('id', 0)}")
            self.logger.debug(f"Full response: {response_str}")
        except Exception as e:
            self.logger.error(f"Error sending response: {str(e)}")
            self.logger.error(traceback.format_exc())


if __name__ == "__main__":
    server = SimpleMCPServer()
    server.run()
