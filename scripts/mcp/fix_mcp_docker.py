#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP Server Docker Fix Script
Fixes MCP server issues in Docker environment
"""

import json
import subprocess
import sys
import time
import os
import signal
import socket
import threading
from pathlib import Path
from typing import Dict, Any, Optional

def print_status(message: str, status: str = "INFO"):
    """Print status message with timestamp"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{status}] {message}")

def stop_existing_mcp_servers():
    """Stop any existing MCP server processes"""
    print_status("=== Stopping Existing MCP Servers ===")
    
    try:
        # Find MCP server processes
        result = subprocess.run(
            ["pgrep", "-f", "neozork_mcp_server.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            print_status(f"Found existing MCP server PIDs: {pids}")
            
            for pid in pids:
                if pid:
                    try:
                        print_status(f"Stopping MCP server PID {pid}...")
                        os.kill(int(pid), signal.SIGTERM)
                        time.sleep(1)
                        
                        # Check if process is still running
                        try:
                            os.kill(int(pid), 0)
                            print_status(f"Force killing PID {pid}...")
                            os.kill(int(pid), signal.SIGKILL)
                        except OSError:
                            print_status(f"PID {pid} stopped successfully")
                            
                    except Exception as e:
                        print_status(f"Error stopping PID {pid}: {e}", "ERROR")
        else:
            print_status("No existing MCP server processes found")
            
    except Exception as e:
        print_status(f"Error checking for existing MCP servers: {e}", "ERROR")

def create_mcp_socket_server():
    """Create a socket-based MCP server for Docker"""
    print_status("=== Creating Socket-based MCP Server ===")
    
    socket_server_script = """#!/usr/bin/env python3
import json
import socket
import threading
import sys
import time
import signal
from pathlib import Path

class MCPSocketServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.running = True
        self.clients = []
        
        # Import the main MCP server
        sys.path.insert(0, '/app')
        from neozork_mcp_server import NeozorkMCPServer
        
        self.mcp_server = NeozorkMCPServer()
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, sig, frame):
        print("Received signal, shutting down...")
        self.running = False
    
    def start(self):
        try:
            # Create socket server
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            print(f"MCP Socket Server listening on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, address = self.server_socket.accept()
                    print(f"New connection from {address}")
                    
                    # Handle client in separate thread
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, address)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error accepting connection: {e}")
                    break
                    
        except Exception as e:
            print(f"Error starting socket server: {e}")
        finally:
            self.server_socket.close()
    
    def _handle_client(self, client_socket, address):
        try:
            while self.running:
                # Receive data
                data = client_socket.recv(4096)
                if not data:
                    break
                
                try:
                    message = json.loads(data.decode('utf-8'))
                    print(f"Received message: {message}")
                    
                    # Process message using MCP server
                    method = message.get("method")
                    request_id = message.get("id")
                    params = message.get("params", {})
                    
                    if hasattr(self.mcp_server, 'handlers') and method in self.mcp_server.handlers:
                        result = self.mcp_server.handlers[method](request_id, params)
                        response = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "result": result
                        }
                    else:
                        response = {
                            "jsonrpc": "2.0",
                            "id": request_id,
                            "error": {
                                "code": -32601,
                                "message": f"Method not found: {method}"
                            }
                        }
                    
                    # Send response
                    client_socket.send(json.dumps(response).encode('utf-8'))
                    
                except json.JSONDecodeError as e:
                    error_response = {
                        "jsonrpc": "2.0",
                        "id": None,
                        "error": {
                            "code": -32700,
                            "message": f"Parse error: {e}"
                        }
                    }
                    client_socket.send(json.dumps(error_response).encode('utf-8'))
                    
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            print(f"Connection from {address} closed")

if __name__ == "__main__":
    server = MCPSocketServer()
    server.start()
"""
    
    socket_file = "/tmp/mcp_socket_server.py"
    with open(socket_file, 'w') as f:
        f.write(socket_server_script)
    
    os.chmod(socket_file, 0o755)
    print_status(f"Created socket server script: {socket_file}")
    
    return socket_file

def create_mcp_client():
    """Create a client for testing MCP socket server"""
    print_status("=== Creating MCP Client ===")
    
    client_script = """#!/usr/bin/env python3
import json
import socket
import time

def test_mcp_socket_server():
    try:
        # Connect to MCP socket server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(('localhost', 8080))
        
        # Send ping request
        test_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "neozork/ping",
            "params": {}
        }
        
        print("Sending ping request to MCP socket server...")
        sock.send(json.dumps(test_message).encode('utf-8'))
        
        # Receive response
        response = sock.recv(4096)
        print(f"Received response: {response.decode('utf-8')}")
        
        sock.close()
        return True
        
    except Exception as e:
        print(f"Error testing MCP socket server: {e}")
        return False

if __name__ == "__main__":
    success = test_mcp_socket_server()
    exit(0 if success else 1)
"""
    
    client_file = "/tmp/mcp_client.py"
    with open(client_file, 'w') as f:
        f.write(client_script)
    
    os.chmod(client_file, 0o755)
    print_status(f"Created client script: {client_file}")
    
    return client_file

def start_mcp_socket_server():
    """Start the MCP socket server"""
    print_status("=== Starting MCP Socket Server ===")
    
    socket_file = create_mcp_socket_server()
    
    try:
        # Start socket server in background
        process = subprocess.Popen(
            ["python3", socket_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print_status(f"MCP socket server started with PID: {process.pid}")
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Test the server
        client_file = create_mcp_client()
        
        print_status("Testing MCP socket server...")
        result = subprocess.run(
            ["python3", client_file],
            capture_output=True,
            text=True,
            timeout=15
        )
        
        print_status(f"Client test exit code: {result.returncode}")
        print_status(f"Client stdout: {result.stdout}")
        print_status(f"Client stderr: {result.stderr}")
        
        if result.returncode == 0:
            print_status("✅ MCP socket server is working correctly", "SUCCESS")
            return True
        else:
            print_status("❌ MCP socket server test failed", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Error starting MCP socket server: {e}", "ERROR")
        return False

def create_mcp_docker_config():
    """Create Docker-specific MCP configuration"""
    print_status("=== Creating Docker MCP Configuration ===")
    
    docker_config = {
        "mcpServers": {
            "neozork-docker-socket": {
                "command": "python3",
                "args": ["/tmp/mcp_socket_server.py"],
                "env": {
                    "PYTHONPATH": "/app",
                    "LOG_LEVEL": "INFO",
                    "DOCKER_CONTAINER": "true",
                    "USE_UV": "true",
                    "UV_ONLY": "true"
                },
                "cwd": "/app"
            }
        },
        "serverSettings": {
            "neozork-docker-socket": {
                "enabled": True,
                "autoStart": True,
                "debug": False,
                "logLevel": "info",
                "features": {
                    "financial_data": True,
                    "technical_indicators": True,
                    "github_copilot": True,
                    "code_completion": True,
                    "project_analysis": True,
                    "ai_suggestions": True,
                    "docker_integration": True,
                    "socket_communication": True
                },
                "performance": {
                    "max_files": 15000,
                    "max_file_size": "10MB",
                    "cache_enabled": True,
                    "cache_size": "200MB",
                    "indexing_timeout": 60,
                    "completion_timeout": 5,
                    "memory_limit_mb": 512
                },
                "monitoring": {
                    "enable_monitoring": True,
                    "health_check_interval": 60,
                    "max_memory_mb": 512,
                    "max_cpu_percent": 80
                },
                "docker": {
                    "enabled": True,
                    "container_name": "neozork-mcp-socket-server",
                    "port": 8080,
                    "socket_enabled": True
                }
            }
        }
    }
    
    config_file = "/app/docker_mcp_config.json"
    with open(config_file, 'w') as f:
        json.dump(docker_config, f, indent=2)
    
    print_status(f"Created Docker MCP config: {config_file}")
    return config_file

def update_entrypoint_script():
    """Update the entrypoint script to use socket server"""
    print_status("=== Updating Entrypoint Script ===")
    
    # Create a new entrypoint section for MCP socket server
    mcp_socket_section = """
# Start MCP socket server
start_mcp_socket_server() {
    echo -e "\\033[1;32m=== Starting MCP Socket Server ===\\033[0m"
    
    # Create socket server script
    python3 /app/scripts/mcp/fix_mcp_docker.py --create-socket-server
    
    # Start socket server
    python3 /tmp/mcp_socket_server.py > /app/logs/mcp_socket_server.log 2>&1 &
    MCP_SOCKET_PID=$!
    echo $MCP_SOCKET_PID > /tmp/mcp_socket_server.pid
    
    echo -e "\\033[1;32mMCP socket server started with PID: $MCP_SOCKET_PID\\033[0m"
    
    # Wait for server to start
    sleep 3
    
    # Test socket server
    if python3 /tmp/mcp_client.py; then
        echo -e "\\033[1;32m✅ MCP socket server is working\\033[0m"
    else
        echo -e "\\033[1;31m❌ MCP socket server test failed\\033[0m"
    fi
}
"""
    
    # Add to entrypoint script
    entrypoint_file = "/app/container-entrypoint.sh"
    if Path(entrypoint_file).exists():
        with open(entrypoint_file, 'r') as f:
            content = f.read()
        
        # Add the new function before the main execution
        if "start_mcp_socket_server()" not in content:
            # Find a good place to insert the function
            lines = content.split('\n')
            insert_index = -1
            for i, line in enumerate(lines):
                if "start_mcp_server()" in line:
                    insert_index = i - 1
                    break
            
            if insert_index >= 0:
                lines.insert(insert_index, mcp_socket_section)
                content = '\n'.join(lines)
                
                with open(entrypoint_file, 'w') as f:
                    f.write(content)
                
                print_status("Updated entrypoint script with socket server function")
            else:
                print_status("Could not find insertion point in entrypoint script", "WARNING")
        else:
            print_status("Socket server function already exists in entrypoint script")
    else:
        print_status("Entrypoint script not found", "WARNING")

def run_fixes():
    """Run all MCP server fixes"""
    print_status("🔧 Starting MCP Server Docker Fixes", "INFO")
    print_status("=" * 50)
    
    # Step 1: Stop existing servers
    stop_existing_mcp_servers()
    
    # Step 2: Create socket server
    socket_server_created = start_mcp_socket_server()
    
    # Step 3: Create Docker config
    config_created = create_mcp_docker_config()
    
    # Step 4: Update entrypoint script
    update_entrypoint_script()
    
    # Summary
    print_status("=" * 50)
    print_status("=== FIX SUMMARY ===")
    
    if socket_server_created:
        print_status("✅ Socket server created and tested successfully", "SUCCESS")
    else:
        print_status("❌ Socket server creation failed", "ERROR")
    
    if config_created:
        print_status("✅ Docker MCP config created", "SUCCESS")
    else:
        print_status("❌ Docker MCP config creation failed", "ERROR")
    
    print_status("💡 To use the fixed MCP server:")
    print_status("  1. Restart the Docker container")
    print_status("  2. The socket server will start automatically")
    print_status("  3. Use the new 'neozork-docker-socket' configuration")
    
    return socket_server_created and config_created

def main():
    """Main entry point"""
    try:
        success = run_fixes()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print_status("Fixes interrupted by user", "WARNING")
        sys.exit(130)
    except Exception as e:
        print_status(f"Fixes failed: {e}", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main() 