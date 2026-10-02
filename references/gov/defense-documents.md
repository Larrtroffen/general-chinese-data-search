# defense-documents —— 国防白皮书与涉军文件

- 去哪找：
  - 国防部网（mod.gov.cn）**白皮书**栏目 `http://www.mod.gov.cn/gfbw/fgwx/bps/index.html`——国新办国防/涉军类白皮书转发（含全文）
  - 国防部网 **法规文献**总栏 `http://www.mod.gov.cn/gfbw/fgwx/index.html`（下含法律法规 `/flfg/`、司法解释 `/sfjs/`、出版物 `/cbw/`、文件 `/wj_213958/`）；**军事文献** `http://www.mod.gov.cn/gfbw/jswj/index.html`；**权威发布** `http://www.mod.gov.cn/gfbw/qwfb/index.html`；**新闻发言人** `http://www.mod.gov.cn/gfbw/xwfyr/index.html`（发言人谈话、例行记者会）
  - 国防部站内检索 JSON API `http://mod-search.mod.gov.cn/api-surface/es/docSearchEasy`
  - 国务院新闻办（国新办）白皮书 `http://www.scio.gov.cn/zfbps/`；历次国防白皮书在分年目录 `/zfbps/ndhf/{年}n/` 下（如 `/zfbps/ndhf/2019n/`）（目录规律来自公开检索索引，未本机实测）；白皮书检索 `http://www.scio.gov.cn/search/bps/index.html`（**本机不可直连**，见坑 1）
  - 国防支出：财政部预算司 **全国财政决算** `http://yss.mof.gov.cn/{年}zyjs/`（如 `/2025zyjs/`）、**中央财政预算** `http://yss.mof.gov.cn/{年}zyczys/`（如 `/2026zyczys/`）——支出决算/预算表内含「国防支出」行；财政部 **财政数据** `https://www.mof.gov.cn/gkml/caizhengshuju/`
- 什么时候用：要国防白皮书历次全文（《新时代的中国国防》2019、《中国军队参加联合国维和行动30年》2020、《新时代的中国军控、裁军与防扩散》2025 等）、国防部发言人表态与例行记者会、军事法规/文献、国防支出预算与决算数字时。
- 怎么搜：国防部各栏目为**静态 HTML**，文章形态 `/{栏目}/{id}.html`；检索走 JSON API（见「细节」），中文词直接传参，返回高亮标题与 `manuscriptData.url`：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # 国防部站内检索（JSON）：title/content/author 三选一为检索字段
  curl -sS -A "$UA" -G 'http://mod-search.mod.gov.cn/api-surface/es/docSearchEasy' \
    --data-urlencode 'indexNames=manuscript' --data-urlencode 'highlightType=2' \
    --data-urlencode 'title=白皮书' --data-urlencode 'searchType=2' \
    --data-urlencode 'pageNumber=1' --data-urlencode 'pageSize=10' --data-urlencode 'channelId=718'
  # 白皮书正文直取（HTML）
  curl -sS -A "$UA" 'http://www.mod.gov.cn/gfbw/fgwx/bps/4846424.html'
  ```
  国防支出走财政部「栏目列表 → 详情 `/{YYYYMM}/t{YYYYMMDD}_{id}.htm`（HTML 表格）」静态结构；国新办站需浏览器。
- 覆盖：国防部白皮书栏目 2019–2025（本机列表 28 条，含国新办非涉军白皮书中转）；国新办白皮书历次（分年目录 `/zfbps/ndhf/`）；国防部法规/军事文献/发言人栏目长期滚动；财政部全国财政决算 2022–2025、中央财政预算 2024–2026。
- 门槛：国防部、财政部**免费、无登录**；国新办站有 JS 挑战（仅浏览器可过，见坑 1）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `mod.gov.cn/` → 200/71 070 B；`/gfbw/fgwx/bps/index.html` → 200/50 100（白皮书栏，最新《新时代的中国军控、裁军与防扩散》2025-11-27）；`/gfbw/fgwx/bps/4846424.html`（《新时代的中国国防》全文）→ 200；`/gfbw/fgwx/bps/index_1.html` → **404**（无分页）；`/gfbw/xwfyr/index.html` → 200/65 521 ✅
  - `GET http://mod-search.mod.gov.cn/api-surface/es/docSearchEasy?title=白皮书&…&channelId=718` → 200 `application/json`，`data.dataList` 命中「国防部新闻发言人…就日本政府2026版《防卫白皮书》答记者问」等 ✅
  - `scio.gov.cn/zfbps/` → HTTP **521**（响应体为 `jsl_clearance` JS 挑战）；`https://www.scio.gov.cn/` → curl 60（证书链含自签）；Chromium 中 HTTP `ERR_BLOCKED_BY_CLIENT`、HTTPS `ERR_CERT_AUTHORITY_INVALID` ❌（本机不可直连）
  - `yss.mof.gov.cn/2025zyjs/` → 200；`/2025zyjs/202609/t20260916_3997526.htm`（2025年全国一般公共预算支出决算表）→ 200，正文含「三、国防支出 18121.19 / 18106.23」✅；`/2026zyczys/` → 200（含 2026年中央本级支出预算表）；`mof.gov.cn/gkml/caizhengshuju/` → 200/18 600 ✅
