#!/usr/bin/env python3
"""
Generate instruction-tuned dataset from Stern NEON articles.

This script converts the raw JSONL articles into various formats suitable
for fine-tuning LLMs with LoRA or other methods.

Output formats:
- Alpaca format (instruction, input, output)
- ChatML/Messages format (for chat models)
- Completion format (simple text format)
"""

import json
import random
import argparse
from pathlib import Path
from typing import Generator
from dataclasses import dataclass

# Category translations for German instructions
CATEGORY_TRANSLATIONS = {
    "fuehlen": "Gefühle",
    "kaufen": "Konsum & Lifestyle",
    "freie-zeit": "Freizeit",
    "sehen": "Beobachtungen",
    "machen": "Aktivitäten",
    "wissen": "Wissen",
    "erwachsen-werden": "Erwachsenwerden",
    "familie": "Familie",
    "liebe": "Liebe",
    "sex": "Sexualität",
    "freundschaft": "Freundschaft",
    "reise": "Reisen",
    "computer-internet": "Computer & Internet",
    "musik": "Musik",
    "film-fernsehen": "Film & Fernsehen",
    "buecher": "Bücher",
    "sport": "Sport",
    "essen-trinken": "Essen & Trinken",
    "mode": "Mode",
    "wohnen": "Wohnen",
    "arbeit": "Arbeit",
    "studium": "Studium",
    "schule": "Schule",
    "politik": "Politik",
    "gesellschaft": "Gesellschaft",
}

# Instruction templates - varied to improve model generalization
INSTRUCTION_TEMPLATES = [
    # Title-based
    "Schreibe einen Artikel mit dem Titel: \"{title}\"",
    "Verfasse einen persönlichen Text zum Thema: \"{title}\"",
    "Erstelle einen NEON-Artikel mit der Überschrift: \"{title}\"",

    # Category-based
    "Schreibe einen persönlichen Artikel über {category}.",
    "Verfasse einen emotionalen Text zum Thema {category}.",

    # Title + Category
    "Schreibe einen {category}-Artikel mit dem Titel \"{title}\".",
    "Erstelle einen persönlichen Text über {category}. Der Titel soll sein: \"{title}\"",

    # With subtitle context
    "Schreibe einen Artikel mit dem Titel \"{title}\". Thema: {subtitle}",
    "Verfasse einen Text zum Thema: {subtitle}",
]

# System prompts for chat format
SYSTEM_PROMPTS = [
    "Du bist ein kreativer Autor im Stil der Stern NEON Community. Du schreibst persönliche, emotionale und authentische Texte über das Leben junger Erwachsener in Deutschland.",
    "Du bist ein talentierter Autor für persönliche Essays und Erfahrungsberichte. Dein Schreibstil ist introspektiv, ehrlich und berührend.",
    "Du schreibst im Stil von Stern NEON: persönlich, nachdenklich, manchmal melancholisch, immer authentisch. Deine Texte handeln vom Erwachsenwerden, von Liebe, Freundschaft und den kleinen Momenten des Lebens.",
]


@dataclass
class Article:
    """Represents a single article from the dataset."""
    title: str
    subtitle: str | None
    text: str
    author: str
    main_category: str
    sub_category: str
    article_id: int

    @classmethod
    def from_json(cls, data: dict) -> "Article | None":
        """Create an Article from JSON data, returns None if invalid."""
        text = data.get("text", "").strip()
        title = data.get("title", "").strip()

        # Skip articles with empty or very short text
        if not text or len(text) < 100 or not title:
            return None

        return cls(
            title=title,
            subtitle=data.get("subtitle"),
            text=text,
            author=data.get("author", "Anonym"),
            main_category=data.get("main_category", ""),
            sub_category=data.get("sub_category", ""),
            article_id=data.get("id", 0),
        )

    def get_category_name(self) -> str:
        """Get human-readable category name."""
        sub = CATEGORY_TRANSLATIONS.get(self.sub_category, self.sub_category)
        main = CATEGORY_TRANSLATIONS.get(self.main_category, self.main_category)
        if sub and sub != main:
            return f"{main} / {sub}"
        return main or "Allgemein"


def load_articles(input_path: Path) -> Generator[Article, None, None]:
    """Load and parse articles from JSONL file."""
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                article = Article.from_json(data)
                if article:
                    yield article
            except json.JSONDecodeError as e:
                print(f"Warning: Failed to parse line: {e}")
                continue


def generate_instruction(article: Article) -> str:
    """Generate a varied instruction for an article."""
    # Choose template based on available data
    available_templates = INSTRUCTION_TEMPLATES[:3]  # Title-based always available

    if article.main_category or article.sub_category:
        available_templates.extend(INSTRUCTION_TEMPLATES[3:7])  # Category templates

    if article.subtitle:
        available_templates.extend(INSTRUCTION_TEMPLATES[7:])  # Subtitle templates

    template = random.choice(available_templates)

    return template.format(
        title=article.title,
        category=article.get_category_name(),
        subtitle=article.subtitle or "",
    )


