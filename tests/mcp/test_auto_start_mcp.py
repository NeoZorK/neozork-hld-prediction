#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for MCP Auto-Start functionality
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

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.auto_start_mcp import MCPAutoStarter, MCPAutoStarterCLI

class TestMCPAutoStarter:
    """Test MCP Auto-Starter functionality"""
    
    @pytest.fixture
    def temp_project(self):
        """Create temporary project directory"""
        temp_dir = tempfile.mkdtemp()
        project_path = Path(temp_dir)
        
        # Create project structure
        (project_path / "src").mkdir()
        (project_path / "tests").mkdir()
        (project_path / "docs").mkdir()
        (project_path / "mql5_feed").mkdir()
        (project_path / "logs").mkdir()
        
        # Create sample files
        (project_path / "src" / "main.py").write_text("print('Hello, World!')")
        (project_path / "requirements.txt").write_text("pandas\nnumpy")
        (project_path / "mql5_feed" / "test.csv").write_text("time,open,close\n2023-01-01,100,101")
        
        yield project_path
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def auto_starter(self, temp_project):
        """Create auto starter instance"""
        with patch('scripts.auto_start_mcp.project_root', temp_project):
            starter = MCPAutoStarter()
            yield starter
    
    def test_initialization(self, auto_starter):
        """Test auto starter initialization"""
        assert auto_starter.project_root is not None
        assert auto_starter.logger is not None
        assert auto_starter.config is not None
        assert auto_starter.running_servers == {}
        assert auto_starter.running is True
    
    def test_load_config(self, auto_starter):
        """Test configuration loading"""
        config = auto_starter._load_config()
        
        assert "auto_start" in config
        assert "servers" in config
        assert "conditions" in config
        assert "monitoring" in config
        
        # Check auto-start settings
        auto_start = config["auto_start"]
        assert auto_start["enabled"] is True
        assert "check_interval" in auto_start
        
        # Check servers
        servers = config["servers"]
        assert "cursor" in servers
        assert "pycharm" in servers
        
        # Check conditions
        conditions = config["conditions"]
        assert "cursor_ide" in conditions
        assert "python_files" in conditions
    
    def test_detect_ide(self, auto_starter):
        """Test IDE detection"""
        with patch('psutil.process_iter') as mock_process_iter:
            # Mock Cursor IDE process
            mock_process = Mock()
            mock_process.info = {'name': 'Cursor', 'pid': 12345}
            mock_process_iter.return_value = [mock_process]
            
            ide = auto_starter.detect_ide()
            assert ide == "cursor"
        
        with patch('psutil.process_iter') as mock_process_iter:
            # Mock PyCharm IDE process
            mock_process = Mock()
            mock_process.info = {'name': 'pycharm64.exe', 'pid': 12346}
            mock_process_iter.return_value = [mock_process]
            
            ide = auto_starter.detect_ide()
            assert ide == "pycharm"
        
        with patch('psutil.process_iter') as mock_process_iter:
            # Mock no IDE process
            mock_process_iter.return_value = []
            
            ide = auto_starter.detect_ide()
            assert ide is None
    
    def test_check_project_conditions(self, auto_starter, temp_project):
        """Test project condition checking"""
        conditions = auto_starter.check_project_conditions()
        
        # Should have Python files
        assert conditions["python_files"] is True
        
        # Should have financial data
        assert conditions["financial_data"] is True
        
        # IDE conditions should be False (no IDE files)
        assert conditions.get("cursor_ide", False) is False
        assert conditions.get("pycharm_ide", False) is False
    
    def test_should_start_server(self, auto_starter):
        """Test server startup condition evaluation"""
        # Test with no conditions met
        with patch.object(auto_starter, 'check_project_conditions') as mock_conditions:
            mock_conditions.return_value = {
                "cursor_ide": False,
                "python_files": False
            }
            
            should_start = auto_starter.should_start_server("cursor")
            assert should_start is False
        
        # Test with conditions met
        with patch.object(auto_starter, 'check_project_conditions') as mock_conditions:
            mock_conditions.return_value = {
                "cursor_ide": True,
                "python_files": True
            }
            
            should_start = auto_starter.should_start_server("cursor")
            assert should_start is True
        
        # Test with server already running
        auto_starter.running_servers["cursor"] = {"process": Mock()}
        
        with patch.object(auto_starter, 'check_project_conditions') as mock_conditions:
            mock_conditions.return_value = {
                "cursor_ide": True,
                "python_files": True
            }
            
            should_start = auto_starter.should_start_server("cursor")
            assert should_start is False
    
    def test_start_server(self, auto_starter):
        """Test server startup"""
        with patch('subprocess.Popen') as mock_popen:
            # Mock successful startup
            mock_process = Mock()
            mock_process.poll.return_value = None
            mock_process.pid = 12345
            mock_popen.return_value = mock_process
            
            success = auto_starter.start_server("cursor")
            assert success is True
            assert "cursor" in auto_starter.running_servers
            
            server_info = auto_starter.running_servers["cursor"]
            assert server_info["pid"] == 12345
            assert "start_time" in server_info
        
        with patch('subprocess.Popen') as mock_popen:
            # Mock failed startup
            mock_process = Mock()
            mock_process.poll.return_value = 1  # Process exited
            mock_popen.return_value = mock_process
            
            success = auto_starter.start_server("pycharm")
            assert success is False
            assert "pycharm" not in auto_starter.running_servers
    
    def test_stop_server(self, auto_starter):
        """Test server shutdown"""
        # Setup running server
        mock_process = Mock()
        mock_process.poll.return_value = None
        auto_starter.running_servers["cursor"] = {
            "process": mock_process,
            "start_time": time.time(),
            "pid": 12345
        }
        
        # Test successful stop
        with patch.object(mock_process, 'wait') as mock_wait:
            mock_wait.return_value = 0
            
            success = auto_starter.stop_server("cursor")
            assert success is True
            assert "cursor" not in auto_starter.running_servers
        
        # Test stop non-existent server
        success = auto_starter.stop_server("nonexistent")
        assert success is True
    
    def test_check_server_health(self, auto_starter):
        """Test server health checking"""
        # Setup healthy server
        mock_process = Mock()
        mock_process.poll.return_value = None
        auto_starter.running_servers["cursor"] = {
            "process": mock_process,
            "start_time": time.time(),
            "pid": 12345
        }
        
        # Test healthy server
        auto_starter.check_server_health()
        assert "cursor" in auto_starter.running_servers
        
        # Setup failed server
        mock_process.poll.return_value = 1  # Process exited
        
        with patch.object(auto_starter, 'should_start_server') as mock_should_start:
            mock_should_start.return_value = True
            
            with patch.object(auto_starter, 'start_server') as mock_start:
                mock_start.return_value = True
                
                auto_starter.check_server_health()
                assert "cursor" not in auto_starter.running_servers
                mock_start.assert_called_once_with("cursor")
    
    def test_evaluate_servers(self, auto_starter):
        """Test server evaluation"""
        with patch.object(auto_starter, 'should_start_server') as mock_should_start:
            with patch.object(auto_starter, 'start_server') as mock_start:
                with patch.object(auto_starter, 'stop_server') as mock_stop:
                    
                    # Test starting new server
                    mock_should_start.return_value = True
                    mock_start.return_value = True
                    
                    auto_starter.evaluate_servers()
                    mock_start.assert_called()
                    
                    # Test stopping server
                    mock_should_start.return_value = False
                    auto_starter.running_servers["cursor"] = {"process": Mock()}
                    
                    auto_starter.evaluate_servers()
                    mock_stop.assert_called_with("cursor")
    
    def test_get_status(self, auto_starter):
        """Test status reporting"""
        with patch.object(auto_starter, 'check_project_conditions') as mock_conditions:
            with patch.object(auto_starter, 'detect_ide') as mock_detect:
                
                mock_conditions.return_value = {
                    "python_files": True,
                    "financial_data": True
                }
                mock_detect.return_value = "cursor"
                
                status = auto_starter.get_status()
                
                assert status["running"] is True
                assert status["ide_detected"] == "cursor"
                assert status["conditions"]["python_files"] is True
                assert status["conditions"]["financial_data"] is True
                assert "servers" in status
    
    def test_cleanup(self, auto_starter):
        """Test cleanup functionality"""
        # Setup running servers
        mock_process = Mock()
        auto_starter.running_servers["cursor"] = {
            "process": mock_process,
            "start_time": time.time(),
            "pid": 12345
        }
        
        with patch.object(auto_starter, 'stop_server') as mock_stop:
            with patch.object(auto_starter.observer, 'stop') as mock_observer_stop:
                with patch.object(auto_starter.observer, 'join') as mock_observer_join:
                    
                    auto_starter.cleanup()
                    
                    mock_stop.assert_called_with("cursor")
                    mock_observer_stop.assert_called_once()
                    mock_observer_join.assert_called_once()

