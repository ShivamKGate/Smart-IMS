from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Smart-IMS DB Server")

@mcp.tool()
def execute_sql_query(sql: str):
    # stub
    return [{"status": "not implemented"}]

if __name__ == "__main__":
    mcp.run()