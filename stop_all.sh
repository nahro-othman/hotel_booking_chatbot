#!/bin/bash

# Hotel Booking Chatbot - Stop All Components

echo "=========================================="
echo "🛑 Stopping Hotel Booking Chatbot"
echo "=========================================="
echo ""

# Check if .pids file exists
if [ -f ".pids" ]; then
    echo "Reading PIDs from .pids file..."
    while read pid; do
        if ps -p $pid > /dev/null 2>&1; then
            echo "Stopping process $pid..."
            kill $pid
        fi
    done < .pids
    rm .pids
    echo "✅ All processes stopped!"
else
    echo "No .pids file found. Stopping by port..."
    
    # Stop by port
    echo "Stopping Rasa (port 5005)..."
    lsof -ti:5005 | xargs kill -9 2>/dev/null
    
    echo "Stopping Actions (port 5055)..."
    lsof -ti:5055 | xargs kill -9 2>/dev/null
    
    echo "Stopping Web UI (port 5001)..."
    lsof -ti:5001 | xargs kill -9 2>/dev/null
    
    echo "✅ All processes stopped!"
fi

echo ""
echo "=========================================="

