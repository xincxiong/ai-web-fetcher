---
name: ai-web-fetcher
description: >-
  Fetches and extracts web content using Scrapling (HTTP, stealth browser, or
  full dynamic Playwright). Supports adaptive CSS when sites change, anti-bot
  bypass, and spider-scale crawls. Use when the user needs reliable page fetch,
  structured extraction, scraping behind Cloudflare, JS-rendered pages, or asks
  for Scrapling / adaptive scraping / stealth fetch / crawl.
homepage: https://github.com/D4Vinci/Scrapling
metadata:
  openclaw:
    emoji: "🕷️"
    requires:
      bins: ["python3"]
---

# AI Web Fetcher (Scrapling)

Use **[Scrapling](https://github.com/D4Vinci/Scrapling)** for fetching and parsing HTML when plain HTTP or simple `curl` is not enough: TLS impersonation, stealth browsers, Cloudflare Turnstile, JS-heavy pages, and **adaptive selectors** that survive DOM changes.

## When to use which fetcher

| Scenario | Class | Notes |
|----------|--------|--------|
| Static HTML, fast path | `Fetcher` / `FetcherSession` | `impersonate='chrome'`, optional `stealthy_headers=True` |
| Anti-bot / Cloudflare | `StealthyFetcher` / `StealthySession` | `solve_cloudflare=True`, `headless=True` |
| Heavy JS / SPA | `DynamicFetcher` / `DynamicSession` | Playwright/Chromium; `network_idle=True` often helps |
| Full site crawl | `scrapling.spiders.Spider` | Concurrency, pause/resume, multi-session |

## Install

Parser-only (no browsers):

```bash
pip install scrapling
```

Fetchers + browsers (required for Stealthy/Dynamic and most real-world fetch):

```bash
pip install "scrapling[fetchers]"
scrapling install
```

Optional extras (from upstream docs):

```bash
pip install "scrapling[ai]"    # MCP server for AI workflows
pip install "scrapling[shell]" # CLI `scrapling shell` / `scrapling extract`
pip install "scrapling[all]"
```

Project helper (this skill):

```bash
pip install -r {baseDir}/scripts/requirements.txt
scrapling install
```

## One-shot CLI (this skill)

```bash
python3 {baseDir}/scripts/extract.py "https://example.com" -o out.md
python3 {baseDir}/scripts/extract.py "https://example.com" --mode http -o -
python3 {baseDir}/scripts/extract.py "https://protected.example" --mode stealth --css "article"
python3 {baseDir}/scripts/extract.py "https://spa.example" --mode dynamic --network-idle
```

## Python patterns (core API)

### HTTP with session (TLS fingerprint)

```python
from scrapling.fetchers import Fetcher, FetcherSession

with FetcherSession(impersonate="chrome") as session:
    page = session.get("https://quotes.toscrape.com/", stealthy_headers=True)
    texts = page.css(".quote .text::text").getall()
```

### Stealth (anti-bot / Cloudflare)

```python
from scrapling.fetchers import StealthyFetcher

StealthyFetcher.adaptive = True
page = StealthyFetcher.fetch(
    "https://example.com",
    headless=True,
    network_idle=True,
    solve_cloudflare=True,
)
nodes = page.css(".product", auto_save=True)  # persist selector hints for later
# After site redesign:
products = page.css(".product", adaptive=True)
```

### Dynamic (full browser)

```python
from scrapling.fetchers import DynamicSession

with DynamicSession(headless=True, network_idle=True) as session:
    page = session.fetch("https://example.com/", load_dom=False)
    items = page.xpath('//span[@class="text"]/text()').getall()
```

### Parser-only (HTML string already in hand)

```python
from scrapling.parser import Selector

page = Selector(html_string)
title = page.css("title::text").get()
```

### Small spider (export JSON)

```python
from scrapling.spiders import Spider, Response

class DemoSpider(Spider):
    name = "demo"
    start_urls = ["https://quotes.toscrape.com/"]

    async def parse(self, response: Response):
        for q in response.css(".quote"):
            yield {"text": q.css(".text::text").get(), "author": q.css(".author::text").get()}

result = DemoSpider().start()
result.items.to_json("out.json")
```

## Official CLI (after `pip install "scrapling[shell]"`)

```bash
scrapling extract get 'https://example.com' content.md
scrapling extract stealthy-fetch 'https://example.com' out.html --solve-cloudflare
```

## Compliance

Scrapling is for legal, ethical use only. Obey **robots.txt**, site **Terms of Service**, and **local laws**. Do not use against sites that prohibit scraping or to collect personal data without grounds.

## More detail

See `{baseDir}/references/scrapling-quickref.md` for links and troubleshooting.
