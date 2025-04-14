"""Configuration module for the Rarity Service."""

import os
import logging
from dotenv import load_dotenv

# Configure logging
def setup_logging():
    """Set up logging configuration."""
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format=log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('logs/rarity_service.log')
        ]
    )
    
    return logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger = setup_logging()

# MongoDB configuration
MONGODB_URI = os.getenv('MONGODB_URI')
if not MONGODB_URI:
    logger.error("MONGODB_URI environment variable not set")
    raise ValueError("MONGODB_URI environment variable not set")

# Update interval configuration
try:
    UPDATE_INTERVAL_MINUTES = int(os.getenv('RARITY_UPDATE_INTERVAL', '15'))
    if UPDATE_INTERVAL_MINUTES < 1:
        logger.warning("RARITY_UPDATE_INTERVAL is less than 1 minute, defaulting to 15 minutes")
        UPDATE_INTERVAL_MINUTES = 15
    logger.info(f"Using update interval of {UPDATE_INTERVAL_MINUTES} minutes from environment")
except ValueError:
    logger.warning("Invalid RARITY_UPDATE_INTERVAL value in environment, defaulting to 15 minutes")
    UPDATE_INTERVAL_MINUTES = 15 