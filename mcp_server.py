#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP (Model Completion Protocol) Server for GitHub Copilot
Works through standard input/output (STDIO)
"""

import json
import logging
import os
import sys
import traceback
from datetime import datetime
import uuid
from pathlib import Path
import glob
import re
import csv
import pandas as pd
import ast
import keyword

# Setting up logging
def setup_logging():
    """Setting up the logging system"""
    try:
        log_dir = Path(__file__).parent / "logs"
        print(f"Attempting to create logs directory at path: {log_dir.absolute()}")
        # Automatically create logs directory if it doesn't exist
        log_dir.mkdir(exist_ok=True)
        print(f"Logs directory created or already exists: {log_dir.exists()}")
        log_file = log_dir / "mcp_server.log"

        # Creating formatter for logs
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(name)s] [Session: %(session_id)s] %(message)s'
        )

        # Setting up file handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)

        # Setting up logger
        logger = logging.getLogger('mcp_server')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

        # Adding session_id to logger context
        session_id = str(uuid.uuid4())
        extra = {'session_id': session_id}
        logger = logging.LoggerAdapter(logger, extra)

        # Adding session separator to log file
        logger.info("="*80)
        logger.info(f"Starting new MCP server session: {session_id}")
        logger.info("="*80)

        return logger
    except Exception as e:
        print(f"Error setting up logging: {str(e)}")
        print(traceback.format_exc())
        # Creating basic logger without file handler
        logger = logging.getLogger('mcp_server')
        logger.setLevel(logging.DEBUG)
        session_id = str(uuid.uuid4())
        extra = {'session_id': session_id}
        return logging.LoggerAdapter(logger, extra)

# Class for indexing and searching code elements in the project
class CodeIndexer:
    """Class for indexing and searching code elements in the project"""

    def __init__(self, logger):
        self.logger = logger

        # Structure for storing indexed code
        self.code_index = {
            'functions': {},  # function_name -> [files where it's defined]
            'classes': {},    # class_name -> [files where it's defined]
            'variables': {},  # variable_name -> [files where it's defined/used]
            'imports': {},    # import_name -> [files where it's used]
            'docstrings': {}  # (name, type) -> docstring
        }

        self.logger.info("Code indexer initialized")

    def index_python_file(self, file_path, content):
        """Indexes the content of a Python file"""
        try:
            # Parse file content into AST
            tree = ast.parse(content)

            # Extract names and types of code elements
            for node in ast.walk(tree):
                # Index functions
                if isinstance(node, ast.FunctionDef):
                    self._index_function(node, file_path)

                # Index classes
                elif isinstance(node, ast.ClassDef):
                    self._index_class(node, file_path)

                # Index imports
                elif isinstance(node, ast.Import):
                    self._index_import(node, file_path)

                # Index from-imports
                elif isinstance(node, ast.ImportFrom):
                    self._index_import_from(node, file_path)

                # Index variables
                elif isinstance(node, ast.Assign):
                    self._index_variable(node, file_path)

            self.logger.debug(f"Successfully indexed file {file_path}")

        except Exception as e:
            self.logger.error(f"Error while indexing file {file_path}: {str(e)}")
            self.logger.error(traceback.format_exc())

    def _index_function(self, node, file_path):
        """Indexes a function"""
        func_name = node.name

        # Skip "private" functions (starting with _)
        if func_name.startswith('_') and not func_name.startswith('__'):
            return

        # Add function information to the index
        if func_name not in self.code_index['functions']:
            self.code_index['functions'][func_name] = []

        if file_path not in self.code_index['functions'][func_name]:
            self.code_index['functions'][func_name].append(file_path)

        # Extract and save docstring
        docstring = ast.get_docstring(node)
        if docstring:
            self.code_index['docstrings'][(func_name, 'function')] = docstring

    def _index_class(self, node, file_path):
        """Indexes a class"""
        class_name = node.name

        # Skip "private" classes (starting with _)
        if class_name.startswith('_') and not class_name.startswith('__'):
            return

        # Add class information to the index
        if class_name not in self.code_index['classes']:
            self.code_index['classes'][class_name] = []

        if file_path not in self.code_index['classes'][class_name]:
            self.code_index['classes'][class_name].append(file_path)

        # Extract and save docstring
        docstring = ast.get_docstring(node)
        if docstring:
            self.code_index['docstrings'][(class_name, 'class')] = docstring

        # Index class methods
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_name = f"{class_name}.{item.name}"

                # Add class method information
                if method_name not in self.code_index['functions']:
                    self.code_index['functions'][method_name] = []

                if file_path not in self.code_index['functions'][method_name]:
                    self.code_index['functions'][method_name].append(file_path)

                # Save method docstring
                method_docstring = ast.get_docstring(item)
                if method_docstring:
                    self.code_index['docstrings'][(method_name, 'method')] = method_docstring

    def _index_import(self, node, file_path):
        """Indexes an import"""
        for alias in node.names:
            import_name = alias.name

            if import_name not in self.code_index['imports']:
                self.code_index['imports'][import_name] = []

            if file_path not in self.code_index['imports'][import_name]:
                self.code_index['imports'][import_name].append(file_path)

    def _index_import_from(self, node, file_path):
        """Indexes a from-import"""
        module_name = node.module
        for alias in node.names:
            import_name = f"{module_name}.{alias.name}"

            if import_name not in self.code_index['imports']:
                self.code_index['imports'][import_name] = []

            if file_path not in self.code_index['imports'][import_name]:
                self.code_index['imports'][import_name].append(file_path)

    def _index_variable(self, node, file_path):
        """Indexes variables"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id

                if var_name not in self.code_index['variables']:
                    self.code_index['variables'][var_name] = []

                if file_path not in self.code_index['variables'][var_name]:
                    self.code_index['variables'][var_name].append(file_path)

    def get_references(self, name):
        """Returns references to a code element"""
        references = []
        for category in ['functions', 'classes', 'variables', 'imports']:
            if name in self.code_index[category]:
                references.extend(self.code_index[category][name])
        return references

    def get_definitions(self, name):
        """Returns definitions of a code element"""
        definitions = []
        for category in ['functions', 'classes', 'variables', 'imports']:
            if name in self.code_index[category]:
                definitions.extend(self.code_index[category][name])
        return definitions

