#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testing MCP connection with PyCharm
This script helps to verify the compatibility of MCP server with PyCharm
"""

import sys
import os
import json
import subprocess
import time
import logging
from typing import Dict, Any

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(logs_dir):
    try:
        os.makedirs(logs_dir)
        print(f"Created logs directory: {logs_dir}")
    except Exception as e:
        print(f"Error creating logs directory: {e}")

# Logging setup
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

    # Form message with headers
    header = f"Content-Length: {len(message_bytes)}\r\n\r\n".encode('utf-8')

    sys.stdout.buffer.write(header)
    sys.stdout.buffer.write(message_bytes)
    sys.stdout.buffer.flush()

    logger.debug(f"Sent message: {message_str}")

def read_message(timeout=5.0):
    """Reads a message from stdin in LSP format with timeout"""
    # Reading headers
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

        # Add to buffer and look for end of headers marker
        buffer += line

        # Support both standard delimiter \r\n\r\n and PyCharm-style \n\n
        if b'\r\n\r\n' in buffer:
            headers, buffer = buffer.split(b'\r\n\r\n', 1)
            break
        elif b'\n\n' in buffer:
            headers, buffer = buffer.split(b'\n\n', 1)
            break

        # Check Content-Length header in current line
        try:
            header = line.decode('utf-8').strip()
            if header.lower().startswith('content-length:'):
                content_length = int(header.split(':', 1)[1].strip())
                logger.debug(f"Found Content-Length: {content_length}")
        except Exception as e:
            logger.warning(f"Error parsing header: {e}")

    # If after header delimiter there's already data, consider it the beginning of the body
    body = buffer

    # If Content-Length not found, return error
    if content_length is None:
        logger.error("Content-Length header not found")
        return None

    # Read remaining part of body
    remaining = content_length - len(body)
    if remaining > 0:
        logger.debug(f"Reading remaining {remaining} bytes of message body")

        # Reading remaining data with timeout
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

    # 4. Wait for any notification from server (optional)
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
    """Tests connection with MCP server through direct stream connection"""
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

    # 4. Wait for any notification from server (optional)
    try:
        # Set short timeout, as server may not send notifications
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

    # Form message with headers
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
    # Reading headers
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

        # Read line completely to find headers
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

        # Check Content-Length header in current line
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

    # If Content-Length not found, try searching in buffer
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

    # If Content-Length still not found, another attempt - search directly in binary buffer
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

    # If Content-Length still not found, return error
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
        # If end of headers not found, consider all read data as headers
        body = b""
        logger.debug("No body found in buffer yet")

    # Read remaining part of message body
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
        # Try to find server automatically
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

    # Create temporary log file in logs directory
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
    if not os.path.exists(logs_dir):
        try:
            os.makedirs(logs_dir)
            logger.info(f"Created logs directory: {logs_dir}")
        except Exception as e:
            logger.warning(f"Error creating logs directory: {e}")

    log_file = os.path.join(logs_dir, "mcp_server_test.log")

    with open(log_file, 'w') as f:
        f.write(f"MCP Server Test Log - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Launch server with stderr redirected to log file
    with open(log_file, 'a') as stderr_file:
        process = subprocess.Popen(
            [sys.executable, server_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=stderr_file,
            env=env,
            bufsize=0
        )

    # Wait some time for server to start
    logger.info(f"Waiting {timeout} seconds for MCP server to start...")
    start_time = time.time()

    # Check log file for signs of successful start
    while time.time() - start_time < timeout:
        if process.poll() is not None:
            # Server unexpectedly exited
            logger.error(f"MCP server process exited with code {process.returncode}")
            with open(log_file, 'r') as f:
                log_content = f.read()
                logger.error(f"Server log: {log_content}")
            raise RuntimeError(f"MCP server failed to start, exit code: {process.returncode}")

        # Check log for signs of successful start
        try:
            with open(log_file, 'r') as f:
                log_content = f.read()
                if "MCP Server started" in log_content or "initialized" in log_content.lower():
                    logger.info("MCP server successfully started")
                    break
        except Exception as e:
            logger.warning(f"Error reading log file: {str(e)}")

        time.sleep(0.1)

    return process, log_file

def run_test_with_server():
    """Runs test with automatic server launch"""
    import argparse

    parser = argparse.ArgumentParser(description="Test MCP connection with PyCharm")
    parser.add_argument("--server", help="Path to MCP server script", default=None)
    parser.add_argument("--no-server", action="store_true", help="Don't start the server, assume it's already running")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout for operations in seconds")
    args = parser.parse_args()

    server_process = None

    try:
        # Launch server if needed
        if not args.no_server:
            try:
                server_process, log_file = launch_mcp_server(args.server, timeout=10)
            except Exception as e:
                logger.error(f"Failed to start MCP server: {str(e)}")
                return False

        # Run test
        if server_process:
            result = test_mcp_connection_direct(server_process)
        else:
            result = test_mcp_connection()

        if result:
            logger.info("✅ Test completed successfully!")
        else:
            logger.error("❌ Test failed")

        return result

    finally:
        # Stop server if it was launched
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
        run_test_with_server()
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        sys.exit(1)
