#!/bin/bash

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || [ "$PYTHON_MAJOR" -eq 3 -a "$PYTHON_MINOR" -lt 10 ] || [ "$PYTHON_MAJOR" -eq 3 -a "$PYTHON_MINOR" -ge 13 ]; then
    echo "Error: Python version must be between 3.10 and 3.12 (current version: $PYTHON_VERSION)"
    echo "OpenRarity requires Python >= 3.10 and < 3.13"
    exit 1
fi

echo "Using Python $PYTHON_VERSION"

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file from .env.example. Please edit it with your MongoDB connection string."
    echo "You can also adjust the RARITY_UPDATE_INTERVAL (in minutes) if needed."
fi

# Make run script executable
chmod +x update_rarity.sh

echo "Setup complete! You can now run the rarity update script with:"
echo "./update_rarity.sh <contract_address>"
echo "Or run the service with automatic updates:"
echo "python update_rarity_ranking.py" 