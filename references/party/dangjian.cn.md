# dangjian.cn —— 党建网文章检索

- 去哪找：首页 `http://www.dangjian.cn/`；检索接口 `http://www.dangjian.cn/mi4-rest-api/pageArticles.js?wbId=91&page=1&limit=25&title={URL编码关键词}`；文章页如 `http://www.dangjian.cn/xccs/2026/09/30/detail_202609307838225.html`。
- 什么时候用：做「党建 / 基层治理 / 街乡吹哨」类**个案点查**（拿标题、发布时间、栏目、原文链接）；也是「权威引用口径」的来源之一。
- 怎么搜：站内检索是**前端异步**：搜索页只是壳，真正干活的是 MI4 CMS 的 `pageArticles.js` 接口（返回一段 JS）。接口直连可用、**无需登录、无需 Referer**。
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
  KW='%E8%A1%97%E4%B9%A1%E5%90%B9%E5%93%A8'   # 街乡吹哨

  # ① 站内检索（标题级）：关键词 → title，翻页 → page，每页条数 → limit
  curl -s -m 20 -A "$UA" \
    "http://www.dangjian.cn/mi4-rest-api/pageArticles.js?wbId=91&subjectId=&page=1&limit=25&title=$KW"

  # ② 文章正文（静态 HTML，UTF-8）
  curl -s -m 20 -A "$UA" 'http://www.dangjian.cn/xccs/2026/09/30/detail_202609307838225.html'
  ```
  结果形态：`text/javascript`，返回 `var MI4_PAGE_ARTICLE=[…]`（非纯 JSON）；**没有全文**（`miSummary` 是摘要），要正文按 URL 二次抓取。
- 覆盖：中央级党建资讯网站，日更新（本次实测最新稿为 2026-09-30）；**标题级检索**，非全文。
- 门槛：免费、免登录，无需 Referer；**只走 http**（https 443 建不起来）。
- 实测：2026-10-02，macOS（arm64），curl 8.x（`-m 20`，桌面 Chrome UA，同主机间隔 ≥1.5s）：首页 200/80602 B；`search.html?keyword=街乡吹哨` 200/16792 B（无列表）；`pageArticles.js`（街乡吹哨，limit=25）→ `_totalCnt=1`（2020-03-13 人民日报转载稿）；`pageArticles.js`（党建，page=1，limit=25）→ `_totalCnt=5605, _totalPage=225`，首条 2026-09-30 10:29；`page=2` → `_currPage=2`、25 条；`limit=5` → `_pageSize=5, _totalPage=1121`；2026 稿正文页 200/42336 B；2020 稿 URL 404「页面已过期」；`https://` 变体 `HTTP=000`；**正文内短语检索 `_totalCnt=0`**（标题级证据）；不带 Referer 调接口同样 200。
- 上游：党建网（中宣部主管·《党建》杂志社主办）`http://www.dangjian.cn/`。

## 细节

### 可用性矩阵（本机实测 2026-10-02，macOS + curl）

| 通道 | URL | 状态 | 现象 |
|---|---|---|---|
| 首页 | `http://www.dangjian.cn/` | ✅ 200 | 80602 B，UTF-8，`<title>党建网 - 中宣部主管全国性党建网站` |
| HTTPS 全文 | `https://www.dangjian.cn/…` | ❌ | 443 建不起来（`HTTP=000`）→ **本机只走 http** |
| 检索页 | `http://www.dangjian.cn/search.html?keyword={kw}` | ⚠️ 200 | 16792 B 外壳页；结果由 JS 拉取，curl 直接看**没有列表** |
| 检索接口 | `http://www.dangjian.cn/mi4-rest-api/pageArticles.js?…` | ✅ 200 | `Content-Type: text/javascript`，返回 `var MI4_PAGE_ARTICLE=[…]`（4316–17342 B） |
| 文章页（2026 稿） | `http://www.dangjian.cn/xccs/2026/09/30/detail_202609307838225.html` | ✅ 200 | 42336 B，UTF-8，正文容器 `<div id="tex" class="article">` → `<div class="TRS_Editor">` |
| 文章页（2020 稿，来自检索结果） | `http://www.dangjian.cn/gddj/2020/03/13/detail_202003135472756.html` | ❌ 404 | 站内 404 页「党建网---您访问的页面已过期」 |

### 请求参数（取自检索页内联 JS，实测均有效）

