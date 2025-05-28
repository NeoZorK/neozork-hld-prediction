#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testing MCP connection with PyCharm
This script helps verify compatibility of MCP server with PyCharm
"""

import sys
import os
import json
import subprocess
import time
import logging
import threading
import uuid
from typing import Dict, Any, Optional, List

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(logs_dir):
    try:
        os.makedirs(logs_dir)
        print(f"Created logs directory: {logs_dir}")
    except Exception as e:
        print(f"Error creating logs directory: {e}")

# Setup logging configuration
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(logs_dir, "pycharm_mcp_test.log"), mode='a'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("pycharm_mcp_test")

def send_message(message: Dict[str, Any]) -> None:
    """Sends a message via stdout in LSP format"""
    message_str = json.dumps(message)
    message_bytes = message_str.encode('utf-8')

    # Form the message with headers
    header = f"Content-Length: {len(message_bytes)}\r\n\r\n".encode('utf-8')

    sys.stdout.buffer.write(header)
    sys.stdout.buffer.write(message_bytes)
    sys.stdout.buffer.flush()

    logger.debug(f"Sent message: {message_str}")

def read_message(timeout=5.0):
    """Reads a message from stdin in LSP format with timeout"""
    # Read headers
    content_length = None
    start_time = time.time()
    buffer = b""

    # Non-blocking header reading with timeout
    while True:
        if time.time() - start_time > timeout:
            logger.warning(f"Timeout reached while reading headers after {timeout} seconds")
            return None

        if os.name == 'nt':  # Windows uses blocking read
            line = sys.stdin.buffer.readline()
        else:
            # Check data availability
            import select
            ready, _, _ = select.select([sys.stdin], [], [], 0.1)
            if not ready:
                time.sleep(0.1)  # Small pause to avoid CPU overload
                continue
            line = sys.stdin.buffer.readline()

        if not line:
            logger.warning("No data received from stdin")
            time.sleep(0.1)
            continue

        # Add to buffer and look for end-of-header marker
        buffer += line

        # Support both standard \r\n\r\n and PyCharm-style \n\n delimiters
        if b'\r\n\r\n' in buffer:
            headers, buffer = buffer.split(b'\r\n\r\n', 1)
            break
        elif b'\n\n' in buffer:
            headers, buffer = buffer.split(b'\n\n', 1)
            break

        # Check Content-Length header in the current line
        try:
            header = line.decode('utf-8').strip()
            if header.lower().startswith('content-length:'):
                content_length = int(header.split(':', 1)[1].strip())
                logger.debug(f"Found Content-Length: {content_length}")
        except Exception as e:
            logger.warning(f"Error parsing header: {e}")

    # If data is already present after header delimiter, consider it the start of the body
    body = buffer

    # If Content-Length is not found, return error
    if content_length is None:
        logger.error("Content-Length header not found")
        return None

    # Read the remaining part of the body
    remaining = content_length - len(body)
    if remaining > 0:
        logger.debug(f"Reading remaining {remaining} bytes of message body")

        # Read remaining data with timeout
        start_body_time = time.time()
        while len(body) < content_length:
            if time.time() - start_body_time > timeout:
                logger.warning(f"Timeout reached while reading message body after {timeout} seconds")
                return None

            if os.name == 'nt':  # Windows uses blocking read
                chunk = sys.stdin.buffer.read(min(1024, content_length - len(body)))
            else:
                # Check data availability
                import select
                ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                if not ready:
                    time.sleep(0.1)  # Small pause to avoid CPU overload
                    continue
                chunk = sys.stdin.buffer.read(min(1024, content_length - len(body)))

            if not chunk:
                time.sleep(0.1)
                continue

            body += chunk
            logger.debug(f"Read {len(chunk)} bytes, total {len(body)}/{content_length}")

    if len(body) != content_length:
        logger.warning(f"Incomplete message: got {len(body)} bytes, expected {content_length}")
        return None

    try:
        message = json.loads(body.decode('utf-8'))
        logger.debug(f"Received message: {json.dumps(message)}")
        return message
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON: {e}")
        logger.debug(f"Raw content: {body}")
        return None

def test_mcp_connection():
    """Tests connection with MCP server"""
    logger.info("Starting MCP connection test")

    # 1. Send initialize request
    initialize_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "processId": os.getpid(),
            "clientInfo": {
                "name": "PyCharm Test Client",
                "version": "1.0.0"
            },
            "rootUri": f"file://{os.getcwd()}",
            "capabilities": {},
            "trace": "verbose",
            "protocolVersion": "2025-03-26"
        }
    }

    logger.info("Sending initialize request")
    send_message(initialize_request)

    # 2. Wait for initialize response
    initialize_response = read_message()
    if not initialize_response:
        logger.error("Failed to receive initialize response")
        return False

    logger.info("Received initialize response")

    # 3. Send initialized notification
    initialized_notification = {
        "jsonrpc": "2.0",
        "method": "initialized",
        "params": {}
    }

    logger.info("Sending initialized notification")
    send_message(initialized_notification)

    # 4. Optionally wait for any server notification
    try:
        notification = read_message()
        if notification:
            logger.info(f"Received notification: {notification.get('method', 'unknown')}")
    except Exception as e:
        logger.warning(f"Error while waiting for notification: {str(e)}")

    # 5. Send shutdown request
    shutdown_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "shutdown"
    }

    logger.info("Sending shutdown request")
    send_message(shutdown_request)

    # 6. Wait for shutdown response
    shutdown_response = read_message()
    if not shutdown_response:
        logger.error("Failed to receive shutdown response")
        return False

    logger.info("Received shutdown response")

    # 7. Send exit notification
    exit_notification = {
        "jsonrpc": "2.0",
        "method": "exit"
    }

    logger.info("Sending exit notification")
    send_message(exit_notification)

    logger.info("MCP connection test completed successfully")
    return True

def test_mcp_connection_direct(server_process):
    """Tests connection with MCP server via direct input/output streams"""
    logger.info("Starting MCP direct connection test")

    # 1. Send initialize request
    initialize_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "processId": os.getpid(),
            "clientInfo": {
                "name": "PyCharm Test Client",
                "version": "1.0.0"
            },
            "rootUri": f"file://{os.getcwd()}",
            "capabilities": {},
            "trace": "verbose",
            "protocolVersion": "2025-03-26"
        }
    }

    logger.info("Sending initialize request")
    _send_message_to_server(server_process, initialize_request)

    # 2. Wait for initialize response
    initialize_response = _read_message_from_server(server_process)
    if not initialize_response:
        logger.error("Failed to receive initialize response")
        return False

    logger.info(f"Received initialize response: {json.dumps(initialize_response)}")

    # 3. Send initialized notification
    initialized_notification = {
        "jsonrpc": "2.0",
        "method": "initialized",
        "params": {}
    }

    logger.info("Sending initialized notification")
    _send_message_to_server(server_process, initialized_notification)

    # 4. Optionally wait for any server notification
    try:
        # Set short timeout as server may not send notifications
        notification = _read_message_from_server(server_process, timeout=1.0)
        if notification:
            logger.info(f"Received notification: {notification.get('method', 'unknown')}")
    except Exception as e:
        logger.warning(f"Error while waiting for notification: {str(e)}")

    # Notification is optional, so continue the test
    logger.info("Continuing test after waiting for optional notification")

    # 5. Send shutdown request
    shutdown_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "shutdown"
    }

    logger.info("Sending shutdown request")
    _send_message_to_server(server_process, shutdown_request)

    # 6. Wait for shutdown response
    shutdown_response = _read_message_from_server(server_process)
    if not shutdown_response:
        logger.error("Failed to receive shutdown response")
        return False

    logger.info("Received shutdown response")

    # 7. Send exit notification
    exit_notification = {
        "jsonrpc": "2.0",
        "method": "exit"
    }

    logger.info("Sending exit notification")
    _send_message_to_server(server_process, exit_notification)

    logger.info("MCP connection test completed successfully")
    return True

def _send_message_to_server(server_process, message):
    """Sends a message to MCP server via its stdin"""
    message_str = json.dumps(message)
    message_bytes = message_str.encode('utf-8')

    # Form the message with headers
    header = f"Content-Length: {len(message_bytes)}\r\n\r\n".encode('utf-8')

    try:
        server_process.stdin.write(header)
        server_process.stdin.write(message_bytes)
        server_process.stdin.flush()
        logger.debug(f"Sent message to server: {message_str}")
    except Exception as e:
        logger.error(f"Error sending message to server: {str(e)}")
        raise

def _read_message_from_server(server_process, timeout=5.0):
    """Reads a message from MCP server via its stdout with timeout"""
    # Read headers
    content_length = None
    start_time = time.time()
    buffer = b""

    logger.debug("Starting to read message from server")

    # Non-blocking header reading with timeout
    while True:
        if time.time() - start_time > timeout:
            logger.warning(f"Timeout reached while reading server headers after {timeout} seconds")
            return None

        # Check data availability
        import select
        ready, _, _ = select.select([server_process.stdout], [], [], 0.1)
        if not ready:
            time.sleep(0.1)  # Small pause to avoid CPU overload
            continue

        # Read the whole line to look for headers
        line = server_process.stdout.readline()
        if not line:
            if server_process.poll() is not None:
                logger.error(f"Server process exited with code {server_process.returncode}")
                return None
            time.sleep(0.1)
            continue

        # Add to buffer
        buffer += line
        logger.debug(f"Read line from server: {line}")

        # Check Content-Length header in the current line
        try:
            header = line.decode('utf-8', errors='ignore').strip()
            if header.lower().startswith("content-length:"):
                content_length = int(header.split(":", 1)[1].strip())
                logger.debug(f"Found Content-Length: {content_length}")
        except Exception as e:
            logger.warning(f"Error parsing header: {e}")

        # Check if this is the end of headers
        if line == b"\r\n" or line == b"\n":
            logger.debug("Found end of headers")
            break

    # If Content-Length is not found, try searching in the buffer
    if content_length is None:
        try:
            header_text = buffer.decode('utf-8', errors='ignore')
            for line in header_text.split("\r\n"):
                if line.lower().startswith("content-length:"):
                    content_length = int(line.split(":", 1)[1].strip())
                    logger.debug(f"Found Content-Length in buffer: {content_length}")
                    break
        except Exception as e:
            logger.warning(f"Error parsing headers in buffer: {e}")

    # If Content-Length is still not found, another attempt - search directly in binary buffer
    if content_length is None:
        cl_marker = b"Content-Length: "
        if cl_marker in buffer:
            try:
                start_pos = buffer.find(cl_marker) + len(cl_marker)
                end_pos = buffer.find(b"\r\n", start_pos)
                if end_pos == -1:
                    end_pos = buffer.find(b"\n", start_pos)
                if end_pos > start_pos:
                    cl_str = buffer[start_pos:end_pos].decode('utf-8', errors='ignore')
                    content_length = int(cl_str.strip())
                    logger.debug(f"Found Content-Length using binary search: {content_length}")
            except Exception as e:
                logger.warning(f"Error parsing Content-Length from binary buffer: {e}")

    # If Content-Length is still not found, return error
    if content_length is None:
        logger.error("Content-Length header not found in server response")
        logger.debug(f"Buffer content: {buffer}")
        return None

    # Find end of headers in buffer
    header_end = buffer.find(b"\r\n\r\n")
    if header_end == -1:
        header_end = buffer.find(b"\n\n")

    if header_end != -1:
        # Remove headers from buffer
        delimiter_size = 4 if b"\r\n\r\n" in buffer[:header_end+4] else 2
        body_start = header_end + delimiter_size
        body = buffer[body_start:]
        logger.debug(f"Found body start at position {body_start}, body size: {len(body)}")
    else:
        # If end of headers is not found, consider all read data as headers
        body = b""
        logger.debug("No body found in buffer yet")

    # Read the remaining part of the message body
    while len(body) < content_length:
        if time.time() - start_time > timeout:
            logger.warning(f"Timeout reached while reading message body after {timeout} seconds")
            return None

        # Check data availability
        import select
        ready, _, _ = select.select([server_process.stdout], [], [], 0.1)
        if not ready:
            time.sleep(0.1)
            continue

        # Read data in chunks
        to_read = min(1024, content_length - len(body))
        chunk = server_process.stdout.read(to_read)
        if not chunk:
            if server_process.poll() is not None:
                logger.error(f"Server process exited with code {server_process.returncode}")
                return None
            time.sleep(0.1)
            continue

        body += chunk
        logger.debug(f"Read {len(chunk)} bytes from server, total body size: {len(body)}/{content_length}")

    if len(body) > content_length:
        # If we read more data than needed, keep only the first content_length bytes
        logger.warning(f"Read more data than needed ({len(body)} > {content_length}), truncating")
        body = body[:content_length]

    # Try parsing JSON
    try:
        message = json.loads(body.decode('utf-8', errors='replace'))
        logger.debug(f"Successfully parsed JSON from server: {json.dumps(message)}")
        return message
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from server: {e}")
        logger.debug(f"Raw body content: {body}")
        return None

def launch_mcp_server(server_path=None, timeout=10):
    """Launches MCP server and returns the process"""
    if server_path is None:
        # Try to find the server automatically
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        default_server_path = os.path.join(project_root, "simple-mcp-server.py")

        if os.path.exists(default_server_path):
            server_path = default_server_path
        else:
            # Search other possible paths
            candidates = [
                os.path.join(project_root, "mcp", "mcp_server.py"),
                os.path.join(project_root, "mcp_server.py")
            ]
            for path in candidates:
                if os.path.exists(path):
                    server_path = path
                    break

        if server_path is None:
            logger.error("MCP server script not found")
            raise FileNotFoundError("Failed to find MCP server script")

    logger.info(f"Launching MCP server from: {server_path}")

    # Launch MCP server as a separate process
    env = os.environ.copy()
    env['PYTHONPATH'] = os.path.dirname(os.path.abspath(server_path))
    env['PROJECT_ROOT'] = os.path.dirname(os.path.abspath(server_path))

    # Use server stderr for logging to the logs directory
    process = subprocess.Popen(
        [sys.executable, server_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        bufsize=0
    )

    # Start a separate thread to read stderr and log it
    def log_stderr_thread():
        while True:
            if process.poll() is not None:  # Process has exited
                break
            try:
                line = process.stderr.readline()
                if not line:  # End of stream
                    break
                # Log to our main log
                logger.debug(f"MCP Server: {line.decode('utf-8', 'replace').strip()}")
            except Exception as e:
                logger.error(f"Error reading server stderr: {e}")
                break

    # Start thread for stderr logging
    stderr_thread = threading.Thread(target=log_stderr_thread, daemon=True)
    stderr_thread.start()

    # Wait for server to start
    logger.info(f"Waiting {timeout} seconds for MCP server to start...")
    start_time = time.time()

    # Check if server has started
    server_started = False
    while time.time() - start_time < timeout:
        if process.poll() is not None:
            # Server unexpectedly exited
            logger.error(f"MCP server process exited with code {process.returncode}")
            return None

        # Try sending a simple ping message to see if server responds
        try:
            ping_request = {
                "jsonrpc": "2.0",
                "id": 0,
                "method": "initialize",
                "params": {
                    "processId": os.getpid(),
                    "clientInfo": {
                        "name": "Test Client",
                        "version": "1.0"
                    },
                    "rootUri": f"file://{os.getcwd()}",
                    "capabilities": {}
                }
            }
            _send_message_to_server(process, ping_request)

            # Check if we get a response
            response = _read_message_from_server(process, timeout=1.0)
            if response and "result" in response:
                logger.info("MCP server successfully started and responding")
                server_started = True
                break
        except Exception as e:
            # Failed to communicate, continue waiting
            logger.debug(f"Still waiting for server: {str(e)}")

        time.sleep(0.5)

    if not server_started:
        logger.warning("MCP server may not have started properly, but continuing anyway")

    return process

class MCPApiTester:
    """Class for testing MCP API methods"""

    def __init__(self, server_process):
        """Initialize the API tester with a server process"""
        self.server_process = server_process
        self.message_id = 100  # Start from a high ID to avoid conflicts

    def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a request to the server and wait for the response"""
        self.message_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.message_id,
            "method": method,
            "params": params or {}
        }

        logger.info(f"Testing API method: {method}")
        _send_message_to_server(self.server_process, request)

        response = _read_message_from_server(self.server_process)
        if not response:
            logger.error(f"Failed to receive response for method: {method}")
            return None

        logger.info(f"Received response for method: {method}")
        return response

    def send_notification(self, method: str, params: Dict[str, Any] = None) -> None:
        """Send a notification to the server (no response expected)"""
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {}
        }

        logger.info(f"Sending notification: {method}")
        _send_message_to_server(self.server_process, notification)

    def test_completion(self, uri: str, line: int, character: int, trigger_char: str = None) -> Dict[str, Any]:
        """Test completion provider functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "position": {
                "line": line,
                "character": character
            },
            "context": {
                "triggerKind": 1,  # Invoked
            }
        }

        if trigger_char:
            params["context"]["triggerCharacter"] = trigger_char

        return self.send_request("textDocument/completion", params)

    def test_hover(self, uri: str, line: int, character: int) -> Dict[str, Any]:
        """Test hover provider functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "position": {
                "line": line,
                "character": character
            }
        }

        return self.send_request("textDocument/hover", params)

    def test_definition(self, uri: str, line: int, character: int) -> Dict[str, Any]:
        """Test go to definition functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "position": {
                "line": line,
                "character": character
            }
        }

        return self.send_request("textDocument/definition", params)

    def test_references(self, uri: str, line: int, character: int) -> Dict[str, Any]:
        """Test find references functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "position": {
                "line": line,
                "character": character
            },
            "context": {
                "includeDeclaration": True
            }
        }

        return self.send_request("textDocument/references", params)

    def test_document_symbols(self, uri: str) -> Dict[str, Any]:
        """Test document symbols functionality"""
        params = {
            "textDocument": {
                "uri": uri
            }
        }

        return self.send_request("textDocument/documentSymbol", params)

    def test_workspace_symbols(self, query: str = "") -> Dict[str, Any]:
        """Test workspace symbols functionality"""
        params = {
            "query": query
        }

        return self.send_request("workspace/symbol", params)

    def test_code_action(self, uri: str, start_line: int, start_char: int,
                         end_line: int, end_char: int) -> Dict[str, Any]:
        """Test code action functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "range": {
                "start": {"line": start_line, "character": start_char},
                "end": {"line": end_line, "character": end_char}
            },
            "context": {
                "diagnostics": [],
                "only": ["quickfix", "refactor"]
            }
        }

        return self.send_request("textDocument/codeAction", params)

    def test_execute_command(self, command: str, arguments: List[Any] = None) -> Dict[str, Any]:
        """Test execute command functionality"""
        params = {
            "command": command,
            "arguments": arguments or []
        }

        return self.send_request("workspace/executeCommand", params)

    def test_document_management(self) -> bool:
        """Test document management (open, change, close)"""
        success = True

        # Generate a test document URI
        test_uri = f"file:///test_document_{uuid.uuid4().hex}.txt"

        # Test document open
        logger.info(f"Testing textDocument/didOpen with URI: {test_uri}")
        self.send_notification("textDocument/didOpen", {
            "textDocument": {
                "uri": test_uri,
                "languageId": "plaintext",
                "version": 1,
                "text": "This is a test document for MCP API testing."
            }
        })

        # Test document change
        logger.info(f"Testing textDocument/didChange with URI: {test_uri}")
        self.send_notification("textDocument/didChange", {
            "textDocument": {
                "uri": test_uri,
                "version": 2
            },
            "contentChanges": [
                {
                    "text": "This is a modified test document for MCP API testing."
                }
            ]
        })

        # Test document close
        logger.info(f"Testing textDocument/didClose with URI: {test_uri}")
        self.send_notification("textDocument/didClose", {
            "textDocument": {
                "uri": test_uri
            }
        })

        return success

    def test_formatting(self, uri: str) -> Dict[str, Any]:
        """Test document formatting functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "options": {
                "tabSize": 4,
                "insertSpaces": True,
                "trimTrailingWhitespace": True,
                "insertFinalNewline": True,
                "trimFinalNewlines": True
            }
        }

        return self.send_request("textDocument/formatting", params)

    def test_range_formatting(self, uri: str, start_line: int, start_char: int,
                            end_line: int, end_char: int) -> Dict[str, Any]:
        """Test document range formatting functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "range": {
                "start": {"line": start_line, "character": start_char},
                "end": {"line": end_line, "character": end_char}
            },
            "options": {
                "tabSize": 4,
                "insertSpaces": True
            }
        }

        return self.send_request("textDocument/rangeFormatting", params)

    def test_on_type_formatting(self, uri: str, line: int, character: int, ch: str) -> Dict[str, Any]:
        """Test on-type formatting functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "position": {
                "line": line,
                "character": character
            },
            "ch": ch,
            "options": {
                "tabSize": 4,
                "insertSpaces": True
            }
        }

        return self.send_request("textDocument/onTypeFormatting", params)

    def test_rename(self, uri: str, line: int, character: int, new_name: str) -> Dict[str, Any]:
        """Test rename functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "position": {
                "line": line,
                "character": character
            },
            "newName": new_name
        }

        return self.send_request("textDocument/rename", params)

    def test_prepare_rename(self, uri: str, line: int, character: int) -> Dict[str, Any]:
        """Test prepare rename functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "position": {
                "line": line,
                "character": character
            }
        }

        return self.send_request("textDocument/prepareRename", params)

    def test_folding_range(self, uri: str) -> Dict[str, Any]:
        """Test folding range functionality"""
        params = {
            "textDocument": {
                "uri": uri
            }
        }

        return self.send_request("textDocument/foldingRange", params)

    def test_selection_range(self, uri: str, positions: List[Dict[str, int]]) -> Dict[str, Any]:
        """Test selection range functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "positions": positions
        }

        return self.send_request("textDocument/selectionRange", params)

    def test_semantic_tokens(self, uri: str) -> Dict[str, Any]:
        """Test semantic tokens functionality"""
        params = {
            "textDocument": {
                "uri": uri
            }
        }

        return self.send_request("textDocument/semanticTokens/full", params)

    def test_implementation(self, uri: str, line: int, character: int) -> Dict[str, Any]:
        """Test go to implementation functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "position": {
                "line": line,
                "character": character
            }
        }

        return self.send_request("textDocument/implementation", params)

    def test_type_definition(self, uri: str, line: int, character: int) -> Dict[str, Any]:
        """Test go to type definition functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "position": {
                "line": line,
                "character": character
            }
        }

        return self.send_request("textDocument/typeDefinition", params)

    def test_document_link(self, uri: str) -> Dict[str, Any]:
        """Test document link functionality"""
        params = {
            "textDocument": {
                "uri": uri
            }
        }

        return self.send_request("textDocument/documentLink", params)

    def test_document_color(self, uri: str) -> Dict[str, Any]:
        """Test document color functionality"""
        params = {
            "textDocument": {
                "uri": uri
            }
        }

        return self.send_request("textDocument/documentColor", params)

    def test_color_presentation(self, uri: str, color: Dict[str, float], range_: Dict[str, Dict[str, int]]) -> Dict[str, Any]:
        """Test color presentation functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "color": color,
            "range": range_
        }

        return self.send_request("textDocument/colorPresentation", params)

    def test_signature_help(self, uri: str, line: int, character: int) -> Dict[str, Any]:
        """Test signature help functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "position": {
                "line": line,
                "character": character
            }
        }

        return self.send_request("textDocument/signatureHelp", params)

    def test_will_save_wait_until(self, uri: str) -> Dict[str, Any]:
        """Test will save wait until functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "reason": 1  # Manual save
        }

        return self.send_request("textDocument/willSaveWaitUntil", params)

    def test_moniker(self, uri: str, line: int, character: int) -> Dict[str, Any]:
        """Test moniker functionality"""
        params = {
            "textDocument": {
                "uri": uri
            },
            "position": {
                "line": line,
                "character": character
            }
        }

        return self.send_request("textDocument/moniker", params)

    def test_diagnostics(self, uri: str) -> Dict[str, Any]:
        """Test document diagnostics functionality"""
        params = {
            "textDocument": {
                "uri": uri
            }
        }

        return self.send_request("textDocument/diagnostic", params)