class TestMCPAutoStarterCLI:
    """Test CLI interface"""
    
    @pytest.fixture
    def cli(self):
        """Create CLI instance"""
        with patch('scripts.auto_start_mcp.MCPAutoStarter'):
            cli = MCPAutoStarterCLI()
            yield cli
    
    def test_start(self, cli):
        """Test start command"""
        with patch.object(cli.auto_starter, 'run') as mock_run:
            with patch.object(cli.auto_starter, 'get_status') as mock_status:
                mock_status.return_value = {
                    "ide_detected": "cursor",
                    "conditions": {"python_files": True}
                }
                
                cli.start()
                mock_run.assert_called_once()
    
    def test_status(self, cli):
        """Test status command"""
        with patch.object(cli.auto_starter, 'get_status') as mock_status:
            mock_status.return_value = {
                "running": True,
                "ide_detected": "cursor",
                "conditions": {
                    "python_files": True,
                    "financial_data": True
                },
                "servers": {
                    "cursor": {
                        "running": True,
                        "pid": 12345,
                        "uptime": 100
                    }
                }
            }
            
            # Capture stdout
            import io
            import sys
            captured_output = io.StringIO()
            sys.stdout = captured_output
            
            try:
                cli.status()
                output = captured_output.getvalue()
                
                assert "MCP Auto Starter Status" in output
                assert "cursor" in output
                assert "12345" in output
            finally:
                sys.stdout = sys.__stdout__
    
    def test_stop(self, cli):
        """Test stop command"""
        with patch.object(cli.auto_starter, 'cleanup') as mock_cleanup:
            cli.stop()
            assert cli.auto_starter.running is False
            mock_cleanup.assert_called_once()
    
    def test_restart(self, cli):
        """Test restart command"""
        # Setup running servers
        cli.auto_starter.running_servers = {
            "cursor": {"process": Mock()},
            "pycharm": {"process": Mock()}
        }
        
        with patch.object(cli.auto_starter, 'stop_server') as mock_stop:
            with patch.object(cli.auto_starter, 'evaluate_servers') as mock_evaluate:
                with patch.object(cli.auto_starter, 'get_status') as mock_status:
                    mock_status.return_value = {
                        "servers": {
                            "cursor": {"running": True},
                            "pycharm": {"running": True}
                        }
                    }
                    
                    cli.restart()
                    
                    assert mock_stop.call_count == 2
                    mock_evaluate.assert_called_once()

