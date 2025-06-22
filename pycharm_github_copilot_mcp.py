#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PyCharm GitHub Copilot MCP Server for Neozork HLD Prediction Project
Enhanced MCP server optimized for PyCharm IDE with GitHub Copilot integration
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

class PyCharmGitHubCopilotMCPServer:
    """Enhanced MCP Server optimized for PyCharm IDE with GitHub Copilot integration"""
    
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
            "pycharm/projectInfo": self._handle_project_info,
            "pycharm/financialData": self._handle_financial_data,
            "pycharm/indicators": self._handle_indicators,
            "pycharm/codeSearch": self._handle_code_search,
            "pycharm/snippets": self._handle_snippets,
            "pycharm/analysis": self._handle_analysis,
            "github/copilot/suggestions": self._handle_copilot_suggestions,
            "github/copilot/context": self._handle_copilot_context
        }
        
        # Initialize project
        self._scan_project()
        self._index_code()
        
        self.logger.info("PyCharm GitHub Copilot MCP Server initialized successfully")

    def _setup_logging(self) -> logging.Logger:
        """Setup enhanced logging system"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"pycharm_copilot_mcp_{datetime.now().strftime('%Y%m%d')}.log"
        
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [PyCharmCopilotMCP] %(message)s'
        )
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        logger = logging.getLogger('pycharm_copilot_mcp_server')
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
                        
                        self.financial_data[f"{symbol}_{timeframe}"] = FinancialData(
                            symbol=symbol,
                            timeframe=timeframe,
                            path=str(csv_file.relative_to(self.project_root)),
                            columns=headers,
                            sample_data=sample_data,
                            size=csv_file.stat().st_size,
                            modified=datetime.fromtimestamp(csv_file.stat().st_mtime)
                        )
                except Exception as e:
                    self.logger.warning(f"Failed to read {csv_file}: {e}")

    def _index_code(self):
        """Index code for fast search and completion"""
        self.logger.info("Indexing project code...")
        
        for file_path, file_info in self.project_files.items():
            if file_info.content:
                try:
                    tree = ast.parse(file_info.content)
                    for node in ast.walk(tree):
                        self._index_ast_node(node, file_path)
                except Exception as e:
                    self.logger.warning(f"Failed to parse {file_path}: {e}")

    def _index_ast_node(self, node: ast.AST, file_path: str):
        """Index AST node for code search"""
        if isinstance(node, ast.FunctionDef):
            self._index_function(node, file_path)
        elif isinstance(node, ast.ClassDef):
            self._index_class(node, file_path)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            self._index_import(node, file_path)

    def _index_function(self, node: ast.FunctionDef, file_path: str):
        """Index function for code search"""
        func_name = node.name
        if not func_name.startswith('_'):
            if func_name not in self.code_index['functions']:
                self.code_index['functions'][func_name] = []
            if file_path not in self.code_index['functions'][func_name]:
                self.code_index['functions'][func_name].append(file_path)

    def _index_class(self, node: ast.ClassDef, file_path: str):
        """Index class for code search"""
        class_name = node.name
        if not class_name.startswith('_'):
            if class_name not in self.code_index['classes']:
                self.code_index['classes'][class_name] = []
            if file_path not in self.code_index['classes'][class_name]:
                self.code_index['classes'][class_name].append(file_path)

    def _index_import(self, node: ast.AST, file_path: str):
        """Index import for code search"""
        if isinstance(node, ast.Import):
            for alias in node.names:
                import_name = alias.name
                if import_name not in self.code_index['imports']:
                    self.code_index['imports'][import_name] = []
                if file_path not in self.code_index['imports'][import_name]:
                    self.code_index['imports'][import_name].append(file_path)

    def start(self):
        """Start the MCP server"""
        self.logger.info("Starting PyCharm GitHub Copilot MCP Server...")
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        try:
            while self.running:
                # Read from stdin
                if select.select([sys.stdin], [], [], 0.1)[0]:
                    line = sys.stdin.readline()
                    if not line:
                        break
                    
                    try:
                        message = json.loads(line)
                        self._process_message(message)
                    except json.JSONDecodeError as e:
                        self.logger.error(f"Invalid JSON: {e}")
                    except Exception as e:
                        self.logger.error(f"Error processing message: {e}")
                        self.logger.error(traceback.format_exc())
                        
        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal")
        finally:
            self.logger.info("Shutting down PyCharm GitHub Copilot MCP Server")

    def _signal_handler(self, sig, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Received signal {sig}")
        self.running = False

    def _process_message(self, message: Dict):
        """Process incoming MCP message"""
        if 'method' in message:
            method = message['method']
            request_id = message.get('id')
            params = message.get('params', {})
            
            if method in self.handlers:
                try:
                    result = self.handlers[method](request_id, params)
                    if result is not None:
                        self._send_response(request_id, result)
                except Exception as e:
                    self.logger.error(f"Error handling {method}: {e}")
                    self._send_error(request_id, -32603, f"Internal error: {str(e)}")
            else:
                self._send_error(request_id, -32601, f"Method not found: {method}")

    def _send_response(self, request_id: Any, result: Any):
        """Send response to client"""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }
        self._send_message(response)

    def _send_error(self, request_id: Any, code: int, message: str, data: Any = None):
        """Send error response to client"""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
        if data:
            response["error"]["data"] = data
        self._send_message(response)

    def _send_message(self, message: Dict):
        """Send message to client"""
        try:
            json.dump(message, sys.stdout)
            sys.stdout.write('\n')
            sys.stdout.flush()
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")

    def _handle_initialize(self, request_id: Any, params: Dict) -> Dict:
        """Handle initialize request"""
        self.logger.info("Handling initialize request")
        return {
            "capabilities": {
                "completionProvider": {
                    "resolveProvider": True,
                    "triggerCharacters": [".", ":", "(", "[", "{", "\"", "'"]
                },
                "hoverProvider": True,
                "definitionProvider": True,
                "referencesProvider": True,
                "workspaceSymbolProvider": True,
                "textDocumentSync": 1
            },
            "serverInfo": {
                "name": "PyCharm GitHub Copilot MCP Server",
                "version": "2.0.0"
            }
        }

    def _handle_shutdown(self, request_id: Any, params: Dict) -> None:
        """Handle shutdown request"""
        self.logger.info("Handling shutdown request")
        self.running = False

    def _handle_exit(self, request_id: Any, params: Dict) -> None:
        """Handle exit request"""
        self.logger.info("Handling exit request")
        sys.exit(0)

    def _handle_completion(self, request_id: Any, params: Dict) -> Dict:
        """Handle completion request"""
        self.logger.debug("Handling completion request")
        
        completions = []
        
        # Add project-specific completions
        completions.extend(self._get_project_completions())
        completions.extend(self._get_financial_completions())
        completions.extend(self._get_indicator_completions())
        completions.extend(self._get_code_snippets())
        
        return {
            "isIncomplete": False,
            "items": [asdict(item) for item in completions]
        }

    def _get_project_completions(self) -> List[CompletionItem]:
        """Get project-specific completions"""
        completions = []
        
        # Functions
        for func_name in self.code_index['functions']:
            completions.append(CompletionItem(
                label=func_name,
                kind=CompletionItemKind.FUNCTION,
                detail=f"Function from project",
                documentation=f"Function defined in project files",
                insert_text=f"{func_name}()"
            ))
        
        # Classes
        for class_name in self.code_index['classes']:
            completions.append(CompletionItem(
                label=class_name,
                kind=CompletionItemKind.CLASS,
                detail=f"Class from project",
                documentation=f"Class defined in project files",
                insert_text=class_name
            ))
        
        return completions

    def _get_financial_completions(self) -> List[CompletionItem]:
        """Get financial data completions"""
        completions = []
        
        # Symbols
        for symbol in self.available_symbols:
            completions.append(CompletionItem(
                label=symbol,
                kind=CompletionItemKind.CONSTANT,
                detail="Financial symbol",
                documentation=f"Available financial symbol: {symbol}",
                insert_text=f'"{symbol}"'
            ))
        
        # Timeframes
        for timeframe in self.available_timeframes:
            completions.append(CompletionItem(
                label=timeframe,
                kind=CompletionItemKind.CONSTANT,
                detail="Timeframe",
                documentation=f"Available timeframe: {timeframe}",
                insert_text=f'"{timeframe}"'
            ))
        
        return completions

    def _get_indicator_completions(self) -> List[CompletionItem]:
        """Get technical indicator completions"""
        indicators = [
            ("SMA", "Simple Moving Average"),
            ("EMA", "Exponential Moving Average"),
            ("RSI", "Relative Strength Index"),
            ("MACD", "Moving Average Convergence Divergence"),
            ("Bollinger_Bands", "Bollinger Bands"),
            ("ATR", "Average True Range"),
            ("Stochastic", "Stochastic Oscillator"),
            ("CCI", "Commodity Channel Index"),
            ("ADX", "Average Directional Index"),
            ("VWAP", "Volume Weighted Average Price")
        ]
        
        completions = []
        for indicator, description in indicators:
            completions.append(CompletionItem(
                label=indicator,
                kind=CompletionItemKind.FUNCTION,
                detail=f"Technical indicator: {description}",
                documentation=f"Calculate {description}",
                insert_text=f"calculate_{indicator.lower()}()"
            ))
        
        return completions

    def _get_code_snippets(self) -> List[CompletionItem]:
        """Get code snippets for common tasks"""
        snippets = [
            ("load_data", "Load financial data", "load_financial_data(symbol, timeframe)"),
            ("calculate_indicators", "Calculate technical indicators", "calculate_indicators(data)"),
            ("plot_analysis", "Create analysis plot", "plot_analysis(data, indicators)"),
            ("backtest_strategy", "Backtest trading strategy", "backtest_strategy(data, strategy)"),
            ("export_results", "Export analysis results", "export_results(results, format='csv')"),
            ("data_quality_check", "Check data quality", "check_data_quality(data)"),
            ("correlation_analysis", "Perform correlation analysis", "analyze_correlations(data)"),
            ("feature_engineering", "Engineer features", "engineer_features(data)"),
            ("model_training", "Train ML model", "train_model(X, y, model_type='random_forest')"),
            ("model_evaluation", "Evaluate model performance", "evaluate_model(model, X_test, y_test)")
        ]
        
        completions = []
        for snippet_name, description, insert_text in snippets:
            completions.append(CompletionItem(
                label=snippet_name,
                kind=CompletionItemKind.SNIPPET,
                detail=f"Code snippet: {description}",
                documentation=f"Snippet for {description}",
                insert_text=insert_text
            ))
        
        return completions

    def _handle_hover(self, request_id: Any, params: Dict) -> Dict:
        """Handle hover request"""
        return {
            "contents": {
                "kind": "markdown",
                "value": "PyCharm GitHub Copilot MCP Server - Enhanced financial analysis tools"
            }
        }

    def _handle_definition(self, request_id: Any, params: Dict) -> Dict:
        """Handle definition request"""
        return {
            "uri": "file:///path/to/definition",
            "range": {
                "start": {"line": 0, "character": 0},
                "end": {"line": 0, "character": 0}
            }
        }

    def _handle_references(self, request_id: Any, params: Dict) -> List[Dict]:
        """Handle references request"""
        return []

    def _handle_workspace_symbols(self, request_id: Any, params: Dict) -> List[Dict]:
        """Handle workspace symbols request"""
        symbols = []
        
        # Add functions
        for func_name, files in self.code_index['functions'].items():
            symbols.append({
                "name": func_name,
                "kind": CompletionItemKind.FUNCTION.value,
                "location": {
                    "uri": f"file:///{files[0]}" if files else "",
                    "range": {
                        "start": {"line": 0, "character": 0},
                        "end": {"line": 0, "character": 0}
                    }
                }
            })
        
        # Add classes
        for class_name, files in self.code_index['classes'].items():
            symbols.append({
                "name": class_name,
                "kind": CompletionItemKind.CLASS.value,
                "location": {
                    "uri": f"file:///{files[0]}" if files else "",
                    "range": {
                        "start": {"line": 0, "character": 0},
                        "end": {"line": 0, "character": 0}
                    }
                }
            })
        
        return symbols

    def _handle_workspace_files(self, request_id: Any, params: Dict) -> List[str]:
        """Handle workspace files request"""
        return list(self.project_files.keys())

    def _handle_project_info(self, request_id: Any, params: Dict) -> Dict:
        """Handle project info request"""
        return {
            "name": "Neozork HLD Prediction",
            "version": "2.0.0",
            "description": "Financial analysis and machine learning project",
            "files_count": len(self.project_files),
            "symbols_count": len(self.available_symbols),
            "timeframes_count": len(self.available_timeframes),
            "functions_count": len(self.code_index['functions']),
            "classes_count": len(self.code_index['classes'])
        }

    def _handle_financial_data(self, request_id: Any, params: Dict) -> Dict:
        """Handle financial data request"""
        return {
            "symbols": list(self.available_symbols),
            "timeframes": list(self.available_timeframes),
            "data_files": list(self.financial_data.keys())
        }

    def _handle_indicators(self, request_id: Any, params: Dict) -> Dict:
        """Handle indicators request"""
        return {
            "available_indicators": [
                "SMA", "EMA", "RSI", "MACD", "Bollinger_Bands",
                "ATR", "Stochastic", "CCI", "ADX", "VWAP"
            ]
        }

    def _handle_code_search(self, request_id: Any, params: Dict) -> Dict:
        """Handle code search request"""
        query = params.get('query', '')
        results = []
        
        # Search in functions
        for func_name in self.code_index['functions']:
            if query.lower() in func_name.lower():
                results.append({
                    "type": "function",
                    "name": func_name,
                    "files": self.code_index['functions'][func_name]
                })
        
        # Search in classes
        for class_name in self.code_index['classes']:
            if query.lower() in class_name.lower():
                results.append({
                    "type": "class",
                    "name": class_name,
                    "files": self.code_index['classes'][class_name]
                })
        
        return {"results": results}

    def _handle_snippets(self, request_id: Any, params: Dict) -> List[Dict]:
        """Handle snippets request"""
        return [
            {
                "name": "load_data",
                "description": "Load financial data",
                "code": "load_financial_data(symbol, timeframe)"
            }
        ]

    def _handle_analysis(self, request_id: Any, params: Dict) -> Dict:
        """Handle analysis request"""
        return {
            "project_stats": {
                "total_files": len(self.project_files),
                "python_files": len([f for f in self.project_files.values() if f.extension == '.py']),
                "total_size": sum(f.size for f in self.project_files.values()),
                "last_modified": max(f.modified for f in self.project_files.values()).isoformat()
            }
        }

    def _handle_copilot_suggestions(self, request_id: Any, params: Dict) -> Dict:
        """Handle GitHub Copilot suggestions request"""
        context = params.get('context', '')
        
        # Generate context-aware suggestions
        suggestions = []
        
        if 'financial' in context.lower() or 'data' in context.lower():
            suggestions.extend([
                "load_financial_data(symbol, timeframe)",
                "calculate_technical_indicators(data)",
                "plot_price_chart(data, indicators)"
            ])
        
        if 'analysis' in context.lower() or 'model' in context.lower():
            suggestions.extend([
                "perform_technical_analysis(data)",
                "train_ml_model(X, y)",
                "evaluate_model_performance(model, X_test, y_test)"
            ])
        
        return {"suggestions": suggestions}

    def _handle_copilot_context(self, request_id: Any, params: Dict) -> Dict:
        """Handle GitHub Copilot context request"""
        return {
            "project_type": "financial_analysis",
            "available_symbols": list(self.available_symbols),
            "available_timeframes": list(self.available_timeframes),
            "common_patterns": [
                "data loading and preprocessing",
                "technical indicator calculation",
                "visualization and plotting",
                "machine learning model training",
                "backtesting and evaluation"
            ]
        }

def main():
    """Main entry point"""
    server = PyCharmGitHubCopilotMCPServer()
    server.start()

if __name__ == "__main__":
    main()

