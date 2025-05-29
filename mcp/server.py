#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server for GitHub Copilot connection
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
import datetime

from mcp.logger import setup_logger
from mcp.handler import RequestHandler
from mcp.utils import SimpleMCPUtils

# Define maximum response delay to prevent buffer issues
MAX_RESPONSE_DELAY = 0.0  # No delay for maximum responsiveness

class SimpleMCPServer:
    """
    Simple MCP server for successful GitHub Copilot connection via stdio
    """

    def __init__(self):
        # Setup logger
        self.logger = logging.getLogger("simple_mcp")

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

        # Display start message
        self.project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

        # Create handler for requests
        self.handler = RequestHandler(self)
        # Create utils for helper methods
        self.utils = SimpleMCPUtils(self)

        # Show initial client info
        self._print_client_info()

    def display_start_message(self):
        """
        Displays a message when the server starts
        """
        print("\n" + "=" * 60)
        print("🚀 MCP SERVER STARTED")
        print("=" * 60 + "\n")
        return

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

        self.logger.info("Waiting for GitHub Copilot connection...")
        self.logger.info("Ready to receive input from stdin")

        # Main processing loop
        while True:
            # Read data from stdin
            try:
                # Announce that we're waiting for input
                if len(self.buffer) == 0:
                    self.logger.debug("Waiting for input on stdin...")

                data = sys.stdin.buffer.read1(4096)
                if not data:
                    self.logger.info("End of stdin stream, exiting")
                    break

                self.buffer += data

                # Improved logging for connection tracking
                self.logger.info(f"📥 Received data from client: {len(data)} bytes")

                # Output information about received data in readable format
                data_preview = str(data)
                if len(data_preview) > 200:
                    data_preview = data_preview[:200] + "... (truncated)"

                self.logger.info(f"📥 Received {len(data)} bytes, buffer size: {len(self.buffer)}")
                # Detect if data is too large for console
                try:
                    decoded_data = data.decode('utf-8', errors='replace')
                    self.logger.info(f"RAW INPUT [{len(data)} bytes]: {decoded_data[:300]}{'...' if len(decoded_data) > 300 else ''}")
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
                self.logger.debug(f"[BUFFER] Buffer empty. content_length={self.content_length}")
                break

            # Log buffer state before processing
            self.logger.debug(f"[BUFFER] Start loop: buffer size={len(self.buffer)}, content_length={self.content_length}")
            try:
                buffer_text = self.buffer.decode('utf-8', errors='replace')
                self.logger.debug(f"[BUFFER] Buffer as text (first 100 chars): {buffer_text[:100]}{'...' if len(buffer_text) > 100 else ''}")
            except Exception as e:
                self.logger.debug(f"Impossible decode buffer as text: {e}")

            # Check for HTTP-style headers with Content-Length
            if self.content_length is None:
                header_end = -1

                # Check for standard LSP header separator
                if b"\r\n\r\n" in self.buffer:
                    header_end = self.buffer.find(b"\r\n\r\n") + 4
                # Alternatively, check for simplified header separator
                elif b"\n\n" in self.buffer:
                    header_end = self.buffer.find(b"\n\n") + 2
                # Check for single Content-Length header with just \r\n
                elif b"Content-Length: " in self.buffer and b"\r\n" in self.buffer:
                    cl_start = self.buffer.find(b"Content-Length: ") + len(b"Content-Length: ")
                    cl_end = self.buffer.find(b"\r\n", cl_start)

                    if cl_end > cl_start:
                        try:
                            self.content_length = int(self.buffer[cl_start:cl_end].decode('utf-8').strip())
                            self.logger.debug(f"Found Content-Length: {self.content_length}")
                            # Skip headers and proceed to content
                            self.buffer = self.buffer[cl_end + 2:]  # +2 for \r\n
                            continue  # Continue to content processing
                        except (ValueError, UnicodeDecodeError) as e:
                            self.logger.debug(f"Failed to parse Content-Length: {str(e)}")

                # Check for JSON content without headers
                elif self.buffer.startswith(b"{") and b"}" in self.buffer:
                    # Try to find a complete JSON object
                    try:
                        # Check for a newline-terminated JSON message
                        if b"\n" in self.buffer:
                            newline_pos = self.buffer.find(b"\n")
                            json_data = self.buffer[:newline_pos].strip()
                            if json_data.startswith(b"{") and json_data.endswith(b"}"):
                                try:
                                    request = json.loads(json_data.decode('utf-8'))
                                    self.logger.debug(f"Found JSON message without headers")

                                    response = self.handler.handle_request(request)

                                    # Send response if available
                                    if response:
                                        self._send_response(response)

                                    # Remove processed message from buffer
                                    self.buffer = self.buffer[newline_pos + 1:]
                                    continue
                                except (json.JSONDecodeError, UnicodeError) as e:
                                    self.logger.debug(f"JSON parse error: {str(e)}")
                    except Exception as e:
                        self.logger.debug(f"Error processing potential JSON message: {str(e)}")

                # If headers found, parse them
                if header_end > 0:
                    headers_text = self.buffer[:header_end-4 if b"\r\n\r\n" in self.buffer else header_end-2].decode('utf-8', errors='replace')

                    # Extract Content-Length
                    for line in headers_text.split("\r\n" if "\r\n" in headers_text else "\n"):
                        if line.lower().startswith("content-length:"):
                            try:
                                self.content_length = int(line.split(":", 1)[1].strip())
                                self.logger.debug(f"Found Content-Length in headers: {self.content_length}")
                                break
                            except ValueError as e:
                                self.logger.warning(f"Invalid Content-Length value: {line}")

                    # Remove headers from buffer
                    self.buffer = self.buffer[header_end:]
                    self.logger.debug(f"Removed headers, remaining buffer size: {len(self.buffer)}")
                else:
                    # No complete headers found, wait for more data
                    self.logger.debug("No complete headers found, waiting for more data")
                    break

            # Process content if we have a content length and enough data
            if self.content_length is not None and len(self.buffer) >= self.content_length:
                message_data = self.buffer[:self.content_length]
                self.buffer = self.buffer[self.content_length:]
                self.logger.debug(f"[BUFFER] Extracted message of {self.content_length} bytes, {len(self.buffer)} bytes remaining")

                try:
                    message_text = message_data.decode('utf-8')
                    message = json.loads(message_text)

                    # Process the message
                    self.logger.debug(f"[BUFFER] Processing message: {message_text[:100]}{'...' if len(message_text) > 100 else ''}")
                    response = self.handler.handle_request(message)

                    # Send response if available
                    if response:
                        self._send_response(response)

                    # Reset content_length for next message
                    self.content_length = None
                    self.logger.debug(f"[BUFFER] content_length reset to None after processing message")
                except json.JSONDecodeError as e:
                    self.logger.error(f"JSON parse error: {str(e)}, message: {message_data[:100]}...")
                    # Попытка отправить error-ответ, если возможно
                    try:
                        msg_id = message.get("id", 0) if 'message' in locals() and isinstance(message, dict) else 0
                        self._send_error(msg_id, -32700, f"Parse error: {str(e)}")
                    except Exception:
                        pass
                    self.content_length = None
                except UnicodeError as e:
                    self.logger.error(f"Unicode decode error: {str(e)}")
                    self.content_length = None
                except Exception as e:
                    self.logger.error(f"Error processing message: {str(e)}")
                    self.logger.error(traceback.format_exc())
                    # Попытка отправить error-ответ, если возможно
                    try:
                        msg_id = message.get("id", 0) if 'message' in locals() and isinstance(message, dict) else 0
                        self._send_error(msg_id, -32001, f"Internal server error: {str(e)}")
                    except Exception:
                        pass
                    self.content_length = None
            else:
                # Not enough data for a complete message
                if self.content_length is not None:
                    self.logger.debug(f"[BUFFER] Waiting for more data. Have {len(self.buffer)}, need {self.content_length}")
                break

        # After processing, reset content_length
        self.logger.debug(f"[BUFFER] End of _process_buffer: buffer size={len(self.buffer)}, content_length={self.content_length}")

    def _send_response(self, response: Dict[str, Any]) -> None:
        """
        Sending response via stdout
        """
        if not response:
            return

        # Disable all delays for GitHub Copilot response
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
            self.logger.info(f"RESPONSE for ID {response_id}: {self.utils.simplify_response(response)}")
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
            self.logger.info(f"⚡ NEW CONNECTION from {client_name} v{client_version}")
        elif status == "disconnected":
            if client_key in self.active_clients:
                self.active_clients[client_key]["status"] = "disconnected"
                self.active_clients[client_key]["disconnected_at"] = time.time()
                # Display disconnection message
                self.logger.info(f"❌ DISCONNECTED: {client_name} v{client_version}")

        # Print updated client information
        self._print_client_info()

    def _print_client_info(self):
        """
        Print information about active clients
        """
        self.logger.info(f"Active clients: {len(self.active_clients)}")

        for client_key, client_data in self.client_info.items():
            self.logger.info(f"Client: {client_key}, Info: {json.dumps(client_data, indent=2)}")

    def shutdown_gracefully(self):
        """
        Gracefully shut down the server, show statistics
        """
        # Display a noticeable message about server shutdown
        print("\n" + "=" * 60)
        print("✅ MCP SERVER SUCCESSFULLY STOPPED")
        print("=" * 60 + "\n")

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
