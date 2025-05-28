# -*- coding: utf-8 -*-
# mcp_server.py
"""
MCP Server for NeoZorK HLD Prediction Project
Provides context about the project structure and code to GitHub Copilot
"""

import os
import sys
import json
import asyncio
import logging
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# fixed path for src directory
project_root = os.environ.get("PROJECT_ROOT", ".")
src_path = os.path.join(os.path.abspath(project_root), 'src')
if os.path.exists(src_path):
    sys.path.insert(0, src_path)

# Set a timeout for MCP responses
MCP_RESPONSE_TIMEOUT = 30  # seconds - timeout increased from 10 to 30 seconds

@dataclass
class ProjectStructure:
    """Project structure information for context"""
    root_path: Path
    python_files: List[Path]
    modules: Dict[str, List[str]]
    dependencies: List[str]


class MCPServer:
    """Model Context Protocol Server for project analysis"""

    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.logger = self._setup_logging()
        self.structure = self._analyze_project_structure()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger('mcp_server')

    def _analyze_project_structure(self) -> ProjectStructure:
        """Analyze project structure and dependencies"""
        python_files = []
        modules = {}

        # Find all Python files
        for py_file in self.project_root.rglob("*.py"):
            if not any(part.startswith('.') or part == '__pycache__' for part in py_file.parts):
                python_files.append(py_file)

        # Organize by modules
        src_path = self.project_root / "src"
        if src_path.exists():
            for module_dir in src_path.iterdir():
                if module_dir.is_dir() and not module_dir.name.startswith('.'):
                    module_files = [
                        f.name for f in module_dir.rglob("*.py")
                        if not f.name.startswith('__')
                    ]
                    modules[module_dir.name] = module_files

        # Read dependencies
        dependencies = []
        requirements_file = self.project_root / "requirements.txt"
        if requirements_file.exists():
            with open(requirements_file, 'r', encoding='utf-8') as f:
                dependencies = [
                    line.strip() for line in f.readlines()
                    if line.strip() and not line.startswith('#')
                ]

        return ProjectStructure(
            root_path=self.project_root,
            python_files=python_files,
            modules=modules,
            dependencies=dependencies
        )

    def get_project_context(self) -> Dict[str, Any]:
        """Get comprehensive project context for Copilot"""
        return {
            "project_name": "NeoZorK HLD Prediction",
            "description": "High Low Prediction for Time Series Financial rates",
            "language": "Python",
            "coding_style": "snake_case",
            "comment_language": "English",
            "project_type": "Financial Time Series Prediction",
            "main_technologies": [
                "TensorFlow", "Keras", "LightGBM", "XGBoost",
                "Pandas", "NumPy", "Matplotlib", "Plotly",
                "yfinance", "python-binance", "backtrader"
            ],
            "modules": {
                "calculation": "Core calculation algorithms for predictions",
                "cli": "Command line interface components",
                "common": "Common utilities and shared functions",
                "data": "Data processing and handling modules",
                "eda": "Exploratory Data Analysis components",
                "plotting": "Visualization and plotting utilities",
                "utils": "General utility functions",
                "workflow": "Workflow management and orchestration"
            },
            "file_structure": self._get_file_structure(),
            "dependencies": self.structure.dependencies[:20],  # Top 20 dependencies
            "code_patterns": {
                "imports": "Standard library first, third-party, then local imports",
                "functions": "snake_case naming convention",
                "classes": "PascalCase naming convention",
                "constants": "UPPER_CASE naming convention",
                "comments": "English language, docstrings for all functions/classes"
            }
        }

    def _get_file_structure(self) -> Dict[str, Any]:
        """Get detailed file structure"""
        structure = {}

        for module_name, files in self.structure.modules.items():
            structure[f"src/{module_name}"] = {
                "type": "module",
                "files": files,
                "description": self._get_module_description(module_name)
            }

        # Add root level files
        root_files = [
            f.name for f in self.project_root.iterdir()
            if f.is_file() and f.suffix in ['.py', '.md', '.txt', '.json']
        ]
        structure["root"] = {
            "type": "root",
            "files": root_files,
            "description": "Root level configuration and entry points"
        }

        return structure

    def _get_module_description(self, module_name: str) -> str:
        """Get description for specific module"""
        descriptions = {
            "calculation": "Financial calculations, indicators, and prediction algorithms",
            "cli": "Command line interface for running analysis and predictions",
            "common": "Shared utilities, constants, and common functionality",
            "data": "Data fetching, preprocessing, and feature engineering",
            "eda": "Exploratory data analysis, statistics, and insights",
            "plotting": "Charts, graphs, and financial visualizations",
            "utils": "Helper functions, file I/O, and general utilities",
            "workflow": "Pipeline orchestration and workflow management"
        }
        return descriptions.get(module_name, f"Module: {module_name}")

    def get_file_content(self, file_path: str) -> Optional[str]:
        """Get content of specific file"""
        try:
            full_path = self.project_root / file_path
            if full_path.exists() and full_path.suffix in ['.py', '.md', '.txt', '.json', '.yaml', '.yml']:
                with open(full_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
        return None

    def get_module_files(self, module_name: str) -> List[Dict[str, str]]:
        """Get all files in a specific module with their content"""
        files_info = []
        module_path = self.project_root / "src" / module_name

        if module_path.exists():
            for py_file in module_path.rglob("*.py"):
                relative_path = py_file.relative_to(self.project_root)
                content = self.get_file_content(str(relative_path))
                if content:
                    files_info.append({
                        "path": str(relative_path),
                        "name": py_file.name,
                        "content": content[:1000] + "..." if len(content) > 1000 else content,
                        "full_content_available": True
                    })

        return files_info

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP requests"""
        try:
            self.logger.info(f"Received request: {request.get('method', 'unknown')}")
            method = request.get("method", "")
            params = request.get("params", {})

            if method == "initialize":
                self.logger.info("Processing initialize request")
                return {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "resources": {"subscribe": True, "listChanged": True},
                        "tools": {"listChanged": True},
                        "prompts": {"listChanged": True}
                    },
                    "serverInfo": {
                        "name": "NeoZorK HLD Prediction MCP Server",
                        "version": "1.0.0"
                    }
                }

            elif method == "resources/list":
                self.logger.info("Processing resources/list request")
                return {
                    "resources": [
                        {
                            "uri": f"file://{self.project_root}/context",
                            "name": "Project Context",
                            "description": "Complete project structure and context",
                            "mimeType": "application/json"
                        },
                        {
                            "uri": f"file://{self.project_root}/modules",
                            "name": "Module Information",
                            "description": "Detailed module structure and files",
                            "mimeType": "application/json"
                        }
                    ]
                }

            elif method == "resources/read":
                uri = params.get("uri", "")
                self.logger.info(f"Processing resources/read request for {uri}")
                try:
                    if "context" in uri:
                        context = self.get_project_context()
                        self.logger.info(f"Returning project context (size: {len(json.dumps(context))} bytes)")
                        return {
                            "contents": [{
                                "uri": uri,
                                "mimeType": "application/json",
                                "text": json.dumps(context, indent=2)
                            }]
                        }
                    elif "modules" in uri:
                        modules_info = {}
                        for module_name in self.structure.modules.keys():
                            self.logger.info(f"Processing module: {module_name}")
                            modules_info[module_name] = self.get_module_files(module_name)

                        self.logger.info(f"Returning modules info (size: {len(json.dumps(modules_info))} bytes)")
                        return {
                            "contents": [{
                                "uri": uri,
                                "mimeType": "application/json",
                                "text": json.dumps(modules_info, indent=2)
                            }]
                        }
                except Exception as e:
                    self.logger.error(f"Error processing resources/read: {e}")
                    self.logger.error(traceback.format_exc())
                    return {"error": f"Failed to read resource: {str(e)}"}

            self.logger.warning(f"Unknown method: {method}")
            return {"error": f"Unknown method: {method}"}
        except Exception as e:
            self.logger.error(f"Error handling request: {str(e)}")
            self.logger.error(traceback.format_exc())
            return {"error": str(e)}

def main():
    """Main entry point for MCP server"""
    # Use environment variables or default to current directory
    project_root = os.environ.get("PROJECT_ROOT", ".")
    server = MCPServer(project_root)

    # For debugging, print project context
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        context = server.get_project_context()
        print(json.dumps(context, indent=2, default=str))
        return

    # Start MCP server
    print("Starting NeoZorK HLD Prediction MCP Server...", file=sys.stderr)
    server.logger.info("MCP Server initialized successfully")
    server.logger.info(f"Using project root: {server.project_root}")

    # Simple STDIO-based MCP server with improved error handling
    try:
        # Setup a basic STDIO server
        print("MCP Server ready to accept requests", file=sys.stderr)

        while True:
            try:
                # Using sys.stdin to read input lines
                line = sys.stdin.readline()
                if not line:
                    server.logger.warning("Empty input received, continuing...")
                    continue

                if line.strip():
                    try:
                        server.logger.info("Processing input line")
                        request = json.loads(line)
                        # Use asyncio to handle requests with timeout
                        async def process_with_timeout():
                            return await asyncio.wait_for(
                                server.handle_request(request),
                                timeout=MCP_RESPONSE_TIMEOUT
                            )

                        response = asyncio.run(process_with_timeout())
                        print(json.dumps(response), flush=True)
                        server.logger.info(f"Response sent for method: {request.get('method', 'unknown')}")
                    except json.JSONDecodeError as e:
                        server.logger.error(f"Invalid JSON: {e}")
                        print(json.dumps({"error": f"Invalid JSON: {str(e)}"}), flush=True)
                    except asyncio.TimeoutError:
                        server.logger.error(f"Request processing timed out after {MCP_RESPONSE_TIMEOUT}s")
                        print(json.dumps({"error": "Request timed out"}), flush=True)
                    except Exception as e:
                        server.logger.error(f"Error handling request: {e}")
                        print(json.dumps({"error": str(e)}), flush=True)
            except Exception as e:
                server.logger.error(f"Error in main loop: {e}")
                # Continue to allow server to keep running
                continue

    except KeyboardInterrupt:
        server.logger.info("MCP Server shutting down due to keyboard interrupt...")
    except EOFError:
        server.logger.info("MCP Server connection closed (EOF)")
    except Exception as e:
        server.logger.critical(f"Critical error in MCP Server: {e}")
    finally:
        server.logger.info("MCP Server shutdown complete")


if __name__ == "__main__":
    main()

