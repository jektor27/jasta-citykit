"""Shared loader for source exports."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..models import Shop


def load_rows(path: str | Path) -> list[dict[str, Any]]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("items") or payload.get("features") or []
    if not isinstance(payload, list):
        raise ValueError("Source export must be a list or an object with items/features")
    return [row for row in payload if isinstance(row, dict)]


def save_shops(shops: list[Shop], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps([shop.to_dict() for shop in shops], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
