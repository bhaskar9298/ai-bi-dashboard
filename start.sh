#!/bin/bash

# AI BI Dashboard - Quick Start Script
# This script sets up and runs the entire application

echo "=========================================="
echo "🚀 AI BI Dashboard Quick Start"
echo "=========================================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+"
    exit 1
fi
echo "✅ Python found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

# Check MongoDB
if ! command -v mongosh &> /dev/null && ! command -v mongo &> /dev/null; then
    echo "⚠️  MongoDB CLI not found. Make sure MongoDB is running."
else
    echo "✅ MongoDB CLI found"
fi

echo ""
echo "=========================================="
echo "📦 Setting up Backend..."
echo "=========================================="
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q -r requirements.txt

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "❗ Please edit backend/.env and add your API keys!"
    echo "   Required: GOOGLE_API_KEY or OPENAI_API_KEY"
    read -p "Press Enter after updating .env file..."
fi

# Generate mock data
echo ""
echo "📊 Generating mock data..."
python generate_mock_db.py

# Start backend in background
echo ""
echo "🚀 Starting backend server..."
python app.py &
BACKEND_PID=$!
echo "Backend running on PID: $BACKEND_PID"

cd ..

echo ""
echo "=========================================="
echo "🎨 Setting up Frontend..."
echo "=========================================="
cd frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Start frontend
echo ""
echo "🚀 Starting frontend..."
npm start

# Cleanup on exit
trap "echo 'Stopping servers...'; kill $BACKEND_PID; exit" INT TERM
