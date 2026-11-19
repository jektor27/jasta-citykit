"""FAQ built only from verified fields."""

from __future__ import annotations

from ..models import Shop


def build_faq(shop: Shop) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    if shop.address:
        pairs.append((f"Где находится {shop.name}?", f"Адрес: {shop.address}."))
    if shop.phone:
        pairs.append((f"Как позвонить в {shop.name}?", f"Телефон: {shop.phone}."))
    if shop.hours:
        pairs.append((f"Когда работает {shop.name}?", f"Часы работы: {shop.hours}."))
    if not pairs:
        pairs.append(
            ("Как уточнить данные?", "Уточните адрес и часы работы по указанному телефону.")
        )
    return pairs
