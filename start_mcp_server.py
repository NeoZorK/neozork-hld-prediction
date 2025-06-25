#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple MCP Server Starter
Quick start script for Neozork MCP Server
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    """Start MCP server"""
    project_root = Path(__file__).parent
    
    print("🚀 Starting Neozork MCP Server...")
    print(f"📁 Project root: {project_root}")
    
    # Check if server file exists
    server_file = project_root / "neozork_mcp_server.py"
    if not server_file.exists():
        print(f"❌ Server file not found: {server_file}")
        return 1
    
    # Set environment
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)
    env["LOG_LEVEL"] = "INFO"
    
    try:
        # Start server in stdio mode
        print("🔄 Starting server in stdio mode...")
        process = subprocess.Popen(
            [sys.executable, "neozork_mcp_server.py"],
            cwd=project_root,
            env=env,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        
        print("✅ MCP Server started successfully")
        print("💡 Press Ctrl+C to stop the server")
        
        # Wait for process to complete
        process.wait()
        return 0
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return 0
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 