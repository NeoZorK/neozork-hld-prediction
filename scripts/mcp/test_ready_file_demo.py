#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Demo script for MCP Server Ready File Flag
Demonstrates the file-based ready flag functionality
"""

import json
import sys
import time
import tempfile
from pathlib import Path
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.mcp.check_mcp_ready import check_mcp_ready


def demo_ready_file():
    """Demonstrate the ready file functionality"""
    print("🚀 Starting MCP Server Ready File Demo")
    print("=" * 50)
    
    # Test 1: No ready file
    print("\n📋 Test 1: No ready file exists")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_project = Path(temp_dir)
        result = check_mcp_ready(temp_project)
        print(f"Result: {result} (Expected: False)")
        assert result is False
    
    # Test 2: Valid ready file
    print("\n📋 Test 2: Valid ready file exists")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_project = Path(temp_dir)
        logs_dir = temp_project / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        ready_file = logs_dir / "mcp_server_ready.flag"
        with open(ready_file, 'w') as f:
            f.write("ready:2025-08-28T15:50:12.901063\n")
        
        result = check_mcp_ready(temp_project)
        print(f"Result: {result} (Expected: True)")
        assert result is True
    
    # Test 3: Old ready file
    print("\n📋 Test 3: Old ready file (should be ignored)")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_project = Path(temp_dir)
        logs_dir = temp_project / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        ready_file = logs_dir / "mcp_server_ready.flag"
        with open(ready_file, 'w') as f:
            f.write("ready:2025-08-28T15:50:12.901063\n")
        
        # Make file old
        old_time = time.time() - 600  # 10 minutes ago
        os.utime(ready_file, (old_time, old_time))
        
        result = check_mcp_ready(temp_project)
        print(f"Result: {result} (Expected: False)")
        assert result is False
    
    # Test 4: Invalid content
    print("\n📋 Test 4: Invalid content in ready file")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_project = Path(temp_dir)
        logs_dir = temp_project / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        ready_file = logs_dir / "mcp_server_ready.flag"
        with open(ready_file, 'w') as f:
            f.write("invalid:content\n")
        
        result = check_mcp_ready(temp_project)
        print(f"Result: {result} (Expected: False)")
        assert result is False
    
    print("\n✅ All tests passed!")
    print("\n📝 How it works:")
    print("1. MCP server creates a ready flag file when initialization completes")
    print("2. Docker entrypoint script checks for this file with retry logic")
    print("3. File must be recent (< 5 minutes old) and contain 'ready:' prefix")
    print("4. This avoids the stdin/stdout communication issues with background processes")


if __name__ == "__main__":
    demo_ready_file()