- 上游：国防部网 `mod.gov.cn`；国防部检索 `mod-search.mod.gov.cn`；国务院新闻办 `scio.gov.cn`；财政部预算司 `yss.mof.gov.cn` 与财政部 `mof.gov.cn`。

## 细节

### 一、国防部网栏目（人读，2026-10-03 实测）

| 栏目 | URL | 说明 |
|---|---|---|
| 白皮书 | `/gfbw/fgwx/bps/index.html` | 国新办国防/涉军白皮书全文（2019 起，无分页） |
| 法律法规 | `/gfbw/fgwx/flfg/index.html` | 军事法律/法规 |
| 司法解释 | `/gfbw/fgwx/sfjs/index.html` | 涉军司法解释与答记者问 |
| 出版物 | `/gfbw/fgwx/cbw/index.html` | 军事出版物 |
| 法规文献·文件 | `/gfbw/fgwx/wj_213958/index.html` | 其他文件 |
| 军事文献 | `/gfbw/jswj/index.html` | 军事文献 |
| 权威发布 | `/gfbw/qwfb/index.html` | 官方发布 |
| 新闻发言人 | `/gfbw/xwfyr/index.html` | 发言人谈话、例行记者会 |

### 二、国防部站内检索 API

`http://mod-search.mod.gov.cn/api-surface/es/docSearchEasy`（**GET**，参数式）：

| 参数 | 值/含义 |
|---|---|
| `indexNames` | `manuscript`（稿件库；另有 `material` 素材库） |
| `highlightType` | `2`（高亮，命中词包 `<span style=color:red>`） |
| `title` / `content` / `author` | 三选一，检索字段；标题检索用 `title=` |
| `searchType` | `2`（模糊）等；与页面「检索方式」一致 |
| `pageNumber` / `pageSize` | 分页 |
| `channelId` | `718`（国防部网频道，写死即可） |

返回 `{"code":200,"data":{"total":N,"dataList":[{"manuscriptData":{"url","channel_name","classify_name"},"title","desc","issueTime"}]}}`。

### 三、国新办白皮书（目录规律，来自检索索引）

- 白皮书总栏 `http://www.scio.gov.cn/zfbps/`；**分年目录** `http://www.scio.gov.cn/zfbps/ndhf/{年}n/`，例：2019 年《新时代的中国国防》`http://www.scio.gov.cn/zfbps/ndhf/2019n/202207/t20220704_130617.html`。
- 白皮书检索页 `http://www.scio.gov.cn/search/bps/index.html`。
- 以上路径来自公开检索索引；**本机 curl 被 JS 挑战拦截**，未能直连验证（见坑 1）。

### 四、国防支出（财政部）

- 全国财政决算：`http://yss.mof.gov.cn/{年}zyjs/`；打开「××年全国一般公共预算支出决算表」`./{YYYYMM}/t{YYYYMMDD}_{id}.htm`，表格含「三、国防支出」行（决算数/上年数/完成率/同比）。
- 中央财政预算：`http://yss.mof.gov.cn/{年}zyczys/`；「××年中央一般公共预算支出预算表」「××年中央本级支出预算表」内含国防支出。
- 财政部财政数据栏 `https://www.mof.gov.cn/gkml/caizhengshuju/` 汇总决算/预算与月度收支。

## 坑

1. **国新办 `www.scio.gov.cn` 本机不可直连**：HTTP 返回 521 + `jsl_clearance` JS 挑战（需在浏览器执行 JS 取 cookie）；HTTPS 证书链含自签（curl 报 60），Chromium 亦分别被拦/证书无效。用浏览器访问可过；否则改走镜像（中国政府网/国防部网/各部委转载）找同一白皮书。
2. **国新办白皮书 ≠ 国防白皮书**：`/zfbps/` 收录国新办各类白皮书（人权、妇女、一带一路…），国防类只是其中一部分；找军事主题用检索或按分年目录筛。
3. **国防部检索 API 主机是 `mod-search.mod.gov.cn`**，不是 `www.mod.gov.cn`；用 GET 参数式，`channelId=718` 固定，缺 `channelId` 可能空结果。
4. **国防部白皮书栏无分页**（`index_1.html` 404），列表最早只到 2019 年（《新时代的中国国防》）；更早历次国防白皮书（1998–2015）须用检索 API、国新办分年目录或中国政府网找。
5. **国防支出不是独立文件**：它是「一般公共预算支出决算/预算表」里的一行，注意区分「全国」与「中央/中央本级」两张表的口径，以及**预算数 vs 决算数**。
6. 财政部表格是网页 `.htm`（非 PDF 附件），直接抓 HTML 表格；同页链接用的**相对路径**，拼接须按文章所在 `{YYYYMM}/` 目录。
