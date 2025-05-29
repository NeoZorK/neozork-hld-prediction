#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for MCP Server
"""

import json
from typing import Dict, Any

class SimpleMCPUtils:
    """
    Utility methods for MCP Server
    """

    def __init__(self, server):
        """
        Initialize utilities with server reference
        """
        self.server = server

    def simplify_params(self, params):
        """
        Simplify request parameters for display
        """
        if not params:
            return "{}"

        # Create a simplified version of parameters for display
        result = {}

        # Handle different types of requests
        if "textDocument" in params:
            doc = params["textDocument"]
            if "uri" in doc:
                result["textDocument"] = {"uri": doc["uri"]}
            if "languageId" in doc:
                if "textDocument" not in result:
                    result["textDocument"] = {}
                result["textDocument"]["languageId"] = doc["languageId"]

        if "clientInfo" in params:
            client_info = params["clientInfo"]
            result["clientInfo"] = {
                "name": client_info.get("name", "Unknown"),
                "version": client_info.get("version", "Unknown")
            }

        if "capabilities" in params:
            # Just indicate we have capabilities without the full details
            result["capabilities"] = "..." if params["capabilities"] else "{}"

        if "processId" in params:
            result["processId"] = params["processId"]

        if "rootUri" in params:
            result["rootUri"] = params["rootUri"]

        if "protocolVersion" in params:
            result["protocolVersion"] = params["protocolVersion"]

        # For other parameters types, just include them directly if they're not too large
        for key, value in params.items():
            if key not in result:
                if isinstance(value, dict):
                    if len(json.dumps(value)) > 50:
                        result[key] = "..."
                    else:
                        result[key] = value
                elif isinstance(value, list):
                    if len(value) > 3:
                        result[key] = f"[...] ({len(value)} items)"
                    else:
                        result[key] = value
                elif isinstance(value, str) and len(value) > 50:
                    result[key] = value[:47] + "..."
                else:
                    result[key] = value

        return json.dumps(result, indent=2)

    def simplify_response(self, response):
        """
        Simplify response for display
        """
        if not response:
            return "{}"

        # Create a simplified version for display
        result = {}

        # Include main response properties
        if "id" in response:
            result["id"] = response["id"]

        if "jsonrpc" in response:
            result["jsonrpc"] = response["jsonrpc"]

        # For results, simplify based on content
        if "result" in response:
            if isinstance(response["result"], dict):
                result_preview = {}
                # Include key information from capabilities
                if "capabilities" in response["result"]:
                    result_preview["capabilities"] = "..." if response["result"]["capabilities"] else "{}"
                if "serverInfo" in response["result"]:
                    result_preview["serverInfo"] = response["result"]["serverInfo"]
                result["result"] = result_preview
            else:
                result["result"] = response["result"]

        # Include error information if present
        if "error" in response:
            result["error"] = response["error"]

        return json.dumps(result, indent=2)
