"""Scheduler module for running regular rarity updates."""

import time
import logging
from datetime import datetime
import schedule

from rarity_service.config import MONGODB_URI, UPDATE_INTERVAL_MINUTES
from rarity_service.updater import RarityRankingUpdater

logger = logging.getLogger(__name__)

def run_scheduled_updates():
    """Run the rarity update on a schedule."""
    if not MONGODB_URI:
        logger.error("MONGODB_URI environment variable not set")
        return

    def update_job():
        try:
            logger.info(f"Starting scheduled update at {datetime.now()}")
            updater = RarityRankingUpdater(MONGODB_URI)
            try:
                updater.update_all_collections()
            finally:
                updater.close()
            logger.info(f"Completed scheduled update at {datetime.now()}")
        except Exception as e:
            logger.error(f"Error in scheduled update: {str(e)}")

    # Schedule the job to run every UPDATE_INTERVAL_MINUTES minutes
    schedule.every(UPDATE_INTERVAL_MINUTES).minutes.do(update_job)
    
    # Run the job immediately on startup
    update_job()
    
    # Keep the script running to execute scheduled tasks
    logger.info(f"Scheduler started. Next update in {UPDATE_INTERVAL_MINUTES} minutes.")
    while True:
        schedule.run_pending()
        time.sleep(1)

def run_once():
    """Run one-time update for all collections."""
    try:
        logger.info("Starting one-time update")
        updater = RarityRankingUpdater(MONGODB_URI)
        try:
            updater.update_all_collections()
        finally:
            updater.close()
        logger.info("One-time update completed")
    except Exception as e:
        logger.error(f"Error in one-time update: {str(e)}")
        return False
    return True

def update_contract(contract_address):
    """Run update for a specific contract."""
    try:
        logger.info(f"Starting update for contract: {contract_address}")
        updater = RarityRankingUpdater(MONGODB_URI)
        try:
            result = updater.update_collection_rarity(contract_address)
        finally:
            updater.close()
        
        if result:
            logger.info(f"Update for contract {contract_address} completed successfully")
        else:
            logger.warning(f"Update for contract {contract_address} failed")
        return result
    except Exception as e:
        logger.error(f"Error updating contract {contract_address}: {str(e)}")
        return False 