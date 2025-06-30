#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Daemon script to start MCP server in background mode
"""

import os
import sys
import time
import signal
import subprocess
from pathlib import Path

def start_mcp_daemon():
    """Start MCP server as daemon"""
    print("🚀 Starting MCP server as daemon...")
    
    # Create a simple daemon script that keeps the server running
    daemon_script = """
#!/usr/bin/env python3
import sys
import time
import signal
import subprocess
import os

def signal_handler(sig, frame):
    print("Received signal, shutting down...")
    sys.exit(0)

signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

# Start MCP server in a loop
while True:
    try:
        print("Starting MCP server process...")
        process = subprocess.Popen([
            sys.executable, 
            "neozork_mcp_server.py",
            "--debug"
        ], 
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        universal_newlines=True
        )
        
        # Save PID
        with open("/tmp/mcp_server.pid", "w") as f:
            f.write(str(process.pid))
        
        print(f"MCP server started with PID: {process.pid}")
        
        # Keep the process running
        process.wait()
        
        print("MCP server process ended, restarting in 5 seconds...")
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("Received interrupt, shutting down...")
        break
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)

# Cleanup
try:
    os.remove("/tmp/mcp_server.pid")
except:
    pass
"""
    
    # Write daemon script to file
    daemon_file = Path("mcp_daemon.py")
    with open(daemon_file, "w") as f:
        f.write(daemon_script)
    
    # Make it executable
    os.chmod(daemon_file, 0o755)
    
    # Start daemon in background
    try:
        process = subprocess.Popen([
            "nohup",
            sys.executable,
            "mcp_daemon.py"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
        )
        
        print(f"✅ Daemon started with PID: {process.pid}")
        
        # Wait a moment for daemon to start MCP server
        time.sleep(3)
        
        # Check if MCP server PID file was created
        pid_file = Path("/tmp/mcp_server.pid")
        if pid_file.exists():
            with open(pid_file, "r") as f:
                mcp_pid = f.read().strip()
                print(f"✅ MCP server PID: {mcp_pid}")
                return True
        else:
            print("❌ MCP server PID file not created")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start daemon: {e}")
        return False

def stop_mcp_daemon():
    """Stop MCP server daemon"""
    print("🛑 Stopping MCP server daemon...")
    
    # Read MCP server PID
    pid_file = Path("/tmp/mcp_server.pid")
    if pid_file.exists():
        with open(pid_file, "r") as f:
            mcp_pid = f.read().strip()
            if mcp_pid.isdigit():
                try:
                    # Kill MCP server process
                    os.kill(int(mcp_pid), signal.SIGTERM)
                    print(f"✅ Sent SIGTERM to MCP server (PID: {mcp_pid})")
                    
                    # Wait a moment
                    time.sleep(2)
                    
                    # Force kill if still running
                    try:
                        os.kill(int(mcp_pid), signal.SIGKILL)
                        print(f"⚠️ Force killed MCP server (PID: {mcp_pid})")
                    except ProcessLookupError:
                        pass
                        
                except ProcessLookupError:
                    print(f"⚠️ MCP server process {mcp_pid} not found")
                except Exception as e:
                    print(f"❌ Error stopping MCP server: {e}")
    
    # Kill daemon process
    try:
        # Find daemon process
        result = subprocess.run(['pgrep', '-f', 'mcp_daemon.py'], capture_output=True, text=True)
        if result.returncode == 0:
            daemon_pids = result.stdout.strip().split('\n')
            for pid in daemon_pids:
                if pid.strip().isdigit():
                    os.kill(int(pid), signal.SIGTERM)
                    print(f"✅ Sent SIGTERM to daemon (PID: {pid})")
    except Exception as e:
        print(f"⚠️ Could not find daemon process: {e}")
    
    # Clean up files
    try:
        os.remove("/tmp/mcp_server.pid")
    except FileNotFoundError:
        pass
    
    try:
        os.remove("mcp_daemon.py")
    except FileNotFoundError:
        pass
    
    print("✅ Cleanup complete")

def test_mcp_server():
    """Test if MCP server is responding"""
    print("🔍 Testing MCP server response...")
    
    try:
        result = subprocess.run([
            "bash", "-c", 
            'echo \'{"method": "neozork/ping", "id": 1, "params": {}}\' | python3 neozork_mcp_server.py'
        ], 
        capture_output=True, 
        text=True, 
        timeout=10
        )
        
        if result.returncode == 0 and '"pong": true' in result.stdout:
            print("✅ MCP server is responding correctly")
            return True
        else:
            print("❌ MCP server not responding correctly")
            print(f"Stdout: {result.stdout}")
            print(f"Stderr: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ MCP server test timed out")
        return False
    except Exception as e:
        print(f"❌ MCP server test failed: {e}")
        return False

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Server Daemon Manager")
    parser.add_argument("action", choices=["start", "stop", "test"], help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == "start":
        if start_mcp_daemon():
            print("✅ MCP server daemon started successfully")
            # Test the server
            time.sleep(2)
            test_mcp_server()
        else:
            print("❌ Failed to start MCP server daemon")
            sys.exit(1)
    
    elif args.action == "stop":
        stop_mcp_daemon()
        print("✅ MCP server daemon stopped")
    
    elif args.action == "test":
        test_mcp_server()

if __name__ == "__main__":
    main() 