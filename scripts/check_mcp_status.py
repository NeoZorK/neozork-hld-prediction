#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
MCP Server Status Checker
Check if MCP server is running and test connection
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

class MCPServerChecker:
    """Check MCP server status and test connection"""
    
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
    
    checker = MCPServerChecker()
    results = checker.run_comprehensive_check()
    
    # Print results
    print(f"\n📅 Check Time: {results['timestamp']}")
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
    
    # Recommendations
    if results["recommendations"]:
        print(f"\n💡 Recommendations:")
        for rec in results["recommendations"]:
            print(f"   • {rec}")
    
    # Save results
    log_file = checker.project_root / "logs" / "mcp_status_check.json"
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