# Smart-IMS - Intelligent Inventory Management System

An AI-powered inventory management system that converts natural language queries to SQL using **Ollama**, **MCP (Model Context Protocol)**, and **PostgreSQL**.

## 🎯 Features

- **Natural Language to SQL**: Type questions like "Add 50 laptops to warehouse 1" and watch them become SQL queries
- **Local LLM Integration**: Uses Ollama with Gemma 3 for text-to-SQL conversion
- **MCP Bridge**: Model Context Protocol connects the LLM directly to your PostgreSQL database
- **Real-time Execution**: Generated SQL queries are executed immediately on your database
- **Web Interface**: Simple HTML frontend for testing and demonstrations
- **Multi-table Queries**: Handles complex JOINs, aggregations, and inventory operations

## 🏗️ Architecture

```
User Input (Natural Language)
        ↓
    FastAPI Backend
        ↓
    MCP Client
        ↓
    Ollama (Gemma 3) → Converts to SQL
        ↓
    MCP Server → Executes SQL
        ↓
    PostgreSQL Database
        ↓
    Results returned to User
```

## 📁 Project Structure

```
Smart-IMS/
├── backend/
│   ├── main.py                    # FastAPI application entry point
│   ├── requirements.txt           # Python dependencies
│   ├── test_ollama_integration.py # Integration testing script
│   ├── mcp_system/               # Model Context Protocol components
│   │   ├── mcp_server.py         # MCP server with database tools
│   │   └── mcp_client.py         # MCP client for FastAPI integration
│   ├── llm/                      # Language model integration
│   │   └── ollama_client.py      # Ollama integration for text-to-SQL
│   ├── database/                 # Database models and setup
│   │   ├── db.py                 # SQLAlchemy models and configuration
│   │   ├── init_db.py            # Database table creation script
│   │   └── seed_data.py          # Sample data population script
│   └── .env                      # Database configuration (create this)
├── frontend/
│   └── index.html                # Web interface for testing
├── examples.txt                  # Multi-table query examples
└── README.md                    # This file
```

## 🗄️ Database Schema

- **categories** - Product categories (Electronics, Clothing, etc.)
- **products** - Products with prices and reorder levels
- **warehouses** - Storage locations
- **inventory** - Current stock levels (product + warehouse)
- **suppliers** - Supplier contact information

## 🚀 Setup Instructions

### 1. Prerequisites

- **Python 3.8+**
- **PostgreSQL** (with pgAdmin recommended)
- **Ollama** (for local LLM)

### 2. Install Ollama

```bash
# Install Ollama from https://ollama.ai/
# Then start the service
ollama serve

# Pull the Gemma 3 model
ollama pull gemma3:latest
```

### 3. Database Setup

1. **Create PostgreSQL database:**
   ```sql
   CREATE DATABASE smartims;
   ```

2. **Configure environment variables:**
   ```bash
   # Edit backend/.env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=smartims
   DB_USER=postgres
   DB_PASSWORD="your_password_here"
   ```

### 4. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 5. Initialize Database

```bash
# Create tables
python init_db.py

# Add sample data
python seed_data.py
```

### 6. Test Integration

```bash
# Test the complete pipeline
python test_ollama_integration.py
```

### 7. Start the Application

```bash
# Start FastAPI server
python main.py

# Open web interface
# Navigate to frontend/index.html in your browser
```

## 🧪 Usage Examples

### Natural Language Queries

Try these queries in the web interface:

1. **"Show me all products with their categories and stock levels"**
2. **"Which items are below their reorder level?"**
3. **"Add 50 laptops to warehouse 1"**
4. **"What's the total inventory value per warehouse?"**
5. **"Find all electronics products in the main warehouse"**

### API Endpoints

- `POST /api/query` - Natural language queries
- `POST /api/sql` - Direct SQL execution
- `GET /api/inventory/low-stock` - Low stock items
- `GET /api/inventory/summary` - Inventory overview
- `POST /api/inventory/add` - Add inventory
- `GET /api/schema` - Database schema

### Example API Usage

```bash
# Natural language query
curl -X POST "http://localhost:8000/api/query" \
     -H "Content-Type: application/json" \
     -d '{"question": "Show me products that are low on stock"}'

# Direct SQL query
curl -X POST "http://localhost:8000/api/sql" \
     -H "Content-Type: application/json" \
     -d '{"sql": "SELECT * FROM products LIMIT 5;"}'
```

## 🔧 Configuration

### Ollama Model Configuration

Edit `backend/ollama_client.py` to change the model:

```python
def __init__(self, base_url: str = "http://localhost:11434", model: str = "gemma3:latest"):
```

### Database Connection

Configure your database in `backend/.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smartims
DB_USER=postgres
DB_PASSWORD="your_password"
```

## 🧩 How It Works

1. **User Input**: Natural language query entered via web interface or API
2. **Text-to-SQL**: Ollama (Gemma 3) converts the query to SQL using trained prompts
3. **MCP Bridge**: Model Context Protocol facilitates communication between LLM and database
4. **SQL Execution**: Generated SQL is executed on PostgreSQL database
5. **Results**: Query results are returned to the user in JSON format

## 🛠️ Development

### Adding New Tools

Add new MCP tools in `backend/mcp_server.py`:

```python
@mcp.tool()
def your_new_tool(param: str) -> List[Dict[str, Any]]:
    """Your tool description"""
    # Implementation here
    return execute_sql_query("YOUR SQL HERE")
```

### Customizing Prompts

Modify the system prompt in `backend/ollama_client.py` to improve SQL generation for your specific use case.

### Testing

Run the integration test to verify all components:

```bash
python test_ollama_integration.py
```

## 🔍 Troubleshooting

### Common Issues

1. **Ollama not running**: Start with `ollama serve`
2. **Model not found**: Pull model with `ollama pull gemma3:latest`
3. **Database connection**: Check `.env` credentials and PostgreSQL status
4. **MCP errors**: Verify database schema exists (`python init_db.py`)

### Logs

Check FastAPI logs for detailed error information:

```bash
python main.py --log-level debug
```

## 📊 Example Queries

See `examples.txt` for comprehensive multi-table query examples that test the system's capabilities.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `python test_ollama_integration.py`
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **Ollama** for local LLM infrastructure
- **FastMCP** for Model Context Protocol implementation
- **FastAPI** for the web framework
- **SQLAlchemy** for database ORM
- **PostgreSQL** for the database engine

## 🛠️ Development Tools

This project was developed with assistance from:
- **Cursor IDE** - For AI-powered code completion, debugging assistance, and intelligent code suggestions
- **GitHub Copilot** - For improving code logic, suggesting refactoring approaches, and helping with implementation patterns

These AI development tools significantly enhanced the development process by providing intelligent suggestions, helping debug complex integration issues, and suggesting optimal code structures for the MCP and Ollama integrations.

---