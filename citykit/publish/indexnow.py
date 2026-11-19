"""IndexNow adapter. The key is read from the environment only."""

from __future__ import annotations

import json
import os
import urllib.request

ENDPOINT = "https://api.indexnow.org/indexnow"


def build_payload(host: str, key: str, urls: list[str]) -> dict[str, object]:
    return {"host": host, "key": key, "urlList": urls}


def submit(host: str, urls: list[str], dry_run: bool = True) -> dict[str, object]:
    key = os.environ.get("CITYKIT_INDEXNOW_KEY", "")
    payload = build_payload(host, key, urls)
    if dry_run:
        return {"status": "dry-run", "count": len(urls), "host": host}
    if not key:
        raise RuntimeError("CITYKIT_INDEXNOW_KEY is not set")
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return {"status": response.status, "count": len(urls), "host": host}
