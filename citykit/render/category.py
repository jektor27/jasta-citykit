"""Category listing page."""

from __future__ import annotations

from html import escape

from ..models import Shop


def render_category(category: str, shops: list[Shop], base_url: str, lang: str = "ru") -> str:
    items = "".join(
        f'<li><a href="{escape(base_url.rstrip("/"))}/shop/{escape(s.name.lower().replace(" ", "-"))}.html">'
        f'{escape(s.name)}</a> — {escape(s.address)}</li>'
        for s in shops
    )
    return f"""<!doctype html>
<html lang="{escape(lang)}">
<head>
<meta charset="utf-8">
<title>{escape(category)} — каталог</title>
<meta name="description" content="Список организаций категории {escape(category)}.">
<link rel="canonical" href="{escape(base_url.rstrip('/'))}/category/{escape(category)}.html">
</head>
<body>
<main>
<h1>{escape(category)}</h1>
<ul>{items}</ul>
</main>
</body>
</html>
"""
