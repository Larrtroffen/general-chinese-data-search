# bjnews.com.cn —— 新京报搜索 API

新京报网站（`www.bjnews.com.cn`）自带**可直读的搜索 API**，支持「标题」与「全文」两种模式、带页码，是找新京报历年报道（含 2018）的可靠通道。其**电子报**（`epaper.bjnews.com.cn`）是**图片版**（版面 JPG + 热点图），正文不在 HTML 里，检索价值低于网站搜索。

- 去哪找：站点 `https://www.bjnews.com.cn/`；搜索 API `GET https://s.bjnews.com.cn/bjnews/getlist`；文章页 `https://www.bjnews.com.cn/detail/<id>.html`；电子报 `https://epaper.bjnews.com.cn/`
- 什么时候用：找新京报历年报道（含 2018）；标题/全文关键词检索
- 怎么搜：`GET` 搜索 API（参数见下），返回 JSON
- 覆盖：网站搜索含 2018 年数据；电子报为图片版（正文不可 grep）
- 门槛：无
- 实测：2026-10-02，macOS + curl：首页 200/90,942 B；文章页 200；搜索 API `bwsk=街乡吹哨` → `status=true`，`ft=0` 3 条 / `ft=1` 19 条，返回 2018 年稿链接；电子报根 200/759 B（meta 跳转壳），版面页含 `epfile.bjnews.com.cn` 版面 JPG 与 `usemap="#mapPage"`（无正文文本）；电子报内检索页 200。
- 上游：<https://www.bjnews.com.cn/>

## 细节

### 可用性矩阵（实测 2026-10-02，macOS + curl，桌面 UA）

| 入口 | 状态 | 现象 |
|---|---|---|
| `https://www.bjnews.com.cn/` | ✅ 200 | 首页 HTML，90,942 B |
| `https://www.bjnews.com.cn/detail/<id>.html` | ✅ 200 | 文章页 33,194 B，正文在 `#contentStr` |
| `https://m.bjnews.com.cn/detail/<id>.html` | ✅（首页大量引用） | 移动版同 id |
| `https://www.bjnews.com.cn/search?q=<kw>` | ⚠️ JS 页 | 39,285 B，结果由下面的 API 渲染 |
| `GET https://s.bjnews.com.cn/bjnews/getlist?...` | ✅ 200 JSON | **搜索 API**（见下） |
| `https://epaper.bjnews.com.cn/` | ⚠️ 200 跳转壳 | 759 B，meta refresh 到当期版面页 |
| `https://epaper.bjnews.com.cn/html/search.html?searchWord=…` | ✅ 200 | 电子报内检索页（用图片版面检索 API，带页内 token） |

### 搜索 API（核心，含 2018 数据）

```bash
curl -s -m 20 -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36' \
  -H 'Referer: https://www.bjnews.com.cn/search' \
  'https://s.bjnews.com.cn/bjnews/getlist?from=bw&page=1&orderby=1&bwsk=%E8%A1%97%E4%B9%A1%E5%90%B9%E5%93%A8&ft=0'
```

- 参数：`from=bw`、`page`（页码）、`orderby`（1=默认）、`bwsk`（关键词，需 URL 编码）、`ft`（`0`=标题匹配，`1`=全文匹配）。
- 返回：`{"status":true,"data":{"data":[{"_source":{…},"highlight":{"title":…}},…]}}`。
- 取结果：标题 `_source.highlight.title`（含 `<em>` 高亮），原文直链 `_source.detail_url.pc_url`（形如 `https://www.bjnews.com.cn/detail/154694208514302.html`）。
- 实测：`bwsk=街乡吹哨`，`ft=0` 返回 3 条（含 2018 年稿）；`ft=1` 返回 19 条。**全文模式检索量显著更大**，做语料建议 `ft=1`。

### 文章页

- URL：`https://www.bjnews.com.cn/detail/<id>.html`；正文节点 `#contentStr`，静态 HTML、curl 直读。
- 例（2018-12 稿）：`https://www.bjnews.com.cn/detail/154694208514302.html`（✅ 200）。

### 电子报（图片版，弱）

- 入口 `https://epaper.bjnews.com.cn/` 是 meta refresh 壳，跳到当期版面，如
  `https://epaper.bjnews.com.cn/html/2026/20260930/20260930_A01/20260930_A01_7315.html`。
- 版面页规律：`/html/YYYY/YYYYMMDD/YYYYMMDD_A0N/YYYYMMDD_A0N_<稿号>.html`（A/B/C/D 叠 + 特刊）。
- **版面为整版图片**：`<img src="//epfile.bjnews.com.cn/group1/M00/…JPG" usemap="#mapPage">` + 版面文章热点图；文章标题/正文由 JS（`static/js/outline.js`）加载，**不在静态 HTML 中**，正文无法直接 grep。
- 电子报内检索页 `https://epaper.bjnews.com.cn/html/search.html?searchWord=<kw>` 调用 `https://epaper.bjnews.com.cn/api/paperDetail/eslist`，但请求需带页内加密参数 `aesPaperInfoId`（每页不同），**难以用 curl 复现**；建议用浏览器打开检索页，或改用上面的网站搜索 API（`s.bjnews.com.cn`，已验证含 2018）。
- 旧期路径实测：2018 版面 URL `…/html/2018/20180315/20180315_A01/20180315_A01_7315.html` 经 301 回落到根壳（未存档/被重定向），**2018 电子报不可靠**；2018 报道走网站搜索。

## 坑

- 搜索 API 要用 `https://s.bjnews.com.cn/bjnews/getlist`，别去解析 `search?q=` 的 SPA HTML。
- 电子报是图片 + 热点图，正文取不到文本；要文本用网站搜索/文章页。
- 电子报 API 有 `aesPaperInfoId` 动态 token，curl 直连不稳，须浏览器。
