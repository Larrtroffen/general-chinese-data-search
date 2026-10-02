# news-aggregator-skill —— 44+ 源新闻聚合

一个 Claude/Agent Skill：一条命令从 44+ 源拉实时头条（国际新闻 + 科技社区 + AI 通讯 + 中文社媒/财经 + 播客/博客），生成中文简报。对我们最大的价值是它**把 44+ 个源的取数 URL 与 OPML 模板整理好了**，可直接抄源/抄 URL，不必用它的分析流程。

- 去哪找：repo <https://github.com/cclank/news-aggregator-skill>；源表在 `SKILL.md`；取数实现在 `scripts/fetch_news.py`；OPML 模板 `user_sources.opml.example`
- 什么时候用：要"一批多源头条"快速扫（科技/财经/国际/中文热榜）；或要找**某个源的公开 JSON/RSS 接口 URL** 直接复用。
- 怎么取：
  - 源清单：`curl -s https://raw.githubusercontent.com/cclank/news-aggregator-skill/main/SKILL.md | sed -n '/Available Sources/,/Custom/p'`
  - OPML 模板：`curl -s https://raw.githubusercontent.com/cclank/news-aggregator-skill/main/user_sources.opml.example`
  - 用它跑：`python3 scripts/fetch_news.py --source 36kr,wallstreetcn,weibo --limit 15 --no-save`（需先 clone，Python3）
  - 自定义源：写标准 OPML 2.0（只需 `xmlUrl`），放 `~/.config/news-aggregator/user_sources.opml`，用 `--source user` 抓。
- 覆盖：44+ 源，含国际新闻、科技社区、AI 通讯、中文社媒热榜、播客/博客、用户 OPML。
- 门槛：无 LICENSE——只记链接与用法，**不复制其代码**；多为**英文源**（BBC/Guardian/arXiv 等，境内可能需代理）。
- 实测：2026-10-03，macOS：通过 `gh api` 读取 `SKILL.md`、`user_sources.opml.example`、`scripts/fetch_news.py` 源码确认上述 URL 与用法；**未在本机运行其脚本**（纪律：不执行第三方脚本），源可用性为"上游声明/代码所示，未本机实测"。GitHub 直连不稳（clone 失败），改用 `gh api`/raw 读取成功。
- 上游：<https://github.com/cclank/news-aggregator-skill>（无 LICENSE，仅参考用法与源清单）

## 细节

### 代表性源（20 条，完整表见 `SKILL.md` 的 "Available Sources"）

| key | 名称 | 底层取数 URL |
|---|---|---|
| `hackernews` | Hacker News | `http://hn.algolia.com/api/v1/search_by_date`（JSON，含 24h 过滤） |
| `weibo` | 微博热搜 | `https://weibo.com/ajax/side/hotSearch`（需 `Referer: https://weibo.com/`） |
| `36kr` | 36氪 | 抓 `https://36kr.com/newsflashes` 页面 |
| `wallstreetcn` | 华尔街见闻 | `https://api-one.wallstcn.com/apiv1/content/information-flow?channel=global-channel&accept=article&limit=30` |
| `tencent` | 腾讯新闻 | `https://i.news.qq.com/web_backend/v2/getTagInfo?tagId=aEWqxLtdgmQ%3D`（需 `Referer: https://news.qq.com/`） |
| `github` | GitHub Trending | 抓 `https://github.com/trending` 页面 |
| `v2ex` | V2EX | `https://www.v2ex.com/api/topics/hot.json` |
| `producthunt` | Product Hunt | `https://www.producthunt.com/feed`（RSS） |
| `lobsters` | Lobsters | `https://lobste.rs/hottest.json` |
| `devto` | Dev.to | `https://dev.to/api/articles?top=1&per_page=30` |
| `arxiv` | arXiv cs.AI/cs.CL/cs.LG | arXiv API（来源内含过滤） |
| `huggingface` | HF Daily Papers | HF papers API |
| `sspai` | 少数派 | RSS |
| `infoq_cn` | InfoQ 中文（RSS 仅标题，建议 `--deep`） | RSS |
| `bbc_top`/`bbc_world`/`bbc_chinese` | BBC（英/中） | BBC RSS（境内需代理） |
| `guardian_world` | The Guardian World | Guardian RSS |
| `aljazeera` / `france24` | 半岛 / 法国24 | 各自 RSS |
| `reuters` | Reuters | **无官方 RSS**，用 Google News RSS `site:reuters.com` fallback |
| `tldr_ai`/`import_ai`/`ai_newsletters` | AI 通讯聚合 | 各 Substack/自建 RSS |
| `podcasts`/`essays` | 播客 / 长文聚合 | 各 RSS |

另有 `latentspace`、`lexfridman`、`80000hours`、`paulgraham`、`waitbutwhy`、`jamesclear`、`farnamstreet`、`dankoe` 等；完整「怎么取全量」= 读 `SKILL.md` 的 Available Sources 表 + `scripts/fetch_news.py` 里每个 `requests.get(...)` 的 URL。

## 坑

- 许可：**无 LICENSE**——只记链接与用法，**不复制其代码**进我们仓库。
- 多为**英文源**（BBC/Guardian/arXiv 等，境内可能需代理）；`reuters` 是 Google News fallback 而非官方源（报告里要如实标注）。
- `weibo`/`tencent` 等需特定 `Referer` 头，裸 curl 可能被拒。
- 抓正文的 `--deep` 走各站 HTML，稳定性取决于站点。
