# people.com.cn —— 人民网站内检索 API

人民网是《人民日报》官网。**站内检索有 JSON 接口**（可关键词 + 日期范围 + 翻页），另有北京频道，区级/街道报道常被其「十六区动态」栏目收录。注意：检索索引**只覆盖约 2021 年至今**，2018 年的稿需另走 `web_search`/数字报。

- 去哪找：检索 API `POST http://search.people.cn/search-platform/front/search`；北京频道 `http://bj.people.com.cn/`；文章页 `http://bj.people.com.cn/n2/YYYY/MMDD/c<栏目id>-<稿号>.html`
- 什么时候用：按关键词 + 日期范围找人民网/北京频道报道（约 2021 年起）；找区级/街道稿的「十六区动态」栏目
- 怎么搜：`POST` JSON 到检索接口（**必须用 `http`**，见下）
- 覆盖：人民网全站（含地方频道/理论频道）；索引约 2021 年至今（2020 及更早未收录）
- 门槛：无（人民日报图文数据库 `data.people.com.cn` 需登录）
- 实测：2026-10-02，macOS + curl：首页 200/145,979 B；`bj.people.com.cn` 200/43,647 B；检索 API `POST http://search.people.cn/search-platform/front/search` 200 JSON（`code=0`，关键词「街乡吹哨」`total=543`）；日期过滤 2021=37/2022=155/2023=67、2020=0/2018=0；北京频道文章页 200。
- 上游：<http://www.people.com.cn/>

## 细节

### 可用性矩阵（实测 2026-10-02，macOS + curl，桌面 UA）

| 入口 | 状态 | 现象 |
|---|---|---|
| `http://www.people.com.cn/` | ✅ 200 | 首页 HTML，145,979 B |
| `http://bj.people.com.cn/` | ✅ 200 | 北京频道首页，43,647 B |
| `https://search.people.cn/` | ⚠️ 301 | 跳到 `http://search.people.cn/`；须用 **http** 访问 |
| `http://search.people.cn/s/?keyword=…` | ⚠️ 200 / JS 壳 | Nuxt SPA，仅 3,370 B，正文由 JS 渲染，curl 取不到结果 |
| `POST http://search.people.cn/search-platform/front/search` | ✅ 200 JSON | **检索数据接口**（见下） |
| `POST https://search.people.cn/search-platform/front/search` | ⚠️ 301/405 | https 下 POST 被重定向/拒绝，**必须用 http** |
| `https://data.people.com.cn/rmrb/YYYYMMDD/N` | ⚠️ 需登录 | 人民日报图文数据库（1946 至今），跳 `member/login` |

### 站内检索 API（核心）

```bash
curl -s -m 20 -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36' \
  -H 'Content-Type: application/json' -H 'Referer: http://search.people.cn/s/' \
  -X POST 'http://search.people.cn/search-platform/front/search' \
  -d '{"key":"街乡吹哨","page":1,"limit":10,"hasTitle":true,"hasContent":true,"sortType":0,"searchType":0}'
```

- 请求体字段：`key`（关键词）、`page`、`limit`、`hasTitle`（是否匹配标题）、`hasContent`（是否匹配正文）、`sortType`、`searchType`；可选 `startTime`/`endTime`。
- **日期过滤**：`startTime`/`endTime` 为 **epoch 毫秒整数**（传字符串会 400）。
- 返回：`{"code":"0","data":{"records":[…],"total":N}}`。
- 记录字段（已实测）：`title`、`url`（原文直链，如 `http://bj.people.com.cn/n2/2026/0911/c82838-41693712.html`）、`author`、`displayTime`（epoch ms，发布日）、`inputTime`、`source`、`belongsName`（栏目，如 `北京频道#十六区动态`）、`content`/`contentOriginal`（高亮/原文正文 HTML）、`originUrl`、`domain`、`id` 等。
- 翻页：`page` 递增；`limit=100` 实测可用。

### 索引深度（重要）

- 实测关键词「街乡吹哨」：`total=543`，第 1 页（limit 100）覆盖 2025-04 ~ 2026-09，最后一页最旧命中 **2021-11-16**。
- 按年过滤：2021 年 `total=37`、2022 `155`、2023 `67`；**2020 及更早 `total=0`（未收录）**。
- 结论：**2018 年数据不在该索引内**；2018 检索请用 `web_search site:people.com.cn`、或人民日报数字报/图文数据库（见 `epaper/`）。

### 北京频道（bj.people.com.cn）

- 文章页：`http://bj.people.com.cn/n2/YYYY/MMDD/c<栏目id>-<稿号>.html`
  - 示例：`http://bj.people.com.cn/n2/2026/0911/c82838-41693712.html`（✅ 200，标题《候选物业向业主做报告 丰台区五里店街道破解老旧小区"失管"困局》）。
- 栏目首页：`http://bj.people.com.cn/GB/<栏目id>/index.html`（如十六区动态 `c82838` → `/GB/82838/index.html`）。
- 检索到的北京频道稿在 API 结果里 `belongsName` 形如 `北京频道#十六区动态`，可据此过滤。

## 坑

- **只能用 http**：`search.people.cn` 的 https 会把 POST 301 到 http、再 405；检索接口务必 `http://`。
- 检索页 `/s/` 是 Nuxt SPA，别试图从 HTML 解析结果，直接打 API。
- 索引时间窗有限（约 2021 至今），不要把「搜不到」当成「没有这篇」。
