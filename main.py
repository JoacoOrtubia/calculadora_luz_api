"""
Entry point for the application - imports from app.main
This file helps Render find the application when app module imports fail
"""
import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Debug: Print current directory and contents
print(f"Current directory: {current_dir}")
print(f"Contents: {os.listdir(current_dir)}")
print(f"Python path: {sys.path[:3]}")

try:
    # Try importing from app.main
    from app.main import app
    print("Successfully imported from app.main")
except ImportError as e:
    print(f"Import error: {e}")
    # Try adding app directory specifically to path
    app_dir = os.path.join(current_dir, 'app')
    if os.path.exists(app_dir):
        sys.path.insert(0, app_dir)
        print(f"Added app directory to path: {app_dir}")
        # Import main module directly
        import main as app_main
        app = app_main.app
        print("Successfully imported via fallback method")
    else:
        print(f"App directory not found at: {app_dir}")
        raise

# This allows uvicorn to find the app at main:app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))