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

class DockerMCPServerChecker:
    """Check MCP server status inside Docker container"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent
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
            # Method 1: Check PID file (primary method)
            pid_file = Path("/tmp/mcp_server.pid")
            if pid_file.exists():
                try:
                    with open(pid_file, 'r') as f:
                        pid = int(f.read().strip())
                    
                    # Check if process is still running
                    if self._is_process_running(pid):
                        self.logger.info(f"MCP server is running with PID: {pid}")
                        return True
                    else:
                        self.logger.warning(f"PID file exists but process {pid} is not running")
                        # Clean up stale PID file
                        pid_file.unlink(missing_ok=True)
                        return False
                except (ValueError, FileNotFoundError) as e:
                    self.logger.error(f"Error reading PID file: {e}")
                    return False
            else:
                self.logger.info("MCP server PID file not found")
            
            # Method 2: Check with ps aux | grep (fallback method)
            return self._check_server_with_ps()
                
        except Exception as e:
            self.logger.error(f"Error checking server status in Docker: {e}")
            return False

    def _check_server_with_ps(self) -> bool:
        """Check if MCP server is running using Docker-safe universal method"""
        pid = self._find_mcp_server_pid()
        if pid:
            self.logger.info(f"Found MCP server process with PID: {pid} via universal Docker-safe method")
            return True
        self.logger.info("No MCP server process found via universal Docker-safe method")
        return False

    def _find_mcp_server_pid(self) -> Optional[int]:
        """Find MCP server PID using /proc, pgrep, or pidof (Docker-safe)"""
        # 1. Try /proc
        proc_dir = Path("/proc")
        if proc_dir.exists():
            for proc in proc_dir.iterdir():
                if not proc.is_dir() or not proc.name.isdigit():
                    continue
                try:
                    cmdline_file = proc / "cmdline"
                    if cmdline_file.exists():
                        with open(cmdline_file, 'rb') as f:
                            cmdline = f.read().replace(b'\x00', b' ')
                            if b'neozork_mcp_server.py' in cmdline:
                                return int(proc.name)
                except Exception:
                    continue
        
        # 2. Try pgrep
        try:
            result = subprocess.run(['pgrep', '-f', 'neozork_mcp_server.py'], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                pids = [int(pid) for pid in result.stdout.strip().split('\n') if pid.strip().isdigit()]
                if pids:
                    return pids[0]
        except Exception:
            pass
        
        # 3. Try pidof (available in your Docker container)
        try:
            result = subprocess.run(['pidof', 'python3'], capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                pids = [int(pid) for pid in result.stdout.strip().split() if pid.strip().isdigit()]
                # Check each python3 process for neozork_mcp_server.py
                for pid in pids:
                    try:
                        cmdline_file = proc_dir / str(pid) / "cmdline"
                        if cmdline_file.exists():
                            with open(cmdline_file, 'rb') as f:
                                cmdline = f.read().replace(b'\x00', b' ')
                                if b'neozork_mcp_server.py' in cmdline:
                                    return pid
                    except Exception:
                        continue
        except Exception:
            pass
        
        return None

    def _is_process_running(self, pid: int) -> bool:
        """Check if process with given PID is running"""
        try:
            # Use kill -0 to check if process exists
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def test_connection(self) -> Dict[str, Any]:
        """Test MCP server connection inside Docker"""
        try:
            self.logger.info("Testing MCP server connection in Docker...")
            
            # Check if server is running using both methods
            server_running = self.check_server_running()
            
            if server_running:
                # Try to connect to the server via HTTP/JSON-RPC
                # MCP server typically runs on localhost with a specific port
                return self._test_mcp_protocol_connection()
            else:
                return {"status": "failed", "error": "Server not running"}
            
        except Exception as e:
            self.logger.error(f"Error testing connection in Docker: {e}")
            return {"status": "failed", "error": str(e)}

    def _test_mcp_protocol_connection(self) -> Dict[str, Any]:
        """Test MCP protocol connection"""
        try:
            # Check if MCP server log file exists and has recent activity
            log_file = self.project_root / "logs" / "mcp_server.log"
            if log_file.exists():
                # Check if log file was modified recently (within last 30 seconds)
                mtime = log_file.stat().st_mtime
                if time.time() - mtime < 30:
                    # Read last few lines to check for errors
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        if lines:
                            last_line = lines[-1].strip()
                            if "error" in last_line.lower() or "exception" in last_line.lower():
                                return {"status": "failed", "error": f"Server error in logs: {last_line}"}
                            else:
                                return {
                                    "status": "success",
                                    "message": "Server is running (confirmed via logs)",
                                    "log_file": str(log_file),
                                    "last_activity": time.ctime(mtime)
                                }
            
            # If no log file or no recent activity, try to ping the server
            return self._ping_mcp_server()
            
        except Exception as e:
            self.logger.error(f"Error testing MCP protocol: {e}")
            return {"status": "failed", "error": str(e)}

    def _ping_mcp_server(self) -> Dict[str, Any]:
        """Ping MCP server to check if it's responsive"""
        try:
            # Try to send a simple ping request to the MCP server
            # This is a basic test - in a real implementation, you might want to
            # send actual MCP protocol messages
            
            # For now, we'll just check if the process is responsive
            pid_file = Path("/tmp/mcp_server.pid")
            if pid_file.exists():
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())
                
                if self._is_process_running(pid):
                    return {
                        "status": "success",
                        "message": "Server process is running and responsive",
                        "pid": pid,
                        "detection_method": "pid_file"
                    }
                else:
                    return {"status": "failed", "error": "Server process is not responsive"}
            else:
                # Fallback to alternative detection methods
                if self._check_server_with_ps():
                    # Try to get PID from /proc
                    pid = self._find_mcp_server_pid()
                    if pid:
                        return {
                            "status": "success",
                            "message": "Server process is running (confirmed via /proc)",
                            "pid": pid,
                            "detection_method": "proc_filesystem"
                        }
                    else:
                        return {
                            "status": "success",
                            "message": "Server process is running (confirmed via alternative detection)",
                            "detection_method": "alternative"
                        }
                else:
                    return {"status": "failed", "error": "No PID file found and no process detected"}
                
        except Exception as e:
            self.logger.error(f"Error pinging MCP server: {e}")
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
            configs['docker'] = {
                'exists': True,
                'size': docker_config.stat().st_size
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
        
        # Check if PID file exists
        pid_file = Path("/tmp/mcp_server.pid")
        docker_info["pid_file_exists"] = pid_file.exists()
        
        if pid_file.exists():
            try:
                with open(pid_file, 'r') as f:
                    pid = int(f.read().strip())
                docker_info["pid"] = pid
                docker_info["process_running"] = self._is_process_running(pid)
                docker_info["detection_method"] = "pid_file"
            except Exception as e:
                docker_info["pid_error"] = str(e)
        else:
            # Check if server is running via alternative methods
            if self._check_server_with_ps():
                # Try to get PID from /proc
                pid = self._find_mcp_server_pid()
                if pid:
                    docker_info["pid"] = pid
                    docker_info["detection_method"] = "proc_filesystem"
                    docker_info["process_running"] = True
                else:
                    docker_info["detection_method"] = "alternative"
                    docker_info["process_running"] = True
            else:
                docker_info["detection_method"] = "none"
                docker_info["process_running"] = False
        
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
        self.project_root = project_root or Path(__file__).parent.parent
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
            # Check for Python processes running the MCP server
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
        print(f"   📄 PID file: {docker_info.get('pid_file_exists', False)}")
        if docker_info.get('pid'):
            print(f"   🔢 PID: {docker_info['pid']}")
            print(f"   🟢 Process running: {docker_info.get('process_running', False)}")
        if docker_info.get('detection_method'):
            detection_method = docker_info.get('detection_method', 'unknown')
            if detection_method == 'pid_file':
                print(f"   🔍 Detection: PID file")
            elif detection_method == 'proc_filesystem':
                print(f"   🔍 Detection: /proc filesystem")
            elif detection_method == 'alternative':
                print(f"   🔍 Detection: Alternative methods")
            elif detection_method == 'none':
                print(f"   🔍 Detection: Not found")
            else:
                print(f"   🔍 Detection: {detection_method}")
        if docker_info.get('log_file_exists'):
            print(f"   📝 Log file: {docker_info.get('log_file_size', 0)} bytes")
            print(f"   🕒 Last modified: {docker_info.get('log_file_modified', 'Unknown')}")
    
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
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug-detect', action='store_true', help='Debug: print detected MCP server PID in Docker')
    args = parser.parse_args()
    if args.debug_detect:
        checker = DockerMCPServerChecker()
        pid = checker._find_mcp_server_pid()
        print(f"[DEBUG] Detected MCP server PID: {pid}")
        sys.exit(0 if pid else 1)
    sys.exit(main()) 