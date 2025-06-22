#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cursor MCP Server for Neozork HLD Prediction Project
Optimized for Cursor IDE with enhanced project-specific features
"""

import json
import logging
import sys
import traceback
import signal
import select
from datetime import datetime
import uuid
from pathlib import Path
import re
import csv
import ast
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum

class CompletionItemKind(Enum):
    TEXT = 1
    METHOD = 2
    FUNCTION = 3
    CONSTRUCTOR = 4
    FIELD = 5
    VARIABLE = 6
    CLASS = 7
    INTERFACE = 8
    MODULE = 9
    PROPERTY = 10
    UNIT = 11
    VALUE = 12
    ENUM = 13
    KEYWORD = 14
    SNIPPET = 15
    COLOR = 16
    FILE = 17
    REFERENCE = 18
    FOLDER = 19
    ENUM_MEMBER = 20
    CONSTANT = 21
    STRUCT = 22
    EVENT = 23
    OPERATOR = 24
    TYPE_PARAMETER = 25

@dataclass
class CompletionItem:
    label: str
    kind: CompletionItemKind
    detail: Optional[str] = None
    documentation: Optional[str] = None
    insert_text: Optional[str] = None
    sort_text: Optional[str] = None
    filter_text: Optional[str] = None
    insert_text_format: Optional[str] = None
    text_edit: Optional[Dict] = None
    additional_text_edits: Optional[List[Dict]] = None
    command: Optional[Dict] = None
    data: Optional[Any] = None

@dataclass
class ProjectFile:
    path: str
    extension: str
    size: int
    modified: datetime
    content: Optional[str] = None
    ast_tree: Optional[ast.AST] = None

@dataclass
class FinancialData:
    symbol: str
    timeframe: str
    path: str
    columns: List[str]
    sample_data: List[List[str]]
    size: int
    modified: datetime

class CursorMCPServer:
    """Enhanced MCP Server optimized for Cursor IDE and Neozork project"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent
        self.logger = self._setup_logging()
        self.running = True
        
        # Project state
        self.project_files: Dict[str, ProjectFile] = {}
        self.financial_data: Dict[str, FinancialData] = {}
        self.code_index = {
            'functions': {},
            'classes': {},
            'variables': {},
            'imports': {},
            'docstrings': {},
            'indicators': {},
            'data_fetchers': {},
            'plotting_functions': {}
        }
        
        # Available symbols and timeframes
        self.available_symbols: Set[str] = set()
        self.available_timeframes: Set[str] = set()
        
        # Message handlers
        self.handlers = {
            "initialize": self._handle_initialize,
            "shutdown": self._handle_shutdown,
            "exit": self._handle_exit,
            "textDocument/completion": self._handle_completion,
            "textDocument/hover": self._handle_hover,
            "textDocument/definition": self._handle_definition,
            "textDocument/references": self._handle_references,
            "workspace/symbols": self._handle_workspace_symbols,
            "workspace/files": self._handle_workspace_files,
            "cursor/projectInfo": self._handle_project_info,
            "cursor/financialData": self._handle_financial_data,
            "cursor/indicators": self._handle_indicators,
            "cursor/codeSearch": self._handle_code_search,
            "cursor/snippets": self._handle_snippets,
            "cursor/analysis": self._handle_analysis
        }
        
        # Initialize project
        self._scan_project()
        self._index_code()
        
        self.logger.info("Cursor MCP Server initialized successfully")

    def _setup_logging(self) -> logging.Logger:
        """Setup enhanced logging system"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"cursor_mcp_{datetime.now().strftime('%Y%m%d')}.log"
        
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [CursorMCP] %(message)s'
        )
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        logger = logging.getLogger('cursor_mcp_server')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        
        return logger

    def _scan_project(self):
        """Scan and index project files"""
        self.logger.info("Scanning project files...")
        
        # Scan Python files
        for py_file in self.project_root.rglob("*.py"):
            if any(ignore in str(py_file) for ignore in ['__pycache__', '.git', '.venv', 'build']):
                continue
                
            relative_path = py_file.relative_to(self.project_root)
            try:
                content = py_file.read_text(encoding='utf-8')
                self.project_files[str(relative_path)] = ProjectFile(
                    path=str(relative_path),
                    extension='.py',
                    size=py_file.stat().st_size,
                    modified=datetime.fromtimestamp(py_file.stat().st_mtime),
                    content=content
                )
            except Exception as e:
                self.logger.warning(f"Failed to read {py_file}: {e}")

        # Scan financial data
        self._scan_financial_data()
        
        self.logger.info(f"Scanned {len(self.project_files)} project files")

    def _scan_financial_data(self):
        """Scan financial data files"""
        mql5_dir = self.project_root / "mql5_feed"
        if not mql5_dir.exists():
            return
            
        pattern = re.compile(r'CSVExport_([A-Z0-9.]+)_PERIOD_([A-Z0-9]+)\.csv')
        
        for csv_file in mql5_dir.glob("*.csv"):
            match = pattern.match(csv_file.name)
            if match:
                symbol, timeframe = match.groups()
                self.available_symbols.add(symbol)
                self.available_timeframes.add(timeframe)
                
                try:
                    with open(csv_file, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        headers = next(reader)
                        sample_data = [next(reader) for _ in range(min(5, 100))]
                        
                    key = f"{symbol}_{timeframe}"
                    self.financial_data[key] = FinancialData(
                        symbol=symbol,
                        timeframe=timeframe,
                        path=str(csv_file),
                        columns=headers,
                        sample_data=sample_data,
                        size=csv_file.stat().st_size,
                        modified=datetime.fromtimestamp(csv_file.stat().st_mtime)
                    )
                except Exception as e:
                    self.logger.warning(f"Failed to read financial data {csv_file}: {e}")

    def _index_code(self):
        """Index code for better search and completion"""
        self.logger.info("Indexing project code...")
        
        for file_path, file_info in self.project_files.items():
            if file_info.content:
                try:
                    tree = ast.parse(file_info.content)
                    self._index_ast_node(tree, file_path)
                except Exception as e:
                    self.logger.warning(f"Failed to parse {file_path}: {e}")

    def _index_ast_node(self, node: ast.AST, file_path: str):
        """Index AST node for code search"""
        for child in ast.walk(node):
            if isinstance(child, ast.FunctionDef):
                self._index_function(child, file_path)
            elif isinstance(child, ast.ClassDef):
                self._index_class(child, file_path)
            elif isinstance(child, (ast.Import, ast.ImportFrom)):
                self._index_import(child, file_path)

    def _index_function(self, node: ast.FunctionDef, file_path: str):
        """Index function definition"""
        func_name = node.name
        if func_name.startswith('_'):
            return
            
        if func_name not in self.code_index['functions']:
            self.code_index['functions'][func_name] = []
        self.code_index['functions'][func_name].append(file_path)
        
        # Index indicators specifically
        if 'indicator' in func_name.lower() or 'calc' in func_name.lower():
            self.code_index['indicators'][func_name] = file_path
            
        # Index data fetchers
        if 'fetcher' in func_name.lower() or 'fetch' in func_name.lower():
            self.code_index['data_fetchers'][func_name] = file_path
            
        # Index plotting functions
        if 'plot' in func_name.lower() or 'chart' in func_name.lower():
            self.code_index['plotting_functions'][func_name] = file_path

    def _index_class(self, node: ast.ClassDef, file_path: str):
        """Index class definition"""
        class_name = node.name
        if class_name.startswith('_'):
            return
            
        if class_name not in self.code_index['classes']:
            self.code_index['classes'][class_name] = []
        self.code_index['classes'][class_name].append(file_path)

    def _index_import(self, node: ast.AST, file_path: str):
        """Index import statements"""
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                if name not in self.code_index['imports']:
                    self.code_index['imports'][name] = []
                self.code_index['imports'][name].append(file_path)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                name = f"{module}.{alias.name}"
                if name not in self.code_index['imports']:
                    self.code_index['imports'][name] = []
                self.code_index['imports'][name].append(file_path)

    def start(self):
        """Start the MCP server"""
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.logger.info("Cursor MCP Server started")
        
        while self.running:
            try:
                rlist, _, _ = select.select([sys.stdin], [], [], 1.0)
                if not rlist:
                    continue
                    
                headers = {}
                while True:
                    line = sys.stdin.readline().strip()
                    if not line:
                        break
                    if ':' in line:
                        key, value = line.split(':', 1)
                        headers[key.strip()] = value.strip()
                
                if not headers:
                    continue
                    
                content_length = int(headers.get('Content-Length', 0))
                if content_length > 0:
                    body = sys.stdin.read(content_length)
                    self._process_message(body)
                    
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                self.logger.error(traceback.format_exc())

    def _signal_handler(self, sig, frame):
        """Handle shutdown signals"""
        self.logger.info("Received shutdown signal")
        self.running = False

    def _process_message(self, message_str: str):
        """Process incoming message"""
        try:
            message = json.loads(message_str)
            
            if "method" in message:
                request_id = message.get("id")
                method = message.get("method")
                params = message.get("params", {})
                
                self.logger.debug(f"Processing {method} request")
                
                if method in self.handlers:
                    result = self.handlers[method](request_id, params)
                    if request_id is not None:
                        self._send_response(request_id, result)
                else:
                    self._send_error(request_id, -32601, f"Method {method} not supported")
                    
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON decode error: {e}")
        except Exception as e:
            self.logger.error(f"Message processing error: {e}")
            self.logger.error(traceback.format_exc())

    def _send_response(self, request_id: Any, result: Any):
        """Send response to client"""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
        self._send_message(response)

    def _send_error(self, request_id: Any, code: int, message: str, data: Any = None):
        """Send error response"""
        error = {"code": code, "message": message}
        if data:
            error["data"] = data
            
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": error
        }
        self._send_message(response)

    def _send_message(self, message: Dict):
        """Send message to client"""
        message_str = json.dumps(message)
        content_length = len(message_str)
        
        response = f"Content-Length: {content_length}\r\n\r\n{message_str}"
        sys.stdout.write(response)
        sys.stdout.flush()

    # Message handlers
    def _handle_initialize(self, request_id: Any, params: Dict) -> Dict:
        """Handle initialize request"""
        return {
            "capabilities": {
                "completionProvider": {
                    "triggerCharacters": [".", ":", "@", "#"],
                    "resolveProvider": True
                },
                "hoverProvider": True,
                "definitionProvider": True,
                "referencesProvider": True,
                "workspaceSymbolProvider": True,
                "textDocumentSync": {
                    "openClose": True,
                    "change": 1
                }
            },
            "serverInfo": {
                "name": "Cursor MCP Server",
                "version": "2.0.0",
                "description": "Enhanced MCP server for Neozork HLD Prediction project"
            }
        }

    def _handle_shutdown(self, request_id: Any, params: Dict) -> None:
        """Handle shutdown request"""
        return None

    def _handle_exit(self, request_id: Any, params: Dict) -> None:
        """Handle exit request"""
        self.running = False
        return None

    def _handle_completion(self, request_id: Any, params: Dict) -> Dict:
        """Handle completion request with enhanced project-specific completions"""
        try:
            text_document = params.get("textDocument", {})
            position = params.get("position", {})
            
            uri = text_document.get("uri", "")
            line = position.get("line", 0)
            character = position.get("character", 0)
            
            # Get file context
            file_path = Path(uri).relative_to(self.project_root) if uri else None
            file_info = self.project_files.get(str(file_path)) if file_path else None
            
            completion_items = []
            
            # Add project-specific completions
            completion_items.extend(self._get_project_completions())
            
            # Add financial data completions
            completion_items.extend(self._get_financial_completions())
            
            # Add indicator completions
            completion_items.extend(self._get_indicator_completions())
            
            # Add code snippets
            completion_items.extend(self._get_code_snippets())
            
            return {
                "isIncomplete": False,
                "items": [asdict(item) for item in completion_items]
            }
            
        except Exception as e:
            self.logger.error(f"Completion error: {e}")
            return {"isIncomplete": False, "items": []}

    def _get_project_completions(self) -> List[CompletionItem]:
        """Get project-specific completion items"""
        items = []
        
        # Functions
        for func_name, files in self.code_index['functions'].items():
            items.append(CompletionItem(
                label=func_name,
                kind=CompletionItemKind.FUNCTION,
                detail=f"Function in {', '.join(files)}",
                documentation=f"Function: {func_name}"
            ))
        
        # Classes
        for class_name, files in self.code_index['classes'].items():
            items.append(CompletionItem(
                label=class_name,
                kind=CompletionItemKind.CLASS,
                detail=f"Class in {', '.join(files)}",
                documentation=f"Class: {class_name}"
            ))
        
        return items

    def _get_financial_completions(self) -> List[CompletionItem]:
        """Get financial data completion items"""
        items = []
        
        # Symbols
        for symbol in sorted(self.available_symbols):
            items.append(CompletionItem(
                label=symbol,
                kind=CompletionItemKind.CONSTANT,
                detail="Financial symbol",
                documentation=f"Available symbol: {symbol}"
            ))
        
        # Timeframes
        for timeframe in sorted(self.available_timeframes):
            items.append(CompletionItem(
                label=timeframe,
                kind=CompletionItemKind.CONSTANT,
                detail="Timeframe",
                documentation=f"Available timeframe: {timeframe}"
            ))
        
        return items

    def _get_indicator_completions(self) -> List[CompletionItem]:
        """Get indicator completion items"""
        items = []
        
        for indicator_name, file_path in self.code_index['indicators'].items():
            items.append(CompletionItem(
                label=indicator_name,
                kind=CompletionItemKind.FUNCTION,
                detail=f"Indicator in {file_path}",
                documentation=f"Technical indicator: {indicator_name}"
            ))
        
        return items

    def _get_code_snippets(self) -> List[CompletionItem]:
        """Get code snippets for common tasks"""
        snippets = [
            CompletionItem(
                label="load_financial_data",
                kind=CompletionItemKind.SNIPPET,
                detail="Load financial data from CSV",
                documentation="Load and prepare financial data for analysis",
                insert_text="""# Load financial data
