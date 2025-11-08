#!/bin/bash
# AgroSmart Backend Startup Script

# Navigate to backend directory
cd "$(dirname "$0")"

echo "🌾 Starting AgroSmart Backend API..."
echo "📍 Directory: $(pwd)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Start the server
echo "🚀 Server starting on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔄 Press Ctrl+C to stop the server"
echo ""

./venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 --reload