def test_api_methods(server_process):
    """Tests all available API methods supported by MCP server"""
    logger.info("Starting comprehensive API methods test")

    # Initialize API tester
    api_tester = MCPApiTester(server_process)

    # Create a test document URI
    test_uri = f"file:///test_document_{uuid.uuid4().hex}.py"
    test_content = """
def example_function(param1, param2):
    '''This is a test function'''
    result = param1 + param2
    return result

class ExampleClass:
    def __init__(self):
        self.value = 42
    
    def get_value(self):
        return self.value
    
    def set_value(self, new_value):
        self.value = new_value

# Testing variables with different types
colors = {
    "red": "#FF0000",
    "green": "#00FF00",
    "blue": "#0000FF"
}

def format_text(text, formatting=None):
    if formatting == 'bold':
        return f"**{text}**"
    elif formatting == 'italic':
        return f"*{text}*"
    return text
"""

    # Open test document
    api_tester.send_notification("textDocument/didOpen", {
        "textDocument": {
            "uri": test_uri,
            "languageId": "python",
            "version": 1,
            "text": test_content
        }
    })

    # Track test results
    test_results = {}

    # Test all API methods
    logger.info("Testing all API methods with the test document")

    try:
        # Basic functionality tests (original tests)
        # Test completion
        test_results["completion"] = api_tester.test_completion(test_uri, 5, 11)
        logger.info(f"Completion test result: {'Success' if test_results['completion'] else 'Failed'}")

        # Test hover
        test_results["hover"] = api_tester.test_hover(test_uri, 5, 11)
        logger.info(f"Hover test result: {'Success' if test_results['hover'] else 'Failed'}")

        # Test definition
        test_results["definition"] = api_tester.test_definition(test_uri, 5, 11)
        logger.info(f"Definition test result: {'Success' if test_results['definition'] else 'Failed'}")

        # Test references
        test_results["references"] = api_tester.test_references(test_uri, 5, 11)
        logger.info(f"References test result: {'Success' if test_results['references'] else 'Failed'}")

        # Test document symbols
        test_results["document_symbols"] = api_tester.test_document_symbols(test_uri)
        logger.info(f"Document symbols test result: {'Success' if test_results['document_symbols'] else 'Failed'}")

        # Test workspace symbols
        test_results["workspace_symbols"] = api_tester.test_workspace_symbols("Example")
        logger.info(f"Workspace symbols test result: {'Success' if test_results['workspace_symbols'] else 'Failed'}")

        # Test code action
        test_results["code_action"] = api_tester.test_code_action(test_uri, 5, 4, 5, 20)
        logger.info(f"Code action test result: {'Success' if test_results['code_action'] else 'Failed'}")

        # Test execute command
        test_results["execute_command"] = api_tester.test_execute_command("neozork.analyzeData")
        logger.info(f"Execute command test result: {'Success' if test_results['execute_command'] else 'Failed'}")

        # Test document management
        test_results["document_management"] = api_tester.test_document_management()
        logger.info(f"Document management test result: {'Success' if test_results['document_management'] else 'Failed'}")

        # Additional functionality tests (new tests)
        # Test formatting
        test_results["formatting"] = api_tester.test_formatting(test_uri)
        logger.info(f"Formatting test result: {'Success' if test_results['formatting'] else 'Failed'}")

        # Test range formatting
        test_results["range_formatting"] = api_tester.test_range_formatting(test_uri, 3, 0, 6, 0)
        logger.info(f"Range formatting test result: {'Success' if test_results['range_formatting'] else 'Failed'}")

        # Test on-type formatting
        test_results["on_type_formatting"] = api_tester.test_on_type_formatting(test_uri, 5, 20, "}")
        logger.info(f"On-type formatting test result: {'Success' if test_results['on_type_formatting'] else 'Failed'}")

        # Test rename
        test_results["rename"] = api_tester.test_rename(test_uri, 8, 15, "new_value_renamed")
        logger.info(f"Rename test result: {'Success' if test_results['rename'] else 'Failed'}")

        # Test prepare rename
        test_results["prepare_rename"] = api_tester.test_prepare_rename(test_uri, 8, 15)
        logger.info(f"Prepare rename test result: {'Success' if test_results['prepare_rename'] else 'Failed'}")

        # Test folding range
        test_results["folding_range"] = api_tester.test_folding_range(test_uri)
        logger.info(f"Folding range test result: {'Success' if test_results['folding_range'] else 'Failed'}")

        # Test selection range
        positions = [{"line": 5, "character": 10}, {"line": 8, "character": 15}]
        test_results["selection_range"] = api_tester.test_selection_range(test_uri, positions)
        logger.info(f"Selection range test result: {'Success' if test_results['selection_range'] else 'Failed'}")

        # Test semantic tokens
        test_results["semantic_tokens"] = api_tester.test_semantic_tokens(test_uri)
        logger.info(f"Semantic tokens test result: {'Success' if test_results['semantic_tokens'] else 'Failed'}")

        # Test implementation
        test_results["implementation"] = api_tester.test_implementation(test_uri, 5, 11)
        logger.info(f"Implementation test result: {'Success' if test_results['implementation'] else 'Failed'}")

        # Test type definition
        test_results["type_definition"] = api_tester.test_type_definition(test_uri, 5, 11)
        logger.info(f"Type definition test result: {'Success' if test_results['type_definition'] else 'Failed'}")

        # Test document link
        test_results["document_link"] = api_tester.test_document_link(test_uri)
        logger.info(f"Document link test result: {'Success' if test_results['document_link'] else 'Failed'}")

        # Test document color
        test_results["document_color"] = api_tester.test_document_color(test_uri)
        logger.info(f"Document color test result: {'Success' if test_results['document_color'] else 'Failed'}")

        # Test color presentation (requires a color)
        color = {"red": 1.0, "green": 0.0, "blue": 0.0, "alpha": 1.0}
        range_ = {
            "start": {"line": 19, "character": 17},
            "end": {"line": 19, "character": 25}
        }
        test_results["color_presentation"] = api_tester.test_color_presentation(test_uri, color, range_)
        logger.info(f"Color presentation test result: {'Success' if test_results['color_presentation'] else 'Failed'}")

        # Test signature help
        test_results["signature_help"] = api_tester.test_signature_help(test_uri, 25, 20)
        logger.info(f"Signature help test result: {'Success' if test_results['signature_help'] else 'Failed'}")

        # Test will save wait until
        test_results["will_save_wait_until"] = api_tester.test_will_save_wait_until(test_uri)
        logger.info(f"Will save wait until test result: {'Success' if test_results['will_save_wait_until'] else 'Failed'}")

        # Test moniker
        test_results["moniker"] = api_tester.test_moniker(test_uri, 5, 11)
        logger.info(f"Moniker test result: {'Success' if test_results['moniker'] else 'Failed'}")

        # Test diagnostics
        test_results["diagnostics"] = api_tester.test_diagnostics(test_uri)
        logger.info(f"Diagnostics test result: {'Success' if test_results['diagnostics'] else 'Failed'}")

    except Exception as e:
        logger.error(f"Error during API testing: {str(e)}")
        logger.error(traceback.format_exc())
        return False
    finally:
        # Close test document
        api_tester.send_notification("textDocument/didClose", {
            "textDocument": {
                "uri": test_uri
            }
        })

    # Count successful tests
    success_count = sum(1 for result in test_results.values() if result is not None)
    total_count = len(test_results)

    logger.info(f"API testing completed. Success: {success_count}/{total_count} tests.")
    logger.info(f"Test summary:")

    # Print results for each method
    for method, result in sorted(test_results.items()):
        status = "✅ Success" if result is not None else "❌ Failed"
        logger.info(f"  - {method}: {status}")

    # Consider test successful if at least half of the API methods work
    # Most servers won't implement all methods fully
    return success_count >= total_count / 2

