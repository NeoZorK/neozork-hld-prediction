#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple MCP Server Starter
Starts the MCP server with proper error handling
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def start_mcp_server():
    """Start the MCP server"""
    print("🚀 Starting MCP server...")
    
    # Get the project root
    project_root = Path(__file__).parent
    
    # Start the MCP server
    try:
        cmd = [sys.executable, str(project_root / "neozork_mcp_server.py")]
        print(f"Running command: {' '.join(cmd)}")
        
        # Start the process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"MCP server started with PID: {process.pid}")
        
        # Wait a bit for initialization
        time.sleep(5)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ MCP server is running successfully")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ MCP server failed to start")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting MCP server: {e}")
        return None

if __name__ == "__main__":
    start_mcp_server() 