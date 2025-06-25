#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test MCP Server Status Checker
Test the check_mcp_status.py script functionality
"""

import pytest
import json
import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.check_mcp_status import MCPServerChecker


class TestMCPServerChecker:
    """Test MCP Server Status Checker functionality"""

    @pytest.fixture
    def checker(self, tmp_path):
        """Create MCPServerChecker instance with temp directory"""
        # Copy project structure to temp directory
        temp_project = tmp_path / "neozork-hld-prediction"
        temp_project.mkdir()
        
        # Create minimal project structure
        (temp_project / "src").mkdir()
        (temp_project / "tests").mkdir()
        (temp_project / "logs").mkdir()
        (temp_project / "data").mkdir()
        
        # Create mock MCP server file
        server_file = temp_project / "neozork_mcp_server.py"
        server_file.write_text("""
#!/usr/bin/env python3
import json
import sys

def main():
    request = json.loads(sys.stdin.read())
    method = request.get('method')
    
    if method == 'neozork/ping':
        response = {
            "jsonrpc": "2.0",
            "id": request.get('id'),
            "result": {
                "pong": True,
                "timestamp": "2025-06-25T23:37:14.965240",
                "server_time": "2025-06-25 23:37:14",
                "timezone": "UTC"
            }
        }
    elif method == 'neozork/status':
        response = {
            "jsonrpc": "2.0",
            "id": request.get('id'),
            "result": {
                "status": "ready",
                "server_file": str(server_file)
            }
        }
    elif method == 'neozork/health':
        response = {
            "jsonrpc": "2.0",
            "id": request.get('id'),
            "result": {
                "status": "healthy",
                "uptime": "ready"
            }
        }
    elif method == 'neozork/projectInfo':
        response = {
            "jsonrpc": "2.0",
            "id": request.get('id'),
            "result": {
                "project_name": "neozork-hld-prediction",
                "version": "1.0.0"
            }
        }
    else:
        response = {
            "jsonrpc": "2.0",
            "id": request.get('id'),
            "error": {
                "code": -32601,
                "message": "Method not found"
            }
        }
    
    print(json.dumps(response))
    sys.exit(0)

if __name__ == "__main__":
    main()
