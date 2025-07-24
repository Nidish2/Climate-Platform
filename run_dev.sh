#!/bin/bash

# Climate Platform Development Runner
# Enhanced development setup script

set -e

echo "🌍 Starting Climate Platform Development Environment"
echo "=================================================="

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.11+ is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Set environment variables for development
export FLASK_ENV=development
export FLASK_DEBUG=True
export FLASK_APP=app.py
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env file with your API keys before running the application"
fi

# Initialize database
echo "🗄️ Initializing database..."
cd backend
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database tables created successfully')
"

# Start the development server
echo "🚀 Starting development server..."
echo "Backend will be available at: http://127.0.0.1:5000"
echo "API documentation: http://127.0.0.1:5000/api/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
