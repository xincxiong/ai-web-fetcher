#!/usr/bin/env python3
"""
Thin CLI for the ai-web-fetcher skill. Wraps Scrapling fetchers for agent use.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _write(path: str, content: str) -> None:
    if path == "-":
        sys.stdout.write(content)
        if not content.endswith("\n"):
            sys.stdout.write("\n")
    else:
        Path(path).write_text(content, encoding="utf-8")


def _extract_body_text(page) -> str:
    # Prefer main text if body exists
    body = page.css("body")
    if body:
        return "\n".join(
            line.strip()
            for line in body[0].xpath(".//text()").getall()
            if line and line.strip()
        )
    return page.xpath("//text()").get() or ""


def main() -> int:
    p = argparse.ArgumentParser(description="Fetch URL via Scrapling (ai-web-fetcher)")
    p.add_argument("url", help="Target URL")
    p.add_argument("-o", "--output", default="-", help="Output file or - for stdout")
    p.add_argument(
        "--mode",
        choices=("http", "stealth", "dynamic"),
        default="http",
        help="http=Fetcher (fast); stealth=StealthyFetcher; dynamic=DynamicFetcher/Playwright",
    )
    p.add_argument("--css", help="CSS selector: dump ::text from all matches joined by newlines")
    p.add_argument("--network-idle", action="store_true", help="For stealth/dynamic: wait for network idle")
    p.add_argument("--solve-cloudflare", action="store_true", help="For stealth: enable Cloudflare solving")
    p.add_argument("--headless", action="store_true", default=True, help="Stealth/dynamic headless (default on)")
    p.add_argument("--no-headless", action="store_true", help="Show browser window")
    args = p.parse_args()

    headless = not args.no_headless

    try:
        if args.mode == "http":
            from scrapling.fetchers import Fetcher

            page = Fetcher.get(args.url)
        elif args.mode == "stealth":
            from scrapling.fetchers import StealthyFetcher

            kw = {"headless": headless}
            if args.network_idle:
                kw["network_idle"] = True
            if args.solve_cloudflare:
                kw["solve_cloudflare"] = True
            page = StealthyFetcher.fetch(args.url, **kw)
        else:
            from scrapling.fetchers import DynamicFetcher

            kw = {"headless": headless}
            if args.network_idle:
                kw["network_idle"] = True
            page = DynamicFetcher.fetch(args.url, **kw)
    except ImportError as e:
        print(
            "Scrapling fetchers not available. Install with:\n"
            '  pip install "scrapling[fetchers]" && scrapling install',
            file=sys.stderr,
        )
        print(e, file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Fetch failed: {e}", file=sys.stderr)
        return 2

    if args.css:
        els = page.css(args.css)
        parts = []
        for el in els:
            t = el.xpath("string(.)").get()
            if t and t.strip():
                parts.append(t.strip())
        out = "\n\n".join(parts) if parts else ""
    else:
        out = _extract_body_text(page)

    _write(args.output, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
