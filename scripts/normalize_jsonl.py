#!/usr/bin/env python3
"""
Script to normalize JSONL entries for LLM fine-tuning.
Filters out entries without text and normalizes content using OpenAI-compatible API.
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import time
import argparse

try:
    import openai
except ImportError:
    print("Error: openai package not found. Install with: pip install openai")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('normalize_log.txt'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class JSONLNormalizer:
    def __init__(self, api_key: str, base_url: str = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the normalizer with OpenAI-compatible API settings.
        
        Args:
            api_key: API key for the service
            base_url: Base URL for API (optional, defaults to OpenAI)
            model: Model name to use for normalization
        """
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        self.processed_count = 0
        self.skipped_count = 0
        self.failed_count = 0
        self.already_normalized_count = 0
        
    def normalize_text(self, text: str, title: str = "", subtitle: str = "") -> Optional[str]:
        """
        Normalize text content using the API.
        
        Args:
            text: Main text content to normalize
            title: Article title for context
            subtitle: Article subtitle for context
            
        Returns:
            Normalized text or None if normalization fails
        """
        try:
            system_prompt = """You are an expert text editor helping to prepare content for LLM fine-tuning. 

Your task is to normalize and clean text while preserving its meaning and literary quality. Make these improvements:

1. Fix obvious typos and spelling errors
2. Normalize punctuation and spacing inconsistencies
3. Remove excessive whitespace and newlines (but preserve intentional line breaks for poetry/paragraphs)
4. Ensure proper capitalization
5. Fix encoding issues or strange characters
6. Maintain the original style and voice
7. Preserve intentional formatting (like poetry line breaks)
8. Remove any metadata or non-content text

Return ONLY the cleaned text, nothing else."""

            user_prompt = f"""Title: {title}
Subtitle: {subtitle}

Text to normalize:
{text}"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1,
                max_tokens=4000
            )
            
            normalized_text = response.choices[0].message.content.strip()
            return normalized_text
            
        except Exception as e:
            logger.error(f"API normalization failed: {str(e)}")
            return None
    
    def is_valid_entry(self, entry: Dict[Any, Any]) -> bool:
        """
        Check if entry has valid text content.
        
        Args:
            entry: JSONL entry dictionary
            
        Returns:
            True if entry has non-empty text field
        """
        text = entry.get('text', '')
        return isinstance(text, str) and text.strip() != ''
    
    def is_already_normalized(self, entry: Dict[Any, Any]) -> bool:
        """
        Check if entry has already been normalized.
        
        Args:
            entry: JSONL entry dictionary
            
        Returns:
            True if entry has already been normalized
        """
        return entry.get('_normalized', False) or entry.get('_normalization_failed', False)
    
    def process_jsonl(self, input_file: str, output_file: str, failed_file: str, 
                     max_entries: Optional[int] = None, delay: float = 0.5, 
                     force_reprocess: bool = False, append: bool = False):
        """
        Process the JSONL file and normalize entries.
        
        Args:
            input_file: Path to input JSONL file
            output_file: Path to output normalized JSONL file
            failed_file: Path to file for failed normalizations
            max_entries: Maximum number of entries to process (for testing)
            delay: Delay between API calls to avoid rate limits
            force_reprocess: If True, reprocess already normalized entries
            append: If True, append to existing output files instead of overwriting them
        """
        logger.info(f"Starting normalization of {input_file}")
        logger.info(f"Output file: {output_file} (mode: {'append' if append else 'overwrite'})")
        logger.info(f"Failed entries file: {failed_file} (mode: {'append' if append else 'overwrite'})")
        if force_reprocess:
            logger.info("Force reprocess enabled - will reprocess already normalized entries")
        
        # Determine file modes based on append flag
        output_mode = 'a' if append else 'w'
        failed_mode = 'a' if append else 'w'
        
        with open(input_file, 'r', encoding='utf-8') as infile, \
             open(output_file, output_mode, encoding='utf-8') as outfile, \
             open(failed_file, failed_mode, encoding='utf-8') as failfile:
            
            for line_num, line in enumerate(infile, 1):
                try:
                    # Parse JSON line
                    entry = json.loads(line.strip())
                    
                    # Skip entries without valid text
                    if not self.is_valid_entry(entry):
                        logger.debug(f"Line {line_num}: Skipping entry without text")
                        self.skipped_count += 1
                        continue
                    
                    # Check if already normalized or failed (unless forcing reprocess)
                    if not force_reprocess and self.is_already_normalized(entry):
                        title = entry.get('title', '')
                        logger.debug(f"Line {line_num}: Entry '{title[:50]}...' already processed")
                        
                        # Write to appropriate file based on previous result
                        if entry.get('_normalized', False):
                            outfile.write(json.dumps(entry, ensure_ascii=False) + '\n')
                        elif entry.get('_normalization_failed', False):
                            failfile.write(json.dumps(entry, ensure_ascii=False) + '\n')
                        
                        self.already_normalized_count += 1
                        
                        # Check max_entries limit after counting already normalized entries
                        if max_entries and (self.processed_count + self.already_normalized_count) >= max_entries:
                            logger.info(f"Reached maximum entries limit: {max_entries}")
                            break
                        continue
                    
                    # Check max_entries limit before processing new entries
                    if max_entries and (self.processed_count + self.already_normalized_count) >= max_entries:
                        logger.info(f"Reached maximum entries limit: {max_entries}")
                        break
                    
                    # Extract content for normalization
                    original_text = entry['text']
                    title = entry.get('title', '')
                    subtitle = entry.get('subtitle', '')
                    
                    logger.info(f"Line {line_num}: Normalizing entry '{title[:50]}...'")
                    
                    # Normalize the text
                    normalized_text = self.normalize_text(original_text, title, subtitle)
                    
                    if normalized_text:
                        # Update entry with normalized text
                        entry['text'] = normalized_text
                        entry['_original_length'] = len(original_text)
                        entry['_normalized_length'] = len(normalized_text)
                        entry['_normalized'] = True
                        
                        # Write to output file
                        outfile.write(json.dumps(entry, ensure_ascii=False) + '\n')
                        self.processed_count += 1
                        logger.info(f"Line {line_num}: Successfully normalized")
                    else:
                        # Write failed entry to failed file
                        entry['_normalization_failed'] = True
                        failfile.write(json.dumps(entry, ensure_ascii=False) + '\n')
                        self.failed_count += 1
                        logger.warning(f"Line {line_num}: Normalization failed")
                    
                    # Rate limiting delay (only for new API calls)
                    if delay > 0:
                        time.sleep(delay)
                        
                except json.JSONDecodeError as e:
                    logger.error(f"Line {line_num}: JSON decode error: {str(e)}")
                    self.failed_count += 1
                except Exception as e:
                    logger.error(f"Line {line_num}: Unexpected error: {str(e)}")
                    self.failed_count += 1
                    
                # Progress update
                if line_num % 10 == 0:
                    total_processed = self.processed_count + self.already_normalized_count
                    logger.info(f"Progress: Processed {line_num} lines, "
                              f"Total processed: {total_processed}, "
                              f"Newly normalized: {self.processed_count}, "
                              f"Already processed: {self.already_normalized_count}, "
                              f"Skipped: {self.skipped_count}, "
                              f"Failed: {self.failed_count}")
        
        # Final summary
        total_processed = self.processed_count + self.already_normalized_count
        logger.info("=" * 50)
        logger.info("NORMALIZATION COMPLETE")
        logger.info(f"Total lines processed: {line_num}")
        logger.info(f"Total entries processed: {total_processed}")
        logger.info(f"Newly normalized: {self.processed_count}")
        logger.info(f"Already processed (skipped): {self.already_normalized_count}")
        logger.info(f"Skipped (no text): {self.skipped_count}")
        logger.info(f"Failed: {self.failed_count}")
        logger.info("=" * 50)

def main():
    parser = argparse.ArgumentParser(description='Normalize JSONL entries for LLM fine-tuning')
    parser.add_argument('input_file', help='Input JSONL file path')
    parser.add_argument('-o', '--output', default='normalized_entries.jsonl', 
                       help='Output file for normalized entries (default: normalized_entries.jsonl)')
    parser.add_argument('-f', '--failed', default='failed_normalizations.jsonl',
                       help='Output file for failed entries (default: failed_normalizations.jsonl)')
    parser.add_argument('-k', '--api-key', help='OpenAI API key (or set OPENAI_API_KEY env var)')
    parser.add_argument('-u', '--base-url', help='Base URL for OpenAI-compatible API')
    parser.add_argument('-m', '--model', default='gpt-3.5-turbo', 
                       help='Model to use (default: gpt-3.5-turbo)')
    parser.add_argument('--max-entries', type=int, help='Maximum entries to process (for testing)')
    parser.add_argument('--delay', type=float, default=0.5, 
                       help='Delay between API calls in seconds (default: 0.5)')
    parser.add_argument('--force-reprocess', action='store_true',
                       help='Force reprocessing of already normalized entries')
    parser.add_argument('--append', action='store_true',
                       help='Append to existing output files instead of overwriting them')
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.error("API key required. Use --api-key or set OPENAI_API_KEY environment variable")
        sys.exit(1)
    
    # Check input file exists
    if not Path(args.input_file).exists():
        logger.error(f"Input file not found: {args.input_file}")
        sys.exit(1)
    
    # Initialize normalizer
    normalizer = JSONLNormalizer(
        api_key=api_key,
        base_url=args.base_url,
        model=args.model
    )
    
    # Process the file
    try:
        normalizer.process_jsonl(
            input_file=args.input_file,
            output_file=args.output,
            failed_file=args.failed,
            max_entries=args.max_entries,
            delay=args.delay,
            force_reprocess=args.force_reprocess,
            append=args.append
        )
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"Process failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 