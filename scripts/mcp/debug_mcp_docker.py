#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP Server Docker Debug Script
Diagnoses and fixes MCP server issues in Docker environment
"""

import json
import subprocess
import sys
import time
import os
import signal
from pathlib import Path
from typing import Dict, Any, Optional

def print_status(message: str, status: str = "INFO"):
    """Print status message with timestamp"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{status}] {message}")

def check_docker_environment() -> Dict[str, Any]:
    """Check Docker environment variables and configuration"""
    print_status("=== Docker Environment Check ===")
    
    env_vars = {
        "DOCKER_CONTAINER": os.environ.get("DOCKER_CONTAINER", "false"),
        "NATIVE_CONTAINER": os.environ.get("NATIVE_CONTAINER", "false"),
        "USE_UV": os.environ.get("USE_UV", "false"),
        "UV_ONLY": os.environ.get("UV_ONLY", "false"),
        "PYTHONPATH": os.environ.get("PYTHONPATH", ""),
        "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO"),
        "MCP_SERVER_TYPE": os.environ.get("MCP_SERVER_TYPE", "unknown")
    }
    
    print_status(f"Docker container: {env_vars['DOCKER_CONTAINER']}")
    print_status(f"Native container: {env_vars['NATIVE_CONTAINER']}")
    print_status(f"UV mode: {env_vars['USE_UV']}")
    print_status(f"UV only: {env_vars['UV_ONLY']}")
    print_status(f"Python path: {env_vars['PYTHONPATH']}")
    print_status(f"Log level: {env_vars['LOG_LEVEL']}")
    print_status(f"MCP server type: {env_vars['MCP_SERVER_TYPE']}")
    
    return env_vars

def check_mcp_server_file() -> Dict[str, Any]:
    """Check MCP server file existence and properties"""
    print_status("=== MCP Server File Check ===")
    
    mcp_file = Path("/app/neozork_mcp_server.py")
    result = {
        "exists": mcp_file.exists(),
        "size": mcp_file.stat().st_size if mcp_file.exists() else 0,
        "readable": mcp_file.is_file() and os.access(mcp_file, os.R_OK),
        "executable": mcp_file.is_file() and os.access(mcp_file, os.X_OK)
    }
    
    print_status(f"MCP server file exists: {result['exists']}")
    print_status(f"MCP server file size: {result['size']} bytes")
    print_status(f"MCP server file readable: {result['readable']}")
    print_status(f"MCP server file executable: {result['executable']}")
    
    return result

