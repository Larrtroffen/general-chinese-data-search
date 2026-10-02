# search-syntax —— 引擎操作符与站内检索参数速查

- 去哪找：综合引擎 Google / 必应 `cn.bing.com` / 百度 / 360 / Yandex / Mojeek·Marginalia·Brave；站内检索页 `s.weibo.com`、`www.zhihu.com`、`weixin.sogou.com`、`api.bilibili.com`、`www.xiaohongshu.com`；内置 `web_search`。逐 host 状态见 `../engines/README.md`（不重复）。
- 什么时候用：要把关键词**拼成正确查询**；怀疑结果被引擎改写或操作符**静默失效**；要按时间 / 类型 / 站点筛；站内检索找不到入口、要直接拼参数。
- 怎么搜：**先选引擎**（保真度不同），再用该引擎认的操作符；**站内检索同理，认参数不认界面**。操作符对照表、引擎分工、站内平台参数见「细节」。
- 覆盖：6+ 综合引擎的操作符差异；5 个站内平台（微博 / 知乎 / 搜狗微信 / B 站 / 小红书）。
- 门槛：多数免登录；知乎 / 小红书 / 微博检索需登录态；内置 `web_search` 批量约 25 次调用后全 provider 429。
- 实测：2026-10-03，macOS（arm64），curl 8.x（`-m 20`，桌面/iPhone UA，同主机间隔 ≥1.5 s）。
- 上游：各引擎与平台站内检索页（入口见「细节」）；逐 host 状态另见 [`../engines/README.md`](../engines/README.md)。

> 凡标「本机实测」= 本机 curl 真跑过；标「上游声明」= 来自文档/他人结论、本机未复现。

## 细节

### A. 综合引擎操作符对照（差异决定结果，不是花边）

| 操作符 | Google | 必应 (Bing) | 百度 | 360 | Yandex | 独立爬虫 (Mojeek/Marginalia/Brave) |
|---|---|---|---|---|---|---|
| `"精确短语"` | 支持但会被改写/词干化 | 更字面 | 支持 | `"` 支持 | 支持 | 通常最字面 |
| `site:` | 支持域名/TLD，但**强去重+截断，无法穷举** | **最字面、枚举最全** | 支持（移动版实测生效） | 支持（实测生效） | 支持，另有 `host:`/`rhost:` | 视引擎 |
| `-排除` | 支持 | 支持 | 支持 | 支持 | 支持，另 `~~` | 视引擎 |
| `OR` / `\|` | 需大写 `OR` | 支持 | 支持 | 支持 | 支持 | 视引擎 |
| `filetype:` | 按**索引判定的文档类型** | `filetype:` + `ext:`（按 URL 后缀，抓 `.env/.bak/.sql` 用这个） | 支持 | 支持 | 用 `mime:` | 常缺 |
| `intitle:` / `inurl:` | 支持（`all*` 形式别混用） | 支持，另有 `url:` | 支持 | 支持 | `title:`/`url:` | 部分支持 |
| `intext:` | 支持 | 支持 | 支持 | 支持 | 支持 | 不可靠 |
| 时间 | `before:`/`after:`（**推断日期，不可当证据**） | 仅 UI 日期筛选 | UI | UI | `date:` | — |
| 区间/数值 | `..`（如 `2018..2020`） | 弱 | 弱 | 弱 | `date:` | — |

- 独家操作符：**必应 `ip:`**（按 IP 反查索引，共享主机/CDN 上无意义）、`contains:`（找链接到某类文件的页）、`language:`/`loc:`；**Yandex** `/n`（词距）、`&`（同句）、`&&`（同文）、前缀 `!`（关闭词形还原）。
- 已失效、别再用（写了不报错、静默变普通词）：`cache:`、`info:`、`link:`、`related:`、`inanchor:`、`AROUND(n)`、`+`强制包含、`~`同义。

### B. 引擎改写 = 最坑的地方（静默失败）

- **Google 最激进**：词干化、同义替换、拼写纠正、丢「无用」词、个性化。唯一可用的 dork 状态是 **Verbatim（工具→「所有结果」下拉）**。结果页顶部出现 `Missing: <term>` 就是它丢了你的词 → **该次查询作废**，用 "Must include:" 重跑。
- **必应**改写较轻，会给「包括…的结果 / 仅搜索原文」链接。
- **Yandex** 默认词形还原（俄语有用、查标识符有害）→ 术语前加 `!`。
- **脚本/无 cookie 请求会静默降级**：操作符被忽略、结果被塞垃圾、计数仍是「正常」的。**脚本返回 ≠ 浏览器返回**；任何依赖的操作符，用「已知答案的对照查询」自检一次。

**引擎分工（经验）**：`site:` 穷举放必应；正文/精确串放 Google Verbatim；非拉丁/图片放 Yandex；老、冷门、个人站放 Mojeek / Marginalia / Brave。**零结果只说「这个索引没有」，别说「网上没有」**。

### C. 站内检索（本机实测）

#### 微博 `s.weibo.com` —— 高级搜索参数

```
https://s.weibo.com/weibo?q={关键词}
  &typeall=1&suball=1                      # 综合/全部子类
  &timescope=custom:2018-01-01:2018-12-31  # 自定义时间窗
  &Refer=g                                 # 高级搜索标记
```
- **本机实测（2026-10-03）**：`https://s.weibo.com/weibo?q=区划调整&typeall=1&suball=1&timescope=custom:2024-01-01:2024-12-31&Refer=g` → **HTTP 302**（→ `passport.weibo.com/visitor/...`），**无登录态取不到结果页**。参数名来自微博高级搜索表单（**上游声明**，生效性未实测）；登录态下的可用性见 `../social/weibo.com.md`（需真实登录 cookie）。
- 唯一匿名可用仍是热搜 JSON（带 `Referer`）。

