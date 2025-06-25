#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for MCP server status checker
Tests both Docker and non-Docker environments
"""

import pytest
import json
import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
import tempfile
import shutil
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.check_mcp_status import (
    MCPServerChecker, 
    DockerMCPServerChecker, 
    is_running_in_docker
)


class TestDockerDetection:
    """Test Docker environment detection"""
    
    def test_is_running_in_docker_with_dockerenv(self):
        """Test Docker detection with /.dockerenv file"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
            assert is_running_in_docker() is True
    
    def test_is_running_in_docker_with_cgroup(self):
        """Test Docker detection with cgroup"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            
            with patch('builtins.open', mock_open(read_data='docker')):
                assert is_running_in_docker() is True
    
    def test_is_running_in_docker_with_env_var(self):
        """Test Docker detection with environment variable"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            
            with patch('builtins.open', side_effect=FileNotFoundError):
                with patch.dict(os.environ, {'DOCKER_CONTAINER': 'true'}):
                    assert is_running_in_docker() is True
    
    def test_is_running_in_docker_not_in_docker(self):
        """Test Docker detection when not in Docker"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            
            with patch('builtins.open', side_effect=FileNotFoundError):
                with patch.dict(os.environ, {}, clear=True):
                    assert is_running_in_docker() is False


class TestDockerMCPServerChecker:
    """Test Docker MCP server checker"""
    
    @pytest.fixture
    def docker_checker(self, tmp_path):
        """Create DockerMCPServerChecker instance"""
        with patch('scripts.check_mcp_status.Path') as mock_path:
            mock_path.return_value.parent.parent = tmp_path
            return DockerMCPServerChecker()
    
    def test_check_server_running_with_pid_file(self, docker_checker):
        """Test server running check with valid PID file"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
            
            with patch('builtins.open', mock_open(read_data='12345')):
                with patch.object(docker_checker, '_is_process_running', return_value=True):
                    assert docker_checker.check_server_running() is True
    
    def test_check_server_running_with_stale_pid_file(self, docker_checker):
        """Test server running check with stale PID file"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
            
            with patch('builtins.open', mock_open(read_data='12345')):
                with patch.object(docker_checker, '_is_process_running', return_value=False):
                    with patch('pathlib.Path.unlink') as mock_unlink:
                        assert docker_checker.check_server_running() is False
                        mock_unlink.assert_called_once()
    
    def test_check_server_running_no_pid_file(self, docker_checker):
        """Test server running check without PID file"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            # Mock ps aux not finding the process
            with patch.object(docker_checker, '_check_server_with_ps', return_value=False):
                assert docker_checker.check_server_running() is False
    
    def test_is_process_running_valid_pid(self, docker_checker):
        """Test process running check with valid PID"""
        with patch('os.kill') as mock_kill:
            mock_kill.return_value = None
            assert docker_checker._is_process_running(12345) is True
    
    def test_is_process_running_invalid_pid(self, docker_checker):
        """Test process running check with invalid PID"""
        with patch('os.kill') as mock_kill:
            mock_kill.side_effect = OSError()
            assert docker_checker._is_process_running(99999) is False
    
    def test_test_connection_server_running(self, docker_checker):
        """Test connection when server is running"""
        with patch.object(docker_checker, 'check_server_running', return_value=True):
            with patch.object(docker_checker, '_test_mcp_protocol_connection') as mock_test:
                mock_test.return_value = {"status": "success", "message": "Connected"}
                result = docker_checker.test_connection()
                assert result["status"] == "success"
    
    def test_test_connection_server_not_running(self, docker_checker):
        """Test connection when server is not running"""
        with patch.object(docker_checker, 'check_server_running', return_value=False):
            result = docker_checker.test_connection()
            assert result["status"] == "failed"
            assert "Server not running" in result["error"]
    
    def test_test_mcp_protocol_connection_with_recent_logs(self, docker_checker):
        """Test MCP protocol connection with recent log activity"""
        # Мокаем open для чтения лога
        with patch.object(docker_checker, 'project_root', Path('/tmp')):
            with patch('builtins.open', mock_open(read_data='Server running normally')):
                # Мокаем весь Path объект для log_file
                mock_log_file = MagicMock()
                mock_log_file.exists.return_value = True
                mock_log_file.stat.return_value.st_mtime = time.time() - 10  # Recent
                
                with patch('scripts.check_mcp_status.Path') as mock_path:
                    # Настраиваем mock_path для возврата mock_log_file при создании log_file
                    def path_side_effect(*args, **kwargs):
                        if args and 'mcp_server.log' in str(args[0]):
                            return mock_log_file
                        return Path(*args, **kwargs)
                    mock_path.side_effect = path_side_effect
                    
                    result = docker_checker._test_mcp_protocol_connection()
                    assert result["status"] == "success"
                    # Теперь может быть либо "confirmed via logs" либо "confirmed via ps aux"
                    assert any(phrase in result["message"] for phrase in ["confirmed via logs", "confirmed via ps aux"])
    
    def test_test_mcp_protocol_connection_with_old_logs(self, docker_checker):
        """Test MCP protocol connection with old log activity"""
        mock_log_file = MagicMock()
        mock_log_file.stat.return_value.st_mtime = time.time() - 60  # Old
        mock_log_file.exists.return_value = True
        
        with patch('pathlib.Path') as mock_path:
            mock_path.return_value.__truediv__.return_value = mock_log_file
            
            with patch.object(docker_checker, '_ping_mcp_server') as mock_ping:
                mock_ping.return_value = {"status": "success", "message": "Ping successful"}
                result = docker_checker._test_mcp_protocol_connection()
                assert result["status"] == "success"
    
    def test_ping_mcp_server_with_pid_file(self, docker_checker):
        """Test ping MCP server with valid PID file"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = True
            
            with patch('builtins.open', mock_open(read_data='12345')):
                with patch.object(docker_checker, '_is_process_running', return_value=True):
                    result = docker_checker._ping_mcp_server()
                    assert result["status"] == "success"
                    assert result["pid"] == 12345
    
    def test_ping_mcp_server_no_pid_file(self, docker_checker):
        """Test ping MCP server without PID file"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            # Mock ps aux not finding the process
            with patch.object(docker_checker, '_check_server_with_ps', return_value=False):
                result = docker_checker._ping_mcp_server()
                assert result["status"] == "failed"
                assert "No PID file found and no process detected" in result["error"]
    
    def test_check_ide_configurations(self, docker_checker):
        """Test IDE configurations check in Docker"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.side_effect = [True, False]  # cursor config exists, docker config doesn't
            
            with patch('builtins.open', mock_open(read_data='{"test": "config"}')):
                with patch('pathlib.Path.stat') as mock_stat:
                    mock_stat.return_value.st_size = 100
                    configs = docker_checker.check_ide_configurations()
                    
                    assert configs['cursor']['exists'] is True
                    assert configs['cursor']['valid_json'] is True
                    assert configs['cursor']['size'] == 100
                    assert configs['docker']['exists'] is False
    
    def test_check_docker_specific(self, docker_checker):
        """Test Docker-specific checks"""
        with patch.object(docker_checker, '_is_running_in_docker', return_value=True):
            with patch.dict(os.environ, {'DOCKER_CONTAINER': 'true', 'PYTHONPATH': '/app'}):
                # Мокаем PID file exists и log_file.exists
                with patch('pathlib.Path.exists', return_value=True):
                    with patch('builtins.open', mock_open(read_data='12345')):
                        with patch.object(docker_checker, '_is_process_running', return_value=True):
                            # Мокаем stat для log_file
                            mock_stat = MagicMock()
                            mock_stat.st_size = 2048
                            mock_stat.st_mtime = time.time() - 5
                            with patch('pathlib.Path.stat', return_value=mock_stat):
                                docker_info = docker_checker._check_docker_specific()
                                assert docker_info['in_docker'] is True
                                assert docker_info['environment_vars']['DOCKER_CONTAINER'] == 'true'
                                assert docker_info['pid_file_exists'] is True
                                assert docker_info['pid'] == 12345
                                assert docker_info['process_running'] is True
                                assert docker_info['log_file_exists'] is True
                                assert docker_info['log_file_size'] == 2048
    
    def test_run_comprehensive_check(self, docker_checker):
        """Test comprehensive check in Docker"""
        with patch.object(docker_checker, 'check_server_running', return_value=True):
            with patch.object(docker_checker, 'test_connection') as mock_test:
                mock_test.return_value = {"status": "success", "message": "Connected"}
                
                with patch.object(docker_checker, 'check_ide_configurations') as mock_configs:
                    mock_configs.return_value = {'cursor': {'exists': True}}
                    
                    with patch.object(docker_checker, '_check_docker_specific') as mock_docker:
                        mock_docker.return_value = {'in_docker': True}
                        
                        results = docker_checker.run_comprehensive_check()
                        
                        assert results['environment'] == 'docker'
                        assert results['server_running'] is True
                        assert results['connection_test']['status'] == 'success'

    def test_check_server_with_ps_found(self, docker_checker):
        """Test ps aux check when server is found"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "user 12345 1.0 0.5 123456 12345 ? S 12:00 0:01 python neozork_mcp_server.py"
            
            assert docker_checker._check_server_with_ps() is True
    
    def test_check_server_with_ps_not_found(self, docker_checker):
        """Test ps aux check when server is not found"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "user 12345 1.0 0.5 123456 12345 ? S 12:00 0:01 python other_process.py"
            
            assert docker_checker._check_server_with_ps() is False
    
    def test_check_server_with_ps_timeout(self, docker_checker):
        """Test ps aux check with timeout"""
        with patch('subprocess.run') as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired('ps', 5)
            
            assert docker_checker._check_server_with_ps() is False
    
    def test_check_server_with_ps_command_failed(self, docker_checker):
        """Test ps aux check when command fails"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stderr = "Permission denied"
            
            assert docker_checker._check_server_with_ps() is False
    
    def test_check_server_running_fallback_to_ps(self, docker_checker):
        """Test server running check with fallback to ps aux"""
        # Mock PID file not existing
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            
            # Mock ps aux finding the process
            with patch.object(docker_checker, '_check_server_with_ps', return_value=True):
                assert docker_checker.check_server_running() is True
    
    def test_check_server_running_no_pid_file_no_ps(self, docker_checker):
        """Test server running check when neither PID file nor ps aux find the process"""
        # Mock PID file not existing
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            
            # Mock ps aux not finding the process
            with patch.object(docker_checker, '_check_server_with_ps', return_value=False):
                assert docker_checker.check_server_running() is False
    
    def test_ping_mcp_server_fallback_to_ps(self, docker_checker):
        """Test ping MCP server with fallback to ps aux"""
        # Mock PID file not existing
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            
            # Mock ps aux finding the process
            with patch.object(docker_checker, '_check_server_with_ps', return_value=True):
                result = docker_checker._ping_mcp_server()
                assert result["status"] == "success"
                assert "ps aux" in result["message"]
                assert result["detection_method"] == "ps_aux"
    
    def test_ping_mcp_server_no_pid_file_no_ps(self, docker_checker):
        """Test ping MCP server when neither PID file nor ps aux find the process"""
        # Mock PID file not existing
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.return_value = False
            
            # Mock ps aux not finding the process
            with patch.object(docker_checker, '_check_server_with_ps', return_value=False):
                result = docker_checker._ping_mcp_server()
                assert result["status"] == "failed"
                assert "No PID file found and no process detected" in result["error"]
    
    def test_check_docker_specific_with_ps_detection(self, docker_checker):
        """Test Docker-specific checks with ps aux detection"""
        with patch.object(docker_checker, '_is_running_in_docker', return_value=True):
            with patch.dict(os.environ, {'DOCKER_CONTAINER': 'true', 'PYTHONPATH': '/app'}):
                with patch('pathlib.Path.exists') as mock_exists:
                    # PID file doesn't exist, but ps aux finds the process
                    mock_exists.return_value = False
                    
                    with patch.object(docker_checker, '_check_server_with_ps', return_value=True):
                        docker_info = docker_checker._check_docker_specific()
                        
                        assert docker_info['in_docker'] is True
                        assert docker_info['pid_file_exists'] is False
                        assert docker_info['detection_method'] == 'ps_aux'
                        assert docker_info['process_running'] is True
    
    def test_check_docker_specific_no_detection(self, docker_checker):
        """Test Docker-specific checks with no detection method"""
        with patch.object(docker_checker, '_is_running_in_docker', return_value=True):
            with patch.dict(os.environ, {'DOCKER_CONTAINER': 'true', 'PYTHONPATH': '/app'}):
                with patch('pathlib.Path.exists') as mock_exists:
                    # PID file doesn't exist, and ps aux doesn't find the process
                    mock_exists.return_value = False
                    
                    with patch.object(docker_checker, '_check_server_with_ps', return_value=False):
                        docker_info = docker_checker._check_docker_specific()
                        
                        assert docker_info['in_docker'] is True
                        assert docker_info['pid_file_exists'] is False
                        assert docker_info['detection_method'] == 'none'
                        assert docker_info['process_running'] is False


