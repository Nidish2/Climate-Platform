@echo off
echo 🌍 Climate Platform Development Setup (Windows)
echo =============================================

REM Check Python version
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

REM Navigate to backend directory
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️ Upgrading pip...
python -m pip install --upgrade pip

REM Install wheel first (helps with Windows compilation issues)
echo 🛠️ Installing build tools...
pip install wheel setuptools

REM Install dependencies one by one to catch errors
echo 📚 Installing core dependencies...
pip install Flask==3.0.0
pip install Flask-CORS==4.0.0
pip install Flask-JWT-Extended==4.6.0
pip install Flask-SQLAlchemy==3.1.1
pip install requests==2.31.0
pip install python-dotenv==1.0.0

echo 📊 Installing data processing libraries...
pip install numpy==1.24.3
pip install pandas==2.0.3
pip install scikit-learn==1.3.0

echo 🔧 Installing remaining dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo ⚙️ Creating .env file...
    copy .env.example .env
    echo 📝 Environment file created with your API keys
)

REM Initialize database
echo 🗄️ Initializing database...
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('✅ Database initialized')"

REM Test API connections
echo 🔌 Testing API connections...
python -c "import os; from dotenv import load_dotenv; load_dotenv(); apis = {'OpenWeather': os.getenv('OPENWEATHER_API_KEY'), 'Carbon Interface': os.getenv('CARBON_INTERFACE_KEY'), 'OpenAQ': os.getenv('OPENAQ_API_KEY'), 'Tomorrow.io': os.getenv('TOMORROW_API_KEY'), 'AirVisual': os.getenv('AIRVISUAL_API_KEY')}; print('API Key Status:'); [print(f'  {api}: {"✅ Configured" if key else "❌ Missing"}') for api, key in apis.items()]"

echo.
echo 🚀 Starting Flask development server...
echo    Backend will be available at: http://127.0.0.1:5000
echo    API Health Check: http://127.0.0.1:5000/api/health
echo.
echo 📱 To start the frontend (open new command prompt):
echo    1. npm install
echo    2. npm run dev
echo.
echo Press Ctrl+C to stop the server
echo.

REM Set environment variables for Flask
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=True

REM Run Flask app
python app.py

pause
