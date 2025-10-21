# MongoDB Setup for Stern Neon Dataset

This guide explains how to set up MongoDB using Docker and import your JSONL dataset.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.6+ with pip
- JSONL dataset file (e.g., `stern_neon_user_poetry.jsonl`)

## Setup Instructions

### 1. Start MongoDB with Docker Compose

```bash
# Start the MongoDB container and Mongo Express web UI
docker-compose up -d
```

This will start:
- MongoDB server on port 27017
- Mongo Express web UI on port 8081

### 2. Install Python Dependencies

```bash
# Install required Python package
pip install pymongo
```

### 3. Import JSONL Data into MongoDB

```bash
# Import the default file (stern_neon_user_poetry.jsonl)
python import_jsonl_to_mongodb.py

# Or specify a different file
python import_jsonl_to_mongodb.py normalized_entries.jsonl
```

## Accessing MongoDB

### Connection Details

- **Host**: localhost
- **Port**: 27017
- **Username**: admin
- **Password**: password
- **Database**: stern_neon_db
- **Collection**: articles

### Using Mongo Express

Access the web UI at: http://localhost:8081

### Using MongoDB Shell

```bash
# Connect to MongoDB container
docker exec -it mongo mongosh -u admin -p password

# Select database
use stern_neon_db

# Query documents
db.articles.find().limit(5)
```

## Environment Variables

You can customize the MongoDB connection by setting these environment variables:

```bash
export MONGO_HOST=localhost
export MONGO_PORT=27017
export MONGO_USER=admin
export MONGO_PASSWORD=password
export MONGO_DB=stern_neon_db
export MONGO_COLLECTION=articles
```

## Data Structure

The imported documents will maintain the same structure as in your JSONL file, with each entry having fields like:
- `id`: Unique identifier
- `title`: Article title
- `subtitle`: Article subtitle
- `text`: Main content
- Other fields from your dataset

An index is automatically created on the `id` field for faster lookups.
