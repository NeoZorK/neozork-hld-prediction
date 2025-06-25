#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests for Neozork MCP Manager
Comprehensive test suite for the unified MCP manager
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

from scripts.neozork_mcp_manager import NeozorkMCPManager, NeozorkMCPManagerCLI

class TestNeozorkMCPManager:
    """Test Neozork MCP Manager functionality"""
    
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
        (project_path / "src" / "main.py").write_text("print('Hello, World!')")
        
        # Create the MCP server file
        (project_path / "neozork_mcp_server.py").write_text("""
#!/usr/bin/env python3
# Test MCP server file
print("Test MCP server")
""")
        
        # Create sample financial data
        (project_path / "data" / "GBPUSD_MN1.csv").write_text("time,open,close\n2023-01-01,100,101")
        
        # Create sample config
        config = {
            "auto_start": {
                "enabled": True,
                "check_interval": 30,
                "ide_detection": True,
                "project_detection": True
            },
            "server": {
                "command": "python",
                "args": ["neozork_mcp_server.py"],
                "env": {
                    "PYTHONPATH": str(project_path),
                    "LOG_LEVEL": "INFO"
                },
                "cwd": str(project_path)
            },
            "conditions": {
                "cursor_ide": {
                    "processes": ["Cursor", "cursor"],
                    "files": [".cursor", "cursor_mcp_config.json"]
                },
                "pycharm_ide": {
                    "processes": ["pycharm", "PyCharm"],
                    "files": [".idea", "pycharm_mcp_config.json"]
                },
                "python_files": {
                    "extensions": [".py"],
                    "min_files": 1
                },
                "financial_data": {
                    "directories": ["mql5_feed", "data"],
                    "files": ["*.csv", "*.parquet"]
                }
            }
        }
        
        (project_path / "neozork_mcp_config.json").write_text(json.dumps(config, indent=2))
        
        yield project_path
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def manager(self, temp_project):
        """Create manager instance"""
        manager = NeozorkMCPManager(project_root=temp_project)
        yield manager
    
    def test_initialization(self, manager):
        """Test manager initialization"""
        assert manager.project_root is not None
        assert manager.logger is not None
        assert manager.config is not None
        assert manager.running_servers == {}
        assert manager.running is True
    
    def test_config_loading(self, manager):
        """Test configuration loading"""
        config = manager.config
        assert "auto_start" in config
        assert "server" in config
        assert "conditions" in config
        assert config["auto_start"]["enabled"] is True
    
    def test_detect_ide(self, manager):
        """Test IDE detection"""
        with patch('psutil.process_iter') as mock_process_iter:
            # Mock Cursor IDE process
            mock_process = Mock()
            mock_process.info = {'name': 'Cursor', 'pid': 12345}
            mock_process_iter.return_value = [mock_process]
            
            ide = manager.detect_ide()
            assert ide == "cursor"
        
        with patch('psutil.process_iter') as mock_process_iter:
            # Mock PyCharm IDE process
            mock_process = Mock()
            mock_process.info = {'name': 'pycharm64.exe', 'pid': 12346}
            mock_process_iter.return_value = [mock_process]
            
            ide = manager.detect_ide()
            assert ide == "pycharm"
        
        with patch('psutil.process_iter') as mock_process_iter:
            # Mock no IDE process
            mock_process_iter.return_value = []
            
            ide = manager.detect_ide()
            assert ide is None
    
    def test_check_project_conditions(self, manager):
        """Test project condition checking"""
        conditions = manager.check_project_conditions()
        
        # Should have Python files
        assert conditions["python_files"] is True
        
        # Should have financial data
        assert conditions["financial_data"] is True
        
        # IDE conditions should be False (no IDE files)
        assert conditions.get("cursor_ide", False) is False
        assert conditions.get("pycharm_ide", False) is False
    
    def test_should_start_server(self, manager):
        """Test server startup condition evaluation"""
        # Test with no conditions met
        with patch.object(manager, 'check_project_conditions') as mock_conditions:
            mock_conditions.return_value = {
                "cursor_ide": False,
                "python_files": False
            }
            
            should_start = manager.should_start_server()
            assert should_start is False
        
        # Test with conditions met
        with patch.object(manager, 'check_project_conditions') as mock_conditions:
            mock_conditions.return_value = {
                "cursor_ide": True,
                "python_files": True
            }
            
            should_start = manager.should_start_server()
            assert should_start is True
        
        # Test with server already running
        manager.running_servers["neozork_mcp"] = {"process": Mock()}
        
        with patch.object(manager, 'check_project_conditions') as mock_conditions:
            mock_conditions.return_value = {
                "cursor_ide": True,
                "python_files": True
            }
            
            should_start = manager.should_start_server()
            assert should_start is False
    
    def test_start_server(self, manager):
        """Test server startup"""
        with patch('subprocess.Popen') as mock_popen:
            # Mock successful startup
            mock_process = Mock()
            mock_process.poll.return_value = None
            mock_process.pid = 12345
            mock_popen.return_value = mock_process
    
            success = manager.start_server("background")
            assert success is True
            assert "neozork_mcp" in manager.running_servers
    
            server_info = manager.running_servers["neozork_mcp"]
            assert server_info["pid"] == 12345
            assert "start_time" in server_info
        
        # Clean up for next test
        manager.running_servers.clear()
        
        with patch('subprocess.Popen') as mock_popen:
            # Mock failed startup
            mock_process = Mock()
            mock_process.poll.return_value = 1  # Process exited
            mock_process.communicate.return_value = ("", "Error message")
            mock_popen.return_value = mock_process
    
            success = manager.start_server("background")
            assert success is False
            assert "neozork_mcp" not in manager.running_servers
    
    def test_stop_server(self, manager):
        """Test server shutdown"""
        # Setup running server
        mock_process = Mock()
        mock_process.poll.return_value = None
        manager.running_servers["neozork_mcp"] = {
            "process": mock_process,
            "start_time": time.time(),
            "pid": 12345
        }
        
        success = manager.stop_server()
        assert success is True
        assert "neozork_mcp" not in manager.running_servers
    
    def test_check_server_health(self, manager):
        """Test server health checking"""
        # Setup running server
        mock_process = Mock()
        mock_process.poll.return_value = None
        manager.running_servers["neozork_mcp"] = {
            "process": mock_process,
            "start_time": time.time(),
            "pid": 12345
        }
        
        # Test healthy server
        manager.check_server_health()
        assert "neozork_mcp" in manager.running_servers
        
        # Test dead server
        mock_process.poll.return_value = 1  # Process exited
        manager.check_server_health()
        assert "neozork_mcp" not in manager.running_servers
    
    def test_evaluate_servers(self, manager):
        """Test server evaluation"""
        with patch.object(manager, 'should_start_server') as mock_should_start:
            mock_should_start.return_value = True
            
            with patch.object(manager, 'start_server') as mock_start:
                mock_start.return_value = True
                
                manager.evaluate_servers()
                mock_start.assert_called_once()
    
    def test_get_status(self, manager):
        """Test status reporting"""
        status = manager.get_status()
        
        assert "manager_running" in status
        assert "auto_start_enabled" in status
        assert "servers" in status
        assert status["manager_running"] is True
        assert status["auto_start_enabled"] is True
    
    def test_create_ide_config(self, manager):
        """Test IDE configuration creation"""
        # Test Cursor config
        with patch.object(manager, '_create_cursor_config') as mock_create:
            mock_create.return_value = True
            success = manager.create_ide_config("cursor")
            assert success is True
            mock_create.assert_called_once()
        
        # Test PyCharm config
        with patch.object(manager, '_create_pycharm_config') as mock_create:
            mock_create.return_value = True
            success = manager.create_ide_config("pycharm")
            assert success is True
            mock_create.assert_called_once()
        
        # Test VS Code config
        with patch.object(manager, '_create_vscode_config') as mock_create:
            mock_create.return_value = True
            success = manager.create_ide_config("vscode")
            assert success is True
            mock_create.assert_called_once()
        
        # Test unsupported IDE
        success = manager.create_ide_config("unsupported")
        assert success is False