class TestIntegration:
    """Integration tests"""
    
    @pytest.fixture
    def temp_project_with_config(self):
        """Create temporary project with configuration"""
        temp_dir = tempfile.mkdtemp()
        project_path = Path(temp_dir)
        
        # Create project structure
        (project_path / "src").mkdir()
        (project_path / "mql5_feed").mkdir()
        (project_path / "logs").mkdir()
        
        # Create sample files
        (project_path / "src" / "main.py").write_text("print('Hello, World!')")
        (project_path / "mql5_feed" / "test.csv").write_text("time,open,close\n2023-01-01,100,101")
        
        # Create configuration
        config = {
            "auto_start": {
                "enabled": True,
                "check_interval": 1
            },
            "servers": {
                "test_server": {
                    "enabled": True,
                    "command": "python",
                    "args": ["-c", "import time; time.sleep(5)"],
                    "conditions": ["python_files"]
                }
            },
            "conditions": {
                "python_files": {
                    "extensions": [".py"],
                    "min_files": 1
                }
            }
        }
        
        (project_path / "mcp_auto_config.json").write_text(json.dumps(config))
        
        yield project_path
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    def test_full_workflow(self, temp_project_with_config):
        """Test complete auto-start workflow"""
        with patch('scripts.auto_start_mcp.project_root', temp_project_with_config):
            auto_starter = MCPAutoStarter()
            
            # Test condition checking
            conditions = auto_starter.check_project_conditions()
            assert conditions["python_files"] is True
            
            # Test server evaluation
            auto_starter.evaluate_servers()
            
            # Should have started test server
            assert "test_server" in auto_starter.running_servers
            
            # Test cleanup
            auto_starter.cleanup()
            assert len(auto_starter.running_servers) == 0

