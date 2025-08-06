#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP Server Status Checker
Check if MCP server is running and test connection
Supports both Docker and non-Docker environments
"""

import json
import subprocess
import sys
import time
import signal
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

def is_running_in_docker() -> bool:
    """Check if the script is running inside a Docker container"""
    try:
        # Check for Docker-specific files
        if Path("/.dockerenv").exists():
            return True
        
        # Check cgroup for Docker
        try:
            with open("/proc/1/cgroup", "r") as f:
                if "docker" in f.read():
                    return True
        except FileNotFoundError:
            pass
        
        # Check environment variable
        if os.environ.get("DOCKER_CONTAINER") == "true":
            return True
        
        return False
    except Exception:
        return False

class DockerMCPServerChecker:
    """Check MCP server status inside Docker container"""
    
    def __init__(self, project_root: Path = None):
        if project_root:
            self.project_root = project_root
        elif is_running_in_docker():
            # In Docker, project root is /app
            self.project_root = Path("/app")
        else:
            # Outside Docker, use relative path
            self.project_root = Path(__file__).parent.parent.parent
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'mcp_status_check_docker.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def check_server_running(self) -> bool:
        """Check if MCP server is running inside Docker container"""
        try:
            # First wait for MCP server initialization to complete
            if not self._wait_for_mcp_initialization():
                self.logger.warning("MCP server initialization did not complete in time")
                return False
            
            # Docker-specific method: send ping request to MCP server
            # MCP server runs on-demand and shuts down after requests
            return self._test_mcp_ping_request()
                
        except Exception as e:
            self.logger.error(f"Error checking server status in Docker: {e}")
            return False

    def _wait_for_mcp_initialization(self, max_wait_time: int = 60) -> bool:
        """Wait for MCP server to complete initialization"""
        self.logger.info(f"Waiting for MCP server initialization (max {max_wait_time}s)...")
        
        start_time = time.time()
        check_interval = 2  # Check every 2 seconds
        
        while time.time() - start_time < max_wait_time:
            try:
                # Check if MCP server is responding to ping
                if self._test_mcp_ping_request():
                    self.logger.info("MCP server initialization completed successfully")
                    return True
                    
                # Check log file for initialization completion message
                log_file = self.project_root / "logs" / "mcp_server.log"
                if log_file.exists():
                    try:
                        with open(log_file, 'r') as f:
                            log_content = f.read()
                            if "✅ Neozork Unified MCP Server initialized successfully" in log_content:
                                self.logger.info("Found initialization completion message in logs")
                                return True
                    except Exception as e:
                        self.logger.debug(f"Error reading log file: {e}")
                
                time.sleep(check_interval)
                
            except Exception as e:
                self.logger.debug(f"Error during initialization check: {e}")
                time.sleep(check_interval)
        
        self.logger.warning(f"MCP server initialization timeout after {max_wait_time}s")
        return False

    def _test_mcp_ping_request(self) -> bool:
        """Test MCP server by sending ping request via echo command"""
        try:
            self.logger.info("Testing MCP server with ping request...")
            
            # Create ping request JSON
            ping_request = '{"method": "neozork/ping", "id": 1, "params": {}}'
            
            # Send request to MCP server via echo command
            cmd = f'echo \'{ping_request}\' | python3 neozork_mcp_server.py'
            
            # Run command with timeout
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,  # Reduced timeout for faster response
                cwd=self.project_root
            )
            
            # Check if we got a valid JSON response
            if result.returncode == 0 and result.stdout.strip():
                try:
                    response = json.loads(result.stdout.strip())
                    # Check if response contains expected ping response structure
                    if (response.get("jsonrpc") == "2.0" and 
                        response.get("id") == 1 and 
                        response.get("result", {}).get("pong") is True):
                        self.logger.info("MCP server responded to ping request successfully")
                        return True
                    else:
                        self.logger.warning(f"Unexpected ping response format: {response}")
                        return False
                except json.JSONDecodeError as e:
                    self.logger.warning(f"Invalid JSON response from MCP server: {e}")
                    self.logger.debug(f"Raw response: {result.stdout}")
                    return False
            else:
                self.logger.info("MCP server did not respond to ping request")
                if result.stderr:
                    self.logger.debug(f"Stderr: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.warning("MCP server ping request timed out")
            return False
        except Exception as e:
            self.logger.error(f"Error testing MCP ping request: {e}")
            return False

    def test_connection(self) -> Dict[str, Any]:
        """Test MCP server connection inside Docker"""
        try:
            self.logger.info("Testing MCP server connection in Docker...")
            
            # First wait for initialization to complete
            if not self._wait_for_mcp_initialization():
                return {
                    "status": "failed", 
                    "error": "MCP server initialization did not complete in time"
                }
            
            # Test MCP server by sending ping request
            server_responding = self._test_mcp_ping_request()
            
            if server_responding:
                return {
                    "status": "success",
                    "message": "MCP server is responding to ping requests",
                    "test_method": "ping_request",
                    "response_time": "immediate"
                }
            else:
                return {"status": "failed", "error": "Server not responding to ping requests"}
            
        except Exception as e:
            self.logger.error(f"Error testing connection in Docker: {e}")
            return {"status": "failed", "error": str(e)}

    def check_ide_configurations(self) -> Dict[str, Any]:
        """Check IDE configuration files in Docker"""
        configs = {}
        
        # In Docker, we only check for Cursor config as it's the most relevant
        cursor_config = self.project_root / "cursor_mcp_config.json"
        if cursor_config.exists():
            try:
                with open(cursor_config, 'r') as f:
                    configs['cursor'] = {
                        'exists': True,
                        'size': cursor_config.stat().st_size,
                        'valid_json': True
                    }
            except Exception as e:
                configs['cursor'] = {
                    'exists': True,
                    'error': str(e),
                    'valid_json': False
                }
        else:
            configs['cursor'] = {'exists': False}
        
        # Docker-specific configurations
        docker_config = self.project_root / "docker.env"
        if docker_config.exists():
            try:
                # Try to read as JSON first (some docker.env files might be JSON)
                with open(docker_config, 'r') as f:
                    content = f.read().strip()
                    # Try to parse as JSON
                    try:
                        json.loads(content)
                        valid_json = True
                    except json.JSONDecodeError:
                        # If not JSON, check if it's valid environment file format
                        valid_json = all('=' in line or line.startswith('#') or not line.strip() 
                                       for line in content.split('\n'))
                    
                    configs['docker'] = {
                        'exists': True,
                        'size': docker_config.stat().st_size,
                        'valid_json': valid_json
                    }
            except Exception as e:
                configs['docker'] = {
                    'exists': True,
                    'error': str(e),
                    'valid_json': False
                }
        else:
            configs['docker'] = {'exists': False}
        
        return configs

    def run_comprehensive_check(self) -> Dict[str, Any]:
        """Run comprehensive MCP server check in Docker"""
        self.logger.info("Starting comprehensive MCP server check in Docker...")
        
        results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "environment": "docker",
            "project_root": str(self.project_root),
            "server_running": False,
            "connection_test": {},
            "ide_configurations": {},
            "docker_specific": {},
            "recommendations": []
        }
        
        # Check if server is running
        results["server_running"] = self.check_server_running()
        
        # Check IDE configurations
        results["ide_configurations"] = self.check_ide_configurations()
        
        # Docker-specific checks
        results["docker_specific"] = self._check_docker_specific()
        
        # Test connection if server is running
        if results["server_running"]:
            results["connection_test"] = self.test_connection()
        else:
            results["connection_test"] = {"status": "skipped", "reason": "Server not running"}
            results["recommendations"].append("Start MCP server in Docker container")
        
        # Generate Docker-specific recommendations
        if not results["server_running"]:
            results["recommendations"].append("Restart Docker container with MCP server enabled")
            results["recommendations"].append("Check Docker logs: docker logs <container_name>")
        
        if results["connection_test"].get("status") == "failed":
            results["recommendations"].append("Check MCP server logs: tail -f logs/mcp_server.log")
        
        return results

    def _check_docker_specific(self) -> Dict[str, Any]:
        """Check Docker-specific configurations and status"""
        docker_info = {}
        
        # Check if we're actually in Docker
        docker_info["in_docker"] = self._is_running_in_docker()
        
        # Check environment variables
        docker_info["environment_vars"] = {
            "DOCKER_CONTAINER": os.environ.get("DOCKER_CONTAINER", "not_set"),
            "PYTHONPATH": os.environ.get("PYTHONPATH", "not_set"),
            "PYTHONUNBUFFERED": os.environ.get("PYTHONUNBUFFERED", "not_set")
        }
        
        # Test MCP server with ping request
        docker_info["mcp_server_responding"] = self._test_mcp_ping_request()
        docker_info["test_method"] = "ping_request"
        
        # Check if MCP server file exists
        mcp_server_file = self.project_root / "neozork_mcp_server.py"
        docker_info["mcp_server_file_exists"] = mcp_server_file.exists()
        if mcp_server_file.exists():
            docker_info["mcp_server_file_size"] = mcp_server_file.stat().st_size
            docker_info["mcp_server_file_modified"] = time.ctime(mcp_server_file.stat().st_mtime)
        
        # Check log file
        log_file = self.project_root / "logs" / "mcp_server.log"
        log_file_exists = log_file.exists()
        docker_info["log_file_exists"] = log_file_exists
        if log_file_exists:
            docker_info["log_file_size"] = log_file.stat().st_size
            docker_info["log_file_modified"] = time.ctime(log_file.stat().st_mtime)
        
        return docker_info

    def _is_running_in_docker(self) -> bool:
        """Check if we're running inside a Docker container"""
        try:
            # Check for Docker-specific files
            if Path("/.dockerenv").exists():
                return True
            
            # Check cgroup for Docker
            with open("/proc/1/cgroup", "r") as f:
                if "docker" in f.read():
                    return True
            
            # Check environment variable
            if os.environ.get("DOCKER_CONTAINER") == "true":
                return True
            
            return False
        except Exception:
            return False

