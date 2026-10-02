# so.toutiao.com —— 资讯检索（SSR + JSON 接口）

字节头条搜索。直出带内嵌 JSON 的 HTML；加 `Accept: application/json` 直接返回结构化 JSON；`offset` 可稳定翻页。中文综搜里翻页能力最好的通道之一。

- 去哪找：`https://so.toutiao.com/search?keyword={q}&pd=information`
- 什么时候用：中文资讯检索首选（翻页最稳、可结构化）；需要文章标题/摘要/时间的放量召回
- 怎么搜：HTML 通道 `curl -s -m 20 -A "$UA" "https://so.toutiao.com/search?keyword=$Q&pd=information"`；JSON 通道加 `-H 'Accept: application/json'`。参数 `keyword` 关键词（空格 `+`）、`pd` 频道（固定 `information` 才返回 JSON）、`offset` 起始序号（0、10、20…，**翻页有效**）。结果形态：SSR HTML（内嵌 JSON）或 `application/json`
- 覆盖：头条资讯索引；粒度 = 文章条目；`offset` 翻页、每页 10 条
- 门槛：无（本次未带 cookie 即拿到结果）
- 实测：2026-10-02，macOS + curl（Chrome 桌面 UA）——HTML/JSON/翻页均 200，HTML 与首页 0 重叠，移动版路径 404；完整记录见下
- 上游：站点自身入口（无 repo/Skill 出处）

## 细节

### 可用性矩阵（本机实测 2026-10-02）

| 通道 | URL | 状态 | 现象 |
|---|---|---|---|
| 网页检索 | `https://so.toutiao.com/search?keyword={q}&pd=information` | ✅ | 200，1819057 B；`<title>{q}-头条搜索`；`<div id="results" … data-test-result-list>`，结果 JSON 内嵌 |
| JSON 接口 | 同上 + `Accept: application/json` | ✅ | 200，441756 B，`application/json`；体 `{"keyword":"街乡吹哨","count":10,"dom":"…","scripts":"…","has_more":1,"first_index":0,"last_index":9,…}` |
| 翻页 | `&offset=10` | ✅ | 200，1814032 B；10 条与首页 **0 重叠** |
| 移动版 | `https://so.toutiao.com/m/search?keyword={q}` | ❌ | **404**，18 B（该路径不存在，勿用） |
| 文章页 | `https://www.toutiao.com/group/{id}/` | ✅ | 302 → `https://www.toutiao.com/article/{id}/`，200，72914 B |

### 请求模板

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
Q='%E8%A1%97%E4%B9%A1%E5%90%B9%E5%93%A8'   # 街乡吹哨
# HTML（内嵌 JSON）
curl -s -m 20 -A "$UA" "https://so.toutiao.com/search?keyword=$Q&pd=information"
# JSON（推荐）
curl -s -m 20 -A "$UA" -H 'Accept: application/json' \
  "https://so.toutiao.com/search?keyword=$Q&pd=information&offset=0"
```

### 解析要点

- 结果页为 **SSR + 内嵌 JSON**，无需执行 JS。
- **JSON 通道**（`Accept: application/json`）：顶层字段 `keyword` / `count` / `dom` / `scripts` / `has_more` / `first_index` / `last_index` / `has_next` / `next_log_id`。条目数据在 **`scripts` 字符串**里（不是 `dom`）：直接对 `scripts` 跑正则/JSON 抽取即可。
- 每条结果字段：`"item_source_url":"/group/<id>/"`（标题链接，拼 `https://www.toutiao.com`）、`"title"`、`"abstract"`、`"display_time"`（Unix 秒字符串）、`"behot_time"`、`"media_type"`。
- **HTML 通道**：同样对整页跑 `"item_source_url":"(/group/\d+/)"` 与 `"title":"…"` 正则，10 条/页。
- 翻页：`offset += 10`，配合 `count` 判停（首页 `count=10`、`has_more=1`）。

### 实测记录

**2026-10-02**，macOS + curl（Chrome 桌面 UA）：

- `?keyword=街乡吹哨&pd=information` → 200，1819057 B，`item_source_url`×10。
- 同上 + `Accept: application/json` → 200，441756 B，`application/json`，`count=10`、`has_more=1`、`last_index=9`。
- `&offset=10` → 200，1814032 B，与首页 0 重叠。
- `so.toutiao.com/m/search?…` → 404，18 B。
- `www.toutiao.com/group/7691552592140190235/` → 302 → `/article/…`，200，72914 B。

**2026-10-01**（历史实测）：

- `https://so.toutiao.com/search?keyword=吹哨报到 试点街乡&pd=synthesis` ✅ 可用，结果页含真实条目（2018-12-09 头条号文章）。

## 坑

- 移动版路径 `so.toutiao.com/m/search` **404**，不要走移动端点。
- `pd=synthesis`（综合频道）实测：即使带 `Accept: application/json` 也返回 **HTML** 而非 JSON，且资讯条目 JSON 明显变少（`item_source_url` 仅 2 条）；要结构化就固定用 `pd=information`。
- 条目链接是 `/group/{id}/`，需拼域名并由 `/group/`→`/article/` 302 跳转；直接请求 `www.toutiao.com/group/{id}/` 也能拿到正文（-L 跟随）。
- HTML 体积大（~1.8 MB/页），批量抓取按 `scripts` 字段做流式/切片解析，别整页 `json.loads`。
- 页内含大量 `argus`/埋点 base64 片段，正则抽取目标字段时要锚定 `item_source_url`，避免误命中。
