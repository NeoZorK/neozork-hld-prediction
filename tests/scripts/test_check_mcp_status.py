#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for MCP Server Status Checker
Tests both Docker and non-Docker environments
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import sys
import os

# Add the scripts directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from check_mcp_status import (
    DockerMCPServerChecker, 
    MCPServerChecker, 
    is_running_in_docker
)


class TestDockerMCPServerChecker:
    """Test Docker MCP Server Checker"""
    
    @pytest.fixture
    def temp_project_root(self):
        """Create temporary project root for testing"""
        temp_dir = tempfile.mkdtemp()
        project_root = Path(temp_dir)
        
        # Create necessary directories
        (project_root / "logs").mkdir(exist_ok=True)
        
        yield project_root
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def docker_checker(self, temp_project_root):
        """Create Docker checker instance"""
        return DockerMCPServerChecker(temp_project_root)
    
    def test_init(self, docker_checker, temp_project_root):
        """Test Docker checker initialization"""
        assert docker_checker.project_root == temp_project_root
        assert docker_checker.logger is not None
    
    @patch('check_mcp_status.Path')
    def test_check_server_running_with_pid_file(self, mock_path, docker_checker):
        """Test server running check with PID file"""
        # Mock PID file exists
        mock_pid_file = MagicMock()
        mock_pid_file.exists.return_value = True
        mock_pid_file.unlink = MagicMock()
        
        with patch('builtins.open', mock_open(read_data='12345')):
            with patch.object(docker_checker, '_is_process_running', return_value=True):
                result = docker_checker.check_server_running()
                assert result is True
    
    @patch('check_mcp_status.Path')
    def test_check_server_running_with_stale_pid_file(self, mock_path, docker_checker):
        """Test server running check with stale PID file"""
        # Mock PID file exists but process is not running
        mock_pid_file = MagicMock()
        mock_pid_file.exists.return_value = True
        mock_pid_file.unlink = MagicMock()
        
        # Configure mock_path to return our mock_pid_file for PID file path
        def path_side_effect(*args, **kwargs):
            if args and str(args[0]) == "/tmp/mcp_server.pid":
                return mock_pid_file
            return Path(*args, **kwargs)
        mock_path.side_effect = path_side_effect
        
        with patch('builtins.open', mock_open(read_data='12345')):
            with patch.object(docker_checker, '_is_process_running', return_value=False):
                result = docker_checker.check_server_running()
                assert result is False
                mock_pid_file.unlink.assert_called_once()
    
    @patch('check_mcp_status.subprocess.run')
    def test_check_server_with_ps_available(self, mock_run, docker_checker):
        """Test server check with ps command available"""
        # Mock ps command success
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "user 12345 python neozork_mcp_server.py"
        
        result = docker_checker._check_server_with_ps()
        assert result is True
    
    @patch('check_mcp_status.subprocess.run')
    def test_check_server_with_ps_unavailable(self, mock_run, docker_checker):
        """Test server check when ps command is unavailable"""
        # Mock ps command failure
        mock_run.side_effect = FileNotFoundError("ps: command not found")
        
        with patch.object(docker_checker, '_check_server_via_proc', return_value=False):
            result = docker_checker._check_server_with_ps()
            assert result is False
    
    @patch('check_mcp_status.Path')
    def test_check_server_via_proc_success(self, mock_path, docker_checker):
        """Test server check via /proc filesystem - success case"""
        # Mock /proc directory structure
        mock_proc_dir = MagicMock()
        mock_proc_dir.exists.return_value = True
        
        # Create mock process directories
        mock_proc_12345 = MagicMock()
        mock_proc_12345.name = "12345"
        mock_proc_12345.is_dir.return_value = True
        
        mock_proc_abc = MagicMock()
        mock_proc_abc.name = "abc"
        mock_proc_abc.is_dir.return_value = True
        
        mock_proc_67890 = MagicMock()
        mock_proc_67890.name = "67890"
        mock_proc_67890.is_dir.return_value = True
        
        mock_proc_dir.iterdir.return_value = [mock_proc_12345, mock_proc_abc, mock_proc_67890]
        
        # Mock exe link for process 12345
        mock_exe_link = MagicMock()
        mock_exe_link.exists.return_value = True
        mock_exe_link.resolve.return_value = Path("/usr/bin/python3")
        
        # Mock cmdline file for process 12345
        mock_cmdline_file = MagicMock()
        mock_cmdline_file.exists.return_value = True
        
        # Configure mock_proc_12345 to return appropriate mocks for exe and cmdline
        def proc_12345_truediv(self, other):
            if other == "exe":
                return mock_exe_link
            elif other == "cmdline":
                return mock_cmdline_file
            return MagicMock()
        
        mock_proc_12345.__truediv__ = proc_12345_truediv
        
        # Configure mock_path to return our mock_proc_dir for /proc
        def path_side_effect(*args, **kwargs):
            if args and str(args[0]) == "/proc":
                return mock_proc_dir
            return Path(*args, **kwargs)
        mock_path.side_effect = path_side_effect
        
        with patch('builtins.open', mock_open(read_data='python\x00neozork_mcp_server.py\x00')):
            result = docker_checker._check_server_via_proc()
            assert result is True
    
    @patch('check_mcp_status.Path')
    def test_check_server_via_proc_not_found(self, mock_path, docker_checker):
        """Test server check via /proc filesystem - not found case"""
        # Mock /proc directory not accessible
        mock_proc_dir = MagicMock()
        mock_proc_dir.exists.return_value = False
        
        with patch('check_mcp_status.Path', return_value=mock_proc_dir):
            result = docker_checker._check_server_via_proc()
            assert result is False
    
    def test_is_process_running(self, docker_checker):
        """Test process running check"""
        # Test with current process PID
        current_pid = os.getpid()
        assert docker_checker._is_process_running(current_pid) is True
        
        # Test with non-existent PID
        assert docker_checker._is_process_running(999999) is False
    
    @patch.object(DockerMCPServerChecker, 'check_server_running')
    def test_test_connection_success(self, mock_check, docker_checker):
        """Test connection test - success case"""
        mock_check.return_value = True
        
        with patch.object(docker_checker, '_test_mcp_protocol_connection') as mock_test:
            mock_test.return_value = {"status": "success", "message": "Connected"}
            result = docker_checker.test_connection()
            
            assert result["status"] == "success"
            mock_test.assert_called_once()
    
    @patch.object(DockerMCPServerChecker, 'check_server_running')
    def test_test_connection_failure(self, mock_check, docker_checker):
        """Test connection test - failure case"""
        mock_check.return_value = False
        
        result = docker_checker.test_connection()
        assert result["status"] == "failed"
        assert "Server not running" in result["error"]
    
    def test_check_ide_configurations(self, docker_checker, temp_project_root):
        """Test IDE configurations check"""
        # Create test config file
        cursor_config = temp_project_root / "cursor_mcp_config.json"
        cursor_config.write_text('{"test": "config"}')
        
        configs = docker_checker.check_ide_configurations()
        
        assert configs['cursor']['exists'] is True
        assert configs['cursor']['valid_json'] is True
        assert configs['cursor']['size'] > 0
        assert configs['docker']['exists'] is False  # No docker.env in temp dir
    
    @patch.object(DockerMCPServerChecker, 'check_server_running')
    @patch.object(DockerMCPServerChecker, 'check_ide_configurations')
    @patch.object(DockerMCPServerChecker, '_check_docker_specific')
    def test_run_comprehensive_check(self, mock_docker, mock_configs, mock_server, docker_checker):
        """Test comprehensive check"""
        mock_server.return_value = True
        mock_configs.return_value = {'cursor': {'exists': True}}
        mock_docker.return_value = {'in_docker': True}
        
        with patch.object(docker_checker, 'test_connection') as mock_conn:
            mock_conn.return_value = {"status": "success"}
            result = docker_checker.run_comprehensive_check()
            
            assert result["environment"] == "docker"
            assert result["server_running"] is True
            assert "recommendations" in result


