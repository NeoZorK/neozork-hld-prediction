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
                        },
                        # Добавляем поддержку файловой системы
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

            # Генерация реальных завершений на основе содержимого документа
            completions = self._generate_completions(document_content, position)

            return {
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

            # Извлекаем слово под курсором
            hover_info = self._generate_hover_info(uri, position)

            return {
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

            # Реализация поиска определений
            definitions = self._find_definitions(uri, position)

            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": definitions  # Возвращаем найденные определения
            }

        # Новый обработчик для workspace/symbol
        elif method == "workspace/symbol":
            self.logger.info(f"Received workspace symbol request (ID: {message_id})")
            params = request.get("params", {})
            query = params.get("query", "")

            # Поиск символов в рабочем пространстве
            symbols = self._find_workspace_symbols(query)

            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": symbols
            }

        # Новый обработчик для textDocument/documentSymbol
        elif method == "textDocument/documentSymbol":
            self.logger.info(f"Received document symbol request (ID: {message_id})")
            params = request.get("params", {})
            text_document = params.get("textDocument", {})
            uri = text_document.get("uri", "")

            # Поиск символов в документе
            symbols = self._find_document_symbols(uri)

            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": symbols
            }

        # Новый обработчик для workspace/executeCommand
        elif method == "workspace/executeCommand":
            self.logger.info(f"Received execute command request (ID: {message_id})")
            params = request.get("params", {})
            command = params.get("command", "")
            arguments = params.get("arguments", [])

            # Выполнение команды
            result = self._execute_command(command, arguments)

            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": result
            }

        # Новый обработчик для textDocument/references
        elif method == "textDocument/references":
            self.logger.info(f"Received references request (ID: {message_id})")
            params = request.get("params", {})
            text_document = params.get("textDocument", {})
            position = params.get("position", {})
            uri = text_document.get("uri", "")

            # Поиск ссылок
            references = self._find_references(uri, position)

            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": references
            }

        # Новый обработчик для workspace/willCreateFiles
        elif method == "workspace/willCreateFiles":
            self.logger.info(f"Received will create files request (ID: {message_id})")

            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None  # Без правок
            }

        # Новый обработчик для workspace/willRenameFiles
        elif method == "workspace/willRenameFiles":
            self.logger.info(f"Received will rename files request (ID: {message_id})")

            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None  # Без правок
            }

        # Новый обработчик для workspace/willDeleteFiles
        elif method == "workspace/willDeleteFiles":
            self.logger.info(f"Received will delete files request (ID: {message_id})")

            return {
                "jsonrpc": "2.0",
                "id": message_id,
                "result": None  # Без правок
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
                params = request.get("params", {})
                doc_uri = params.get("doc", {}).get("uri", "")
                position = params.get("position", {})
                self.logger.info(f"Query for Copilot completions in {doc_uri} at position {position}")

                # Получаем содержимое документа если есть
                document_content = ""
                if doc_uri and doc_uri in self.server.documents:
                    document_content = self.server.documents[doc_uri]

                # Генерируем более осмысленные завершения для Copilot
                return {
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
                return {
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
                return {
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
                return {
                    "jsonrpc": "2.0",
                    "id": message_id,
                    "result": {
                        "tokens": text.split()  # Простая токенизация по пробелам
                    }
                }
            elif method == "copilot/getCaptionContext":
                self.logger.info("Copilot caption context request")
                return {
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

    def _generate_completions(self, document_content, position):
        """
        Generate completions based on document content and cursor position
        """
        line = position.get("line", 0)
        character = position.get("character", 0)

        # Разбиваем содержимое документа на строки
        lines = document_content.split("\n") if document_content else []

        # Базовые завершения
        completions = [
            {
                "label": "Simple placeholder completion",
                "kind": 1,  # Text
                "detail": "NeoZork MCP Server placeholder completion",
                "documentation": "This is a placeholder completion from the simple MCP server",
                "insertText": "placeholder_completion"
            }
        ]

        # Если документ содержит Python код
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
            # Простая эвристика для выделения слова под курсором
            start = max(0, character)
            while start > 0 and current_line[start-1].isalnum() or current_line[start-1] == '_':
                start -= 1

            end = min(len(current_line), character)
            while end < len(current_line) and (current_line[end].isalnum() or current_line[end] == '_'):
                end += 1

            word = current_line[start:end]

            if word:
                # Генерируем информацию на основе слова
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
            # Выделяем слово под курсором
            start = max(0, character)
            while start > 0 and (current_line[start-1].isalnum() or current_line[start-1] == '_'):
                start -= 1

            end = min(len(current_line), character)
            while end < len(current_line) and (current_line[end].isalnum() or current_line[end] == '_'):
                end += 1

            word = current_line[start:end]

            if word:
                # Поиск определений в документе
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

        return []  # Если не найдено

    def _find_workspace_symbols(self, query):
        """
        Find symbols in the workspace matching the query
        """
        symbols = []

        # Простая имитация символов в рабочем пространстве
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

        # Поиск определений функций и классов
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
            # Имитация анализа данных
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
            # Выделяем слово под курсором
            start = max(0, character)
            while start > 0 and (current_line[start-1].isalnum() or current_line[start-1] == '_'):
                start -= 1

            end = min(len(current_line), character)
            while end < len(current_line) and (current_line[end].isalnum() or current_line[end] == '_'):
                end += 1

            word = current_line[start:end]

            if word:
                references = []
                # Поиск всех упоминаний слова в документе
                for i, line_text in enumerate(lines):
                    pos = 0
                    while True:
                        pos = line_text.find(word, pos)
                        if pos == -1:
                            break

                        # Проверка, что это отдельное слово
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

