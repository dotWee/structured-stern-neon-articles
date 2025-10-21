#!/usr/bin/env python3
"""
Import JSONL data into MongoDB.
Usage: python import_jsonl_to_mongodb.py [jsonl_file]
"""
import json
import sys
from pymongo import MongoClient
import os

# Default file if not specified
DEFAULT_JSONL_FILE = 'stern_neon_user_poetry.jsonl'

def import_jsonl_to_mongodb(jsonl_file):
    """Import JSONL data into MongoDB."""
    # MongoDB connection settings
    mongo_host = os.environ.get('MONGO_HOST', 'localhost')
    mongo_port = int(os.environ.get('MONGO_PORT', 27017))
    mongo_user = os.environ.get('MONGO_USER', 'admin')
    mongo_password = os.environ.get('MONGO_PASSWORD', 'password')
    mongo_db = os.environ.get('MONGO_DB', 'stern_neon_db')
    mongo_collection = os.environ.get('MONGO_COLLECTION', 'articles')
    
    # Connect to MongoDB
    connection_string = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/?authSource=admin"
    client = MongoClient(connection_string)
    db = client[mongo_db]
    collection = db[mongo_collection]
    
    # Read and import JSONL file
    count = 0
    batch_size = 10
    batch = []
    
    print(f"Importing data from {jsonl_file} to MongoDB ({mongo_host}:{mongo_port})...")
    print(f"Database: {mongo_db}, Collection: {mongo_collection}")
    
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
                
            try:
                # Parse JSON line
                document = json.loads(line)
                
                # Add to batch
                batch.append(document)
                count += 1
                
                # Insert batch when it reaches batch_size
                if len(batch) >= batch_size:
                    collection.insert_many(batch)
                    print(f"Imported {count} documents...")
                    batch = []
                    
            except json.JSONDecodeError as e:
                print(f"Error parsing line {line_num}: {e}")
            except Exception as e:
                print(f"Error importing line {line_num}: {e}")
    
    # Insert remaining documents
    if batch:
        collection.insert_many(batch)
    
    print(f"Import complete. Total documents imported: {count}")
    
    # Create index on 'id' field for faster lookups
    if count > 0:
        print("Creating index on 'id' field...")
        collection.create_index('id')
        print("Index created.")

if __name__ == '__main__':
    # Get JSONL file from command line argument or use default
    jsonl_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_JSONL_FILE
    
    if not os.path.exists(jsonl_file):
        print(f"Error: File '{jsonl_file}' not found.")
        sys.exit(1)
        
    import_jsonl_to_mongodb(jsonl_file)
