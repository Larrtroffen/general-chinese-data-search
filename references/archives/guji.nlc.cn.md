# guji.nlc.cn —— 中华古籍书目检索平台

国家图书馆牵头、联动全国古籍收藏单位的古籍平台（原「中华古籍资源库」的升级版）。前端是 Vite/Vue SPA，**后端 `/api/**` 匿名 POST 可用**——检索、类型统计、省份分布、书目详情都能直接 curl 拿 JSON。（与 `nlc.cn.md` 的分工：那张卡讲国图门户与民国文献入口，本卡专讲古籍平台。）

- 去哪找：
  - 首页（SPA）：`https://guji.nlc.cn/`
  - 资源检索页（浏览器）：`https://guji.nlc.cn/resource/resourceList?keyword=<词>&select=%5B%221%22%2C%222%22%2C%223%22%2C%224%22%5D`
  - 资源详情页：`https://guji.nlc.cn/resource/resourceDetail?id=<metadataId>`
  - 原文阅读：`https://guji.nlc.cn/read/book?metadataId=<metadataId>`
  - **书目检索 API**：`POST https://guji.nlc.cn/api/resource/list`
  - 总量统计：`POST /api/anc/indexAncCountList`；省份/馆别分布：`POST /api/anc/searchMetadataCountStatistic`
  - 书目详情：`GET /api/anc/ancMetadataDetail/{metadataId}`
  - 其余端点（高级检索字段表、分类导航、收藏机构、丛书、viewer）见「细节」。
- 什么时候用：
  - 找**善本/普通古籍的书目题录**：书名、著者、版本（刻本/抄本/活字本）、出版年、装帧、册数、**收藏单位**；
  - 需要**按收藏省份/馆**盘家底（`searchMetadataCountStatistic` 直接给各省数字）；
  - 需要**古籍书影**做版本比对、影印底本核查；
  - 做「某部书有哪些版本、分别藏在哪家馆」这类**跨馆比对**。
- 怎么搜：
  ```bash
  R='-H Referer:https://guji.nlc.cn/'   # 必须带 Referer，否则 code 105 访问被拒绝

  # 1) 关键词检索（keyword="论语"）
  curl -sS -X POST 'https://guji.nlc.cn/api/resource/list' -H 'Content-Type: application/json' $R \
    -d '{"keyword":"论语","type":"1","typeList":["1","2","3","4"],
         "advancedRetrievalParams":[],"sort":"","order":"","page":1,"rows":10}'
  # → {"msg":"成功","code":200,"data":{"total":14,"rows":[{...}]}}

  # 2) 家底/分布
  curl -sS -X POST 'https://guji.nlc.cn/api/anc/indexAncCountList' -H 'Content-Type: application/json' $R -d '{}'
  curl -sS -X POST 'https://guji.nlc.cn/api/anc/searchMetadataCountStatistic' -H 'Content-Type: application/json' $R -d '{}'

  # 3) 取详情（metadataId 来自 1) 的 rows[].metadataId）
  curl -sS $R 'https://guji.nlc.cn/api/anc/ancMetadataDetail/1016321'
  ```
  **结果字段**（`data.rows[]`）：`metadataId`/`id`、`parallelTitle-title`（**书名，带 `<font color='red'>` 高亮，须剥标签**）、`parallelTitle-creators-creator`（著者）、`edition`（版本，如"刻本"）、`publisher-publishing-issuedGregorian-issuedGregorianCalendar`（出版年）、`physicalDescription-quantity`/`-binding`（册数/装帧）、`location-collectionUnit`（**收藏单位**，如"上海圖書館"）、`coverPath`、`ftpPath`。`data.total` 为命中数。
  **图像**：`ancMetadataDetail/{id}` 返回 `picArray[]`（`fileName`、`filePath`、`imageId`、`structureId`、`fileType:"PDF;TXT"`）；书影经 `/common/jpgViewer?filePathName=<filePath>`（HTML 阅读器）呈现——**直图 URL 未验证**（见「坑」）。
- 覆盖：
  - `indexAncCountList`（2026-10-03 实测）：`ancStructureCount` **166101**、`ancMetadataCount` **15609**、`ancCatalogCount` **3336013**（结构/书目/目录条数）。
  - `searchMetadataCountStatistic`：国图 **11806** 条居首，江苏 672、浙江 699、上海 167…
  - 粒度：书目（种）→ 卷/册/页（`picArray`）；含**收藏单位**字段，适合跨馆比对。
  - 与 `nlc.cn.md` 的「中华古籍资源库」为同一家机构的并行入口；旧库仍可从 `read.nlc.cn/thematDataSearch/toGujiIndex` 进。
- 门槛：
  - **检索/统计/书目详情接口：匿名可用**（无 cookie/token，POST 空 JSON 即通）。
  - **图像阅读与下载**：阅读器页可打开，但**高清图是否需登录未验证**——国图古籍库历史上多为公网免费看图、下载受限。**不要承诺可批量下载**。
