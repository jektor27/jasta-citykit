"""Sitemap generation and lastmod updates."""

from __future__ import annotations

import re
from pathlib import Path


def url_for(path: str | Path, root: str | Path, base_url: str) -> str:
    relative = Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
    if relative == "index.html":
        relative = ""
    return f"{base_url.rstrip('/')}/{relative}"


def build_sitemap(paths: list[str], root: str | Path, base_url: str) -> str:
    urls = "".join(
        f"<url><loc>{url_for(path, root, base_url)}</loc></url>" for path in paths
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'


def update_lastmod(path: str | Path, slug: str, date: str) -> bool:
    """Set lastmod for one URL slug. Returns True when a value changed."""
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    blocks = re.findall(r"<url>.*?</url>", text, flags=re.DOTALL)
    changed = False
    for block in blocks:
        if f"<loc>" not in block or slug not in block:
            continue
        cleaned = re.sub(r"<lastmod>.*?</lastmod>", "", block, flags=re.DOTALL)
        updated = cleaned.replace("</url>", f"<lastmod>{date}</lastmod></url>")
        if updated != block:
            text = text.replace(block, updated)
            changed = True
    if changed:
        target.write_text(text, encoding="utf-8")
    return changed