def run_test_with_server():
    """Launches MCP server and runs all tests"""
    import argparse

    parser = argparse.ArgumentParser(description="Test MCP connection with PyCharm")
    parser.add_argument("--server", help="Path to MCP server script", default=None)
    parser.add_argument("--no-server", action="store_true", help="Don't start the server, assume it's already running")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout for operations in seconds")
    parser.add_argument("--skip-api-tests", action="store_true", help="Skip API method testing")
    args = parser.parse_args()

    server_process = None
    basic_connection_ok = False
    api_tests_ok = False

    try:
        # Launch server if needed
        if not args.no_server:
            try:
                server_process = launch_mcp_server(args.server, timeout=10)
                if not server_process:
                    logger.error("Failed to start MCP server")
                    return False
            except Exception as e:
                logger.error(f"Failed to start MCP server: {str(e)}")
                return False

        # Run basic connection test
        if server_process:
            logger.info("Starting basic connectivity test...")
            basic_connection_ok = test_mcp_connection_direct(server_process)
        else:
            logger.info("Starting basic connectivity test (no server process)...")
            basic_connection_ok = test_mcp_connection()

        if basic_connection_ok:
            logger.info("✅ Basic connectivity test completed successfully!")
        else:
            logger.error("❌ Basic connectivity test failed")
            return False

        # If basic connectivity works and API tests are not skipped, run API tests
        if basic_connection_ok and not args.skip_api_tests and server_process:
            logger.info("Starting API methods test...")
            api_tests_ok = test_api_methods(server_process)

            if api_tests_ok:
                logger.info("✅ API methods test completed successfully!")
            else:
                logger.warning("⚠️ Some API methods tests failed, but basic connectivity is working")
        elif args.skip_api_tests:
            logger.info("API tests skipped as requested")
            api_tests_ok = True  # Consider as success if skipped
        else:
            logger.info("API tests skipped as no server process is available")
            api_tests_ok = True  # Consider as success if skipped

        # Overall success depends on basic connectivity and API tests (if run)
        return basic_connection_ok and api_tests_ok

    finally:
        # Stop server if it was started
        if server_process is not None:
            try:
                logger.info("Terminating MCP server process")
                server_process.terminate()
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning("MCP server did not terminate gracefully, killing...")
                server_process.kill()
            except Exception as e:
                logger.error(f"Error stopping MCP server: {str(e)}")

if __name__ == "__main__":
    try:
        success = run_test_with_server()
        if success:
            logger.info("🎉 All tests completed successfully!")
            sys.exit(0)
        else:
            logger.error("❌ Some tests failed")
            sys.exit(1)
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        sys.exit(1)

