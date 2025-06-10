#!/bin/bash

echo "🚀 Starting FastAPI Backend..."

# Check if we're in production
if [ "$ENVIRONMENT" = "production" ]; then
    echo "📦 Production mode detected"
    # Run with gunicorn for production
    exec gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:${PORT:-8000}
else
    echo "🔧 Development mode detected"
    # Run with uvicorn for development
    exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --reload
fi
