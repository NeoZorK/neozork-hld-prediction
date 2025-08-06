#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Optimized MCP Status Check
Quick test for the optimized check_mcp_status.py
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from scripts.mcp.check_mcp_status import DockerMCPServerChecker

def test_optimized_check():
    """Test the optimized MCP status checker"""
    print("=== Testing Optimized MCP Status Check ===")
    
    start_time = time.time()
    
    # Create checker
    checker = DockerMCPServerChecker()
    
    # Run comprehensive check
    print("Running comprehensive check...")
    results = checker.run_comprehensive_check()
    
    end_time = time.time()
    duration = end_time - start_time
    
    # Print results
    print(f"\n=== Results (took {duration:.2f}s) ===")
    print(f"Server Running: {results.get('server_running', False)}")
    print(f"Connection Status: {results.get('connection_test', {}).get('status', 'unknown')}")
    print(f"Socket Connection: {results.get('docker_specific', {}).get('socket_connection', False)}")
    print(f"MCP Responding: {results.get('docker_specific', {}).get('mcp_server_responding', False)}")
    
    # Print recommendations
    if results.get('recommendations'):
        print("\n=== Recommendations ===")
        for rec in results['recommendations']:
            print(f"- {rec}")
    
    return results

def main():
    """Main test function"""
    print("🚀 Testing Optimized MCP Status Check")
    
    try:
        results = test_optimized_check()
        
        # Check if test was successful
        if results.get('connection_test', {}).get('status') == 'success':
            print("\n✅ Test PASSED - MCP server is working correctly")
            return True
        else:
            print("\n❌ Test FAILED - MCP server has issues")
            return False
            
    except Exception as e:
        print(f"\n❌ Test ERROR: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 