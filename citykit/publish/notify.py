"""Orchestration for sitemap-based notifications."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

from .indexnow import submit


def read_sitemap_urls(path: str | Path) -> list[str]:
    text = Path(path).read_text(encoding="utf-8")
    return re.findall(r"<loc>(.*?)</loc>", text, flags=re.DOTALL)


def notify(sitemap: str | Path, dry_run: bool = True) -> dict[str, object]:
    urls = read_sitemap_urls(sitemap)
    host = urlparse(urls[0]).netloc if urls else ""
    return submit(host, urls, dry_run=dry_run)
