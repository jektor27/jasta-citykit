"""Token helpers for similarity scoring."""

from __future__ import annotations

from .normalize import normalize_text


def tokenize(value: str) -> set[str]:
    return {token for token in normalize_text(value).split() if len(token) > 1}


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)
