#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script for PyCharm GitHub Copilot MCP Server stdio mode
Can be run from any directory
"""

import json
import subprocess
import sys
import time
import select
from pathlib import Path

# Try to import pytest, but handle gracefully if not available
try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    # Create mock pytest functions for standalone execution
    class MockPytest:
        @staticmethod
        def skip(reason):
            print(f"SKIPPED: {reason}")
            sys.exit(0)
        
        @staticmethod
        def fail(reason):
            print(f"FAILED: {reason}")
            raise AssertionError(reason)
    
    pytest = MockPytest()

def test_stdio_mode():
    """Test the MCP server in stdio mode"""
    print("🧪 Testing PyCharm GitHub Copilot MCP Server in stdio mode...")
    
    # Get project root (parent of tests directory)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    server_file = project_root / "pycharm_github_copilot_mcp.py"
    
    if not server_file.exists():
        pytest.skip(f"Server file not found: {server_file}")
    
    print(f"📁 Project root: {project_root}")
    print(f"🐍 Server file: {server_file}")
    
    # Start the server
    server_process = subprocess.Popen(
        [sys.executable, str(server_file)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        cwd=str(project_root)  # Set working directory to project root
    )
    
    try:
        # Wait for server to initialize
        print("⏳ Waiting for server initialization...")
        time.sleep(3)
        
        # Prepare all requests
        requests = [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "processId": 12345,
                    "rootUri": f"file://{project_root}",
                    "capabilities": {}
                }
            },
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "textDocument/completion",
                "params": {
                    "textDocument": {
                        "uri": f"file://{project_root}/test.py"
                    },
                    "position": {
                        "line": 0,
                        "character": 0
                    }
                }
            },
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "shutdown",
                "params": {}
            },
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "exit",
                "params": {}
            }
        ]
        
        # Send all requests at once
        print("📤 Sending all requests...")
        for req in requests:
            req_str = json.dumps(req) + '\n'
            server_process.stdin.write(req_str)
        server_process.stdin.flush()
        print("✅ All requests sent successfully")
        
        # Read all responses
        print("📥 Reading responses...")
        responses = {}
        expected_ids = {1, 2, 3}  # We expect responses for initialize, completion, and shutdown
        timeout = time.time() + 15  # 15 second timeout
        
        while expected_ids and time.time() < timeout:
            line = server_process.stdout.readline()
            if not line:
                print("⚠️ No more output from server")
                break
                
            line = line.strip()
            if not line:
                continue
                
            print(f"[STDOUT] {line[:100]}{'...' if len(line) > 100 else ''}")
            
            try:
                resp = json.loads(line)
                resp_id = resp.get('id')
                if resp_id in expected_ids:
                    responses[resp_id] = resp
                    expected_ids.remove(resp_id)
                    print(f"✅ Received response for id {resp_id}")
                else:
                    print(f"ℹ️ Received response for unexpected id {resp_id}")
            except json.JSONDecodeError as e:
                print(f"⚠️ Could not parse JSON response: {e}")
                print(f"Raw line (first 200 chars): {line[:200]}")
                # Try to read more lines to get complete JSON
                print("🔄 Attempting to read more lines for complete JSON...")
                continue
        
        # Check if we received all expected responses
        if expected_ids:
            pytest.fail(f"Did not receive responses for ids: {expected_ids}")
        
        # Validate responses
        print("🔍 Validating responses...")
        
        # Validate initialize response
        if 1 in responses:
            resp = responses[1]
            assert resp.get('jsonrpc') == '2.0', "Invalid JSON-RPC version in initialize"
            assert 'result' in resp, "No result in initialize response"
            server_name = resp['result'].get('serverInfo', {}).get('name', 'Unknown')
            print(f"✅ Initialize response: {server_name}")
        else:
            pytest.fail("No initialize response received")
        
        # Validate completion response
        if 2 in responses:
            resp = responses[2]
            assert resp.get('jsonrpc') == '2.0', "Invalid JSON-RPC version in completion"
            assert 'result' in resp, "No result in completion response"
            items = resp['result'].get('items', [])
            print(f"✅ Completion response: {len(items)} items")
            # Check that we have some completion items
            assert len(items) > 0, "No completion items returned"
        else:
            pytest.fail("No completion response received")
        
        # Validate shutdown response
        if 3 in responses:
            resp = responses[3]
            assert resp.get('jsonrpc') == '2.0', "Invalid JSON-RPC version in shutdown"
            print("✅ Shutdown response received")
        else:
            pytest.fail("No shutdown response received")
        
        print("✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        pytest.fail(f"Error during testing: {e}")
        
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

def main():
    """Main function for standalone execution"""
    try:
        test_stdio_mode()
        print("🎉 All tests passed!")
        sys.exit(0)
    except Exception as e:
        print(f"💥 Some tests failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 