"""Lightweight HTML audit without external dependencies."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


class _Collector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.description = ""
        self.h1 = 0
        self.lang = ""
        self.canonical = ""
        self.images_without_alt: list[str] = []
        self.links: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key: value or "" for key, value in attrs}
        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self.h1 += 1
        elif tag == "meta" and values.get("name") == "description":
            self.description = values.get("content", "")
        elif tag == "link" and values.get("rel") == "canonical":
            self.canonical = values.get("href", "")
        elif tag == "img" and not values.get("alt"):
            self.images_without_alt.append(values.get("src", ""))
        elif tag == "a" and values.get("href"):
            self.links.append(values["href"])
        if tag == "html" and not self.lang:
            self.lang = values.get("lang", "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data


def audit_file(path: str | Path) -> dict[str, object]:
    parser = _Collector()
    parser.feed(Path(path).read_text(encoding="utf-8"))
    issues: list[str] = []
    if not parser.title.strip():
        issues.append("missing title")
    if not parser.description.strip():
        issues.append("missing description")
    if parser.h1 != 1:
        issues.append(f"h1 count is {parser.h1}")
    if not parser.lang:
        issues.append("missing lang")
    if not parser.canonical:
        issues.append("missing canonical")
    if parser.images_without_alt:
        issues.append(f"{len(parser.images_without_alt)} images without alt")
    return {
        "file": str(path),
        "title": parser.title.strip(),
        "issues": issues,
        "links": parser.links,
    }


def audit_paths(paths: Iterable[str | Path]) -> dict[str, object]:
    reports = [audit_file(path) for path in paths]
    broken = [
        f"{report['file']}: {link}"
        for report in reports
        for link in report["links"]  # type: ignore[index]
        if link.startswith(("./", "../")) or link.startswith("/")
    ]
    total = len(reports)
    failed = sum(1 for report in reports if report["issues"])
    return {
        "files": total,
        "failed": failed,
        "local_links": broken,
        "reports": reports,
    }
