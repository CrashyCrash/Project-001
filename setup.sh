#!/bin/bash

echo "Setting up the environment..."

# Check for Python and Node.js installation
if ! command -v python3 &>/dev/null; then
    echo "Python is not installed. Please install it first."
    exit 1
fi

if ! command -v node &>/dev/null; then
    echo "Node.js is not installed. Please install it first."
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Ensure requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
pip install -r requirements.txt
fi

# Check for package.json and install npm dependencies if found
if [ -f "package.json" ]; then
    echo "Installing npm dependencies..."
npm install
fi

echo "Setup complete. Run ./launch.sh to start the program."
