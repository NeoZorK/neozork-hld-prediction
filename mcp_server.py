# mcp_server.py
# MCP server stub for local file access

from mcp.server import Server
import os

# Specify the directory to allow access
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

class FileAccessServer(Server):
    def __init__(self):
        super().__init__("mcp_server")

    def on_connect(self, client):
        print(f"Client connected: {client}")

    def on_disconnect(self, client):
        print(f"Client disconnected: {client}")

    # Example handler for file read request
    def handle_read_file(self, client, path):
        abs_path = os.path.abspath(os.path.join(WORKSPACE_DIR, path))
        if not abs_path.startswith(WORKSPACE_DIR):
            return {"error": "Access denied"}
        try:
            with open(abs_path, 'r') as f:
                content = f.read()
            return {"content": content}
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    server = FileAccessServer()
    print("MCP server started...")
    server.run()
