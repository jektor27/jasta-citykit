"""schema.org JSON-LD generation."""

from __future__ import annotations

import json
from typing import Any

from ..models import Shop


def shop_schema(shop: Shop, base_url: str) -> str:
    data: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Store",
        "name": shop.name,
        "url": f"{base_url.rstrip('/')}/shop/{shop.name.lower().replace(' ', '-')}.html",
    }
    if shop.address:
        data["address"] = {"@type": "PostalAddress", "streetAddress": shop.address}
    if shop.phone:
        data["telephone"] = shop.phone
    if shop.hours:
        data["openingHours"] = shop.hours
    if shop.description:
        data["description"] = shop.description
    return json.dumps(data, ensure_ascii=False, indent=2)
