import asyncio
import subprocess
import os
import logging
import json
from typing import Dict, Any
from fastmcp.client import MCPClient as BaseMCP
from ollama.ollama_client import ollama_client

logger = logging.getLogger(__name__)

class MCPClient(BaseMCP):
    def __init__(self):
        super().__init__()
        self.server_process = None
        self.server_running = False
    async def start_server(self):
        self.server_process = subprocess.Popen(
            ["python", os.path.join(os.path.dirname(__file__), "mcp_server.py")],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        self.server_running = True

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "text_to_sql":
            return {"success": True, "result": ollama_client.text_to_sql(arguments["text"])}

        if not self.server_running: await self.start_server()
        request = {"jsonrpc":"2.0","id":1,"method":"tools/call","params": {"name":tool_name, "arguments":arguments}}
        # send and receive via pipes
        self.server_process.stdin.write(json.dumps(request) + "\n")
        self.server_process.stdin.flush()
        response = self.server_process.stdout.readline()
        return json.loads(response)