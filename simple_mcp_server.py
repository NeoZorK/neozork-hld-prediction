#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple MCP Server for GitHub Copilot connection
This is a minimal implementation that only handles successful connection
"""

import json
import sys
import traceback
import logging
from typing import Dict, Any

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("simple_mcp")

class SimpleMCPServer:
    """
    Простой MCP сервер для успешного подключения GitHub Copilot
    """

    def __init__(self):
        self.logger = logger
        self.logger.info("Simple MCP Server initialized")

    def run(self):
        """
        Запускает MCP сервер для обработки запросов от GitHub Copilot
        """
        self.logger.info("MCP Server started and ready to process requests")

        try:
            while True:
                # Чтение сообщения
                content_length = self._read_header()
                if content_length == 0:
                    continue

                # Чтение тела сообщения
                body = self._read_body(content_length)

                # Обработка запроса
                response = self._handle_request(body)

                # Отправка ответа
                self._send_response(response)
        except Exception as e:
            self.logger.error(f"Ошибка в MCP сервере: {str(e)}")
            self.logger.error(traceback.format_exc())
            sys.exit(1)

    def _read_header(self) -> int:
        """
        Чтение заголовка сообщения
        """
        content_length = 0
        while True:
            line = sys.stdin.readline().strip()
            if not line:
                break

            if line.startswith("Content-Length:"):
                content_length = int(line.split(":", 1)[1].strip())

        return content_length

    def _read_body(self, content_length: int) -> Dict[str, Any]:
        """
        Чтение тела сообщения
        """
        if content_length == 0:
            return {}

        body = sys.stdin.read(content_length)
        return json.loads(body)

    def _handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Обработка запроса от GitHub Copilot
        """
        if not request:
            return {}

        method = request.get("method", "")
        message_id = request.get("id", 0)

        self.logger.info(f"Received request: {method} (ID: {message_id})")

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
                        "textDocumentSync": 1
                    }
                }
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

        # Стандартный ответ для любых других запросов
        return {
            "jsonrpc": "2.0",
            "id": message_id,
            "result": None
        }

    def _send_response(self, response: Dict[str, Any]) -> None:
        """
        Отправка ответа
        """
        if not response:
            return

        response_str = json.dumps(response)
        sys.stdout.write(f"Content-Length: {len(response_str)}\r\n\r\n{response_str}")
        sys.stdout.flush()

        self.logger.info(f"Sent response for ID: {response.get('id', 0)}")


if __name__ == "__main__":
    server = SimpleMCPServer()
    server.run()