def to_alpaca_format(article: Article) -> dict:
    """Convert article to Alpaca instruction format."""
    return {
        "instruction": generate_instruction(article),
        "input": "",
        "output": article.text,
        "metadata": {
            "title": article.title,
            "author": article.author,
            "category": article.get_category_name(),
            "id": article.article_id,
        }
    }


def to_chat_format(article: Article) -> dict:
    """Convert article to ChatML/messages format."""
    system_prompt = random.choice(SYSTEM_PROMPTS)
    user_message = generate_instruction(article)

    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": article.text},
        ],
        "metadata": {
            "title": article.title,
            "author": article.author,
            "id": article.article_id,
        }
    }


def to_completion_format(article: Article) -> dict:
    """Convert article to simple completion format."""
    category = article.get_category_name()
    subtitle_line = f"\n### Untertitel: {article.subtitle}" if article.subtitle else ""

    text = f"""### Kategorie: {category}
### Titel: {article.title}{subtitle_line}

{article.text}"""

    return {
        "text": text,
        "metadata": {
            "title": article.title,
            "author": article.author,
            "id": article.article_id,
        }
    }


def to_sharegpt_format(article: Article) -> dict:
    """Convert article to ShareGPT format (used by Axolotl and others)."""
    system_prompt = random.choice(SYSTEM_PROMPTS)
    user_message = generate_instruction(article)

    return {
        "conversations": [
            {"from": "system", "value": system_prompt},
            {"from": "human", "value": user_message},
            {"from": "gpt", "value": article.text},
        ],
        "id": f"neon_{article.article_id}",
    }


FORMAT_HANDLERS = {
    "alpaca": to_alpaca_format,
    "chat": to_chat_format,
    "completion": to_completion_format,
    "sharegpt": to_sharegpt_format,
}


def process_dataset(
    input_path: Path,
    output_path: Path,
    output_format: str = "alpaca",
    min_length: int = 100,
    max_length: int | None = None,
    seed: int = 42,
) -> dict:
    """Process the entire dataset and write to output file."""
    random.seed(seed)

    handler = FORMAT_HANDLERS.get(output_format)
    if not handler:
        raise ValueError(f"Unknown format: {output_format}. Choose from: {list(FORMAT_HANDLERS.keys())}")

    stats = {
        "total_processed": 0,
        "skipped_short": 0,
        "skipped_long": 0,
        "categories": {},
    }

    with open(output_path, "w", encoding="utf-8") as out_file:
        for article in load_articles(input_path):
            # Length filtering
            text_len = len(article.text)
            if text_len < min_length:
                stats["skipped_short"] += 1
                continue
            if max_length and text_len > max_length:
                stats["skipped_long"] += 1
                continue

            # Convert to output format
            output_record = handler(article)
            out_file.write(json.dumps(output_record, ensure_ascii=False) + "\n")

            # Update stats
            stats["total_processed"] += 1
            cat = article.get_category_name()
            stats["categories"][cat] = stats["categories"].get(cat, 0) + 1

    return stats


def main():
    parser = argparse.ArgumentParser(
        description="Generate instruction-tuned dataset from Stern NEON articles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Alpaca format (default)
  python generate_instructions.py ../stern_neon_user_poetry.jsonl -o ../neon_alpaca.jsonl

  # Generate ChatML format for chat models
  python generate_instructions.py ../stern_neon_user_poetry.jsonl -o ../neon_chat.jsonl -f chat

  # Generate ShareGPT format for Axolotl
  python generate_instructions.py ../stern_neon_user_poetry.jsonl -o ../neon_sharegpt.jsonl -f sharegpt

  # Filter by text length
  python generate_instructions.py ../stern_neon_user_poetry.jsonl -o ../neon_filtered.jsonl --min-length 500 --max-length 5000
        """
    )

    parser.add_argument(
        "input",
        type=Path,
        help="Path to input JSONL file (stern_neon_user_poetry.jsonl)",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        required=True,
        help="Path to output JSONL file",
    )
    parser.add_argument(
        "-f", "--format",
        choices=list(FORMAT_HANDLERS.keys()),
        default="alpaca",
        help="Output format (default: alpaca)",
    )
    parser.add_argument(
        "--min-length",
        type=int,
        default=100,
        help="Minimum text length in characters (default: 100)",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=None,
        help="Maximum text length in characters (default: no limit)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)",
    )

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1

    print(f"Processing {args.input}...")
    print(f"Output format: {args.format}")
    print(f"Output file: {args.output}")
    print()

    stats = process_dataset(
        input_path=args.input,
        output_path=args.output,
        output_format=args.format,
        min_length=args.min_length,
        max_length=args.max_length,
        seed=args.seed,
    )

    print("=" * 50)
    print("Processing complete!")
    print(f"  Total articles processed: {stats['total_processed']}")
    print(f"  Skipped (too short): {stats['skipped_short']}")
    print(f"  Skipped (too long): {stats['skipped_long']}")
    print()
    print("Top categories:")
    sorted_cats = sorted(stats["categories"].items(), key=lambda x: x[1], reverse=True)
    for cat, count in sorted_cats[:10]:
        print(f"  {cat}: {count}")
    print()
    print(f"Output written to: {args.output}")

    return 0


if __name__ == "__main__":
    exit(main())
