# NFT Rarity Ranking Service

This service calculates and updates rarity rankings for NFT collections stored in MongoDB. It uses the OpenRarity library to compute rarity scores and ranks based on NFT attributes.

## Features

- Calculates rarity rankings for NFT collections
- Updates both metadata and nft_search collections with rarity data
- Supports bulk operations for efficient updates
- Configurable update intervals

## Requirements

- Python >= 3.10, < 3.13 (required for OpenRarity compatibility)
- MongoDB database
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository
2. Run the setup script:
   ```
   chmod +x setup.sh
   ./setup.sh
   ```
   
   This will:
   - Check Python version compatibility
   - Create a virtual environment
   - Install dependencies
   - Create a .env file from .env.example if it doesn't exist
   - Make the update_rarity.sh script executable

## Configuration

The setup script will create a `.env` file if it doesn't exist. Edit this file with your MongoDB connection string and update interval:

```
MONGODB_URI=your_mongodb_connection_string
RARITY_UPDATE_INTERVAL=15  # Update interval in minutes (default: 15)
```

## Usage

### Running the Service

To start the service with automatic updates:

```
python update_rarity_ranking.py
```

This will:
- Run an initial update immediately
- Schedule updates every `RARITY_UPDATE_INTERVAL` minutes
- Log all operations to console

### Updating a Specific Collection

To update a specific NFT collection:

```
./update_rarity.sh <contract_address>
```

Example:
```
./update_rarity.sh 0x58ca3e72102871cf795908bd13e01df8b38b671e
```

## Logging

The service logs all operations to console output, including:
- Update start and completion times
- Number of NFTs processed
- Success/failure of operations
- Any errors encountered

## Error Handling

The service includes robust error handling:
- Invalid environment variables default to safe values
- Failed NFT conversions are logged but don't stop the process
- Database connection issues are logged
- Keyboard interrupts are handled gracefully

## MongoDB Collections

The service updates two collections:
- `metadata`: Contains detailed NFT metadata
- `nft_search`: Contains searchable NFT data

Both collections are updated with rarity information in the format:
```json
{
  "rarity": {
    "score": float,
    "rank": integer,
    "updatedAt": datetime
  }
}
```

## Version Control

This project includes a `.gitignore` file to exclude sensitive information and dependencies from version control:

- `.env` file containing sensitive connection strings
- Virtual environment directories (`venv/`, `env/`)
- Python cache files and compiled code
- IDE-specific files
- MongoDB data directories
- Temporary files

Always ensure your `.env` file is not committed to the repository to protect sensitive information.

## Project Structure

- `update_rarity_ranking.py`: Main script for calculating and updating rarity rankings
- `requirements.txt`: Python dependencies
- `setup.sh`: Setup script for initial configuration
- `update_rarity.sh`: Convenience script for running updates
- `.env.example`: Example environment variables file
- `.env`: Configuration file (created during setup)

## How It Works

1. **Data Fetching**: 
   - Retrieves all NFTs for a given contract address from the MongoDB database
   - Supports case-insensitive contract address matching

2. **Rarity Calculation**:
   - Uses OpenRarity algorithm for standardized rarity calculation
   - Considers trait frequency and correlations
   - Generates normalized rarity scores

3. **Database Updates**:
   - Updates both metadata and nft_search collections
   - Uses bulk operations for better performance
   - Updates include:
     - Rarity score
     - Rank
     - Update timestamp

4. **Logging**:
   - Detailed logging of all operations
   - Success/failure status for each update
   - Number of NFTs processed and updated

## Dependencies

Main dependencies (see requirements.txt for complete list):
- pymongo>=4.6.0: MongoDB driver
- python-dotenv>=1.0.0: Environment variable management
- open-rarity: OpenRarity standard implementation (requires Python >= 3.10 and < 3.13)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 