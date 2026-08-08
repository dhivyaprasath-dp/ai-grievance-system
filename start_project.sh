#!/bin/bash

# AI Grievance System - One-Click Start Script

echo "==============================================="
echo "🚀 Starting AI Grievance System Setup..."
echo "==============================================="

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Navigate to backend
cd backend

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "⬇️ Installing dependencies..."
pip install -r requirements.txt

# Setup .env
if [ ! -f ".env" ]; then
    echo "⚙️ Configuring environment variables..."
    cp .env.example .env
    echo "⚠️ Created .env file. If you have a database password, please edit backend/.env"
fi

# Initialize Database
echo "🗄️ Initializing Database..."
python init_db.py

# Start Backend in background
echo "🔥 Starting Backend Server on port 5001..."
export FLASK_APP=app.start
export FLASK_ENV=development
flask run --port=5001 > ../backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start Frontend in background
echo "🌐 Starting Frontend Server on port 8000..."
cd ../frontend
python3 -m http.server 8000 > ../frontend.log 2>&1 &
FRONTEND_PID=$!

echo "==============================================="
echo "✅ System is RUNNING!"
echo "==============================================="
echo "👉 Frontend URL: http://localhost:8000"
echo "👉 Backend URL:  http://localhost:5001"
echo "👉 Admin Login:  admin@grievance.gov.in / admin123"
echo ""
echo "📝 Logs are being written to backend.log and frontend.log"
echo "❌ Press CTRL+C to stop the servers and exit."
echo "==============================================="

# Cleanup function to kill processes on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

# Trap SIGINT (CTRL+C)
trap cleanup SIGINT

# Keep script running
wait
