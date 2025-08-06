#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP Server Docker Client Test
Tests MCP server communication in Docker environment
"""

import json
import socket
import time
import sys
from typing import Dict, Any

def print_status(message: str, status: str = "INFO"):
    """Print status message with timestamp"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{status}] {message}")

def test_mcp_socket_connection():
    """Test connection to MCP socket server"""
    print_status("=== Testing MCP Socket Connection ===")
    
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
        ("neozork/projectInfo", {}),
        ("neozork/financialData", {}),
        ("neozork/indicators", {})
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

def test_mcp_performance():
    """Test MCP server performance"""
    print_status("=== Testing MCP Performance ===")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(('localhost', 8080))
        
        # Test multiple rapid requests
        start_time = time.time()
        
        for i in range(10):
            test_message = {
                "jsonrpc": "2.0",
                "id": i + 1,
                "method": "neozork/ping",
                "params": {}
            }
            
            sock.send(json.dumps(test_message).encode('utf-8'))
            response = sock.recv(4096)
            
            if i % 3 == 0:
                print_status(f"Completed {i + 1}/10 requests...")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print_status(f"✅ Performance test completed in {duration:.2f} seconds")
        print_status(f"Average response time: {duration/10:.3f} seconds per request")
        
        sock.close()
        return True
        
    except Exception as e:
        print_status(f"❌ Performance test failed: {e}", "ERROR")
        return False

def main():
    """Main test function"""
    print_status("🚀 Starting MCP Docker Client Tests", "INFO")
    print_status("=" * 50)
    
    tests = [
        ("Socket Connection", test_mcp_socket_connection),
        ("MCP Methods", test_mcp_methods),
        ("Performance", test_mcp_performance)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print_status(f"\n--- Running {test_name} Test ---")
        try:
            success = test_func()
            results[test_name] = success
        except Exception as e:
            print_status(f"❌ {test_name} test failed with exception: {e}", "ERROR")
            results[test_name] = False
    
    # Final summary
    print_status("\n" + "=" * 50)
    print_status("=== FINAL TEST RESULTS ===")
    
    successful_tests = sum(1 for success in results.values() if success)
    total_tests = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print_status(f"{status}: {test_name}")
    
    print_status(f"\nOverall: {successful_tests}/{total_tests} tests passed")
    
    if successful_tests == total_tests:
        print_status("🎉 All tests passed! MCP server is working correctly.", "SUCCESS")
        sys.exit(0)
    else:
        print_status("❌ Some tests failed. Check MCP server configuration.", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main() 