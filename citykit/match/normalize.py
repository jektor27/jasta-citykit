"""Deterministic text normalization for Russian city data."""

from __future__ import annotations

import re
import unicodedata

_YO = str.maketrans("ёЁ", "еЕ")
_SPACES = re.compile(r"\s+")
_PUNCT = re.compile(r"[^\w\s+]+", flags=re.UNICODE)


def normalize_text(value: str) -> str:
    """Lowercase, replace ё with е, collapse spaces and drop punctuation."""
    text = unicodedata.normalize("NFKC", value or "").translate(_YO).lower()
    text = _PUNCT.sub(" ", text)
    return _SPACES.sub(" ", text).strip()


def normalize_address(value: str) -> str:
    """Bring street addresses to a comparable form."""
    text = normalize_text(value)
    text = re.sub(r"\bул\b", "улица", text)
    text = re.sub(r"\bпер\b", "переулок", text)
    text = re.sub(r"\bпр\b", "проспект", text)
    text = re.sub(r"\bдом\b", "д", text)
    return _SPACES.sub(" ", text).strip()
