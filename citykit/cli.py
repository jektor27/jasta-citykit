"""Command line interface for CityKit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .audit.html import audit_paths
from .audit.report import exit_code, write_report
from .config import DEFAULT_CITY, DEFAULT_LANG, DEFAULT_MIN_SCORE
from .match.dedupe import dedupe
from .models import Shop
from .publish.notify import notify
from .render.faq import build_faq
from .render.site import build_site
from .sources import demo, osm, two_gis
from .sources.base import save_shops


def _load_shops(path: str) -> list[Shop]:
    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Shop.from_dict(row) for row in rows if isinstance(row, dict)]


def _collect(args: argparse.Namespace) -> int:
    if args.source == "demo":
        shops = demo.collect_demo(args.limit)
    elif args.source == "2gis":
        if not args.input:
            raise SystemExit("--input is required for source 2gis")
        shops = two_gis.collect_2gis(args.input, args.limit)
    elif args.source == "osm":
        if not args.input:
            raise SystemExit("--input is required for source osm")
        shops = osm.collect_osm(args.input, args.limit)
    else:
        raise SystemExit(f"Unknown source: {args.source}")
    if args.dry_run:
        print(json.dumps({"city": args.city, "count": len(shops), "dry_run": True}, ensure_ascii=False))
        return 0
    save_shops(shops, args.out)
    print(json.dumps({"city": args.city, "count": len(shops), "out": args.out}, ensure_ascii=False))
    return 0


def _dedupe(args: argparse.Namespace) -> int:
    shops, removed = dedupe(_load_shops(args.input), args.threshold)
    if args.dry_run:
        print(json.dumps({"kept": len(shops), "removed": removed, "dry_run": True}))
        return 0
    save_shops(shops, args.out)
    print(json.dumps({"kept": len(shops), "removed": removed, "out": args.out}))
    return 0


def _build(args: argparse.Namespace) -> int:
    shops = _load_shops(args.input)
    if args.dry_run:
        print(json.dumps({"shops": len(shops), "out": args.out, "dry_run": True}))
        return 0
    written = build_site(shops, args.out, args.base_url, args.lang)
    print(json.dumps({"shops": len(shops), "written": len(written), "out": args.out}))
    return 0


def _faq(args: argparse.Namespace) -> int:
    payload = {
        shop.name: [{"question": q, "answer": a} for q, a in build_faq(shop)]
        for shop in _load_shops(args.input)
    }
    if args.dry_run:
        print(json.dumps({"entries": len(payload), "dry_run": True}, ensure_ascii=False))
        return 0
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"entries": len(payload), "out": args.out}, ensure_ascii=False))
    return 0


def _audit(args: argparse.Namespace) -> int:
    paths = [str(path) for path in Path(args.path).rglob("*.html")]
    report = audit_paths(paths)
    if args.json:
        write_report(report, args.json)
    print(json.dumps({"files": report["files"], "failed": report["failed"]}, ensure_ascii=False))
    return exit_code(report)


def _notify(args: argparse.Namespace) -> int:
    result = notify(args.sitemap, dry_run=args.dry_run or not args.indexnow)
    print(json.dumps(result, ensure_ascii=False))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="citykit", description="CityKit CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    collect = sub.add_parser("collect", help="collect shops into a normalized JSON file")
    collect.add_argument("--source", choices=("demo", "2gis", "osm"), default="demo")
    collect.add_argument("--city", default=DEFAULT_CITY)
    collect.add_argument("--input")
    collect.add_argument("--out", default="data/shops.json")
    collect.add_argument("--limit", type=int)
    collect.add_argument("--dry-run", action="store_true")
    collect.set_defaults(func=_collect)

    dedupe_cmd = sub.add_parser("dedupe", help="remove noise and duplicate rows")
    dedupe_cmd.add_argument("--in", dest="input", required=True)
    dedupe_cmd.add_argument("--out", default="data/unique.json")
    dedupe_cmd.add_argument("--threshold", type=float, default=DEFAULT_MIN_SCORE)
    dedupe_cmd.add_argument("--dry-run", action="store_true")
    dedupe_cmd.set_defaults(func=_dedupe)

    build = sub.add_parser("build", help="render a static site")
    build.add_argument("--in", dest="input", required=True)
    build.add_argument("--out", default="site/")
    build.add_argument("--base-url", default="https://example.org")
    build.add_argument("--lang", default=DEFAULT_LANG)
    build.add_argument("--dry-run", action="store_true")
    build.set_defaults(func=_build)

    faq = sub.add_parser("faq", help="build FAQ from verified fields")
    faq.add_argument("--in", dest="input", required=True)
    faq.add_argument("--out", default="data/faq.json")
    faq.add_argument("--dry-run", action="store_true")
    faq.set_defaults(func=_faq)

    audit = sub.add_parser("audit", help="audit generated HTML")
    audit.add_argument("path")
    audit.add_argument("--json")
    audit.set_defaults(func=_audit)

    notify_cmd = sub.add_parser("notify", help="submit sitemap URLs to IndexNow")
    notify_cmd.add_argument("--sitemap", default="site/sitemap.xml")
    notify_cmd.add_argument("--indexnow", action="store_true")
    notify_cmd.add_argument("--dry-run", action="store_true")
    notify_cmd.set_defaults(func=_notify)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)
