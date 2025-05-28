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
import signal
from typing import Dict, Any, Optional, List
import os
import pathlib

# Determine the project root directory regardless of where the script is run from
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
# If script is run from the mcp directory, use parent directory as root
if os.path.basename(script_dir) == "mcp":
    project_root = os.path.dirname(script_dir)
else:
    project_root = script_dir

# Create logs directory in the project root
logs_dir = os.path.join(project_root, "logs")
if not os.path.exists(logs_dir):
    try:
        os.makedirs(logs_dir)
        print(f"Created logs directory: {logs_dir}")
    except Exception as e:
        print(f"Error creating logs directory: {e}")

# Logging setup
logging.basicConfig(
    level=logging.DEBUG,  # Increase logging level for debugging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(logs_dir, "mcp_server.log"), mode='a'),  # Save logs to logs directory
        logging.StreamHandler(sys.stdout)      # Output logs to stdout for console display
    ]
)
logger = logging.getLogger("simple_mcp")

# Setup additional console output only for detailed debugging (not for regular info messages)
console_handler = logging.StreamHandler(sys.stderr)
# Set console handler to DEBUG level to capture all messages
console_handler.setLevel(logging.DEBUG)
# Filter to only show DEBUG messages in console
class DebugOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG

console_handler.addFilter(DebugOnlyFilter())
console_formatter = logging.Formatter('🔍 DEBUG: %(message)s')
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)

# Add log entry about server startup
logger.info("========================")
logger.info("MCP Server starting up at %s", time.strftime("%Y-%m-%d %H:%M:%S"))
logger.info("Working directory: %s", os.getcwd())
logger.info("Project root directory: %s", project_root)
logger.info("Script location: %s", os.path.abspath(__file__))
logger.info("========================")

# Add colored logging for better console readability
class ColoredFormatter(logging.Formatter):
    """Class for colored log formatting"""
    COLORS = {
        'DEBUG': '\033[94m',  # blue
        'INFO': '\033[92m',   # green
        'WARNING': '\033[93m', # yellow
        'ERROR': '\033[91m',   # red
        'CRITICAL': '\033[91m\033[1m', # bold red
        'RESET': '\033[0m',    # reset color
        'CLIENT': '\033[96m',  # cyan for client info
        'REQUEST': '\033[95m', # magenta for requests
        'RESPONSE': '\033[93m' # yellow for responses
    }

    def format(self, record):
        log_message = super().format(record)
        if hasattr(record, 'levelname') and record.levelname in self.COLORS:
            return f"{self.COLORS[record.levelname]}{log_message}{self.COLORS['RESET']}"
        if hasattr(record, 'client_info'):
            return f"{self.COLORS['CLIENT']}{log_message}{self.COLORS['RESET']}"
        if hasattr(record, 'request_info'):
            return f"{self.COLORS['REQUEST']}{log_message}{self.COLORS['RESET']}"
        if hasattr(record, 'response_info'):
            return f"{self.COLORS['RESPONSE']}{log_message}{self.COLORS['RESET']}"
        return log_message

# Apply colored formatter for console if not Windows
if os.name != 'nt':
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            if handler.stream == sys.stdout:
                # Use more noticeable formatting for console output
                handler.setFormatter(ColoredFormatter('📝 %(asctime)s - %(levelname)s - %(message)s'))

# Create a special console handler for client and request details
client_console_handler = logging.StreamHandler(sys.stderr)
client_console_handler.setLevel(logging.INFO)
client_formatter = logging.Formatter('👥 CLIENTS: %(message)s')
client_console_handler.setFormatter(client_formatter)

request_console_handler = logging.StreamHandler(sys.stderr)
request_console_handler.setLevel(logging.INFO)
request_formatter = logging.Formatter('📡 REQUEST/RESPONSE: %(message)s')
request_console_handler.setFormatter(request_formatter)

