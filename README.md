# NFT Rarity Ranking Service

A service that calculates and updates rarity rankings for NFT collections stored in MongoDB using the OpenRarity library.

## Features

- Calculates rarity scores for NFT collections using OpenRarity
- Stores NFT metadata and rarity rankings in MongoDB
- Supports multiple blockchain networks (Ethereum, Polygon, etc.)
- Configurable rarity calculation parameters
- Efficient bulk updates for large collections
- Error handling and logging
- Environment-based configuration

## Requirements

- Python 3.8+
- MongoDB
- OpenRarity library
- Web3.py
- Required Python packages (see requirements.txt)

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
MONGODB_DB=nft_ranking
MONGODB_COLLECTION=nft_search

# Blockchain Configuration
ETHEREUM_RPC_URL=https://mainnet.infura.io/v3/your-project-id
POLYGON_RPC_URL=https://polygon-rpc.com

# OpenRarity Configuration
RARITY_WEIGHTS={"trait_count": 0.3, "statistical_rarity": 0.7}
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

Logs are stored in the `logs` directory:
- `nft_ranking.log`: Main application logs
- `error.log`: Error logs

## Error Handling

The service includes comprehensive error handling for:
- MongoDB connection issues
- Blockchain RPC failures
- Invalid NFT metadata
- Rate limiting
- Network timeouts

## Project Structure

```
nft-ranking-service/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── setup.sh
├── update_rarity.sh
├── update_rarity_ranking.py
└── logs/
    ├── nft_ranking.log
    └── error.log
``` 