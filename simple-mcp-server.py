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
from typing import Dict, Any, Optional, List
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
        # Словарь для хранения открытых документов
        self.documents = {}
        # Идентификатор для сообщений
        self.next_id = 1

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
            # Отправляем уведомление об ошибке
            self._send_notification("window/showMessage", {
                "type": 1,  # Error
                "message": f"MCP Server Error: {str(e)}"
            })

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
                self.logger.debug(f"Received {len(data)} bytes, buffer size: {len(self.buffer)}")

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
                except Exception as e:
                    self.logger.error(f"Error handling request: {str(e)}")
                    self.logger.error(traceback.format_exc())
                    # Отправляем ошибку, если был ID запроса
                    if isinstance(request, dict) and "id" in request:
                        self._send_error(request["id"], -32603, f"Internal error: {str(e)}")

                # Сбрасываем content_length для следующего сообщения
                self.content_length = None
            else:
                # Если недостаточно данных, ждем больше
                break

    def _handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Обработка запроса от GitHub Copilot
        """
        if not request:
            return {}

        # Проверяем, является ли это уведомлением (без ID)
        if "id" not in request:
            method = request.get("method", "")
            self.logger.info(f"Received notification: {method}")
            self.logger.debug(f"Full notification: {json.dumps(request)}")

            # Обрабатываем некоторые уведомления
            if method == "textDocument/didOpen":
                params = request.get("params", {})
                text_document = params.get("textDocument", {})
                uri = text_document.get("uri", "")
                if uri:
                    self.documents[uri] = text_document.get("text", "")
                    self.logger.info(f"Document opened: {uri}")

            elif method == "textDocument/didChange":
                params = request.get("params", {})
                text_document = params.get("textDocument", {})
                uri = text_document.get("uri", "")
                changes = params.get("contentChanges", [])
                if uri and uri in self.documents and changes:
                    # Простое обновление документа (не учитывает позиции изменений)
                    self.documents[uri] = changes[-1].get("text", self.documents[uri])
                    self.logger.info(f"Document changed: {uri}")

            elif method == "textDocument/didClose":
                params = request.get("params", {})
                text_document = params.get("textDocument", {})
                uri = text_document.get("uri", "")
                if uri and uri in self.documents:
                    del self.documents[uri]
                    self.logger.info(f"Document closed: {uri}")

            # Для уведомлений не отправляем ответ
            return None

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
                            "triggerCharacters": [".", " ", "\t", "(", "[", ",", ":"]
                        },
                        "textDocumentSync": {
                            "openClose": True,
                            "change": 1,  # Full document synchronization
                            "willSave": False,
                            "willSaveWaitUntil": False,
                            "save": {
                                "includeText": False
                            }
                        },
                        "hoverProvider": True,
                        "definitionProvider": True,
                        "referencesProvider": True,
                        "documentSymbolProvider": True,
                        "workspaceSymbolProvider": True,
                        "codeActionProvider": {
                            "codeActionKinds": ["quickfix", "refactor"]
                        },
                        "executeCommandProvider": {
                            "commands": ["neozork.analyzeData"]
                        }
                    },
                    "serverInfo": {
                        "name": "NeoZorK HLD Prediction MCP Server",
                        "version": "1.0.0"
                    }
                }
            }

        # Ответ на initialized
        elif method == "initialized":
            # Отправляем уведомление о готовности
            self._send_notification("window/showMessage", {
                "type": 3,  # Info
                "message": "MCP Server is ready and connected"
            })
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }

        # Ответ на shutdown
        elif method == "shutdown":
            self.logger.info("Received shutdown request")
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }

        # Ответ на exit
        elif method == "exit":
            self.logger.info("Received exit request, shutting down...")
            # Отправляем ответ перед выходом
            response = {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }
            self._send_response(response)
            # Завершаем программу
            sys.exit(0)
            return None  # Это не выполнится, но оставляем для согласованности

        # Обработка завершения кода
        elif method == "textDocument/completion":
            params = request.get("params", {})
            context = params.get("context", {})
            trigger_kind = context.get("triggerKind", 1)

            # Готовим результат с пустым списком (в реальном приложении здесь было бы больше логики)
            items = []

            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "isIncomplete": False,
                    "items": items
                }
            }

        # Обработка наведения мыши
        elif method == "textDocument/hover":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "contents": {
                        "kind": "markdown",
                        "value": "NeoZorK HLD Prediction Project"
                    }
                }
            }

        # Обработка перехода к определению
        elif method == "textDocument/definition":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": []
            }

        # Обработка поиска ссылок
        elif method == "textDocument/references":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": []
            }

        # Обработка символов документа
        elif method == "textDocument/documentSymbol":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": []
            }

        # Обработка символов рабочего пространства
        elif method == "workspace/symbol":
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": []
            }

        # Ответ на текстовые события
        elif method.startswith("textDocument/"):
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }

        # Обработка команд
        elif method == "workspace/executeCommand":
            params = request.get("params", {})
            command = params.get("command", "")

            if command == "neozork.analyzeData":
                return {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": {
                        "status": "success",
                        "message": "Data analysis started"
                    }
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

    def _send_notification(self, method: str, params: Dict[str, Any]) -> None:
        """
        Отправка уведомления (сообщения без ID) серверу
        """
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }

        notification_str = json.dumps(notification)
        notification_bytes = notification_str.encode('utf-8')

        # Формируем полное сообщение с заголовками
        header = f"Content-Length: {len(notification_bytes)}\r\n\r\n".encode('utf-8')

        # Отправляем сообщение в stdout
        try:
            sys.stdout.buffer.write(header)
            sys.stdout.buffer.write(notification_bytes)
            sys.stdout.buffer.flush()

            self.logger.info(f"Sent notification: {method}")
            self.logger.debug(f"Full notification: {notification_str}")
        except Exception as e:
            self.logger.error(f"Error sending notification: {str(e)}")
            self.logger.error(traceback.format_exc())

    def _send_error(self, id: int, code: int, message: str) -> None:
        """
        Отправка сообщения об ошибке
        """
        error_response = {
            "jsonrpc": "2.0",
            "id": id,
            "error": {
                "code": code,
                "message": message
            }
        }

        self._send_response(error_response)


if __name__ == "__main__":
    server = SimpleMCPServer()
    server.run()
