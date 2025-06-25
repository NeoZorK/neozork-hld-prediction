#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for Cursor MCP Server
"""

import pytest
import json
import time
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import os
import logging

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from cursor_mcp_server import CursorMCPServer, CompletionItem, CompletionItemKind, ProjectFile, FinancialData

class TestCursorMCPServer:
    """Test Cursor MCP Server functionality"""
    
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
""")
        
        # Create sample financial data
        (project_path / "data" / "GBPUSD_MN1.csv").write_text("time,open,close\n2023-01-01,100,101")
        
        yield project_path
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def server(self, temp_project):
        """Create server instance"""
        # Create server with custom project root
        server = CursorMCPServer(project_root=temp_project)
        yield server
    
    def test_initialization(self, server):
        """Test server initialization"""
        assert server.project_root is not None
        assert server.logger is not None
        assert server.running is True
        assert len(server.project_files) > 0
        assert len(server.financial_data) > 0
    
    def test_scan_project(self, server):
        """Test project scanning"""
        # Check that Python files are scanned
        assert any('main.py' in file_path for file_path in server.project_files.keys())
        
        # Check that financial data is scanned
        assert len(server.financial_data) > 0
        assert any('GBPUSD' in data.symbol for data in server.financial_data.values())
    
    def test_index_code(self, server):
        """Test code indexing"""
        # Check that functions are indexed
        assert len(server.code_index['functions']) > 0
        assert any('calculate_rsi' in func_info['name'] for func_info in server.code_index['functions'].values())
        
        # Check that classes are indexed
        assert len(server.code_index['classes']) > 0
        assert any('FinancialAnalyzer' in class_info['name'] for class_info in server.code_index['classes'].values())
    
    def test_handle_initialize(self, server):
        """Test initialize handler"""
        result = server._handle_initialize(1, {})
        
        assert "protocolVersion" in result
        assert "capabilities" in result
        assert "serverInfo" in result
        assert result["serverInfo"]["name"] == "Cursor MCP Server"
    
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
    
    def test_get_project_completions(self, server):
        """Test project completions"""
        completions = server._get_project_completions()
        
        assert len(completions) > 0
        
        # Check function completions
        func_completions = [c for c in completions if c.kind == CompletionItemKind.FUNCTION]
        assert len(func_completions) > 0
        assert any("calculate_rsi" in c.label for c in func_completions)
        
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
    
    def test_get_indicator_completions(self, server):
        """Test indicator completions"""
        completions = server._get_indicator_completions()
        
        assert len(completions) > 0
        
        # Check that common indicators are included
        indicator_labels = [c.label for c in completions]
        assert "RSI" in indicator_labels
        assert "MACD" in indicator_labels
        assert "EMA" in indicator_labels
    
    def test_get_code_snippets(self, server):
        """Test code snippets"""
        completions = server._get_code_snippets()
        
        assert len(completions) > 0
        
        # Check that snippets have correct kind
        snippet_completions = [c for c in completions if c.kind == CompletionItemKind.SNIPPET]
        assert len(snippet_completions) > 0
        
        # Check that common snippets are included
        snippet_labels = [c.label for c in snippet_completions]
        assert "import_pandas" in snippet_labels
        assert "read_csv" in snippet_labels
    
    def test_handle_project_info(self, server):
        """Test project info handler"""
        result = server._handle_project_info(1, {})
        
        assert "name" in result
        assert "files_count" in result
        assert "financial_data_count" in result
        assert "available_symbols" in result
        assert "available_timeframes" in result
        assert result["name"] == "Neozork HLD Prediction"
    
    def test_handle_financial_data(self, server):
        """Test financial data handler"""
        result = server._handle_financial_data(1, {})
        
        assert "data_files" in result
        assert "symbols" in result
        assert "timeframes" in result
        assert len(result["data_files"]) > 0
        assert len(result["symbols"]) > 0
    
    def test_handle_indicators(self, server):
        """Test indicators handler"""
        result = server._handle_indicators(1, {})
        
        assert "available_indicators" in result
        assert len(result["available_indicators"]) > 0
        assert "RSI" in result["available_indicators"]
        assert "MACD" in result["available_indicators"]
    
    def test_handle_code_search(self, server):
        """Test code search handler"""
        result = server._handle_code_search(1, {"query": "calculate_rsi"})
        
        assert "query" in result
        assert "results" in result
        assert len(result["results"]) > 0
    
    def test_handle_snippets(self, server):
        """Test snippets handler"""
        result = server._handle_snippets(1, {})
        
        assert len(result) > 0
        assert all("name" in snippet for snippet in result)
        assert all("description" in snippet for snippet in result)
        assert all("code" in snippet for snippet in result)
    
    def test_handle_analysis(self, server):
        """Test analysis handler"""
        result = server._handle_analysis(1, {})
        
        assert "project_size" in result
        assert "file_types" in result
        assert "most_recent_file" in result
        assert result["project_size"] > 0
    
    def test_handle_suggestions(self, server):
        """Test suggestions handler"""
        result = server._handle_suggestions(1, {})
        
        assert "suggestions" in result
        assert len(result["suggestions"]) > 0
        assert all(isinstance(suggestion, str) for suggestion in result["suggestions"])
    
    def test_handle_context(self, server):
        """Test context handler"""
        result = server._handle_context(1, {})
        
        assert "project_context" in result
        context = result["project_context"]
        assert "type" in context
        assert "languages" in context
        assert "frameworks" in context
        assert "data_sources" in context
        assert context["type"] == "financial_analysis"
    
    def test_workspace_symbols(self, server):
        """Test workspace symbols handler"""
        result = server._handle_workspace_symbols(1, {})
        
        assert len(result) > 0
        assert all("name" in symbol for symbol in result)
        assert all("kind" in symbol for symbol in result)
        assert all("location" in symbol for symbol in result)
    
    def test_workspace_files(self, server):
        """Test workspace files handler"""
        result = server._handle_workspace_files(1, {})
        
        assert len(result) > 0
        assert all(isinstance(file_path, str) for file_path in result)
        assert any("main.py" in file_path for file_path in result)