class TestMCPServerChecker:
    """Test non-Docker MCP server checker"""
    
    @pytest.fixture
    def host_checker(self, tmp_path):
        """Create MCPServerChecker instance"""
        with patch('scripts.check_mcp_status.Path') as mock_path:
            mock_path.return_value.parent.parent = tmp_path
            return MCPServerChecker()
    
    def test_check_server_running_with_pgrep(self, host_checker):
        """Test server running check with pgrep"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "12345\n67890"
            
            assert host_checker.check_server_running() is True
    
    def test_check_server_running_no_process(self, host_checker):
        """Test server running check when no process found"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stdout = ""
            
            assert host_checker.check_server_running() is False
    
    def test_start_server_success(self, host_checker):
        """Test starting server successfully"""
        mock_process = MagicMock()
        mock_process.poll.return_value = None
        mock_process.pid = 12345
        
        with patch('subprocess.Popen', return_value=mock_process):
            with patch('time.sleep'):
                assert host_checker.start_server() is True
                assert host_checker.server_process == mock_process
    
    def test_start_server_failure(self, host_checker):
        """Test starting server failure"""
        mock_process = MagicMock()
        mock_process.poll.return_value = 1
        mock_process.communicate.return_value = ("stdout", "stderr")
        
        with patch('subprocess.Popen', return_value=mock_process):
            with patch('time.sleep'):
                assert host_checker.start_server() is False
    
    def test_stop_server_graceful(self, host_checker):
        """Test stopping server gracefully"""
        mock_process = MagicMock()
        mock_process.wait.return_value = 0
        host_checker.server_process = mock_process
        
        host_checker.stop_server()
        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once_with(timeout=5)
    
    def test_stop_server_force_kill(self, host_checker):
        """Test stopping server with force kill"""
        mock_process = MagicMock()
        mock_process.wait.side_effect = subprocess.TimeoutExpired('cmd', 5)
        host_checker.server_process = mock_process
        
        host_checker.stop_server()
        mock_process.terminate.assert_called_once()
        mock_process.kill.assert_called_once()
    
    def test_test_connection_success(self, host_checker):
        """Test connection when server is running"""
        with patch.object(host_checker, 'check_server_running', return_value=True):
            with patch.object(host_checker, '_get_server_pids', return_value=['12345']):
                result = host_checker.test_connection()
                assert result["status"] == "success"
                assert result["pids"] == ['12345']
    
    def test_test_connection_failure(self, host_checker):
        """Test connection when server is not running"""
        with patch.object(host_checker, 'check_server_running', return_value=False):
            result = host_checker.test_connection()
            assert result["status"] == "failed"
            assert "Server not running" in result["error"]
    
    def test_get_server_pids(self, host_checker):
        """Test getting server PIDs"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "12345\n67890"
            
            pids = host_checker._get_server_pids()
            assert pids == ['12345', '67890']
    
    def test_get_server_pids_no_processes(self, host_checker):
        """Test getting server PIDs when no processes found"""
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 1
            mock_run.return_value.stdout = ""
            
            pids = host_checker._get_server_pids()
            assert pids == []
    
    def test_check_ide_configurations(self, host_checker):
        """Test IDE configurations check"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.side_effect = [True, True, False]  # cursor, vscode exist, pycharm doesn't
            
            with patch('builtins.open', mock_open(read_data='{"test": "config"}')):
                with patch('pathlib.Path.stat') as mock_stat:
                    mock_stat.return_value.st_size = 100
                    configs = host_checker.check_ide_configurations()
                    
                    assert configs['cursor']['exists'] is True
                    assert configs['cursor']['valid_json'] is True
                    assert configs['cursor']['size'] == 100
                    assert configs['vscode']['exists'] is True
                    assert configs['pycharm']['exists'] is False
    
    def test_run_comprehensive_check(self, host_checker):
        """Test comprehensive check on host"""
        with patch.object(host_checker, 'check_server_running', return_value=True):
            with patch.object(host_checker, 'test_connection') as mock_test:
                mock_test.return_value = {"status": "success", "message": "Connected"}
                
                with patch.object(host_checker, 'check_ide_configurations') as mock_configs:
                    mock_configs.return_value = {'cursor': {'exists': True}}
                    
                    results = host_checker.run_comprehensive_check()
                    
                    assert results['environment'] == 'host'
                    assert results['server_running'] is True
                    assert results['connection_test']['status'] == 'success'


