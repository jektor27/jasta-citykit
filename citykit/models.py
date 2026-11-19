"""Typed shop record used by every CityKit stage."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Shop:
    name: str
    address: str = ""
    phone: str = ""
    hours: str = ""
    category: str = ""
    description: str = ""
    source_url: str = ""
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, row: dict[str, Any]) -> "Shop":
        return cls(
            name=str(row.get("name") or row.get("title") or "").strip(),
            address=str(row.get("address") or row.get("addr") or "").strip(),
            phone=str(row.get("phone") or row.get("tel") or "").strip(),
            hours=str(row.get("hours") or row.get("opening_hours") or "").strip(),
            category=str(row.get("category") or "").strip(),
            description=str(row.get("description") or "").strip(),
            source_url=str(row.get("source_url") or row.get("url") or "").strip(),
            raw=dict(row),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def is_valid(self) -> bool:
        return bool(self.name)