class TestNeozorkMCPManagerCLI:
    """Test CLI interface"""
    
    @pytest.fixture
    def cli(self):
        """Create CLI instance"""
        cli = NeozorkMCPManagerCLI()
        yield cli
    
    def test_start(self, cli):
        """Test CLI start command"""
        with patch.object(cli, 'manager') as mock_manager:
            cli.manager = Mock()
            cli.start()
            cli.manager.run.assert_called_once()
    
    def test_status(self, cli):
        """Test CLI status command"""
        with patch('scripts.neozork_mcp_manager.NeozorkMCPManager') as mock_manager_class:
            mock_manager = Mock()
            mock_manager_class.return_value = mock_manager
            
            mock_manager.get_status.return_value = {
                "manager_running": True,
                "auto_start_enabled": True,
                "servers": {}
            }
            
            mock_manager.check_project_conditions.return_value = {
                "python_files": True,
                "financial_data": True
            }
            
            mock_manager.detect_ide.return_value = None
            
            cli.status()
            
            mock_manager.get_status.assert_called_once()
            mock_manager.check_project_conditions.assert_called_once()
            mock_manager.detect_ide.assert_called_once()
    
    def test_stop(self, cli):
        """Test CLI stop command"""
        with patch('scripts.neozork_mcp_manager.NeozorkMCPManager') as mock_manager_class:
            mock_manager = Mock()
            mock_manager_class.return_value = mock_manager
            
            cli.stop()
            
            mock_manager.stop_server.assert_called_once()
    
    def test_restart(self, cli):
        """Test CLI restart command"""
        with patch('scripts.neozork_mcp_manager.NeozorkMCPManager') as mock_manager_class:
            mock_manager = Mock()
            mock_manager_class.return_value = mock_manager
            
            cli.restart()
            
            mock_manager.stop_server.assert_called_once()
            mock_manager.start_server.assert_called_once()
    
    def test_manual_start(self, cli):
        """Test CLI manual start command"""
        with patch('scripts.neozork_mcp_manager.NeozorkMCPManager') as mock_manager_class:
            mock_manager = Mock()
            mock_manager_class.return_value = mock_manager
            mock_manager.start_server.return_value = True
            
            cli.manual_start("background")
            
            mock_manager.start_server.assert_called_once_with("background")
    
    def test_create_config(self, cli):
        """Test CLI create config command"""
        with patch('scripts.neozork_mcp_manager.NeozorkMCPManager') as mock_manager_class:
            mock_manager = Mock()
            mock_manager_class.return_value = mock_manager
            mock_manager.create_ide_config.return_value = True
            
            cli.create_config("cursor")
            
            mock_manager.create_ide_config.assert_called_once_with("cursor")

