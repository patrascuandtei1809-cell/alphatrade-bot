#!/bin/bash
# AlphaTrade Bot - Linux Startup Script

echo "========================================"
echo "AlphaTrade Bot - Startup (Linux)"
echo "========================================"
echo ""

# Check if Python is installed
python3 --version >/dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "ERROR: Python 3 is not installed"
    echo "Install with: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing required packages..."
pip install -q -r requirements.txt

# Start the bot
echo ""
echo "========================================"
echo "Starting AlphaTrade Bot..."
echo "========================================"
echo ""
python bot.py

# Deactivate on exit
deactivate
