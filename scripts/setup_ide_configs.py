#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
IDE Configuration Setup Script
Automatically configures MCP server settings for Cursor, VS Code, and PyCharm
Supports Docker and uv integration
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
import shutil
import subprocess
import logging

class IDESetupManager:
    """Manages IDE configuration setup for MCP servers"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.logger = self._setup_logging()
        
        # IDE configurations
        self.ide_configs = {
            'cursor': {
                'config_file': 'cursor_mcp_config.json',
                'enabled': True
            },
            'vscode': {
                'config_dir': '.vscode',
                'config_file': 'settings.json',
                'enabled': True
            },
            'pycharm': {
                'config_file': 'pycharm_mcp_config.json',
                'enabled': True
            }
        }
        
        # Docker configuration
        self.docker_config = {
            'enabled': True,
            'container_name': 'neozork-mcp-server',
            'port': 8080,
            'volumes': [
                "${PROJECT_ROOT}:/workspace",
                "${PROJECT_ROOT}/logs:/workspace/logs"
            ],
            'environment': {
                'PYTHONPATH': '/workspace/src:/workspace',
                'LOG_LEVEL': 'INFO',
                'USE_UV': 'true'
            }
        }
        
        # UV configuration
        self.uv_config = {
            'enabled': True,
            'python_path': 'python3',
            'uv_path': 'uv',
            'auto_install': True
        }

    def _setup_logging(self) -> logging.Logger:
        """Setup logging"""
        log_dir = self.project_root / "logs"
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'ide_setup.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def check_docker_availability(self) -> bool:
        """Check if Docker is available"""
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True, check=True)
            self.logger.info(f"Docker available: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.warning("Docker not available")
            return False

    def check_uv_availability(self) -> bool:
        """Check if uv is available"""
        try:
            result = subprocess.run(['uv', '--version'], 
                                  capture_output=True, text=True, check=True)
            self.logger.info(f"UV available: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.warning("UV not available")
            return False

    def create_cursor_config(self) -> bool:
        """Create Cursor IDE configuration"""
        try:
            config_path = self.project_root / 'cursor_mcp_config.json'
            
            if config_path.exists():
                self.logger.info("Cursor config already exists, updating...")
            
            # Load existing config if available
            existing_config = {}
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    existing_config = json.load(f)
            
            # Update with latest settings
            config = self._get_cursor_config()
            config.update(existing_config)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Cursor config created/updated: {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create Cursor config: {e}")
            return False

    def create_vscode_config(self) -> bool:
        """Create VS Code configuration"""
        try:
            vscode_dir = self.project_root / '.vscode'
            vscode_dir.mkdir(exist_ok=True)
            
            config_path = vscode_dir / 'settings.json'
            
            if config_path.exists():
                self.logger.info("VS Code config already exists, updating...")
                with open(config_path, 'r', encoding='utf-8') as f:
                    existing_config = json.load(f)
            else:
                existing_config = {}
            
            # Update with latest settings
            config = self._get_vscode_config()
            config.update(existing_config)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"VS Code config created/updated: {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create VS Code config: {e}")
            return False

    def create_pycharm_config(self) -> bool:
        """Create PyCharm configuration"""
        try:
            config_path = self.project_root / 'pycharm_mcp_config.json'
            
            if config_path.exists():
                self.logger.info("PyCharm config already exists, updating...")
            
            # Load existing config if available
            existing_config = {}
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    existing_config = json.load(f)
            
            # Update with latest settings
            config = self._get_pycharm_config()
            config.update(existing_config)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"PyCharm config created/updated: {config_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create PyCharm config: {e}")
            return False

    def _get_cursor_config(self) -> Dict[str, Any]:
        """Get Cursor configuration"""
        return {
            "mcpServers": {
                "neozork": {
                    "command": "python3",
                    "args": ["neozork_mcp_server.py"],
                    "env": {
                        "PYTHONPATH": "${PROJECT_ROOT}",
                        "LOG_LEVEL": "INFO",
                        "DOCKER_CONTAINER": "false",
                        "USE_UV": "true",
                        "UV_PYTHON": "python3"
                    },
                    "cwd": "${PROJECT_ROOT}"
                },
                "neozork-docker": {
                    "command": "docker",
                    "args": [
                        "compose", "run", "--rm", "-T",
                        "-e", "PYTHONPATH=/app",
                        "-e", "LOG_LEVEL=INFO",
                        "-e", "DOCKER_CONTAINER=true",
                        "-e", "USE_UV=true",
                        "neozork-hld",
                        "python3", "neozork_mcp_server.py"
                    ],
                    "env": {
                        "DOCKER_HOST": "unix:///var/run/docker.sock"
                    },
                    "cwd": "${PROJECT_ROOT}"
                }
            },
            "serverSettings": {
                "neozork": {
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
                        "docker_integration": self.docker_config['enabled'],
                        "real_time_monitoring": True,
                        "uv_integration": self.uv_config['enabled']
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
                    "docker": self.docker_config,
                    "development": {
                        "auto_reload": False,
                        "hot_reload": False,
                        "debug_mode": False,
                        "profiling": False,
                        "coverage": False
                    }
                }
            },
            "cursor": {
                "mcp": {
                    "autoStart": True,
                    "logLevel": "info",
                    "features": {
                        "completion": True,
                        "hover": True,
                        "definition": True,
                        "references": True,
                        "workspaceSymbols": True,
                        "diagnostics": True,
                        "codeActions": True,
                        "formatting": True
                    },
                    "preferences": {
                        "defaultServer": "neozork",
                        "fallbackToDocker": self.docker_config['enabled'],
                        "useUV": self.uv_config['enabled'],
                        "dockerEnabled": self.docker_config['enabled']
                    }
                },
                "python": {
                    "interpreter": self.uv_config['python_path'],
                    "packageManager": "uv" if self.uv_config['enabled'] else "pip",
                    "uvPath": self.uv_config['uv_path'],
                    "autoInstallDependencies": self.uv_config['auto_install']
                }
            }
        }

    def _get_vscode_config(self) -> Dict[str, Any]:
        """Get VS Code configuration"""
        return {
            "mcp.servers": {
                "neozork": {
                    "command": "python3",
                    "args": ["neozork_mcp_server.py"],
                    "env": {
                        "PYTHONPATH": "${workspaceFolder}",
                        "LOG_LEVEL": "INFO",
                        "DOCKER_CONTAINER": "false",
                        "USE_UV": "true",
                        "UV_PYTHON": "python3"
                    },
                    "cwd": "${workspaceFolder}"
                },
                "neozork-docker": {
                    "command": "docker",
                    "args": [
                        "compose", "run", "--rm", "-T",
                        "-e", "PYTHONPATH=/app",
                        "-e", "LOG_LEVEL=INFO",
                        "-e", "DOCKER_CONTAINER=true",
                        "-e", "USE_UV=true",
                        "neozork-hld",
                        "python3", "neozork_mcp_server.py"
                    ],
                    "env": {
                        "DOCKER_HOST": "unix:///var/run/docker.sock"
                    },
                    "cwd": "${workspaceFolder}"
                }
            },
            "mcp.serverSettings": {
                "neozork": {
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
                        "docker_integration": self.docker_config['enabled'],
                        "real_time_monitoring": True,
                        "uv_integration": self.uv_config['enabled']
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
                    "docker": self.docker_config
                }
            },
            "python.defaultInterpreterPath": self.uv_config['python_path'],
            "python.packageManager": "uv" if self.uv_config['enabled'] else "pip",
            "python.terminal.activateEnvironment": True,
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": True,
            "python.formatting.provider": "black",
            "python.testing.pytestEnabled": True,
            "python.testing.pytestArgs": ["tests"],
            "files.associations": {
                "*.parquet": "csv",
                "*.json": "json"
            },
            "editor.suggest.snippetsPreventQuickSuggestions": False,
            "editor.tabCompletion": "on",
            "editor.quickSuggestions": {
                "other": True,
                "comments": True,
                "strings": True
            }
        }

    def _get_pycharm_config(self) -> Dict[str, Any]:
        """Get PyCharm configuration"""
        return {
            "mcpServers": {
                "neozork": {
                    "command": "python3",
                    "args": ["neozork_mcp_server.py"],
                    "env": {
                        "PYTHONPATH": "${PROJECT_ROOT}",
                        "LOG_LEVEL": "INFO",
                        "DOCKER_CONTAINER": "false",
                        "USE_UV": "true",
                        "UV_PYTHON": "python3"
                    },
                    "cwd": "${PROJECT_ROOT}"
                },
                "neozork-docker": {
                    "command": "docker",
                    "args": [
                        "compose", "run", "--rm", "-T",
                        "-e", "PYTHONPATH=/app",
                        "-e", "LOG_LEVEL=INFO",
                        "-e", "DOCKER_CONTAINER=true",
                        "-e", "USE_UV=true",
                        "neozork-hld",
                        "python3", "neozork_mcp_server.py"
                    ],
                    "env": {
                        "DOCKER_HOST": "unix:///var/run/docker.sock"
                    },
                    "cwd": "${PROJECT_ROOT}"
                }
            },
            "serverSettings": {
                "neozork": {
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
                        "docker_integration": self.docker_config['enabled'],
                        "real_time_monitoring": True,
                        "uv_integration": self.uv_config['enabled']
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
                    "docker": self.docker_config
                }
            },
            "pycharm": {
                "python": {
                    "interpreter": self.uv_config['python_path'],
                    "packageManager": "uv" if self.uv_config['enabled'] else "pip",
                    "uvPath": self.uv_config['uv_path'],
                    "autoInstallDependencies": self.uv_config['auto_install']
                },
                "mcp": {
                    "autoStart": True,
                    "logLevel": "info",
                    "features": {
                        "completion": True,
                        "hover": True,
                        "definition": True,
                        "references": True,
                        "workspaceSymbols": True,
                        "diagnostics": True
                    }
                }
            }
        }

    def setup_all_ides(self) -> Dict[str, bool]:
        """Setup all IDE configurations"""
        self.logger.info("Starting IDE configuration setup...")
        
        # Check system capabilities
        docker_available = self.check_docker_availability()
        uv_available = self.check_uv_availability()
        
        # Update configurations based on availability
        self.docker_config['enabled'] = docker_available
        self.uv_config['enabled'] = uv_available
        
        results = {}
        
        # Setup each IDE
        if self.ide_configs['cursor']['enabled']:
            results['cursor'] = self.create_cursor_config()
        
        if self.ide_configs['vscode']['enabled']:
            results['vscode'] = self.create_vscode_config()
        
        if self.ide_configs['pycharm']['enabled']:
            results['pycharm'] = self.create_pycharm_config()
        
        # Create summary
        self._create_setup_summary(results, docker_available, uv_available)
        
        return results

    def _create_setup_summary(self, results: Dict[str, bool], docker_available: bool, uv_available: bool):
        """Create setup summary"""
        summary = {
            "timestamp": str(Path().cwd()),
            "project_root": str(self.project_root),
            "system_capabilities": {
                "docker_available": docker_available,
                "uv_available": uv_available
            },
            "ide_setup_results": results,
            "configuration_files": {
                "cursor": str(self.project_root / 'cursor_mcp_config.json'),
                "vscode": str(self.project_root / '.vscode' / 'settings.json'),
                "pycharm": str(self.project_root / 'pycharm_mcp_config.json')
            }
        }
        
        summary_path = self.project_root / 'logs' / 'ide_setup_summary.json'
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Setup summary saved to: {summary_path}")

def main():
    """Main function"""
    project_root = Path(__file__).parent.parent
    
    print("🚀 Starting IDE Configuration Setup...")
    print(f"📁 Project root: {project_root}")
    
    setup_manager = IDESetupManager(project_root)
    results = setup_manager.setup_all_ides()
    
    print("\n✅ Setup Results:")
    for ide, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"   {ide.upper()}: {status}")
    
    print("\n📋 Next Steps:")
    print("   1. Restart your IDE to load new configurations")
    print("   2. Check logs/ide_setup_summary.json for details")
    print("   3. Test MCP server connection in your IDE")
    
    if all(results.values()):
        print("\n🎉 All IDE configurations setup successfully!")
        return 0
    else:
        print("\n⚠️  Some configurations failed. Check logs for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 