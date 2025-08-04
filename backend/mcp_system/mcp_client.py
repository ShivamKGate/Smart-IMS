import asyncio
import json
import subprocess
import os
from typing import Dict, List, Any, Optional
import logging
from llm.ollama_client import ollama_client

logger = logging.getLogger(__name__)

class MCPClient:
    """Client to communicate with the MCP server"""
    
    def __init__(self):
        self.server_process = None
        self.server_running = False
    
    async def start_server(self):
        """Start the MCP server process"""
        try:
            # Start the MCP server as a subprocess
            server_path = os.path.join(os.path.dirname(__file__), "mcp_server.py")
            self.server_process = subprocess.Popen(
                ["python", server_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.server_running = True
            logger.info("MCP Server started successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to start MCP server: {e}")
            return False
    
    async def stop_server(self):
        """Stop the MCP server process"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
            self.server_running = False
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a tool on the MCP server
        
        Args:
            tool_name: Name of the tool to call
            arguments: Arguments to pass to the tool
            
        Returns:
            Result from the tool execution
        """
        try:
            if not self.server_running:
                await self.start_server()
            
            # Create the MCP request
            request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            }
            
            # For now, we'll simulate the MCP call
            # In a real implementation, this would use the MCP protocol
            result = await self._simulate_tool_call(tool_name, arguments)
            
            return {
                "success": True,
                "result": result
            }
            
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _simulate_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Simulate tool calls for now - this will be replaced with real MCP communication
        """
        if tool_name == "execute_sql_query":
            # Import here to avoid circular imports
            from mcp_system.mcp_server import execute_sql_query
            return execute_sql_query(arguments.get("sql", ""))
        
        elif tool_name == "get_low_stock_items":
            from mcp_system.mcp_server import get_low_stock_items
            return get_low_stock_items(arguments.get("warehouse_id"))
        
        elif tool_name == "add_inventory":
            from mcp_system.mcp_server import add_inventory
            return add_inventory(
                arguments.get("product_id"),
                arguments.get("warehouse_id"), 
                arguments.get("quantity")
            )
        
        elif tool_name == "get_inventory_summary":
            from mcp_system.mcp_server import get_inventory_summary
            return get_inventory_summary()
        
        elif tool_name == "get_database_schema":
            from mcp_system.mcp_server import get_database_schema
            return get_database_schema()
        
        elif tool_name == "text_to_sql":
            # This now uses the real Ollama integration!
            return await self._convert_text_to_sql(arguments.get("text", ""))
        
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    async def _convert_text_to_sql(self, text: str) -> str:
        """
        Convert natural language to SQL using Ollama
        This is the real implementation using your local Ollama service!
        """
        logger.info(f"Converting text to SQL: {text}")
        
        # Use the Ollama client to convert text to SQL
        sql_result = await ollama_client.text_to_sql(text)
        
        logger.info(f"Generated SQL: {sql_result}")
        return sql_result

# Global MCP client instance
mcp_client = MCPClient() 