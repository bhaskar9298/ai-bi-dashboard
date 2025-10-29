@echo off
REM AI BI Dashboard - Quick Start Script for Windows
REM This script sets up and runs the entire application

echo ==========================================
echo 🚀 AI BI Dashboard Quick Start
echo ==========================================
echo.

echo 📋 Checking prerequisites...

REM Check Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+
    pause
    exit /b 1
)
echo ✅ Python found

REM Check Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 16+
    pause
    exit /b 1
)
echo ✅ Node.js found

echo.
echo ==========================================
echo 📦 Setting up Backend...
echo ==========================================
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -q -r requirements.txt

REM Check .env file
if not exist ".env" (
    echo ⚠️  .env file not found. Copying from .env.example...
    copy .env.example .env
    echo ❗ Please edit backend\.env and add your API keys!
    echo    Required: GOOGLE_API_KEY or OPENAI_API_KEY
    pause
)

REM Generate mock data
echo.
echo 📊 Generating mock data...
python generate_mock_db.py

REM Start backend
echo.
echo 🚀 Starting backend server...
start cmd /k "python app.py"

cd ..

echo.
echo ==========================================
echo 🎨 Setting up Frontend...
echo ==========================================
cd frontend

REM Install dependencies
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
)

REM Start frontend
echo.
echo 🚀 Starting frontend...
call npm start

pause
