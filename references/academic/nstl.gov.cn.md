# nstl.gov.cn —— 外文科技文献检索与原文传递

科技部直属的**国家科技文献保障机构**（成员单位：中信所、中科院文献情报中心、机械信息院、农科院信息所、医科院信息所、中国标准院、冶金信息标准院等）。收录以**外文期刊/会议/学位论文/科技报告/标准/专利**为主，兼收少量中文科技文献；**检索与元数据匿名可直连 JSON API**，**全文靠注册后的「全文传递（原文申请单）」**。是做外文科技文献「先查后订」的首选入口，也是本层少数**无需登录就能批量取元数据**的源。

- 去哪找：`https://www.nstl.gov.cn/`；检索列表 API `POST https://www.nstl.gov.cn/api/service/nstl/web/execute?target=nstl4.search4&function=paper/pc/list/pl`；自助服务 `https://selfservice.nstl.gov.cn`；全文获取说明 `https://www.nstl.gov.cn/Portal/fw_qw.html`；全国开通数据库 `https://qwwx.nstl.gov.cn/`
- 什么时候用：要外文科技期刊/会议/学位论文/科技报告/标准/专利的检索与元数据；要"先查后订"的原文传递；要条目的 OA 开放获取标识
- 怎么搜：`POST` 表单，`query` 是 **JSON 字符串**（再被表单编码一次）；端点与 `query` 结构、完整 curl 模板见下「细节·检索接口」
- 覆盖：外文科技文献为主，兼收少量中文；资源类型码 `t` 见下「细节·资源类型码」
- 门槛：检索/元数据匿名 ✅；全文须免费注册后提交原文传递申请单（付费，资费未公开，高校/机构常有补贴）；机构用户走「全国开通服务」
- 实测：2026-10-03，macOS 27（arm64），curl 8.x（`-m 30`，桌面 Chrome UA，单主机 ≤3 请求/轮、间隔 ≥1.5 s），Python 3.9 stdlib，见下「细节·实测记录」
- 上游：`https://www.nstl.gov.cn/`（科技部直属国家科技文献保障机构）

## 细节

### 可用性矩阵

| 入口 | 状态 | 现象 |
|---|---|---|
| `https://www.nstl.gov.cn/` | ✅ | HTTP 200，117 KB，服务端渲染首页 |
| `GET /search.html?t=JournalPaper&q=<词>` | ⚠️ | 200（47 KB），但是 **JS 壳**，结果全由下方 XHR 填充；`q`/`t` 由页面内 `searchParamMap` 解析 |
| `POST /api/service/nstl/web/execute?target=nstl4.search4&function=paper/pc/list/pl` | ✅ | **200 JSON，匿名无验证码**（本机实测，检索主接口） |
| `POST …&function=paper/pc/list/fc` | （源码） | 分面计数（源码读出，未单独实测） |
| `POST /api/service/nstl/web/service-search4/_get/outer/details` | （源码） | 详情（`getArticleDetailByIdsUrl`，未单独实测） |
| `https://selfservice.nstl.gov.cn` | ✅→登录 | 用户自助服务（个人中心 / 申请单 / 收藏 / 期刊订阅）：**302 → `https://login.nstl.gov.cn/login?service=…`**（统一认证登录页，200 / 55 KB） |
| `https://qwwx.nstl.gov.cn/` | ✅ 可达 | **全国开通数据库**系统（机构登录/新机构注册），非个人入口 |
| 全文下载 | ❌→注册 | 检索到的条目带 `availableOrderType:"全文申请单"`，须注册后提交原文传递申请 |

### 检索接口（本机实测可用）

**端点**（两个都在 `https://www.nstl.gov.cn`，`Content-Type: application/x-www-form-urlencoded`，建议带 `X-Requested-With: XMLHttpRequest`）：

```
POST /api/service/nstl/web/execute?target=nstl4.search4&function=paper/pc/list/pl   # 列表
POST /api/service/nstl/web/execute?target=nstl4.search4&function=paper/pc/list/fc   # 分面（源码）
```

表单字段（<u>关键：`query` 是一个 JSON 字符串</u>）：

| 字段 | 值 |
|---|---|
| `query` | JSON 字符串，见下 |
| `webDisplayId` | `11`（论文列表 paperList） |
| `sl` | `0`（首页实测值，含义未验证） |
| `searchWordId` / `searchId` | 首页可留空 `''`（站点 JS 会做 `md5(...)` 签名，但**本机留空仍返回正常结果**） |
| `facetRelation` | `[]` |
| `pageSize` / `pageNumber` | 分页（实测 `pageSize=3..20`、`pageNumber=2` 均正常） |

