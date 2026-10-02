# Scrapling —— 反爬绕过 + 三级抓取

`D4Vinci/Scrapling`（BSD-3-Clause，v0.4.15，**requires-python ≥3.10**）：解析器（自适应定位，页面改版后能重找元素）+ 多种 fetcher（普通/异步/隐身/动态浏览器）+ 爬虫框架（Spider，带断点续爬、代理轮换、自适应限速）。对中文站的用处：**Cloudflare / 反爬站** —— `StealthyFetcher` 官方称开箱处理 Cloudflare Turnstile，有 `--solve-cloudflare` CLI 开关。

- 去哪找：仓库 https://github.com/D4Vinci/Scrapling ；文档 https://scrapling.readthedocs.io/en/latest/ ；Agent 技能（仓库内）`agent-skill/Scrapling-Skill`（另有 MCP server `scrapling[ai]`）；Docker `docker pull pyd4vinci/scrapling` / `ghcr.io/d4vinci/scrapling:latest`
- 什么时候用：目标站有 **Cloudflare Turnstile / 强反爬 + JS 渲染**（普通 curl 拿不到内容、`web_search` 也点不开）；需要**批量并发抓取**且要**断点续跑**（Spider pause/resume）；元素定位怕页面改版（`auto_save=True` + `adaptive=True`）
- 怎么用：`pip install scrapling` → `pip install "scrapling[fetchers]"` → `scrapling install`；CLI `scrapling extract stealthy-fetch '<url>' out.html --solve-cloudflare`；Python 用 `StealthyFetcher.fetch(...)`
- 覆盖：通用网页；解析器/fetcher/Spider 三层；含反爬（Cloudflare Turnstile）、MCP server、Docker 镜像；许可 BSD-3-Clause
- 门槛：**Python ≥3.10**（本机系统 `python3` 是 **3.9** → 需另建 3.11/3.12 环境，uv/conda；`playwright` extra 同要求）；`scrapling install` 拉浏览器 + 系统依赖 + 指纹库（数百 MB）
- 实测：2026-10-02，macOS 27（arm64）——仅只读侦察（`gh api` 元数据、tarball 读 README/pyproject）；**未安装、未跑 `scrapling extract`**
- 上游：https://github.com/D4Vinci/Scrapling

## 细节

### 安装

```bash
pip install scrapling                  # 只装解析器（不含 fetcher，import scrapling.fetchers 会 ModuleNotFoundError）
pip install "scrapling[fetchers]"      # 浏览器/隐身抓取
scrapling install                      # 下载浏览器 + 系统依赖 + 指纹依赖（--force 重装）
pip install "scrapling[shell]"         # 需要 CLI extract / 交互 shell；[all] = ai+rag+shell
```

### CLI（不写代码就能取页）

输出后缀决定格式（`.txt` 纯文本 / `.md` Markdown / `.html` 原始 HTML）：

```bash
scrapling extract get 'https://example.com' content.md --css-selector '#main' --impersonate 'chrome'
scrapling extract fetch 'https://example.com' content.md --no-headless          # 动态渲染
scrapling extract stealthy-fetch 'https://nopecha.com/demo/cloudflare' out.html --solve-cloudflare
```

### Python：fetcher（自适应定位）

```python
from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher
StealthyFetcher.adaptive = True
p = StealthyFetcher.fetch('https://example.com', headless=True, network_idle=True)
items = p.css('.product', auto_save=True)      # 先存元素指纹
items = p.css('.product', adaptive=True)       # 改版后按指纹重找
```

### Python：批量爬（Spider，含 pause/resume、代理轮换、自适应限速）

```python
from scrapling.spiders import Spider, Response
class MySpider(Spider):
    name = "demo"; start_urls = ["https://example.com/"]
    async def parse(self, response: Response):
        for item in response.css('.product'): yield {"title": item.css('h2::text').get()}
MySpider().start()
```

### 实测记录（2026-10-02）

macOS 27（arm64）。本机仅做**可用性侦察**：`gh api` 得到 repo `size=11333 KB`、`license=BSD-3-Clause`、`pushed_at=2026-09-30`；tarball 拉取并阅读 README/pyproject → `requires-python = ">=3.10"`、`version = 0.4.15`、extras（fetchers/rag/ai/shell/all）、CLI 示例与 `--solve-cloudflare` 均在文档中确认。**未安装、未跑 `scrapling extract`**（系统 Python 3.9 不满足；遵守「不执行第三方安装」纪律）。

## 坑

- **Python ≥3.10**：本机系统 `python3` 是 **3.9** → 系统解释器装不上，要另建 3.11/3.12 环境（uv/conda）。
- 安装体积大：`scrapling install` 拉浏览器 + 系统依赖 + 指纹库（数百 MB）；Docker 更省心。
- `--solve-cloudflare` / `StealthyFetcher` 是**对抗性能力**：只用于公开数据、遵守 robots 与站点条款，不要用在已被明确禁止抓取的站（见 `../archives/ctext.md`）；隐身能力随反爬升级会退化 → **上线前必须探活实测**。
- 仓库 README 里赞助商代理链接很多，别误当官方推荐。

> 顺序建议：先用本仓 `scripts/fetch.py` 直连试；被挡 → 本库 `stealthy-fetch`；要可见浏览器手工过验证码 → `playwright-cli.md` / `agent-browser.md`。
