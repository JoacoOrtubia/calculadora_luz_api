"""
Entry point for the application - imports from app.main
This file helps Render find the application when app module imports fail
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the actual FastAPI app
from app.main import app

# This allows uvicorn to find the app at main:app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))