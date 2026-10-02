# ncpssd.org —— 中文社科期刊检索与摘要

国家哲学社会科学文献中心（中国社会科学院图书馆承建），收录中文社科期刊论文 3000 万+，**检索与摘要公开**；PDF 全文需登录（免费注册）后下载。是中文社科论文最可用的机器检索通道（curl 直连 JSON API，实测无验证码）。

- 去哪找：`https://www.ncpssd.org/`；人可读检索页 `https://www.ncpssd.org/Literature/articlelist?sType=0&search={base64表达式}`；结果 API `POST https://www.ncpssd.org/searchHandler/search`；详情 API `POST https://www.ncpssd.org/articleinfoHandler/getjournalarticletable`；下载 `GET https://www.ncpssd.org/Literature/Download?id=…&title=…`
- 什么时候用：要中文社科期刊论文列表/摘要/机构/核心收录；要匿名 JSON 直连（无验证码/无 cookie）的中文通道
- 怎么搜：构造 base64 检索表达式 → 走 POST JSON API（模板与字段码见下「细节」）
- 覆盖：中文社科期刊论文 3000 万+；检索/摘要公开；PDF 全文需登录
- 门槛：检索/摘要免费匿名；PDF 下载需免费注册登录（机构用户走 `POST /organLogin`）
- 实测：2026-10-02，macOS + curl 8.x + Python 3.9（stdlib）：
  - `GET https://www.ncpssd.org/` → `HTTP 200 size=198008`
  - `POST /searchHandler/search`，`搜 一带一路` → `total=32702`（首行《"一带"和"一路"如何成为"一带一路"?》）；`吹哨` → `total=154`；`基层治理` → `total=7279`
  - `IKTE="基层治理"` → 4168；`IKST="基层治理"` → 5788；`IKCR="孟天广"` → 0
  - `POST /articleinfoHandler/getjournalarticletable` `{"lngid":"7000476172",…}` → `HTTP 200 size=2466`，`pagecount=2`
  - `GET /Literature/Download?id=7000476172` → `HTTP 302 Location: /login`
  - `GET http://www.nssd.org/articles/article_down.aspx?id=7000476172` → 200 text/html（域名停放广告）
- 上游：`https://www.ncpssd.org/`（中国社会科学院图书馆承建）

## 细节

### 可用性矩阵

| 入口 | 状态 | 现象 |
|---|---|---|
| `https://www.ncpssd.org/` | ✅ | HTTP 200，服务端渲染首页 |
| `GET /Literature/articlelist?sType=0&search=<base64表达式>` | ⚠️ | 200，但结果区是 JS 壳（HTML 内不含条目），需走下方 POST API |
| `POST /searchHandler/search` | ✅ | 200，返回 JSON 列表（本机全程无验证码/无 cookie） |
| `POST /articleinfoHandler/getjournalarticletable` | ✅ | 200，返回单篇详情 JSON（首次约 19s，偏慢） |
| `GET /Literature/Download?id=…&title=…` | ❌→登录 | 302 跳 `/login`，PDF 下载需登录 |
| 行内字段 `pdfurl`（`www.nssd.org/...`） | ❌ | 该域名已是被停放"域名出售"页（2026-10-02 实测 200 但正文为域名交易广告），**勿用** |

### 检索流程（curl 模板）

**1) 构造检索表达式**——站点把表达式 base64 后放 URL：`search` 的明文形态为：

```
(IKTE="关键词" OR IKPYTE="关键词"  OR IKST="关键词" OR IKET="关键词" OR IKSE="关键词")
```

字段码（实测）：`IKTE`=题名（`IKTE="基层治理"` → 4168 条）、`IKST`=主题词/关键词（→ 5788 条）。`IKPYTE`/`IKET`/`IKSE` 见首页链接原样，**未逐项验证**；作者字段名未探明（试 `IKCR` 返回 0，**未验证**）。

```bash
KW='基层治理'
SEARCH=$(python3 -c "import base64,sys;print(base64.b64encode(('(IKTE=\"%s\" OR IKPYTE=\"%s\"  OR IKST=\"%s\" OR IKET=\"%s\" OR IKSE=\"%s\")'%((sys.argv[1],)*5)).encode()).decode())" "$KW")
# 人可读的检索页（浏览器打开）：
# https://www.ncpssd.org/Literature/articlelist?sType=0&search=$SEARCH
```

