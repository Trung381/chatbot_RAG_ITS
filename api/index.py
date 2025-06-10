import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.main import app
except ImportError:
    # Fallback if import fails
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {"message": "FastAPI Backend is running", "status": "ok"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}

# Vercel expects the ASGI app to be available at module level