class TestIDEConfigCreation:
    """Test IDE configuration creation"""
    
    @pytest.fixture
    def temp_project(self):
        """Create temporary project directory"""
        temp_dir = tempfile.mkdtemp()
        project_path = Path(temp_dir)
        yield project_path
        shutil.rmtree(temp_dir)
    
    def test_create_cursor_config(self, temp_project):
        """Test Cursor configuration creation"""
        manager = NeozorkMCPManager(project_root=temp_project)
        
        success = manager._create_cursor_config()
        assert success is True
        
        config_file = temp_project / ".cursor" / "settings.json"
        assert config_file.exists()
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        assert "mcpServers" in config
        assert "neozork-mcp" in config["mcpServers"]
    
    def test_create_pycharm_config(self, temp_project):
        """Test PyCharm configuration creation"""
        manager = NeozorkMCPManager(project_root=temp_project)
        
        success = manager._create_pycharm_config()
        assert success is True
        
        config_file = temp_project / ".idea" / "mcp_servers.xml"
        assert config_file.exists()
        
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "neozork-mcp" in content
        assert "python" in content
    
    def test_create_vscode_config(self, temp_project):
        """Test VS Code configuration creation"""
        manager = NeozorkMCPManager(project_root=temp_project)
        
        success = manager._create_vscode_config()
        assert success is True
        
        config_file = temp_project / ".vscode" / "settings.json"
        assert config_file.exists()
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        assert "mcp.servers" in config
        assert "neozork-mcp" in config["mcp.servers"]

