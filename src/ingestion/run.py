"""
src/ingestion/run.py

Entry point for the Bronze ingestion pipeline.

Run with:
    python src/ingestion/run.py

What it does:
    1. Calls the Scryfall catalogue to get the download URL and updated_at
    2. Compares updated_at with the last download (saved in a .meta.json file)
    3. Skips the download if nothing changed — saves time and bandwidth
    4. Parses each file card by card using ijson (streaming)
    5. Validates each record with Pydantic
    6. Writes validated records to Parquet in data/bronze/
"""

import json
import logging
import sys
import time
from pathlib import Path

import ijson

from ingestion.client import download_bulk_file, get_bulk_info
from ingestion.schemas import BronzeCard, BronzeRuling
from ingestion.writer import write_parquet

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

RAW_DIR = Path("data/raw")


def _read_meta(raw_path: Path) -> dict:
    """
    Read the metadata file saved from the previous download.
    Returns an empty dict if the file does not exist yet.
    """
    meta_path = raw_path.with_suffix(".meta.json")
    if meta_path.exists():
        return json.loads(meta_path.read_text())
    return {}


def _write_meta(raw_path: Path, updated_at: str) -> None:
    """
    Save the updated_at timestamp from Scryfall next to the raw file.
    On the next run, we compare this to decide whether to re-download.
    """
    meta_path = raw_path.with_suffix(".meta.json")
    meta_path.write_text(json.dumps({"updated_at": updated_at}))
    logger.info("Saved metadata to %s", meta_path)


def _download_if_changed(bulk_type: str, raw_path: Path) -> None:
    """
    Download the bulk file only if Scryfall has updated it since last run.
    """
    info = get_bulk_info(bulk_type)
    meta = _read_meta(raw_path)

    if raw_path.exists() and meta.get("updated_at") == info["updated_at"]:
        logger.info("'%s' is up to date — skipping download.", bulk_type)
        return

    download_bulk_file(info["download_uri"], raw_path)
    _write_meta(raw_path, info["updated_at"])


def ingest_cards() -> None:
    """Download oracle_cards JSON (if changed) and write to Bronze Parquet."""
    logger.info("=== START: oracle_cards ingestion ===")
    start = time.time()

    raw_path = RAW_DIR / "oracle_cards.json"
    _download_if_changed("oracle_cards", raw_path)

    logger.info("Parsing cards with ijson (streaming)...")
    cards: list[BronzeCard] = []
    errors = 0

    with open(raw_path, "rb") as f:
        for raw_card in ijson.items(f, "item"):
            try:
                cards.append(BronzeCard(**raw_card))
            except Exception as e:
                errors += 1
                logger.warning("Skipped card: %s", e)

    logger.info("Parsed %d cards, %d errors.", len(cards), errors)
    dest = write_parquet(cards, "cards")
    elapsed = time.time() - start
    logger.info("=== DONE: cards → %s (%.1fs) ===", dest, elapsed)


def ingest_rulings() -> None:
    """Download rulings JSON (if changed) and write to Bronze Parquet."""
    logger.info("=== START: rulings ingestion ===")
    start = time.time()

    raw_path = RAW_DIR / "rulings.json"
    _download_if_changed("rulings", raw_path)

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

    logger.info("Parsed %d rulings, %d errors.", len(rulings), errors)
    dest = write_parquet(rulings, "rulings")
    elapsed = time.time() - start
    logger.info("=== DONE: rulings → %s (%.1fs) ===", dest, elapsed)


if __name__ == "__main__":
    try:
        ingest_cards()
        ingest_rulings()
        logger.info("Pipeline complete.")
    except Exception as e:
        logger.error("Pipeline failed: %s", e)
        sys.exit(1)