**`query` 的结构**（从站点 `common.js` 的 `buildQueryParam()` 读出，本机按此构造成功）：

```json
{"c":10, "st":"", "f":[], "p":"",
 "q":[{"k":"","v":"基层治理","e":1,"o":"AND","a":0}],
 "op":"AND", "s":["nstl","haveAbsAuK:desc","yea:desc","score"],
 "t":["JournalPaper","DegreePaper"]}
```

- `q[]`：条件数组，每项 `{k: 字段码(空=全部字段), v: 词, e:1, o:"AND", a:0}`；`a=0` 为「包含」，`a=1` 为「匹配」（求精确时把词写成 `字段：值`）。
- `t[]`：**资源类型（可多值，实测 `["JournalPaper","DegreePaper"]` → total 6006）**。
- `s[]`：排序键数组；`c` ＝每页条数。
- 多处搜索词可直接用 `q:[{k:"",v:"词A"},{k:"",v:"词B"}]`，`op:"AND"`。

**最小复现（curl）**

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
curl -s -m 30 -A "$UA" -X POST \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -H 'X-Requested-With: XMLHttpRequest' -H 'Referer: https://www.nstl.gov.cn/search.html' \
  --data-urlencode 'query={"c":10,"st":"","f":[],"p":"","q":[{"k":"","v":"基层治理","e":1,"o":"AND","a":0}],"op":"AND","s":["nstl","haveAbsAuK:desc","yea:desc","score"],"t":["JournalPaper"]}' \
  --data-urlencode 'webDisplayId=11' --data-urlencode 'sl=0' \
  --data-urlencode 'searchWordId=' --data-urlencode 'searchId=' \
  --data-urlencode 'facetRelation=[]' --data-urlencode 'pageSize=10' --data-urlencode 'pageNumber=1' \
  'https://www.nstl.gov.cn/api/service/nstl/web/execute?target=nstl4.search4&function=paper/pc/list/pl'
```

返回：`{"code":"0","took":252,"total":4987,"data":[[…]],"traceId":"…"}`；`data` 是**行数组，每行 = 字段对象数组**（非字典），每项形如 `{"f":"tit","v":["<em>基层</em><em>治理</em>…"]}`。

### 结果行字段（实测 `rows[0]`，值为短码）

| 字段 | 含义 / 观测 |
|---|---|
| `id` | 记录号（32 位 hex，如 `8790ba6094e57b47de1877ad53b29379`） |
| `type` | 文献类型（`JournalPaper` …） |
| `tit` | 题名，**含 `<em>` 检索词高亮标签，须去标签** |
| `abs` | 摘要（字符串**数组**，被高亮切段；拼接后再去标签） |
| `key` | 关键词数组（同样带 `<em>`） |
| `hasAut` | 作者：数组，每项是 `[{f:id},{f:type},{f:nam,[名]}]` |
| `hasCrOr` | 机构/单位（结构同作者） |
| `hasHol` | 馆藏：`lico`＝馆藏机构代码（如 `CN111001` 中国科学技术信息研究所）、`honu`＝馆藏号 |
| `acty` | 访问标识：`nstl`＝NSTL 馆藏；`oa`＝**开放获取**（站点将其渲染为「OA 开放获取」角标） |
| `sysuty` | `j07`＝NSTL（站点 JS 的字段映射） |
| `availableOrderType` | 如 `全文申请单` —— **有值即表示可提交原文传递** |
| `yea` / `vol` / `iss` / `stpa` / `paco` | 年 / 卷 / 期 / 起始页 / 页数（均为数组） |
| `lan` | 语言：`[{zh:汉语}]` |
| `syid` / `score` / `sysfiin` | 系统号 / 相关度分 / 系统字段索引列表 |

### 资源类型码 `t`

| 码 | 含义 | 本机实测（`基层治理` 除非注明） |
|---|---|---|
| `JournalPaper` | 期刊论文 | ✅ total **4987** |
| `DegreePaper` | 学位论文 | ✅ total **965** |
| `ProceedingsPaper` | 会议论文 | ✅ total **11** |
| `BookMatrix` | 图书 | ✅ 有效（英文词 `governance` → 269；中文「基层治理」→ 0，说明**以科技外文图书为主**） |
| `ReportMatrix` | 科技报告 | ⚠️ 码有效但中文词 0 条（**未验证英文命中**） |
| `JournalMatrix` | — | ❌ total **0**（导航页用它，但**检索接口不吃这个码**，勿混用） |
| `Patent` / `StandardLiterature` / `Survey` / `CorpusCompileMatrix` | 专利 / 标准 / 综述 / 文集 | 上游页面声明，**未验证** |

导航页（`/resources_search.html?t=JournalMatrix` 等）用的是**另一套资源导航码**，与检索接口的 `t` 不通用。

### 全文获取（原文传递 / 全文传递）

- 官网「资源与服务 → **全文获取**」`https://www.nstl.gov.cn/Portal/fw_qw.html` 原文口径：
  > 「注册用户在 NSTL 网站上检索到的文献资源，可通过**全文传递**方式请求原文传递服务。」申请单在「提交成功」状态可自行取消；1 个月内未收到全文可联系热线免费重发，超期需重新申请。
