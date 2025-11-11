#!/bin/bash

# Hotel Booking Chatbot Stop Script
# Stops all running Rasa processes

echo "=========================================="
echo "  Stopping Hotel Booking Chatbot"
echo "=========================================="
echo ""

# Find and kill Rasa action server
if lsof -Pi :5055 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "🛑 Stopping action server on port 5055..."
    lsof -ti:5055 | xargs kill -9 2>/dev/null || true
    echo "✅ Action server stopped"
else
    echo "ℹ️  No action server running on port 5055"
fi

# Kill any remaining Rasa processes
RASA_PIDS=$(pgrep -f "rasa" 2>/dev/null || true)
if [ ! -z "$RASA_PIDS" ]; then
    echo "🛑 Stopping other Rasa processes..."
    echo "$RASA_PIDS" | xargs kill -9 2>/dev/null || true
    echo "✅ All Rasa processes stopped"
else
    echo "ℹ️  No other Rasa processes found"
fi

# Clean up log files
if [ -f "action_server.log" ]; then
    rm action_server.log
    echo "🧹 Cleaned up log files"
fi

echo ""
echo "✅ Shutdown complete!"

