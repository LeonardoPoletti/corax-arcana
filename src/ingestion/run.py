"""
src/ingestion/run.py

Entry point for the Bronze ingestion pipeline.

Run with:
    python src/ingestion/run.py

What it does:
    1. Featches the download URL for oracle_cards and rulings from Scryfall
    2. Downloads bouth files to data/raw/ as compressed JSON
    3. Parses each file card by card using ijson (streaming - no RAM overload)
    4. Validates each record with Pydantic
    5. Writes validated records to Parquet in data/bronze/
"""

import logging
import sys
import time
from pathlib import Path

import ijson

from ingestion.client import download_bulk_file, get_bulk_download_url
from ingestion.schemas import BronzeCard, BronzeRuling
from ingestion.writer import write_parquet

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# Where raw JSON files land before parsing
RAW_DIR = Path("data/raw")


def ingest_cards() -> None:
    """Download oracle_cards JSON and write to Bronze Parquet."""
    logger.info("=== START: oracle_cards ingestion ===")
    start = time.time()

    url = get_bulk_download_url("oracle_cards")
    raw_path = RAW_DIR / "oracle_cards.json"
    download_bulk_file(url, raw_path)

    logger.info("Parsing cards with ijson (streaming)...")
    cards: list[BronzeCard] = []
    errors = 0

    with open(raw_path, "rb") as f:
        for raw_card in ijson.items(f, "item"):
            try:
                cards.append(BronzeCard(**raw_card))
            except Exception as e:
                errors += 1
                logger.warning("Shipped card: %s", e)

    logger.info("Parsed %d cards, %d errors.", len(cards), errors)
    dest = write_parquet(cards, "cards")
    elapsed = time.time() - start
    logger.info("=== DONE: cards -> %s (%.1fs) ===", dest, elapsed)


def ingest_rulings() -> None:
    """Download rulings JSON and write to Bronze Parquet."""
    logger.info("=== START: rulings ingestion ===")
    start = time.time()

    url = get_bulk_download_url("rulings")
    raw_path = RAW_DIR / "rulings.json"
    download_bulk_file(url, raw_path)

    logger.info("Parsing rulings with ijson (streaming)...")
    rulings: list[BronzeRuling] = []
    errors = 0

    with open(raw_path, "rb") as f:
        for raw_ruling in ijson.items(f, "item"):
            try:
                rulings.append(BronzeRuling(**raw_ruling))
            except Exception as e:
                errors += 1
                logger.warning("Skipped ruling: %s", e)

    logger.info("Parsed %d rulings, %d erros.", len(rulings), errors)
    dest = write_parquet(rulings, "rulings")
    elapsed = time.time() - start
    logger.info("=== DONE: rulings -> %s (%.1fs) ===", dest, elapsed)


if __name__ == "__main__":
    try:
        ingest_cards()
        ingest_rulings()
        logger.info("Pipeline complete.")
    except Exception as e:
        logger.error("Pipeline failed: %s", e)
        sys.exit(1)
