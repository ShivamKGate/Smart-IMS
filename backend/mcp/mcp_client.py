import asyncio
import subprocess
import os
import logging
from typing import Dict, Any
from fastmcp.client import MCPClient as BaseMCP
from ollama.ollama_client import ollama_client

logger = logging.getLogger(__name__)

class MCPClient(BaseMCP):
    def __init__(self):
        super().__init__()
        self.server_process = None
        self.server_running = False

    async def start_server(self) -> bool:
        try:
            server_path = os.path.join(os.path.dirname(__file__), "mcp_server.py")
            self.server_process = subprocess.Popen(
                ["python", server_path], text=True
            )
            self.server_running = True
            logger.info("MCP Server started")
            return True
        except Exception as e:
            logger.error(f"Start server failed: {e}")
            return False

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if tool_name == "text_to_sql":

            # directly call Ollama for text to sql
            sql = ollama_client.text_to_sql(arguments.get("text", ""))
            return {"success": True, "result": sql}

        if not self.server_running:
            await self.start_server()
        return {"success": True, "result": {"invoked": tool_name}}