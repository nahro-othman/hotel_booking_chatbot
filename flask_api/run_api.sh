#!/bin/bash

# Start Flask API Server
# This script starts the Flask API server for the hotel booking chatbot

set -e

echo "======================================================"
echo "🚀 Starting Hotel Booking Chatbot API + Frontend"
echo "======================================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the parent directory
PARENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Check if virtual environment exists in parent directory
if [ ! -d "$PARENT_DIR/.venv" ]; then
    echo -e "${RED}❌ Virtual environment not found!${NC}"
    echo "Please run ./setup.sh from the root directory first"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}📦 Activating virtual environment...${NC}"
source "$PARENT_DIR/.venv/bin/activate"

# Check if Flask is installed
echo -e "${BLUE}📦 Checking Flask dependencies...${NC}"
pip show flask > /dev/null 2>&1 || pip install -q flask flask-cors requests

# Check if Rasa is running
echo -e "${BLUE}🔍 Checking Rasa server status...${NC}"
RASA_STATUS=$(curl -s http://localhost:5005/status 2>/dev/null || echo "down")
if [[ "$RASA_STATUS" == "down" ]]; then
    echo -e "${YELLOW}⚠️  Warning: Rasa server is not running!${NC}"
    echo ""
    echo "To start Rasa, open another terminal and run:"
    echo -e "${BLUE}  cd $PARENT_DIR && ./run.sh${NC}"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✅ Rasa server is running${NC}"
fi

# Start Flask API
echo ""
echo -e "${GREEN}✅ Starting Flask API + Frontend server...${NC}"
echo ""

cd "$(dirname "${BASH_SOURCE[0]}")"
python api.py

