#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quick MCP Server Test
Fast test for MCP server fixes
"""

import json
import socket
import time
import sys
import os

def test_mcp_socket():
    """Test MCP socket server"""
    print("=== Quick MCP Socket Test ===")
    
    try:
        # Connect to socket server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        print("Connecting to MCP server on localhost:8080...")
        sock.connect(('localhost', 8080))
        print("✅ Connected to MCP server")
        
        # Test ping request
        ping_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "neozork/ping",
            "params": {}
        }
        
        print("Sending ping request...")
        sock.send(json.dumps(ping_request).encode('utf-8'))
        
        # Receive response
        response = sock.recv(4096)
        response_data = json.loads(response.decode('utf-8'))
        
        print(f"Response: {json.dumps(response_data, indent=2)}")
        
        if response_data.get("result", {}).get("pong"):
            print("✅ Ping successful!")
            return True
        else:
            print("❌ Ping failed")
            return False
            
    except ConnectionRefusedError:
        print("❌ Connection refused - server not running")
        return False
    except socket.timeout:
        print("❌ Connection timeout")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        try:
            sock.close()
        except:
            pass

def test_mcp_methods():
    """Test various MCP methods"""
    print("\n=== Testing MCP Methods ===")
    
    methods = [
        ("neozork/ping", {}),
        ("neozork/status", {}),
        ("neozork/health", {}),
        ("neozork/version", {})
    ]
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('localhost', 8080))
        
        for method, params in methods:
            try:
                request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": method,
                    "params": params
                }
                
                print(f"Testing {method}...")
                sock.send(json.dumps(request).encode('utf-8'))
                
                response = sock.recv(4096)
                response_data = json.loads(response.decode('utf-8'))
                
                if "error" in response_data:
                    print(f"❌ {method}: {response_data['error']['message']}")
                else:
                    print(f"✅ {method}: Success")
                    
            except Exception as e:
                print(f"❌ {method}: {e}")
        
        sock.close()
        return True
        
    except Exception as e:
        print(f"❌ Socket error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting Quick MCP Test")
    
    # Test 1: Socket connection and ping
    test1_success = test_mcp_socket()
    
    # Test 2: Multiple methods
    test2_success = test_mcp_methods()
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"Socket Test: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Methods Test: {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    if test1_success and test2_success:
        print("\n🎉 All tests passed!")
        return True
    else:
        print("\n❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 