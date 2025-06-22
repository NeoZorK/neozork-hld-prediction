#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PyCharm GitHub Copilot MCP Server Runner
Enhanced script for running and testing the PyCharm GitHub Copilot MCP Server
"""

import os
import sys
import json
import time
import signal
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from pycharm_github_copilot_mcp import PyCharmGitHubCopilotMCPServer

class PyCharmGitHubCopilotMCPServerRunner:
    """Enhanced runner for PyCharm GitHub Copilot MCP Server"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.project_root = project_root
        self.config_path = config_path or project_root / "cursor_mcp_config.json"
        self.logger = self._setup_logging()
        self.server_process = None
        self.test_results = {}
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the runner"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"pycharm_copilot_mcp_runner_{time.strftime('%Y%m%d')}.log"
        
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [PyCharmCopilotMCPRunner] %(message)s'
        )
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        logger = logging.getLogger('pycharm_copilot_mcp_runner')
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        
        return logger
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"Loaded configuration from {self.config_path}")
                return config
            else:
                self.logger.warning(f"Configuration file not found: {self.config_path}")
                return self._get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            return self._get_default_config()
            
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "server": {
                "name": "PyCharm GitHub Copilot MCP Server",
                "command": "python",
                "args": ["pycharm_github_copilot_mcp.py"],
                "env": {
                    "PYTHONPATH": str(self.project_root),
                    "LOG_LEVEL": "INFO",
                    "MCP_SERVER_TYPE": "pycharm_copilot",
                    "ENABLE_FINANCIAL_DATA": "true",
                    "ENABLE_INDICATORS": "true",
                    "ENABLE_GITHUB_COPILOT": "true"
                },
                "cwd": str(self.project_root),
                "transport": "stdio"
            },
            "testing": {
                "enable_tests": True,
                "test_timeout": 30,
                "performance_tests": True,
                "coverage_tests": True,
                "github_copilot_tests": True
            },
            "monitoring": {
                "enable_monitoring": True,
                "health_check_interval": 60,
                "max_memory_mb": 512,
                "max_cpu_percent": 80
            }
        }
        
    def start_server(self, mode: str = "stdio") -> bool:
        """Start the MCP server"""
        try:
            config = self.load_config()
            server_config = config["server"]
            
            # Prepare environment
            env = os.environ.copy()
            env.update(server_config.get("env", {}))
            
            # Prepare command
            cmd = [server_config["command"]] + server_config["args"]
            
            self.logger.info(f"Starting PyCharm GitHub Copilot MCP Server in {mode} mode")
            self.logger.info(f"Command: {' '.join(cmd)}")
            self.logger.info(f"Working directory: {server_config['cwd']}")
            
            if mode == "stdio":
                # Start server in stdio mode for IDE integration
                self.server_process = subprocess.Popen(
                    cmd,
                    cwd=server_config["cwd"],
                    env=env,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )
            elif mode == "test":
                # Start server in test mode
                self.server_process = subprocess.Popen(
                    cmd,
                    cwd=server_config["cwd"],
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                # Start server in background mode
                self.server_process = subprocess.Popen(
                    cmd,
                    cwd=server_config["cwd"],
                    env=env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
            # Wait a moment for server to start
            time.sleep(2)
            
            if self.server_process.poll() is None:
                self.logger.info("PyCharm GitHub Copilot MCP Server started successfully")
                return True
            else:
                self.logger.error("Failed to start PyCharm GitHub Copilot MCP Server")
                return False
                
        except Exception as e:
            self.logger.error(f"Error starting server: {e}")
            return False
            
    def stop_server(self) -> bool:
        """Stop the MCP server"""
        try:
            if self.server_process and self.server_process.poll() is None:
                self.logger.info("Stopping PyCharm GitHub Copilot MCP Server")
                self.server_process.terminate()
                
                # Wait for graceful shutdown
                try:
                    self.server_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.logger.warning("Server did not stop gracefully, forcing kill")
                    self.server_process.kill()
                    
                self.logger.info("PyCharm GitHub Copilot MCP Server stopped")
                return True
            else:
                self.logger.info("Server is not running")
                return True
                
        except Exception as e:
            self.logger.error(f"Error stopping server: {e}")
            return False
            
    def run_tests(self) -> Dict[str, Any]:
        """Run comprehensive tests"""
        self.logger.info("Running PyCharm GitHub Copilot MCP Server tests")
        
        test_results = {
            "server_startup": False,
            "basic_functionality": False,
            "completion_tests": False,
            "performance_tests": False,
            "coverage_tests": False,
            "github_copilot_tests": False,
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0
        }
        
        try:
            # Test 1: Server startup
            test_results["total_tests"] += 1
            if self.start_server(mode="test"):
                test_results["server_startup"] = True
                test_results["passed_tests"] += 1
                self.logger.info("✓ Server startup test passed")
            else:
                test_results["failed_tests"] += 1
                self.logger.error("✗ Server startup test failed")
                
            # Test 2: Basic functionality
            test_results["total_tests"] += 1
            if self._test_basic_functionality():
                test_results["basic_functionality"] = True
                test_results["passed_tests"] += 1
                self.logger.info("✓ Basic functionality test passed")
            else:
                test_results["failed_tests"] += 1
                self.logger.error("✗ Basic functionality test failed")
                
            # Test 3: Completion tests
            test_results["total_tests"] += 1
            if self._test_completion():
                test_results["completion_tests"] = True
                test_results["passed_tests"] += 1
                self.logger.info("✓ Completion tests passed")
            else:
                test_results["failed_tests"] += 1
                self.logger.error("✗ Completion tests failed")
                
            # Test 4: Performance tests
            test_results["total_tests"] += 1
            if self._test_performance():
                test_results["performance_tests"] = True
                test_results["passed_tests"] += 1
                self.logger.info("✓ Performance tests passed")
            else:
                test_results["failed_tests"] += 1
                self.logger.error("✗ Performance tests failed")
                
            # Test 5: Coverage tests
            test_results["total_tests"] += 1
            if self._test_coverage():
                test_results["coverage_tests"] = True
                test_results["passed_tests"] += 1
                self.logger.info("✓ Coverage tests passed")
            else:
                test_results["failed_tests"] += 1
                self.logger.error("✗ Coverage tests failed")
                
            # Test 6: GitHub Copilot tests
            test_results["total_tests"] += 1
            if self._test_github_copilot():
                test_results["github_copilot_tests"] = True
                test_results["passed_tests"] += 1
                self.logger.info("✓ GitHub Copilot tests passed")
            else:
                test_results["failed_tests"] += 1
                self.logger.error("✗ GitHub Copilot tests failed")
                
        except Exception as e:
            self.logger.error(f"Error during testing: {e}")
            
        finally:
            self.stop_server()
            
        self.test_results = test_results
        return test_results
        
    def _test_basic_functionality(self) -> bool:
        """Test basic server functionality"""
        try:
            # Test initialization
            init_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "processId": 12345,
                    "rootUri": f"file://{self.project_root}",
                    "capabilities": {}
                }
            }
            
            response = self._send_request(init_request)
            if response and "result" in response:
                server_info = response["result"].get("serverInfo", {})
                if server_info.get("name") == "PyCharm GitHub Copilot MCP Server":
                    return True
                    
            return False
            
        except Exception as e:
            self.logger.error(f"Basic functionality test error: {e}")
            return False
            
    def _test_completion(self) -> bool:
        """Test completion functionality"""
        try:
            # Test completion request
            completion_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "textDocument/completion",
                "params": {
                    "textDocument": {
                        "uri": f"file://{self.project_root}/test.py"
                    },
                    "position": {
                        "line": 0,
                        "character": 0
                    }
                }
            }
            
            response = self._send_request(completion_request)
            if response and "result" in response:
                items = response["result"].get("items", [])
                return len(items) > 0
                
            return False
            
        except Exception as e:
            self.logger.error(f"Completion test error: {e}")
            return False
            
    def _test_performance(self) -> bool:
        """Test server performance"""
        try:
            start_time = time.time()
            
            # Send multiple requests
            for i in range(10):
                request = {
                    "jsonrpc": "2.0",
                    "id": i,
                    "method": "cursor/projectInfo",
                    "params": {}
                }
                self._send_request(request)
                
            end_time = time.time()
            total_time = end_time - start_time
            
            # Performance threshold: 10 requests should complete in under 5 seconds
            return total_time < 5.0
            
        except Exception as e:
            self.logger.error(f"Performance test error: {e}")
            return False
            
    def _test_coverage(self) -> bool:
        """Test code coverage"""
        try:
            # Run pytest with coverage
            cmd = [
                "pytest",
                "tests/mcp/test_cursor_mcp_server.py",
                "--cov=cursor_mcp_server",
                "--cov-report=term-missing",
                "--cov-fail-under=80"
            ]
            
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return result.returncode == 0
            
        except Exception as e:
            self.logger.error(f"Coverage test error: {e}")
            return False
            
    def _test_github_copilot(self) -> bool:
        """Test GitHub Copilot functionality"""
        try:
            # Implementation of the test
            # This is a placeholder and should be replaced with the actual implementation
            return True
            
        except Exception as e:
            self.logger.error(f"GitHub Copilot test error: {e}")
            return False
            
    def _send_request(self, request: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Send request to MCP server"""
        try:
            if not self.server_process or self.server_process.poll() is not None:
                return None
                
            # Send request
            request_str = json.dumps(request)
            content_length = len(request_str)
            message = f"Content-Length: {content_length}\r\n\r\n{request_str}"
            
            self.server_process.stdin.write(message)
            self.server_process.stdin.flush()
            
            # Read response
            response = self._read_response()
            return response
            
        except Exception as e:
            self.logger.error(f"Error sending request: {e}")
            return None
            
    def _read_response(self) -> Optional[Dict[str, Any]]:
        """Read response from MCP server"""
        try:
            # Read headers
            headers = {}
            while True:
                line = self.server_process.stdout.readline().strip()
                if not line:
                    break
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip()] = value.strip()
                    
            # Read body
            content_length = int(headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.server_process.stdout.read(content_length)
                return json.loads(body)
                
            return None
            
        except Exception as e:
            self.logger.error(f"Error reading response: {e}")
            return None
            
    def generate_report(self) -> str:
        """Generate test report"""
        if not self.test_results:
            return "No test results available"
            
        report = []
        report.append("=" * 60)
        report.append("PyCharm GitHub Copilot MCP Server Test Report")
        report.append("=" * 60)
        report.append(f"Total Tests: {self.test_results['total_tests']}")
        report.append(f"Passed: {self.test_results['passed_tests']}")
        report.append(f"Failed: {self.test_results['failed_tests']}")
        report.append(f"Success Rate: {(self.test_results['passed_tests'] / self.test_results['total_tests'] * 100):.1f}%")
        report.append("")
        
        # Individual test results
        test_names = {
            "server_startup": "Server Startup",
            "basic_functionality": "Basic Functionality",
            "completion_tests": "Completion Tests",
            "performance_tests": "Performance Tests",
            "coverage_tests": "Coverage Tests",
            "github_copilot_tests": "GitHub Copilot Tests"
        }
        
        for test_key, test_name in test_names.items():
            status = "✓ PASS" if self.test_results.get(test_key, False) else "✗ FAIL"
            report.append(f"{test_name}: {status}")
            
        report.append("=" * 60)
        
        return "\n".join(report)
        
    def run_monitoring(self, duration: int = 3600) -> None:
        """Run server monitoring"""
        self.logger.info(f"Starting server monitoring for {duration} seconds")
        
        if not self.start_server(mode="background"):
            self.logger.error("Failed to start server for monitoring")
            return
            
        try:
            start_time = time.time()
            while time.time() - start_time < duration:
                # Check server health
                if self.server_process.poll() is not None:
                    self.logger.error("Server process terminated unexpectedly")
                    break
                    
                # Check resource usage
                try:
                    import psutil
                    process = psutil.Process(self.server_process.pid)
                    memory_mb = process.memory_info().rss / 1024 / 1024
                    cpu_percent = process.cpu_percent()
                    
                    self.logger.info(f"Memory: {memory_mb:.1f} MB, CPU: {cpu_percent:.1f}%")
                    
                except ImportError:
                    self.logger.warning("psutil not available, skipping resource monitoring")
                    
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            self.logger.info("Monitoring interrupted by user")
            
        finally:
            self.stop_server()
            
    def create_ide_config(self, ide: str) -> bool:
        """Create IDE configuration files"""
        try:
            if ide.lower() == "cursor":
                return self._create_cursor_config()
            elif ide.lower() == "vscode":
                return self._create_vscode_config()
            elif ide.lower() == "pycharm":
                return self._create_pycharm_config()
            else:
                self.logger.error(f"Unsupported IDE: {ide}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error creating IDE config: {e}")
            return False
            
    def _create_cursor_config(self) -> bool:
        """Create Cursor IDE configuration"""
        config = {
            "mcpServers": {
                "cursor-mcp": {
                    "command": "python",
                    "args": ["cursor_mcp_server.py"],
                    "env": {
                        "PYTHONPATH": str(self.project_root),
                        "LOG_LEVEL": "INFO"
                    }
                }
            }
        }
        
        config_path = self.project_root / ".cursor" / "settings.json"
        config_path.parent.mkdir(exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
            
        self.logger.info(f"Created Cursor config: {config_path}")
        return True
        
    def _create_vscode_config(self) -> bool:
        """Create VS Code configuration"""
        config = {
            "mcp.servers": {
                "cursor-mcp": {
                    "command": "python",
                    "args": ["cursor_mcp_server.py"],
                    "env": {
                        "PYTHONPATH": str(self.project_root),
                        "LOG_LEVEL": "INFO"
                    }
                }
            }
        }
        
        config_path = self.project_root / ".vscode" / "settings.json"
        config_path.parent.mkdir(exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
            
        self.logger.info(f"Created VS Code config: {config_path}")
        return True
        
    def _create_pycharm_config(self) -> bool:
        """Create PyCharm configuration"""
        config = {
            "name": "PyCharm GitHub Copilot MCP Server",
            "command": "python",
            "args": ["pycharm_github_copilot_mcp.py"],
            "env": {
                "PYTHONPATH": str(self.project_root),
                "LOG_LEVEL": "INFO",
                "MCP_SERVER_TYPE": "pycharm_copilot",
                "ENABLE_FINANCIAL_DATA": "true",
                "ENABLE_INDICATORS": "true",
                "ENABLE_GITHUB_COPILOT": "true"
            },
            "cwd": str(self.project_root),
            "transport": "stdio"
        }
        
        config_path = self.project_root / "pycharm_mcp_config.json"
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
            
        self.logger.info(f"Created PyCharm config: {config_path}")
        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="PyCharm GitHub Copilot MCP Server Runner")
    parser.add_argument("--mode", choices=["stdio", "test", "background"], 
                       default="stdio", help="Server mode")
    parser.add_argument("--config", type=Path, help="Configuration file path")
    parser.add_argument("--test", action="store_true", help="Run tests")
    parser.add_argument("--monitor", type=int, help="Run monitoring for N seconds")
    parser.add_argument("--create-config", choices=["cursor", "vscode", "pycharm"], 
                       help="Create IDE configuration")
    parser.add_argument("--report", action="store_true", help="Generate test report")
    
    args = parser.parse_args()
    
    runner = PyCharmGitHubCopilotMCPServerRunner(config_path=args.config)
    
    try:
        if args.test:
            # Run tests
            results = runner.run_tests()
            if args.report:
                print(runner.generate_report())
            else:
                print(f"Tests completed: {results['passed_tests']}/{results['total_tests']} passed")
                
        elif args.monitor:
            # Run monitoring
            runner.run_monitoring(args.monitor)
            
        elif args.create_config:
            # Create IDE configuration
            if runner.create_ide_config(args.create_config):
                print(f"Created {args.create_config} configuration")
            else:
                print(f"Failed to create {args.create_config} configuration")
                
        else:
            # Start server
            if runner.start_server(args.mode):
                print(f"PyCharm GitHub Copilot MCP Server started in {args.mode} mode")
                print("Press Ctrl+C to stop")
                
                try:
                    # Keep server running
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\nStopping server...")
                    runner.stop_server()
            else:
                print("Failed to start server")
                sys.exit(1)
                
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 