class TestErrorHandling:
    """Test error handling"""
    
    @pytest.fixture
    def temp_project(self):
        """Create temporary project directory"""
        temp_dir = tempfile.mkdtemp()
        project_path = Path(temp_dir)
        
        # Create project structure
        (project_path / "src").mkdir()
        (project_path / "data").mkdir()
        
        # Create sample Python file
        (project_path / "src" / "main.py").write_text("print('Hello, World!')")
        
        # Create the MCP server file
        (project_path / "neozork_mcp_server.py").write_text("""
#!/usr/bin/env python3
# Test MCP server file
print("Test MCP server")
""")
        
        # Create sample config
        config = {
            "auto_start": {
                "enabled": True,
                "check_interval": 30,
                "ide_detection": True,
                "project_detection": True
            },
            "server": {
                "command": "python",
                "args": ["neozork_mcp_server.py"],
                "env": {
                    "PYTHONPATH": str(project_path),
                    "LOG_LEVEL": "INFO"
                },
                "cwd": str(project_path)
            },
            "conditions": {
                "cursor_ide": {
                    "processes": ["Cursor", "cursor"],
                    "files": [".cursor", "cursor_mcp_config.json"]
                },
                "pycharm_ide": {
                    "processes": ["pycharm", "PyCharm"],
                    "files": [".idea", "pycharm_mcp_config.json"]
                },
                "python_files": {
                    "extensions": [".py"],
                    "min_files": 1
                },
                "financial_data": {
                    "directories": ["mql5_feed", "data"],
                    "files": ["*.csv", "*.parquet"]
                }
            }
        }
        
        (project_path / "neozork_mcp_config.json").write_text(json.dumps(config, indent=2))
        
        yield project_path
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def manager(self, temp_project):
        """Create manager instance"""
        manager = NeozorkMCPManager(project_root=temp_project)
        yield manager
    
    def test_config_load_error(self, temp_project):
        """Test configuration load error handling"""
        # Remove config file
        config_file = temp_project / "neozork_mcp_config.json"
        if config_file.exists():
            config_file.unlink()
        
        # Should not crash
        manager = NeozorkMCPManager(project_root=temp_project)
        assert manager.config is not None
        assert "auto_start" in manager.config
    
    def test_process_error(self, manager):
        """Test process error handling"""
        with patch('psutil.process_iter') as mock_process_iter:
            mock_process_iter.side_effect = Exception("Process error")
            
            ide = manager.detect_ide()
            assert ide is None
    
    def test_server_start_error(self, manager):
        """Test server start error handling"""
        with patch('subprocess.Popen') as mock_popen:
            mock_popen.side_effect = Exception("Start error")
            
            success = manager.start_server("background")
            assert success is False
    
    def test_file_monitoring_error(self, manager):
        """Test file monitoring error handling"""
        with patch('watchdog.observers.Observer') as mock_observer:
            mock_observer.side_effect = Exception("Observer error")
            
            # Should not crash
            manager.monitor_project_changes()
            assert manager.observer is None

class TestPerformance:
    """Test performance aspects"""
    
    @pytest.fixture
    def temp_project(self):
        """Create temporary project directory"""
        temp_dir = tempfile.mkdtemp()
        project_path = Path(temp_dir)
        
        # Create project structure
        (project_path / "src").mkdir()
        (project_path / "data").mkdir()
        
        # Create sample Python file
        (project_path / "src" / "main.py").write_text("print('Hello, World!')")
        
        # Create the MCP server file
        (project_path / "neozork_mcp_server.py").write_text("""
#!/usr/bin/env python3
# Test MCP server file
print("Test MCP server")
""")
        
        # Create sample config
        config = {
            "auto_start": {
                "enabled": True,
                "check_interval": 30,
                "ide_detection": True,
                "project_detection": True
            },
            "server": {
                "command": "python",
                "args": ["neozork_mcp_server.py"],
                "env": {
                    "PYTHONPATH": str(project_path),
                    "LOG_LEVEL": "INFO"
                },
                "cwd": str(project_path)
            },
            "conditions": {
                "cursor_ide": {
                    "processes": ["Cursor", "cursor"],
                    "files": [".cursor", "cursor_mcp_config.json"]
                },
                "pycharm_ide": {
                    "processes": ["pycharm", "PyCharm"],
                    "files": [".idea", "pycharm_mcp_config.json"]
                },
                "python_files": {
                    "extensions": [".py"],
                    "min_files": 1
                },
                "financial_data": {
                    "directories": ["mql5_feed", "data"],
                    "files": ["*.csv", "*.parquet"]
                }
            }
        }
        
        (project_path / "neozork_mcp_config.json").write_text(json.dumps(config, indent=2))
        
        yield project_path
        
        # Cleanup
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def manager(self, temp_project):
        """Create manager instance"""
        manager = NeozorkMCPManager(project_root=temp_project)
        yield manager
    
    def test_condition_check_performance(self, manager):
        """Test condition check performance"""
        start_time = time.time()
        
        for _ in range(100):
            conditions = manager.check_project_conditions()
        
        end_time = time.time()
        
        # Should be fast
        assert end_time - start_time < 5  # 5 seconds max
        assert conditions is not None
    
    def test_server_evaluation_performance(self, manager):
        """Test server evaluation performance"""
        start_time = time.time()
        
        for _ in range(50):
            manager.evaluate_servers()
        
        end_time = time.time()
        
        # Should be fast
        assert end_time - start_time < 3  # 3 seconds max
    
    def test_status_reporting_performance(self, manager):
        """Test status reporting performance"""
        start_time = time.time()
        
        for _ in range(100):
            status = manager.get_status()
        
        end_time = time.time()
        
        # Should be very fast
        assert end_time - start_time < 1  # 1 second max
        assert status is not None

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 