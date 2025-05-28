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
import time
from typing import Dict, Any, Optional, List
import os

# Создаем директорию logs, если она не существует
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
if not os.path.exists(logs_dir):
    try:
        os.makedirs(logs_dir)
        print(f"Created logs directory: {logs_dir}")
    except Exception as e:
        print(f"Error creating logs directory: {e}")

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Повышаем уровень логирования для отладки
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(logs_dir, "mcp_server.log"), mode='a'),  # Сохраняем логи в директорию logs
        logging.StreamHandler(sys.stdout)      # Вывод логов в stdout для отображения в консоли
    ]
)
logger = logging.getLogger("simple_mcp")

# Настройка дополнительного вывода в консоль для лучшей отладки
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('🔍 CONSOLE: %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Добавляем запись в лог о запуске сервера
logger.info("========================")
logger.info("MCP Server starting up at %s", time.strftime("%Y-%m-%d %H:%M:%S"))
logger.info("Working directory: %s", os.getcwd())
logger.info("Script location: %s", os.path.abspath(__file__))
logger.info("========================")

# Добавляем цветное логирование для лучшей читаемости в консоли
class ColoredFormatter(logging.Formatter):
    """Класс для цветного форматирования логов"""
    COLORS = {
        'DEBUG': '\033[94m',  # синий
        'INFO': '\033[92m',   # зеленый
        'WARNING': '\033[93m', # желтый
        'ERROR': '\033[91m',   # красный
        'CRITICAL': '\033[91m\033[1m', # красный жирный
        'RESET': '\033[0m'    # сброс цвета
    }

    def format(self, record):
        log_message = super().format(record)
        if hasattr(record, 'levelname') and record.levelname in self.COLORS:
            return f"{self.COLORS[record.levelname]}{log_message}{self.COLORS['RESET']}"
        return log_message

# Применяем цветной форматтер для консоли, если не Windows
if os.name != 'nt':
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            if handler.stream == sys.stdout:
                # Используем более заметное форматирование для вывода в консоль
                handler.setFormatter(ColoredFormatter('📝 %(asctime)s - %(levelname)s - %(message)s'))

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
        # Счетчики для статистики
        self.connection_attempts = 0
        self.successful_connections = 0
        self.request_count = 0
        self.start_time = time.time()
        # Информация о клиентах и протоколах
        self.client_info = {}
        self.protocol_versions = set()

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

                # Выводим информацию о полученных данных в понятном формате
                data_preview = str(data)
                if len(data_preview) > 200:
                    data_preview = data_preview[:200] + "... (truncated)"

                self.logger.info(f"📥 Received {len(data)} bytes, buffer size: {len(self.buffer)}")
                self.logger.info(f"📄 Received data content: {data_preview}")

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
            self.logger.debug(f"Processing buffer (size: {len(self.buffer)}): {self.buffer[:100]}...")

            # Проверяем, нет ли в буфере сообщения JSON без заголовков
            # Это может происходить с GitHub Copilot или PyCharm, которые отправляют сообщения с \n в конце
            if self.content_length is None and self.buffer.find(b"\n") > -1:
                newline_pos = self.buffer.find(b"\n")
                possible_json = self.buffer[:newline_pos].strip()

                try:
                    # Пробуем разобрать сообщение как JSON
                    decoded_json = possible_json.decode('utf-8')
                    if decoded_json.startswith('{') and decoded_json.endswith('}'):
                        self.logger.debug(f"Found possible JSON message without headers: {decoded_json}")

                        request = json.loads(decoded_json)
                        response = self._handle_request(request)

                        # Отправляем ответ, если он есть
                        if response:
                            self._send_response(response)

                        # Удаляем обработанное сообщение из буфера
                        self.buffer = self.buffer[newline_pos + 1:]
                        continue
                except (UnicodeDecodeError, json.JSONDecodeError) as e:
                    self.logger.debug(f"Not a valid JSON message: {str(e)}, continuing with standard parsing")

            # Стандартная обработка сообщений с заголовками
            if self.content_length is None:
                # Ищем двойной перенос строки, отделяющий заголовки от тела
                header_end = self.buffer.find(b"\r\n\r\n")
                if header_end == -1:
                    # Альтернативно, PyCharm может использовать только \n\n вместо \r\n\r\n
                    header_end = self.buffer.find(b"\n\n")
                    if header_end == -1:
                        # Если не найден, ждем больше данных
                        break

                # Извлекаем заголовки
                headers = self.buffer[:header_end].decode('utf-8', errors='replace')
                self.logger.debug(f"Found headers: {headers}")

                # Ищем Content-Length
                for line in headers.split("\r\n" if "\r\n" in headers else "\n"):
                    if line.lower().startswith("content-length:"):
                        self.content_length = int(line.split(":", 1)[1].strip())
                        self.logger.debug(f"Found Content-Length: {self.content_length}")
                        break

                # Удаляем заголовки из буфера
                delim_len = 4 if b"\r\n\r\n" in self.buffer[:header_end+4] else 2  # 4 = len("\r\n\r\n"), 2 = len("\n\n")
                self.buffer = self.buffer[header_end + delim_len:]
                self.logger.debug(f"Removed headers, buffer size now: {len(self.buffer)}")

            # Если у нас достаточно данных для всего сообщения
            if self.content_length is not None and len(self.buffer) >= self.content_length:
                # Извлекаем тело сообщения
                message_body = self.buffer[:self.content_length].decode('utf-8', errors='replace')
                self.logger.debug(f"Extracted message body: {message_body}")
                self.buffer = self.buffer[self.content_length:]
                self.logger.debug(f"Remaining buffer size: {len(self.buffer)}")

                # Обрабатываем запрос
                try:
                    request = json.loads(message_body)
                    response = self._handle_request(request)

                    # Отправляем ответ
                    if response:
                        self._send_response(response)
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON: {message_body}, error: {str(e)}")
                except Exception as e:
                    self.logger.error(f"Error handling request: {str(e)}")
                    self.logger.error(traceback.format_exc())
                    # Отправляем ошибку, если был ID запроса
                    if 'request' in locals() and isinstance(request, dict) and "id" in request:
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

        self.request_count += 1
        current_time = time.time()
        uptime = current_time - self.start_time

        # Проверяем, является ли это уведомлением (без ID)
        if "id" not in request:
            method = request.get("method", "")
            self.logger.info(f"Received notification: {method} [req #{self.request_count}, uptime: {int(uptime)}s]")
            self.logger.debug(f"Full notification: {json.dumps(request)}")

            # Обрабатываем некоторые уведомления
            if method == "textDocument/didOpen":
                params = request.get("params", {})
                text_document = params.get("textDocument", {})
                uri = text_document.get("uri", "")
                if uri:
                    self.documents[uri] = text_document.get("text", "")
                    language_id = text_document.get("languageId", "unknown")
                    self.logger.info(f"Document opened: {uri} (Language: {language_id}, Size: {len(self.documents[uri])} chars)")

            elif method == "textDocument/didChange":
                params = request.get("params", {})
                text_document = params.get("textDocument", {})
                uri = text_document.get("uri", "")
                changes = params.get("contentChanges", [])
                if uri and uri in self.documents and changes:
                    # Простое обновление документа (не учитывает позиции изменений)
                    old_size = len(self.documents[uri])
                    self.documents[uri] = changes[-1].get("text", self.documents[uri])
                    new_size = len(self.documents[uri])
                    change_size = new_size - old_size
                    self.logger.info(f"Document changed: {uri} (Size delta: {'+' if change_size >= 0 else ''}{change_size} chars)")

            elif method == "textDocument/didClose":
                params = request.get("params", {})
                text_document = params.get("textDocument", {})
                uri = text_document.get("uri", "")
                if uri and uri in self.documents:
                    self.logger.info(f"Document closed: {uri} (Final size: {len(self.documents[uri])} chars)")
                    del self.documents[uri]

            # Для уведомлений не отправляем ответ
            return None

        method = request.get("method", "")
        message_id = request.get("id", 0)

        self.logger.info(f"Received request: {method} (ID: {message_id}) [req #{self.request_count}, uptime: {int(uptime)}s]")
        self.logger.debug(f"Full request: {json.dumps(request)}")

        # Стандартный ответ на initialize
        if method == "initialize":
            self.connection_attempts += 1
            params = request.get("params", {})
            client_info = params.get("clientInfo", {})
            client_name = client_info.get("name", "Unknown Client")
            client_version = client_info.get("version", "Unknown Version")
            protocol_version = params.get("protocolVersion", "Unknown")

            # Сохраняем информацию о клиенте и протоколе
            client_key = f"{client_name}_{client_version}"
            self.client_info[client_key] = {
                "name": client_name,
                "version": client_version,
                "last_connection": time.time(),
                "protocol": protocol_version,
                "capabilities": params.get("capabilities", {})
            }
            self.protocol_versions.add(protocol_version)

            self.logger.info(f"🔌 CONNECTION ATTEMPT #{self.connection_attempts} from {client_name} v{client_version}")
            self.logger.info(f"Protocol version: {protocol_version}")
            self.logger.info(f"Client capabilities: {json.dumps(params.get('capabilities', {}), indent=2)}")

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
            self.successful_connections += 1
            self.logger.info(f"✅ CONNECTION SUCCESSFUL #{self.successful_connections} (Total attempts: {self.connection_attempts})")

            # Отправляем уведомление о готовности
            self._send_notification("window/showMessage", {
                "type": 3,  # Info
                "message": f"MCP Server is ready and connected (Connection #{self.successful_connections})"
            })
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }

        # Ответ на shutdown
        elif method == "shutdown":
            self.logger.info(f"Received shutdown request after {int(uptime)}s uptime")
            self.logger.info(f"Connection stats: {self.successful_connections} successful connections out of {self.connection_attempts} attempts")
            self.logger.info(f"Processed {self.request_count} requests")
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }

        # Ответ на exit
        elif method == "exit":
            self.logger.info(f"Received exit request after {int(uptime)}s uptime")
            self.logger.info(f"Final stats: {self.successful_connections}/{self.connection_attempts} connections, {self.request_count} requests processed")

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