#### 知乎 `www.zhihu.com`

- `https://www.zhihu.com/search?type=content&q={kw}` → **403**，body 含 `<meta id="zh-zse-ck">` 反爬标记（实测）。
- `https://www.zhihu.com/api/v4/search_v3?t=general&q={kw}&correction=1&offset=0&limit=20` → **400 `{"HitLabels":null}`**（需 `x-zse-96` 客户端签名，未签名不可用，实测）。
- **结论：匿名只能拿搜索引擎里的标题/URL 线索**（`site:zhihu.com {kw}`）；正文要登录态工具箱，见 `../social/README.md`。

#### 微信公众号：搜狗微信 `weixin.sogou.com`

```
https://weixin.sogou.com/weixin?type=2&query={关键词}&ie=utf8   # type=2 文章；type=1 公众号
```
- **本机实测（2026-10-03，iPhone UA + cookie jar）**：200 / 31 KB，title `区划调整的相关微信公众号文章 – 搜狗微信搜索`，首页 9 条 `class="txt-box"`，页内 10 个 `page=` 链接。
- **`query` 的硬限制 = 索引上限**：每条检索式最多 **10 页 × 10 条 = 100 条**；`tsn/ft/et` 时间过滤已封死 → 放量只能靠「**年份词 + 主题词**」拆式，主题词饱和后新增趋零。详见 `../wechat/weixin.sogou.com.md`。

#### B 站（bilibili）—— 有开放 JSON，实测 ✅

```
https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={kw}&page=1
  # search_type: video | media_bangumi | media_ft | live | article | bili_user
```
- **本机实测（2026-10-03，桌面 UA，无 cookie）**：**200 / 27 KB JSON，`code:0`、`numResults:1000`、`numPages:50`**（无需登录）。HTML 壳 `https://search.bilibili.com/all?keyword={kw}` 也 200，但结构化结果在 API。
- 用途：地方政务号/媒体号的视频、事件传播线索；`?page=` 可翻页。风控阈值未探（未做高频）。

#### 小红书 `www.xiaohongshu.com`

- **本机实测**：`/search_result?keyword=test` → **301**（补尾斜杠后 200 / 60 KB，title `test - 小红书搜索`）。SSR 的 `window.__INITIAL_STATE__` 里 `search.searchContext = {keyword, page:1, pageSize:20, sort:'general', noteType:0, filters:[], geo:''}` —— 说明参数结构；但 **`search.feeds: []` 为空 → 结果不入 SSR，需登录 + JS**。
- 结论：**仅浏览器/需登录**；走 `../social/xiaohongshu-mcp.md`（扫码 + 住宅 IP；时间粒度只有「一天/一周/半年」，做不了按年回溯）。

#### 兜底：内置 `web_search`

- 支持 `site:`/`after:`/`intitle:`/`filetype:`，短点查最快；但实测约 **25 次调用后全 provider 429**，批量别用（见 `../engines/README.md`）。

### 实测

2026-10-03，macOS（arm64），curl 8.x（`-m 20`，桌面/iPhone UA，同主机间隔 ≥1.5 s）：`https://www.google.com/search?q=test` → **000**（DNS 层：`www.google.com`→31.13.92.37 非 Google 段）；`https://www.google.com.hk/search?q=test` → 000；`https://cn.bing.com/search?q=site%3Abjchy.gov.cn+吹哨&format=rss` → 200/4248 B，但条目为无关垃圾域（未预热 cookie 即降级）；`https://www.baidu.com/s?wd=site%3Agov.cn+区划调整` → **302**（body 含 `wappass`/安全验证）；`https://m.baidu.com/s?word=site%3Agov.cn+区划调整` → 200/1.84 MB，title `site:gov.cn 区划调整 - 百度`，含 6 处 gov.cn 结果域（`site:` 生效）；`https://www.so.com/s?q=site%3Agov.cn+区划调整` → 200/255 KB，`res-title` 7 条，首条「省人民政府批复同意石阡县部分行政区划调整」；`weixin.sogou.com/weixin?type=2&query=区划调整` → 200/31 KB，9 条结果 + 10 个 `page=`；`s.weibo.com/weibo?q=...&timescope=...` → 302 visitor；`www.zhihu.com/search?type=content&q=...` → 403（`zh-zse-ck`），`api/v4/search_v3` → 400；`api.bilibili.com/x/web-interface/search/type?...` → 200 JSON `code:0`；`www.xiaohongshu.com/search_result/?keyword=test` → 200 且 `search.feeds=[]`（结果需登录）。

## 坑

1. **操作符失效是静默的**——`cache:`/`info:` 这类写进去变成普通词，返回「看似正常」的泛结果；定期用已知答案自检。
2. **结果计数不可引用**：各引擎口径不同、翻页会变，都是估计值。
3. **`before:/after:` 是推断日期**，CMS 每次渲染会盖当前日期；要真日期去档案（`historical-web.md`）。
4. **`site:` 不穷举**：Google 截断狠、必应深但也不全；要真枚举用档案 CDX。
5. **反爬看客户端指纹（TLS/头序/是否执行 JS），不只是频率**——降速往往没用；限频按各卡：≤3 次/主机、间隔 ≥1.5s、timeout 20s、桌面 UA。
6. 站内检索**优先直接调它的 JSON 接口**（B 站是范例：页面是壳、接口是正路）。
