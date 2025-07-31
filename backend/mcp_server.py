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