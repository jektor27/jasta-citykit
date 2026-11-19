"""Single shop card page."""

from __future__ import annotations

from html import escape

from ..models import Shop
from .faq import build_faq
from .schema import shop_schema

STYLE = """
body{font:16px/1.5 system-ui,sans-serif;margin:0 auto;max-width:760px;padding:24px;color:#222}
h1{font-size:28px}.muted{color:#666}dl dt{font-weight:600;margin-top:12px}
details{border:1px solid #ddd;border-radius:8px;padding:8px 12px;margin:8px 0}
"""


def render_shop(shop: Shop, base_url: str, lang: str = "ru") -> str:
    title = f"{escape(shop.name)} — адрес и телефон"
    description = shop.description or f"{shop.name}: адрес, телефон и часы работы."
    rows = []
    for label, value in (
        ("Адрес", shop.address),
        ("Телефон", shop.phone),
        ("Часы работы", shop.hours),
        ("Категория", shop.category),
    ):
        if value:
            rows.append(f"<dt>{escape(label)}</dt><dd>{escape(value)}</dd>")
    faq = "".join(
        f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>"
        for q, a in build_faq(shop)
    )
    return f"""<!doctype html>
<html lang="{escape(lang)}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<meta name="description" content="{escape(description)}">
<link rel="canonical" href="{escape(base_url.rstrip('/'))}/shop/{escape(shop.name.lower().replace(' ', '-'))}.html">
<style>{STYLE}</style>
<script type="application/ld+json">{shop_schema(shop, base_url)}</script>
</head>
<body>
<main>
<h1>{escape(shop.name)}</h1>
<p class="muted">Карточка магазина из открытых данных.</p>
<dl>{''.join(rows)}</dl>
<h2>Вопросы и ответы</h2>
{faq}
</main>
</body>
</html>
"""