- 实测：2026-10-03，macOS 27（arm64），curl 8.x，桌面 Chrome UA，`Referer: https://guji.nlc.cn/`。① `GET https://guji.nlc.cn/` → **200 / 5954 B**，`<title>中华古籍智慧化服务平台</title>`，Vite SPA。② `GET /index.Cpr0DIYL.js` → 200 / 166 KB；`baseURL:"/api"`；抓 30 个懒加载 chunk 后定位检索函数 `url:"/resource/list"`。③ `POST /api/resource/list`（keyword=论语, page=1, rows=3）→ **200**，`{"msg":"成功","code":200,"data":{"total":14,"rows":[{"location-collectionUnit":"上海圖書館","edition":"刻本","publisher-…":"1662","metadataId":1016321,…}]}}`。④ `POST /api/anc/indexAncCountList {}` → **200**，`{"ancStructureCount":166101,"ancMetadataCount":15609,"ancCatalogCount":3336013}`。⑤ `POST /api/anc/searchMetadataCountStatistic {}` → **200**，`[{"province":"国家图书馆","provinceNum":11806},…]`。⑥ `GET /api/anc/ancMetadataDetail/1016321` → **200 / 2213 B**，返回 `picArray`、`edition:"刻本"`、`description[]`（`frameSize:"23.9×15.1cm"`）。⑦ `GET /api/resource/getHighFieldList`（缺 `type` 参数）→ 200 但 `{"msg":"Required request parameter 'type' …"}` → 该接口**必须带 `type`**。⑧ `GET /common/jpgViewer?filePathName=<token>` → **200 text/html**（阅读器页，非直图）。⑨ 对照实验：同一条 `POST /api/resource/list` **不带 Referer** → 200 但 body `{"msg":"访问被拒绝！","code":105}`；**带 `Referer: https://guji.nlc.cn/`** → 200 `{"msg":"成功","code":200,…}`。→ Referer 是硬要求。
- 上游：https://guji.nlc.cn/

## 细节

### 端点表

| 用途 | 端点 / URL |
|---|---|
| 首页（SPA） | `https://guji.nlc.cn/` |
| 资源检索页（浏览器） | `https://guji.nlc.cn/resource/resourceList?keyword=<词>&select=%5B%221%22%2C%222%22%2C%223%22%2C%224%22%5D` |
| 高级检索页 | `https://guji.nlc.cn/resource/advancedSearch` |
| 资源详情页 | `https://guji.nlc.cn/resource/resourceDetail?id=<metadataId>` |
| 原文阅读 | `https://guji.nlc.cn/read/book?metadataId=<metadataId>` |
| **书目检索 API** | `POST https://guji.nlc.cn/api/resource/list` |
| 高级检索字段表 | `GET /api/resource/getHighFieldList?type=<1>` |
| 分类导航（聚类） | `POST /api/resource/getClassifyList`；`GET /api/resource/getMetadataNavigationList` |
| 收藏机构列表 | `POST /api/resource/getOrgNameList` |
| **总量统计** | `POST /api/anc/indexAncCountList` |
| **省份/馆别分布** | `POST /api/anc/searchMetadataCountStatistic` |
| 书目详情 | `GET /api/anc/ancMetadataDetail/{metadataId}` |
| 丛书/系列 | `GET /api/anc/ancSeriesDetail/{id}` |
| 图像 viewer | `/common/jpgViewer?filePathName=<token>`（HTML5 阅读器页） |
| 兼容旧入口 | `http://read.nlc.cn/thematDataSearch/toGujiIndex`（老「中华古籍资源库」） |

接口发现路径（改版可照做）：首页 5.9 KB 壳 → `index.Cpr0DIYL.js` 里 `baseURL:"/api"` + 一串 `url:"/anc/…"`；检索函数在入口 chunk：`jo=e=>ye.request({url:"/resource/list",method:"post",data:e})`。

### 请求参数（取自前端 `jl()`）

`keyword`（检索词）、`type`（资源类型，`1`/`2`/`3`/`4`，`10` = 中华古籍书目总目）、`typeList`（默认 `["1","2","3","4"]`）、`page`/`rows`（**前端把 page 上限压到 100**）、`sort`（`""` 或 `orderSeq`）、`order`（`""`/`asc`）、`advancedRetrievalParams`（数组，元素形如 `{"field":…,"keyword":…,"match":…,"relation":…}`，同一 field 多次出现会以 `;` 串联）、`nameIndex`（点击左侧人名索引时）、`seriesId`（丛书内检索）、`adCode`（地区）。

## 坑

1. ⚠️ **必须带 `Referer: https://guji.nlc.cn/`**：不带 → `HTTP 200` 但 body 是 `{"msg":"访问被拒绝！","code":105}`（实测；带 Referer 立即正常）。
2. 所有接口是 **POST + JSON body**，用 GET 一律 `{"msg":"Request method 'GET' is not supported","code":500}`（**HTTP 状态仍是 200，必须看 body 里的 `code`**）。
3. 命中字段名带连字符（`parallelTitle-title`、`publisher-publishing-issuedGregorian-issuedGregorianCalendar`），取值要按字面。
4. 高亮标签是 `<font color='red'>`（区别于 modernhistory 的 `<span style=…>`），入库统一清洗。
5. 前端把 `page` 截断到 100，翻页拿全量要走 `advancedRetrievalParams` 精炼或按 `adCode`/收藏单位切分。
6. 书影 viewer 是 HTML 壳，`filePathName` 是 token（不是明文路径），**直图端点未探到**——需要批量图时先做一次浏览器抓包。
