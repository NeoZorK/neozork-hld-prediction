#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Integrated MCP Server Test for Docker
Tests MCP server in a single container
"""

import json
import socket
import time
import sys
import subprocess
import threading
import os
from typing import Dict, Any

def print_status(message: str, status: str = "INFO"):
    """Print status message with timestamp"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{status}] {message}")

def wait_for_server(port=8080, timeout=30):
    """Wait for server to be ready"""
    print_status(f"Waiting for server on port {port}...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            
            if result == 0:
                print_status(f"✅ Server is ready on port {port}", "SUCCESS")
                return True
                
        except Exception:
            pass
        
        time.sleep(1)
        print_status(f"Waiting... ({int(time.time() - start_time)}s)")
    
    print_status(f"❌ Server not ready on port {port} after {timeout}s", "ERROR")
    return False

def start_mcp_server():
    """Start MCP server in background"""
    print_status("=== Starting MCP Server ===")
    
    # Set Docker environment
    env = os.environ.copy()
    env["DOCKER_CONTAINER"] = "true"
    
    try:
        # Start MCP server in background
        process = subprocess.Popen(
            ["python3", "neozork_mcp_server.py"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print_status(f"MCP server started with PID: {process.pid}")
        
        # Wait for server to be ready
        if wait_for_server(8080, 30):
            print_status("✅ MCP server is running and ready", "SUCCESS")
            return process
        else:
            # Check if process is still running
            if process.poll() is None:
                stdout, stderr = process.communicate()
                print_status(f"❌ MCP server failed to start properly", "ERROR")
                print_status(f"Stdout: {stdout}")
                print_status(f"Stderr: {stderr}")
            else:
                stdout, stderr = process.communicate()
                print_status(f"❌ MCP server process died", "ERROR")
                print_status(f"Stdout: {stdout}")
                print_status(f"Stderr: {stderr}")
            return None
            
    except Exception as e:
        print_status(f"❌ Error starting MCP server: {e}", "ERROR")
        return None

def test_mcp_connection():
    """Test connection to MCP server"""
    print_status("=== Testing MCP Connection ===")
    
    try:
        # Connect to MCP socket server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        
        print_status("Connecting to MCP server on localhost:8080...")
        sock.connect(('localhost', 8080))
        print_status("✅ Connected to MCP server")
        
        # Test ping request
        test_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "neozork/ping",
            "params": {}
        }
        
        print_status("Sending ping request...")
        sock.send(json.dumps(test_message).encode('utf-8'))
        
        # Receive response
        response = sock.recv(4096)
        response_data = json.loads(response.decode('utf-8'))
        
        print_status(f"Received response: {json.dumps(response_data, indent=2)}")
        
        if response_data.get("result", {}).get("pong"):
            print_status("✅ Ping test successful", "SUCCESS")
            return True
        else:
            print_status("❌ Ping test failed", "ERROR")
            return False
            
    except socket.timeout:
        print_status("❌ Connection timeout", "ERROR")
        return False
    except ConnectionRefusedError:
        print_status("❌ Connection refused - server not running", "ERROR")
        return False
    except Exception as e:
        print_status(f"❌ Connection error: {e}", "ERROR")
        return False
    finally:
        try:
            sock.close()
        except:
            pass

def test_mcp_methods():
    """Test various MCP methods"""
    print_status("=== Testing MCP Methods ===")
    
    methods_to_test = [
        ("neozork/ping", {}),
        ("neozork/status", {}),
        ("neozork/health", {}),
        ("neozork/version", {}),
        ("neozork/capabilities", {}),
        ("neozork/projectInfo", {})
    ]
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(('localhost', 8080))
        
        results = {}
        
        for method, params in methods_to_test:
            try:
                test_message = {
                    "jsonrpc": "2.0",
                    "id": len(results) + 1,
                    "method": method,
                    "params": params
                }
                
                print_status(f"Testing method: {method}")
                sock.send(json.dumps(test_message).encode('utf-8'))
                
                response = sock.recv(4096)
                response_data = json.loads(response.decode('utf-8'))
                
                if "error" in response_data:
                    print_status(f"❌ {method}: {response_data['error']['message']}", "ERROR")
                    results[method] = False
                else:
                    print_status(f"✅ {method}: Success", "SUCCESS")
                    results[method] = True
                    
            except Exception as e:
                print_status(f"❌ {method}: {e}", "ERROR")
                results[method] = False
        
        sock.close()
        
        # Summary
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        print_status(f"=== Test Summary: {successful}/{total} methods successful ===")
        
        return successful == total
        
    except Exception as e:
        print_status(f"Error testing methods: {e}", "ERROR")
        return False

def main():
    """Main test function"""
    print_status("🚀 Starting Integrated MCP Server Test", "INFO")
    print_status("=" * 50)
    
    # Step 1: Start MCP server
    server_process = start_mcp_server()
    if not server_process:
        print_status("❌ Failed to start MCP server", "ERROR")
        sys.exit(1)
    
    try:
        # Step 2: Test connection
        connection_success = test_mcp_connection()
        
        # Step 3: Test methods
        methods_success = test_mcp_methods()
        
        # Final summary
        print_status("\n" + "=" * 50)
        print_status("=== FINAL TEST RESULTS ===")
        
        if connection_success and methods_success:
            print_status("🎉 All tests passed! MCP server is working correctly.", "SUCCESS")
            result = True
        else:
            print_status("❌ Some tests failed. Check MCP server configuration.", "ERROR")
            result = False
            
    finally:
        # Cleanup
        print_status("Stopping MCP server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        
        print_status("MCP server stopped")
    
    sys.exit(0 if result else 1)

if __name__ == "__main__":
    main() 