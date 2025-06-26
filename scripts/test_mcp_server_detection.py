#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to start MCP server in background and test detection
"""

import subprocess
import time
import signal
import os
import sys
from pathlib import Path

def start_mcp_server_background():
    """Start MCP server in background mode"""
    print("🚀 Starting MCP server in background...")
    
    # Start MCP server with nohup to run in background
    cmd = [
        "nohup", 
        "python3", 
        "neozork_mcp_server.py",
        "--debug"
    ]
    
    try:
        # Start process in background
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid  # Create new process group
        )
        
        print(f"✅ MCP server started with PID: {process.pid}")
        
        # Save PID to file for our detection script
        with open("/tmp/mcp_server.pid", "w") as f:
            f.write(str(process.pid))
        
        return process
        
    except Exception as e:
        print(f"❌ Failed to start MCP server: {e}")
        return None

def test_detection():
    """Test our detection script"""
    print("\n🔍 Testing MCP server detection...")
    
    # Wait a moment for server to start
    time.sleep(2)
    
    # Test our detection script
    try:
        result = subprocess.run(
            ["python3", "scripts/check_mcp_status.py", "--debug-detect"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        print(f"Detection result: {result.stdout.strip()}")
        print(f"Exit code: {result.returncode}")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ Detection test timed out")
        return False
    except Exception as e:
        print(f"❌ Detection test failed: {e}")
        return False

def stop_mcp_server(process):
    """Stop MCP server"""
    if process:
        print(f"\n🛑 Stopping MCP server (PID: {process.pid})...")
        
        try:
            # Kill the process group
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            
            # Wait for graceful shutdown
            try:
                process.wait(timeout=5)
                print("✅ MCP server stopped gracefully")
            except subprocess.TimeoutExpired:
                # Force kill if needed
                os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                print("⚠️ MCP server force killed")
                
        except Exception as e:
            print(f"❌ Error stopping MCP server: {e}")
    
    # Clean up PID file
    try:
        os.remove("/tmp/mcp_server.pid")
    except FileNotFoundError:
        pass

def main():
    """Main test function"""
    print("🧪 MCP Server Detection Test")
    print("=" * 40)
    
    # Check if we're in Docker
    if os.path.exists("/.dockerenv"):
        print("🐳 Running in Docker container")
    else:
        print("💻 Running on host system")
    
    # Start MCP server
    process = start_mcp_server_background()
    if not process:
        print("❌ Cannot continue without MCP server")
        return 1
    
    try:
        # Test detection
        detected = test_detection()
        
        if detected:
            print("✅ MCP server successfully detected!")
            return 0
        else:
            print("❌ MCP server not detected")
            return 1
            
    finally:
        # Always clean up
        stop_mcp_server(process)

if __name__ == "__main__":
    sys.exit(main()) 