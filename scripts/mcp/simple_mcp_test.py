#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simple MCP Server Test
Quick test for MCP server in Docker
"""

import json
import socket
import time
import sys
import subprocess
import os

def print_status(message: str):
    """Print status message"""
    print(f"[{time.strftime('%H:%M:%S')}] {message}")

def test_mcp_server():
    """Test MCP server"""
    print_status("=== Simple MCP Server Test ===")
    
    # Check environment
    docker_container = os.environ.get("DOCKER_CONTAINER", "false")
    print_status(f"DOCKER_CONTAINER: {docker_container}")
    
    # Start MCP server
    print_status("Starting MCP server...")
    env = os.environ.copy()
    env["DOCKER_CONTAINER"] = "true"
    
    process = subprocess.Popen(
        ["python3", "neozork_mcp_server.py"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print_status(f"MCP server PID: {process.pid}")
    
    # Wait for server to start
    print_status("Waiting for server to start...")
    time.sleep(10)
    
    # Check if process is running
    if process.poll() is not None:
        stdout, stderr = process.communicate()
        print_status(f"❌ Server died. Exit code: {process.returncode}")
        print_status(f"Stdout: {stdout}")
        print_status(f"Stderr: {stderr}")
        return False
    
    print_status("✅ Server is running")
    
    # Test socket connection
    print_status("Testing socket connection...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('localhost', 8080))
        print_status("✅ Socket connection successful")
        
        # Test ping
        ping_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "neozork/ping",
            "params": {}
        }
        
        print_status("Sending ping request...")
        sock.send(json.dumps(ping_request).encode('utf-8'))
        
        response = sock.recv(4096)
        response_data = json.loads(response.decode('utf-8'))
        
        print_status(f"Response: {json.dumps(response_data, indent=2)}")
        
        if response_data.get("result", {}).get("pong"):
            print_status("✅ Ping successful")
            result = True
        else:
            print_status("❌ Ping failed")
            result = False
            
        sock.close()
        
    except Exception as e:
        print_status(f"❌ Socket test failed: {e}")
        result = False
    
    # Cleanup
    print_status("Stopping server...")
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    
    return result

if __name__ == "__main__":
    success = test_mcp_server()
    sys.exit(0 if success else 1) 