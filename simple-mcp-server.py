#!/usr/bin/env python3
# filepath: /Users/rost/Documents/DIS/REPO/neozork-hld-prediction/simple-mcp-server.py
# -*- coding: utf-8 -*-
"""
Simple MCP Server for GitHub Copilot connection
This is a minimal implementation that handles stdio interface for GitHub Copilot
"""

import json
import sys
import traceback
import logging
import time
import signal
from typing import Dict, Any, Optional
import os

# Define maximum response delay to prevent buffer issues
MAX_RESPONSE_DELAY = 0.1  # Уменьшаем максимальную задержку с 0.5 до 0.1 секунд

# Determine the project root directory regardless of where the script is run from
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
# If script is run from the mcp directory, use parent directory as root
if os.path.basename(script_dir) == "mcp":
    project_root = os.path.dirname(script_dir)
else:
    project_root = script_dir

# Logging setup
logging.basicConfig(
    level=logging.DEBUG,  # Increase logging level for debugging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)      # Output logs to stdout for console display
    ]
)
logger = logging.getLogger("simple_mcp")

# Настройка логирования для вывода ВСЕЙ информации в консоль
# Убедимся, что никакие логи не будут фильтроваться
for handler in logging.root.handlers:
    handler.setLevel(logging.DEBUG)

