# cpc.people.com.cn —— 人民网中国共产党新闻网

- 去哪找：频道首页 `http://cpc.people.com.cn/`；检索接口 `POST http://search.people.cn/search-platform/front/search`；检索页（空壳）`http://search.people.cn/getNewsResult/?channel=cpc&x=10&y=11&keyword={kw}`；文章页如 `http://sc.people.com.cn/n2/2026/1002/c345167-41713549.html`。
- 什么时候用：**「已知某稿存在、要找权威网页版全文」**；做「党建 / 基层治理 / 街乡吹哨」类标题或全文检索，并可跨人民网全站（含地方频道/理论频道）找转载。
- 怎么搜：检索入口挂在 `search.people.cn`：Nuxt SPA + JSON API —— **页面直连只有空壳，必须 POST JSON 接口**。
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

  # 检索：无需登录/cookie（本次带 Origin+Referer 调用成功）
  curl -s -m 20 -A "$UA" -H 'Content-Type: application/json;charset=UTF-8' \
    -H 'Origin: http://search.people.cn' -H 'Referer: http://search.people.cn/' \
    -X POST --data '{"key":"街乡吹哨","page":1,"limit":10,"hasTitle":false,"hasContent":true,"sortType":0,"startTime":0,"endTime":0}' \
    'http://search.people.cn/search-platform/front/search'

  # 正文
  curl -s -m 20 -A "$UA" 'http://sc.people.com.cn/n2/2026/1002/c345167-41713549.html'
  ```
  结果形态：JSON（`{"code":"0","data":{"records":[…]}}`）；**入库前剥 `<em>`**，要正文用 `contentOriginal` 或按 `url` 回抓。
- 覆盖：结果跨人民网全站（各地频道、理论频道、`*.people.com.cn`）；**索引只覆盖约 2021 年至今**（2020 及更早 = 0 条）。
- 门槛：免费，无需登录/cookie/Referer。
- 实测：2026-10-02，macOS（arm64），curl 8.x（`-m 20`，桌面 Chrome UA）：`cpc.people.com.cn` 首页 200/152789 B；`getNewsResult/?channel=cpc&keyword=街乡吹哨` 200/3370 B（空壳）；`POST /search-platform/front/search`（街乡吹哨 + hasTitle）→ 200 `total=0`；（街乡吹哨 + hasContent）→ 200 `total=543, pages=109, size=5`；（党建 + hasContent）→ 200 `total=134114`；`sc.people.com.cn` 文章页 200/45822 B 且 `div#rm_txt_zw` 命中。
- 上游：人民网 `https://www.people.com.cn/`；检索中台 `search.people.cn`。

## 细节

### 可用性矩阵（本机实测 2026-10-02，macOS + curl）

| 通道 | URL | 状态 | 现象 |
|---|---|---|---|
| 频道首页 | `http://cpc.people.com.cn/` | ✅ 200 | 152789 B，UTF-8，`<title>中国共产党新闻网--人民网` |
| 检索页（SPA） | `http://search.people.cn/getNewsResult/?channel=cpc&x=10&y=11&keyword={kw}` | ⚠️ 200 | 仅 3370 B Nuxt 空壳 + 4 个 `_nuxt/*.js`；**无服务端结果** |
| 检索 API | `POST http://search.people.cn/search-platform/front/search` | ✅ 200 | `application/json`，`{"code":"0","data":{"records":[…]}}` |
| 文章页 | `http://sc.people.com.cn/n2/2026/1002/c345167-41713549.html` | ✅ 200 | 45822 B，UTF-8；正文容器 `div#rm_txt_zw` |

### 请求体字段

| 字段 | 值 | 说明 |
|---|---|---|
| `key` | 关键词 | 接口内部会把 `@中央文件` / `@习近平经济思想数据库` 前缀剥掉（前端 JS 包中可见） |
| `page` | 1,2,… | 页码 |
| `limit` | 5 / 10 | 每页条数（实测 5、10 均正常） |
| `hasTitle` | true/false | **标题检索**开关 |
| `hasContent` | true/false | **全文检索**开关 |
| `sortType` | 0 | 排序（0 = 默认相关度；其他值**未验证**） |
| `startTime` / `endTime` | 0 | 时间区间（留 0 = 不限；非 0 的行为**未验证**） |

### 返回结构与解析

