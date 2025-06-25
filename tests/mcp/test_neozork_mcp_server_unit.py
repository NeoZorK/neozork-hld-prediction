#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for Neozork MCP Server
Comprehensive unit test suite for the unified MCP server
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import logging
from datetime import datetime
import ast

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from neozork_mcp_server import (
    NeozorkMCPServer, 
    CompletionItem, 
    CompletionItemKind, 
    ProjectFile, 
    FinancialData,
    print_to_stderr
)

class TestCompletionItemKind:
    """Test CompletionItemKind enum"""
    
    def test_enum_values(self):
        """Test enum values are correctly defined"""
        assert CompletionItemKind.TEXT.value == 1
        assert CompletionItemKind.FUNCTION.value == 3
        assert CompletionItemKind.CLASS.value == 7
        assert CompletionItemKind.CONSTANT.value == 21
        assert CompletionItemKind.SNIPPET.value == 15

class TestCompletionItem:
    """Test CompletionItem dataclass"""
    
    def test_completion_item_creation(self):
        """Test CompletionItem creation with all fields"""
        item = CompletionItem(
            label="test_function",
            kind=CompletionItemKind.FUNCTION,
            detail="Test function detail",
            documentation="This is a test function",
            insert_text="test_function()",
            sort_text="test_function",
            filter_text="test_function",
            insert_text_format="plaintext",
            text_edit={"range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 0}}, "newText": "test_function()"},
            additional_text_edits=[{"range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 0}}, "newText": "import test"}],
            command={"command": "test.command", "title": "Test Command"},
            data={"key": "value"}
        )
        
        assert item.label == "test_function"
        assert item.kind == CompletionItemKind.FUNCTION
        assert item.detail == "Test function detail"
        assert item.documentation == "This is a test function"
        assert item.insert_text == "test_function()"
        assert item.sort_text == "test_function"
        assert item.filter_text == "test_function"
        assert item.insert_text_format == "plaintext"
        assert item.text_edit is not None
        assert item.additional_text_edits is not None
        assert item.command is not None
        assert item.data is not None
    
    def test_completion_item_minimal(self):
        """Test CompletionItem creation with minimal fields"""
        item = CompletionItem(
            label="minimal_item",
            kind=CompletionItemKind.TEXT
        )
        
        assert item.label == "minimal_item"
        assert item.kind == CompletionItemKind.TEXT
        assert item.detail is None
        assert item.documentation is None
        assert item.insert_text is None

class TestProjectFile:
    """Test ProjectFile dataclass"""
    
    def test_project_file_creation(self):
        """Test ProjectFile creation with all fields"""
        from datetime import datetime
        
        content = "def test_function(): pass"
        ast_tree = ast.parse(content)
        
        file_info = ProjectFile(
            path="src/test.py",
            extension=".py",
            size=1024,
            modified=datetime.now(),
            content=content,
            ast_tree=ast_tree
        )
        
        assert file_info.path == "src/test.py"
        assert file_info.extension == ".py"
        assert file_info.size == 1024
        assert file_info.content == content
        assert file_info.ast_tree is not None
    
    def test_project_file_minimal(self):
        """Test ProjectFile creation with minimal fields"""
        from datetime import datetime
        
        file_info = ProjectFile(
            path="src/test.py",
            extension=".py",
            size=1024,
            modified=datetime.now()
        )
        
        assert file_info.path == "src/test.py"
        assert file_info.extension == ".py"
        assert file_info.size == 1024
        assert file_info.content is None
        assert file_info.ast_tree is None

class TestFinancialData:
    """Test FinancialData dataclass"""
    
    def test_financial_data_creation(self):
        """Test FinancialData creation with all fields"""
        from datetime import datetime
        
        data = FinancialData(
            symbol="GBPUSD",
            timeframe="MN1",
            path="data/GBPUSD_MN1.csv",
            columns=["time", "open", "high", "low", "close", "volume"],
            sample_data=[["2023-01-01", "100.0", "101.0", "99.0", "100.5", "1000"]],
            size=2048,
            modified=datetime.now()
        )
        
        assert data.symbol == "GBPUSD"
        assert data.timeframe == "MN1"
        assert data.path == "data/GBPUSD_MN1.csv"
        assert data.columns == ["time", "open", "high", "low", "close", "volume"]
        assert len(data.sample_data) == 1
        assert data.size == 2048

class TestPrintToStderr:
    """Test print_to_stderr function"""
    
    def test_print_to_stderr(self, capsys):
        """Test print_to_stderr function"""
        print_to_stderr("Test message")
        captured = capsys.readouterr()
        assert "Test message" in captured.err
    
    def test_print_to_stderr_with_args(self, capsys):
        """Test print_to_stderr with multiple arguments"""
        print_to_stderr("Test", "message", "with", "args")
        captured = capsys.readouterr()
        assert "Test message with args" in captured.err

class TestNeozorkMCPServerUnit:
    """Unit tests for NeozorkMCPServer class"""
    
    @pytest.fixture
    def temp_project(self):
        """Create temporary project directory"""
        temp_dir = tempfile.mkdtemp()
        project_path = Path(temp_dir)
        
        # Create project structure
        (project_path / "src").mkdir()
        (project_path / "tests").mkdir()
        (project_path / "docs").mkdir()
        (project_path / "data").mkdir()
        (project_path / "logs").mkdir()
        
        # Create sample Python files
        (project_path / "src" / "main.py").write_text("""
def calculate_rsi(data, period=14):
    \"\"\"Calculate RSI indicator\"\"\"
    return data

class FinancialAnalyzer:
    \"\"\"Financial data analyzer\"\"\"
    def __init__(self):
        pass

def backtest_strategy(data, strategy_params):
    \"\"\"Backtest trading strategy\"\"\"
    return {"returns": 0.15, "sharpe": 1.2}
""")
        
        # Create sample financial data
        (project_path / "data" / "GBPUSD_MN1.csv").write_text("time,open,close\n2023-01-01,100,101")
        (project_path / "data" / "EURUSD_H1.csv").write_text("time,open,close\n2023-01-01,1.1000,1.1001")
        
        # Create sample config
        config = {
            "server_mode": "unified",
            "server_name": "Test Neozork MCP Server",
            "version": "2.0.0",
            "features": {
                "financial_data": True,
                "technical_indicators": True,
                "github_copilot": True
            }
        }
        
        (project_path / "neozork_mcp_config.json").write_text(json.dumps(config, indent=2))
        
        yield project_path
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def server(self, temp_project):
        """Create server instance"""
        with patch('neozork_mcp_server.print_to_stderr'):
            server = NeozorkMCPServer(project_root=temp_project)
            yield server
    
    def test_server_initialization(self, temp_project):
        """Test server initialization"""
        with patch('neozork_mcp_server.print_to_stderr'):
            server = NeozorkMCPServer(project_root=temp_project)
            
            assert server.project_root == temp_project
            assert server.logger is not None
            assert server.config is not None
            assert server.running is True
            assert len(server.project_files) > 0
            assert len(server.financial_data) > 0
            assert server.code_index is not None
            assert server.handlers is not None
    
    def test_load_config(self, temp_project):
        """Test configuration loading"""
        with patch('neozork_mcp_server.print_to_stderr'):
            server = NeozorkMCPServer(project_root=temp_project)
            
            config = server.config
            assert "server_mode" in config
            assert "server_name" in config
            assert "version" in config
            assert "features" in config
            assert config["server_mode"] == "unified"
            assert config["server_name"] == "Test Neozork MCP Server"
    
    def test_load_default_config(self):
        """Test default configuration when no config file exists"""
        with patch('neozork_mcp_server.print_to_stderr'):
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                server = NeozorkMCPServer(project_root=temp_path)
                
                config = server.config
                assert "server_mode" in config
                assert "server_name" in config
                assert "version" in config
                assert "features" in config
                assert config["server_mode"] == "unified"
                assert config["server_name"] == "Neozork Unified MCP Server"
    
    def test_setup_logging(self, temp_project):
        """Test logging setup"""
        with patch('neozork_mcp_server.print_to_stderr'):
            server = NeozorkMCPServer(project_root=temp_project)
            
            logger = server.logger
            assert logger is not None
            assert logger.name == 'neozork_mcp_server'
            assert logger.level in [logging.DEBUG, logging.INFO]
    
    def test_scan_project(self, server):
        """Test project scanning"""
        # Check that Python files are scanned
        assert len(server.project_files) > 0
        assert any('main.py' in file_path for file_path in server.project_files.keys())
        
        # Check that financial data is scanned
        assert len(server.financial_data) > 0
        assert any('GBPUSD' in data.symbol for data in server.financial_data.values())
        assert any('EURUSD' in data.symbol for data in server.financial_data.values())
    
    def test_index_code(self, server):
        """Test code indexing"""
        # Check that functions are indexed
        assert len(server.code_index['functions']) > 0
        assert any('calculate_rsi' in func_info['name'] for func_info in server.code_index['functions'].values())
        assert any('backtest_strategy' in func_info['name'] for func_info in server.code_index['functions'].values())
        
        # Check that classes are indexed
        assert len(server.code_index['classes']) > 0
        assert any('FinancialAnalyzer' in class_info['name'] for class_info in server.code_index['classes'].values())
    
    def test_handle_initialize(self, server):
        """Test initialize handler"""
        result = server._handle_initialize(1, {})
        
        assert "protocolVersion" in result
        assert "capabilities" in result
        assert "serverInfo" in result
        assert result["serverInfo"]["name"] == "Test Neozork MCP Server"
        assert result["serverInfo"]["version"] == "2.0.0"
    
    def test_handle_shutdown(self, server):
        """Test shutdown handler"""
        server._handle_shutdown(1, {})
        assert server.running is False
    
    def test_handle_exit(self, server):
        """Test exit handler"""
        server._handle_exit(1, {})
        assert server.running is False
    
    def test_handle_completion(self, server):
        """Test completion handler"""
        result = server._handle_completion(1, {})
        
        assert "isIncomplete" in result
        assert "items" in result
        assert isinstance(result["items"], list)
        
        # Check that we have project completions
        completion_labels = [item["label"] for item in result["items"]]
        assert any("calculate_rsi" in label for label in completion_labels)
        assert any("FinancialAnalyzer" in label for label in completion_labels)
        assert any("backtest_strategy" in label for label in completion_labels)
    
    def test_get_project_completions(self, server):
        """Test project completions"""
        completions = server._get_project_completions()
        
        assert len(completions) > 0
        
        # Check function completions
        func_completions = [c for c in completions if c.kind == CompletionItemKind.FUNCTION]
        assert len(func_completions) > 0
        assert any("calculate_rsi" in c.label for c in func_completions)
        assert any("backtest_strategy" in c.label for c in func_completions)
        
        # Check class completions
        class_completions = [c for c in completions if c.kind == CompletionItemKind.CLASS]
        assert len(class_completions) > 0
        assert any("FinancialAnalyzer" in c.label for c in class_completions)
    
    def test_get_financial_completions(self, server):
        """Test financial completions"""
        completions = server._get_financial_completions()
        
        assert len(completions) > 0
        
        # Check symbol completions
        symbol_completions = [c for c in completions if c.kind == CompletionItemKind.CONSTANT]
        assert len(symbol_completions) > 0
        assert any("GBPUSD" in c.label for c in symbol_completions)
        assert any("EURUSD" in c.label for c in symbol_completions)
    
    def test_get_indicator_completions(self, server):
        """Test indicator completions"""
        completions = server._get_indicator_completions()
        
        assert len(completions) > 0
        
        # Check that common indicators are included
        indicator_labels = [c.label for c in completions]
        assert "RSI" in indicator_labels
        assert "MACD" in indicator_labels
        assert "EMA" in indicator_labels
        assert "Bollinger_Bands" in indicator_labels
        assert "Kelly_Criterion" in indicator_labels
        assert "Monte_Carlo" in indicator_labels
    
    def test_get_code_snippets(self, server):
        """Test code snippets"""
        snippets = server._get_code_snippets()
        
        assert len(snippets) > 0
        
        # Check that snippets have correct structure
        for snippet in snippets:
            assert snippet.kind == CompletionItemKind.SNIPPET
            assert snippet.label is not None
            assert snippet.insert_text is not None
    
    def test_handle_hover(self, server):
        """Test hover handler"""
        result = server._handle_hover(1, {"textDocument": {"uri": "file://test.py"}, "position": {"line": 0, "character": 0}})
        
        assert "contents" in result
        assert isinstance(result["contents"], (list, dict))
    
    def test_handle_definition(self, server):
        """Test definition handler"""
        result = server._handle_definition(1, {"textDocument": {"uri": "file://test.py"}, "position": {"line": 0, "character": 0}})
        
        assert result is not None
        if result:  # If result is not empty
            assert "uri" in result
            assert "range" in result
    
    def test_handle_references(self, server):
        """Test references handler"""
        result = server._handle_references(1, {"textDocument": {"uri": "file://test.py"}, "position": {"line": 0, "character": 0}})
        
        assert isinstance(result, list)
    
    def test_handle_workspace_symbols(self, server):
        """Test workspace symbols handler"""
        result = server._handle_workspace_symbols(1, {})
        
        assert len(result) > 0
        assert all("name" in symbol for symbol in result)
        assert all("kind" in symbol for symbol in result)
        assert all("location" in symbol for symbol in result)
    
    def test_handle_workspace_files(self, server):
        """Test workspace files handler"""
        result = server._handle_workspace_files(1, {})
        
        assert len(result) > 0
        assert all(isinstance(file_path, str) for file_path in result)
        assert any("main.py" in file_path for file_path in result)
    
    def test_handle_project_info(self, server):
        """Test project info handler"""
        result = server._handle_project_info(1, {})
        
        assert "files_count" in result or "available_symbols" in result
        assert "available_symbols" in result
        assert "available_timeframes" in result
    
    def test_handle_financial_data(self, server):
        """Test financial data handler"""
        result = server._handle_financial_data(1, {})
        
        assert "data_files" in result or "symbols" in result
        assert "symbols" in result
        assert "timeframes" in result
    
    def test_handle_indicators(self, server):
        """Test indicators handler"""
        result = server._handle_indicators(1, {})
        
        assert "available_indicators" in result
    
    def test_handle_code_search(self, server):
        """Test code search handler"""
        result = server._handle_code_search(1, {"query": "calculate"})
        
        assert "results" in result
        assert isinstance(result["results"], list)
    
    def test_handle_snippets(self, server):
        """Test snippets handler"""
        result = server._handle_snippets(1, {})
        
        assert len(result) > 0
        for snippet in result:
            assert isinstance(snippet, dict)
            # Check for actual keys in snippets
            assert "name" in snippet
            assert "description" in snippet
            assert "code" in snippet
    
    def test_handle_analysis(self, server):
        """Test analysis handler"""
        result = server._handle_analysis(1, {})
        
        assert "file_types" in result or "project_size" in result
    
    def test_handle_suggestions(self, server):
        """Test suggestions handler"""
        result = server._handle_suggestions(1, {})
        
        assert "suggestions" in result
        assert isinstance(result["suggestions"], list)
    
    def test_handle_context(self, server):
        """Test context handler"""
        result = server._handle_context(1, {})
        
        assert "project_context" in result
    
    def test_handle_copilot_suggestions(self, server):
        """Test copilot suggestions handler"""
        result = server._handle_copilot_suggestions(1, {})
        
        assert "suggestions" in result
        assert isinstance(result["suggestions"], list)
    
    def test_handle_copilot_context(self, server):
        """Test copilot context handler"""
        result = server._handle_copilot_context(1, {})
        
        assert "common_patterns" in result or "project_structure" in result
    
    def test_save_state(self, server):
        """Test state saving"""
        server._save_state()
        
        state_file = server.project_root / "logs" / "neozork_mcp_state.json"
        assert state_file.exists()
        
        with open(state_file, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        assert "timestamp" in state
        assert "project_files_count" in state
        assert "financial_data_count" in state
        assert "available_symbols" in state
        assert "available_timeframes" in state
    
    def test_process_message(self, server):
        """Test message processing"""
        # Test valid message
        message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        
        with patch.object(server, '_send_response') as mock_send:
            server._process_message(message)
            mock_send.assert_called_once()
        
        # Test invalid message
        invalid_message = {"invalid": "message"}
        
        with patch.object(server, '_send_error') as mock_error:
            server._process_message(invalid_message)
            mock_error.assert_called_once()
    
    def test_send_response(self, server):
        """Test response sending"""
        with patch.object(server, '_send_message') as mock_send:
            server._send_response(1, {"result": "test"})
            mock_send.assert_called_once()
    
    def test_send_error(self, server):
        """Test error sending"""
        with patch.object(server, '_send_message') as mock_send:
            server._send_error(1, -1, "Test error")
            mock_send.assert_called_once()
    
    def test_send_message(self, server):
        """Test message sending"""
        with patch('sys.stdout') as mock_stdout:
            server._send_message({"test": "message"})
            mock_stdout.write.assert_called()

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 