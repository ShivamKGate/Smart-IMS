import os
import psycopg2
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

mcp = FastMCP("Smart-IMS DB Server")

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )

@mcp.tool()
def execute_sql_query(sql: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    try:
        results = cur.fetchall()
    except:
        conn.commit()
        results = []
    conn.close()
    return results

@mcp.tool()
def get_database_schema():
    return {"tables": { ... }}  # simplified

@mcp.tool()
def get_low_stock_items(warehouse_id: int = None):
    where = f"AND i.warehouse_id={warehouse_id}" if warehouse_id else ""
    sql = f"SELECT p.name, i.quantity FROM inventory i JOIN products p ON ... WHERE i.quantity <= p.reorder_level {where}"
    return execute_sql_query(sql)