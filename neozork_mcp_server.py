#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NeoZorK Unified MCP Server
Modern, unified Model Context Protocol server for financial analysis projects
Supports all IDEs (Cursor, PyCharm, VS Code) with intelligent autocompletion and AI integration
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
import argparse
import os
import time

class CompletionItemKind(Enum):
    """LSP completion item kinds"""
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
    """LSP completion item"""
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
    """Project file information"""
    path: str
    extension: str
    size: int
    modified: datetime
    content: Optional[str] = None
    ast_tree: Optional[ast.AST] = None

@dataclass
class FinancialData:
    """Financial data metadata"""
    symbol: str
    timeframe: str
    path: str
    columns: List[str]
    sample_data: List[List[str]]
    size: int
    modified: datetime

def print_to_stderr(*args, **kwargs):
    """Print to stderr to avoid interfering with MCP protocol"""
    print(*args, **kwargs, file=sys.stderr)

class NeoZorKMCPServer:
    """Unified MCP Server for NeoZorK HLD Prediction Project"""
    
    def __init__(self, project_root: Path = None, config: Dict[str, Any] = None):
        self.project_root = project_root or Path(__file__).parent
        self.logger = self._setup_logging()
        self.config = config or self._load_config()
        self.running = True
        self.start_time = datetime.now()  # Add start time for uptime tracking
        self.ready = False  # Add ready flag
        
        # Print startup message
        print_to_stderr("🚀 Starting NeoZorK Unified MCP Server...")
        print_to_stderr(f"📁 Project root: {self.project_root}")
        print_to_stderr(f"🐍 Python version: {sys.version}")
        print_to_stderr(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print_to_stderr(f"🎯 Server mode: {self.config.get('server_mode', 'unified')}")
        
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
            "neozork/projectInfo": self._handle_project_info,
            "neozork/financialData": self._handle_financial_data,
            "neozork/indicators": self._handle_indicators,
            "neozork/codeSearch": self._handle_code_search,
            "neozork/snippets": self._handle_snippets,
            "neozork/analysis": self._handle_analysis,
            "neozork/suggestions": self._handle_suggestions,
            "neozork/context": self._handle_context,
            "neozork/status": self._handle_status,
            "neozork/health": self._handle_health,
            "neozork/ping": self._handle_ping,
            "neozork/metrics": self._handle_metrics,
            "neozork/diagnostics": self._handle_diagnostics,
            "neozork/version": self._handle_version,
            "neozork/capabilities": self._handle_capabilities,
            "neozork/restart": self._handle_restart,
            "neozork/reload": self._handle_reload,
            "github/copilot/suggestions": self._handle_copilot_suggestions,
            "github/copilot/context": self._handle_copilot_context
        }
        
        # Initialize project
        print_to_stderr("📊 Scanning project files...")
        self._scan_project()
        print_to_stderr("🔍 Indexing code...")
        self._index_code()
        
        # Set ready flag after initialization
        self.ready = True
        
        self.logger.info("NeoZorK Unified MCP Server initialized successfully")
        print_to_stderr("✅ NeoZorK Unified MCP Server initialized successfully")
        print_to_stderr("📈 Server Statistics:")
        print_to_stderr(f"   - Project files: {len(self.project_files)}")
        print_to_stderr(f"   - Financial symbols: {len(self.available_symbols)}")
        print_to_stderr(f"   - Timeframes: {len(self.available_timeframes)}")
        print_to_stderr(f"   - Functions indexed: {len(self.code_index['functions'])}")
        print_to_stderr(f"   - Classes indexed: {len(self.code_index['classes'])}")
        print_to_stderr("🔄 Server is ready to accept connections...")
        print_to_stderr("💡 Press Ctrl+C to stop the server")

    def _load_config(self) -> Dict[str, Any]:
        """Load server configuration"""
        config_path = self.project_root / "neozork_mcp_config.json"
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"Loaded config from {config_path}")
                return config
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
        
        # Default configuration
        return {
            "server_mode": "unified",
            "server_name": "NeoZorK Unified MCP Server",
            "version": "2.0.0",
            "features": {
                "financial_data": True,
                "technical_indicators": True,
                "github_copilot": True,
                "code_completion": True,
                "project_analysis": True,
                "ai_suggestions": True
            },
            "performance": {
                "max_files": 15000,
                "max_file_size": "10MB",
                "cache_enabled": True,
                "cache_size": "200MB",
                "indexing_timeout": 60
            },
            "logging": {
                "level": "INFO",
                "file": "logs/neozork_mcp.log",
                "max_size": "10MB",
                "backup_count": 5
            }
        }

    def _setup_logging(self) -> logging.Logger:
        """Setup enhanced logging system"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"neozork_mcp_{datetime.now().strftime('%Y%m%d')}.log"
        
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [NeozorkMCP] %(message)s'
        )
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        logger = logging.getLogger('neozork_mcp_server')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)
        
        return logger

    def _scan_project(self):
        """Scan and index project files"""
        self.logger.info("Scanning project files...")
        
        # Scan Python files - only essential directories
        essential_dirs = ['src', 'scripts', 'tests']
        scanned_files = 0
        indexed_files = 0
        
        for py_file in self.project_root.rglob("*.py"):
            scanned_files += 1
            if scanned_files % 50 == 0:
                self.logger.info(f"Scanned {scanned_files} Python files so far...")
                
            if any(ignore in str(py_file) for ignore in ['__pycache__', '.git', '.venv', 'build', '.uv_cache']):
                continue
            
            # Only scan files in essential directories or root level Python files
            relative_path = py_file.relative_to(self.project_root)
            if not any(essential_dir in str(relative_path) for essential_dir in essential_dirs) and len(relative_path.parts) > 1:
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                self.project_files[str(relative_path)] = ProjectFile(
                    path=str(relative_path),
                    extension='.py',
                    size=py_file.stat().st_size,
                    modified=datetime.fromtimestamp(py_file.stat().st_mtime),
                    content=content
                )
                indexed_files += 1
            except Exception as e:
                self.logger.warning(f"Failed to read {py_file}: {e}")
        
        self.logger.info(f"Project scanning completed: {scanned_files} files scanned, {indexed_files} files indexed")
        
        # Scan financial data (limited to metadata only)
        self._scan_financial_data()

    def _scan_financial_data(self):
        """Scan financial data files"""
        self.logger.info("Scanning financial data...")
        
        # Scan data directories - limit to avoid hanging
        data_dirs = ['data', 'mql5_feed']
        max_files_per_dir = 50  # Limit to prevent hanging
        
        for data_dir in data_dirs:
            data_path = self.project_root / data_dir
            if not data_path.exists():
                continue
                
            file_count = 0
            for file_path in data_path.rglob("*"):
                if file_count >= max_files_per_dir:
                    self.logger.info(f"Reached limit of {max_files_per_dir} files for {data_dir}, skipping remaining files")
                    break
                    
                if file_path.is_file() and file_path.suffix in ['.csv', '.parquet', '.json']:
                    # Skip very large files that might cause hanging
                    if file_path.stat().st_size > 10 * 1024 * 1024:  # Skip files larger than 10MB
                        continue
                        
                    try:
                        # Extract symbol and timeframe from filename
                        filename = file_path.stem
                        symbol = "UNKNOWN"
                        timeframe = "UNKNOWN"
                        
                        # Try to parse symbol and timeframe from filename
                        if '_' in filename:
                            parts = filename.split('_')
                            if len(parts) >= 2:
                                symbol = parts[0]
                                timeframe = parts[-1]
                        
                        # Read sample data (limited for performance)
                        sample_data = []
                        if file_path.suffix == '.csv' and file_path.stat().st_size < 1024 * 1024:  # Only read small CSV files
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    reader = csv.reader(f)
                                    sample_data = [row for row in reader][:3]  # First 3 rows only
                            except Exception:
                                sample_data = []
                        
                        self.financial_data[str(file_path)] = FinancialData(
                            symbol=symbol,
                            timeframe=timeframe,
                            path=str(file_path),
                            columns=sample_data[0] if sample_data else [],
                            sample_data=sample_data[1:] if len(sample_data) > 1 else [],
                            size=file_path.stat().st_size,
                            modified=datetime.fromtimestamp(file_path.stat().st_mtime)
                        )
                        
                        self.available_symbols.add(symbol)
                        self.available_timeframes.add(timeframe)
                        file_count += 1
                        
                    except Exception as e:
                        self.logger.warning(f"Failed to read financial data {file_path}: {e}")

    def _index_code(self):
        """Index code for better completion"""
        self.logger.info("Indexing code...")
        
        # Add timeout to prevent hanging
        import signal
        import time
        
        def timeout_handler(signum, frame):
            raise TimeoutError("Indexing timed out")
        
        # Set timeout for indexing (30 seconds)
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)
        
        try:
            file_count = 0
            total_files = len(self.project_files)
            self.logger.info(f"Starting to index {total_files} files...")
            
            for file_path, file_info in self.project_files.items():
                if file_count % 10 == 0:  # Log progress every 10 files
                    self.logger.info(f"Indexing progress: {file_count}/{total_files} files")
                
                if file_info.content:
                    try:
                        tree = ast.parse(file_info.content)
                        self._index_ast_node(tree, file_path)
                        file_count += 1
                    except Exception as e:
                        self.logger.warning(f"Failed to parse AST for {file_path}: {e}")
                        file_count += 1
                        
                # Check for timeout every 100 files
                if file_count % 100 == 0:
                    signal.alarm(30)  # Reset alarm
                    
        except TimeoutError:
            self.logger.warning("Indexing timed out, continuing with partial index")
        finally:
            signal.alarm(0)  # Cancel the alarm
            self.logger.info(f"Indexing completed: {file_count} files processed")

    def _index_ast_node(self, node: ast.AST, file_path: str):
        """Index AST node"""
        if isinstance(node, ast.FunctionDef):
            self._index_function(node, file_path)
        elif isinstance(node, ast.ClassDef):
            self._index_class(node, file_path)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            self._index_import(node, file_path)
        
        # Recursively process child nodes
        for child in ast.iter_child_nodes(node):
            self._index_ast_node(child, file_path)

    def _index_function(self, node: ast.FunctionDef, file_path: str):
        """Index function definition"""
        func_key = f"{file_path}:{node.name}"
        self.code_index['functions'][func_key] = {
            'name': node.name,
            'file': file_path,
            'line': node.lineno,
            'docstring': ast.get_docstring(node)
        }

    def _index_class(self, node: ast.ClassDef, file_path: str):
        """Index class definition"""
        class_key = f"{file_path}:{node.name}"
        self.code_index['classes'][class_key] = {
            'name': node.name,
            'file': file_path,
            'line': node.lineno,
            'docstring': ast.get_docstring(node)
        }

    def _index_import(self, node: ast.AST, file_path: str):
        """Index import statement"""
        if isinstance(node, ast.Import):
            for alias in node.names:
                self.code_index['imports'][alias.name] = file_path
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                self.code_index['imports'][f"{module}.{alias.name}"] = file_path

    def start(self):
        """Start the MCP server"""
        print_to_stderr("🔄 Starting MCP server loop...")
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        try:
            while self.running:
                # Read message from stdin with timeout
                try:
                    # Use select with timeout to prevent blocking indefinitely
                    ready, _, _ = select.select([sys.stdin], [], [], 1.0)
                    if ready:
                        line = sys.stdin.readline()
                        if not line:
                            break
                        
                        try:
                            message = json.loads(line)
                            self._process_message(message)
                        except json.JSONDecodeError as e:
                            self.logger.error(f"Invalid JSON: {e}")
                            continue
                        except Exception as e:
                            self.logger.error(f"Error processing message: {e}")
                            continue
                    else:
                        # No input available, continue loop
                        continue
                        
                except Exception as e:
                    self.logger.error(f"Error reading from stdin: {e}")
                    # If stdin is not available (background mode), keep running
                    time.sleep(1)
                    continue
                        
        except KeyboardInterrupt:
            print_to_stderr("🛑 Received interrupt signal")
        except Exception as e:
            self.logger.error(f"Server error: {e}")
            print_to_stderr(f"❌ Server error: {e}")
        finally:
            self._cleanup()

    def _signal_handler(self, sig, frame):
        """Handle shutdown signals"""
        print_to_stderr(f"🛑 Received signal {sig}")
        self.running = False

    def _cleanup(self):
        """Cleanup resources"""
        print_to_stderr("🧹 Cleaning up...")
        self._save_state()
        self.logger.info("Server shutdown complete")
        print_to_stderr("✅ Server shutdown complete")

    def _save_state(self):
        """Save server state"""
        try:
            state = {
                'timestamp': datetime.now().isoformat(),
                'project_files_count': len(self.project_files),
                'financial_data_count': len(self.financial_data),
                'available_symbols': list(self.available_symbols),
                'available_timeframes': list(self.available_timeframes)
            }
            
            state_file = self.project_root / "logs" / "neozork_mcp_state.json"
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2, default=str)
                
        except Exception as e:
            self.logger.error(f"Failed to save state: {e}")

    def _process_message(self, message: Dict):
        """Process incoming MCP message"""
        try:
            method = message.get("method")
            request_id = message.get("id")
            params = message.get("params", {})
            
            if method in self.handlers:
                result = self.handlers[method](request_id, params)
                if result is not None:
                    self._send_response(request_id, result)
            else:
                self._send_error(request_id, -32601, f"Method not found: {method}")
                
        except Exception as e:
            self.logger.error(f"Error processing message: {e}")
            self._send_error(message.get("id"), -32603, f"Internal error: {e}")

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
        self._send_message(response)

    def _send_message(self, message: Dict):
        """Send message to client"""
        try:
            json.dump(message, sys.stdout)
            sys.stdout.write('\n')
            sys.stdout.flush()
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")

    def _handle_initialize(self, request_id: Any, params: Dict) -> Dict:
        """Handle initialize request"""
        self.logger.info("Received initialize request")
        
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "completionProvider": {
                    "triggerCharacters": [".", ":", "(", "[", "{", "\"", "'"]
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
                "name": self.config.get("server_name", "NeoZorK Unified MCP Server"),
                "version": self.config.get("version", "2.0.0")
            }
        }

    def _handle_shutdown(self, request_id: Any, params: Dict) -> None:
        """Handle shutdown request"""
        self.logger.info("Received shutdown request")
        self.running = False

    def _handle_exit(self, request_id: Any, params: Dict) -> None:
        """Handle exit request"""
        self.logger.info("Received exit request")
        self.running = False

    def _handle_completion(self, request_id: Any, params: Dict) -> Dict:
        """Handle completion request"""
        self.logger.debug("Received completion request")
        
        completions = []
        
        # Add project-specific completions
        completions.extend(self._get_project_completions())
        
        # Add financial data completions
        completions.extend(self._get_financial_completions())
        
        # Add indicator completions
        completions.extend(self._get_indicator_completions())
        
        # Add code snippets
        completions.extend(self._get_code_snippets())
        
        return {
            "isIncomplete": False,
            "items": [asdict(item) for item in completions]
        }

    def _get_project_completions(self) -> List[CompletionItem]:
        """Get project-specific completions"""
        completions = []
        
        # Add function completions
        for func_key, func_info in self.code_index['functions'].items():
            completions.append(CompletionItem(
                label=func_info['name'],
                kind=CompletionItemKind.FUNCTION,
                detail=f"Function in {func_info['file']}",
                documentation=func_info.get('docstring', ''),
                insert_text=f"{func_info['name']}()"
            ))
        
        # Add class completions
        for class_key, class_info in self.code_index['classes'].items():
            completions.append(CompletionItem(
                label=class_info['name'],
                kind=CompletionItemKind.CLASS,
                detail=f"Class in {class_info['file']}",
                documentation=class_info.get('docstring', ''),
                insert_text=class_info['name']
            ))
        
        return completions

    def _get_financial_completions(self) -> List[CompletionItem]:
        """Get financial data completions"""
        completions = []
        
        # Add symbol completions
        for symbol in self.available_symbols:
            completions.append(CompletionItem(
                label=symbol,
                kind=CompletionItemKind.CONSTANT,
                detail="Financial symbol",
                documentation=f"Available financial symbol: {symbol}",
                insert_text=symbol
            ))
        
        # Add timeframe completions
        for timeframe in self.available_timeframes:
            completions.append(CompletionItem(
                label=timeframe,
                kind=CompletionItemKind.CONSTANT,
                detail="Timeframe",
                documentation=f"Available timeframe: {timeframe}",
                insert_text=timeframe
            ))
        
        return completions

    def _get_indicator_completions(self) -> List[CompletionItem]:
        """Get technical indicator completions"""
        indicators = [
            ("RSI", "Relative Strength Index"),
            ("MACD", "Moving Average Convergence Divergence"),
            ("EMA", "Exponential Moving Average"),
            ("SMA", "Simple Moving Average"),
            ("Bollinger_Bands", "Bollinger Bands"),
            ("ATR", "Average True Range"),
            ("Stochastic", "Stochastic Oscillator"),
            ("CCI", "Commodity Channel Index"),
            ("ADX", "Average Directional Index"),
            ("VWAP", "Volume Weighted Average Price"),
            ("OBV", "On-Balance Volume"),
            ("Donchian_Channels", "Donchian Channels"),
            ("Fibonacci_Retracements", "Fibonacci Retracements"),
            ("Pivot_Points", "Pivot Points"),
            ("HMA", "Hull Moving Average"),
            ("Kelly_Criterion", "Kelly Criterion"),
            ("Monte_Carlo", "Monte Carlo Simulation")
        ]
        
        completions = []
        for indicator, description in indicators:
            completions.append(CompletionItem(
                label=indicator,
                kind=CompletionItemKind.FUNCTION,
                detail=f"Technical Indicator: {indicator}",
                documentation=description,
                insert_text=indicator
            ))
        
        return completions

    def _get_code_snippets(self) -> List[CompletionItem]:
        """Get code snippets"""
        snippets = [
            ("import_pandas", "import pandas as pd", "Import pandas"),
            ("import_numpy", "import numpy as np", "Import numpy"),
            ("import_matplotlib", "import matplotlib.pyplot as plt", "Import matplotlib"),
            ("read_csv", "df = pd.read_csv('data.csv')", "Read CSV file"),
            ("read_parquet", "df = pd.read_parquet('data.parquet')", "Read Parquet file"),
            ("plot_data", "plt.plot(df['close'])\nplt.show()", "Plot data"),
            ("calculate_rsi", "rsi = calculate_rsi(df['close'], period=14)", "Calculate RSI"),
            ("calculate_macd", "macd = calculate_macd(df['close'])", "Calculate MACD"),
            ("backtest_strategy", "results = backtest_strategy(data, strategy_params)", "Backtest strategy"),
            ("ml_pipeline", "model = create_ml_pipeline(data, target)", "ML pipeline"),
            ("docker_setup", "docker compose up -d", "Start Docker services"),
            ("run_tests", "python -m pytest tests/ -v", "Run tests"),
            ("run_analysis", "python run_analysis.py show --symbol BTCUSD --timeframe D1", "Run analysis")
        ]
        
        completions = []
        for snippet_id, code, description in snippets:
            completions.append(CompletionItem(
                label=snippet_id,
                kind=CompletionItemKind.SNIPPET,
                detail=description,
                documentation=code,
                insert_text=code
            ))
        
        return completions

    def _handle_hover(self, request_id: Any, params: Dict) -> Dict:
        """Handle hover request"""
        return {
            "contents": {
                "kind": "markdown",
                "value": "**NeoZorK Unified MCP Server**\n\nEnhanced MCP server for financial data analysis with AI integration"
            }
        }

    def _handle_definition(self, request_id: Any, params: Dict) -> Dict:
        """Handle definition request"""
        return {
            "uri": f"file://{self.project_root}/README.md",
            "range": {
                "start": {"line": 0, "character": 0},
                "end": {"line": 0, "character": 10}
            }
        }

    def _handle_references(self, request_id: Any, params: Dict) -> List[Dict]:
        """Handle references request"""
        return []

    def _handle_workspace_symbols(self, request_id: Any, params: Dict) -> List[Dict]:
        """Handle workspace symbols request"""
        symbols = []
        
        # Add function symbols
        for func_key, func_info in self.code_index['functions'].items():
            symbols.append({
                "name": func_info['name'],
                "kind": 12,  # Function
                "location": {
                    "uri": f"file://{self.project_root}/{func_info['file']}",
                    "range": {
                        "start": {"line": func_info['line'] - 1, "character": 0},
                        "end": {"line": func_info['line'] - 1, "character": 0}
                    }
                }
            })
        
        # Add class symbols
        for class_key, class_info in self.code_index['classes'].items():
            symbols.append({
                "name": class_info['name'],
                "kind": 5,  # Class
                "location": {
                    "uri": f"file://{self.project_root}/{class_info['file']}",
                    "range": {
                        "start": {"line": class_info['line'] - 1, "character": 0},
                        "end": {"line": class_info['line'] - 1, "character": 0}
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
            "name": "NeoZorK HLD Prediction",
            "files_count": len(self.project_files),
            "financial_data_count": len(self.financial_data),
            "available_symbols": list(self.available_symbols),
            "available_timeframes": list(self.available_timeframes),
            "functions_count": len(self.code_index['functions']),
            "classes_count": len(self.code_index['classes'])
        }

    def _handle_financial_data(self, request_id: Any, params: Dict) -> Dict:
        """Handle financial data request"""
        return {
            "data_files": list(self.financial_data.keys()),
            "symbols": list(self.available_symbols),
            "timeframes": list(self.available_timeframes)
        }

    def _handle_indicators(self, request_id: Any, params: Dict) -> Dict:
        """Handle indicators request"""
        return {
            "available_indicators": [
                "RSI", "MACD", "EMA", "SMA", "Bollinger_Bands",
                "ATR", "Stochastic", "CCI", "ADX", "VWAP",
                "OBV", "Donchian_Channels", "Fibonacci_Retracements",
                "Pivot_Points", "HMA", "Kelly_Criterion", "Monte_Carlo"
            ]
        }

    def _handle_code_search(self, request_id: Any, params: Dict) -> Dict:
        """Handle code search request"""
        query = params.get("query", "")
        results = []
        
        for file_path, file_info in self.project_files.items():
            if query.lower() in file_info.content.lower():
                results.append({
                    "file": file_path,
                    "matches": file_info.content.count(query)
                })
        
        return {
            "query": query,
            "results": results
        }

    def _handle_snippets(self, request_id: Any, params: Dict) -> List[Dict]:
        """Handle snippets request"""
        return [
            {
                "name": "import_pandas",
                "description": "Import pandas library",
                "code": "import pandas as pd"
            },
            {
                "name": "read_financial_data",
                "description": "Read financial data file",
                "code": "df = pd.read_csv('data/financial_data.csv')"
            },
            {
                "name": "backtest_strategy",
                "description": "Backtest trading strategy",
                "code": "results = backtest_strategy(data, strategy_params)"
            }
        ]

    def _handle_analysis(self, request_id: Any, params: Dict) -> Dict:
        """Handle analysis request"""
        return {
            "project_size": sum(f.size for f in self.project_files.values()),
            "file_types": list(set(f.extension for f in self.project_files.values())),
            "most_recent_file": max(self.project_files.values(), key=lambda x: x.modified).path
        }

    def _handle_suggestions(self, request_id: Any, params: Dict) -> Dict:
        """Handle suggestions request"""
        return {
            "suggestions": [
                "Consider adding more technical indicators",
                "Implement data validation for financial data",
                "Add unit tests for new features",
                "Optimize data loading performance",
                "Add real-time data streaming capabilities",
                "Implement machine learning models for prediction",
                "Add risk management features",
                "Create comprehensive documentation"
            ]
        }

    def _handle_context(self, request_id: Any, params: Dict) -> Dict:
        """Handle context request"""
        return {
            "project_context": {
                "type": "financial_analysis",
                "languages": ["Python"],
                "frameworks": ["pandas", "numpy", "matplotlib", "scikit-learn"],
                "data_sources": list(self.available_symbols),
                "features": ["technical_analysis", "machine_learning", "backtesting", "risk_management"]
            }
        }

    def _handle_copilot_suggestions(self, request_id: Any, params: Dict) -> Dict:
        """Handle GitHub Copilot suggestions"""
        context = params.get("context", "")
        
        suggestions = []
        
        if "financial" in context.lower() or "data" in context.lower():
            suggestions.extend([
                "Load financial data using pandas",
                "Calculate technical indicators",
                "Perform data validation",
                "Create visualization plots"
            ])
        
        if "test" in context.lower():
            suggestions.extend([
                "Write unit tests for functions",
                "Create integration tests",
                "Add test data fixtures",
                "Implement test coverage"
            ])
        
        if "docker" in context.lower():
            suggestions.extend([
                "Create Dockerfile for containerization",
                "Set up docker-compose for services",
                "Configure environment variables",
                "Add health checks"
            ])
        
        return {
            "suggestions": suggestions,
            "context": context
        }

    def _handle_copilot_context(self, request_id: Any, params: Dict) -> Dict:
        """Handle GitHub Copilot context"""
        return {
            "project_structure": {
                "src": "Source code directory",
                "tests": "Test files directory",
                "docs": "Documentation directory",
                "data": "Data files directory",
                "scripts": "Utility scripts directory"
            },
            "key_files": {
                "run_analysis.py": "Main analysis script",
                "neozork_mcp_server.py": "MCP server for IDE integration",
                "docker-compose.yml": "Docker services configuration",
                "pyproject.toml": "Project configuration and dependencies"
            },
            "common_patterns": [
                "Financial data loading and preprocessing",
                "Technical indicator calculations",
                "Backtesting strategies",
                "Machine learning model training",
                "Data visualization and plotting"
            ]
        }

    def _handle_status(self, request_id: Any, params: Dict) -> Dict:
        """Handle status request"""
        return {
            "status": "running" if self.running else "stopped",
            "ready": self.ready,
            "initialization_status": "ready" if self.ready else "initializing",
            "uptime": (datetime.now() - self.start_time).total_seconds() if hasattr(self, 'start_time') else 0,
            "server_mode": self.config.get("server_mode", "unified"),
            "version": self.config.get("version", "2.0.0"),
            "project_root": str(self.project_root),
            "python_version": sys.version,
            "platform": sys.platform,
            "memory_usage": self._get_memory_usage(),
            "cpu_usage": self._get_cpu_usage(),
            "active_connections": self._get_active_connections(),
            "last_activity": self._get_last_activity()
        }

    def _handle_health(self, request_id: Any, params: Dict) -> Dict:
        """Handle health check request"""
        health_status = "healthy"
        issues = []
        
        # Check if server is running
        if not self.running:
            health_status = "unhealthy"
            issues.append("Server is not running")
        
        # Check if server is ready
        if not self.ready:
            health_status = "initializing"
            issues.append("Server is still initializing")
        
        # Check project files
        if len(self.project_files) == 0:
            health_status = "warning"
            issues.append("No project files found")
        
        # Check financial data
        if len(self.financial_data) == 0:
            health_status = "warning"
            issues.append("No financial data found")
        
        # Check code index
        if len(self.code_index['functions']) == 0:
            health_status = "warning"
            issues.append("No functions indexed")
        
        return {
            "status": health_status,
            "ready": self.ready,
            "initialization_status": "ready" if self.ready else "initializing",
            "issues": issues,
            "checks": {
                "server_running": self.running,
                "server_ready": self.ready,
                "project_files_count": len(self.project_files),
                "financial_data_count": len(self.financial_data),
                "functions_indexed": len(self.code_index['functions']),
                "classes_indexed": len(self.code_index['classes']),
                "available_symbols": len(self.available_symbols),
                "available_timeframes": len(self.available_timeframes)
            },
            "timestamp": datetime.now().isoformat()
        }

    def _handle_ping(self, request_id: Any, params: Dict) -> Dict:
        """Handle ping request"""
        response = {
            "pong": True,
            "timestamp": datetime.now().isoformat(),
            "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "timezone": "UTC",
            "ready": self.ready,
            "initialization_status": "ready" if self.ready else "initializing"
        }
        
        if not self.ready:
            response["message"] = "Server is still initializing, please wait..."
            response["estimated_wait"] = "5-30 seconds"
        
        return response

    def _handle_metrics(self, request_id: Any, params: Dict) -> Dict:
        """Handle metrics request"""
        return {
            "performance": {
                "uptime_seconds": (datetime.now() - self.start_time).total_seconds() if hasattr(self, 'start_time') else 0,
                "memory_usage_mb": self._get_memory_usage(),
                "cpu_usage_percent": self._get_cpu_usage(),
                "files_processed": len(self.project_files),
                "indexing_time_ms": getattr(self, 'indexing_time', 0)
            },
            "project": {
                "total_files": len(self.project_files),
                "python_files": len([f for f in self.project_files.values() if f.extension == '.py']),
                "data_files": len([f for f in self.project_files.values() if f.extension in ['.csv', '.parquet', '.json']]),
                "total_size_bytes": sum(f.size for f in self.project_files.values()),
                "largest_file": max(self.project_files.values(), key=lambda x: x.size).path if self.project_files else None
            },
            "code_analysis": {
                "functions_count": len(self.code_index['functions']),
                "classes_count": len(self.code_index['classes']),
                "imports_count": len(self.code_index['imports']),
                "docstrings_count": len(self.code_index['docstrings']),
                "indicators_count": len(self.code_index['indicators']),
                "data_fetchers_count": len(self.code_index['data_fetchers']),
                "plotting_functions_count": len(self.code_index['plotting_functions'])
            },
            "financial_data": {
                "symbols_count": len(self.available_symbols),
                "timeframes_count": len(self.available_timeframes),
                "data_files_count": len(self.financial_data),
                "total_data_size_bytes": sum(d.size for d in self.financial_data.values())
            }
        }

    def _handle_diagnostics(self, request_id: Any, params: Dict) -> Dict:
        """Handle diagnostics request"""
        return {
            "system": {
                "python_version": sys.version,
                "platform": sys.platform,
                "architecture": sys.maxsize > 2**32 and "64-bit" or "32-bit",
                "executable": sys.executable,
                "path": sys.path[:5]  # First 5 entries
            },
            "server": {
                "config": self.config,
                "project_root": str(self.project_root),
                "running": self.running,
                "handlers_count": len(self.handlers),
                "logger_level": self.logger.level,
                "logger_handlers": len(self.logger.handlers)
            },
            "project": {
                "files_by_extension": self._get_files_by_extension(),
                "largest_files": self._get_largest_files(10),
                "recent_files": self._get_recent_files(10),
                "missing_directories": self._get_missing_directories()
            },
            "issues": self._get_diagnostic_issues()
        }

    def _handle_version(self, request_id: Any, params: Dict) -> Dict:
        """Handle version request"""
        return {
            "server_version": self.config.get("version", "2.0.0"),
            "python_version": sys.version,
            "platform": sys.platform,
            "build_date": "2025-06-25",
            "features": self.config.get("features", {}),
            "capabilities": self._get_server_capabilities()
        }

    def _handle_capabilities(self, request_id: Any, params: Dict) -> Dict:
        """Handle capabilities request"""
        return {
            "capabilities": self._get_server_capabilities(),
            "supported_methods": list(self.handlers.keys()),
            "features": self.config.get("features", {}),
            "extensions": [
                "neozork/financialData",
                "neozork/indicators", 
                "neozork/codeSearch",
                "neozork/snippets",
                "neozork/analysis",
                "neozork/status",
                "neozork/health",
                "neozork/metrics",
                "github/copilot/suggestions"
            ]
        }

    def _handle_restart(self, request_id: Any, params: Dict) -> Dict:
        """Handle restart request"""
        try:
            self.logger.info("Restarting server...")
            # Save current state
            self._save_state()
            
            # Reset server state
            self.running = True
            self.start_time = datetime.now()
            
            # Re-scan project
            self._scan_project()
            self._index_code()
            
            self.logger.info("Server restarted successfully")
            return {
                "status": "restarted",
                "timestamp": datetime.now().isoformat(),
                "message": "Server restarted successfully"
            }
        except Exception as e:
            self.logger.error(f"Failed to restart server: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _handle_reload(self, request_id: Any, params: Dict) -> Dict:
        """Handle reload request"""
        try:
            self.logger.info("Reloading project data...")
            
            # Clear current data
            self.project_files.clear()
            self.financial_data.clear()
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
            self.available_symbols.clear()
            self.available_timeframes.clear()
            
            # Re-scan everything
            self._scan_project()
            self._index_code()
            
            self.logger.info("Project data reloaded successfully")
            return {
                "status": "reloaded",
                "timestamp": datetime.now().isoformat(),
                "message": "Project data reloaded successfully",
                "files_count": len(self.project_files),
                "symbols_count": len(self.available_symbols)
            }
        except Exception as e:
            self.logger.error(f"Failed to reload project data: {e}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    # Helper methods for diagnostics and monitoring
    def _get_memory_usage(self) -> float:
        """Get memory usage in MB"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except ImportError:
            return 0.0

    def _get_cpu_usage(self) -> float:
        """Get CPU usage percentage"""
        try:
            import psutil
            return psutil.cpu_percent(interval=0.1)
        except ImportError:
            return 0.0

    def _get_active_connections(self) -> int:
        """Get number of active connections"""
        # For stdio-based MCP server, this is typically 1
        return 1 if self.running else 0

    def _get_last_activity(self) -> str:
        """Get last activity timestamp"""
        return getattr(self, 'last_activity', datetime.now()).isoformat()

    def _get_files_by_extension(self) -> Dict[str, int]:
        """Get file count by extension"""
        extensions = {}
        for file_info in self.project_files.values():
            ext = file_info.extension
            extensions[ext] = extensions.get(ext, 0) + 1
        return extensions

    def _get_largest_files(self, count: int = 10) -> List[Dict]:
        """Get largest files"""
        sorted_files = sorted(self.project_files.values(), key=lambda x: x.size, reverse=True)
        return [
            {"path": f.path, "size": f.size, "extension": f.extension}
            for f in sorted_files[:count]
        ]

    def _get_recent_files(self, count: int = 10) -> List[Dict]:
        """Get most recently modified files"""
        sorted_files = sorted(self.project_files.values(), key=lambda x: x.modified, reverse=True)
        return [
            {"path": f.path, "modified": f.modified.isoformat(), "size": f.size}
            for f in sorted_files[:count]
        ]

    def _get_missing_directories(self) -> List[str]:
        """Get missing expected directories"""
        expected_dirs = ['src', 'tests', 'docs', 'data', 'logs']
        missing = []
        for dir_name in expected_dirs:
            if not (self.project_root / dir_name).exists():
                missing.append(dir_name)
        return missing

    def _get_diagnostic_issues(self) -> List[Dict]:
        """Get diagnostic issues"""
        issues = []
        
        if len(self.project_files) == 0:
            issues.append({
                "type": "warning",
                "message": "No project files found",
                "suggestion": "Check project root path"
            })
        
        if len(self.financial_data) == 0:
            issues.append({
                "type": "info",
                "message": "No financial data found",
                "suggestion": "Add data files to data/ directory"
            })
        
        if len(self.code_index['functions']) == 0:
            issues.append({
                "type": "warning",
                "message": "No functions indexed",
                "suggestion": "Check Python files in src/ directory"
            })
        
        return issues

    def _get_server_capabilities(self) -> Dict:
        """Get server capabilities"""
        return {
            "textDocument": {
                "completion": {"completionItem": {"snippetSupport": True}},
                "hover": {"contentFormat": ["markdown", "plaintext"]},
                "definition": {"definitionProvider": True},
                "references": {"referencesProvider": True}
            },
            "workspace": {
                "symbol": {"symbolProvider": True},
                "workspaceFolders": {"supported": True}
            },
            "neozork": {
                "financialData": True,
                "indicators": True,
                "codeSearch": True,
                "snippets": True,
                "analysis": True,
                "status": True,
                "health": True,
                "metrics": True,
                "diagnostics": True
            }
        }

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="NeoZorK Unified MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start server in stdio mode (for IDE integration)
  python neozork_mcp_server.py

  # Start with custom config
  python neozork_mcp_server.py --config custom_config.json

  # Start in debug mode
  python neozork_mcp_server.py --debug

  # Show version
  python neozork_mcp_server.py --version
        """
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--debug", "-d",
        action="store_true",
        help="Enable debug logging"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="NeoZorK Unified MCP Server 2.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        # Load custom config if provided
        config = None
        if args.config:
            config_path = Path(args.config)
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                print_to_stderr(f"❌ Configuration file not found: {config_path}")
                sys.exit(1)
        
        # Set debug logging if requested
        if args.debug:
            os.environ["LOG_LEVEL"] = "DEBUG"
        
        server = NeoZorKMCPServer(config=config)
        server.start()
        
    except Exception as e:
        print_to_stderr(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 