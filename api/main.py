from fastapi import FastAPI

app = FastAPI(title="FastAPI Backend", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on Vercel!", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

@app.get("/api/v1/health")
async def api_health():
    return {"status": "healthy", "message": "API v1 is running"}

# For more complex functionality, uncomment below:
# try:
#     import sys
#     import os
#     sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#     from app.main import app as full_app
#     app = full_app
# except Exception as e:
#     print(f"Could not import full app: {e}")
#     pass
