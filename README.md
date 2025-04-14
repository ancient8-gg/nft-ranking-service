# Rarity Service

A service that calculates and updates rarity rankings for NFT collections stored in nft-indexer using the OpenRarity library.

## Features

- Calculates rarity scores for NFT collections using OpenRarity
- Stores NFT metadata and rarity rankings in nft-indexer
- Configurable rarity calculation parameters
- Efficient bulk updates for large collections
- Error handling and logging
- Environment-based configuration

## Requirements

- **Python 3.10 or 3.11** (Note: Python 3.12+ is NOT compatible with OpenRarity)
- MongoDB
- pymongo >= 4.6.0
- python-dotenv >= 1.0.0
- schedule >= 1.2.0
- open-rarity >= 0.7.5

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rarity-service.git
cd rarity-service
```

2. **Ensure you have Python 3.10 or 3.11 installed**:
```bash
python --version
```

   If you don't have the correct Python version, you can:
   
   - Install via pyenv:
     ```bash
     pyenv install 3.10.13
     pyenv local 3.10.13
     ```
   - Or use Docker (recommended, see Docker section below)

3. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Setup the project:
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

This script will:
- Check Python version
- Create a virtual environment
- Install dependencies
- Create necessary directories
- Copy the .env.example to .env

5. Configure your settings in the .env file:
```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/nft_indexer

# Update Configuration
RARITY_UPDATE_INTERVAL=15  # Update interval in minutes

# Logging Configuration
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

## Usage

### Running Locally

1. Start the service (automatic updates):
```bash
python src/main.py
```

2. Update rarity rankings for a specific contract:
```bash
chmod +x scripts/update_rarity.sh
./scripts/update_rarity.sh <contract_address>
```

3. Run one-time update for all collections:
```bash
python src/main.py --run-once
```

### Running with Docker (Recommended)

Using Docker is recommended as it bundles the correct Python version and all dependencies:

1. Make sure your `.env` file is configured correctly with the MongoDB connection string.

2. Build the Docker image:
```bash
docker build -t rarity-service .
```

3. Run the container:
```bash
docker run -d --name rarity-service --env-file .env rarity-service
```

4. Check the logs:
```bash
docker logs -f rarity-service
```

5. To update rarity rankings for a specific contract:
```bash
docker exec -it rarity-service python src/main.py --contract-address <contract_address>
```

6. Stop and remove the container:
```bash
docker stop rarity-service
docker rm rarity-service
```

#### Docker Notes

- If your MongoDB is running on the host machine, use `host.docker.internal` instead of `localhost` in the MongoDB URI.
- For MongoDB with authentication:
  ```
  MONGODB_URI=mongodb://username:password@your-mongodb-host:27017/nft_indexer
  ```

## Project Structure

```
rarity-service/
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── requirements.txt
├── setup.py
├── logs/
│   └── .gitkeep
├── scripts/
│   ├── setup.sh
│   └── update_rarity.sh
└── src/
    ├── main.py
    └── rarity_service/
        ├── __init__.py
        ├── cli.py
        ├── config.py
        ├── scheduler.py
        └── updater.py
``` 