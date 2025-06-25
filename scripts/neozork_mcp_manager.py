#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Neozork MCP Manager
Unified management script for Neozork MCP Server (autostart, manual start, monitoring)
"""

import os
import sys
import json
import time
import signal
import subprocess
import psutil
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class NeozorkMCPManager:
    """Unified MCP server manager with autostart and monitoring capabilities"""
    
    def __init__(self, config_path: Optional[Path] = None, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.config_path = config_path or self.project_root / "neozork_mcp_config.json"
        self.logger = self._setup_logging()
        self.config = self._load_config()
        self.running_servers = {}
        self.observer = None
        self.running = True
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for MCP manager"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"neozork_mcp_manager_{time.strftime('%Y%m%d')}.log"
        
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [NeozorkMCPManager] %(message)s'
        )
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        logger = logging.getLogger('neozork_mcp_manager')
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)
        
        return logger
        
    def _load_config(self) -> Dict[str, Any]:
        """Load MCP configuration"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"Loaded config from {self.config_path}")
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
            "server": {
                "command": "python",
                "args": ["neozork_mcp_server.py"],
                "env": {
                    "PYTHONPATH": str(self.project_root),
                    "LOG_LEVEL": "INFO"
                },
                "cwd": str(self.project_root)
            },
            "conditions": {
                "cursor_ide": {
                    "processes": ["Cursor", "cursor", "Cursor.exe"],
                    "files": [".cursor", "cursor_mcp_config.json"]
                },
                "pycharm_ide": {
                    "processes": ["pycharm", "PyCharm", "idea", "pycharm64.exe"],
                    "files": [".idea", "pycharm_mcp_config.json"]
                },
                "vscode_ide": {
                    "processes": ["code", "Code", "code.exe"],
                    "files": [".vscode", ".vscode/settings.json"]
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
                        
                    # Check for VS Code IDE
                    if any(ide in proc_name for ide in self.config["conditions"]["vscode_ide"]["processes"]):
                        self.logger.info("Detected VS Code IDE")
                        return "vscode"
                        
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
        
    def should_start_server(self) -> bool:
        """Determine if server should be started"""
        if not self.config["auto_start"]["enabled"]:
            return False
            
        # Check if server is already running
        if "neozork_mcp" in self.running_servers:
            return False
            
        # Check conditions
        conditions = self.check_project_conditions()
        
        # Need at least Python files
        if not conditions.get("python_files", False):
            return False
            
        # Check if any IDE is detected
        ide_detected = any(
            conditions.get(ide, False) 
            for ide in ["cursor_ide", "pycharm_ide", "vscode_ide"]
        )
        
        return ide_detected
        
    def start_server(self, mode: str = "background") -> bool:
        """Start the MCP server"""
        try:
            server_config = self.config["server"]
            
            # Check if server file exists
            server_file = self.project_root / "neozork_mcp_server.py"
            if not server_file.exists():
                self.logger.error(f"Server file not found: {server_file}")
                print(f"❌ Server file not found: {server_file}")
                return False
            
            # Prepare environment
            env = os.environ.copy()
            env.update(server_config.get("env", {}))
            
            # Prepare command
            cmd = [server_config["command"]] + server_config["args"]
            
            self.logger.info(f"Starting Neozork MCP Server in {mode} mode")
            self.logger.info(f"Command: {' '.join(cmd)}")
            self.logger.info(f"Working directory: {server_config['cwd']}")
            
            print(f"🚀 Starting Neozork MCP Server in {mode} mode...")
            print(f"📁 Working directory: {server_config['cwd']}")
            print(f"🐍 Command: {' '.join(cmd)}")
            
            if mode == "stdio":
                # Start server in stdio mode for IDE integration
                process = subprocess.Popen(
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
                process = subprocess.Popen(
                    cmd,
                    cwd=server_config["cwd"],
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                # Start server in background mode
                process = subprocess.Popen(
                    cmd,
                    cwd=server_config["cwd"],
                    env=env,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
            # Wait a moment for server to start
            time.sleep(2)
            
            if process.poll() is None:
                self.running_servers["neozork_mcp"] = {
                    "process": process,
                    "start_time": time.time(),
                    "pid": process.pid,
                    "mode": mode
                }
                
                self.logger.info("Neozork MCP Server started successfully")
                print("✅ Neozork MCP Server started successfully")
                return True
            else:
                # Check for errors
                try:
                    stdout, stderr = process.communicate(timeout=2)
                except Exception:
                    stdout, stderr = '', ''
                self.logger.error(f"Failed to start Neozork MCP Server")
                self.logger.error(f"STDOUT: {stdout}")
                self.logger.error(f"STDERR: {stderr}")
                print("❌ Failed to start Neozork MCP Server")
                print(f"Error output: {stderr}")
                # Ensure server is not in running_servers
                if "neozork_mcp" in self.running_servers:
                    del self.running_servers["neozork_mcp"]
                return False
        
        except Exception as e:
            self.logger.error(f"Error starting server: {e}")
            print(f"❌ Error starting server: {e}")
            # Ensure server is not in running_servers
            if "neozork_mcp" in self.running_servers:
                del self.running_servers["neozork_mcp"]
            return False
            
    def stop_server(self) -> bool:
        """Stop the MCP server"""
        try:
            if "neozork_mcp" in self.running_servers:
                server_info = self.running_servers["neozork_mcp"]
                process = server_info["process"]
                
                if process.poll() is None:
                    self.logger.info("Stopping Neozork MCP Server")
                    print("🛑 Stopping Neozork MCP Server...")
                    process.terminate()
                    
                    # Wait for graceful shutdown
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        self.logger.warning("Server did not stop gracefully, forcing kill")
                        print("⚠️ Server did not stop gracefully, forcing kill...")
                        process.kill()
                        
                    self.logger.info("Neozork MCP Server stopped")
                    print("✅ Neozork MCP Server stopped")
                    
                del self.running_servers["neozork_mcp"]
                return True
            else:
                print("ℹ️ No server running")
                return True
                
        except Exception as e:
            self.logger.error(f"Error stopping server: {e}")
            print(f"❌ Error stopping server: {e}")
            return False
            
    def check_server_health(self) -> None:
        """Check health of running servers"""
        for server_name, server_info in list(self.running_servers.items()):
            process = server_info["process"]
            
            if process.poll() is not None:
                self.logger.warning(f"Server {server_name} has stopped")
                print(f"⚠️ Server {server_name} has stopped")
                del self.running_servers[server_name]
                
    def monitor_project_changes(self) -> None:
        """Monitor project changes and restart servers if needed"""
        class ProjectChangeHandler(FileSystemEventHandler):
            def __init__(self, manager):
                self.manager = manager
                
            def on_created(self, event):
                if not event.is_directory:
                    self.manager.handle_file_change("created", event.src_path)
                    
            def on_modified(self, event):
                if not event.is_directory:
                    self.manager.handle_file_change("modified", event.src_path)
                    
            def on_deleted(self, event):
                if not event.is_directory:
                    self.manager.handle_file_change("deleted", event.src_path)
        
        if self.observer is None:
            self.observer = Observer()
            self.observer.schedule(
                ProjectChangeHandler(self),
                str(self.project_root),
                recursive=True
            )
            self.observer.start()
            
    def handle_file_change(self, change_type: str, file_path: str) -> None:
        """Handle file change events"""
        try:
            # Only react to Python file changes
            if file_path.endswith('.py'):
                self.logger.info(f"File {change_type}: {file_path}")
                
                # Re-evaluate server conditions
                if self.should_start_server():
                    if "neozork_mcp" not in self.running_servers:
                        self.start_server()
                else:
                    if "neozork_mcp" in self.running_servers:
                        self.stop_server()
                        
        except Exception as e:
            self.logger.error(f"Error handling file change: {e}")
            
    def evaluate_servers(self) -> None:
        """Evaluate and manage servers based on conditions"""
        try:
            # Check if server should be running
            if self.should_start_server():
                if "neozork_mcp" not in self.running_servers:
                    self.logger.info("Conditions met, starting server")
                    self.start_server()
            else:
                if "neozork_mcp" in self.running_servers:
                    self.logger.info("Conditions not met, stopping server")
                    self.stop_server()
                    
        except Exception as e:
            self.logger.error(f"Error evaluating servers: {e}")
            
    def run(self) -> None:
        """Run the MCP manager"""
        print("🔄 Starting Neozork MCP Manager...")
        print(f"📁 Project root: {self.project_root}")
        print(f"⚙️ Auto-start enabled: {self.config['auto_start']['enabled']}")
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        try:
            # Start file monitoring
            self.monitor_project_changes()
            
            # Initial evaluation
            self.evaluate_servers()
            
            # Main loop
            while self.running:
                try:
                    # Check server health
                    self.check_server_health()
                    
                    # Evaluate servers
                    self.evaluate_servers()
                    
                    # Sleep
                    time.sleep(self.config["auto_start"]["check_interval"])
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    self.logger.error(f"Error in main loop: {e}")
                    time.sleep(5)
                    
        except Exception as e:
            self.logger.error(f"Error running manager: {e}")
            print(f"❌ Error running manager: {e}")
        finally:
            self.cleanup()
            
    def _signal_handler(self, sig, frame):
        """Handle shutdown signals"""
        print(f"🛑 Received signal {sig}")
        self.running = False
        
    def cleanup(self) -> None:
        """Cleanup resources"""
        print("🧹 Cleaning up...")
        
        # Stop file monitoring
        if self.observer:
            self.observer.stop()
            self.observer.join()
            
        # Stop all servers
        for server_name in list(self.running_servers.keys()):
            self.stop_server()
            
        self.logger.info("Manager shutdown complete")
        print("✅ Manager shutdown complete")
        
    def get_status(self) -> Dict[str, Any]:
        """Get status of all servers"""
        status = {
            "manager_running": self.running,
            "auto_start_enabled": self.config["auto_start"]["enabled"],
            "servers": {}
        }
        
        for server_name, server_info in self.running_servers.items():
            process = server_info["process"]
            status["servers"][server_name] = {
                "running": process.poll() is None,
                "pid": server_info["pid"],
                "start_time": server_info["start_time"],
                "mode": server_info["mode"],
                "uptime": time.time() - server_info["start_time"] if process.poll() is None else 0
            }
            
        return status
        
    def create_ide_config(self, ide: str) -> bool:
        """Create IDE configuration for MCP server"""
        try:
            if ide == "cursor":
                return self._create_cursor_config()
            elif ide == "pycharm":
                return self._create_pycharm_config()
            elif ide == "vscode":
                return self._create_vscode_config()
            else:
                print(f"❌ Unsupported IDE: {ide}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error creating IDE config: {e}")
            return False
            
    def _create_cursor_config(self) -> bool:
        """Create Cursor IDE configuration"""
        try:
            cursor_dir = self.project_root / ".cursor"
            cursor_dir.mkdir(exist_ok=True)
            
            config_file = cursor_dir / "settings.json"
            config = {
                "mcpServers": {
                    "neozork-mcp": {
                        "command": "python",
                        "args": ["neozork_mcp_server.py"],
                        "cwd": str(self.project_root),
                        "env": {
                            "PYTHONPATH": f"{self.project_root}/src:{self.project_root}",
                            "LOG_LEVEL": "INFO"
                        }
                    }
                }
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
                
            print(f"✅ Created Cursor config: {config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating Cursor config: {e}")
            return False
            
    def _create_pycharm_config(self) -> bool:
        """Create PyCharm IDE configuration"""
        try:
            idea_dir = self.project_root / ".idea"
            idea_dir.mkdir(exist_ok=True)
            
            config_file = idea_dir / "mcp_servers.xml"
            config = f"""<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="MCPProjectSettings">
    <option name="mcpServers">
      <map>
        <entry key="neozork-mcp">
          <value>
            <MCPProjectSettings.MCPServer>
              <option name="command" value="python" />
              <option name="args" value="neozork_mcp_server.py" />
              <option name="cwd" value="{self.project_root}" />
              <option name="env">
                <map>
                  <entry key="PYTHONPATH" value="{self.project_root}/src:{self.project_root}" />
                  <entry key="LOG_LEVEL" value="INFO" />
                </map>
              </option>
            </MCPProjectSettings.MCPServer>
          </value>
        </entry>
      </map>
    </option>
  </component>
</project>"""
            
            with open(config_file, 'w', encoding='utf-8') as f:
                f.write(config)
                
            print(f"✅ Created PyCharm config: {config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating PyCharm config: {e}")
            return False
            
    def _create_vscode_config(self) -> bool:
        """Create VS Code IDE configuration"""
        try:
            vscode_dir = self.project_root / ".vscode"
            vscode_dir.mkdir(exist_ok=True)
            
            config_file = vscode_dir / "settings.json"
            config = {
                "mcp.servers": {
                    "neozork-mcp": {
                        "command": "python",
                        "args": ["neozork_mcp_server.py"],
                        "cwd": str(self.project_root),
                        "env": {
                            "PYTHONPATH": f"{self.project_root}/src:{self.project_root}",
                            "LOG_LEVEL": "INFO"
                        }
                    }
                }
            }
            
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
                
            print(f"✅ Created VS Code config: {config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating VS Code config: {e}")
            return False

class NeozorkMCPManagerCLI:
    """CLI interface for Neozork MCP Manager"""
    
    def __init__(self):
        self.manager = None
        
    def start(self) -> None:
        """Start the MCP manager in auto-start mode"""
        print("🚀 Starting Neozork MCP Manager in auto-start mode...")
        self.manager = NeozorkMCPManager()
        self.manager.run()
        
    def status(self) -> None:
        """Show status of MCP servers"""
        manager = NeozorkMCPManager()
        status = manager.get_status()
        
        print("📊 Neozork MCP Manager Status")
        print("=" * 40)
        print(f"Manager running: {status['manager_running']}")
        print(f"Auto-start enabled: {status['auto_start_enabled']}")
        print()
        
        if status['servers']:
            print("🟢 Running Servers:")
            for server_name, server_info in status['servers'].items():
                if server_info['running']:
                    uptime = server_info['uptime']
                    hours = int(uptime // 3600)
                    minutes = int((uptime % 3600) // 60)
                    print(f"  • {server_name} (PID: {server_info['pid']}, Mode: {server_info['mode']}, Uptime: {hours}h {minutes}m)")
                else:
                    print(f"  • {server_name} (stopped)")
        else:
            print("🔴 No servers running")
            
        # Check conditions
        conditions = manager.check_project_conditions()
        print()
        print("📋 Project Conditions:")
        for condition, met in conditions.items():
            status_icon = "✅" if met else "❌"
            print(f"  {status_icon} {condition}: {met}")
            
        # Check IDE detection
        ide = manager.detect_ide()
        if ide:
            print(f"🖥️  Detected IDE: {ide}")
        else:
            print("🖥️  No IDE detected")
            
    def stop(self) -> None:
        """Stop all MCP servers"""
        print("🛑 Stopping all MCP servers...")
        manager = NeozorkMCPManager()
        manager.stop_server()
        print("✅ All servers stopped")
        
    def restart(self) -> None:
        """Restart all MCP servers"""
        print("🔄 Restarting MCP servers...")
        manager = NeozorkMCPManager()
        manager.stop_server()
        time.sleep(2)
        manager.start_server()
        print("✅ Servers restarted")
        
    def manual_start(self, mode: str = "background") -> None:
        """Manually start MCP server"""
        print(f"🚀 Manually starting MCP server in {mode} mode...")
        manager = NeozorkMCPManager()
        if manager.start_server(mode):
            print("✅ Server started successfully")
        else:
            print("❌ Failed to start server")
            
    def create_config(self, ide: str) -> None:
        """Create IDE configuration"""
        print(f"⚙️ Creating {ide} configuration...")
        manager = NeozorkMCPManager()
        if manager.create_ide_config(ide):
            print(f"✅ {ide} configuration created")
        else:
            print(f"❌ Failed to create {ide} configuration")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Neozork MCP Manager - Unified MCP server management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start auto-start mode
  python scripts/neozork_mcp_manager.py start

  # Show status
  python scripts/neozork_mcp_manager.py status

  # Manually start server
  python scripts/neozork_mcp_manager.py start-server

  # Start in stdio mode (for IDE integration)
  python scripts/neozork_mcp_manager.py start-server --mode stdio

  # Stop all servers
  python scripts/neozork_mcp_manager.py stop

  # Restart servers
  python scripts/neozork_mcp_manager.py restart

  # Create IDE configuration
  python scripts/neozork_mcp_manager.py create-config cursor
  python scripts/neozork_mcp_manager.py create-config pycharm
  python scripts/neozork_mcp_manager.py create-config vscode
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start auto-start mode')
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show server status')
    
    # Stop command
    stop_parser = subparsers.add_parser('stop', help='Stop all servers')
    
    # Restart command
    restart_parser = subparsers.add_parser('restart', help='Restart all servers')
    
    # Start server command
    start_server_parser = subparsers.add_parser('start-server', help='Manually start server')
    start_server_parser.add_argument(
        '--mode', '-m',
        choices=['background', 'stdio', 'test'],
        default='background',
        help='Server mode (default: background)'
    )
    
    # Create config command
    create_config_parser = subparsers.add_parser('create-config', help='Create IDE configuration')
    create_config_parser.add_argument(
        'ide',
        choices=['cursor', 'pycharm', 'vscode'],
        help='IDE to create configuration for'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
        
    cli = NeozorkMCPManagerCLI()
    
    try:
        if args.command == 'start':
            cli.start()
        elif args.command == 'status':
            cli.status()
        elif args.command == 'stop':
            cli.stop()
        elif args.command == 'restart':
            cli.restart()
        elif args.command == 'start-server':
            cli.manual_start(args.mode)
        elif args.command == 'create-config':
            cli.create_config(args.ide)
        else:
            parser.print_help()
            
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 