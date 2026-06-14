"""
src/ingestion/client.py

HTTP client for the Sryfall API
Two responsibilities:
    1. Get the download URL for a bulk data file
    2. Stream that file to disk without loading it all into memory
"""

import logging
from pathlib import Path

import httpx

logger = logging.getLogger(__name__)

BULK_DATA_CATALOGUE = "https://api.scryfall.com/bulk-data"


def get_bulk_info(bulk_type: str) -> dict:
    """
    Call the Scryfall bulk data catalogue and return a dict with:
        - download_uri: the URL to download the file
        - updated_at: when Scryfall last regenerated this file

    We retun both so the caller can decide whether to download
    or skip (if the file has not changed since last run).

    Raises ValuesError if the type is not found.
    """
    logger.info("Fetching bulk data catalogue...")

    with httpx.Client() as client:
        response = client.get(BULK_DATA_CATALOGUE)
        response.raise_for_status()  # raises if HTTP status is 4xx or 5xx
        catalogue = response.json()

    for entry in catalogue["data"]:
        if entry["type"] == bulk_type:
            size_mb = entry["size"] / 1_000_000
            logger.info(
                "Found '%s': %.1f MB, updated at %s",
                bulk_type,
                size_mb,
                entry["updated_at"],
            )
            return {
                "download_uri": entry["download_uri"],
                "updated_at": entry["updated_at"],
            }

    available = [e["type"] for e in catalogue["data"]]
    raise ValueError(f"Bulk type '{bulk_type}' not found. Available: {available}")


def download_bulk_file(url: str, dest_path: Path) -> Path:
    """
    Stream a bulk data file from Scryfall to disk in 1 MB chunks.

    Streaming means we never load the whole 176 MB int memory -
    we write each chunk directly to disk as it arrives.
    """
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    logger.info("Downloading %s", url)

    downloaded = 0
    last_log = 0

    with httpx.Client() as client:
        with client.stream("GET", url, follow_redirects=True) as response:
            response.raise_for_status()
            with open(dest_path, "wb") as f:
                for chunk in response.iter_bytes(1024 * 1024):  # 1 MB per chunk
                    f.write(chunk)
                    downloaded += len(chunk)
                    mb = downloaded / 1_000_000
                    if mb - last_log >= 10:  # log evey 10 MB
                        logger.info("  %0f MB downloaded...", mb)
                        last_log = mb

    logger.info("Done: %.1f MB saved to %s", downloaded / 1_000_000, dest_path)
    return dest_path