class TestIntegration:
    """Integration tests for the complete functionality"""
    
    def test_main_function_docker_environment(self):
        """Test main function in Docker environment"""
        with patch('scripts.check_mcp_status.is_running_in_docker', return_value=True):
            with patch('scripts.check_mcp_status.DockerMCPServerChecker') as mock_checker_class:
                mock_checker = MagicMock()
                mock_checker.run_comprehensive_check.return_value = {
                    'timestamp': '2024-01-01 12:00:00',
                    'environment': 'docker',
                    'project_root': '/app',
                    'server_running': True,
                    'connection_test': {'status': 'success'},
                    'ide_configurations': {},
                    'recommendations': []
                }
                mock_checker_class.return_value = mock_checker
                
                with patch('builtins.print'):  # Suppress print output
                    with patch('builtins.open', mock_open()):
                        from scripts.check_mcp_status import main
                        exit_code = main()
                        assert exit_code == 0
    
    def test_main_function_host_environment(self):
        """Test main function in host environment"""
        with patch('scripts.check_mcp_status.is_running_in_docker', return_value=False):
            with patch('scripts.check_mcp_status.MCPServerChecker') as mock_checker_class:
                mock_checker = MagicMock()
                mock_checker.run_comprehensive_check.return_value = {
                    'timestamp': '2024-01-01 12:00:00',
                    'environment': 'host',
                    'project_root': '/home/user/project',
                    'server_running': False,
                    'connection_test': {'status': 'failed'},
                    'ide_configurations': {},
                    'recommendations': ['Start server']
                }
                mock_checker_class.return_value = mock_checker
                
                with patch('builtins.print'):  # Suppress print output
                    with patch('builtins.open', mock_open()):
                        from scripts.check_mcp_status import main
                        exit_code = main()
                        assert exit_code == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 