from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from mcp.mcp_client import MCPClient
from pydantic import BaseModel

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

class QueryRequest(BaseModel):
    question: str

@app.post("/api/query")
async def natural_language_query(request: QueryRequest):
    sql_result = await MCPClient.call_tool("text_to_sql", {"text": request.question})
    if not sql_result["success"]:
        raise HTTPException(status_code=500)
    return sql_result["result"]