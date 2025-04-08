import os
import argparse
import logging
import time
from datetime import datetime
from typing import Dict, List, Any
import schedule

from pymongo import MongoClient
from open_rarity import Collection, Token, RarityRanker
from dotenv import load_dotenv
from pymongo.operations import UpdateOne

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get update interval from environment with validation (in minutes)
try:
    UPDATE_INTERVAL_MINUTES = int(os.getenv('RARITY_UPDATE_INTERVAL', '15'))
    if UPDATE_INTERVAL_MINUTES < 1:
        logger.warning("RARITY_UPDATE_INTERVAL is less than 1 minute, defaulting to 15 minutes")
        UPDATE_INTERVAL_MINUTES = 15
    logger.info(f"Using update interval of {UPDATE_INTERVAL_MINUTES} minutes from environment")
except ValueError:
    logger.warning("Invalid RARITY_UPDATE_INTERVAL value in environment, defaulting to 15 minutes")
    UPDATE_INTERVAL_MINUTES = 15

class RarityRankingUpdater:
    def __init__(self, connection_string: str):
        """Initialize the updater with MongoDB connection string."""
        self.client = MongoClient(connection_string)
        self.db = self.client.get_database('nft_indexer')
        self.logger = logger
        
    def get_all_contract_addresses(self) -> List[str]:
        """Get all unique contract addresses from the metadata collection."""
        return list(self.db['metadata'].distinct('address'))
        
    def fetch_nfts_by_contract(self, contract_address: str) -> List[Dict[str, Any]]:
        """Fetch all NFTs from the specified contract address."""
        contract_address = contract_address.lower()
        return list(self.db['metadata'].find({'address': contract_address}))
    
    def convert_to_token(self, nft_data: Dict[str, Any], token_id: int) -> Token:
        """Convert MongoDB NFT data to OpenRarity Token format."""
        metadata = {}
        
        if 'attributes' in nft_data:
            for trait in nft_data['attributes']:
                if isinstance(trait, dict) and 'traitType' in trait and 'value' in trait:
                    metadata[trait['traitType']] = trait['value']
        else:
            raise ValueError("No metadata found in the NFT data")

        contract_address = nft_data.get('address', '0x0')
        actual_token_id = int(nft_data.get('tokenId', token_id))
        
        return Token.from_erc721(
            contract_address=contract_address,
            token_id=actual_token_id,
            metadata_dict=metadata
        )
    
    def calculate_rarity_rankings(self, contract_address: str, tokens: List[Token]) -> List[Dict[str, Any]]:
        """Calculate rarity rankings for the collection."""
        collection = Collection(
            name=f"Collection_{contract_address}",
            tokens=tokens
        )

        ranked_tokens = RarityRanker.rank_collection(collection=collection)
        
        rankings = []
        for ranked_token in ranked_tokens:
            token_id = ranked_token.token.token_identifier.token_id
            rankings.append({
                'token_id': token_id,
                'rank': ranked_token.rank,
                'score': float(ranked_token.score),
            })
        
        return rankings
    
    def update_metadata_with_rarity(self, contract_address: str, rankings: List[Dict[str, Any]]) -> None:
        """
        Update metadata collection with rarity data using bulk operations
        """
        try:
            # First, query and log the number of NFTs that will be updated
            token_ids = [str(ranking['token_id']) for ranking in rankings]
            
            # Query metadata collection
            metadata_count = self.db['metadata'].count_documents({
                'address': {'$regex': f'^{contract_address}$', '$options': 'i'},
                'tokenId': {'$in': token_ids}
            })
            
            # Query nft_search collection
            nft_search_count = self.db['nft_search'].count_documents({
                'address': {'$regex': f'^{contract_address}$', '$options': 'i'},
                'tokenId': {'$in': token_ids}
            })
            
            self.logger.info(f"Found {metadata_count} NFTs to update in metadata collection")
            self.logger.info(f"Found {nft_search_count} NFTs to update in nft_search collection")
            
            if metadata_count == 0 and nft_search_count == 0:
                self.logger.warning("No NFTs found to update in either collection")
                return
            
            # Prepare bulk operations for metadata collection
            metadata_bulk = []
            # Prepare bulk operations for nft_search collection
            nft_search_bulk = []
            
            for ranking in rankings:
                token_id = str(ranking['token_id'])
                
                # Create the rarity object according to the metadata entity structure
                rarity_data = {
                    'score': ranking['score'],
                    'rank': ranking['rank'],
                    'updatedAt': datetime.now()
                }
                
                # Add operations to bulk with case-insensitive address comparison
                metadata_bulk.append(UpdateOne(
                    {
                        'address': {'$regex': f'^{contract_address}$', '$options': 'i'},
                        'tokenId': token_id
                    },
                    {
                        '$set': {
                            'rarity': rarity_data
                        }
                    }
                ))
                
                nft_search_bulk.append(UpdateOne(
                    {
                        'address': {'$regex': f'^{contract_address}$', '$options': 'i'},
                        'tokenId': token_id
                    },
                    {
                        '$set': {
                            'rarity': rarity_data
                        }
                    }
                ))
            
            # Execute bulk operations if we have any
            if metadata_bulk:
                metadata_result = self.db['metadata'].bulk_write(metadata_bulk)
                nft_search_result = self.db['nft_search'].bulk_write(nft_search_bulk)
                
                self.logger.info(f"Bulk update completed. Metadata modified: {metadata_result.modified_count}, "
                               f"NFT Search modified: {nft_search_result.modified_count}")
            
        except Exception as e:
            self.logger.error(f"Error updating rarity data: {str(e)}")
            raise
    
    def update_collection_rarity(self, contract_address: str) -> bool:
        """Main method to update rarity rankings for an NFT collection."""
        try:
            logger.info(f"Fetching NFTs for contract: {contract_address}")
            nfts = self.fetch_nfts_by_contract(contract_address)
            logger.info(f"Found {len(nfts)} NFTs")
            
            if not nfts:
                logger.warning("No NFTs found for this contract address")
                return False
            
            logger.info("Converting NFTs to OpenRarity format...")
            tokens = []
            for i, nft in enumerate(nfts):
                try:
                    token = self.convert_to_token(nft, i + 1)
                    tokens.append(token)
                except Exception as e:
                    logger.error(f"Error converting NFT {i}: {str(e)}")
                    continue
            
            logger.info(f"Successfully converted {len(tokens)} NFTs")
            
            logger.info("Calculating rarity rankings...")
            rankings = self.calculate_rarity_rankings(contract_address, tokens)
            
            # Sort by rank
            rankings.sort(key=lambda x: x['rank'])
            
            # Update the metadata collection with rarity rankings
            logger.info("Updating metadata with rarity rankings...")
            self.update_metadata_with_rarity(contract_address, rankings)
            
            logger.info(f"Successfully updated rarity rankings for contract {contract_address}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating rarity rankings: {str(e)}")
            return False

    def update_all_collections(self) -> None:
        """Update rarity rankings for all collections in the database."""
        contracts = self.get_all_contract_addresses()
        logger.info(f"Found {len(contracts)} contracts to update")
        
        for contract in contracts:
            logger.info(f"\n{'='*50}\nProcessing contract: {contract}\n{'='*50}")
            self.update_collection_rarity(contract)
            
        logger.info("Completed updating all collections")
    
    def close(self):
        """Close MongoDB connection."""
        self.client.close()

