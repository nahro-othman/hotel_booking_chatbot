#!/bin/bash

# Hotel Booking Chatbot Setup Script
# Run this once to set up the project

set -e  # Exit on error

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

echo "=========================================="
echo "  Hotel Booking Chatbot - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "🔍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

echo "Found Python $PYTHON_VERSION"

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo ""
    echo "❌ ERROR: Python 3.10+ is required for Rasa 3.6"
    echo "You have Python $PYTHON_VERSION"
    echo ""
    echo "Please install Python 3.10 or higher:"
    echo "  - Download from: https://www.python.org/downloads/"
    echo "  - Or use Homebrew: brew install python@3.10"
    echo ""
    echo "After installing, you may need to use:"
    echo "  python3.10 -m venv .venv"
    echo "  source .venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

echo "✅ Python version OK"
echo ""

# Create virtual environment
if [ -d ".venv" ]; then
    echo "⚠️  Virtual environment already exists. Removing old one..."
    rm -rf .venv
fi

echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Train model
echo ""
echo "🎓 Training Rasa model..."
python -m rasa train

echo ""
echo "=========================================="
echo "  ✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To run the chatbot:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source .venv/bin/activate"
echo "  python -m rasa run actions (Terminal 1)"
echo "  python -m rasa shell (Terminal 2)"
echo ""

