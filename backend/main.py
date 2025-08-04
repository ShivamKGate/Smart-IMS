from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import subprocess
import json
from typing import Dict, Any, List
from pydantic import BaseModel
from mcp_system.mcp_client import mcp_client

load_dotenv()

app = FastAPI(title="Smart-IMS API")

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class QueryRequest(BaseModel):
    question: str

class SQLRequest(BaseModel):
    sql: str

class InventoryRequest(BaseModel):
    product_id: int
    warehouse_id: int
    quantity: int

@app.get("/")
def read_root():
    return {"message": "Smart-IMS API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Smart-IMS API"}

@app.post("/api/query")
async def natural_language_query(request: QueryRequest):
    """
    Process a natural language query about inventory using Ollama + MCP
    """
    try:
        # Step 1: Convert natural language to SQL using Ollama (via MCP)
        sql_result = await mcp_client.call_tool("text_to_sql", {"text": request.question})
        
        if not sql_result.get("success"):
            raise HTTPException(status_code=500, detail=f"Failed to convert text to SQL: {sql_result.get('error')}")
        
        generated_sql = sql_result["result"]
        
        # Step 2: Execute the generated SQL
        if generated_sql and not generated_sql.startswith("--"):
            execution_result = await mcp_client.call_tool("execute_sql_query", {"sql": generated_sql})
            
            if not execution_result.get("success"):
                raise HTTPException(status_code=500, detail=f"Failed to execute SQL: {execution_result.get('error')}")
            
            results = execution_result["result"]
        else:
            results = [{"message": "Could not generate executable SQL", "generated_sql": generated_sql}]
        
        response = {
            "question": request.question,
            "sql_generated": generated_sql,
            "results": results,
            "status": "success"
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sql")
async def execute_sql(request: SQLRequest):
    """
    Execute a raw SQL query (for testing/admin use)
    """
    try:
        result = await mcp_client.call_tool("execute_sql_query", {"sql": request.sql})
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        response = {
            "sql": request.sql,
            "results": result["result"],
            "status": "success"
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/inventory/low-stock")
async def get_low_stock():
    """
    Get products with low stock levels
    """
    try:
        result = await mcp_client.call_tool("get_low_stock_items", {})
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        return {
            "low_stock_items": result["result"],
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/inventory/summary")
async def get_inventory_summary():
    """
    Get inventory summary across all warehouses
    """
    try:
        result = await mcp_client.call_tool("get_inventory_summary", {})
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        return {
            "summary": result["result"],
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/inventory/add")
async def add_inventory(request: InventoryRequest):
    """
    Add inventory for a product at a warehouse
    """
    try:
        result = await mcp_client.call_tool("add_inventory", {
            "product_id": request.product_id,
            "warehouse_id": request.warehouse_id,
            "quantity": request.quantity
        })
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        return {
            "message": f"Added {request.quantity} units of product {request.product_id} to warehouse {request.warehouse_id}",
            "details": result["result"],
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/schema")
async def get_database_schema():
    """
    Get the database schema (useful for understanding the structure)
    """
    try:
        result = await mcp_client.call_tool("get_database_schema", {})
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get('error'))
        
        return {
            "schema": result["result"],
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
