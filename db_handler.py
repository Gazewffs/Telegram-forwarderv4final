"""
Database handler for the Telegram message forwarding system.
Tracks forwarded messages to avoid duplicates.
"""

import os
import json
import logging
import sqlite3
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class MessageTracker:
    """
    Tracks forwarded messages to avoid duplicates.
    Uses SQLite for storage.
    """
    
    def __init__(self, db_file='forwarded_messages.db'):
        self.db_file = db_file
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize the SQLite database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Create table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS forwarded_messages (
                    message_id INTEGER PRIMARY KEY,
                    timestamp TEXT NOT NULL
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info(f"Database initialized: {self.db_file}")
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
    
    def is_forwarded(self, message_id):
        """Check if a message was already forwarded"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute("SELECT 1 FROM forwarded_messages WHERE message_id = ?", (message_id,))
            result = cursor.fetchone() is not None
            
            conn.close()
            
            # Add debug log to see if messages are being detected as already forwarded
            if result:
                logger.info(f"Message {message_id} found in database as already forwarded")
            else:
                logger.info(f"Message {message_id} is new, not found in database")
                
            return result
        except Exception as e:
            logger.error(f"Error checking if message {message_id} was forwarded: {str(e)}")
            return False
    
    def mark_as_forwarded(self, message_id):
        """Mark a message as forwarded"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Insert the message ID with current timestamp
            cursor.execute(
                "INSERT OR REPLACE INTO forwarded_messages (message_id, timestamp) VALUES (?, ?)",
                (message_id, datetime.now().isoformat())
            )
            
            conn.commit()
            conn.close()
            logger.debug(f"Message {message_id} marked as forwarded")
        except Exception as e:
            logger.error(f"Error marking message {message_id} as forwarded: {str(e)}")
    
    def clear_old_records(self, days=30):
        """Clear old records to prevent the database from growing too large"""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM forwarded_messages WHERE timestamp < ?", (cutoff_date,))
            deleted = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            if deleted > 0:
                logger.info(f"Cleared {deleted} old message records from database")
        except Exception as e:
            logger.error(f"Error clearing old records: {str(e)}")
            
    def reset_database(self):
        """Reset/clear the entire message tracking database"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Count records before deletion
            cursor.execute("SELECT COUNT(*) FROM forwarded_messages")
            count = cursor.fetchone()[0]
            
            # Delete all records
            cursor.execute("DELETE FROM forwarded_messages")
            
            conn.commit()
            conn.close()
            
            logger.info(f"Reset message tracking database - deleted {count} message records")
            return True
        except Exception as e:
            logger.error(f"Error resetting database: {str(e)}")
            return False


class SimpleMessageTracker:
    """
    A simple in-memory message tracker with JSON file persistence.
    Can be used as a fallback if SQLite is not available.
    """
    
    def __init__(self, storage_file='forwarded_messages.json'):
        self.storage_file = storage_file
        self.forwarded_messages = set()
        self._load_from_file()
    
    def _load_from_file(self):
        """Load forwarded message IDs from JSON file"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    data = json.load(f)
                    self.forwarded_messages = set(data)
                logger.info(f"Loaded {len(self.forwarded_messages)} message IDs from {self.storage_file}")
        except Exception as e:
            logger.error(f"Error loading message IDs from file: {str(e)}")
    
    def _save_to_file(self):
        """Save forwarded message IDs to JSON file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(list(self.forwarded_messages), f)
        except Exception as e:
            logger.error(f"Error saving message IDs to file: {str(e)}")
    
    def is_forwarded(self, message_id):
        """Check if a message was already forwarded"""
        return message_id in self.forwarded_messages
    
    def mark_as_forwarded(self, message_id):
        """Mark a message as forwarded"""
        self.forwarded_messages.add(message_id)
        self._save_to_file()
