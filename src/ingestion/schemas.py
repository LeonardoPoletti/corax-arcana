"""
src/ingestion/schemas.py

Pydantic models for Scryfall bulk data.

Bronze layer philosophy:
    - Capture every field the API sends us.
    - Make almost everything Optional — cards don't all have the same fields.
    - Use extra = "allow" so nre Scryfall fields are captured automatically.
    - Field selection is Silver layer's responsibility, not ours.
"""

from datetime import datetime, timezone
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BronzeCard(BaseModel):
    """
    Represents one card object from the Scryfall oracle_cards bulk file.

    Only 'id', 'oracle_id', and 'name' are required — every other field
    is Optional because not all cards have all fields (e.g. tokens have
    no mana cost, double-faced cards have no image_uris at the top level).
    """

    model_config = ConfigDict(extra="allow")

    # --- Required identifiers ---
    id: str
    oracle_id: Optional[str] = None
    name: str

    # --- Core card data ---
    lang: Optional[str] = None
    released_at: Optional[str] = None
    layout: Optional[str] = None
    mana_cost: Optional[str] = None
    cmc: Optional[float] = None
    type_line: Optional[str] = None
    oracle_text: Optional[str] = None
    power: Optional[str] = None
    toughness: Optional[str] = None
    loyalty: Optional[str] = None
    colors: Optional[list[str]] = None
    color_identity: Optional[list[str]] = None
    keywords: Optional[list[str]] = None

    # --- Format legalities ---
    legalities: Optional[dict[str, str]] = None

    # --- Print and set data ---
    set_id: Optional[str] = None
    set: Optional[str] = None
    set_name: Optional[str] = None
    set_type: Optional[str] = None
    rarity: Optional[str] = None
    collector_number: Optional[str] = None
    digital: Optional[bool] = None
    reprint: Optional[bool] = None
    reserved: Optional[bool] = None

    # --- Images ---
    image_uris: Optional[dict[str, str]] = None

    # --- Prices ---
    prices: Optional[dict[str, Any]] = None

    # --- Rankings ---
    edhrec_rank: Optional[int] = None

    # --- Audit columns (added by us, not from Scryfall) ---
    _loaded_at: datetime = datetime.now(timezone.utc)
    _source: str = "scryfall"


class BronzeRuling(BaseModel):
    """
    Represents one ruling from the Scryfall rulings bulk file.
    Rulings are linked to cards via oracle_id.
    """

    model_config = ConfigDict(extra="allow")

    oracle_id: str
    source: str
    published_at: str
    comment: str

    # --- Audit columns ---
    _loaded_at: datetime = datetime.now(timezone.utc)
    _source: str = "scryfall"
