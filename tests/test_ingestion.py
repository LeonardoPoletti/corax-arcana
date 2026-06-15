"""
tests/test_ingestion.py

Tests for the Bronze ingestion module.
We test logic, not the network — HTTP calls are mocked with respx.
"""

import httpx
import pytest
import respx
from pydantic import ValidationError

from ingestion.client import get_bulk_info
from ingestion.schemas import BronzeCard

# A valid card dict that matches what Scryfall sends
VALID_CARD = {
    "id": "abc123",
    "oracle_id": "def456",
    "name": "Lightning Bolt",
    "lang": "en",
    "mana_cost": "{R}",
    "cmc": 1.0,
    "type_line": "Instant",
    "oracle_text": "Lightning Bolt deals 3 damage to any target.",
    "colors": ["R"],
    "color_identity": ["R"],
    "keywords": [],
    "rarity": "common",
    "set": "lea",
    "set_name": "Limited Edition Alpha",
}

# A fake Scryfall catalogue response for the mock
MOCK_CATALOGUE = {
    "object": "list",
    "has_more": False,
    "data": [
        {
            "object": "bulk_data",
            "id": "some-id",
            "type": "oracle_cards",
            "updated_at": "2026-06-14T21:03:15.234+00:00",
            "uri": "https://api.scryfall.com/bulk-data/some-id",
            "name": "Oracle Cards",
            "description": "Test",
            "size": 176000000,
            "download_uri": "https://data.scryfall.io/oracle-cards/test.json",
            "content_type": "application/json",
            "content_encoding": "gzip",
        }
    ],
}


def test_bronze_card_validates_correct_card():
    """A card with all required fields should validate without errors."""
    card = BronzeCard(**VALID_CARD)
    assert card.id == "abc123"
    assert card.name == "Lightning Bolt"


def test_bronze_card_accepts_missing_optional_fields():
    """A card with only the required fields should still be valid."""
    card = BronzeCard(id="xyz789", name="Storm Crow")
    assert card.name == "Storm Crow"
    assert card.mana_cost is None
    assert card.image_uris is None


def test_bronze_card_rejects_missing_name():
    """A card without 'name' must raise a ValidationError."""
    with pytest.raises(ValidationError):
        BronzeCard(id="abc123")


@respx.mock
def test_get_bulk_info_returns_correct_keys():
    """get_bulk_info() should return download_uri and updated_at."""
    respx.get("https://api.scryfall.com/bulk-data").mock(
        return_value=httpx.Response(200, json=MOCK_CATALOGUE)
    )
    info = get_bulk_info("oracle_cards")
    assert "download_uri" in info
    assert "updated_at" in info
    assert info["download_uri"] == "https://data.scryfall.io/oracle-cards/test.json"