# Create special loggers for client and request info
client_logger = logging.getLogger("client_info")
client_logger.setLevel(logging.INFO)
client_logger.addHandler(client_console_handler)
client_logger.propagate = False

request_logger = logging.getLogger("request_info")
request_logger.setLevel(logging.INFO)
request_logger.addHandler(request_console_handler)
request_logger.propagate = False

class SimpleMCPServer:
    """
    Simple MCP server for successful GitHub Copilot connection via stdio
    """

    def __init__(self):
        self.logger = logger
        self.client_logger = client_logger
        self.request_logger = request_logger
        self.logger.info("Simple MCP Server initialized with stdio interface")
        # Create buffer for incoming data
        self.buffer = b""
        self.content_length = None
        # Dictionary for storing open documents
        self.documents = {}
        # Message identifier
        self.next_id = 1
        # Counters for statistics
        self.connection_attempts = 0
        self.successful_connections = 0
        self.request_count = 0
        self.start_time = time.time()
        # Client and protocol information
        self.client_info = {}
        self.protocol_versions = set()
        # Active client sessions
        self.active_clients = {}

        # Show initial client info
        self._print_client_info()

    def run(self):
        """
        Runs MCP server to process requests from GitHub Copilot via stdio
        """
        try:
            self.logger.info("MCP Server started with stdio interface")

            # Main loop for reading from stdin and writing to stdout
            self._handle_stdio()

        except Exception as e:
            self.logger.error(f"Error in MCP server: {str(e)}")
            self.logger.error(traceback.format_exc())
            # Send error notification
            self._send_notification("window/showMessage", {
                "type": 1,  # Error
                "message": f"MCP Server Error: {str(e)}"
            })

    def _handle_stdio(self):
        """
        Handles input/output through standard streams
        """
        # Set binary mode for stdin and stdout on Windows
        if os.name == 'nt':
            import msvcrt
            msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
            msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

        # Main processing loop
        while True:
            # Read data from stdin
            try:
                data = sys.stdin.buffer.read1(4096)
                if not data:
                    self.logger.info("End of stdin stream, exiting")
                    break

                self.buffer += data

                # Output information about received data in readable format
                data_preview = str(data)
                if len(data_preview) > 200:
                    data_preview = data_preview[:200] + "... (truncated)"

                self.logger.info(f"📥 Received {len(data)} bytes, buffer size: {len(self.buffer)}")
                # Подробное логирование содержимого запроса
                try:
                    decoded_data = data.decode('utf-8', errors='replace')
                    self.request_logger.info(f"RAW INPUT [{len(data)} bytes]: {decoded_data[:300]}{'...' if len(decoded_data) > 300 else ''}")
                except Exception as e:
                    self.logger.debug(f"Unable to decode data for display: {e}")

                # Process messages while they exist in the buffer
                self._process_buffer()

            except Exception as e:
                self.logger.error(f"Error reading from stdin: {str(e)}")
                self.logger.error(traceback.format_exc())
                break

    def _process_buffer(self):
        """
        Processes the buffer and extracts messages
        """
        while True:
            if len(self.buffer) == 0:
                break

            self.logger.debug(f"Processing buffer (size: {len(self.buffer)}): {self.buffer[:100]}...")

            # Check for JSON message without headers in the buffer
            # This can happen with GitHub Copilot or PyCharm, which send messages with \n at the end
            if self.content_length is None and self.buffer.find(b"\n") > -1:
                newline_pos = self.buffer.find(b"\n")
                possible_json = self.buffer[:newline_pos].strip()

                try:
                    # Try to parse the message as JSON
                    decoded_json = possible_json.decode('utf-8')
                    if decoded_json.startswith('{') and decoded_json.endswith('}'):
                        self.logger.debug(f"Found possible JSON message without headers: {decoded_json}")

                        request = json.loads(decoded_json)
                        response = self._handle_request(request)

                        # Send response if available
                        if response:
                            self._send_response(response)

                        # Remove processed message from buffer
                        self.buffer = self.buffer[newline_pos + 1:]
                        continue
                except (UnicodeDecodeError, json.JSONDecodeError) as e:
                    self.logger.debug(f"Not a valid JSON message: {str(e)}, continuing with standard parsing")

            # Standard message processing with headers
            if self.content_length is None:
                # Look for double line break separating headers from body
                header_end = self.buffer.find(b"\r\n\r\n")
                if header_end == -1:
                    # Alternatively, PyCharm might use just \n\n instead of \r\n\r\n
                    header_end = self.buffer.find(b"\n\n")
                    if header_end == -1:
                        # GitHub Copilot might send single Content-Length header with \r\n
                        content_length_header = b"Content-Length: "
                        if content_length_header in self.buffer:
                            cl_start = self.buffer.find(content_length_header) + len(content_length_header)
                            cl_end = self.buffer.find(b"\r\n", cl_start)
                            if cl_end > cl_start:
                                try:
                                    self.content_length = int(self.buffer[cl_start:cl_end].decode('utf-8').strip())
                                    self.logger.debug(f"Found standalone Content-Length: {self.content_length}")
                                    # Remove header from buffer
                                    header_end = cl_end
                                    self.buffer = self.buffer[cl_end + 2:]  # +2 for \r\n
                                    self.logger.debug(f"Removed Content-Length header, buffer size now: {len(self.buffer)}")
                                    # Continue processing with the known content length
                                    continue
                                except (ValueError, UnicodeDecodeError) as e:
                                    self.logger.debug(f"Error parsing Content-Length: {str(e)}")

                        # If no headers found, dump buffer contents for debugging and wait for more data
                        if len(self.buffer) > 0:
                            self.logger.debug(f"No complete headers found. Buffer content (hex): {self.buffer.hex()}")
                            self.logger.debug(f"Buffer content (text, if possible): {self.buffer.decode('utf-8', errors='replace')}")
                        break

                # Extract headers
                headers = self.buffer[:header_end].decode('utf-8', errors='replace')
                self.logger.debug(f"Found headers: {headers}")

                # Look for Content-Length
                for line in headers.split("\r\n" if "\r\n" in headers else "\n"):
                    if line.lower().startswith("content-length:"):
                        self.content_length = int(line.split(":", 1)[1].strip())
                        self.logger.debug(f"Found Content-Length: {self.content_length}")
                        break

                # Remove headers from buffer
                delim_len = 4 if b"\r\n\r\n" in self.buffer[:header_end+4] else 2  # 4 = len("\r\n\r\n"), 2 = len("\n\n")
                self.buffer = self.buffer[header_end + delim_len:]
                self.logger.debug(f"Removed headers, buffer size now: {len(self.buffer)}")

            # If we have enough data for the entire message
            if self.content_length is not None and len(self.buffer) >= self.content_length:
                # Extract message body
                message_body = self.buffer[:self.content_length].decode('utf-8', errors='replace')
                self.logger.debug(f"Extracted message body: {message_body}")
                self.buffer = self.buffer[self.content_length:]
                self.logger.debug(f"Remaining buffer size: {len(self.buffer)}")

                # Process request
                try:
                    request = json.loads(message_body)
                    response = self._handle_request(request)

                    # Send response
                    if response:
                        self._send_response(response)
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON: {message_body}, error: {str(e)}")
                except Exception as e:
                    self.logger.error(f"Error handling request: {str(e)}")
                    self.logger.error(traceback.format_exc())
                    # Send error if there was a request ID
                    if 'request' in locals() and isinstance(request, dict) and "id" in request:
                        self._send_error(request["id"], -32603, f"Internal error: {str(e)}")

                # Reset content_length for next message
                self.content_length = None
            else:
                # If not enough data, wait for more
                break

    def _handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Processing requests from GitHub Copilot
        """
        if not request:
            return {}

        self.request_count += 1
        current_time = time.time()
        uptime = current_time - self.start_time

        # Display request details on screen
        request_method = request.get("method", "unknown")
        request_id = request.get("id", "notification")
        request_params = request.get("params", {})
        simplified_params = self._simplify_params(request_params)
        self.request_logger.info(f"REQUEST #{self.request_count}: {request_method} (ID: {request_id})")
        self.request_logger.info(f"PARAMS: {simplified_params}")

        # Check if this is a notification (without ID)
        if "id" not in request:
            method = request.get("method", "")
            self.logger.info(f"Received notification: {method} [req #{self.request_count}, uptime: {int(uptime)}s]")
            self.logger.debug(f"Full notification: {json.dumps(request)}")

            # Process some notifications
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
                    # Simple document update (does not account for change positions)
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

            # New case for initialized notification to fix connection problems
            elif method == "initialized":
                self.successful_connections += 1
                self.logger.info(f"✅ CONNECTION SUCCESSFUL #{self.successful_connections} (Total attempts: {self.connection_attempts})")

                # Send ready notification
                self._send_notification("window/showMessage", {
                    "type": 3,  # Info
                    "message": f"MCP Server is ready and connected (Connection #{self.successful_connections})"
                })

                # Send server ready notification
                self._send_notification("$/neozork/serverReady", {
                    "status": "ready",
                    "features": ["completion", "hover", "definition"]
                })

            # For notifications, we don't send a response
            return None

        method = request.get("method", "")
        message_id = request.get("id", 0)

        self.logger.info(f"Received request: {method} (ID: {message_id}) [req #{self.request_count}, uptime: {int(uptime)}s]")
        self.logger.debug(f"Full request: {json.dumps(request)}")

        # Standard response to initialize
        if method == "initialize":
            self.connection_attempts += 1
            params = request.get("params", {})
            client_info = params.get("clientInfo", {})
            client_name = client_info.get("name", "Unknown Client")
            client_version = client_info.get("version", "Unknown Version")
            protocol_version = params.get("protocolVersion", "Unknown")

            # Save client and protocol information
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

            self._update_client_list(client_name, client_version, status="connected")

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

        # Response to textDocument/completion
        elif method == "textDocument/completion":
            self.logger.info(f"Received completion request (ID: {message_id})")

            # Create a simple completion response
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "isIncomplete": False,
                    "items": [
                        {
                            "label": "Simple placeholder completion",
                            "kind": 1,  # Text
                            "detail": "NeoZork MCP Server placeholder completion",
                            "documentation": "This is a placeholder completion from the simple MCP server",
                            "insertText": "placeholder_completion"
                        }
                    ]
                }
            }

        # Response to textDocument/hover
        elif method == "textDocument/hover":
            self.logger.info(f"Received hover request (ID: {message_id})")
            params = request.get("params", {})
            position = params.get("position", {})
            text_document = params.get("textDocument", {})
            uri = text_document.get("uri", "")

            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "contents": {
                        "kind": "markdown",
                        "value": "Hover information from NeoZork MCP Server"
                    }
                }
            }

        # Response to textDocument/definition
        elif method == "textDocument/definition":
            self.logger.info(f"Received definition request (ID: {message_id})")

            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": [] # Empty array means no definitions found
            }

        # Response to custom method that GitHub Copilot might send
        elif method.startswith("copilot/"):
            self.logger.info(f"Received Copilot-specific request: {method}")

            # Детальное логирование запроса Copilot
            self.client_logger.info(f"🤖 COPILOT REQUEST: {method} (ID: {message_id})")

            # Специальная обработка запросов Copilot по их типу
            if method == "copilot/signIn":
                # Обработка авторизации Copilot
                self.logger.info("Обработка запроса авторизации Copilot")
                return {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": {
                        "status": "Success",
                        "user": "NeozorkMCPUser"
                    }
                }
            elif method == "copilot/getCompletions" or method == "getCompletions":
                # Запрос автодополнений
                self.logger.info("Обработка запроса на автодополнения")
                return {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": {
                        "completions": [
                            {
                                "text": "// Placeholder completion from NeozorkMCP",
                                "displayText": "Placeholder completion",
                                "position": {"line": 0, "character": 0}
                            }
                        ]
                    }
                }

            # Обработка всех остальных запросов Copilot с общим положительным ответом
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": {
                    "status": "Success"
                }
            }

        # Response to shutdown
        elif method == "shutdown":
            self.logger.info(f"Received shutdown request after {int(uptime)}s uptime")
            self.logger.info(f"Connection stats: {self.successful_connections} successful connections out of {self.connection_attempts} attempts")
            self.logger.info(f"Processed {self.request_count} requests")
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }

        # Response to exit
        elif method == "exit":
            self.logger.info(f"Received exit request after {int(uptime)}s uptime")
            self.logger.info(f"Final stats: {self.successful_connections}/{self.connection_attempts} connections, {self.request_count} requests processed")

            # Send response before exiting
            response = {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }
            self._send_response(response)
            # Terminate program
            self.shutdown_gracefully()
            sys.exit(0)
            return None  # This won't execute, but leave it for consistency

        # Add default response for unknown requests
        else:
            self.logger.warning(f"Received unknown request method: {method}")
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }

    def _send_response(self, response: Dict[str, Any]) -> None:
        """
        Sending response via stdout
        """
        if not response:
            return

        response_str = json.dumps(response)
        response_bytes = response_str.encode('utf-8')

        # Form complete message with headers
        header = f"Content-Length: {len(response_bytes)}\r\n\r\n".encode('utf-8')

        # Send message to stdout
        try:
            sys.stdout.buffer.write(header)
            sys.stdout.buffer.write(response_bytes)
            sys.stdout.buffer.flush()

            response_id = response.get('id', 0)
            self.logger.info(f"Sent response for ID: {response_id}")
            # Добавляем более подробный вывод для отладки
            self.request_logger.info(f"RESPONSE for ID {response_id}: {self._simplify_response(response)}")
            self.logger.debug(f"Full response: {response_str}")
        except Exception as e:
            self.logger.error(f"Error sending response: {str(e)}")
            self.logger.error(traceback.format_exc())

    def _send_notification(self, method: str, params: Dict[str, Any]) -> None:
        """
        Sending notification (message without ID) to server
        """
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }

        notification_str = json.dumps(notification)
        notification_bytes = notification_str.encode('utf-8')

        # Form complete message with headers
        header = f"Content-Length: {len(notification_bytes)}\r\n\r\n".encode('utf-8')

        # Send message to stdout
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
        Sending error message
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

    def _simplify_params(self, params):
        """
        Simplify request parameters for display
        """
        if not params:
            return "{}"

        # Create a simplified version of parameters for display
        result = {}

        # Handle different types of requests
        if "textDocument" in params:
            doc = params["textDocument"]
            if "uri" in doc:
                result["textDocument"] = {"uri": doc["uri"]}
            if "languageId" in doc:
                if "textDocument" not in result:
                    result["textDocument"] = {}
                result["textDocument"]["languageId"] = doc["languageId"]

        if "clientInfo" in params:
            client_info = params["clientInfo"]
            result["clientInfo"] = {
                "name": client_info.get("name", "Unknown"),
                "version": client_info.get("version", "Unknown")
            }

        if "capabilities" in params:
            # Just indicate we have capabilities without the full details
            result["capabilities"] = "..." if params["capabilities"] else "{}"

        if "processId" in params:
            result["processId"] = params["processId"]

        if "rootUri" in params:
            result["rootUri"] = params["rootUri"]

        if "protocolVersion" in params:
            result["protocolVersion"] = params["protocolVersion"]

        # For other parameters types, just include them directly if they're not too large
        for key, value in params.items():
            if key not in result:
                if isinstance(value, dict):
                    if len(json.dumps(value)) > 50:
                        result[key] = "..."
                    else:
                        result[key] = value
                elif isinstance(value, list):
                    if len(value) > 3:
                        result[key] = f"[...] ({len(value)} items)"
                    else:
                        result[key] = value
                elif isinstance(value, str) and len(value) > 50:
                    result[key] = value[:47] + "..."
                else:
                    result[key] = value

        return json.dumps(result, indent=2)

    def _simplify_response(self, response):
        """
        Simplify response for display
        """
        if not response:
            return "{}"

        # Create a simplified version for display
        result = {}

        # Include main response properties
        if "id" in response:
            result["id"] = response["id"]

        if "jsonrpc" in response:
            result["jsonrpc"] = response["jsonrpc"]

        # For results, simplify based on content
        if "result" in response:
            if isinstance(response["result"], dict):
                result_preview = {}
                # Include key information from capabilities
                if "capabilities" in response["result"]:
                    result_preview["capabilities"] = "..." if response["result"]["capabilities"] else "{}"
                if "serverInfo" in response["result"]:
                    result_preview["serverInfo"] = response["result"]["serverInfo"]
                result["result"] = result_preview
            else:
                result["result"] = response["result"]

        # Include error information if present
        if "error" in response:
            result["error"] = response["error"]

        return json.dumps(result, indent=2)

    def _update_client_list(self, client_name, client_version, status="connected"):
        """
        Update the list of active clients
        """
        client_key = f"{client_name}_{client_version}"

        # Update active clients list
        if status == "connected":
            self.active_clients[client_key] = {
                "name": client_name,
                "version": client_version,
                "connected_at": time.time(),
                "status": "active"
            }
            # Сразу выводим информацию о новом подключении через client_logger
            self.client_logger.info(f"⚡ NEW CONNECTION from {client_name} v{client_version}")
        elif status == "disconnected":
            if client_key in self.active_clients:
                self.active_clients[client_key]["status"] = "disconnected"
                self.active_clients[client_key]["disconnected_at"] = time.time()
                # Выводим информацию об отключении
                self.client_logger.info(f"❌ DISCONNECTED: {client_name} v{client_version}")

        # Print updated client information
        self._print_client_info()

    def _print_client_info(self):
        """
        Print information about active clients
        """
        self.client_logger.info(f"Active clients: {len(self.active_clients)}")
        for client_key, client_data in self.client_info.items():
            self.client_logger.info(f"Client: {client_key}, Info: {json.dumps(client_data, indent=2)}")

    def shutdown_gracefully(self):
        """
        Gracefully shut down the server, show statistics
        """
        uptime = time.time() - self.start_time
        self.logger.info("=" * 50)
        self.logger.info(f"⚠️ Server shutting down after {int(uptime)}s uptime")
        self.logger.info(f"📊 Connection stats: {self.successful_connections} successful connections out of {self.connection_attempts} attempts")
        self.logger.info(f"📊 Processed {self.request_count} requests")

        # Display information about active clients
        active_count = len([c for c in self.active_clients.values() if c.get("status") == "active"])
        self.logger.info(f"👥 Active clients at shutdown: {active_count}")
        for client_key, client_data in self.active_clients.items():
            if client_data.get("status") == "active":
                self.logger.info(f"   - {client_data.get('name')} v{client_data.get('version')}")

        self.logger.info("🛑 Server shutdown complete")
        self.logger.info("=" * 50)

        # Can perform any other cleanup needed here

        return


if __name__ == "__main__":
    # Создаем экземпляр сервера
    server = SimpleMCPServer()

    # Регистрируем обработчик сигналов для корректного завершения
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}, shutting down gracefully...")
        server.shutdown_gracefully()
        sys.exit(0)

    # Регистрируем обработчики сигналов SIGINT (Ctrl+C) и SIGTERM
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("Signal handlers registered for graceful shutdown (Ctrl+C/SIGTERM)")

    # Запускаем сервер
    server.run()