class MCPServerChecker:
    """Check MCP server status and test connection (non-Docker environment)"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent.parent
        self.logger = self._setup_logging()
        self.server_process = None
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'mcp_status_check.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def check_server_running(self) -> bool:
        """Check if MCP server is already running"""
        try:
            # First try ping-based detection (like Docker)
            if self._test_mcp_ping_request():
                self.logger.info("MCP server is responding to ping requests")
                return True
            
            # Fallback to process-based detection
            result = subprocess.run(
                ['pgrep', '-f', 'neozork_mcp_server.py'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                pids = result.stdout.strip().split('\n')
                self.logger.info(f"MCP server is running with PIDs: {pids}")
                return True
            else:
                self.logger.info("MCP server is not running")
                return False
                
        except Exception as e:
            self.logger.error(f"Error checking server status: {e}")
            return False

    def start_server(self, timeout: int = 10) -> bool:
        """Start MCP server"""
        try:
            self.logger.info("Starting MCP server...")
            
            # Start server in background
            self.server_process = subprocess.Popen(
                [sys.executable, 'neozork_mcp_server.py'],
                cwd=self.project_root,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            time.sleep(2)
            
            # Check if process is still running
            if self.server_process.poll() is None:
                self.logger.info(f"MCP server started with PID: {self.server_process.pid}")
                return True
            else:
                stdout, stderr = self.server_process.communicate()
                self.logger.error(f"Server failed to start. STDOUT: {stdout}, STDERR: {stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error starting server: {e}")
            return False

    def stop_server(self):
        """Stop MCP server"""
        if self.server_process:
            try:
                self.logger.info("Stopping MCP server...")
                self.server_process.terminate()
                self.server_process.wait(timeout=5)
                self.logger.info("MCP server stopped")
            except subprocess.TimeoutExpired:
                self.logger.warning("Server didn't stop gracefully, killing...")
                self.server_process.kill()
            except Exception as e:
                self.logger.error(f"Error stopping server: {e}")

    def test_connection(self) -> Dict[str, Any]:
        """Test MCP server connection"""
        try:
            self.logger.info("Testing MCP server connection...")
            
            # Simple test - just check if server is running
            if self.check_server_running():
                return {
                    "status": "success",
                    "message": "Server is running",
                    "pids": self._get_server_pids()
                }
            else:
                return {"status": "failed", "error": "Server not running"}
            
        except Exception as e:
            self.logger.error(f"Error testing connection: {e}")
            return {"status": "failed", "error": str(e)}

    def _test_mcp_ping_request(self) -> bool:
        """Test MCP server by sending ping request via echo command"""
        try:
            self.logger.info("Testing MCP server with ping request...")
            
            # Create ping request JSON
            ping_request = '{"method": "neozork/ping", "id": 1, "params": {}}'
            
            # Send request to MCP server via echo command
            cmd = f'echo \'{ping_request}\' | python3 neozork_mcp_server.py'
            
            # Run command with timeout
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5,  # Reduced timeout for faster response
                cwd=self.project_root
            )
            
            # Check if we got a valid JSON response
            if result.returncode == 0 and result.stdout.strip():
                try:
                    response = json.loads(result.stdout.strip())
                    # Check if response contains expected ping response structure
                    if (response.get("jsonrpc") == "2.0" and 
                        response.get("id") == 1 and 
                        response.get("result", {}).get("pong") is True):
                        self.logger.info("MCP server responded to ping request successfully")
                        return True
                    else:
                        self.logger.warning(f"Unexpected ping response format: {response}")
                        return False
                except json.JSONDecodeError as e:
                    self.logger.warning(f"Invalid JSON response from MCP server: {e}")
                    self.logger.debug(f"Raw response: {result.stdout}")
                    return False
            else:
                self.logger.info("MCP server did not respond to ping request")
                if result.stderr:
                    self.logger.debug(f"Stderr: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.warning("MCP server ping request timed out")
            return False
        except Exception as e:
            self.logger.error(f"Error testing MCP ping request: {e}")
            return False

    def _get_server_pids(self) -> List[str]:
        """Get server PIDs"""
        try:
            result = subprocess.run(
                ['pgrep', '-f', 'neozork_mcp_server.py'],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return result.stdout.strip().split('\n')
            else:
                return []
                
        except Exception:
            return []

    def check_ide_configurations(self) -> Dict[str, Any]:
        """Check IDE configuration files"""
        configs = {}
        
        # Check Cursor config
        cursor_config = self.project_root / "cursor_mcp_config.json"
        if cursor_config.exists():
            try:
                with open(cursor_config, 'r') as f:
                    configs['cursor'] = {
                        'exists': True,
                        'size': cursor_config.stat().st_size,
                        'valid_json': True
                    }
            except Exception as e:
                configs['cursor'] = {
                    'exists': True,
                    'error': str(e),
                    'valid_json': False
                }
        else:
            configs['cursor'] = {'exists': False}
        
        # Check VS Code config
        vscode_config = self.project_root / ".vscode" / "settings.json"
        if vscode_config.exists():
            try:
                with open(vscode_config, 'r') as f:
                    configs['vscode'] = {
                        'exists': True,
                        'size': vscode_config.stat().st_size,
                        'valid_json': True
                    }
            except Exception as e:
                configs['vscode'] = {
                    'exists': True,
                    'error': str(e),
                    'valid_json': False
                }
        else:
            configs['vscode'] = {'exists': False}
        
        # Check PyCharm config
        pycharm_config = self.project_root / "pycharm_mcp_config.json"
        if pycharm_config.exists():
            try:
                with open(pycharm_config, 'r') as f:
                    configs['pycharm'] = {
                        'exists': True,
                        'size': pycharm_config.stat().st_size,
                        'valid_json': True
                    }
            except Exception as e:
                configs['pycharm'] = {
                    'exists': True,
                    'error': str(e),
                    'valid_json': False
                }
        else:
            configs['pycharm'] = {'exists': False}
        
        # Check Docker configuration (relevant for both host and Docker environments)
        docker_config = self.project_root / "docker.env"
        if docker_config.exists():
            try:
                # Try to read as JSON first (some docker.env files might be JSON)
                with open(docker_config, 'r') as f:
                    content = f.read().strip()
                    # Try to parse as JSON
                    try:
                        json.loads(content)
                        valid_json = True
                    except json.JSONDecodeError:
                        # If not JSON, check if it's valid environment file format
                        valid_json = all('=' in line or line.startswith('#') or not line.strip() 
                                       for line in content.split('\n'))
                    
                    configs['docker'] = {
                        'exists': True,
                        'size': docker_config.stat().st_size,
                        'valid_json': valid_json
                    }
            except Exception as e:
                configs['docker'] = {
                    'exists': True,
                    'error': str(e),
                    'valid_json': False
                }
        else:
            configs['docker'] = {'exists': False}
        
        return configs

    def run_comprehensive_check(self) -> Dict[str, Any]:
        """Run comprehensive MCP server check"""
        self.logger.info("Starting comprehensive MCP server check...")
        
        results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "environment": "host",
            "project_root": str(self.project_root),
            "server_running": False,
            "connection_test": {},
            "ide_configurations": {},
            "recommendations": []
        }
        
        # Check if server is running
        results["server_running"] = self.check_server_running()
        
        # Check IDE configurations
        results["ide_configurations"] = self.check_ide_configurations()
        
        # Test connection if server is running
        if results["server_running"]:
            results["connection_test"] = self.test_connection()
        else:
            results["connection_test"] = {"status": "skipped", "reason": "Server not running"}
            results["recommendations"].append("Start MCP server to test connection")
        
        # Generate recommendations
        if not results["server_running"]:
            results["recommendations"].append("Run: python3 neozork_mcp_server.py")
        
        missing_configs = [ide for ide, config in results["ide_configurations"].items() 
                          if not config.get('exists', False)]
        if missing_configs:
            results["recommendations"].append(f"Setup IDE configurations: python3 scripts/setup_ide_configs.py")
        
        if results["connection_test"].get("status") == "failed":
            results["recommendations"].append("Check MCP server logs: tail -f logs/neozork_mcp.log")
        
        return results

def main():
    """Main function"""
    print("🔍 MCP Server Status Checker")
    print("=" * 50)
    
    # Detect environment and use appropriate checker
    if is_running_in_docker():
        print("🐳 Detected Docker environment")
        checker = DockerMCPServerChecker()
    else:
        print("🖥️  Detected host environment")
        checker = MCPServerChecker()
    
    results = checker.run_comprehensive_check()
    
    # Print results
    print(f"\n📅 Check Time: {results['timestamp']}")
    print(f"🌍 Environment: {results['environment']}")
    print(f"📁 Project Root: {results['project_root']}")
    
    # Server status
    print(f"\n🚀 MCP Server Status:")
    if results["server_running"]:
        print("   ✅ Server is running")
    else:
        print("   ❌ Server is not running")
    
    # Connection test
    print(f"\n🔗 Connection Test:")
    connection = results["connection_test"]
    if connection.get("status") == "success":
        print("   ✅ Connection successful")
        if "test_method" in connection:
            print(f"   🔍 Test method: {connection['test_method']}")
        if "response_time" in connection:
            print(f"   ⏱️  Response time: {connection['response_time']}")
        if "pids" in connection:
            pids = connection["pids"]
            print(f"   👥 PIDs: {', '.join(pids)}")
        if "pid" in connection:
            print(f"   👥 PID: {connection['pid']}")
        if "log_file" in connection:
            print(f"   📄 Log file: {connection['log_file']}")
    elif connection.get("status") == "skipped":
        print(f"   ⏭️  Skipped: {connection.get('reason', 'Unknown')}")
    else:
        print(f"   ❌ Failed: {connection.get('error', 'Unknown error')}")
    
    # IDE configurations
    print(f"\n💻 IDE Configurations:")
    for ide, config in results["ide_configurations"].items():
        if config.get('exists'):
            size = config.get('size', 0)
            valid = config.get('valid_json', False)
            status = "✅" if valid else "⚠️"
            print(f"   {status} {ide.upper()}: {size} bytes")
        else:
            print(f"   ❌ {ide.upper()}: Not configured")
    
    # Docker-specific information
    if results.get("docker_specific"):
        print(f"\n🐳 Docker Information:")
        docker_info = results["docker_specific"]
        print(f"   📦 In Docker: {docker_info.get('in_docker', 'Unknown')}")
        print(f"   🔄 MCP Server responding: {docker_info.get('mcp_server_responding', False)}")
        print(f"   🔍 Test method: {docker_info.get('test_method', 'unknown')}")
        
        # MCP server file info
        if docker_info.get('mcp_server_file_exists'):
            print(f"   📄 MCP server file: {docker_info.get('mcp_server_file_size', 0)} bytes")
            print(f"   🕒 File modified: {docker_info.get('mcp_server_file_modified', 'Unknown')}")
        else:
            print(f"   ❌ MCP server file: Not found")
        
        # Log file info
        if docker_info.get('log_file_exists'):
            print(f"   📝 Log file: {docker_info.get('log_file_size', 0)} bytes")
            print(f"   🕒 Log modified: {docker_info.get('log_file_modified', 'Unknown')}")
        else:
            print(f"   ❌ Log file: Not found")
    
    # Recommendations
    if results["recommendations"]:
        print(f"\n💡 Recommendations:")
        for rec in results["recommendations"]:
            print(f"   • {rec}")
    
    # Save results
    log_file = checker.project_root / "logs" / f"mcp_status_check_{results['environment']}.json"
    with open(log_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📝 Results saved to: {log_file}")
    
    # Return exit code
    if results["server_running"] and results["connection_test"].get("status") == "success":
        print("\n✅ All checks passed!")
        return 0
    else:
        print("\n⚠️  Some checks failed. See recommendations above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 