csv_path = 'mql5_feed/CSVExport_${1:BTCUSD}_PERIOD_${2:D1}.csv'
df = pd.read_csv(csv_path)
df['time'] = pd.to_datetime(df['time'])
df.set_index('time', inplace=True)
print(f"Loaded {len(df)} records for ${1:BTCUSD} ${2:D1}")"""
            ),
            CompletionItem(
                label="calculate_indicators",
                kind=CompletionItemKind.SNIPPET,
                detail="Calculate technical indicators",
                documentation="Calculate common technical indicators",
                insert_text="""# Calculate technical indicators
df['sma_20'] = df['close'].rolling(window=20).mean()
df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
df['rsi'] = calculate_rsi(df['close'], period=14)
df['macd'], df['macd_signal'] = calculate_macd(df['close'])"""
            ),
            CompletionItem(
                label="plot_analysis",
                kind=CompletionItemKind.SNIPPET,
                detail="Create analysis plot",
                documentation="Create comprehensive analysis plot",
                insert_text="""# Create analysis plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

# Price and indicators
ax1.plot(df.index, df['close'], label='Close', alpha=0.7)
ax1.plot(df.index, df['sma_20'], label='SMA 20', alpha=0.7)
ax1.plot(df.index, df['ema_50'], label='EMA 50', alpha=0.7)
ax1.set_title('${1:BTCUSD} - ${2:D1} Analysis')
ax1.legend()
ax1.grid(True)

