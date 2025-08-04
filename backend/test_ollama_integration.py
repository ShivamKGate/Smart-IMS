import asyncio
import sys
from mcp_system.mcp_client import mcp_client
from llm.ollama_client import ollama_client

async def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    print("🔍 Testing Ollama connection...")
    
    if ollama_client.is_available():
        print("✅ Ollama is running!")
        
        # Test a simple text-to-SQL conversion
        test_query = "Show me all products"
        print(f"🧪 Testing with: '{test_query}'")
        
        sql = await ollama_client.text_to_sql(test_query)
        print(f"🔧 Generated SQL: {sql}")
        return True
    else:
        print("❌ Ollama is not running!")
        print("💡 Start Ollama with: ollama serve")
        print("💡 Pull the model with: ollama pull gemma2:2b")
        return False

async def test_mcp_integration():
    """Test the MCP integration with database"""
    print("\n🔍 Testing MCP integration...")
    
    try:
        # Test database schema retrieval
        schema_result = await mcp_client.call_tool("get_database_schema", {})
        if schema_result.get("success"):
            print("✅ MCP can access database schema!")
        else:
            print(f"❌ MCP schema error: {schema_result.get('error')}")
            return False
        
        # Test direct SQL execution
        sql_result = await mcp_client.call_tool("execute_sql_query", {"sql": "SELECT COUNT(*) FROM products;"})
        if sql_result.get("success"):
            count = sql_result["result"][0] if sql_result["result"] else {"count": 0}
            print(f"✅ Database has {count} products")
        else:
            print(f"❌ SQL execution error: {sql_result.get('error')}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ MCP integration error: {e}")
        return False

async def test_full_pipeline():
    """Test the complete text-to-SQL pipeline"""
    print("\n🔍 Testing complete text-to-SQL pipeline...")
    
    test_queries = [
        "Show me all products with their categories",
        "Find items that are low on stock",
        "Add 25 tablets to warehouse 2",
        "What's the total inventory value?"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: '{query}'")
        
        try:
            # Step 1: Convert text to SQL using Ollama
            sql_result = await mcp_client.call_tool("text_to_sql", {"text": query})
            
            if not sql_result.get("success"):
                print(f"❌ Text-to-SQL failed: {sql_result.get('error')}")
                continue
            
            generated_sql = sql_result["result"]
            print(f"🔧 Generated SQL: {generated_sql}")
            
            # Step 2: Execute the SQL (only if it's a SELECT query for safety)
            if generated_sql.strip().upper().startswith("SELECT"):
                execution_result = await mcp_client.call_tool("execute_sql_query", {"sql": generated_sql})
                
                if execution_result.get("success"):
                    results = execution_result["result"]
                    print(f"✅ Results: {results[:3] if len(results) > 3 else results}")  # Show first 3 results
                else:
                    print(f"❌ Execution failed: {execution_result.get('error')}")
            else:
                print("⚠️  Non-SELECT query - execution skipped for safety")
                
        except Exception as e:
            print(f"❌ Pipeline error: {e}")

async def main():
    print("🚀 SMART-IMS OLLAMA + MCP INTEGRATION TEST")
    print("=" * 50)
    
    # Test 1: Ollama connection
    ollama_ok = await test_ollama_connection()
    
    # Test 2: MCP integration
    mcp_ok = await test_mcp_integration()
    
    # Test 3: Full pipeline (only if both components work)
    if ollama_ok and mcp_ok:
        await test_full_pipeline()
        
        print("\n🎉 INTEGRATION TEST COMPLETE!")
        print("\n💡 Next steps:")
        print("   1. Run: python main.py")
        print("   2. Open: frontend/index.html")
        print("   3. Try queries like: 'Add 50 laptops to warehouse 1'")
        
    else:
        print("\n❌ INTEGRATION TEST FAILED!")
        print("\n🔧 Setup requirements:")
        print("   1. Install Ollama: https://ollama.ai/")
        print("   2. Start Ollama: ollama serve")
        print("   3. Pull model: ollama pull gemma2:2b")
        print("   4. Setup database: python init_db.py && python seed_data.py")

if __name__ == "__main__":
    asyncio.run(main()) 