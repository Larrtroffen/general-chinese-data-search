# xinhuanet.com —— 新华网文章直读/检索

新华网现主域为 `news.cn`（`www.xinhuanet.com` 仍可访问）。文章页静态、curl 直读；**站内检索 `so.news.cn/getNews` 走 WAF/JS 挑战，本机 curl 出 405，仅在真实浏览器会话（同源 fetch + cookie）内返回 JSON**。

- 去哪找：总网 `http://www.news.cn/`；北京频道 `http://bj.news.cn/`；文章页 `https://www.news.cn/YYYYMMDD/<32位hex>/c.html`；站内检索 `https://so.news.cn/getNews?lang=cn&curPage=1&searchFields=0&sortField=0&keyword=<关键词>`
- 什么时候用：取新华网总网/北京频道文章；按关键词做站内检索（须真实浏览器）
- 怎么搜：文章页 curl 直读（grep 首页链接即可批量抽）；检索接口只能在 `so.news.cn` 页面上下文内同源 `fetch`
- 覆盖：总网 + 北京频道文章；检索每页 10 条
- 门槛：无（检索需真实浏览器会话）
- 实测：2026-10-02，macOS + curl：`www.news.cn` 200/164,701 B、`www.xinhuanet.com` 200、`bj.news.cn` 200/54,047 B；文章页 200；`so.news.cn` 与 `getNews` curl 均 405（WAF 页）；浏览器页面内 fetch `getNews` 200 JSON（`code=200`，返回 10 条，字段 title/url/pubtime/sitename）。
- 上游：<http://www.news.cn/>

## 细节

### 可用性矩阵（实测 2026-10-02，macOS + curl，桌面 UA）

| 入口 | 状态 | 现象 |
|---|---|---|
| `http://www.news.cn/` | ✅ 200 | 首页 HTML，164,701 B |
| `http://www.xinhuanet.com/` | ✅ 200 | 仍可访问（本机未 301），内容与 news.cn 同源 |
| `http://bj.news.cn/` | ✅ 200 | 北京频道，54,047 B，`<title>新华网北京频道_北京新闻_首都</title>` |
| `https://www.news.cn/YYYYMMDD/<hash>/c.html` | ✅ 200 | 文章页静态 HTML（示例 18,916 B） |
| `http://bj.news.cn/YYYYMMDD/<hash>/c.html` | ✅ 200 | 北京频道文章（示例 13,960 B），正文在 `#detailContent` / `#articleEdit` |
| `GET https://so.news.cn/getNews?...`（curl） | ❌ 405 | 返回 WAF 拦截页（`<title>405</title>`，65,179 B）；带浏览器 UA/Referer/cookie 仍 405 |
| `GET https://so.news.cn/`（curl） | ❌ 405 | 同上，整个 `so.news.cn` 对非浏览器请求拦死 |
| `GET https://so.news.cn/getNews?...`（**浏览器页面内 fetch**） | ✅ 200 JSON | 同源、带 cookie 时返回结果（见下） |

### 文章页 URL 规律

```
总网：    https://www.news.cn/YYYYMMDD/<32位hex>/c.html
北京频道：http://bj.news.cn/YYYYMMDD/<32位hex>/c.html
```

- 例：`https://www.news.cn/20260806/0ab87c34c9654d56834eeff74e300b34/c.html`（✅ 200）。
- 例：`http://bj.news.cn/20260930/c1aa02d0e0d3462cb7655bfcd1575d1c/c.html`（✅ 200）。
- 首页/频道页里的文章链接即此格式，可直接 grep `/(\d{8})/([a-f0-9]{32})/c\.html` 批量抽取。

### 站内检索（so.news.cn/getNews）——需浏览器

接口（GET，返回 JSON）：

```
https://so.news.cn/getNews?lang=cn&curPage=1&searchFields=0&sortField=0&keyword=<关键词>
```

- `searchFields`：`0`=新闻全文（默认），`1`=仅标题（页面另有「在新闻全文中 / 仅在新闻标题中 / 学术理论文献」单选）。
- `curPage`：页码，从 1 起。
- 返回：`{"code":200,"content":{"keyword":…,"curPage":1,"results":[{title,url,pubtime,sitename,contentId,des,imgUrl}…]}}`（每页 10 条）。
- **curl 直连被 WAF 拦（405）**；只有从 `so.news.cn` 页面上下文发同源 `fetch`（携带页面 JS 下发的 `xhs` 等 cookie）才 200。

**workaround（推荐用浏览器，不用 curl）：**

```js
// Playwright/Chromium 打开 https://so.news.cn 后，在页面上下文执行：
const r = await fetch('https://so.news.cn/getNews?lang=cn&curPage=1&searchFields=0&sortField=0&keyword=' + encodeURIComponent('街乡吹哨'));
const j = await r.json(); // j.code===200, j.content.results[]
```

- 或退回 `web_search site:news.cn {关键词}`（本机内置 `web_search` 适合点查）。
- 搜索页地址：`https://so.news.cn/#search/0/<关键词>/1/`（hash 路由，SPA）。

## 坑

- `so.news.cn` 检索**不能靠 curl**（WAF 识别 TLS/JS 指纹，仅设 cookie 无效）；要么浏览器，要么换通道。
- 文章页用 `http://` 与 `https://` 皆可；北京频道链接在首页以 `http://bj.news.cn/…` 出现。
- `news.cn` 与 `xinhuanet.com` 是同一批文章，可互为备用域名。
