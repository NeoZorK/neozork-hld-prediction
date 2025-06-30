#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Extended debug script for MCP server detection analysis
"""

import subprocess
from pathlib import Path
import time

def check_specific_pid(pid):
    """Check specific PID for MCP server"""
    print(f"\n=== Checking PID {pid} specifically ===")
    
    proc_dir = Path("/proc") / str(pid)
    if not proc_dir.exists():
        print(f"❌ Process {pid} does not exist")
        return False
    
    try:
        # Check cmdline
        cmdline_file = proc_dir / "cmdline"
        if cmdline_file.exists():
            with open(cmdline_file, 'rb') as f:
                cmdline = f.read().replace(b'\x00', b' ')
                cmdline_str = cmdline.decode('utf-8', errors='ignore')
                print(f"📝 Cmdline: {cmdline_str}")
                
                # Check for various patterns
                patterns = [
                    b'neozork_mcp_server.py',
                    b'neozork_mcp_server',
                    b'mcp_server',
                    b'neozork'
                ]
                
                for pattern in patterns:
                    if pattern in cmdline:
                        print(f"✅ Found pattern: {pattern}")
                        return True
                
                print("❌ No MCP patterns found in cmdline")
        else:
            print("❌ Cmdline file does not exist")
            
        # Check comm (process name)
        comm_file = proc_dir / "comm"
        if comm_file.exists():
            with open(comm_file, 'r') as f:
                comm = f.read().strip()
                print(f"📝 Comm: {comm}")
        
        # Check exe (executable path)
        exe_file = proc_dir / "exe"
        if exe_file.exists():
            try:
                exe_target = exe_file.resolve()
                print(f"📝 Exe: {exe_target}")
            except Exception as e:
                print(f"📝 Exe: {exe_file} (resolve failed: {e})")
        
        return False
        
    except Exception as e:
        print(f"❌ Error checking PID {pid}: {e}")
        return False

def check_all_python_processes():
    """Check all Python processes in detail"""
    print("\n=== Checking all Python processes in detail ===")
    
    proc_dir = Path("/proc")
    python_processes = []
    
    for proc in proc_dir.iterdir():
        if not proc.is_dir() or not proc.name.isdigit():
            continue
        
        try:
            cmdline_file = proc / "cmdline"
            if cmdline_file.exists():
                with open(cmdline_file, 'rb') as f:
                    cmdline = f.read().replace(b'\x00', b' ')
                    cmdline_str = cmdline.decode('utf-8', errors='ignore')
                    if 'python' in cmdline_str.lower():
                        python_processes.append((int(proc.name), cmdline_str.strip()))
        except Exception:
            continue
    
    print(f"Found {len(python_processes)} Python processes:")
    for pid, cmdline in python_processes:
        print(f"  PID {pid}: {cmdline}")
        
        # Check if this looks like MCP server
        if any(keyword in cmdline.lower() for keyword in ['neozork', 'mcp', 'server']):
            print(f"    ⭐ This looks like MCP server!")
            check_specific_pid(pid)

def test_pidof():
    """Test pidof command"""
    print("\n=== Testing pidof command ===")
    
    try:
        result = subprocess.run(['pidof', 'python3'], capture_output=True, text=True, timeout=2)
        print(f"pidof python3 exit code: {result.returncode}")
        print(f"pidof python3 output: {result.stdout.strip()}")
        print(f"pidof python3 error: {result.stderr.strip()}")
        
        if result.returncode == 0:
            pids = result.stdout.strip().split()
            print(f"Found PIDs: {pids}")
            
            for pid in pids:
                if pid.isdigit():
                    print(f"\n--- Checking PID {pid} from pidof ---")
                    check_specific_pid(int(pid))
                    
    except Exception as e:
        print(f"❌ pidof test failed: {e}")

def test_our_detection_method():
    """Test our detection method step by step"""
    print("\n=== Testing our detection method step by step ===")
    
    from check_mcp_status import DockerMCPServerChecker
    
    checker = DockerMCPServerChecker()
    
    print("1. Testing _find_mcp_server_pid()...")
    pid = checker._find_mcp_server_pid()
    print(f"   Result: {pid}")
    
    if pid:
        print("2. Testing _is_process_running()...")
        running = checker._is_process_running(pid)
        print(f"   Result: {running}")
        
        print("3. Testing _check_server_with_ps()...")
        found = checker._check_server_with_ps()
        print(f"   Result: {found}")

def main():
    """Main debug function"""
    print("🔍 Extended MCP Server Detection Debug")
    print("=" * 50)
    
    # Check if PID file exists
    pid_file = Path("/tmp/mcp_server.pid")
    if pid_file.exists():
        with open(pid_file, 'r') as f:
            saved_pid = f.read().strip()
            print(f"📄 PID file exists with PID: {saved_pid}")
            
            if saved_pid.isdigit():
                print(f"\n--- Checking saved PID {saved_pid} ---")
                check_specific_pid(int(saved_pid))
    else:
        print("📄 No PID file found")
    
    # Check all Python processes
    check_all_python_processes()
    
    # Test pidof
    test_pidof()
    
    # Test our detection method
    test_our_detection_method()

if __name__ == "__main__":
    main() 