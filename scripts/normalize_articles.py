#!/usr/bin/env python3
"""
Normalize MongoDB `articles` documents for LLM fine-tuning using an OpenAI-compatible API.
Supports concurrent processing with configurable concurrency level.

Environment variables:
  - MONGO_HOST (default: localhost)
  - MONGO_PORT (default: 27017)
  - MONGO_USER (default: admin)
  - MONGO_PASSWORD (default: password)
  - MONGO_DB (default: stern_neon_db)
  - MONGO_COLLECTION (default: articles)
  - OPENAI_API_KEY (required)
  - OPENAI_BASE_URL (optional; e.g., http://localhost:11434/v1)
  - OPENAI_MODEL (default: gpt-4o-mini)

Usage examples:
  python normalize_articles.py --limit 100 --dry-run
  python normalize_articles.py --resume-from 652e... --batch-size 20 --concurrency 5
"""
import argparse
import asyncio
import os
import sys
import time
from typing import Any, Dict, Optional, List, Tuple

from pymongo import MongoClient
from pymongo.collection import Collection
from bson import ObjectId

import aiohttp


def load_env_file(env_path: str) -> None:
    """Load key=value pairs from a .env-like file into os.environ.

    Lines starting with '#' or empty lines are ignored. Keys and values are stripped.
    Values are not unescaped; simple literal assignment only.
    """
    if not env_path:
        return
    if not os.path.exists(env_path):
        return
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                os.environ[key] = value
    except Exception as e:
        print(f"Warning: failed to load env file '{env_path}': {e}")


def get_mongo_collection() -> Collection:
    # Support both MONGODB_* and MONGO_* names, prefer MONGODB_* if present
    mongo_host = os.environ.get('MONGODB_HOST') or os.environ.get('MONGO_HOST', 'localhost')
    mongo_port = int(os.environ.get('MONGODB_PORT') or os.environ.get('MONGO_PORT', 27017))
    mongo_user = os.environ.get('MONGODB_USER') or os.environ.get('MONGO_USER', 'admin')
    mongo_password = os.environ.get('MONGODB_PASSWORD') or os.environ.get('MONGO_PASSWORD', 'password')
    mongo_db = os.environ.get('MONGODB_DATABASE') or os.environ.get('MONGO_DB', 'stern_neon_db')
    mongo_collection = os.environ.get('MONGODB_COLLECTION') or os.environ.get('MONGO_COLLECTION', 'articles')

    connection_string = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:{mongo_port}/?authSource=admin"
    client = MongoClient(connection_string)
    db = client[mongo_db]
    return db[mongo_collection]


