"""JSON report helpers for CI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def write_report(report: dict[str, Any], path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def exit_code(report: dict[str, Any]) -> int:
    return 1 if report.get("failed") or report.get("local_links") else 0
