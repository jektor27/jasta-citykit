"""Noise filtering and deterministic deduplication."""

from __future__ import annotations

from ..config import NOISE_HINTS
from ..models import Shop
from .normalize import normalize_address, normalize_text
from .tokens import jaccard, tokenize


def is_noise(shop: Shop) -> bool:
    haystack = normalize_text(f"{shop.name} {shop.address}")
    return any(hint in haystack for hint in NOISE_HINTS)


def similarity(left: Shop, right: Shop) -> float:
    name_score = jaccard(tokenize(left.name), tokenize(right.name))
    address_score = jaccard(
        tokenize(normalize_address(left.address)),
        tokenize(normalize_address(right.address)),
    )
    score = 0.65 * name_score + 0.35 * address_score
    if left.phone and left.phone == right.phone:
        score += 0.2
    return min(score, 1.0)


def dedupe(shops: list[Shop], threshold: float = 0.82) -> tuple[list[Shop], int]:
    """Return unique shops and the number of discarded duplicates and noise rows."""
    kept: list[Shop] = []
    removed = 0
    for shop in shops:
        if not shop.is_valid() or is_noise(shop):
            removed += 1
            continue
        if any(similarity(shop, existing) >= threshold for existing in kept):
            removed += 1
            continue
        kept.append(shop)
    return kept, removed
