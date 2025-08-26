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
import pytest
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

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
        # Test with debug detection
        result = subprocess.run(
            ["python3", "scripts/mcp/check_mcp_status.py", "--debug-detect"],
            capture_output=True,
            text=True,
            cwd=project_root
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

class TestMCPServerDetection:
    """Test class for MCP server detection"""
    
    def test_mcp_server_detection(self):
        """Test MCP server detection functionality"""
        print("🧪 Testing MCP server detection...")
        
        process = None
        try:
            # Start MCP server
            process = start_mcp_server_background()
            assert process is not None, "Failed to start MCP server"
            
            # Test detection
            detection_success = test_detection()
            assert detection_success, "MCP server detection failed"
            
            print("✅ MCP server detection test passed!")
            
        except Exception as e:
            print(f"❌ MCP server detection test failed: {e}")
            pytest.fail(f"Test failed: {e}")
        finally:
            # Always stop the server
            stop_mcp_server(process)

def main():
    """Run the test manually"""
    print("🧪 Running MCP server detection test...")
    
    process = None
    try:
        # Start MCP server
        process = start_mcp_server_background()
        if process is None:
            print("❌ Failed to start MCP server")
            return False
        
        # Test detection
        if test_detection():
            print("✅ MCP server detection test passed!")
            return True
        else:
            print("❌ MCP server detection test failed!")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False
    finally:
        # Always stop the server
        stop_mcp_server(process)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
