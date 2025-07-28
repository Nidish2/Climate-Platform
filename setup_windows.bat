@echo off
echo 🌍 Climate Platform Windows Setup
echo ================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.11+ from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found. Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo ✅ Node.js found

REM Setup backend
echo 📦 Setting up backend...
cd backend
call run_dev.bat

REM The batch file will handle the rest
pause
