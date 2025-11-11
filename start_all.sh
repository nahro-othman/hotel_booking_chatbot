#!/bin/bash

# Hotel Booking Chatbot - Start All Components
# This script starts the Rasa server, Action server, and Web UI

echo "=========================================="
echo "🏨 Hotel Booking Chatbot"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Check if model exists
if [ ! -d "models" ] || [ -z "$(ls -A models)" ]; then
    echo "❌ No trained model found!"
    echo "Please run: rasa train"
    exit 1
fi

echo "Starting components..."
echo ""

# Start Rasa server
echo "🚀 Starting Rasa Server (Port 5005)..."
source venv/bin/activate
rasa run --enable-api --cors "*" > /dev/null 2>&1 &
RASA_PID=$!
echo "   PID: $RASA_PID"

# Wait for Rasa to start
sleep 5

# Start Action server
echo "🎬 Starting Action Server (Port 5055)..."
rasa run actions > /dev/null 2>&1 &
ACTIONS_PID=$!
echo "   PID: $ACTIONS_PID"

# Wait for Actions to start
sleep 3

# Start Web UI
echo "🌐 Starting Web UI (Port 5001)..."
cd web_ui
python app.py > /dev/null 2>&1 &
UI_PID=$!
echo "   PID: $UI_PID"
cd ..

# Wait for UI to start
sleep 2

echo ""
echo "=========================================="
echo "✅ All components started!"
echo "=========================================="
echo ""
echo "🌐 Open your browser: http://localhost:5001"
echo ""
echo "To stop all servers, run:"
echo "  kill $RASA_PID $ACTIONS_PID $UI_PID"
echo ""
echo "Or save these PIDs to a file:"
echo "$RASA_PID" > .pids
echo "$ACTIONS_PID" >> .pids
echo "$UI_PID" >> .pids
echo ""
echo "Logs are suppressed. To see logs, start each component manually."
echo "=========================================="

