#!/bin/bash

# Hotel Booking Chatbot Startup Script
# This script sets up and runs the Rasa chatbot

set -e  # Exit on error

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "=========================================="
echo "  Hotel Booking Chatbot - Startup"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup first:"
    echo "  python3 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo "  python -m rasa train"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check if model exists
if [ ! -d "models" ] || [ -z "$(ls -A models 2>/dev/null)" ]; then
    echo "❌ No trained model found!"
    echo "Training model now..."
    python -m rasa train
fi

# Check if action server is already running
if lsof -Pi :5055 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Action server already running on port 5055"
else
    echo "🚀 Starting action server..."
    python -m rasa run actions --port 5055 > action_server.log 2>&1 &
    ACTION_PID=$!
    echo "Action server PID: $ACTION_PID"
    sleep 3
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "=========================================="
echo "  Starting Rasa Shell"
echo "=========================================="
echo ""
echo "Type your messages to chat with the bot."
echo "Type '/stop' to exit."
echo ""

# Run Rasa shell
python -m rasa shell

# Cleanup on exit
echo ""
echo "Shutting down..."
if [ ! -z "$ACTION_PID" ]; then
    kill $ACTION_PID 2>/dev/null || true
fi

