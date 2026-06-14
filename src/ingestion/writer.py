"""
src/ingestion/writer.py

Writer validated Bronze card and ruling onjects to Parquet files.

Dessign decisions:
    - Nested fields (dicts, lists) are serialized to JSON strings.
    - Silver layer is responsible for parsing them.
    - Each run writes a new timestamped file — we never overwrite.
    - Audit columns (_loaded_at, _source, _file_name) are adde4d here.
"""

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Root folder for all Bronze data
BRONZE_ROOT = Path("data/bronze")


def _serialize_value(value: Any) -> Any:
    """
    Convert a value to something pyarrow can write cleanly.
    - dicts and lists became JSON strings
    - everything else passes through unchangend
    """
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return value


def _model_to_row(model: BaseModel, file_name: str) -> dict[str, Any]:
    """
    Convert a Pydantic model to a flat dictionary ready for Parquet.
    Adds audit colmns and serializes nested fields.
    """
    # model_dump() returns all fields including extras from extra="allow"
    raw = model.model_dump()

    row = {key: _serialize_value(val) for key, val in raw.items()}

    # Audit columns - added by us, not from Scryfall
    row["loaded_at"] = datetime.now(timezone.utc).isoformat()
    row["_source"] = "scryfall"
    row["_file_name"] = file_name

    return row


def write_parquet(
    models: list[BaseModel],
    entity: str,
) -> Path:
    """
    Write a list of Pydantic models to a timestamped Parquet file.

    Args:
        models: List of BronzeCard or BronzeRuling objects.
        entity: Folder name = 'cards' or 'rulings'

    Returns:
        Path to the file that was written.
    """
    if not models:
        raise ValueError("Cannot write empty list to Parquet.")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    file_name = f"{entity}_{timestamp}.parquet"

    dest_dir = BRONZE_ROOT / "source=scryfall" / f"entity={entity}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / file_name

    logger.info("Converting %d records to rows...", len(models))
    rows = [_model_to_row(m, file_name) for m in models]

    table = pa.Table.from_pylist(rows)

    logger.info("Writing Parquet to %s", dest_path)
    pq.write_table(table, dest_path, compression="snappy")

    size_mb = dest_path.stat().st_size / 1_000_000
    logger.info("Done: %.2f MB written.", size_mb)

    return dest_path