| 参数 | 值 | 说明 |
|---|---|---|
| `wbId` | `91` | 本站站点 ID（写死） |
| `subjectId` | 空串 | 检索页内置为空；栏目限定是否可用**未验证** |
| `page` | 1,2,… | 页码（实测 `page=2` 返回第 26–50 条） |
| `limit` | 25（检索页默认） | 每页条数；实测 `limit=5` → `_pageSize=5`、`_totalPage=1121`（与 5605 条自洽） |
| `title` | 关键词（URL 编码） | **标题检索**（见「坑」#1） |

### 返回结构与解析

返回的是**一段 JS**（不是纯 JSON）：4 个统计变量 + 一个数组。

```javascript
var _totalCnt=5605;//总数量
var _totalPage=225;//总页数
var _currPage=1;//当前页码
var _pageSize=25;//页显示数量
var MI4_PAGE_ARTICLE = [{"miViewCnt":475,"miCover11":"","shortTitle":"",
  "title":"以习近平党建思想规定中共党史党建学学科根本使命","pub_date":"2026-09-30 10:29",
  "subNm":"宣传阐释","miSummary":"程美东 习近平党建思想对新时代党的建设所面临的一系列方向性、根本性、全局性问题作出了系统而深刻的回答，…",
  "miType":4,"miRespAuthor":"王寒","miCover169":"","miCover43":"","pubAuthor":"","miAuthor":"",
  "url":"http://www.dangjian.cn/xccs/2026/09/30/detail_202609307838225.html","external_link":"",
  "subtitle":"","miOrigin":"《中州学刊》2026年第8期","miTags":"研究,理论,机制,党建,治理"}]
```

```python
import re, json
s = open('resp.js', encoding='utf-8').read()
cnt  = re.search(r'_totalCnt=(\d+)', s).group(1)
pgs  = re.search(r'_totalPage=(\d+)', s).group(1)
arr  = json.loads(s[s.index('['): s.rindex(']') + 1])
for r in arr:
    url = r.get('external_link') or r.get('url')     # 页面 JS 同样优先取 external_link
```

- 记录字段（**随稿件新旧而变，务必用 `.get()`**）：`title`、`url`、`pub_date`（`YYYY-MM-DD HH:MM`）、`subNm`（栏目：宣传阐释 / 各地党建 / 机关党建 …）、`miOrigin`（来源，如「《中州学刊》2026年第8期」「人民日报」）、`shortTitle`；
  常见可选：`miSummary`（**摘要**，本次 25 条中 14 条非空）、`miTags`（逗号分隔标签）、`external_link`（**外链，有值时应优先当目标地址**，本次 25 条中 8 条非空）、`subtitle`、`miAuthor`/`pubAuthor`/`miRespAuthor`、`miCover11/169/43`（配图）、`miViewCnt`。
- 老稿记录字段更少（「街乡吹哨」唯一一条 2020 年稿只有 title/url/pub_date/subNm/miOrigin/… 无 `miSummary`/`miTags`）。
- **没有全文**（`miSummary` 是摘要，不是正文）→ 需要正文时按 URL 二次抓取。

### 与同类源的关系

- 中组部党员教育平台 → `12371.cn.md`；北京市委组织部 → `bjdj.gov.cn.md`；顺义组工镜像 → `cdcghy.com.md`；人民网·中国共产党新闻网（全文检索可用）→ `cpc.people.com.cn.md`。

## 坑

1. **检索是标题级，不是全文**：拿文章正文里的独有短语（「一切创造，归结」）检索 → `_totalCnt=0`；拿标题词（「街乡吹哨」）→ 命中。别指望它做内容检索（要全文检索请用 `cpc.people.com.cn.md` 的人民网接口）。
2. **旧链接大量失效**：索引里仍挂着 2020 年老稿，但点开是站内 404「您访问的页面已过期」（改版后老路径未保留）。批量消费检索结果前先验活：
   ```bash
   curl -s -o /dev/null -w '%{http_code} %{url_effective}\n' -m 15 -A "$UA" '<url>'
   ```
3. **只支持 http**：`https://www.dangjian.cn/...` 本机 `HTTP=000`。
4. **检索页直连没结果**：`search.html?keyword=` 是壳（搜索框点击后 `window.open('/search.html?keyword=…')`，列表再靠 `pageArticles.js` 拉）→ 直接调接口。
5. 未验证：全文/栏目（`subjectId`）检索、日期区间参数、`limit` 上限、调用限流（本次约 12 次请求、间隔 ≥1.5s，未触发任何验证码）。
