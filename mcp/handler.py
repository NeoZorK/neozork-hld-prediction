#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Request handler for MCP Server
"""

import json
import time
import logging
from typing import Dict, Any, Optional

class RequestHandler:
    """
    Handler for processing client requests
    """

    def __init__(self, server):
        """
        Initialize the request handler
        """
        self.server = server
        self.logger = logging.getLogger("simple_mcp")

    def handle_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Processing requests from GitHub Copilot
        """
        if not request:
            return {}

        self.server.request_count += 1
        current_time = time.time()
        uptime = current_time - self.server.start_time

        # Display request details on screen
        request_method = request.get("method", "unknown")
        request_id = request.get("id", "notification")
        request_params = request.get("params", {})
        simplified_params = self.server.utils.simplify_params(request_params)

        self.logger.info(f"REQUEST #{self.server.request_count}: {request_method} (ID: {request_id})")
        self.logger.info(f"PARAMS: {simplified_params}")

        # Check if this is a notification (without ID)
        if "id" not in request:
            method = request.get("method", "")
            self.logger.info(f"Received notification: {method} [req #{self.server.request_count}, uptime: {int(uptime)}s]")
            self.logger.debug(f"Full notification: {json.dumps(request)}")

            # Process some notifications
            if method == "textDocument/didOpen":
                params = request.get("params", {})
                text_document = params.get("textDocument", {})
                uri = text_document.get("uri", "")
                if uri:
                    self.server.documents[uri] = text_document.get("text", "")
                    language_id = text_document.get("languageId", "unknown")
                    self.logger.info(f"Document opened: {uri} (Language: {language_id}, Size: {len(self.server.documents[uri])} chars)")

            elif method == "textDocument/didChange":
                params = request.get("params", {})
                text_document = params.get("textDocument", {})
                uri = text_document.get("uri", "")
                changes = params.get("contentChanges", [])
                if uri and uri in self.server.documents and changes:
                    # Simple document update (does not account for change positions)
                    old_size = len(self.server.documents[uri])
                    self.server.documents[uri] = changes[-1].get("text", self.server.documents[uri])
                    new_size = len(self.server.documents[uri])
                    change_size = new_size - old_size
                    self.logger.info(f"Document changed: {uri} (Size delta: {'+' if change_size >= 0 else ''}{change_size} chars)")

            elif method == "textDocument/didClose":
                params = request.get("params", {})
                text_document = params.get("textDocument", {})
                uri = text_document.get("uri", "")
                if uri and uri in self.server.documents:
                    self.logger.info(f"Document closed: {uri} (Final size: {len(self.server.documents[uri])} chars)")
                    del self.server.documents[uri]

            # New case for initialized notification to fix connection problems
            elif method == "initialized":
                # Connection success is now counted upon sending the 'initialize' response.
                # This notification from the client confirms it has also initialized.
                self.logger.info(f"Received 'initialized' notification. Client is ready. (Current successful connections: {self.server.successful_connections}, Attempts: {self.server.connection_attempts})")
                # Note: self.successful_connections is no longer incremented here.

                # Send ready notification
                self.server._send_notification("window/showMessage", {
                    "type": 3,  # Info
                    "message": f"MCP Server is ready and connected (Connection #{self.server.successful_connections})"
                })

                # Send server ready notification
                self.server._send_notification("$/neozork/serverReady", {
                    "status": "ready",
                    "features": ["completion", "hover", "definition"]
                })

            # For notifications, we don't send a response
            return None

        method = request.get("method", "")
        message_id = request.get("id", 0)

        self.logger.info(f"Received request: {method} (ID: {message_id}) [req #{self.server.request_count}, uptime: {int(uptime)}s]")
        self.logger.debug(f"Full request: {json.dumps(request)}")

        # Standard response to initialize
        if method == "initialize":
            self.server.connection_attempts += 1
            params = request.get("params", {})
            client_info = params.get("clientInfo", {})
            client_name = client_info.get("name", "Unknown Client")
            client_version = client_info.get("version", "Unknown Version")
            protocol_version = params.get("protocolVersion", "Unknown")

            # Save client and protocol information
            client_key = f"{client_name}_{client_version}"
            self.server.client_info[client_key] = {
                "name": client_name,
                "version": client_version,
                "last_connection": time.time(),
                "protocol": protocol_version,
                "capabilities": params.get("capabilities", {})
            }
            self.server.protocol_versions.add(protocol_version)

            self.logger.info(f"🔌 CONNECTION ATTEMPT #{self.server.connection_attempts} from {client_name} v{client_version}")
            self.logger.info(f"Protocol version: {protocol_version}")
            self.logger.info(f"Client capabilities: {json.dumps(params.get('capabilities', {}), indent=2)}")

            self.server._update_client_list(client_name, client_version, status="connected")

            # Mark connection as successful after server processes 'initialize' and sends response.
            if self.server.active_clients.get(client_key) and \
               not self.server.active_clients[client_key].get('initialization_counted_successful', False):
                self.server.successful_connections += 1
                self.server.active_clients[client_key]['initialization_counted_successful'] = True
                self.logger.info(f"✅ Connection marked SUCCESSFUL after 'initialize' response for {client_key}. Total successful: {self.server.successful_connections}, Attempts: {self.server.connection_attempts}")
            elif self.server.active_clients.get(client_key) and self.server.active_clients[client_key].get('initialization_counted_successful', False):
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
            self.logger.info(f"🤖 COPILOT REQUEST: {method} (ID: {message_id})")

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
                                "text": "# Placeholder completion from NeozorkMCP",
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
            self.logger.info(f"Connection stats: {self.server.successful_connections} successful connections out of {self.server.connection_attempts} attempts")
            self.logger.info(f"Processed {self.server.request_count} requests")
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }

        # Response to exit
        elif method == "exit":
            self.logger.info(f"Received exit request after {int(uptime)}s uptime")
            self.logger.info(f"Final stats: {self.server.successful_connections}/{self.server.connection_attempts} connections, {self.server.request_count} requests processed")

            # Send response before exiting
            response = {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }
            self.server._send_response(response)
            # Terminate program
            self.server.shutdown_gracefully()
            import sys
            sys.exit(0)

        # Add default response for unknown requests
        else:
            self.logger.warning(f"Received unknown request method: {method}")
            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None
            }
