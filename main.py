#!/usr/bin/env python3
"""
Telegram Message Forwarder - Main Entry Point
This script initializes and runs the Telegram message forwarding system.
"""

import os
import sys
import time
import logging
import asyncio
import argparse
from telethon import TelegramClient, events
from telethon.sessions import StringSession

from config import Config
from forwarder import TelegramForwarder

# Import app from app.py for Gunicorn to work
from app import app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('forwarder.log')
    ]
)
logger = logging.getLogger(__name__)

async def main():
    """Main function that initializes and runs the forwarder"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Telegram Message Forwarder')
    parser.add_argument('--config', type=str, default='config.json', help='Path to config file')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    args = parser.parse_args()
    
    # Set debug logging if requested
    if args.debug:
        logger.setLevel(logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")
    
    logger.info("Starting Telegram message forwarder...")
    
    # Load configuration
    config = Config(args.config)
    if not config.is_valid():
        logger.error("Invalid configuration. Please set up your config file correctly or use the web interface at http://localhost:5000")
        return
    
    # Initialize the Telegram client
    try:
        # Use string session if available, otherwise use regular session
        if config.session_string:
            client = TelegramClient(StringSession(config.session_string), 
                                   config.api_id, 
                                   config.api_hash)
        else:
            client = TelegramClient('telegram_forwarder', 
                                   config.api_id, 
                                   config.api_hash)

        logger.info("Connecting to Telegram...")
        await client.start()
        
        # Save session string for future use
        if not config.session_string:
            config.session_string = client.session.save()
            config.save()
            logger.info("Session string saved for future use")
            
        # Initialize the forwarder
        forwarder = TelegramForwarder(client, config)
        
        # Start forwarding messages
        await forwarder.start_forwarding()
        
        # Keep the script running
        logger.info("Forwarder is now running. Press Ctrl+C to stop.")
        while True:
            await asyncio.sleep(3600)  # Keep the script running
            
    except KeyboardInterrupt:
        logger.info("Stopping forwarder due to keyboard interrupt...")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}", exc_info=True)
    finally:
        if 'client' in locals() and client.is_connected():
            await client.disconnect()
            logger.info("Disconnected from Telegram")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.critical(f"Critical error: {str(e)}", exc_info=True)
