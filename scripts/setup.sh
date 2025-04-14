#!/bin/bash

# Set the working directory to the project's root directory
cd "$(dirname "$0")/.."

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || [ "$PYTHON_MAJOR" -eq 3 -a "$PYTHON_MINOR" -lt 10 ] || [ "$PYTHON_MAJOR" -eq 3 -a "$PYTHON_MINOR" -gt 11 ]; then
    echo "Error: Python version must be 3.10 or 3.11 (current version: $PYTHON_VERSION)"
    echo "OpenRarity is NOT compatible with Python 3.12 or higher"
    echo "Consider using Docker instead (see README.md) or install Python 3.10/3.11 using pyenv:"
    echo "  pyenv install 3.10.13"
    echo "  pyenv local 3.10.13"
    exit 1
fi

echo "Using Python $PYTHON_VERSION - This version is compatible with OpenRarity"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install package and dependencies
pip install -e .

# Create directories if they don't exist
mkdir -p logs

# Create .env file from example if it doesn't exist
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Created .env file from .env.example. Please edit it with your MongoDB connection string."
        echo "You can also adjust the RARITY_UPDATE_INTERVAL (in minutes) and LOG_LEVEL if needed."
    else
        echo "Warning: .env.example file not found. Please create a .env file manually."
    fi
fi

# Make scripts executable
chmod +x scripts/update_rarity.sh

echo "Setup complete! You can now run the rarity update script with:"
echo "./scripts/update_rarity.sh <contract_address>"
echo "Or run the service with automatic updates:"
echo "python src/main.py" 