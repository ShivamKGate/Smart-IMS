from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from mcp.mcp_client import MCPClient
from pydantic import BaseModel

load_dotenv()
app = FastAPI(title="Smart-IMS API")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

class QueryRequest(BaseModel): question: str
class SQLRequest(BaseModel): sql: str
class InventoryRequest(BaseModel): product_id: int; warehouse_id: int; quantity: int

@app.get("/health")
def health(): return {"status": "healthy"}

@app.post("/api/query")
async def nl_query(req: QueryRequest):
    res = await MCPClient.call_tool("text_to_sql", {"text": req.question})
    if not res["success"]: raise HTTPException(500)
    return res["result"]

@app.post("/api/sql")
async def raw_sql(req: SQLRequest):
    res = await MCPClient.call_tool("execute_sql_query", {"sql": req.sql})
    if not res["success"]: raise HTTPException(500)
    return res["result"]

@app.get("/api/inventory/low-stock")
async def low_stock():
    res = await MCPClient.call_tool("get_low_stock_items", {})
    return res["result"]

@app.get("/api/inventory/summary")
async def summary():
    res = await MCPClient.call_tool("get_inventory_summary", {})
    return res["result"]

@app.post("/api/inventory/add")
async def add_inv(req: InventoryRequest):
    res = await MCPClient.call_tool("add_inventory", req.dict())
    return res["result"]