class TestMCPServerChecker:
    """Test non-Docker MCP Server Checker"""
    
    @pytest.fixture
    def temp_project_root(self):
        """Create temporary project root for testing"""
        temp_dir = tempfile.mkdtemp()
        project_root = Path(temp_dir)
        
        # Create necessary directories
        (project_root / "logs").mkdir(exist_ok=True)
        
        yield project_root
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def host_checker(self, temp_project_root):
        """Create host checker instance"""
        return MCPServerChecker(temp_project_root)
    
    def test_init(self, host_checker, temp_project_root):
        """Test host checker initialization"""
        assert host_checker.project_root == temp_project_root
        assert host_checker.logger is not None
        assert host_checker.server_process is None
    
    @patch('check_mcp_status.subprocess.run')
    def test_check_server_running_success(self, mock_run, host_checker):
        """Test server running check - success case"""
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "12345\n67890"
        
        result = host_checker.check_server_running()
        assert result is True
    
    @patch('check_mcp_status.subprocess.run')
    def test_check_server_running_not_found(self, mock_run, host_checker):
        """Test server running check - not found case"""
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = ""
        
        result = host_checker.check_server_running()
        assert result is False
    
    @patch('check_mcp_status.subprocess.Popen')
    def test_start_server_success(self, mock_popen, host_checker):
        """Test server start - success case"""
        mock_process = MagicMock()
        mock_process.poll.return_value = None
        mock_process.pid = 12345
        mock_popen.return_value = mock_process
        
        with patch('time.sleep'):
            result = host_checker.start_server()
            assert result is True
            assert host_checker.server_process == mock_process
    
    @patch('check_mcp_status.subprocess.Popen')
    def test_start_server_failure(self, mock_popen, host_checker):
        """Test server start - failure case"""
        mock_process = MagicMock()
        mock_process.poll.return_value = 1
        mock_process.communicate.return_value = ("stdout", "stderr")
        mock_popen.return_value = mock_process
        
        with patch('time.sleep'):
            result = host_checker.start_server()
            assert result is False
    
    def test_stop_server(self, host_checker):
        """Test server stop"""
        mock_process = MagicMock()
        host_checker.server_process = mock_process
        
        host_checker.stop_server()
        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once_with(timeout=5)
    
    @patch.object(MCPServerChecker, 'check_server_running')
    def test_test_connection_success(self, mock_check, host_checker):
        """Test connection test - success case"""
        mock_check.return_value = True
        
        with patch.object(host_checker, '_get_server_pids') as mock_pids:
            mock_pids.return_value = ["12345"]
            result = host_checker.test_connection()
            
            assert result["status"] == "success"
            assert result["pids"] == ["12345"]
    
    @patch.object(MCPServerChecker, 'check_server_running')
    def test_test_connection_failure(self, mock_check, host_checker):
        """Test connection test - failure case"""
        mock_check.return_value = False
        
        result = host_checker.test_connection()
        assert result["status"] == "failed"
        assert "Server not running" in result["error"]
    
    def test_check_ide_configurations(self, host_checker, temp_project_root):
        """Test IDE configurations check"""
        # Create test config files
        cursor_config = temp_project_root / "cursor_mcp_config.json"
        cursor_config.write_text('{"test": "config"}')
        
        vscode_dir = temp_project_root / ".vscode"
        vscode_dir.mkdir()
        vscode_config = vscode_dir / "settings.json"
        vscode_config.write_text('{"test": "vscode"}')
        
        configs = host_checker.check_ide_configurations()
        
        assert configs['cursor']['exists'] is True
        assert configs['cursor']['valid_json'] is True
        assert configs['vscode']['exists'] is True
        assert configs['vscode']['valid_json'] is True
        assert configs['pycharm']['exists'] is False


class TestEnvironmentDetection:
    """Test environment detection functions"""
    
    @patch('check_mcp_status.Path')
    def test_is_running_in_docker_true(self, mock_path):
        """Test Docker detection - true case"""
        # Mock /.dockerenv exists
        mock_dockerenv = MagicMock()
        mock_dockerenv.exists.return_value = True
        mock_path.return_value = mock_dockerenv
        
        result = is_running_in_docker()
        assert result is True
    
    @patch('check_mcp_status.Path')
    def test_is_running_in_docker_false(self, mock_path):
        """Test Docker detection - false case"""
        # Mock /.dockerenv doesn't exist
        mock_dockerenv = MagicMock()
        mock_dockerenv.exists.return_value = False
        mock_path.return_value = mock_dockerenv
        
        with patch('builtins.open', side_effect=FileNotFoundError):
            with patch.dict(os.environ, {}, clear=True):
                result = is_running_in_docker()
                assert result is False
    
    @patch.dict(os.environ, {'DOCKER_CONTAINER': 'true'})
    def test_is_running_in_docker_env_var(self):
        """Test Docker detection via environment variable"""
        result = is_running_in_docker()
        assert result is True


if __name__ == "__main__":
    pytest.main([__file__]) 