""")
        
        return MCPServerChecker(temp_project)

    def test_init(self, checker):
        """Test MCPServerChecker initialization"""
        assert checker.project_root.exists()
        assert checker.server_process is None
        assert checker.logger is not None

    def test_setup_logging(self, checker):
        """Test logging setup"""
        log_dir = checker.project_root / "logs"
        assert log_dir.exists()
        
        # Test logger configuration
        assert checker.logger.level == 20  # INFO level
        assert len(checker.logger.handlers) >= 2  # File and Stream handlers

    @patch('subprocess.run')
    def test_check_server_running_true(self, mock_run, checker):
        """Test server running check when server is running"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "12345\n67890"
        
        result = checker.check_server_running()
        
        assert result is True
        mock_run.assert_called_once_with(
            ['pgrep', '-f', 'neozork_mcp_server.py'],
            capture_output=True,
            text=True
        )

    @patch('subprocess.run')
    def test_check_server_running_false(self, mock_run, checker):
        """Test server running check when server is not running"""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = ""
        
        result = checker.check_server_running()
        
        assert result is False

    @patch('subprocess.run')
    def test_check_server_running_error(self, mock_run, checker):
        """Test server running check with error"""
        mock_run.side_effect = Exception("pgrep not found")
        
        result = checker.check_server_running()
        
        assert result is False

    @patch('subprocess.Popen')
    def test_start_server_success(self, mock_popen, checker):
        """Test successful server start"""
        mock_process = MagicMock()
        mock_process.poll.return_value = None
        mock_process.pid = 12345
        mock_popen.return_value = mock_process
        
        result = checker.start_server()
        
        assert result is True
        assert checker.server_process == mock_process
        mock_popen.assert_called_once()

    @patch('subprocess.Popen')
    def test_start_server_failure(self, mock_popen, checker):
        """Test server start failure"""
        mock_process = MagicMock()
        mock_process.poll.return_value = 1
        mock_process.communicate.return_value = ("stdout", "stderr")
        mock_popen.return_value = mock_process
        
        result = checker.start_server()
        
        assert result is False

    def test_stop_server(self, checker):
        """Test server stop"""
        # Mock server process
        mock_process = MagicMock()
        mock_process.wait.return_value = None
        checker.server_process = mock_process
        
        checker.stop_server()
        
        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once_with(timeout=5)

    def test_stop_server_timeout(self, checker):
        """Test server stop with timeout"""
        # Mock server process with timeout
        mock_process = MagicMock()
        mock_process.wait.side_effect = subprocess.TimeoutExpired("cmd", 5)
        checker.server_process = mock_process
        
        checker.stop_server()
        
        mock_process.terminate.assert_called_once()
        mock_process.kill.assert_called_once()

    def test_send_request_success(self, checker):
        """Test successful request sending"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = '{"jsonrpc": "2.0", "id": 1, "result": {"pong": true}}'
            
            result = checker._send_request("neozork/ping", {})
            
            assert result == {"pong": True}
            mock_run.assert_called_once()

    def test_send_request_failure(self, checker):
        """Test failed request sending"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stderr = "Error"
            
            result = checker._send_request("neozork/ping", {})
            
            assert result is None

    def test_send_request_invalid_json(self, checker):
        """Test request with invalid JSON response"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "invalid json"
            
            result = checker._send_request("neozork/ping", {})
            
            assert result is None

    def test_send_request_timeout(self, checker):
        """Test request timeout"""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired("cmd", 10)
            
            result = checker._send_request("neozork/ping", {})
            
            assert result is None

    def test_test_connection_success(self, checker):
        """Test successful connection test"""
        with patch.object(checker, '_send_request') as mock_send:
            mock_send.side_effect = [
                {"pong": True},  # ping
                {"status": "ready"},  # status
                {"status": "healthy"},  # health
                {"project_name": "test"}  # project info
            ]
            
            result = checker.test_connection()
            
            assert result["status"] == "success"
            assert "ping" in result
            assert "status_info" in result
            assert "health" in result
            assert "project_info" in result

    def test_test_connection_ping_failure(self, checker):
        """Test connection test with ping failure"""
        with patch.object(checker, '_send_request') as mock_send:
            mock_send.return_value = None  # ping fails
            
            result = checker.test_connection()
            
            assert result["status"] == "failed"
            assert "Ping failed" in result["error"]

    def test_check_ide_configurations(self, checker):
        """Test IDE configuration checking"""
        # Create mock configuration files
        cursor_config = checker.project_root / "cursor_mcp_config.json"
        cursor_config.write_text('{"test": "data"}')
        
        vscode_dir = checker.project_root / ".vscode"
        vscode_dir.mkdir()
        vscode_config = vscode_dir / "settings.json"
        vscode_config.write_text('{"test": "data"}')
        
        pycharm_config = checker.project_root / "pycharm_mcp_config.json"
        pycharm_config.write_text('{"test": "data"}')
        
        result = checker.check_ide_configurations()
        
        assert "cursor" in result
        assert "vscode" in result
        assert "pycharm" in result
        
        assert result["cursor"]["exists"] is True
        assert result["cursor"]["valid_json"] is True
        assert result["cursor"]["size"] > 0
        
        assert result["vscode"]["exists"] is True
        assert result["vscode"]["valid_json"] is True
        assert result["vscode"]["size"] > 0
        
        assert result["pycharm"]["exists"] is True
        assert result["pycharm"]["valid_json"] is True
        assert result["pycharm"]["size"] > 0

    def test_check_ide_configurations_missing(self, checker):
        """Test IDE configuration checking with missing files"""
        result = checker.check_ide_configurations()
        
        assert "cursor" in result
        assert "vscode" in result
        assert "pycharm" in result
        
        assert result["cursor"]["exists"] is False
        assert result["vscode"]["exists"] is False
        assert result["pycharm"]["exists"] is False

    def test_check_ide_configurations_invalid_json(self, checker):
        """Test IDE configuration checking with invalid JSON"""
        # Create invalid JSON file
        cursor_config = checker.project_root / "cursor_mcp_config.json"
        cursor_config.write_text('{"invalid": json}')
        
        result = checker.check_ide_configurations()
        
        assert result["cursor"]["exists"] is True
        assert result["cursor"]["valid_json"] is False
        assert "error" in result["cursor"]

    def test_run_comprehensive_check_server_not_running(self, checker):
        """Test comprehensive check when server is not running"""
        with patch.object(checker, 'check_server_running', return_value=False):
            with patch.object(checker, 'check_ide_configurations') as mock_check_configs:
                mock_check_configs.return_value = {
                    "cursor": {"exists": True, "valid_json": True, "size": 100},
                    "vscode": {"exists": True, "valid_json": True, "size": 100},
                    "pycharm": {"exists": True, "valid_json": True, "size": 100}
                }
                
                result = checker.run_comprehensive_check()
                
                assert result["server_running"] is False
                assert result["connection_test"]["status"] == "skipped"
                assert "Start MCP server to test connection" in result["recommendations"]
                assert "Run: python3 neozork_mcp_server.py" in result["recommendations"]

    def test_run_comprehensive_check_server_running(self, checker):
        """Test comprehensive check when server is running"""
        with patch.object(checker, 'check_server_running', return_value=True):
            with patch.object(checker, 'test_connection') as mock_test_conn:
                with patch.object(checker, 'check_ide_configurations') as mock_check_configs:
                    mock_test_conn.return_value = {
                        "status": "success",
                        "ping": {"pong": True},
                        "health": {"status": "healthy"}
                    }
                    mock_check_configs.return_value = {
                        "cursor": {"exists": True, "valid_json": True, "size": 100},
                        "vscode": {"exists": True, "valid_json": True, "size": 100},
                        "pycharm": {"exists": True, "valid_json": True, "size": 100}
                    }
                    
                    result = checker.run_comprehensive_check()
                    
                    assert result["server_running"] is True
                    assert result["connection_test"]["status"] == "success"
                    assert len(result["recommendations"]) == 0

    def test_run_comprehensive_check_missing_configs(self, checker):
        """Test comprehensive check with missing IDE configurations"""
        with patch.object(checker, 'check_server_running', return_value=False):
            with patch.object(checker, 'check_ide_configurations') as mock_check_configs:
                mock_check_configs.return_value = {
                    "cursor": {"exists": False},
                    "vscode": {"exists": False},
                    "pycharm": {"exists": False}
                }
                
                result = checker.run_comprehensive_check()
                
                assert "Setup IDE configurations" in result["recommendations"][0]

    def test_run_comprehensive_check_connection_failed(self, checker):
        """Test comprehensive check with failed connection"""
        with patch.object(checker, 'check_server_running', return_value=True):
            with patch.object(checker, 'test_connection') as mock_test_conn:
                with patch.object(checker, 'check_ide_configurations') as mock_check_configs:
                    mock_test_conn.return_value = {
                        "status": "failed",
                        "error": "Connection timeout"
                    }
                    mock_check_configs.return_value = {
                        "cursor": {"exists": True, "valid_json": True, "size": 100}
                    }
                    
                    result = checker.run_comprehensive_check()
                    
                    assert result["connection_test"]["status"] == "failed"
                    assert "Check MCP server logs" in result["recommendations"][0]


class TestMCPServerCheckerIntegration:
    """Integration tests for MCP Server Checker"""

    def test_script_execution(self):
        """Test script execution from command line"""
        script_path = project_root / "scripts" / "check_mcp_status.py"
        
        # Test script exists
        assert script_path.exists()
        
        # Test script can be imported
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("check_mcp_status", script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            assert hasattr(module, 'MCPServerChecker')
        except Exception as e:
            pytest.fail(f"Failed to import script: {e}")

    def test_script_main_function(self):
        """Test main function exists"""
        script_path = project_root / "scripts" / "check_mcp_status.py"
        
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("check_mcp_status", script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            assert hasattr(module, 'main')
        except Exception as e:
            pytest.fail(f"Failed to import main function: {e}")

    @pytest.mark.integration
    def test_real_project_check(self):
        """Test checker with real project structure"""
        checker = MCPServerChecker(project_root)
        
        # Test basic functionality
        result = checker.run_comprehensive_check()
        
        # Verify result structure
        assert "timestamp" in result
        assert "project_root" in result
        assert "server_running" in result
        assert "connection_test" in result
        assert "ide_configurations" in result
        assert "recommendations" in result
        
        # Verify project root
        assert result["project_root"] == str(project_root)
        
        # Verify IDE configurations check
        ide_configs = result["ide_configurations"]
        assert "cursor" in ide_configs
        assert "vscode" in ide_configs
        assert "pycharm" in ide_configs


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 