class TestErrorHandling:
    """Test error handling"""
    
    def test_config_load_error(self, temp_project):
        """Test configuration loading error handling"""
        with patch('scripts.auto_start_mcp.project_root', temp_project):
            # Remove config file to trigger error
            config_file = temp_project / "mcp_auto_config.json"
            if config_file.exists():
                config_file.unlink()
            
            auto_starter = MCPAutoStarter()
            
            # Should load default config
            config = auto_starter._load_config()
            assert "auto_start" in config
            assert "servers" in config
    
    def test_process_error(self, auto_starter):
        """Test process error handling"""
        with patch('psutil.process_iter') as mock_process_iter:
            mock_process_iter.side_effect = Exception("Process error")
            
            ide = auto_starter.detect_ide()
            assert ide is None
    
    def test_server_start_error(self, auto_starter):
        """Test server startup error handling"""
        with patch('subprocess.Popen') as mock_popen:
            mock_popen.side_effect = Exception("Startup error")
            
            success = auto_starter.start_server("cursor")
            assert success is False
    
    def test_file_monitoring_error(self, auto_starter):
        """Test file monitoring error handling"""
        with patch('watchdog.observers.Observer') as mock_observer:
            mock_observer.side_effect = Exception("Observer error")
            
            # Should not crash
            auto_starter.monitor_project_changes()
            assert auto_starter.observer is None

class TestPerformance:
    """Performance tests"""
    
    def test_condition_check_performance(self, auto_starter, temp_project):
        """Test condition checking performance"""
        import time
        
        start_time = time.time()
        conditions = auto_starter.check_project_conditions()
        end_time = time.time()
        
        # Should complete quickly
        assert end_time - start_time < 1.0
        assert "python_files" in conditions
    
    def test_server_evaluation_performance(self, auto_starter):
        """Test server evaluation performance"""
        import time
        
        with patch.object(auto_starter, 'should_start_server') as mock_should_start:
            with patch.object(auto_starter, 'start_server') as mock_start:
                mock_should_start.return_value = False
                
                start_time = time.time()
                auto_starter.evaluate_servers()
                end_time = time.time()
                
                # Should complete quickly
                assert end_time - start_time < 1.0
    
    def test_status_reporting_performance(self, auto_starter):
        """Test status reporting performance"""
        import time
        
        with patch.object(auto_starter, 'check_project_conditions') as mock_conditions:
            with patch.object(auto_starter, 'detect_ide') as mock_detect:
                mock_conditions.return_value = {"python_files": True}
                mock_detect.return_value = None
                
                start_time = time.time()
                status = auto_starter.get_status()
                end_time = time.time()
                
                # Should complete quickly
                assert end_time - start_time < 1.0
                assert "running" in status

if __name__ == "__main__":
    pytest.main([__file__]) 