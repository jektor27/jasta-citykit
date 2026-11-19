"""Small synthetic export for a quick, offline demonstration."""

from __future__ import annotations

from ..models import Shop


def collect_demo(limit: int | None = None) -> list[Shop]:
    rows = [
        {
            "name": "Стройматериалы Примерска",
            "address": "ул. Центральная, 5",
            "phone": "+7 000 111-22-33",
            "hours": "ежедневно 08:00–19:00",
            "category": "stroymaterialy",
            "description": "Стройматериалы и инструменты.",
        },
        {
            "name": "Цветы у дома",
            "address": "Центральная улица 5",
            "phone": "+7 000 111-22-33",
            "hours": "ежедневно 09:00–20:00",
            "category": "cvety",
            "description": "Цветы и букеты.",
        },
        {
            "name": "Аптека Здоровье",
            "address": "ул. Садовая, 12",
            "phone": "+7 000 444-55-66",
            "hours": "круглосуточно",
            "category": "apteka",
            "description": "Лекарства и товары для здоровья.",
        },
    ]
    shops = [Shop.from_dict(row) for row in rows]
    return shops[:limit] if limit else shops
