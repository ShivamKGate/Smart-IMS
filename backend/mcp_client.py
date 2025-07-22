from fastmcp.client import MCPClient

class MyMCPClient(MCPClient):
    def __init__(self):
        super().__init__()

    def get_greeting(self, name: str) -> str:
        return f"Hello, {name}!"    
