#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Request handler for MCP Server
"""

import json
import time
import logging
import os
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
        try:
            # Explicit logging of all incoming requests (including notifications)
            self.logger.debug(f"handle_request called with: {json.dumps(request)}")
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

                # New notification for workspace/didChangeWatchedFiles
                elif method == "workspace/didChangeWatchedFiles":
                    params = request.get("params", {})
                    changes = params.get("changes", [])
                    for change in changes:
                        uri = change.get("uri", "")
                        change_type = change.get("type", 0)
                        change_type_str = {1: "Created", 2: "Changed", 3: "Deleted"}.get(change_type, "Unknown")
                        self.logger.info(f"File {change_type_str}: {uri}")

                # New notification for workspace/didChangeConfiguration
                elif method == "workspace/didChangeConfiguration":
                    self.logger.info("Configuration changed, updating settings")
                    params = request.get("params", {})
                    settings = params.get("settings", {})
                    self.server.settings = settings
                    self.logger.debug(f"New settings: {json.dumps(settings)}")

                # LSP keepalive/heartbeat and $/ping/$/heartbeat support
                if method in ["$/heartbeat", "$/ping"]:
                    self.logger.info(f"Received keepalive notification: {method}")
                    return None

                # Logging all notifications (INFO)
                self.logger.info(f"Notification: {request.get('method', '')} {json.dumps(request)}")

                # For notifications, we don't send a response
                return None

            # Check: if workspace/didChangeConfiguration came as a request (with id), return response
            if request.get("method") == "workspace/didChangeConfiguration" and "id" in request:
                self.logger.info("workspace/didChangeConfiguration came as request, returning result: None")
                return {
                    "jsonrpc": "2.0",
                    "id": request["id"],
                    "result": None
                }

            # Check for repeated initialize
            if request.get("method") == "initialize" and self.server.successful_connections > 0:
                self.logger.warning("Repeated initialize received without shutdown/exit. Ignoring state reset.")

            # Validation of incoming messages
            if not request.get("jsonrpc") or not request.get("method"):
                self.logger.error("Invalid LSP message: missing 'jsonrpc' or 'method'")
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id", 0),
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request: missing 'jsonrpc' or 'method'"
                    }
                }

            method = request.get("method", "")
            message_id = request.get("id", 0)

            self.logger.info(f"Received request: {method} (ID: {message_id}) [req #{self.server.request_count}, uptime: {int(uptime)}s]")
            self.logger.debug(f"Full request: {json.dumps(request)}")

            # Logging request processing time
            start_time = time.time()

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

                response = {
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
                            },
                            # Adding file system support
                            "workspace": {
                                "fileOperations": {
                                    "didCreate": {"filters": [{"scheme": "file", "pattern": "**/*"}]},
                                    "didRename": {"filters": [{"scheme": "file", "pattern": "**/*"}]},
                                    "didDelete": {"filters": [{"scheme": "file", "pattern": "**/*"}]}
                                }
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
                params = request.get("params", {})
                text_document = params.get("textDocument", {})
                position = params.get("position", {})
                uri = text_document.get("uri", "")

                # Get document content if available
                document_content = self.server.documents.get(uri, "")

                # Generate real completions based on document content
                completions = self._generate_completions(document_content, position)

                response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": {
                        "isIncomplete": False,
                        "items": completions
                    }
                }

            # Response to textDocument/hover
            elif method == "textDocument/hover":
                self.logger.info(f"Received hover request (ID: {message_id})")
                params = request.get("params", {})
                position = params.get("position", {})
                text_document = params.get("textDocument", {})
                uri = text_document.get("uri", "")

                # Extract word under cursor
                hover_info = self._generate_hover_info(uri, position)

                response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": {
                        "contents": {
                            "kind": "markdown",
                            "value": hover_info
                        }
                    }
                }

            # Response to textDocument/definition
            elif method == "textDocument/definition":
                self.logger.info(f"Received definition request (ID: {message_id})")
                params = request.get("params", {})
                text_document = params.get("textDocument", {})
                position = params.get("position", {})
                uri = text_document.get("uri", "")

                # Implementation of definition search
                definitions = self._find_definitions(uri, position)

                response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": definitions  # Return found definitions
                }

            # New handler for workspace/symbol
            elif method == "workspace/symbol":
                self.logger.info(f"Received workspace symbol request (ID: {message_id})")
                params = request.get("params", {})
                query = params.get("query", "")

                # Search for symbols in the workspace
                symbols = self._find_workspace_symbols(query)

                response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": symbols
                }

            # New handler for textDocument/documentSymbol
            elif method == "textDocument/documentSymbol":
                self.logger.info(f"Received document symbol request (ID: {message_id})")
                params = request.get("params", {})
                text_document = params.get("textDocument", {})
                uri = text_document.get("uri", "")

                # Search for symbols in the document
                symbols = self._find_document_symbols(uri)

                response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": symbols
                }

            # New handler for workspace/executeCommand
            elif method == "workspace/executeCommand":
                self.logger.info(f"Received execute command request (ID: {message_id})")
                params = request.get("params", {})
                command = params.get("command", "")
                arguments = params.get("arguments", [])

                # Execute command
                result = self._execute_command(command, arguments)

                response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": result
                }

            # New handler for textDocument/references
            elif method == "textDocument/references":
                self.logger.info(f"Received references request (ID: {message_id})")
                params = request.get("params", {})
                text_document = params.get("textDocument", {})
                position = params.get("position", {})
                uri = text_document.get("uri", "")

                # Search for references
                references = self._find_references(uri, position)

                response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": references
                }

            # New handler for workspace/willCreateFiles
            elif method == "workspace/willCreateFiles":
                self.logger.info(f"Received will create files request (ID: {message_id})")

                response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": None  # No changes
                }

            # New handler for workspace/willRenameFiles
            elif method == "workspace/willRenameFiles":
                self.logger.info(f"Received will rename files request (ID: {message_id})")

                response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": None  # No changes
                }

            # New handler for workspace/willDeleteFiles
            elif method == "workspace/willDeleteFiles":
                self.logger.info(f"Received will delete files request (ID: {message_id})")

                response = {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": None  # No changes
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
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "result": {
                            "status": "Success",
                            "user": "NeozorkMCPUser"
                        }
                    }
                elif method == "copilot/getCompletions" or method == "getCompletions":
                    # Query for completions
                    params = request.get("params", {})
                    doc_uri = params.get("doc", {}).get("uri", "")
                    position = params.get("position", {})
                    self.logger.info(f"Query for Copilot completions in {doc_uri} at position {position}")

                    # Get document content if available
                    document_content = ""
                    if doc_uri and doc_uri in self.server.documents:
                        document_content = self.server.documents[doc_uri]

                    # Generate more meaningful completions for Copilot
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "result": {
                            "completions": [
                                {
                                    "text": "# Generated by NeozorkMCP\ndef process_data(data):\n    \"\"\"Process the input data and return results\"\"\"\n    results = []\n    for item in data:\n        if isinstance(item, dict):\n            results.append(item.get('value', 0))\n    return results",
                                    "displayText": "def process_data(data): ...",
                                    "position": position
                                },
                                {
                                    "text": "# Helper function\ndef analyze_results(results):\n    \"\"\"Analyze processing results\"\"\"\n    if not results:\n        return None\n    return {\n        'mean': sum(results) / len(results),\n        'max': max(results),\n        'min': min(results)\n    }",
                                    "displayText": "def analyze_results(results): ...",
                                    "position": position
                                }
                            ]
                        }
                    }
                elif method == "copilot/getCompletionsCycling":
                    self.logger.info("Query for Copilot completions cycling")
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "result": {
                            "completions": [
                                {
                                    "text": "# Option 1\ndef option_one():\n    print('This is option one')\n    return 1",
                                    "displayText": "Option 1: def option_one()",
                                    "position": {"line": 0, "character": 0}
                                },
                                {
                                    "text": "# Option 2\ndef option_two():\n    print('This is option two')\n    return 2",
                                    "displayText": "Option 2: def option_two()",
                                    "position": {"line": 0, "character": 0}
                                }
                            ]
                        }
                    }
                elif method == "copilot/updateCompletionTracker":
                    self.logger.info("Updating Copilot completion tracker")
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "result": {
                            "status": "Success",
                            "action": "Updated"
                        }
                    }
                elif method == "copilot/tokenize":
                    self.logger.info("Copilot tokenize request")
                    params = request.get("params", {})
                    text = params.get("text", "")
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "result": {
                            "tokens": text.split()  # Simple tokenization by spaces
                        }
                    }
                elif method == "copilot/getCaptionContext":
                    self.logger.info("Copilot caption context request")
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "result": {
                            "context": {
                                "repo": "neozork-hld-prediction",
                                "file": "current_file.py",
                                "functions": ["analyze_data", "process_results"]
                            }
                        }
                    }

                # Query for other Copilot features
                response = {
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
                response = {
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

            # Dynamic log level change via workspace/didChangeConfiguration
            if request.get("method") == "workspace/didChangeConfiguration":
                params = request.get("params", {})
                settings = params.get("settings", {})
                if isinstance(settings, dict) and settings.get("debug") is True:
                    self.logger.setLevel(logging.DEBUG)
                    self.logger.info("Log level set to DEBUG by client config")
                elif isinstance(settings, dict) and settings.get("debug") is False:
                    self.logger.setLevel(logging.INFO)
                    self.logger.info("Log level set to INFO by client config")

            # Logging and handling $/cancelRequest
            if request.get("method") == "$/cancelRequest":
                self.logger.info(f"Received $/cancelRequest: {json.dumps(request)}")
                return None

            # Logging and handling large messages
            if len(json.dumps(request)) > 10000:
                self.logger.warning(f"Large message received: {len(json.dumps(request))} bytes")

            # Add default response for unknown requests
            if response is None and request.get("id") is not None:
                self.logger.warning(f"Unknown method: {request.get('method', '')}")
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id", 0),
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {request.get('method', '')}"
                    }
                }

            # Logging request processing time
            end_time = time.time()
            self.logger.info(f"Request {request.get('method', '')} processed in {end_time - start_time:.4f} sec")
            return response
        except Exception as e:
            import traceback
            self.logger.error(f"Exception in handle_request: {e}")
            self.logger.error(traceback.format_exc())
            return {
                "jsonrpc": "2.0",
                "id": request.get("id", 0),
                "error": {
                    "code": -32001,
                    "message": f"Internal server error: {str(e)}"
                }
            }

    def _generate_completions(self, document_content, position):
        """
        Generate completions based on document content and cursor position
        """
        line = position.get("line", 0)
        character = position.get("character", 0)

        # Split document content into lines
        lines = document_content.split("\n") if document_content else []

        # Basic completions
        completions = [
            {
                "label": "Simple placeholder completion",
                "kind": 1,  # Text
                "detail": "NeoZork MCP Server placeholder completion",
                "documentation": "This is a placeholder completion from the simple MCP server",
                "insertText": "placeholder_completion"
            }
        ]

        # If the document contains Python code
        if any(l.startswith("def ") or l.startswith("class ") for l in lines):
            completions.extend([
                {
                    "label": "def function_name(args)",
                    "kind": 3,  # Function
                    "detail": "Create a new function",
                    "documentation": "Define a new Python function",
                    "insertText": "def ${1:function_name}(${2:args}):\n\t${3:pass}"
                },
                {
                    "label": "class ClassName",
                    "kind": 7,  # Class
                    "detail": "Create a new class",
                    "documentation": "Define a new Python class",
                    "insertText": "class ${1:ClassName}:\n\tdef __init__(self, ${2:args}):\n\t\t${3:pass}"
                },
                {
                    "label": "if condition",
                    "kind": 14,  # Keyword
                    "detail": "If statement",
                    "documentation": "Create an if statement",
                    "insertText": "if ${1:condition}:\n\t${2:pass}"
                }
            ])

        return completions

    def _generate_hover_info(self, uri, position):
        """
        Generate hover information for the current position
        """
        document_content = self.server.documents.get(uri, "")
        if not document_content:
            return "No document content available"

        lines = document_content.split("\n")
        line = position.get("line", 0)
        character = position.get("character", 0)

        if line < len(lines):
            current_line = lines[line]
            # Simple heuristic to extract the word under the cursor
            start = max(0, character)
            while start > 0 and current_line[start-1].isalnum() or current_line[start-1] == '_':
                start -= 1

            end = min(len(current_line), character)
            while end < len(current_line) and (current_line[end].isalnum() or current_line[end] == '_'):
                end += 1

            word = current_line[start:end]

            if word:
                # Generate information based on the word
                if word == "RequestHandler":
                    return "**RequestHandler**\n\nHandles incoming LSP requests from clients.\n\nProperties:\n- server: Server instance\n- logger: Logging instance"
                elif word == "SimpleMCPServer":
                    return "**SimpleMCPServer**\n\nMCP server implementation for GitHub Copilot.\n\nMethods:\n- run(): Start the server\n- shutdown_gracefully(): Stop the server"
                else:
                    return f"**{word}**\n\nNo detailed information available for this symbol."

        return "Hover information from NeoZork MCP Server"

    def _find_definitions(self, uri, position):
        """
        Find definition locations for symbol at position
        """
        document_content = self.server.documents.get(uri, "")
        if not document_content:
            return []

        lines = document_content.split("\n")
        line = position.get("line", 0)
        character = position.get("character", 0)

        if line < len(lines):
            current_line = lines[line]
            # Extract the word under the cursor
            start = max(0, character)
            while start > 0 and (current_line[start-1].isalnum() or current_line[start-1] == '_'):
                start -= 1

            end = min(len(current_line), character)
            while end < len(current_line) and (current_line[end].isalnum() or current_line[end] == '_'):
                end += 1

            word = current_line[start:end]

            if word:
                # Search for definitions in the document
                for i, line_text in enumerate(lines):
                    if line_text.startswith(f"def {word}") or line_text.startswith(f"class {word}"):
                        return [
                            {
                                "uri": uri,
                                "range": {
                                    "start": {"line": i, "character": 0},
                                    "end": {"line": i, "character": len(line_text)}
                                }
                            }
                        ]

        return []  # If not found

    def _find_workspace_symbols(self, query):
        """
        Find symbols in the workspace matching the query
        """
        symbols = []

        # Simple simulation of symbols in the workspace
        if not query or "handler" in query.lower():
            symbols.append({
                "name": "RequestHandler",
                "kind": 5,  # Class
                "location": {
                    "uri": "file:///Users/rost/Documents/DIS/REPO/neozork-hld-prediction/mcp/handler.py",
                    "range": {
                        "start": {"line": 12, "character": 0},
                        "end": {"line": 12, "character": 14}
                    }
                }
            })

        if not query or "server" in query.lower():
            symbols.append({
                "name": "SimpleMCPServer",
                "kind": 5,  # Class
                "location": {
                    "uri": "file:///Users/rost/Documents/DIS/REPO/neozork-hld-prediction/mcp/server.py",
                    "range": {
                        "start": {"line": 20, "character": 0},
                        "end": {"line": 20, "character": 15}
                    }
                }
            })

        return symbols

    def _find_document_symbols(self, uri):
        """
        Find symbols in the document
        """
        document_content = self.server.documents.get(uri, "")
        if not document_content:
            return []

        symbols = []
        lines = document_content.split("\n")

        # Search for function and class definitions
        for i, line in enumerate(lines):
            line = line.strip()
            if line.startswith("def "):
                name = line[4:].split("(")[0].strip()
                symbols.append({
                    "name": name,
                    "kind": 12,  # Function
                    "range": {
                        "start": {"line": i, "character": 0},
                        "end": {"line": i, "character": len(line)}
                    },
                    "selectionRange": {
                        "start": {"line": i, "character": line.find(name)},
                        "end": {"line": i, "character": line.find(name) + len(name)}
                    }
                })
            elif line.startswith("class "):
                name = line[6:].split("(")[0].split(":")[0].strip()
                symbols.append({
                    "name": name,
                    "kind": 5,  # Class
                    "range": {
                        "start": {"line": i, "character": 0},
                        "end": {"line": i, "character": len(line)}
                    },
                    "selectionRange": {
                        "start": {"line": i, "character": line.find(name)},
                        "end": {"line": i, "character": line.find(name) + len(name)}
                    }
                })

        return symbols

    def _execute_command(self, command, arguments):
        """
        Execute the given command with arguments
        """
        self.logger.info(f"Executing command: {command} with arguments: {arguments}")

        if command == "neozork.analyzeData":
            # Simulated data analysis
            return {
                "status": "success",
                "message": "Data analysis complete",
                "results": {
                    "analyzed_files": 10,
                    "metrics": {
                        "accuracy": 0.95,
                        "recall": 0.87,
                        "precision": 0.92
                    }
                }
            }

        return None

    def _find_references(self, uri, position):
        """
        Find references to the symbol at the given position
        """
        document_content = self.server.documents.get(uri, "")
        if not document_content:
            return []

        lines = document_content.split("\n")
        line = position.get("line", 0)
        character = position.get("character", 0)

        if line < len(lines):
            current_line = lines[line]
            # Extract the word under the cursor
            start = max(0, character)
            while start > 0 and (current_line[start-1].isalnum() or current_line[start-1] == '_'):
                start -= 1

            end = min(len(current_line), character)
            while end < len(current_line) and (current_line[end].isalnum() or current_line[end] == '_'):
                end += 1

            word = current_line[start:end]

            if word:
                references = []
                # Search for all mentions of the word in the document
                for i, line_text in enumerate(lines):
                    pos = 0
                    while True:
                        pos = line_text.find(word, pos)
                        if pos == -1:
                            break

                        # Check that this is a separate word
                        is_word_boundary_left = pos == 0 or not (line_text[pos-1].isalnum() or line_text[pos-1] == '_')
                        is_word_boundary_right = pos + len(word) >= len(line_text) or not (line_text[pos + len(word)].isalnum() or line_text[pos + len(word)] == '_')

                        if is_word_boundary_left and is_word_boundary_right:
                            references.append({
                                "uri": uri,
                                "range": {
                                    "start": {"line": i, "character": pos},
                                    "end": {"line": i, "character": pos + len(word)}
                                }
                            })

                        pos += len(word)

                return references

        return []

