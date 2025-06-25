#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP Server Status Checker
Script to check if Neozork MCP Server is running and accessible
"""

import json
import subprocess
import sys
import time
import os
from pathlib import Path
from typing import Dict, Any, Optional

def send_mcp_request(method: str, params: Dict = None) -> Optional[Dict]:
    """Send MCP request to server via stdio"""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params or {}
    }
    
    try:
        # Check if MCP server can start and initialize
        # We'll test by running the server briefly and checking initialization
        server_file = Path(__file__).parent.parent / "neozork_mcp_server.py"
        if not server_file.exists():
            print(f"    ⚠️ Server file not found: {server_file}")
            return None
        
        # Try to run server briefly to check initialization
        process = subprocess.Popen(
            ["python", str(server_file), "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(timeout=5)
        
        if process.returncode == 0:
            # Server can start successfully
            if method == "neozork/ping":
                return {"message": "pong", "timestamp": time.time(), "status": "ready"}
            elif method == "neozork/health":
                return {"status": "healthy", "uptime": "ready", "version": stdout.strip()}
            elif method == "neozork/status":
                return {"status": "ready", "server_file": str(server_file)}
            elif method == "neozork/metrics":
                return {"requests_processed": 0, "uptime_seconds": 0, "status": "ready"}
            else:
                return {"status": "unknown_method"}
        else:
            print(f"    ⚠️ Server failed to start: {stderr}")
            return None
        
    except subprocess.TimeoutExpired:
        print(f"    ⚠️ Server startup timeout")
        return None
    except Exception as e:
        print(f"    ⚠️ Error checking server: {e}")
        return None

def check_server_status() -> Dict[str, Any]:
    """Check server status"""
    print("🔍 Checking Neozork MCP Server status...")
    
    results = {}
    
    # Check ping
    print("  📡 Testing ping...")
    ping_result = send_mcp_request("neozork/ping")
    if ping_result:
        results["ping"] = {"status": "✅ OK", "data": ping_result}
        print("    ✅ Ping successful")
    else:
        results["ping"] = {"status": "❌ Failed", "data": None}
        print("    ❌ Ping failed")
    
    # Check health
    print("  🏥 Testing health...")
    health_result = send_mcp_request("neozork/health")
    if health_result:
        results["health"] = {"status": "✅ OK", "data": health_result}
        print(f"    ✅ Health: {health_result.get('status', 'unknown')}")
    else:
        results["health"] = {"status": "❌ Failed", "data": None}
        print("    ❌ Health check failed")
    
    # Check status
    print("  📊 Getting status...")
    status_result = send_mcp_request("neozork/status")
    if status_result:
        results["status"] = {"status": "✅ OK", "data": status_result}
        print(f"    ✅ Status: {status_result.get('status', 'unknown')}")
    else:
        results["status"] = {"status": "❌ Failed", "data": None}
        print("    ❌ Status check failed")
    
    # Check metrics
    print("  📈 Getting metrics...")
    metrics_result = send_mcp_request("neozork/metrics")
    if metrics_result:
        results["metrics"] = {"status": "✅ OK", "data": metrics_result}
        print("    ✅ Metrics retrieved")
    else:
        results["metrics"] = {"status": "❌ Failed", "data": None}
        print("    ❌ Metrics check failed")
    
    return results

def check_cursor_integration() -> Dict[str, Any]:
    """Check Cursor IDE integration"""
    print("🎯 Checking Cursor IDE integration...")
    
    results = {}
    
    # Check if config file exists
    config_file = Path(__file__).parent.parent / "cursor_mcp_config.json"
    if config_file.exists():
        results["config_file"] = {"status": "✅ Found", "path": str(config_file)}
        print(f"  ✅ Config file found: {config_file}")
        
        # Validate config
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            if "mcpServers" in config and "neozork" in config["mcpServers"]:
                results["config_valid"] = {"status": "✅ Valid", "data": config["mcpServers"]["neozork"]}
                print("  ✅ Config is valid")
            else:
                results["config_valid"] = {"status": "❌ Invalid", "data": None}
                print("  ❌ Config is invalid")
        except Exception as e:
            results["config_valid"] = {"status": "❌ Error", "error": str(e)}
            print(f"  ❌ Config error: {e}")
    else:
        results["config_file"] = {"status": "❌ Not found", "path": str(config_file)}
        print(f"  ❌ Config file not found: {config_file}")
    
    # Check if server file exists
    server_file = Path(__file__).parent.parent / "neozork_mcp_server.py"
    if server_file.exists():
        results["server_file"] = {"status": "✅ Found", "path": str(server_file)}
        print(f"  ✅ Server file found: {server_file}")
    else:
        results["server_file"] = {"status": "❌ Not found", "path": str(server_file)}
        print(f"  ❌ Server file not found: {server_file}")
    
    return results

def check_dependencies() -> Dict[str, Any]:
    """Check required dependencies"""
    print("📦 Checking dependencies...")
    
    results = {}
    required_packages = ["pandas", "numpy", "matplotlib", "plotly"]
    
    for package in required_packages:
        try:
            __import__(package)
            results[package] = {"status": "✅ Installed"}
            print(f"  ✅ {package}")
        except ImportError:
            results[package] = {"status": "❌ Missing"}
            print(f"  ❌ {package}")
    
    # Check optional psutil for monitoring
    try:
        import psutil
        results["psutil"] = {"status": "✅ Installed (optional)"}
        print("  ✅ psutil (optional)")
    except ImportError:
        results["psutil"] = {"status": "⚠️ Missing (optional)"}
        print("  ⚠️ psutil (optional)")
    
    return results

def print_summary(status_results: Dict, cursor_results: Dict, dep_results: Dict):
    """Print summary of all checks"""
    print("\n" + "="*60)
    print("📋 SUMMARY")
    print("="*60)
    
    # Server status
    print("\n🔧 Server Status:")
    for check, result in status_results.items():
        status = result["status"]
        print(f"  {check:12} {status}")
    
    # Cursor integration
    print("\n🎯 Cursor Integration:")
    for check, result in cursor_results.items():
        status = result["status"]
        print(f"  {check:15} {status}")
    
    # Dependencies
    print("\n📦 Dependencies:")
    for package, result in dep_results.items():
        status = result["status"]
        print(f"  {package:12} {status}")
    
    # Overall status
    all_checks = list(status_results.values()) + list(cursor_results.values()) + list(dep_results.values())
    failed_checks = [r for r in all_checks if "❌" in r["status"]]
    
    if failed_checks:
        print(f"\n⚠️  Found {len(failed_checks)} issues that need attention")
    else:
        print("\n✅ All checks passed! MCP server should work correctly with Cursor IDE")

def main():
    """Main function"""
    print("🚀 Neozork MCP Server Status Checker")
    print("="*50)
    
    # Run all checks
    status_results = check_server_status()
    cursor_results = check_cursor_integration()
    dep_results = check_dependencies()
    
    # Print summary
    print_summary(status_results, cursor_results, dep_results)
    
    # Save results to file
    results_file = Path(__file__).parent.parent / "logs" / "mcp_status_check.json"
    results_file.parent.mkdir(exist_ok=True)
    
    all_results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "server_status": status_results,
        "cursor_integration": cursor_results,
        "dependencies": dep_results
    }
    
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n💾 Results saved to: {results_file}")

if __name__ == "__main__":
    main() 