def run_scheduled_updates():
    """Run the rarity update on a schedule."""
    connection_string = os.getenv('MONGODB_URI')
    if not connection_string:
        logger.error("MONGODB_URI environment variable not set")
        return

    def update_job():
        try:
            logger.info(f"Starting scheduled update at {datetime.now()}")
            updater = RarityRankingUpdater(connection_string)
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
    
    logger.info(f"Scheduled rarity updates every {UPDATE_INTERVAL_MINUTES} minutes")
    
    # Keep the script running
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Rarity update service stopped by user")
            break
        except Exception as e:
            logger.error(f"Error in scheduler: {str(e)}")
            time.sleep(60)

def main():
    parser = argparse.ArgumentParser(description='Update NFT rarity rankings')
    parser.add_argument('--contract-address', type=str, help='Contract address to update (optional)', required=False)
    
    args = parser.parse_args()
    
    if args.contract_address:
        # Update specific contract
        connection_string = os.getenv('MONGODB_URI')
        if not connection_string:
            logger.error("MONGODB_URI environment variable not set")
            return
        
        updater = RarityRankingUpdater(connection_string)
        try:
            updater.update_collection_rarity(args.contract_address)
        finally:
            updater.close()
    else:
        # Run scheduled updates
        run_scheduled_updates()

if __name__ == "__main__":
    main() 