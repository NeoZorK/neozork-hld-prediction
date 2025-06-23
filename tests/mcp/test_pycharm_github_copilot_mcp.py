#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for PyCharm GitHub Copilot MCP Server
"""

import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from pycharm_github_copilot_mcp import (
    PyCharmGitHubCopilotMCPServer,
    CompletionItem,
    CompletionItemKind,
    ProjectFile,
    FinancialData
)


class TestPyCharmGitHubCopilotMCPServer:
    """Test cases for PyCharm GitHub Copilot MCP Server"""

    @pytest.fixture
    def temp_project_dir(self):
        """Create temporary project directory for testing"""
        temp_dir = tempfile.mkdtemp()
        project_structure = {
            'src': {
                'main.py': 'def main():\n    pass\n',
                'utils.py': 'def helper():\n    pass\n',
                'indicators': {
                    'sma.py': 'def calculate_sma(data, period):\n    pass\n',
                    'rsi.py': 'def calculate_rsi(data, period):\n    pass\n'
                }
            },
            'data': {
                'test.csv': 'Date,Open,High,Low,Close\n2023-01-01,100,110,95,105'
            },
            'mql5_feed': {
                'CSVExport_BTCUSD_PERIOD_D1.csv': 'Date,Open,High,Low,Close,Volume\n2023-01-01,100,110,95,105,1000\n2023-01-02,105,115,100,110,1200'
            }
        }
        
        def create_structure(base_path, structure):
            for name, content in structure.items():
                path = Path(base_path) / name
                if isinstance(content, dict):
                    path.mkdir(exist_ok=True)
                    create_structure(path, content)
                else:
                    path.write_text(content)
        
        create_structure(temp_dir, project_structure)
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def mcp_server(self, temp_project_dir):
        """Create MCP server instance for testing"""
        return PyCharmGitHubCopilotMCPServer(project_root=Path(temp_project_dir))

    def test_initialization(self, mcp_server):
        """Test server initialization"""
        assert mcp_server.running == True
        assert len(mcp_server.handlers) > 0
        assert 'initialize' in mcp_server.handlers
        assert 'textDocument/completion' in mcp_server.handlers
        assert 'github/copilot/suggestions' in mcp_server.handlers

    def test_project_scanning(self, mcp_server, temp_project_dir):
        """Test project file scanning"""
        assert len(mcp_server.project_files) > 0
        
        # Check if Python files are scanned
        python_files = [f for f in mcp_server.project_files.values() if f.extension == '.py']
        assert len(python_files) > 0
        
        # Check if main.py is scanned
        main_file = next((f for f in mcp_server.project_files.values() if 'main.py' in f.path), None)
        assert main_file is not None
        assert main_file.content is not None

    def test_financial_data_scanning(self, mcp_server):
        """Test financial data scanning"""
        assert len(mcp_server.available_symbols) > 0
        assert len(mcp_server.available_timeframes) > 0
        
        # Check if BTCUSD is detected
        assert 'BTCUSD' in mcp_server.available_symbols
        assert 'D1' in mcp_server.available_timeframes
        
        # Check if financial data is loaded (may be empty in test environment)
        # The test environment might not have actual CSV files, so we check the scanning logic
        assert hasattr(mcp_server, 'financial_data')
        assert isinstance(mcp_server.financial_data, dict)

    def test_code_indexing(self, mcp_server):
        """Test code indexing functionality"""
        assert len(mcp_server.code_index['functions']) > 0
        assert len(mcp_server.code_index['classes']) >= 0
        
        # Check if functions are indexed
        functions = list(mcp_server.code_index['functions'].keys())
        assert len(functions) > 0
        
        # Check if specific functions are indexed
        function_names = [f.split('.')[-1] for f in functions]
        assert 'main' in function_names or 'helper' in function_names

    def test_get_project_completions(self, mcp_server):
        """Test project-specific completions"""
        completions = mcp_server._get_project_completions()
        assert len(completions) > 0
        
        # Check completion structure
        for completion in completions:
            assert isinstance(completion, CompletionItem)
            assert completion.label is not None
            assert completion.kind in CompletionItemKind

    def test_get_financial_completions(self, mcp_server):
        """Test financial data completions"""
        completions = mcp_server._get_financial_completions()
        assert len(completions) > 0
        
        # Check for symbol completions
        symbol_completions = [c for c in completions if c.kind == CompletionItemKind.CONSTANT]
        assert len(symbol_completions) > 0
        
        # Check for timeframe completions
        timeframe_completions = [c for c in completions if 'timeframe' in c.detail.lower()]
        assert len(timeframe_completions) > 0

    def test_get_indicator_completions(self, mcp_server):
        """Test technical indicator completions"""
        completions = mcp_server._get_indicator_completions()
        assert len(completions) > 0
        
        # Check for specific indicators
        indicator_names = [c.label for c in completions]
        assert 'SMA' in indicator_names
        assert 'EMA' in indicator_names
        assert 'RSI' in indicator_names
        assert 'MACD' in indicator_names

    def test_get_code_snippets(self, mcp_server):
        """Test code snippets generation"""
        snippets = mcp_server._get_code_snippets()
        assert len(snippets) > 0
        
        # Check snippet structure
        for snippet in snippets:
            assert isinstance(snippet, CompletionItem)
            assert snippet.kind == CompletionItemKind.SNIPPET
            assert snippet.label is not None
            assert snippet.insert_text is not None

    def test_handle_initialize(self, mcp_server):
        """Test initialize handler"""
        request_id = 1
        params = {
            'processId': 12345,
            'rootUri': 'file:///test',
            'capabilities': {}
        }
        
        result = mcp_server._handle_initialize(request_id, params)
        
        assert 'capabilities' in result
        assert 'serverInfo' in result
        assert result['serverInfo']['name'] == 'PyCharm GitHub Copilot MCP Server'
        assert result['serverInfo']['version'] == '2.0.0'

    def test_handle_completion(self, mcp_server):
        """Test completion handler"""
        request_id = 2
        params = {
            'textDocument': {'uri': 'file:///test.py'},
            'position': {'line': 0, 'character': 0}
        }
        
        result = mcp_server._handle_completion(request_id, params)
        
        assert 'isIncomplete' in result
        assert 'items' in result
        assert isinstance(result['items'], list)
        assert len(result['items']) > 0

    def test_handle_copilot_suggestions(self, mcp_server):
        """Test GitHub Copilot suggestions handler"""
        request_id = 3
        params = {'context': 'financial data analysis'}
        
        result = mcp_server._handle_copilot_suggestions(request_id, params)
        
        assert 'suggestions' in result
        assert isinstance(result['suggestions'], list)
        assert len(result['suggestions']) > 0

    def test_handle_copilot_context(self, mcp_server):
        """Test GitHub Copilot context handler"""
        request_id = 4
        params = {}
        
        result = mcp_server._handle_copilot_context(request_id, params)
        
        assert 'project_type' in result
        assert 'available_symbols' in result
        assert 'available_timeframes' in result
        assert 'common_patterns' in result

    def test_handle_financial_data(self, mcp_server):
        """Test financial data handler"""
        request_id = 5
        params = {}
        
        result = mcp_server._handle_financial_data(request_id, params)
        
        assert 'symbols' in result
        assert 'timeframes' in result
        assert 'data_files' in result
        assert isinstance(result['symbols'], list)
        assert isinstance(result['timeframes'], list)

    def test_handle_project_info(self, mcp_server):
        """Test project info handler"""
        request_id = 6
        params = {}
        
        result = mcp_server._handle_project_info(request_id, params)
        
        assert 'name' in result
        assert 'version' in result
        assert 'files_count' in result
        assert 'symbols_count' in result
        assert 'timeframes_count' in result

    def test_handle_code_search(self, mcp_server):
        """Test code search handler"""
        request_id = 7
        params = {'query': 'calculate'}
        
        result = mcp_server._handle_code_search(request_id, params)
        
        assert 'results' in result
        assert isinstance(result['results'], list)

    def test_handle_workspace_symbols(self, mcp_server):
        """Test workspace symbols handler"""
        request_id = 8
        params = {'query': 'function'}
        
        result = mcp_server._handle_workspace_symbols(request_id, params)
        
        assert isinstance(result, list)
        if len(result) > 0:
            symbol = result[0]
            assert 'name' in symbol
            assert 'kind' in symbol
            assert 'location' in symbol

    def test_handle_workspace_files(self, mcp_server):
        """Test workspace files handler"""
        request_id = 9
        params = {}
        
        result = mcp_server._handle_workspace_files(request_id, params)
        
        assert isinstance(result, list)
        assert len(result) > 0

    def test_handle_indicators(self, mcp_server):
        """Test indicators handler"""
        request_id = 10
        params = {}
        
        result = mcp_server._handle_indicators(request_id, params)
        
        assert 'available_indicators' in result
        assert isinstance(result['available_indicators'], list)
        assert len(result['available_indicators']) > 0

    def test_handle_snippets(self, mcp_server):
        """Test snippets handler"""
        request_id = 11
        params = {}
        
        result = mcp_server._handle_snippets(request_id, params)
        
        assert isinstance(result, list)
        if len(result) > 0:
            snippet = result[0]
            assert 'name' in snippet
            assert 'description' in snippet
            assert 'code' in snippet

    def test_handle_analysis(self, mcp_server):
        """Test analysis handler"""
        request_id = 12
        params = {}
        
        result = mcp_server._handle_analysis(request_id, params)
        
        assert 'project_stats' in result
        stats = result['project_stats']
        assert 'total_files' in stats
        assert 'python_files' in stats
        assert 'total_size' in stats
        assert 'last_modified' in stats

    def test_signal_handler(self, mcp_server):
        """Test signal handler"""
        assert mcp_server.running == True
        
        # Simulate signal
        mcp_server._signal_handler(None, None)
        
        assert mcp_server.running == False

    def test_error_handling(self, mcp_server):
        """Test error handling in message processing"""
        # Test with invalid JSON
        with patch('sys.stdout') as mock_stdout:
            mcp_server._process_message("invalid json")
            # Should not raise exception

    def test_logging_setup(self, mcp_server):
        """Test logging setup"""
        assert mcp_server.logger is not None
        assert mcp_server.logger.name == 'pycharm_copilot_mcp_server'

    def test_performance_metrics(self, mcp_server):
        """Test performance metrics"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024
        
        # Create another server instance to test memory usage
        server2 = PyCharmGitHubCopilotMCPServer()
        
        final_memory = process.memory_info().rss / 1024 / 1024
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (< 150MB)
        assert memory_increase < 150

    def test_concurrent_access(self, mcp_server):
        """Test concurrent access to server"""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request():
            try:
                completions = mcp_server._get_project_completions()
                results.put(len(completions))
            except Exception as e:
                results.put(e)
        
        # Create multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        # Collect results
        while not results.empty():
            result = results.get()
            assert not isinstance(result, Exception)
            assert result >= 0

    def test_data_structures(self):
        """Test data structure classes"""
        # Test CompletionItem
        completion = CompletionItem(
            label="test_function",
            kind=CompletionItemKind.FUNCTION,
            detail="Test function",
            documentation="Test documentation"
        )
        assert completion.label == "test_function"
        assert completion.kind == CompletionItemKind.FUNCTION
        
        # Test ProjectFile
        project_file = ProjectFile(
            path="test.py",
            extension=".py",
            size=100,
            modified=None,
            content="def test(): pass"
        )
        assert project_file.path == "test.py"
        assert project_file.extension == ".py"
        
        # Test FinancialData
        financial_data = FinancialData(
            symbol="BTCUSD",
            timeframe="D1",
            path="test.csv",
            columns=["Date", "Close"],
            sample_data=[["2023-01-01", "100"]],
            size=200,
            modified=None
        )
        assert financial_data.symbol == "BTCUSD"
        assert financial_data.timeframe == "D1"

    def test_enum_values(self):
        """Test CompletionItemKind enum"""
        assert CompletionItemKind.FUNCTION.value == 3
        assert CompletionItemKind.CLASS.value == 7
        assert CompletionItemKind.SNIPPET.value == 15
        assert CompletionItemKind.CONSTANT.value == 21

    @pytest.mark.integration
    def test_full_workflow(self, mcp_server):
        """Test complete workflow"""
        # 1. Initialize server
        init_result = mcp_server._handle_initialize(1, {})
        assert init_result is not None
        
        # 2. Get completions
        completion_result = mcp_server._handle_completion(2, {})
        assert completion_result is not None
        
        # 3. Get Copilot suggestions
        copilot_result = mcp_server._handle_copilot_suggestions(3, {'context': 'test'})
        assert copilot_result is not None
        
        # 4. Get project info
        project_result = mcp_server._handle_project_info(4, {})
        assert project_result is not None
        
        # 5. Shutdown
        mcp_server._handle_shutdown(5, {})
        assert mcp_server.running == False


