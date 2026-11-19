"""Adapter for an Overpass JSON export from OpenStreetMap."""

from __future__ import annotations

from ..models import Shop
from .base import load_rows


def collect_osm(path: str, limit: int | None = None) -> list[Shop]:
    shops: list[Shop] = []
    for element in load_rows(path):
        tags = element.get("tags") or {}
        if not tags.get("name"):
            continue
        shops.append(
            Shop.from_dict(
                {
                    "name": tags.get("name"),
                    "address": " ".join(
                        str(tags.get(key, ""))
                        for key in ("addr:street", "addr:housenumber")
                    ).strip(),
                    "phone": tags.get("phone") or tags.get("contact:phone"),
                    "hours": tags.get("opening_hours"),
                    "category": tags.get("shop") or tags.get("amenity"),
                    "description": tags.get("description"),
                    "source_url": tags.get("website") or tags.get("contact:website"),
                    "raw": element,
                }
            )
        )
    return shops[:limit] if limit else shops