- 流程图：`https://www.nstl.gov.cn/img/Portal/sy_qwfw3.png`；配套系统 `https://selfservice.nstl.gov.cn`（申请单/个人中心）、`https://qwwx.nstl.gov.cn/`（全国开通数据库·机构）。
- **门槛**：① 检索/元数据 → **匿名 ✅**；② 全文 → **须免费注册个人账号**后提交申请单，属**付费**原文传递（资费未在公开页列示，本机未验证；高校/机构常有 NSTL 补贴）；③ 机构用户走「全国开通服务」可直接看全文。
- 相关免费通道：`acty` 含 `oa` 的条目基本可从出版社/OA 站点自取，不必走付费传递。

### 其他可复用端点（源码读出，未逐个实测）

`serverURL_search = {origin}/api/service/nstl/web/execute?target=nstl4.search4&function=`，常见 function：
`paper/pc/list/pl`（列表）· `paper/pc/list/fc`（分面）· `paper/pc/docct`（自动补全）· `paper/pc/detail/sm/facet`（相似文献）· `paper/pc/details`（导出预览）· `export/preview`、`export/findIdList` · `charts/pc/hotWord`、`charts/pc/hotAuthor`、`charts/pc/hotOrganization`（热榜）。
另有 `baseUrl = {origin}/api/service/nstl/web/`（用户/购物车：`order/getDocOrder`、`cartAdd`…）与 `/api/service/nstl/web/service-search4/_get/outer/details`（详情）。

### 实测记录

2026-10-03，macOS 27（arm64），curl 8.x（`-m 30`，桌面 Chrome UA，单主机 ≤3 请求/轮、间隔 ≥1.5 s），Python 3.9 stdlib。

- `GET https://www.nstl.gov.cn/` → `HTTP 200 size=117028`，`<title>NSTL国家科技图书文献中心</title>`
- `POST …function=paper/pc/list/pl`（`q=基层治理`, `t=["JournalPaper"]`, `pageSize=10`, `pageNumber=1`）→ **200 / 29044 B / `application/json`**，`code=0`、`total=4987`、`took=252`、返回 10 行
- 同上 `pageNumber=2, pageSize=3` → 200，3 行（分页 ✅）；`t=["JournalPaper","DegreePaper"]` → `total=6006`
- `t` 取值实测：`JournalPaper` 4987 · `DegreePaper` 965 · `ProceedingsPaper` 11 · `BookMatrix`(governance) 269 · `ReportMatrix` 0 · `JournalMatrix` 0
- `GET /search.html?t=JournalPaper&q=基层治理` → 200 / 47358 B（HTML 壳，结果由 XHR 填充）
- `GET /Portal/fw_qw.html` → 200（全文获取说明 + 流程图 `/img/Portal/sy_qwfw3.png`）；`GET https://qwwx.nstl.gov.cn/` → 200（全国开通数据库登录页）；`GET https://selfservice.nstl.gov.cn/` → **302 → `https://login.nstl.gov.cn/login?service=…`** → 200（统一认证，需登录）

## 坑

- **`query` 是 JSON 字符串**（再被表单编码一次）；直接传 `q=基层治理` 这种朴素参数不会命中。
- **结果字段是短码 + 数组 + HTML 高亮**：`tit`/`abs`/`key` 都带 `<em>`；`data` 的每一行是 `[{f,v},…]` 而不是对象 → 必须先转成字典再解析。
- `JournalMatrix` ≠ `JournalPaper`：导航码与检索码不通用（实测前者 0 条）。
- 站点 JS 会给 `searchId` 做 `md5(searchWordId+_tk+时间戳+NCK cookie)` 签名，但**签名只影响检索历史/翻页态**；首屏检索不带也 200。
- 分页只认 `pageNumber`（1 起），`pageSize` 过大可能被服务端截断（未系统验证）。
- 收录偏**外文科技**：拿中文人文社科中文图书请改用 [`methods/literature-delivery.md`](../methods/literature-delivery.md) 的 CALIS / 国图 / NCPSSD 路径。
