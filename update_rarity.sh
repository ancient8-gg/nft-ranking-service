#!/bin/bash

# Check if contract address is provided
if [ -z "$1" ]; then
    echo "Usage: ./update_rarity.sh <contract_address>"
    echo "This script updates rarity rankings for a specific contract address."
    echo "For automatic updates at regular intervals, run: python update_rarity_ranking.py"
    exit 1
fi

CONTRACT_ADDRESS=$1

# Load environment variables
source .env

# Set the working directory to the script's directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the Python script for the specified contract
echo "Updating rarity rankings for contract $CONTRACT_ADDRESS..."
python3 update_rarity_ranking.py --contract-address $CONTRACT_ADDRESS

# Deactivate virtual environment if it was activated
if [ -d "venv" ]; then
    deactivate
fi

# Log completion
echo "Rarity update completed for contract $CONTRACT_ADDRESS at $(date)" >> rarity_update.log
echo "Rarity update completed for contract $CONTRACT_ADDRESS at $(date)" 