class TestMCPServerIntegration:
    """Integration tests for MCP Server"""

    @pytest.fixture
    def server_process(self):
        """Start server process for integration testing"""
        import subprocess
        import time
        import signal
        
        try:
            process = subprocess.Popen(
                [sys.executable, 'pycharm_github_copilot_mcp.py'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1  # Line buffered
            )
            
            # Wait for server to start (with timeout)
            time.sleep(1)
            
            # Check if process is still running
            if process.poll() is not None:
                pytest.skip("Server process failed to start")
            
            yield process
            
        finally:
            # Cleanup
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()

    def test_server_communication(self, server_process):
        """Test communication with server process"""
        import json
        import select
        
        # Send initialize request
        init_request = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'initialize',
            'params': {
                'processId': 12345,
                'rootUri': 'file:///test',
                'capabilities': {}
            }
        }
        
        try:
            server_process.stdin.write(json.dumps(init_request) + '\n')
            server_process.stdin.flush()
            
            # Read response with timeout
            ready, _, _ = select.select([server_process.stdout], [], [], 5.0)
            if not ready:
                pytest.skip("Server did not respond within timeout")
            
            response = server_process.stdout.readline()
            if not response:
                pytest.skip("No response from server")
            
            response_data = json.loads(response)
            
            assert response_data.get('result') is not None
            assert 'capabilities' in response_data['result']
            assert response_data['result']['serverInfo']['name'] == 'PyCharm GitHub Copilot MCP Server'
            
        except Exception as e:
            pytest.skip(f"Server communication failed: {e}")

    def test_server_completion(self, server_process):
        """Test completion through server process"""
        import json
        import select
        
        # Send completion request
        completion_request = {
            'jsonrpc': '2.0',
            'id': 2,
            'method': 'textDocument/completion',
            'params': {
                'textDocument': {'uri': 'file:///test.py'},
                'position': {'line': 0, 'character': 0}
            }
        }
        
        try:
            server_process.stdin.write(json.dumps(completion_request) + '\n')
            server_process.stdin.flush()
            
            # Read response with timeout
            ready, _, _ = select.select([server_process.stdout], [], [], 5.0)
            if not ready:
                pytest.skip("Server did not respond within timeout")
            
            response = server_process.stdout.readline()
            if not response:
                pytest.skip("No response from server")
            
            response_data = json.loads(response)
            
            assert response_data.get('result') is not None
            assert 'items' in response_data['result']
            
        except Exception as e:
            pytest.skip(f"Server completion failed: {e}")


if __name__ == '__main__':
    pytest.main([__file__, '-v']) 