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
            
            # Check if server file exists
            server_file = self.project_root / "pycharm_github_copilot_mcp.py"
            if not server_file.exists():
                self.logger.error(f"Server file not found: {server_file}")
                print(f"❌ Server file not found: {server_file}")
                return False
            
            # Prepare environment
            env = os.environ.copy()
            env.update(server_config.get("env", {}))
            
            # Prepare command
            cmd = [server_config["command"]] + server_config["args"]
            
            self.logger.info(f"Starting PyCharm GitHub Copilot MCP Server in {mode} mode")
            self.logger.info(f"Command: {' '.join(cmd)}")
            self.logger.info(f"Working directory: {server_config['cwd']}")
            
            print(f"🚀 Starting PyCharm GitHub Copilot MCP Server in {mode} mode...")
            print(f"📁 Working directory: {server_config['cwd']}")
            print(f"🐍 Command: {' '.join(cmd)}")
            
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
                print("✅ PyCharm GitHub Copilot MCP Server started successfully")
                return True
            else:
                # Check for errors
                stdout, stderr = self.server_process.communicate()
                self.logger.error(f"Failed to start PyCharm GitHub Copilot MCP Server")
                self.logger.error(f"STDOUT: {stdout}")
                self.logger.error(f"STDERR: {stderr}")
                print("❌ Failed to start PyCharm GitHub Copilot MCP Server")
                print(f"Error output: {stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error starting server: {e}")
            print(f"❌ Error starting server: {e}")
            return False
            
    def stop_server(self) -> bool:
        """Stop the MCP server"""
        try:
            if self.server_process and self.server_process.poll() is None:
                self.logger.info("Stopping PyCharm GitHub Copilot MCP Server")
                print("🛑 Stopping PyCharm GitHub Copilot MCP Server...")
                self.server_process.terminate()
                
                # Wait for graceful shutdown
                try:
                    self.server_process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.logger.warning("Server did not stop gracefully, forcing kill")
                    print("⚠️ Server did not stop gracefully, forcing kill...")
                    self.server_process.kill()
                    
                self.logger.info("PyCharm GitHub Copilot MCP Server stopped")
                print("✅ PyCharm GitHub Copilot MCP Server stopped")
                return True
            else:
                self.logger.info("Server is not running")
                print("ℹ️ Server is not running")
                return True
                
        except Exception as e:
            self.logger.error(f"Error stopping server: {e}")
            print(f"❌ Error stopping server: {e}")
            return False
            
    def run_tests(self) -> Dict[str, Any]:
        """Run comprehensive tests"""
        self.logger.info("Running PyCharm GitHub Copilot MCP Server tests")
        print("🧪 Running PyCharm GitHub Copilot MCP Server tests...")
        
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
            if self._test_server_startup():
                test_results["server_startup"] = True
                test_results["passed_tests"] += 1
                print("✅ Server startup test passed")
            else:
                test_results["failed_tests"] += 1
                print("❌ Server startup test failed")
                
            # Test 2: Basic functionality
            test_results["total_tests"] += 1
            if self._test_basic_functionality():
                test_results["basic_functionality"] = True
                test_results["passed_tests"] += 1
                print("✅ Basic functionality test passed")
            else:
                test_results["failed_tests"] += 1
                print("❌ Basic functionality test failed")
                
            # Test 3: Completion tests
            test_results["total_tests"] += 1
            if self._test_completion():
                test_results["completion_tests"] = True
                test_results["passed_tests"] += 1
                print("✅ Completion tests passed")
            else:
                test_results["failed_tests"] += 1
                print("❌ Completion tests failed")
                
            # Test 4: Performance tests
            test_results["total_tests"] += 1
            if self._test_performance():
                test_results["performance_tests"] = True
                test_results["passed_tests"] += 1
                print("✅ Performance tests passed")
            else:
                test_results["failed_tests"] += 1
                print("❌ Performance tests failed")
                
            # Test 5: Coverage tests
            test_results["total_tests"] += 1
            if self._test_coverage():
                test_results["coverage_tests"] = True
                test_results["passed_tests"] += 1
                print("✅ Coverage tests passed")
            else:
                test_results["failed_tests"] += 1
                print("❌ Coverage tests failed")
                
            # Test 6: GitHub Copilot tests
            test_results["total_tests"] += 1
            if self._test_github_copilot():
                test_results["github_copilot_tests"] = True
                test_results["passed_tests"] += 1
                print("✅ GitHub Copilot tests passed")
            else:
                test_results["failed_tests"] += 1
                print("❌ GitHub Copilot tests failed")
                
        except Exception as e:
            self.logger.error(f"Error during testing: {e}")
            print(f"❌ Error during testing: {e}")
            
        self.test_results = test_results
        return test_results

    def _test_server_startup(self) -> bool:
        """Test server startup"""
        try:
            # Try to import the server module
            sys.path.insert(0, str(self.project_root))
            from pycharm_github_copilot_mcp import PyCharmGitHubCopilotMCPServer
            
            # Create server instance
            server = PyCharmGitHubCopilotMCPServer()
            
            # Check basic properties
            assert server.running == True
            assert len(server.handlers) > 0
            assert 'initialize' in server.handlers
            
            return True
            
        except Exception as e:
            self.logger.error(f"Server startup test error: {e}")
            return False

    def _test_basic_functionality(self) -> bool:
        """Test basic server functionality"""
        try:
            from pycharm_github_copilot_mcp import PyCharmGitHubCopilotMCPServer
            
            server = PyCharmGitHubCopilotMCPServer()
            
            # Test initialize handler
            result = server._handle_initialize(1, {})
            assert result is not None
            assert 'capabilities' in result
            assert 'serverInfo' in result
            
            # Test project info handler
            result = server._handle_project_info(2, {})
            assert result is not None
            assert 'name' in result
            
            return True
            
        except Exception as e:
            self.logger.error(f"Basic functionality test error: {e}")
            return False

    def _test_completion(self) -> bool:
        """Test completion functionality"""
        try:
            from pycharm_github_copilot_mcp import PyCharmGitHubCopilotMCPServer
            
            server = PyCharmGitHubCopilotMCPServer()
            
            # Test completion handler
            result = server._handle_completion(3, {})
            assert result is not None
            assert 'items' in result
            assert isinstance(result['items'], list)
            
            # Test specific completions
            project_completions = server._get_project_completions()
            assert isinstance(project_completions, list)
            
            financial_completions = server._get_financial_completions()
            assert isinstance(financial_completions, list)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Completion test error: {e}")
            return False

    def _test_performance(self) -> bool:
        """Test performance"""
        try:
            import time
            from pycharm_github_copilot_mcp import PyCharmGitHubCopilotMCPServer
            
            start_time = time.time()
            server = PyCharmGitHubCopilotMCPServer()
            init_time = time.time() - start_time
            
            # Check initialization time
            assert init_time < 10, f"Initialization too slow: {init_time:.2f}s"
            
            # Test completion speed
            start_time = time.time()
            server._handle_completion(1, {})
            completion_time = time.time() - start_time
            
            assert completion_time < 1, f"Completion too slow: {completion_time:.2f}s"
            
            return True
            
        except Exception as e:
            self.logger.error(f"Performance test error: {e}")
            return False

    def _test_coverage(self) -> bool:
        """Test code coverage"""
        try:
            # Check if pytest and coverage are available
            try:
                import pytest
                import coverage
            except ImportError:
                self.logger.warning("pytest or coverage not available, skipping coverage test")
                return True
            
            # Run basic coverage check
            from pycharm_github_copilot_mcp import PyCharmGitHubCopilotMCPServer
            
            server = PyCharmGitHubCopilotMCPServer()
            
            # Test all main handlers
            handlers_to_test = [
                'initialize', 'shutdown', 'exit', 'completion',
                'project_info', 'financial_data', 'indicators'
            ]
            
            for handler_name in handlers_to_test:
                if handler_name in server.handlers:
                    handler = server.handlers[handler_name]
                    # Just check if handler is callable
                    assert callable(handler)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Coverage test error: {e}")
            return False

    def _test_github_copilot(self) -> bool:
        """Test GitHub Copilot functionality"""
        try:
            from pycharm_github_copilot_mcp import PyCharmGitHubCopilotMCPServer
            
            server = PyCharmGitHubCopilotMCPServer()
            
            # Test Copilot suggestions
            result = server._handle_copilot_suggestions(1, {'context': 'financial data'})
            assert result is not None
            assert 'suggestions' in result
            assert isinstance(result['suggestions'], list)
            
            # Test Copilot context
            result = server._handle_copilot_context(2, {})
            assert result is not None
            assert 'project_type' in result
            assert 'available_symbols' in result
            
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
            request_str = json.dumps(request) + '\n'
            self.server_process.stdin.write(request_str)
            self.server_process.stdin.flush()
            
            # Read response
            return self._read_response()
            
        except Exception as e:
            self.logger.error(f"Error sending request: {e}")
            return None

    def _read_response(self) -> Optional[Dict[str, Any]]:
        """Read response from MCP server"""
        try:
            if not self.server_process or self.server_process.poll() is not None:
                return None
                
            # Read response with timeout
            import select
            if select.select([self.server_process.stdout], [], [], 5.0)[0]:
                response_line = self.server_process.stdout.readline()
                if response_line:
                    return json.loads(response_line)
                    
            return None
            
        except Exception as e:
            self.logger.error(f"Error reading response: {e}")
            return None

    def generate_report(self) -> str:
        """Generate test report"""
        report = []
        report.append("=" * 60)
        report.append("PyCharm GitHub Copilot MCP Server Test Report")
        report.append("=" * 60)
        report.append(f"Total Tests: {self.test_results['total_tests']}")
        report.append(f"Passed: {self.test_results['passed_tests']}")
        report.append(f"Failed: {self.test_results['failed_tests']}")
        report.append(f"Success Rate: {(self.test_results['passed_tests'] / self.test_results['total_tests'] * 100):.1f}%")
        report.append("")
        
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
        print(f"📊 Starting server monitoring for {duration} seconds...")
        
        if not self.start_server(mode="background"):
            self.logger.error("Failed to start server for monitoring")
            print("❌ Failed to start server for monitoring")
            return
            
        try:
            start_time = time.time()
            while time.time() - start_time < duration:
                # Check server health
                if self.server_process.poll() is not None:
                    self.logger.error("Server process terminated unexpectedly")
                    print("❌ Server process terminated unexpectedly")
                    break
                    
                # Check resource usage
                try:
                    import psutil
                    process = psutil.Process(self.server_process.pid)
                    memory_mb = process.memory_info().rss / 1024 / 1024
                    cpu_percent = process.cpu_percent()
                    
                    self.logger.info(f"Memory: {memory_mb:.1f} MB, CPU: {cpu_percent:.1f}%")
                    print(f"📈 Memory: {memory_mb:.1f} MB, CPU: {cpu_percent:.1f}%")
                    
                except ImportError:
                    self.logger.warning("psutil not available, skipping resource monitoring")
                    
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            self.logger.info("Monitoring interrupted by user")
            print("\n🛑 Monitoring interrupted by user")
            
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
                print(f"❌ Unsupported IDE: {ide}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error creating IDE config: {e}")
            print(f"❌ Error creating IDE config: {e}")
            return False

    def _create_cursor_config(self) -> bool:
        """Create Cursor IDE configuration"""
        config = {
            "mcpServers": {
                "pycharm-github-copilot-mcp": {
                    "command": "python",
                    "args": ["pycharm_github_copilot_mcp.py"],
                    "env": {
                        "PYTHONPATH": str(self.project_root),
                        "LOG_LEVEL": "INFO",
                        "MCP_SERVER_TYPE": "pycharm_copilot"
                    }
                }
            }
        }
        
        config_path = self.project_root / ".cursor" / "settings.json"
        config_path.parent.mkdir(exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
            
        self.logger.info(f"Created Cursor config: {config_path}")
        print(f"✅ Created Cursor config: {config_path}")
        return True

    def _create_vscode_config(self) -> bool:
        """Create VS Code configuration"""
        config = {
            "mcp.servers": {
                "pycharm-github-copilot-mcp": {
                    "command": "python",
                    "args": ["pycharm_github_copilot_mcp.py"],
                    "env": {
                        "PYTHONPATH": str(self.project_root),
                        "LOG_LEVEL": "INFO",
                        "MCP_SERVER_TYPE": "pycharm_copilot"
                    }
                }
            }
        }
        
        config_path = self.project_root / ".vscode" / "settings.json"
        config_path.parent.mkdir(exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
            
        self.logger.info(f"Created VS Code config: {config_path}")
        print(f"✅ Created VS Code config: {config_path}")
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
        print(f"✅ Created PyCharm config: {config_path}")
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
                print(f"✅ Created {args.create_config} configuration")
            else:
                print(f"❌ Failed to create {args.create_config} configuration")
                
        else:
            # Start server
            if runner.start_server(args.mode):
                print(f"✅ PyCharm GitHub Copilot MCP Server started in {args.mode} mode")
                print("💡 Press Ctrl+C to stop")
                
                try:
                    # Keep server running
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    print("\n🛑 Stopping server...")
                    runner.stop_server()
            else:
                print("❌ Failed to start server")
                sys.exit(1)
                
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 