# Scrapling quick reference

- **Repo**: [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling)
- **Docs**: [scrapling.readthedocs.io](https://scrapling.readthedocs.io/en/latest/)
- **Python**: 3.10+

## Common issues

1. **`ModuleNotFoundError` for fetchers** → `pip install "scrapling[fetchers]"` then `scrapling install`.
2. **Browser crashes in containers** → use upstream Docker image `pyd4vinci/scrapling` or install missing OS deps from Playwright docs.
3. **403 / blocked on HTTP path** → switch to `StealthyFetcher` or `DynamicSession`; add proxies via Scrapling `ProxyRotator` if needed.
4. **Selectors break after redesign** → use `adaptive=True` or `auto_save=True` on `css()` / XPath as per README.

## Adaptive scraping

Training flow: scrape with `auto_save=True` once; later passes can use `adaptive=True` so the library relocates elements after layout changes (similarity-based).

## MCP

`pip install "scrapling[ai]"` exposes an MCP server for AI tools (see upstream README).
