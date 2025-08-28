#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test MCP Server Ready File Flag
Test the file-based ready flag functionality
"""

import pytest
import tempfile
import time
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.mcp.check_mcp_ready import check_mcp_ready


class TestReadyFile:
    """Test the ready file functionality"""
    
    def test_ready_file_not_exists(self):
        """Test when ready file doesn't exist"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_project = Path(temp_dir)
            assert check_mcp_ready(temp_project) is False
    
    def test_ready_file_exists_and_valid(self):
        """Test when ready file exists and is valid"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_project = Path(temp_dir)
            logs_dir = temp_project / "logs"
            logs_dir.mkdir(exist_ok=True)
            
            ready_file = logs_dir / "mcp_server_ready.flag"
            with open(ready_file, 'w') as f:
                f.write("ready:2025-08-28T15:50:12.901063\n")
            
            assert check_mcp_ready(temp_project) is True
    
    def test_ready_file_old(self):
        """Test when ready file is too old"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_project = Path(temp_dir)
            logs_dir = temp_project / "logs"
            logs_dir.mkdir(exist_ok=True)
            
            ready_file = logs_dir / "mcp_server_ready.flag"
            with open(ready_file, 'w') as f:
                f.write("ready:2025-08-28T15:50:12.901063\n")
            
            # Make file old by setting modification time to 10 minutes ago
            old_time = time.time() - 600  # 10 minutes ago
            os.utime(ready_file, (old_time, old_time))
            
            assert check_mcp_ready(temp_project) is False
    
    def test_ready_file_invalid_content(self):
        """Test when ready file has invalid content"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_project = Path(temp_dir)
            logs_dir = temp_project / "logs"
            logs_dir.mkdir(exist_ok=True)
            
            ready_file = logs_dir / "mcp_server_ready.flag"
            with open(ready_file, 'w') as f:
                f.write("invalid:content\n")
            
            assert check_mcp_ready(temp_project) is False
    
    def test_ready_file_empty(self):
        """Test when ready file is empty"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_project = Path(temp_dir)
            logs_dir = temp_project / "logs"
            logs_dir.mkdir(exist_ok=True)
            
            ready_file = logs_dir / "mcp_server_ready.flag"
            ready_file.touch()
            
            assert check_mcp_ready(temp_project) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