# RSI
ax2.plot(df.index, df['rsi'], label='RSI', color='purple')
ax2.axhline(y=70, color='r', linestyle='--', alpha=0.5)
ax2.axhline(y=30, color='g', linestyle='--', alpha=0.5)
ax2.set_ylabel('RSI')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()"""
            )
        ]
        
        return snippets

    def _handle_hover(self, request_id: Any, params: Dict) -> Dict:
        """Handle hover request"""
        return {
            "contents": {
                "kind": "markdown",
                "value": "**Neozork HLD Prediction Project**\n\nEnhanced MCP server for financial analysis and prediction."
            }
        }

    def _handle_definition(self, request_id: Any, params: Dict) -> Dict:
        """Handle definition request"""
        return {"uri": "", "range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 0}}}

    def _handle_references(self, request_id: Any, params: Dict) -> List[Dict]:
        """Handle references request"""
        return []

    def _handle_workspace_symbols(self, request_id: Any, params: Dict) -> List[Dict]:
        """Handle workspace symbols request"""
        symbols = []
        
        for func_name, files in self.code_index['functions'].items():
            symbols.append({
                "name": func_name,
                "kind": CompletionItemKind.FUNCTION.value,
                "location": {"uri": f"file://{files[0]}" if files else ""}
            })
        
        for class_name, files in self.code_index['classes'].items():
            symbols.append({
                "name": class_name,
                "kind": CompletionItemKind.CLASS.value,
                "location": {"uri": f"file://{files[0]}" if files else ""}
            })
        
        return symbols

    def _handle_workspace_files(self, request_id: Any, params: Dict) -> List[str]:
        """Handle workspace files request"""
        return list(self.project_files.keys())

    def _handle_project_info(self, request_id: Any, params: Dict) -> Dict:
        """Handle project info request"""
        return {
            "name": "Neozork HLD Prediction",
            "description": "Machine Learning enhancement of proprietary trading indicators",
            "files_count": len(self.project_files),
            "symbols_count": len(self.available_symbols),
            "timeframes_count": len(self.available_timeframes),
            "indicators_count": len(self.code_index['indicators']),
            "data_fetchers_count": len(self.code_index['data_fetchers']),
            "plotting_functions_count": len(self.code_index['plotting_functions'])
        }

    def _handle_financial_data(self, request_id: Any, params: Dict) -> Dict:
        """Handle financial data request"""
        return {
            "symbols": list(self.available_symbols),
            "timeframes": list(self.available_timeframes),
            "data_files": {k: asdict(v) for k, v in self.financial_data.items()}
        }

    def _handle_indicators(self, request_id: Any, params: Dict) -> Dict:
        """Handle indicators request"""
        return {
            "indicators": list(self.code_index['indicators'].keys()),
            "data_fetchers": list(self.code_index['data_fetchers'].keys()),
            "plotting_functions": list(self.code_index['plotting_functions'].keys())
        }

    def _handle_code_search(self, request_id: Any, params: Dict) -> Dict:
        """Handle code search request"""
        query = params.get("query", "").lower()
        results = {
            "functions": [],
            "classes": [],
            "indicators": []
        }
        
        # Search functions
        for func_name, files in self.code_index['functions'].items():
            if query in func_name.lower():
                results["functions"].append({"name": func_name, "files": files})
        
        # Search classes
        for class_name, files in self.code_index['classes'].items():
            if query in class_name.lower():
                results["classes"].append({"name": class_name, "files": files})
        
        # Search indicators
        for indicator_name, file_path in self.code_index['indicators'].items():
            if query in indicator_name.lower():
                results["indicators"].append({"name": indicator_name, "file": file_path})
        
        return results

    def _handle_snippets(self, request_id: Any, params: Dict) -> List[Dict]:
        """Handle snippets request"""
        return [asdict(snippet) for snippet in self._get_code_snippets()]

    def _handle_analysis(self, request_id: Any, params: Dict) -> Dict:
        """Handle analysis request"""
        return {
            "project_stats": {
                "total_files": len(self.project_files),
                "python_files": len([f for f in self.project_files.values() if f.extension == '.py']),
                "total_lines": sum(len(f.content.splitlines()) for f in self.project_files.values() if f.content)
            },
            "code_analysis": {
                "functions": len(self.code_index['functions']),
                "classes": len(self.code_index['classes']),
                "indicators": len(self.code_index['indicators'])
            },
            "financial_data": {
                "symbols": len(self.available_symbols),
                "timeframes": len(self.available_timeframes),
                "data_files": len(self.financial_data)
            }
        }

if __name__ == "__main__":
    server = CursorMCPServer()
    server.start()
