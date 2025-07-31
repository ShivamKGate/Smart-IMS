import os, urllib.parse
import psycopg2, psycopg2.extras
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
load_dotenv()

# DB config
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = urllib.parse.unquote(os.getenv('DB_PASSWORD'))

mcp = FastMCP("Smart-IMS Database Server")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, database=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
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
    return {
        "tables": {
            "categories": ["id", "name"],
            "products": ["id", "name", "category_id", "price", "reorder_level"],
            "warehouses": ["id", "name", "location"],
            "inventory": ["product_id", "warehouse_id", "quantity"],
            "suppliers": ["id", "name", "contact"],
        }
    }

@mcp.tool()
def add_inventory(product_id: int, warehouse_id: int, quantity: int):
    sql = (
        "INSERT INTO inventory (product_id, warehouse_id, quantity) VALUES "
        f"({product_id}, {warehouse_id}, {quantity}) "
        "ON CONFLICT (product_id, warehouse_id) DO UPDATE SET quantity = inventory.quantity + "
        f"{quantity};"
    )
    return execute_sql_query(sql)

@mcp.tool()
def get_inventory_summary():
    sql = "SELECT p.name, i.quantity, p.price, (i.quantity * p.price) AS total FROM inventory i JOIN products p ON i.product_id = p.id;"
    return execute_sql_query(sql)

@mcp.tool()
def get_low_stock_items(warehouse_id: int = None):
    where = f"AND i.warehouse_id={warehouse_id}" if warehouse_id else ""
    sql = (
        "SELECT p.name, i.quantity FROM inventory i JOIN products p ON i.product_id = p.id "
        f"WHERE i.quantity <= p.reorder_level {where};"
    )
    return execute_sql_query(sql)

if __name__ == "__main__":
    mcp.run()