def check_mcp_server_process() -> Dict[str, Any]:
    """Check if MCP server process is running"""
    print_status("=== MCP Server Process Check ===")
    
    try:
        # Check for MCP server processes
        result = subprocess.run(
            ["pgrep", "-f", "neozork_mcp_server.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        pids = result.stdout.strip().split('\n') if result.stdout.strip() else []
        pids = [pid for pid in pids if pid]
        
        print_status(f"Found MCP server PIDs: {pids}")
        
        # Check process details
        process_info = []
        for pid in pids:
            try:
                proc_result = subprocess.run(
                    ["ps", "-p", pid, "-o", "pid,ppid,cmd"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                process_info.append({
                    "pid": pid,
                    "info": proc_result.stdout.strip()
                })
            except Exception as e:
                print_status(f"Error getting process info for PID {pid}: {e}", "ERROR")
        
        return {
            "running": len(pids) > 0,
            "pids": pids,
            "process_info": process_info
        }
        
    except Exception as e:
        print_status(f"Error checking MCP server process: {e}", "ERROR")
        return {"running": False, "pids": [], "process_info": []}

def test_mcp_server_communication() -> Dict[str, Any]:
    """Test MCP server communication"""
    print_status("=== MCP Server Communication Test ===")
    
    # Test direct communication with MCP server
    test_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "neozork/ping",
        "params": {}
    }
    
    try:
        # Try to send test message to MCP server
        print_status("Sending ping request to MCP server...")
        
        # Check if we can communicate via stdin/stdout
        result = subprocess.run(
            ["python3", "/app/neozork_mcp_server.py"],
            input=json.dumps(test_message) + "\n",
            capture_output=True,
            text=True,
            timeout=15
        )
        
        print_status(f"Exit code: {result.returncode}")
        print_status(f"Stdout: {result.stdout[:200]}...")
        print_status(f"Stderr: {result.stderr[:200]}...")
        
        return {
            "success": result.returncode == 0,
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
        
    except subprocess.TimeoutExpired:
        print_status("MCP server communication timed out", "WARNING")
        return {"success": False, "timeout": True}
    except Exception as e:
        print_status(f"Error testing MCP server communication: {e}", "ERROR")
        return {"success": False, "error": str(e)}

def check_mcp_logs() -> Dict[str, Any]:
    """Check MCP server logs"""
    print_status("=== MCP Server Logs Check ===")
    
    log_files = [
        "/app/logs/mcp_server.log",
        "/app/logs/neozork_mcp.log",
        "/tmp/mcp_server.log"
    ]
    
    log_info = {}
    for log_file in log_files:
        log_path = Path(log_file)
        if log_path.exists():
            try:
                size = log_path.stat().st_size
                modified = time.ctime(log_path.stat().st_mtime)
                
                # Read last 10 lines
                with open(log_path, 'r') as f:
                    lines = f.readlines()
                    last_lines = lines[-10:] if len(lines) > 10 else lines
                
                log_info[log_file] = {
                    "exists": True,
                    "size": size,
                    "modified": modified,
                    "last_lines": [line.strip() for line in last_lines]
                }
                
                print_status(f"Log file {log_file}: {size} bytes, modified {modified}")
                
            except Exception as e:
                print_status(f"Error reading log file {log_file}: {e}", "ERROR")
                log_info[log_file] = {"exists": True, "error": str(e)}
        else:
            print_status(f"Log file {log_file}: not found")
            log_info[log_file] = {"exists": False}
    
    return log_info

def create_mcp_test_script() -> str:
    """Create a test script for MCP server"""
    print_status("=== Creating MCP Test Script ===")
    
    test_script = """#!/usr/bin/env python3
import json
import sys
import time

def test_mcp_server():
    # Test message
    test_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "neozork/ping",
        "params": {}
    }
    
    print("Sending test message to MCP server...")
    print(json.dumps(test_message))
    
    # Wait for response
    time.sleep(2)
    
    # Try to read response
    try:
        response = input()
        print(f"Received response: {response}")
        return True
    except EOFError:
        print("No response received (EOF)")
        return False

if __name__ == "__main__":
    success = test_mcp_server()
    sys.exit(0 if success else 1)
"""
    
    test_file = "/tmp/test_mcp_communication.py"
    with open(test_file, 'w') as f:
        f.write(test_script)
    
    os.chmod(test_file, 0o755)
    print_status(f"Created test script: {test_file}")
    
    return test_file

def run_comprehensive_diagnosis() -> Dict[str, Any]:
    """Run comprehensive MCP server diagnosis"""
    print_status("🔍 Starting MCP Server Docker Diagnosis", "INFO")
    print_status("=" * 50)
    
    results = {
        "docker_environment": check_docker_environment(),
        "mcp_file": check_mcp_server_file(),
        "mcp_process": check_mcp_server_process(),
        "mcp_communication": test_mcp_server_communication(),
        "mcp_logs": check_mcp_logs()
    }
    
    # Create test script
    test_script = create_mcp_test_script()
    results["test_script"] = test_script
    
    # Summary
    print_status("=" * 50)
    print_status("=== DIAGNOSIS SUMMARY ===")
    
    issues = []
    recommendations = []
    
    # Check Docker environment
    if results["docker_environment"]["DOCKER_CONTAINER"] != "true":
        issues.append("Not running in Docker container")
        recommendations.append("Ensure DOCKER_CONTAINER=true")
    
    # Check MCP file
    if not results["mcp_file"]["exists"]:
        issues.append("MCP server file not found")
        recommendations.append("Check if neozork_mcp_server.py exists in /app/")
    
    # Check MCP process
    if not results["mcp_process"]["running"]:
        issues.append("MCP server process not running")
        recommendations.append("Start MCP server with: python3 neozork_mcp_server.py")
    
    # Check communication
    if not results["mcp_communication"]["success"]:
        issues.append("MCP server communication failed")
        recommendations.append("Check MCP server logs and configuration")
    
    # Print issues and recommendations
    if issues:
        print_status("❌ ISSUES FOUND:", "ERROR")
        for issue in issues:
            print_status(f"  - {issue}", "ERROR")
    else:
        print_status("✅ No major issues found", "SUCCESS")
    
    if recommendations:
        print_status("💡 RECOMMENDATIONS:", "INFO")
        for rec in recommendations:
            print_status(f"  - {rec}", "INFO")
    
    # Save results
    results_file = "/app/logs/mcp_docker_diagnosis.json"
    try:
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print_status(f"Results saved to: {results_file}")
    except Exception as e:
        print_status(f"Error saving results: {e}", "ERROR")
    
    return results

def main():
    """Main entry point"""
    try:
        results = run_comprehensive_diagnosis()
        
        # Exit with appropriate code
        if any(not results["mcp_file"]["exists"], 
               not results["mcp_process"]["running"],
               not results["mcp_communication"]["success"]):
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print_status("Diagnosis interrupted by user", "WARNING")
        sys.exit(130)
    except Exception as e:
        print_status(f"Diagnosis failed: {e}", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main() 