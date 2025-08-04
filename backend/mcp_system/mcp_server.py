import asyncio
import logging
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP
from mcp.server.models import InitializationOptions
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import os
import urllib.parse

# Load environment variables
load_dotenv()

# Database configuration
DB_HOST = os.getenv('DB_HOST', '').strip('"\'')
DB_PORT = os.getenv('DB_PORT', '').strip('"\'')
DB_NAME = os.getenv('DB_NAME', '').strip('"\'')
DB_USER = os.getenv('DB_USER', '').strip('"\'')
DB_PASSWORD = urllib.parse.quote(os.getenv('DB_PASSWORD', '').strip('"\''))

# Create the MCP server instance
mcp = FastMCP("Smart-IMS Database Server")

def get_db_connection():
    """Create a database connection"""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=urllib.parse.unquote(DB_PASSWORD)
    )

@mcp.tool()
def execute_sql_query(sql: str) -> List[Dict[str, Any]]:
    """
    Execute a SQL query on the Smart-IMS database.
    Returns results as a list of dictionaries.
    
    Args:
        sql: The SQL query to execute
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(sql)
        
        # Handle SELECT queries
        if cursor.description:
            results = cursor.fetchall()
            return [dict(row) for row in results]
        else:
            # Handle INSERT/UPDATE/DELETE queries
            conn.commit()
            return [{"affected_rows": cursor.rowcount, "status": "success"}]
            
    except Exception as e:
        return [{"error": str(e), "status": "error"}]
    finally:
        if conn:
            conn.close()

@mcp.tool()
def get_database_schema() -> Dict[str, Any]:
    """
    Get the database schema information for the LLM to understand the structure.
    This helps Ollama generate accurate SQL queries.
    """
    schema_info = {
        "tables": {
            "categories": {
                "columns": ["id (INTEGER, PRIMARY KEY)", "name (VARCHAR)"],
                "description": "Product categories like Electronics, Clothing, etc."
            },
            "products": {
                "columns": [
                    "id (INTEGER, PRIMARY KEY)", 
                    "name (VARCHAR)", 
                    "category_id (INTEGER, FOREIGN KEY to categories.id)",
                    "price (FLOAT)",
                    "reorder_level (INTEGER)"
                ],
                "description": "Products with their details and reorder thresholds"
            },
            "warehouses": {
                "columns": ["id (INTEGER, PRIMARY KEY)", "location (VARCHAR)"],
                "description": "Warehouse locations"
            },
            "inventory": {
                "columns": [
                    "product_id (INTEGER, FOREIGN KEY to products.id)",
                    "warehouse_id (INTEGER, FOREIGN KEY to warehouses.id)",
                    "quantity (INTEGER)"
                ],
                "description": "Current stock levels for each product at each warehouse"
            },
            "suppliers": {
                "columns": ["id (INTEGER, PRIMARY KEY)", "name (VARCHAR)", "contact (VARCHAR)"],
                "description": "Supplier information"
            }
        },
        "common_queries": [
            "Find low stock items: JOIN products, inventory, warehouses WHERE inventory.quantity <= products.reorder_level",
            "Add inventory: INSERT INTO inventory or UPDATE inventory SET quantity = quantity + ?",
            "Get product info: SELECT from products JOIN categories",
            "Inventory summary: JOIN all tables for comprehensive view"
        ]
    }
    
    return schema_info

@mcp.tool()
def get_low_stock_items(warehouse_id: int = None) -> List[Dict[str, Any]]:
    """
    Get products that are below their reorder level.
    
    Args:
        warehouse_id: Optional warehouse ID to filter by
    """
    where_clause = ""
    if warehouse_id:
        where_clause = f"AND i.warehouse_id = {warehouse_id}"
    
    sql = f"""
    SELECT 
        p.id as product_id,
        p.name as product_name,
        c.name as category,
        p.reorder_level,
        i.quantity as current_stock,
        w.location as warehouse,
        p.price
    FROM products p
    JOIN categories c ON p.category_id = c.id
    JOIN inventory i ON p.id = i.product_id
    JOIN warehouses w ON i.warehouse_id = w.id
    WHERE i.quantity <= p.reorder_level
    {where_clause}
    ORDER BY (p.reorder_level - i.quantity) DESC
    """
    
    return execute_sql_query(sql)

@mcp.tool()
def add_inventory(product_id: int, warehouse_id: int, quantity: int) -> List[Dict[str, Any]]:
    """
    Add inventory for a product at a warehouse.
    
    Args:
        product_id: ID of the product
        warehouse_id: ID of the warehouse
        quantity: Quantity to add
    """
    sql = f"""
    INSERT INTO inventory (product_id, warehouse_id, quantity)
    VALUES ({product_id}, {warehouse_id}, {quantity})
    ON CONFLICT (product_id, warehouse_id)
    DO UPDATE SET quantity = inventory.quantity + {quantity}
    """
    
    return execute_sql_query(sql)

@mcp.tool()
def get_inventory_summary() -> List[Dict[str, Any]]:
    """
    Get a summary of all inventory across warehouses.
    """
    sql = """
    SELECT 
        p.name as product_name,
        c.name as category,
        w.location as warehouse,
        i.quantity,
        p.reorder_level,
        CASE 
            WHEN i.quantity <= p.reorder_level THEN 'LOW STOCK'
            WHEN i.quantity <= p.reorder_level * 1.5 THEN 'WARNING'
            ELSE 'OK'
        END as stock_status,
        p.price,
        (i.quantity * p.price) as total_value
    FROM products p
    JOIN categories c ON p.category_id = c.id
    JOIN inventory i ON p.id = i.product_id
    JOIN warehouses w ON i.warehouse_id = w.id
    ORDER BY stock_status DESC, p.name
    """
    
    return execute_sql_query(sql)

if __name__ == "__main__":
    # Run the MCP server
    mcp.run() 