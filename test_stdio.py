#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for PyCharm GitHub Copilot MCP Server stdio mode
"""

import json
import subprocess
import sys
import time
import select
from pathlib import Path

def test_stdio_mode():
    """Test the MCP server in stdio mode"""
    print("🧪 Testing PyCharm GitHub Copilot MCP Server in stdio mode...")
    
    # Start the server
    server_process = subprocess.Popen(
        ["python", "pycharm_github_copilot_mcp.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Wait for server to initialize
        print("⏳ Waiting for server initialization...")
        time.sleep(3)
        
        # Test initialize request
        print("📤 Sending initialize request...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "processId": 12345,
                "rootUri": f"file://{Path.cwd()}",
                "capabilities": {}
            }
        }
        
        # Send request
        request_str = json.dumps(init_request) + '\n'
        server_process.stdin.write(request_str)
        server_process.stdin.flush()
        
        # Read response with timeout
        print("📥 Reading response...")
        if select.select([server_process.stdout], [], [], 5.0)[0]:
            response_line = server_process.stdout.readline()
            if response_line.strip():
                try:
                    response = json.loads(response_line.strip())
                    server_name = response.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')
                    print(f"✅ Received response: {server_name}")
                except json.JSONDecodeError as e:
                    print(f"❌ Invalid JSON response: {e}")
                    print(f"Raw response: {response_line}")
            else:
                print("❌ Empty response received")
        else:
            print("❌ No response received (timeout)")
            
        # Test completion request
        print("📤 Sending completion request...")
        completion_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "textDocument/completion",
            "params": {
                "textDocument": {
                    "uri": f"file://{Path.cwd()}/test.py"
                },
                "position": {
                    "line": 0,
                    "character": 0
                }
            }
        }
        
        # Send request
        request_str = json.dumps(completion_request) + '\n'
        server_process.stdin.write(request_str)
        server_process.stdin.flush()
        
        # Read response with timeout
        if select.select([server_process.stdout], [], [], 5.0)[0]:
            response_line = server_process.stdout.readline()
            if response_line.strip():
                try:
                    response = json.loads(response_line.strip())
                    items_count = len(response.get('result', {}).get('items', []))
                    print(f"✅ Received {items_count} completion items")
                except json.JSONDecodeError as e:
                    print(f"❌ Invalid JSON response: {e}")
            else:
                print("❌ Empty completion response")
        else:
            print("❌ No completion response (timeout)")
            
        # Test shutdown request
        print("📤 Sending shutdown request...")
        shutdown_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "shutdown",
            "params": {}
        }
        
        # Send request
        request_str = json.dumps(shutdown_request) + '\n'
        server_process.stdin.write(request_str)
        server_process.stdin.flush()
        
        # Read response with timeout
        if select.select([server_process.stdout], [], [], 5.0)[0]:
            response_line = server_process.stdout.readline()
            if response_line.strip():
                try:
                    response = json.loads(response_line.strip())
                    print("✅ Shutdown response received")
                except json.JSONDecodeError as e:
                    print(f"❌ Invalid JSON response: {e}")
            else:
                print("❌ Empty shutdown response")
        else:
            print("❌ No shutdown response (timeout)")
            
        # Test exit request
        print("📤 Sending exit request...")
        exit_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "exit",
            "params": {}
        }
        
        # Send request
        request_str = json.dumps(exit_request) + '\n'
        server_process.stdin.write(request_str)
        server_process.stdin.flush()
        
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Clean up
        print("🧹 Cleaning up...")
        if server_process.poll() is None:
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
        
        # Check for any error output
        stderr_output = server_process.stderr.read()
        if stderr_output:
            print(f"⚠️ Server stderr output: {stderr_output}")
        
        print("🧹 Cleanup completed")

if __name__ == "__main__":
    test_stdio_mode() 