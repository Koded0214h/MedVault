
import sys
sys.path.insert(0, "/Users/koded/Desktop/Code/MedVault/env/lib/python3.11/site-packages")

# Test FastMCP import without Django
try:
    from fastmcp import FastMCP
    print("FastMCP imported successfully")
    
    # Create a simple app
    app = FastMCP("Test MCP Server")
    print("FastMCP app created successfully")
    
    @app.tool()
    def test_tool():
        """A simple test tool"""
        return "Hello from test tool"
    
    print("Tool registered successfully")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
