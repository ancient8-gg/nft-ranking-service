# NFT Rarity Ranking Service

A service that calculates and updates rarity rankings for NFT collections stored in nft-indexer using the OpenRarity library.

## Features

- Calculates rarity scores for NFT collections using OpenRarity
- Stores NFT metadata and rarity rankings in nft-indexer
- Configurable rarity calculation parameters
- Efficient bulk updates for large collections
- Error handling and logging
- Environment-based configuration

## Requirements

- Python >= 3.10, < 3.13 (required for OpenRarity compatibility)
- MongoDB
- pymongo >= 4.6.0
- python-dotenv >= 1.0.0
- schedule >= 1.2.0
- OpenRarity (from GitHub)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nft-ranking-service.git
cd nft-ranking-service
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file and configure your settings:
```bash
cp .env.example .env
```

## Configuration

Edit the `.env` file with your settings:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017

# Update Configuration
RARITY_UPDATE_INTERVAL=15  # Update interval in minutes
```

## Usage

1. Start the service:
```bash
./setup.sh
```

2. Update rarity rankings:
```bash
./update_rarity.sh
```

## Logging

The service logs all operations to console output, including:
- Update start and completion times
- Number of NFTs processed
- Success/failure of operations
- Any errors encountered

## Error Handling

The service includes comprehensive error handling for:
- MongoDB connection issues
- Invalid NFT metadata

## Project Structure

```
nft-ranking-service/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── setup.sh
├── update_rarity.sh
└── update_rarity_ranking.py
``` 