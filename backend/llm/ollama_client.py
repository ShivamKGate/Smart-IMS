import requests
import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class OllamaClient:
    """Client to communicate with Ollama service for text-to-SQL conversion"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "gemma3:latest"):
        self.base_url = base_url
        self.model = model
        self.session = requests.Session()
    
    def is_available(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama not available: {e}")
            return False
    
    def get_system_prompt(self) -> str:
        """Get the system prompt that teaches the LLM about our database schema"""
        return """You are a SQL expert for an inventory management system. Convert natural language queries to PostgreSQL SQL.

DATABASE SCHEMA:
- categories (id, name) - Product categories like Electronics, Clothing
- products (id, name, category_id, price, reorder_level) - Products with details
- warehouses (id, location) - Warehouse locations  
- inventory (product_id, warehouse_id, quantity) - Current stock levels
- suppliers (id, name, contact) - Supplier information

RULES:
1. Always return valid PostgreSQL SQL only
2. Use proper JOINs when accessing multiple tables
3. For adding inventory: Use INSERT ... ON CONFLICT DO UPDATE
4. For queries about stock: JOIN products, inventory, warehouses
5. For low stock: WHERE inventory.quantity <= products.reorder_level
6. Return only the SQL query, no explanations

EXAMPLES:
User: "Add 50 laptops to warehouse 1"
SQL: INSERT INTO inventory (product_id, warehouse_id, quantity) SELECT 1, 1, 50 WHERE EXISTS (SELECT 1 FROM products WHERE id = 1 AND name ILIKE '%laptop%') ON CONFLICT (product_id, warehouse_id) DO UPDATE SET quantity = inventory.quantity + 50;

User: "Show me low stock items"
SQL: SELECT p.name, c.name as category, i.quantity, p.reorder_level, w.location FROM products p JOIN categories c ON p.category_id = c.id JOIN inventory i ON p.id = i.product_id JOIN warehouses w ON i.warehouse_id = w.id WHERE i.quantity <= p.reorder_level;

User: "What's the total value of electronics inventory?"
SQL: SELECT SUM(i.quantity * p.price) as total_value FROM inventory i JOIN products p ON i.product_id = p.id JOIN categories c ON p.category_id = c.id WHERE c.name ILIKE '%electronics%';

Now convert the user's request to SQL:"""

    async def text_to_sql(self, user_input: str) -> str:
        """
        Convert natural language to SQL using Ollama
        
        Args:
            user_input: Natural language query from user
            
        Returns:
            Generated SQL query
        """
        try:
            if not self.is_available():
                return f"-- Error: Ollama service not available\n-- Original request: {user_input}"
            
            # Prepare the prompt
            system_prompt = self.get_system_prompt()
            full_prompt = f"{system_prompt}\n\nUser: {user_input}\nSQL:"
            
            # Make request to Ollama
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Low temperature for more consistent SQL
                    "top_p": 0.9,
                    "max_tokens": 200
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code != 200:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return f"-- Error: Ollama API returned {response.status_code}\n-- Original request: {user_input}"
            
            result = response.json()
            generated_sql = result.get("response", "").strip()
            
            # Clean up the generated SQL
            generated_sql = self._clean_sql(generated_sql)
            
            logger.info(f"Generated SQL for '{user_input}': {generated_sql}")
            return generated_sql
            
        except Exception as e:
            logger.error(f"Error generating SQL: {e}")
            return f"-- Error generating SQL: {str(e)}\n-- Original request: {user_input}"
    
    def _clean_sql(self, sql: str) -> str:
        """Clean and validate the generated SQL"""
        # Remove any extra explanations or markdown
        lines = sql.split('\n')
        sql_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip empty lines, comments, or explanations
            if not line or line.startswith('--') or line.startswith('#'):
                continue
            # Stop at explanations
            if any(word in line.lower() for word in ['explanation:', 'note:', 'this query']):
                break
            sql_lines.append(line)
        
        cleaned_sql = ' '.join(sql_lines)
        
        # Ensure it ends with semicolon
        if cleaned_sql and not cleaned_sql.endswith(';'):
            cleaned_sql += ';'
        
        return cleaned_sql

# Global Ollama client instance
ollama_client = OllamaClient() 