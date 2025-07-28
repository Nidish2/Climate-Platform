#!/bin/bash

# Climate Platform Development Setup Script
# This script sets up and runs the development environment

set -e  # Exit on any error

echo "🌍 Climate Platform Development Setup"
echo "===================================="

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
required_version="3.11"

if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)" 2>/dev/null; then
    echo "❌ Python 3.11+ is required. Found: $python_version"
    echo "Please install Python 3.11 or higher and try again."
    exit 1
fi

echo "✅ Python version: $python_version"

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
else
    echo "✅ Virtual environment exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
cd backend
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "📝 Please edit backend/.env with your API keys before continuing"
    echo "   Your API keys have been pre-configured in the template"
else
    echo "✅ Environment file exists"
fi

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo "🗄️  Initializing database..."
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('✅ Database initialized successfully')
"

# Test API connections
echo "🔌 Testing API connections..."
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

apis = {
    'OpenWeather': os.getenv('OPENWEATHER_API_KEY'),
    'Carbon Interface': os.getenv('CARBON_INTERFACE_KEY'),
    'OpenAQ': os.getenv('OPENAQ_API_KEY'),
    'Tomorrow.io': os.getenv('TOMORROW_API_KEY'),
    'AirVisual': os.getenv('AIRVISUAL_API_KEY')
}

print('API Key Status:')
for api, key in apis.items():
    status = '✅ Configured' if key else '❌ Missing'
    print(f'  {api}: {status}')
"

# Start the Flask development server
echo ""
echo "🚀 Starting Flask development server..."
echo "   Backend will be available at: http://127.0.0.1:5000"
echo "   API Health Check: http://127.0.0.1:5000/api/health"
echo ""
echo "📱 To start the frontend:"
echo "   1. Open a new terminal"
echo "   2. Run: npm install"
echo "   3. Run: npm run dev"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Set environment variables for Flask
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=True

# Run Flask app
python app.py
