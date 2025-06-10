#!/bin/bash

echo "🧪 Running FastAPI Backend Tests"
echo "================================"

# Set test environment
export ENVIRONMENT=testing

# Run tests with coverage
echo "📊 Running tests with coverage..."
pytest --cov=app --cov-report=html --cov-report=term-missing

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "✅ All tests passed!"
    echo "📊 Coverage report generated in htmlcov/"
else
    echo "❌ Some tests failed!"
    exit 1
fi
