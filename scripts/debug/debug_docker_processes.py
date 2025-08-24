#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Debug script to check processes in Docker container
"""

import subprocess
from pathlib import Path

def check_proc_filesystem():
    """Check what processes are visible in /proc"""
    print("=== Checking /proc filesystem ===")
    proc_dir = Path("/proc")
    if not proc_dir.exists():
        print("❌ /proc directory does not exist")
        return
    
    print(f"✅ /proc directory exists")
    
    # List all process directories
    processes = []
    for proc in proc_dir.iterdir():
        if proc.is_dir() and proc.name.isdigit():
            processes.append(int(proc.name))
    
    print(f"Found {len(processes)} processes: {sorted(processes)}")
    
    # Check first few processes
    for pid in sorted(processes)[:5]:
        try:
            cmdline_file = proc_dir / str(pid) / "cmdline"
            if cmdline_file.exists():
                with open(cmdline_file, 'rb') as f:
                    cmdline = f.read().replace(b'\x00', b' ').decode('utf-8', errors='ignore')
                    print(f"PID {pid}: {cmdline.strip()}")
        except Exception as e:
            print(f"PID {pid}: Error reading cmdline - {e}")

def check_available_commands():
    """Check what commands are available"""
    print("\n=== Checking available commands ===")
    
    commands = ['ps', 'pgrep', 'top', 'htop', 'pidof']
    for cmd in commands:
        try:
            result = subprocess.run([cmd, '--version'], capture_output=True, text=True, timeout=2)
            print(f"✅ {cmd}: available")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            try:
                result = subprocess.run([cmd, '-h'], capture_output=True, text=True, timeout=2)
                print(f"✅ {cmd}: available (no --version)")
            except (FileNotFoundError, subprocess.TimeoutExpired):
                print(f"❌ {cmd}: not available")

def check_python_processes():
    """Check for Python processes specifically"""
    print("\n=== Checking for Python processes ===")
    
    proc_dir = Path("/proc")
    python_processes = []
    
    for proc in proc_dir.iterdir():
        if not proc.is_dir() or not proc.name.isdigit():
            continue
        
        try:
            cmdline_file = proc / "cmdline"
            if cmdline_file.exists():
                with open(cmdline_file, 'rb') as f:
                    cmdline = f.read().replace(b'\x00', b' ').decode('utf-8', errors='ignore')
                    if 'python' in cmdline.lower():
                        python_processes.append((int(proc.name), cmdline.strip()))
        except Exception:
            continue
    
    if python_processes:
        print(f"Found {len(python_processes)} Python processes:")
        for pid, cmdline in python_processes:
            print(f"  PID {pid}: {cmdline}")
    else:
        print("No Python processes found")

def check_mcp_server_specific():
    """Check specifically for MCP server"""
    print("\n=== Checking for MCP server specifically ===")
    
    proc_dir = Path("/proc")
    mcp_processes = []
    
    for proc in proc_dir.iterdir():
        if not proc.is_dir() or not proc.name.isdigit():
            continue
        
        try:
            cmdline_file = proc / "cmdline"
            if cmdline_file.exists():
                with open(cmdline_file, 'rb') as f:
                    cmdline = f.read().replace(b'\x00', b' ').decode('utf-8', errors='ignore')
                    if any(keyword in cmdline.lower() for keyword in ['mcp', 'neozork', 'server']):
                        mcp_processes.append((int(proc.name), cmdline.strip()))
        except Exception:
            continue
    
    if mcp_processes:
        print(f"Found {len(mcp_processes)} potential MCP-related processes:")
        for pid, cmdline in mcp_processes:
            print(f"  PID {pid}: {cmdline}")
    else:
        print("No MCP-related processes found")

if __name__ == "__main__":
    check_proc_filesystem()
    check_available_commands()
    check_python_processes()
    check_mcp_server_specific() 