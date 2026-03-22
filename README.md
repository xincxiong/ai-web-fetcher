# ai-web-fetcher

面向 **Cursor Agent** 的 Skill：用 [Scrapling](https://github.com/D4Vinci/Scrapling) 做可靠的网页抓取与正文/结构化抽取（HTTP、隐身浏览器、Playwright 动态渲染），适合反爬、Cloudflare、重 JS 页面以及需要**自适应 CSS** 的场景。

- **仓库**：<https://github.com/xincxiong/ai-web-fetcher>
- **上游库**：<https://github.com/D4Vinci/Scrapling> · [文档](https://scrapling.readthedocs.io/en/latest/)

## 内容结构

| 路径 | 说明 |
|------|------|
| `SKILL.md` | Cursor Skill 说明：何时用哪种 Fetcher、安装与 Python 示例 |
| `scripts/extract.py` | 命令行拉取；纯文本或 **Markdown 文档**（`--format markdown` / `-o *.md`） |
| `scripts/requirements.txt` | Scrapling + Markdown 导出依赖（trafilatura / markdownify / bs4） |
| `references/scrapling-quickref.md` | 常见问题与文档链接 |

## 安装

```bash
cd /path/to/ai-web-fetcher
pip install -r scripts/requirements.txt
scrapling install   # 下载浏览器，Stealthy/Dynamic 模式需要
```

仅解析 HTML、不需要拉取网页时，可只装：`pip install scrapling`。

## 命令行（extract.py）

```bash
# 默认 HTTP 模式，纯文本
python3 scripts/extract.py "https://example.com" -o out.txt

# Markdown 文档（标题、来源、抓取时间、正文；正文优先智能抽取）
python3 scripts/extract.py "https://example.com" --format markdown -o article.md
python3 scripts/extract.py "https://example.com" -o article.md   # .md 后缀自动启用 markdown

# 标准输出
python3 scripts/extract.py "https://example.com" --format markdown -o -

# 隐身模式 + CSS 片段 → Markdown
python3 scripts/extract.py "https://example.com" --mode stealth --css "article" --format markdown -o piece.md

# 动态页面（Playwright）
python3 scripts/extract.py "https://example.com" --mode dynamic --network-idle --format markdown -o spa.md
```

常用参数：`--mode {http,stealth,dynamic}`、`--format {text,markdown}`、`--css`、`--network-idle`、`--solve-cloudflare`、`--no-headless`。

## 在 Cursor 里使用

将本仓库（或解压后的目录）放到 Cursor Skills 约定位置，Agent 会读取 `SKILL.md` 中的抓取策略与 Scrapling API 示例。详细片段见 `SKILL.md`。

## 合规

仅用于合法、合规场景：遵守 robots.txt、网站服务条款与当地法律；勿对禁止抓取的站点滥用，勿无法律依据收集个人信息。
