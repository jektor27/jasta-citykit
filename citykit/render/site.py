"""Render a complete static site into an output directory."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from ..models import Shop
from ..publish.sitemap import build_sitemap
from .category import render_category
from .shop import render_shop


def slug(value: str) -> str:
    return value.lower().replace(" ", "-")


def build_site(shops: list[Shop], out: str | Path, base_url: str, lang: str = "ru") -> list[str]:
    root = Path(out)
    (root / "shop").mkdir(parents=True, exist_ok=True)
    (root / "category").mkdir(parents=True, exist_ok=True)

    written: list[str] = []
    for shop in shops:
        path = root / "shop" / f"{slug(shop.name)}.html"
        path.write_text(render_shop(shop, base_url, lang), encoding="utf-8")
        written.append(str(path))

    grouped: dict[str, list[Shop]] = defaultdict(list)
    for shop in shops:
        grouped[shop.category or "other"].append(shop)
    for category, items in grouped.items():
        path = root / "category" / f"{slug(category)}.html"
        path.write_text(render_category(category, items, base_url, lang), encoding="utf-8")
        written.append(str(path))

    index = root / "index.html"
    links = "".join(
        f'<li><a href="category/{slug(c)}.html">{c}</a>: {len(items)}</li>'
        for c, items in sorted(grouped.items())
    )
    index.write_text(
        f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
        f'<title>Каталог</title><meta name="description" content="Статический каталог из открытых данных.">'
        f'<link rel="canonical" href="{base_url.rstrip("/")}/"></head>'
        f'<body><main><h1>Каталог</h1><ul>{links}</ul></main></body></html>',
        encoding="utf-8",
    )
    written.append(str(index))

    sitemap = root / "sitemap.xml"
    sitemap.write_text(build_sitemap(written, root, base_url), encoding="utf-8")
    written.append(str(sitemap))
    return written
