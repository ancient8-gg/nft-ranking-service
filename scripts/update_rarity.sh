#!/bin/bash

# Check if contract address is provided
if [ -z "$1" ]; then
    echo "Usage: ./scripts/update_rarity.sh <contract_address>"
    echo "This script updates rarity rankings for a specific contract address."
    echo "For automatic updates at regular intervals, run: python src/main.py"
    exit 1
fi

CONTRACT_ADDRESS=$1

# Set the working directory to the project's root directory
cd "$(dirname "$0")/.."

# Load environment variables
if [ -f ".env" ]; then
    source .env
else
    echo "Warning: .env file not found. Using default environment settings."
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the Python script for the specified contract
echo "Updating rarity rankings for contract $CONTRACT_ADDRESS..."
python src/main.py --contract-address $CONTRACT_ADDRESS

# Deactivate virtual environment if it was activated
if [ -d "venv" ]; then
    deactivate
fi

# Log completion
echo "Rarity update completed for contract $CONTRACT_ADDRESS at $(date)" >> logs/rarity_update.log
echo "Rarity update completed for contract $CONTRACT_ADDRESS at $(date)" 