async def normalize_text_via_openai_compatible(text: str, api_key: str, base_url: Optional[str], model: str, session: aiohttp.ClientSession, timeout: int = 60) -> str:
    """Send text to an OpenAI-compatible Chat Completions API and return normalized text.

    The function uses a simple prompt to clean and normalize content for LLM fine-tuning.
    """
    url = (base_url.rstrip('/') if base_url else 'https://api.openai.com/v1') + '/chat/completions'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }
    payload = {
        'model': model,
        'temperature': 0.1,
        'messages': [
            {
                'role': 'system',
                'content': (
                    'You are a precise text normalization assistant for preparing training data for LLM fine-tuning.\n'
                    'TASK: Normalize ONLY the provided main article text. Return ONLY the normalized text with no extra commentary, no markdown, no metadata.\n'
                    'REQUIREMENTS:\n'
                    '1) Fix obvious typos and spelling errors.\n'
                    '2) Normalize punctuation and spacing inconsistencies.\n'
                    '3) Remove excessive whitespace/newlines, but preserve intentional line breaks for poetry and paragraphs.\n'
                    '   - Allow at most three consecutive empty lines.\n'
                    '4) Ensure proper capitalization where appropriate.\n'
                    '5) Fix encoding issues or strange characters.\n'
                    '6) Maintain the original meaning, literary quality, style, and voice.\n'
                    '7) Preserve intentional formatting (e.g., poetry line breaks), but avoid over-spacing.\n'
                    '8) Remove any metadata or non-content text (e.g., headers, footers, navigation, ads).\n'
                    '9) Normalize quote characters to straight ASCII single (\'\') and double (\"\") quotes.\n'
                    'CONSTRAINTS: Do not add content. Do not summarize. Do not rephrase stylistically beyond necessary corrections. Output plain text only.'
                ),
            },
            {
                'role': 'user',
                'content': text,
            },
        ],
    }

    print(f"Sending text to {url} with model {model}")

    try:
        async with session.post(url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
            if resp.status != 200:
                response_text = await resp.text()
                raise RuntimeError(f"OpenAI-compatible API error: {resp.status} {response_text}")
            
            data = await resp.json()
            try:
                content = data['choices'][0]['message']['content']
                return content.strip()
            except Exception:
                raise RuntimeError(f"Unexpected API response format: {data}")
    except asyncio.TimeoutError:
        raise RuntimeError(f"Request timeout after {timeout} seconds")
    except Exception as e:
        raise RuntimeError(f"Request failed: {e}")


def normalize_quote_characters(text: str) -> str:
    """Normalize various curly and localized quotes to straight ASCII quotes.

    This is a deterministic post-process to ensure consistent quotes regardless of model behavior.
    """
    if not text:
        return text
    replacements = {
        '“': '"', '”': '"', '„': '"', '‟': '"', '«': '"', '»': '"',
        '‟': '"', '＂': '"',
        '‘': '\'', '’': '\'', '‚': '\'', '‛': '\'', '‹': '\'', '›': '\'', '＇': '\'',
    }
    out = text
    for src, dst in replacements.items():
        out = out.replace(src, dst)
    return out


def build_revision(original: Dict[str, Any], normalized_text: str) -> Dict[str, Any]:
    """Return a new revision object to be stored alongside the original under the same _id.

    Stores a minimal revision metadata and the normalized text. Does not overwrite original fields.
    """
    return {
        'revision_type': 'normalized',
        'normalized_at': int(time.time()),
        'source_fields': ['text'],
        'text': normalized_text,
    }


async def process_single_document(doc: Dict[str, Any], api_key: str, base_url: Optional[str], model: str, session: aiohttp.ClientSession, dry_run: bool, collection: Collection) -> bool:
    """Process a single document for normalization."""
    text = str(doc.get('text', '')).strip()
    if not text:
        return False

    try:
        normalized = await normalize_text_via_openai_compatible(text, api_key=api_key, base_url=base_url, model=model, session=session)
        normalized = normalize_quote_characters(normalized)
    except Exception as e:
        print(f"_id={doc.get('_id')} normalization failed: {e}")
        return False

    revision = build_revision(doc, normalized)

    update = {
        '$push': { 'revisions': revision }
    }

    if dry_run:
        print(f"DRY-RUN _id={doc.get('_id')} would append a normalized revision")
        print("--- ORIGINAL TEXT ---")
        print(text)
        print("--- NORMALIZED TEXT ---")
        print(normalized)
        print("======================\n")
    else:
        print(f"Updating _id={doc.get('_id')} with normalized text")
        collection.update_one({ '_id': doc['_id'] }, update)

    return True


async def process_documents_batch(docs: List[Dict[str, Any]], api_key: str, base_url: Optional[str], model: str, dry_run: bool, collection: Collection, semaphore: asyncio.Semaphore) -> int:
    """Process a batch of documents concurrently."""
    
    print(f"Processing batch of {len(docs)} documents")
    async def process_with_semaphore(doc):
        async with semaphore:
            async with aiohttp.ClientSession() as session:
                return await process_single_document(doc, api_key, base_url, model, session, dry_run, collection)
    
    tasks = [process_with_semaphore(doc) for doc in docs]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Count successful normalizations
    successful = sum(1 for result in results if result is True)
    return successful


def process_documents(collection: Collection, limit: Optional[int], resume_from: Optional[str], batch_size: int, dry_run: bool, api_key: str, base_url: Optional[str], model: str, concurrency: int = 5) -> None:
    async def run_async_processing():
        query: Dict[str, Any] = {
            # skip docs without text or with empty/whitespace-only text
            'text': { '$type': 'string', '$regex': r'\S' },
            # only process documents that do NOT already contain a normalized revision
            '$or': [
                { 'revisions': { '$exists': False } },
                { 'revisions': { '$not': { '$elemMatch': { 'revision_type': 'normalized' } } } },
            ],
        }
        if resume_from:
            try:
                query['_id'] = { '$gt': ObjectId(resume_from) }
            except Exception:
                print(f"Warning: invalid --resume-from ObjectId: {resume_from}. Ignoring.")

        # Print amount of documents to process
        print(f"Processing {collection.count_documents(query)} documents")

        cursor = collection.find(query, no_cursor_timeout=True).sort('_id', 1)
        processed = 0
        batch: List[Dict[str, Any]] = []
        semaphore = asyncio.Semaphore(concurrency)
        
        try:
            for doc in cursor:
                if limit is not None and processed >= limit:
                    break
                
                batch.append(doc)
                
                # Process batch when it reaches batch_size or we're at the end
                if len(batch) >= batch_size:
                    batch_processed = await process_documents_batch(batch, api_key, base_url, model, dry_run, collection, semaphore)
                    processed += batch_processed
                    batch = []
                    
                    if batch_size > 0 and processed % batch_size == 0:
                        print(f"Processed {processed} documents...")
            
            # Process remaining documents in the last batch
            if batch:
                batch_processed = await process_documents_batch(batch, api_key, base_url, model, dry_run, collection, semaphore)
                processed += batch_processed

        finally:
            cursor.close()

        print(f"Done. Total processed: {processed}")
    
    # Run the async processing
    asyncio.run(run_async_processing())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Normalize MongoDB articles using an OpenAI-compatible API')
    parser.add_argument('--env-file', type=str, default='normalize.env', help='Path to env file with configuration')
    parser.add_argument('--limit', type=int, default=None, help='Limit number of documents to process')
    parser.add_argument('--resume-from', type=str, default=None, help='Resume from a given ObjectId (exclusive)')
    parser.add_argument('--batch-size', type=int, default=20, help='Progress print frequency')
    parser.add_argument('--concurrency', type=int, default=5, help='Number of concurrent API calls')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes: print original and normalized text; no DB writes')
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # Load env file first, allowing it to supply all needed variables
    if args.env_file:
        load_env_file(args.env_file)

    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print('Error: OPENAI_API_KEY is required in environment.')
        sys.exit(1)

    # Support OPENAI_API_URL as well as OPENAI_BASE_URL
    base_url = os.environ.get('OPENAI_API_URL') or os.environ.get('OPENAI_BASE_URL')
    model = os.environ.get('OPENAI_MODEL', 'gemini-flash-lite-latest')

    collection = get_mongo_collection()
    process_documents(
        collection=collection,
        limit=args.limit,
        resume_from=args.resume_from,
        batch_size=args.batch_size,
        dry_run=args.dry_run,
        api_key=api_key,
        base_url=base_url,
        model=model,
        concurrency=args.concurrency,
    )


if __name__ == '__main__':
    main()