# Class for processing messages via MCP protocol
class MCPServer:
    def __init__(self, logger):
        self.logger = logger
        self.running = True
        self.request_id_to_handler = {}
        self.project_root = Path(__file__).parent
        self.project_files = {}
        self.file_content_cache = {}
        self.available_symbols = set()
        self.available_timeframes = set()
        self.financial_data_summary = {}
        # Buffer for testing send_message output
        self.sent = []

        # Initializing code indexing system
        self.code_indexer = CodeIndexer(logger)

        # Scanning project files on initialization
        self.scan_project_files()

        # Scanning financial instrument data
        self.scan_mql5_feed_data()

        # Indexing project code
        self.index_project_code()

        # Registration of handlers for different types of requests
        self.handlers = {
            "initialize": self.handle_initialize,
            "shutdown": self.handle_shutdown,
            "exit": self.handle_exit,
            "textDocument/completion": self.handle_completion,
            "workspace/symbols": self.handle_workspace_symbols,
            "workspace/files": self.handle_workspace_files,
            "textDocument/context": self.handle_document_context,
            "financialData/symbols": self.handle_financial_symbols,
            "financialData/timeframes": self.handle_financial_timeframes,
            "financialData/info": self.handle_financial_data_info,
            "financialData/summary": self.handle_financial_data_summary,
            "codeSearch/byName": self.handle_code_search_by_name,
            "codeSearch/references": self.handle_code_search_references,
            "codeSearch/definition": self.handle_code_search_definition,
            # Add other handlers as needed
        }

        self.logger.info("MCP Server initialized")

    def scan_project_files(self):
        """Scanning project files"""
        self.logger.info("Scanning project files")
        try:
            # Create a dictionary to store file information
            self.project_files = {}
            self.file_content_cache = {}

            # List of file extensions to scan
            code_extensions = ['.py', '.json', '.md', '.csv', '.txt']

            # Ignored directories
            ignore_dirs = ['__pycache__', '.git', '.idea', 'logs']

            # Recursive directory traversal
            for file_path in self.project_root.rglob('*'):
                # Skip directories from the ignore list
                if any(ignore_dir in str(file_path) for ignore_dir in ignore_dirs):
                    continue

                # Check if it's a file, not a directory
                if file_path.is_file():
                    # Check file extension
                    if file_path.suffix in code_extensions or file_path.suffix == '':
                        # Get the relative path to the file
                        relative_path = file_path.relative_to(self.project_root)
                        self.project_files[str(relative_path)] = {
                            'path': file_path,
                            'extension': file_path.suffix,
                            'size': file_path.stat().st_size,
                            'modified': datetime.fromtimestamp(file_path.stat().st_mtime)
                        }

                        # Cache content only for text files and not too large
                        if file_path.suffix in ['.py', '.json', '.md', '.txt'] and file_path.stat().st_size < 1024 * 1024:  # No more than 1 MB
                            try:
                                self.file_content_cache[str(relative_path)] = file_path.read_text(encoding='utf-8')
                            except UnicodeDecodeError:
                                # If decoding error occurs, the file may be binary
                                self.logger.warning(f"Failed to read file {relative_path} as text")

            self.logger.info(f"Files found: {len(self.project_files)}")
        except Exception as e:
            self.logger.error(f"Error while scanning project files: {str(e)}")
            self.logger.error(traceback.format_exc())

    def scan_mql5_feed_data(self):
        """Scanning and analyzing financial instrument data from the mql5_feed directory"""
        self.logger.info("Scanning MQL5 Feed data")

        self.available_symbols = set()
        self.available_timeframes = set()
        self.financial_data_summary = {}

        mql5_feed_dir = self.project_root / "mql5_feed"

        if not mql5_feed_dir.exists() or not mql5_feed_dir.is_dir():
            self.logger.warning(f"Directory {mql5_feed_dir} not found")
            return

        # Regular expression to extract symbol and timeframe from file name
        pattern = re.compile(r'CSVExport_([A-Z0-9\.]+)_PERIOD_([A-Z0-9]+)\.csv')

        csv_files = list(mql5_feed_dir.glob("*.csv"))
        self.logger.info(f"Found {len(csv_files)} CSV files in the mql5_feed directory")

        for file_path in csv_files:
            match = pattern.match(file_path.name)
            if match:
                symbol, timeframe = match.groups()
                self.available_symbols.add(symbol)
                self.available_timeframes.add(timeframe)

                # Analyze the structure of the CSV file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        headers = next(reader)  # First row with headers

                        # Read the first 5 rows to determine data types
                        sample_data = []
                        for _ in range(5):
                            try:
                                sample_data.append(next(reader))
                            except StopIteration:
                                break

                    # Save metadata about the file
                    key = f"{symbol}_{timeframe}"
                    self.financial_data_summary[key] = {
                        'path': str(file_path),
                        'symbol': symbol,
                        'timeframe': timeframe,
                        'columns': headers,
                        'sample_data': sample_data,
                        'size': file_path.stat().st_size,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime)
                    }

                except Exception as e:
                    self.logger.error(f"Error analyzing file {file_path.name}: {str(e)}")

        self.logger.info(f"Symbols found: {', '.join(sorted(self.available_symbols))}")
        self.logger.info(f"Timeframes found: {', '.join(sorted(self.available_timeframes))}")

    def index_project_code(self):
        """Indexes project code"""
        self.logger.info("Indexing project code")
        try:
            for file_path, file_info in self.project_files.items():
                if file_info['extension'] == '.py':
                    content = self.file_content_cache.get(file_path)
                    if content:
                        self.code_indexer.index_python_file(file_path, content)
        except Exception as e:
            self.logger.error(f"Error while indexing project code: {str(e)}")
            self.logger.error(traceback.format_exc())

    def start(self):
        """Start the server and process incoming messages"""
        self.logger.info("MCP Server started and waiting for messages")

        while self.running:
            try:
                # Read headers
                headers = {}
                while True:
                    line = sys.stdin.readline().strip()
                    if not line:
                        break
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()

                if not headers:
                    continue

                # Read message body
                content_length = int(headers.get('Content-Length', 0))
                if content_length > 0:
                    body = sys.stdin.read(content_length)
                    self.logger.debug(f"Message received: {body}")
                    self.process_message(body)
                else:
                    self.logger.warning("Received message with zero length")

            except Exception as e:
                self.logger.error(f"Error while processing message: {str(e)}")
                self.logger.error(traceback.format_exc())

    def process_message(self, message_str):
        """Process incoming message"""
        try:
            message = json.loads(message_str)
            self.logger.debug(f"Processing message: {message}")

            # Check if the message is a request or response
            if "method" in message:
                # It's a request
                request_id = message.get("id")
                method = message.get("method")
                params = message.get("params", {})

                self.logger.info(f"Received request {method} with ID: {request_id}")

                # Call the corresponding method handler
                if method in self.handlers:
                    self.handlers[method](request_id, params)
                else:
                    self.logger.warning(f"Unknown method: {method}")
                    self.send_error_response(request_id, -32601, f"Method {method} is not supported")

            # Here you can add processing of responses from the client,
            # if such are expected

        except json.JSONDecodeError:
            self.logger.error(f"JSON decoding error: {message_str}")
        except Exception as e:
            self.logger.error(f"Error while processing message: {str(e)}")
            self.logger.error(traceback.format_exc())

    def send_response(self, request_id, result):
        """Send response to request"""
        if request_id is None:
            return

        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }

        self.send_message(response)

    def send_error_response(self, request_id, code, message, data=None):
        """Send error response"""
        if request_id is None:
            return

        error = {
            "code": code,
            "message": message
        }

        if data:
            error["data"] = data

        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": error
        }

        self.send_message(response)

    def send_message(self, message):
        """Send message to client"""
        message_str = json.dumps(message)
        content_length = len(message_str)

        # Form and send the message
        response = f"Content-Length: {content_length}\r\n\r\n{message_str}"
        sys.stdout.write(response)
        sys.stdout.flush()

        self.logger.debug(f"Message sent: {message_str}")

    # Handlers for various MCP methods

    def handle_initialize(self, request_id, params):
        """Handle initialize request"""
        self.logger.info("Handling initialize request")

        # Protocol version and server capabilities
        capabilities = {
            "completionProvider": {
                "triggerCharacters": ["."]
            },
            "workspaceSymbolProvider": True,
            # Additional capabilities as needed
        }

        result = {
            "capabilities": capabilities,
            "serverInfo": {
                "name": "Neozork MCP Server",
                "version": "1.0.0"
            }
        }

        self.send_response(request_id, result)

    def handle_shutdown(self, request_id, params):
        """Handle shutdown request"""
        self.logger.info("Handling shutdown request")

        # Send an empty result as specified in the LSP specification
        self.send_response(request_id, None)

        # Actual termination occurs upon receiving the exit request
        # But we should prepare for termination

    def handle_exit(self, request_id, params):
        """Handle exit request"""
        self.logger.info("Exit request received, shutting down server")
        self.running = False

        # Exit does not require a response

    def handle_completion(self, request_id, params):
        """Handle completion request"""
        self.logger.info("Handling completion request")

        try:
            # Get information about the current document and cursor position
            text_document = params.get("textDocument", {})
            position = params.get("position", {})

            if not text_document or not position:
                self.send_error_response(request_id, -32602, "Document or cursor position not specified")
                return

            uri = text_document.get("uri", "")
            line = position.get("line", 0)
            character = position.get("character", 0)

            # Get file and line context
            file_context = self.get_file_context(uri, line, character)
            if not file_context:
                # If context could not be obtained, return an empty list
                result = {
                    "isIncomplete": False,
                    "items": []
                }
                self.send_response(request_id, result)
                return

            # Determine file type by extension
            file_extension = Path(uri).suffix.lower()

            # Array for completion items
            completion_items = []

            # Analyze the current line to determine context
            current_line = file_context.get("current_line", "")
            prefix = current_line[:character]

            # If it's a Python file
            if file_extension == '.py':
                completion_items.extend(self.get_python_completions(prefix, file_context))

            # If the text mentions financial symbols or timeframes
            if any(symbol in prefix for symbol in self.available_symbols) or \
               any(timeframe in prefix for timeframe in self.available_timeframes):
                completion_items.extend(self.get_financial_completions(prefix))

            # Add general workspace symbols
            completion_items.extend(self.get_workspace_completions(prefix))

            # Return result with found completion items
            result = {
                "isIncomplete": False,
                "items": completion_items
            }

            self.send_response(request_id, result)

        except Exception as e:
            self.logger.error(f"Error while handling completion request: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.send_error_response(request_id, -32603, "Internal server error")

    def get_file_context(self, uri, line, character):
        """Get file context for completion"""
        try:
            file_path = Path(uri)
            if not file_path.exists():
                # Try to get the file from our cache
                relative_path = file_path.relative_to(self.project_root)
                content = self.file_content_cache.get(str(relative_path))
                if not content:
                    return None

                lines = content.splitlines()
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

            # Check validity of line number
            if line >= len(lines):
                return None

            # Get the current line
            current_line = lines[line].rstrip('\r\n')

            # Get the previous 5 lines for context
            start_line = max(0, line - 5)
            previous_lines = lines[start_line:line]

            # Get the next 5 lines for context
            end_line = min(len(lines), line + 5)
            next_lines = lines[line+1:end_line]

            return {
                "current_line": current_line,
                "previous_lines": previous_lines,
                "next_lines": next_lines,
                "full_content": lines
            }

        except Exception as e:
            self.logger.error(f"Error while getting file context: {str(e)}")
            return None

    def get_python_completions(self, prefix, file_context):
        """Generate completion suggestions for Python files"""
        completion_items = []

        # Main Python keywords
        python_keywords = ["def", "class", "if", "else", "elif", "for", "while", "try", "except",
                          "finally", "with", "import", "from", "as", "return", "yield", "lambda",
                          "True", "False", "None", "and", "or", "not", "in", "is"]

        # Useful methods for working with financial data
        finance_methods = [
            {
                "label": "load_financial_data",
                "kind": 3,  # Function
                "detail": "Load financial data from CSV file",
                "documentation": "load_financial_data(symbol, timeframe)\nLoads data for the specified symbol and timeframe",
                "insertText": "load_financial_data('${1:symbol}', '${2:timeframe}')"
            },
            {
                "label": "calculate_sma",
                "kind": 3,  # Function
                "detail": "Calculate Simple Moving Average (SMA)",
                "documentation": "calculate_sma(data, period)\nCalculates the simple moving average for the specified data",
                "insertText": "calculate_sma(${1:data}, ${2:period})"
            },
            {
                "label": "calculate_ema",
                "kind": 3,  # Function
                "detail": "Calculate Exponential Moving Average (EMA)",
                "documentation": "calculate_ema(data, period)\nCalculates the exponential moving average for the specified data",
                "insertText": "calculate_ema(${1:data}, ${2:period})"
            },
            {
                "label": "predict_trend",
                "kind": 3,  # Function
                "detail": "Predict price trend",
                "documentation": "predict_trend(data)\nPredicts the direction of price movement based on historical data",
                "insertText": "predict_trend(${1:data})"
            }
        ]

        # If pandas is imported, add pandas methods
        if "import pandas" in "\n".join(file_context.get("previous_lines", [])) or "from pandas" in "\n".join(file_context.get("previous_lines", [])):
            pandas_methods = [
                {
                    "label": "pd.read_csv",
                    "kind": 3,  # Function
                    "detail": "Load data from CSV file",
                    "documentation": "pd.read_csv(filepath_or_buffer, sep=',', header='infer', ...)\nReads a CSV file into a DataFrame",
                    "insertText": "pd.read_csv('${1:filepath}')"
                },
                {
                    "label": "pd.DataFrame",
                    "kind": 3,  # Function
                    "detail": "Create DataFrame",
                    "documentation": "pd.DataFrame(data=None, index=None, columns=None, dtype=None, copy=False)\nCreates a two-dimensional data structure with row and column labels",
                    "insertText": "pd.DataFrame(${1:data})"
                },
                {
                    "label": "df.rolling",
                    "kind": 3,  # Method
                    "detail": "Rolling window for DataFrame",
                    "documentation": "df.rolling(window, min_periods=None, center=False, ...)\nCreates a rolling window object for calculating statistics",
                    "insertText": "df.rolling(${1:window}).${2:mean}()"
                }
            ]
            completion_items.extend(pandas_methods)

        # Add Python keywords
        for keyword in python_keywords:
            if keyword.startswith(prefix.strip()):
                completion_items.append({
                    "label": keyword,
                    "kind": 14,  # Keyword
                    "detail": "Python keyword",
                    "insertText": keyword
                })

        # Add methods for working with financial data
        completion_items.extend(finance_methods)

        return completion_items

    def get_financial_completions(self, prefix):
        """Generate completion suggestions for financial data"""
        completion_items = []

        # Add available symbols
        for symbol in sorted(self.available_symbols):
            completion_items.append({
                "label": symbol,
                "kind": 14,  # Constant
                "detail": f"Financial symbol",
                "documentation": f"Symbol {symbol} is available in timeframes: {', '.join(sorted(self.available_timeframes))}",
                "insertText": symbol
            })

        # Add available timeframes
        for timeframe in sorted(self.available_timeframes):
            completion_items.append({
                "label": timeframe,
                "kind": 14,  # Constant
                "detail": f"Timeframe",
                "documentation": f"Timeframe {timeframe} (period)",
                "insertText": timeframe
            })

        # Add special functions for financial data analysis
        data_analysis_snippets = [
            {
                "label": "load_and_analyze",
                "kind": 15,  # Snippet
                "detail": "Load and analyze financial data",
                "documentation": "Loads data for the specified symbol and timeframe and performs basic analysis",
                "insertText": "# Load data\ncsv_path = 'mql5_feed/CSVExport_${1:BTCUSD}_PERIOD_${2:D1}.csv'\ndf = pd.read_csv(csv_path)\n\n# Convert time\ndf['time'] = pd.to_datetime(df['time'])\ndf.set_index('time', inplace=True)\n\n# Calculate indicators\ndf['sma_20'] = df['close'].rolling(window=20).mean()\ndf['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()\n\n# Visualization\nplt.figure(figsize=(12, 6))\nplt.plot(df.index, df['close'], label='Close')\nplt.plot(df.index, df['sma_20'], label='SMA 20')\nplt.plot(df.index, df['ema_50'], label='EMA 50')\nplt.legend()\nplt.title('${1:BTCUSD} - ${2:D1}')\nplt.show()"
            },
            {
                "label": "predict_hld",
                "kind": 15,  # Snippet
                "detail": "Predict HLD (High, Low, Direction)",
                "documentation": "Creates a model to predict high and low values, as well as trend direction",
                "insertText": "# Prepare data for HLD prediction\ndef prepare_hld_data(df):\n    # Add price lags\n    for i in range(1, 6):\n        df[f'close_lag_{i}'] = df['close'].shift(i)\n        df[f'high_lag_{i}'] = df['high'].shift(i)\n        df[f'low_lag_{i}'] = df['low'].shift(i)\n    \n    # Add target variables\n    df['next_high'] = df['high'].shift(-1)\n    df['next_low'] = df['low'].shift(-1)\n    df['next_direction'] = np.where(df['close'].shift(-1) > df['close'], 1, -1)\n    \n    # Remove rows with NaN\n    df.dropna(inplace=True)\n    \n    return df\n\n# Load data\ncsv_path = 'mql5_feed/CSVExport_${1:BTCUSD}_PERIOD_${2:D1}.csv'\ndf = pd.read_csv(csv_path)\ndf['time'] = pd.to_datetime(df['time'])\n\n# Prepare data\ndf_prepared = prepare_hld_data(df)\n\n# Train models\n# ... code for training models ...\n\n# Prediction\n# ... code for prediction ...\n"
            }
        ]

        completion_items.extend(data_analysis_snippets)

        return completion_items

    def get_workspace_completions(self, prefix):
        """Generate completion suggestions based on workspace files"""
        completion_items = []

        # Analyze Python files in the project to find classes and functions
        python_files = [path for path in self.project_files.keys() if path.endswith('.py')]

        for file_path in python_files:
            try:
                content = self.file_content_cache.get(file_path)
                if not content:
                    continue

                # Find function definitions
                func_pattern = re.compile(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\):', re.MULTILINE)
                functions = func_pattern.findall(content)

                # Find class definitions
                class_pattern = re.compile(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(\(.*?\))?:', re.MULTILINE)
                classes = class_pattern.findall(content)

                # Add found functions to completion
                for func_name, params in functions:
                    if func_name.startswith(prefix.strip()) or prefix.strip() == "":
                        completion_items.append({
                            "label": func_name,
                            "kind": 3,  # Function
                            "detail": f"Function from {file_path}",
                            "documentation": f"def {func_name}({params})",
                            "insertText": func_name
                        })

                # Add found classes to completion
                for class_name, _ in classes:
                    if class_name.startswith(prefix.strip()) or prefix.strip() == "":
                        completion_items.append({
                            "label": class_name,
                            "kind": 7,  # Class
                            "detail": f"Class from {file_path}",
                            "documentation": f"class {class_name}",
                            "insertText": class_name
                        })

            except Exception as e:
                self.logger.error(f"Error analyzing file {file_path}: {str(e)}")

        return completion_items

    def handle_workspace_symbols(self, request_id, params):
        """Handle workspace/symbols request"""
        self.logger.info("Handling workspace/symbols request")

        # Here should be the logic for searching symbols in the workspace
        # As a placeholder, return an empty list
        result = []

        self.send_response(request_id, result)

    def handle_workspace_files(self, request_id, params):
        """Handle workspace/files request"""
        self.logger.info("Handling workspace/files request")
        result = list(self.project_files.keys())
        self.send_response(request_id, result)

    def handle_document_context(self, request_id, params):
        """Handle textDocument/context request"""
        self.logger.info("Handling textDocument/context request")
        try:
            file_path = params.get("textDocument", {}).get("uri")
            if not file_path:
                self.send_error_response(request_id, -32602, "File path not specified")
                return

            relative_path = Path(file_path).relative_to(self.project_root)
            content = self.file_content_cache.get(str(relative_path))
            if content is None:
                self.send_error_response(request_id, -32602, f"File {file_path} not found")
                return

            result = {
                "content": content
            }
            self.send_response(request_id, result)
        except Exception as e:
            self.logger.error(f"Error while processing document context: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.send_error_response(request_id, -32603, "Internal server error")

    def handle_financial_symbols(self, request_id, params):
        """Handle financialData/symbols request"""
        self.logger.info("Handling financialData/symbols request")
        result = list(self.available_symbols)
        self.send_response(request_id, result)

    def handle_financial_timeframes(self, request_id, params):
        """Handle financialData/timeframes request"""
        self.logger.info("Handling financialData/timeframes request")
        result = list(self.available_timeframes)
        self.send_response(request_id, result)

    def handle_financial_data_info(self, request_id, params):
        """Handle financialData/info request"""
        self.logger.info("Handling financialData/info request")
        try:
            symbol = params.get("symbol")
            timeframe = params.get("timeframe")
            key = f"{symbol}_{timeframe}"
            data_info = self.financial_data_summary.get(key)
            if not data_info:
                self.send_error_response(request_id, -32602, f"Data for {symbol} and {timeframe} not found")
                return
            self.send_response(request_id, data_info)
        except Exception as e:
            self.logger.error(f"Error processing financialData/info: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.send_error_response(request_id, -32603, "Internal server error")

    def handle_financial_data_summary(self, request_id, params):
        """Handle financialData/summary request"""
        self.logger.info("Handling financialData/summary request")
        result = self.financial_data_summary
        self.send_response(request_id, result)

    def handle_code_search_by_name(self, request_id, params):
        """Handle codeSearch/byName request"""
        self.logger.info("Handling codeSearch/byName request")
        try:
            name = params.get("name")
            if not name:
                self.send_error_response(request_id, -32602, "Name for search not specified")
                return

            result = {
                "functions": self.code_indexer.code_index['functions'].get(name, []),
                "classes": self.code_indexer.code_index['classes'].get(name, []),
                "variables": self.code_indexer.code_index['variables'].get(name, []),
                "imports": self.code_indexer.code_index['imports'].get(name, [])
            }
            self.send_response(request_id, result)
        except Exception as e:
            self.logger.error(f"Error processing codeSearch/byName: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.send_error_response(request_id, -32603, "Internal server error")

    def handle_code_search_references(self, request_id, params):
        """Handle codeSearch/references request"""
        self.logger.info("Handling codeSearch/references request")
        try:
            name = params.get("name")
            if not name:
                self.send_error_response(request_id, -32602, "Name for reference search not specified")
                return

            result = {
                "references": self.code_indexer.get_references(name)
            }
            self.send_response(request_id, result)
        except Exception as e:
            self.logger.error(f"Error processing codeSearch/references: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.send_error_response(request_id, -32603, "Internal server error")

    def handle_code_search_definition(self, request_id, params):
        """Handle codeSearch/definition request"""
        self.logger.info("Handling codeSearch/definition request")
        try:
            name = params.get("name")
            if not name:
                self.send_error_response(request_id, -32602, "Name for definition search not specified")
                return

            result = {
                "definition": self.code_indexer.get_definitions(name)
            }
            self.send_response(request_id, result)
        except Exception as e:
            self.logger.error(f"Error processing codeSearch/definition: {str(e)}")
            self.logger.error(traceback.format_exc())
            self.send_error_response(request_id, -32603, "Internal server error")