```json
{"code":"0","data":{
  "records":[{"title":"积极推动资源、服务、管理向基层下沉",
    "url":"http://theory.people.com.cn/n1/2026/0916/c40531-40799517.html",
    "content":"比如“<em>街</em><em>乡</em><em>吹</em><em>哨</em>、部门报到”的机制，就是由基层按需发起，部门依责响应，…",
    "contentOriginal":"<p>…</p>",
    "author":"付伟","source":1,"belongsName":"理论#经济社会","originName":"光明日报",
    "displayTime":1789518351000,"inputTime":1789518351000,
    "id":1000040799517,"domain":"theory.people.com.cn","pretitle":""}],
  "total":543,"size":5,"current":1,"pages":109}}
```

- 记录字段（实测）：`title`、`url`、`content`（**含 `<em>` 逐字高亮**）、`contentOriginal`（原始 HTML 正文）、`author`、`source`（**数值型来源 id**，非文本）、`originName`（来源名，如「光明日报」）、`belongsName`（频道，`#` 分隔，如「理论#经济社会」「四川频道#基层联播」）、`displayTime`/`inputTime`（**epoch 毫秒**，如 `1789518351000` = 2026-09-16）、`id`、`domain`、`newsJson`、`pretitle`/`subtitle`/`shorttitle`、`hasImg`/`hasVideo`、`isOfficial`、`belongsId` 等。
- 分页元数据齐全：`total`/`size`/`current`/`pages`。
- **入库前剥 `<em>`**：`content` 是带高亮的检索片段，不是干净正文；要正文用 `contentOriginal` 或按 `url` 回抓。

### 实测命中量（2026-10-02）

| 请求体关键项 | 结果 |
|---|---|
| `key=街乡吹哨, hasTitle=true` | `total=0` —— 人民网几乎没有以「街乡吹哨」为标题的稿 |
| `key=街乡吹哨, hasContent=true` | `total=543, pages=109`；首条 `theory.people.com.cn` 2026-09-16《积极推动资源、服务、管理向基层下沉》，正文含「街乡吹哨、部门报到」 |
| `key=党建, hasContent=true` | `total=134114`；5 条为 2026-10-02 各地频道稿 |

### 正文抓取

```bash
curl -s -m 20 -A "$UA" '<url>' | python3 -c "
import sys,re
h=sys.stdin.read()
m=re.search(r'id=\"rm_txt_zw\"[^>]*>(.*?)(?:</div>\s*){1}',h,re.S)
print(re.sub(r'(?s)<[^>]+>','',m.group(1)) if m else 'NO MATCH')"
```

- 人民网系文章页是**静态 HTML、UTF-8**；正文标准容器 `div#rm_txt_zw`（外层为 `div.rm_txt_con.cf`、`div.layout.rm_txt.cf`）—— `rm_txt` 命名的页面族基本通用。
- 标题取 `<title>`；页内导航/相关推荐很多，按容器截取，别整页入库。

## 坑

1. **别直连检索页**：`search.people.cn/getNewsResult/` 是 Nuxt 空壳（3.3 KB），结果全靠 `_nuxt/*.js` 调的 `POST /search-platform/front/search`。本次是从 `_nuxt/21b102a.js` 里挖出接口路径（`apiGetsearch` → `$axios.$post("/search-platform/front/search", e)`），路径同样出现在 `get-ip`/`searchRank`/`searchKeysRank` 等兄弟接口里。
2. **`hasTitle` 单独开召回极少**：本课题关键词在标题里几乎不出现，直接用 `hasContent=true`。
3. **结果跨人民网全站**，不限于 cpc 子站（各地频道、理论频道、`*.people.com.cn`）→ 需要「只看党建/理论」时按 `belongsName`/`domain` 自行过滤；老检索页 URL 里的 `channel=cpc` 在 JSON API 里的等价参数**未验证**。
4. **索引时间窗（做 2018 年课题请注意）**：人民网站内检索索引只覆盖约 **2021 年至今**；同日 `../media/people.com.cn.md` 实测「街乡吹哨」按年：2021=37、2022=155、2023=67，**2020 及更早 = 0**。想找 2018 年的人民网稿，别用这个检索，改走 `web_search site:people.com.cn` 或数字报（见 `../media/epaper/`）。
5. 未验证（**另有同日实测结论见 `../media/people.com.cn.md`**）：`startTime`/`endTime` 为 epoch 毫秒整数（本文件未验证）；`limit` 上限（media 文件实测 `limit=100` 可用）；`sortType` 语义；高频调用限流（本次 8 次请求、间隔 ≥1.5s，未触发任何验证/验证码）。
6. 落盘：结果 URL 分布在多个 `*.people.com.cn` 子域，抓正文按域名分片 JSONL（避免多进程 append 撕裂行）。
