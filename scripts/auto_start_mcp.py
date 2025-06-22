#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Auto Start MCP Server
Automatically starts MCP servers based on project conditions and IDE detection
"""

import os
import sys
import json
import time
import signal
import subprocess
import psutil
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class MCPAutoStarter:
    """Automatic MCP server starter with intelligent detection"""
    
    def __init__(self):
        self.project_root = project_root
        self.logger = self._setup_logging()
        self.running_servers = {}
        self.config = self._load_config()
        self.observer = None
        self.running = True
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for auto starter"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"mcp_auto_starter_{time.strftime('%Y%m%d')}.log"
        
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [MCPAutoStarter] %(message)s'
        )
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        logger = logging.getLogger('mcp_auto_starter')
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        
        return logger
        
    def _load_config(self) -> Dict[str, Any]:
        """Load auto-start configuration"""
        config_path = self.project_root / "mcp_auto_config.json"
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"Loaded auto-start config from {config_path}")
                return config
            except Exception as e:
                self.logger.error(f"Error loading config: {e}")
                
        # Default configuration
        return {
            "auto_start": {
                "enabled": True,
                "check_interval": 30,
                "ide_detection": True,
                "project_detection": True
            },
            "servers": {
                "cursor": {
                    "enabled": True,
                    "command": "python",
                    "args": ["cursor_mcp_server.py"],
                    "conditions": ["cursor_ide", "python_files"],
                    "env": {
                        "PYTHONPATH": str(self.project_root),
                        "LOG_LEVEL": "INFO"
                    }
                },
                "pycharm": {
                    "enabled": True,
                    "command": "python",
                    "args": ["pycharm_github_copilot_mcp.py"],
                    "conditions": ["pycharm_ide", "python_files"],
                    "env": {
                        "PYTHONPATH": str(self.project_root),
                        "LOG_LEVEL": "INFO"
                    }
                }
            },
            "conditions": {
                "cursor_ide": {
                    "processes": ["Cursor", "cursor"],
                    "files": [".cursor", "cursor_mcp_config.json"]
                },
                "pycharm_ide": {
                    "processes": ["pycharm", "PyCharm", "idea"],
                    "files": [".idea", "pycharm_mcp_config.json"]
                },
                "python_files": {
                    "extensions": [".py"],
                    "min_files": 1
                },
                "financial_data": {
                    "directories": ["mql5_feed", "data"],
                    "files": ["*.csv", "*.parquet"]
                }
            }
        }
        
    def detect_ide(self) -> Optional[str]:
        """Detect running IDE"""
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    proc_info = proc.info
                    proc_name = proc_info['name'].lower()
                    
                    # Check for Cursor IDE
                    if any(ide in proc_name for ide in self.config["conditions"]["cursor_ide"]["processes"]):
                        self.logger.info("Detected Cursor IDE")
                        return "cursor"
                        
                    # Check for PyCharm IDE
                    if any(ide in proc_name for ide in self.config["conditions"]["pycharm_ide"]["processes"]):
                        self.logger.info("Detected PyCharm IDE")
                        return "pycharm"
                        
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
            return None
            
        except Exception as e:
            self.logger.error(f"Error detecting IDE: {e}")
            return None
            
    def check_project_conditions(self) -> Dict[str, bool]:
        """Check project conditions"""
        conditions = {}
        
        try:
            # Check for Python files
            python_files = list(self.project_root.rglob("*.py"))
            conditions["python_files"] = len(python_files) >= self.config["conditions"]["python_files"]["min_files"]
            
            # Check for financial data
            financial_data_found = False
            for directory in self.config["conditions"]["financial_data"]["directories"]:
                if (self.project_root / directory).exists():
                    financial_data_found = True
                    break
            conditions["financial_data"] = financial_data_found
            
            # Check for IDE-specific files
            for ide, ide_config in self.config["conditions"].items():
                if ide.endswith("_ide"):
                    for file_pattern in ide_config["files"]:
                        if (self.project_root / file_pattern).exists():
                            conditions[ide] = True
                            break
                    else:
                        conditions[ide] = False
                        
        except Exception as e:
            self.logger.error(f"Error checking project conditions: {e}")
            
        return conditions
        
    def should_start_server(self, server_name: str) -> bool:
        """Determine if server should be started"""
        if not self.config["auto_start"]["enabled"]:
            return False
            
        server_config = self.config["servers"].get(server_name)
        if not server_config or not server_config.get("enabled", False):
            return False
            
        # Check if server is already running
        if server_name in self.running_servers:
            return False
            
        # Check conditions
        conditions = self.check_project_conditions()
        required_conditions = server_config.get("conditions", [])
        
        for condition in required_conditions:
            if not conditions.get(condition, False):
                self.logger.debug(f"Condition not met for {server_name}: {condition}")
                return False
                
        self.logger.info(f"All conditions met for {server_name}")
        return True
        
    def start_server(self, server_name: str) -> bool:
        """Start MCP server"""
        try:
            server_config = self.config["servers"][server_name]
            
            # Prepare environment
            env = os.environ.copy()
            env.update(server_config.get("env", {}))
            
            # Prepare command
            cmd = [server_config["command"]] + server_config["args"]
            
            self.logger.info(f"Starting {server_name} MCP server")
            self.logger.debug(f"Command: {' '.join(cmd)}")
            
            # Start server process
            process = subprocess.Popen(
                cmd,
                cwd=self.project_root,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a moment to check if it started successfully
            time.sleep(2)
            
            if process.poll() is None:
                self.running_servers[server_name] = {
                    "process": process,
                    "start_time": time.time(),
                    "pid": process.pid
                }
                self.logger.info(f"{server_name} MCP server started successfully (PID: {process.pid})")
                return True
            else:
                self.logger.error(f"Failed to start {server_name} MCP server")
                return False
                
        except Exception as e:
            self.logger.error(f"Error starting {server_name} server: {e}")
            return False
            
    def stop_server(self, server_name: str) -> bool:
        """Stop MCP server"""
        try:
            if server_name in self.running_servers:
                server_info = self.running_servers[server_name]
                process = server_info["process"]
                
                self.logger.info(f"Stopping {server_name} MCP server")
                process.terminate()
                
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    self.logger.warning(f"{server_name} server did not stop gracefully, forcing kill")
                    process.kill()
                    
                del self.running_servers[server_name]
                self.logger.info(f"{server_name} MCP server stopped")
                return True
            else:
                self.logger.debug(f"{server_name} server is not running")
                return True
                
        except Exception as e:
            self.logger.error(f"Error stopping {server_name} server: {e}")
            return False
            
    def check_server_health(self) -> None:
        """Check health of running servers"""
        for server_name, server_info in list(self.running_servers.items()):
            process = server_info["process"]
            
            if process.poll() is not None:
                self.logger.warning(f"{server_name} server process terminated unexpectedly")
                del self.running_servers[server_name]
                
                # Restart if conditions are still met
                if self.should_start_server(server_name):
                    self.logger.info(f"Restarting {server_name} server")
                    self.start_server(server_name)
                    
    def monitor_project_changes(self) -> None:
        """Monitor project file changes"""
        class ProjectChangeHandler(FileSystemEventHandler):
            def __init__(self, auto_starter):
                self.auto_starter = auto_starter
                
            def on_created(self, event):
                if not event.is_directory:
                    self.auto_starter.handle_file_change("created", event.src_path)
                    
            def on_modified(self, event):
                if not event.is_directory:
                    self.auto_starter.handle_file_change("modified", event.src_path)
                    
            def on_deleted(self, event):
                if not event.is_directory:
                    self.auto_starter.handle_file_change("deleted", event.src_path)
                    
        event_handler = ProjectChangeHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.project_root), recursive=True)
        self.observer.start()
        
    def handle_file_change(self, change_type: str, file_path: str) -> None:
        """Handle file system changes"""
        try:
            file_path = Path(file_path)
            relative_path = file_path.relative_to(self.project_root)
            
            # Check if change affects server conditions
            if file_path.suffix == '.py' or file_path.name in ['cursor_mcp_config.json', 'pycharm_mcp_config.json']:
                self.logger.debug(f"Project file {change_type}: {relative_path}")
                
                # Re-evaluate server conditions
                self.evaluate_servers()
                
        except Exception as e:
            self.logger.error(f"Error handling file change: {e}")
            
    def evaluate_servers(self) -> None:
        """Evaluate which servers should be running"""
        try:
            # Check each server
            for server_name in self.config["servers"]:
                if self.should_start_server(server_name):
                    if server_name not in self.running_servers:
                        self.start_server(server_name)
                else:
                    if server_name in self.running_servers:
                        self.stop_server(server_name)
                        
        except Exception as e:
            self.logger.error(f"Error evaluating servers: {e}")
            
    def run(self) -> None:
        """Main run loop"""
        self.logger.info("Starting MCP Auto Starter")
        
        # Start file monitoring
        if self.config["auto_start"].get("project_detection", True):
            self.monitor_project_changes()
            
        try:
            while self.running:
                # Check server health
                self.check_server_health()
                
                # Evaluate servers
                self.evaluate_servers()
                
                # Log status
                if self.running_servers:
                    server_names = list(self.running_servers.keys())
                    self.logger.info(f"Running servers: {', '.join(server_names)}")
                else:
                    self.logger.debug("No servers currently running")
                    
                # Wait for next check
                time.sleep(self.config["auto_start"].get("check_interval", 30))
                
        except KeyboardInterrupt:
            self.logger.info("Received shutdown signal")
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
        finally:
            self.cleanup()
            
    def cleanup(self) -> None:
        """Cleanup resources"""
        self.logger.info("Cleaning up MCP Auto Starter")
        
        # Stop all servers
        for server_name in list(self.running_servers.keys()):
            self.stop_server(server_name)
            
        # Stop file monitoring
        if self.observer:
            self.observer.stop()
            self.observer.join()
            
        self.logger.info("MCP Auto Starter stopped")
        
    def get_status(self) -> Dict[str, Any]:
        """Get current status"""
        status = {
            "running": self.running,
            "servers": {},
            "conditions": self.check_project_conditions(),
            "ide_detected": self.detect_ide()
        }
        
        for server_name, server_info in self.running_servers.items():
            process = server_info["process"]
            status["servers"][server_name] = {
                "running": process.poll() is None,
                "pid": server_info["pid"],
                "uptime": time.time() - server_info["start_time"]
            }
            
        return status

class MCPAutoStarterCLI:
    """Command-line interface for MCP Auto Starter"""
    
    def __init__(self):
        self.auto_starter = MCPAutoStarter()
        
    def start(self) -> None:
        """Start the auto starter"""
        print("🚀 Starting MCP Auto Starter...")
        print(f"📁 Project root: {self.auto_starter.project_root}")
        print("📋 Configuration loaded")
        
        # Show initial status
        status = self.auto_starter.get_status()
        print(f"🔍 IDE detected: {status['ide_detected'] or 'None'}")
        print(f"📊 Project conditions: {status['conditions']}")
        
        # Start the auto starter
        self.auto_starter.run()
        
    def status(self) -> None:
        """Show current status"""
        status = self.auto_starter.get_status()
        
        print("=" * 60)
        print("MCP Auto Starter Status")
        print("=" * 60)
        
        print(f"Running: {status['running']}")
        print(f"IDE Detected: {status['ide_detected'] or 'None'}")
        
        print("\nProject Conditions:")
        for condition, met in status['conditions'].items():
            status_icon = "✅" if met else "❌"
            print(f"  {status_icon} {condition}")
            
        print("\nRunning Servers:")
        if status['servers']:
            for server_name, server_status in status['servers'].items():
                status_icon = "🟢" if server_status['running'] else "🔴"
                uptime = int(server_status['uptime'])
                print(f"  {status_icon} {server_name} (PID: {server_status['pid']}, Uptime: {uptime}s)")
        else:
            print("  No servers running")
            
        print("=" * 60)
        
    def stop(self) -> None:
        """Stop the auto starter"""
        print("🛑 Stopping MCP Auto Starter...")
        self.auto_starter.running = False
        self.auto_starter.cleanup()
        print("✅ MCP Auto Starter stopped")
        
    def restart(self) -> None:
        """Restart all servers"""
        print("🔄 Restarting all MCP servers...")
        
        # Stop all servers
        for server_name in list(self.auto_starter.running_servers.keys()):
            self.auto_starter.stop_server(server_name)
            
        # Re-evaluate and start servers
        self.auto_starter.evaluate_servers()
        
        status = self.auto_starter.get_status()
        running_count = len([s for s in status['servers'].values() if s['running']])
        print(f"✅ Restarted {running_count} servers")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Auto Starter")
    parser.add_argument("command", choices=["start", "status", "stop", "restart"], 
                       help="Command to execute")
    parser.add_argument("--config", type=Path, help="Configuration file path")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    
    args = parser.parse_args()
    
    cli = MCPAutoStarterCLI()
    
    try:
        if args.command == "start":
            if args.daemon:
                # Run as daemon
                import daemon
                with daemon.DaemonContext():
                    cli.start()
            else:
                cli.start()
        elif args.command == "status":
            cli.status()
        elif args.command == "stop":
            cli.stop()
        elif args.command == "restart":
            cli.restart()
            
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted by user")
        cli.stop()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 