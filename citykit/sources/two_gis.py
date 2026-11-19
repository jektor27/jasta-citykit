"""Adapter for an exported 2GIS JSON file.

CityKit does not scrape 2GIS and does not ship its data. The adapter only maps
fields from a file the user exports himself.
"""

from __future__ import annotations

from ..models import Shop
from .base import load_rows


def collect_2gis(path: str, limit: int | None = None) -> list[Shop]:
    rows = load_rows(path)
    shops = [
        Shop.from_dict(
            {
                "name": row.get("name"),
                "address": row.get("address") or row.get("address_comment"),
                "phone": (row.get("contact_groups") or [{}])[0].get("phone"),
                "hours": (row.get("working_hours") or [{}])[0].get("text"),
                "category": row.get("category"),
                "description": row.get("description"),
                "source_url": row.get("link"),
                "raw": row,
            }
        )
        for row in rows
    ]
    return shops[:limit] if limit else shops