class TestCompletionItem:
    """Test CompletionItem dataclass"""
    
    def test_completion_item_creation(self):
        """Test CompletionItem creation"""
        item = CompletionItem(
            label="test_function",
            kind=CompletionItemKind.FUNCTION,
            detail="Test function",
            documentation="This is a test function",
            insert_text="test_function()"
        )
        
        assert item.label == "test_function"
        assert item.kind == CompletionItemKind.FUNCTION
        assert item.detail == "Test function"
        assert item.documentation == "This is a test function"
        assert item.insert_text == "test_function()"

class TestProjectFile:
    """Test ProjectFile dataclass"""
    
    def test_project_file_creation(self):
        """Test ProjectFile creation"""
        from datetime import datetime
        
        file_info = ProjectFile(
            path="src/main.py",
            extension=".py",
            size=1024,
            modified=datetime.now(),
            content="print('Hello, World!')"
        )
        
        assert file_info.path == "src/main.py"
        assert file_info.extension == ".py"
        assert file_info.size == 1024
        assert file_info.content == "print('Hello, World!')"

class TestFinancialData:
    """Test FinancialData dataclass"""
    
    def test_financial_data_creation(self):
        """Test FinancialData creation"""
        from datetime import datetime
        
        data = FinancialData(
            symbol="GBPUSD",
            timeframe="MN1",
            path="data/GBPUSD_MN1.csv",
            columns=["time", "open", "close"],
            sample_data=[["2023-01-01", "100", "101"]],
            size=1024,
            modified=datetime.now()
        )
        
        assert data.symbol == "GBPUSD"
        assert data.timeframe == "MN1"
        assert data.path == "data/GBPUSD_MN1.csv"
        assert data.columns == ["time", "open", "close"]
        assert len(data.sample_data) == 1

class TestErrorHandling:
    """Test error handling"""
    
    @pytest.fixture
    def temp_project_with_errors(self):
        """Create temporary project with problematic files"""
        temp_dir = tempfile.mkdtemp()
        project_path = Path(temp_dir)
        
        # Create invalid Python file
        (project_path / "invalid.py").write_text("def invalid syntax {")
        
        # Create inaccessible directory
        (project_path / "inaccessible").mkdir()
        os.chmod(project_path / "inaccessible", 0o000)
        
        yield project_path
        
        # Cleanup
        os.chmod(project_path / "inaccessible", 0o755)
        shutil.rmtree(temp_dir)
    
    def test_handles_invalid_python_files(self, temp_project_with_errors):
        """Test handling of invalid Python files"""
        # Should not crash and should log warnings
        server = CursorMCPServer(project_root=temp_project_with_errors)
        assert server.project_root is not None
        assert server.logger is not None
    
    def test_handles_missing_files(self, temp_project):
        """Test handling of missing files"""
        server = CursorMCPServer(project_root=temp_project)
        
        # Test with non-existent file
        result = server._handle_definition(1, {"textDocument": {"uri": "file://nonexistent.py"}})
        assert result is not None

class TestPerformance:
    """Test performance aspects"""
    
    def test_large_project_scanning(self, temp_project):
        """Test scanning large project"""
        # Create many files
        for i in range(100):
            (temp_project / "src" / f"file_{i}.py").write_text(f"def func_{i}(): pass")
        
        start_time = time.time()
        server = CursorMCPServer(project_root=temp_project)
        end_time = time.time()
        
        # Should complete within reasonable time
        assert end_time - start_time < 10  # 10 seconds max
        assert len(server.project_files) >= 100
    
    def test_completion_response_time(self, server):
        """Test completion response time"""
        start_time = time.time()
        result = server._handle_completion(1, {})
        end_time = time.time()
        
        # Should respond quickly
        assert end_time - start_time < 1  # 1 second max
        assert "items" in result

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 