# Установим DEBUG уровень для всех логгеров
logging.getLogger().setLevel(logging.DEBUG)

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
    # Get the root logger
    root_logger_instance = logging.getLogger()
    for handler in root_logger_instance.handlers:
        if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
            # Use more noticeable formatting for console output, including logger name
            handler.setFormatter(ColoredFormatter('📝 %(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            # Ensure the handler itself also processes DEBUG messages if not already configured
            # This might be redundant if basicConfig level is DEBUG and handler level is not explicitly set higher
            if handler.level > logging.DEBUG:
                handler.setLevel(logging.DEBUG)
            break # Assuming only one stdout handler for the root logger

# Create special loggers for client and request info
client_logger = logging.getLogger("client_info")
client_logger.setLevel(logging.DEBUG) # Changed from INFO to DEBUG
client_logger.propagate = True
# Добавляем явный обработчик для client_logger
client_handler = logging.StreamHandler(sys.stdout)
client_handler.setLevel(logging.DEBUG)
if os.name != 'nt':
    client_handler.setFormatter(ColoredFormatter('🔌 %(asctime)s - CLIENT - %(message)s'))
client_logger.addHandler(client_handler)

request_logger = logging.getLogger("request_info")
request_logger.setLevel(logging.DEBUG) # Changed from INFO to DEBUG
request_logger.propagate = True

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
                # Detect if data is too large for console
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

            # Always reset content length for new message
            self.logger.info(f"💾 Current buffer (size: {len(self.buffer)} byte): {self.buffer[:200].hex()}...")
            try:
                buffer_text = self.buffer.decode('utf-8', errors='replace')
                self.logger.info(f"💾 Buffer as text: {buffer_text[:300]}{'...' if len(buffer_text) > 300 else ''}")
            except Exception as e:
                self.logger.debug(f"Impossible decode buffer as text: {e}")

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
                request_obj = None  # Initialize for robust error handling
                try:
                    request_obj = json.loads(message_body)  # Use request_obj
                    response = self._handle_request(request_obj)

                    # Send response immediately for initialize or other critical requests
                    if response:
                        self._send_response(response)

                    # If the request was 'initialize' and it was successful (response has a result)
                    # Send readiness notifications immediately to potentially prevent client timeout
                    if request_obj and request_obj.get("method") == "initialize" and response and "result" in response:
                        self.logger.info("Sending readiness notifications immediately after 'initialize' response.")
                        self._send_notification("$/neozork/serverReady", {
                            "status": "ready",
                            "features": ["completion", "hover", "definition"]
                        })
                        self._send_notification("window/showMessage", {
                            "type": 3,  # Info
                            "message": f"MCP Server is ready and connected (Connection #{self.successful_connections})"
                        })

                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON: {message_body}, error: {str(e)}")
                except Exception as e:
                    self.logger.error(f"Error handling request: {str(e)}")
                    self.logger.error(traceback.format_exc())
                    # Send error if there was a request ID, using request_obj
                    if request_obj and isinstance(request_obj, dict) and "id" in request_obj:
                        self._send_error(request_obj["id"], -32603, f"Internal error: {str(e)}")

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

        # Создаем логи с атрибутом request_info для правильного форматирования
        req_log_record = logging.LogRecord(
            "request_info", logging.INFO, "", 0,
            f"REQUEST #{self.request_count}: {request_method} (ID: {request_id})",
            (), None
        )
        req_log_record.request_info = True
        self.request_logger.handle(req_log_record)

        params_log_record = logging.LogRecord(
            "request_info", logging.INFO, "", 0,
            f"PARAMS: {simplified_params}",
            (), None
        )
        params_log_record.request_info = True
        self.request_logger.handle(params_log_record)

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
                # Connection success is now counted upon sending the 'initialize' response.
                # This notification from the client confirms it has also initialized.
                self.logger.info(f"Received 'initialized' notification. Client is ready. (Current successful connections: {self.successful_connections}, Attempts: {self.connection_attempts})")
                # Note: self.successful_connections is no longer incremented here.

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

            # Mark connection as successful after server processes 'initialize' and sends response.
            if self.active_clients.get(client_key) and \
               not self.active_clients[client_key].get('initialization_counted_successful', False):
                self.successful_connections += 1
                self.active_clients[client_key]['initialization_counted_successful'] = True
                self.logger.info(f"✅ Connection marked SUCCESSFUL after 'initialize' response for {client_key}. Total successful: {self.successful_connections}, Attempts: {self.connection_attempts}")
            elif self.active_clients.get(client_key) and self.active_clients[client_key].get('initialization_counted_successful', False):
                self.logger.info(f"Connection for {client_key} already marked successful. 'initialize' received again?")
            else:
                self.logger.warning(f"Could not mark {client_key} as successful: client_key not found in active_clients after update.")

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

            # Detect if this is a Copilot request
            self.client_logger.info(f"🤖 COPILOT REQUEST: {method} (ID: {message_id})")

            # Store client information for Copilot
            if method == "copilot/signIn":
                # Authorization request
                self.logger.info("Query for Copilot sign-in")
                return {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": {
                        "status": "Success",
                        "user": "NeozorkMCPUser"
                    }
                }
            elif method == "copilot/getCompletions" or method == "getCompletions":
                # Query for completions
                self.logger.info("Query for Copilot completions")
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

            # Query for other Copilot features
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

        # Отключаем все задержки при ответе для GitHub Copilot
        response_delay = 0

        response_str = json.dumps(response)
        response_bytes = response_str.encode('utf-8')

        # Form complete message with headers
        header = f"Content-Length: {len(response_bytes)}\r\n\r\n".encode('utf-8')

        # Send message to stdout
        try:
            # Send response as a single block to prevent fragmentation
            message = header + response_bytes
            sys.stdout.buffer.write(message)
            sys.stdout.buffer.flush()

            response_id = response.get('id', 0)
            self.logger.info(f"Sent response for ID: {response_id} (size: {len(response_bytes)} bytes, delay: {response_delay:.3f}s)")
            # Add request info to the request logger
            self.request_logger.info(f"RESPONSE for ID {response_id}: {self._simplify_response(response)}")
            self.logger.debug(f"Full response: {response_str}")
        except Exception as e:
            self.logger.error(f"Error sending response: {str(e)}")
            self.logger.error(traceback.format_exc())
            # Try to send an error notification if stdout is still available
            try:
                self._send_notification("window/showMessage", {
                    "type": 1,  # Error
                    "message": f"Error sending response: {str(e)}"
                })
            except:
                pass

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
            # Send notification as a single block to prevent fragmentation
            message = header + notification_bytes
            sys.stdout.buffer.write(message)
            sys.stdout.buffer.flush()

            self.logger.info(f"Sent notification: {method} (size: {len(notification_bytes)} bytes)")
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
                "status": "active",
                "initialization_counted_successful": False # Initialize the flag
            }
            # Delete old entries if they exist
            # Создаем запись лога с атрибутом client_info для правильного форматирования
            log_record = logging.LogRecord(
                "client_info", logging.INFO, "", 0,
                f"⚡ NEW CONNECTION from {client_name} v{client_version}",
                (), None
            )
            log_record.client_info = True
            self.client_logger.handle(log_record)
        elif status == "disconnected":
            if client_key in self.active_clients:
                self.active_clients[client_key]["status"] = "disconnected"
                self.active_clients[client_key]["disconnected_at"] = time.time()
                # Display disconnection message
                log_record = logging.LogRecord(
                    "client_info", logging.INFO, "", 0,
                    f"❌ DISCONNECTED: {client_name} v{client_version}",
                    (), None
                )
                log_record.client_info = True
                self.client_logger.handle(log_record)

        # Print updated client information
        self._print_client_info()

    def _print_client_info(self):
        """
        Print information about active clients
        """
        # Создаем запись лога с атрибутом client_info для правильного форматирования
        log_record = logging.LogRecord(
            "client_info", logging.INFO, "", 0,
            f"Active clients: {len(self.active_clients)}",
            (), None
        )
        log_record.client_info = True
        self.client_logger.handle(log_record)

        for client_key, client_data in self.client_info.items():
            log_record = logging.LogRecord(
                "client_info", logging.INFO, "", 0,
                f"Client: {client_key}, Info: {json.dumps(client_data, indent=2)}",
                (), None
            )
            log_record.client_info = True
            self.client_logger.handle(log_record)

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
    # Create MCP server instance
    server = SimpleMCPServer()

    # Register signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        logger.info(f"Received signal {sig}, shutting down gracefully...")
        server.shutdown_gracefully()
        sys.exit(0)

    # Register signal handlers for SIGINT and SIGTERM
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    logger.info("Signal handlers registered for graceful shutdown (Ctrl+C/SIGTERM)")

    # Run the server
    server.run()