**2) 取结果列表（JSON，推荐）**——**关键坑**：`/Literature/articlelist` 的 URL 参数是 **base64(表达式)**；而 API `/searchHandler/search` 的 `search` 表单字段要传 **明文表达式**（即 base64 解码后的那串）。传错就 `total:0`。

```bash
curl -s -m 20 \
  -A 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' -H 'Referer: https://www.ncpssd.org/Literature/articlelist' \
  --data-urlencode "search=(IKTE=\"$KW\" OR IKPYTE=\"$KW\"  OR IKST=\"$KW\" OR IKET=\"$KW\" OR IKSE=\"$KW\")" \
  --data-urlencode 'pageNum=1' --data-urlencode 'pageSize=20' \
  --data-urlencode 'sort=' --data-urlencode 'sType=0' \
  --data-urlencode 'ajaxKeys=' --data-urlencode 'customShowCondition=' \
  'https://www.ncpssd.org/searchHandler/search'
```

返回：`{"result":true,"code":200,"data":{"total":32702,"rows":[…],"pages":…,"currentPage":…}}`。
`sType=0` 为"全部文献"（URL 实测）；其他取值 **未验证**。`sort` 可留空。

**3) 结果行字段（实测 `rows[0]`）**

| 字段 | 含义 |
|---|---|
| `id` / `data_id` | 文献号，即详情接口的 `lngid` |
| `title` | 题名 |
| `creator` | 作者（含机构序号，如 `邵妍[1]`） |
| `cbw_name` | 刊名 |
| `date` | ISO 时间（如 `2018-04-01T00:00:00.000+0000`） |
| `type` | 文献类型（`中文期刊文章`） |
| `num` / `volumn` / `years` | 期 / 卷 / 年 |
| `range` | 核心收录（如 `核心刊;BDHX2014;CSSCI2017_2018`） |
| `beginpage`/`endpage`/`pagecount` | 起止页 / 页数 |
| `remark` | 摘要 |
| `subject` | 主题词（分号分隔） |
| `institutions` | 机构 |
| `issn` / `gch` | ISSN / 国内刊号 |
| `tab_name` | 资源表（`journalArticle`） |
| `pdfurl` | ⚠️ 指向已失效的 `nssd.org`，勿用 |

**4) 单篇详情**

```bash
curl -s -m 40 -A '<desktop UA>' \
  -H 'Content-Type: application/json; charset=utf-8' -H 'X-Requested-With: XMLHttpRequest' \
  --data '{"lngid":"7000476172","type":"中文期刊文章","pageType":1}' \
  'https://www.ncpssd.org/articleinfoHandler/getjournalarticletable'
```

返回字段较列表更全：`titlec`(题名)、`remarkc`(摘要)、`keywordc`、`showwriter`(作者)、`firstorgan`/`fstorgan`、`beginpage`/`endpage`、`mediac`(刊名)、`issn`、`publishdate` 等。

详情**页面** URL（JS 壳，数据仍来自上面的 API）：

```
https://www.ncpssd.org/Literature/articleinfo?id=<b64(id)>&type=<b64(Journal)>&datatype=<b64(typename)>&typename=<b64(typename)>
```

### 全文下载（登录墙）

- 下载端点：`GET https://www.ncpssd.org/Literature/Download?id=<id>&title=<title>` → 实测 **302 → `/login`**。
- 个人免费注册账号后可下载（页面免费开放中文期刊全文为其卖点）；机构用户走机构登录（页面另有 `POST /organLogin`）。
- 站内 JS 有网宿 WAF 的 `wzws-api-verify` 逻辑，但本次 curl 探针（无该头、无 cookie）均正常，**说明检索/详情接口不强制该头**。

## 坑

- **base64 vs 明文**：URL 用 base64，API 用明文，最容易踩。
- URL 里的 `search` 若手工拼错一个中文引号/空格数量即可导致 0 结果；直接复刻首页链接格式最稳。
- 详情接口较慢（冷启 ~19s），批量抓取请并发+限速（本库礼貌值：≤3 req/host/s，间隔 ≥1.5s）。
- `pdfurl` 字段不可信。
