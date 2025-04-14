"""Command-line interface for the Rarity Service."""

import argparse
import logging
import sys

from rarity_service.scheduler import run_scheduled_updates, run_once, update_contract

logger = logging.getLogger(__name__)

def main():
    """Main function to handle command-line arguments and execution."""
    parser = argparse.ArgumentParser(
        description="NFT Rarity Ranking Service"
    )
    
    # Define command-line arguments
    parser.add_argument(
        "--contract-address",
        help="Contract address to update rarity rankings for a specific collection"
    )
    
    parser.add_argument(
        "--run-once",
        action="store_true",
        help="Run update once for all collections and exit"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the appropriate function based on arguments
    try:
        if args.contract_address:
            logger.info(f"Running update for contract address: {args.contract_address}")
            if not update_contract(args.contract_address):
                logger.error(f"Failed to update contract {args.contract_address}")
                sys.exit(1)
        elif args.run_once:
            logger.info("Running one-time update for all collections")
            if not run_once():
                logger.error("Failed to run one-time update")
                sys.exit(1)
        else:
            logger.info("Starting scheduled updates")
            run_scheduled_updates()
    except KeyboardInterrupt:
        logger.info("Service interrupted, shutting down")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
    
if __name__ == "__main__":
    main() 