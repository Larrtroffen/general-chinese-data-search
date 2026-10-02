# ndl-japan —— 日本国立国会图书馆检索与数字馆藏

- 去哪找：
  - 书目/跨库检索：`https://ndlsearch.ndl.go.jp/`（NDL Search，聚合全国图书馆 + 数字馆藏）
  - 数字馆藏本体：`https://dl.ndl.go.jp/`（国立国会図書館デジタルコレクション）
- 什么时候用：找**日文近代中国相关资料**——战前日本出版的中国调查/满蒙文献、官报、帝国议会资料、古典籍、地图、博士论文的书目与（部分）全文图像；也可当「日文书的联合目录」用（NDL Search 聚合日本全国馆藏）。
- 怎么搜：两条路，**优先 API**：
  1. NDL Search OpenSearch（XML，含 `openSearch:totalResults`）：
     `https://ndlsearch.ndl.go.jp/api/opensearch?any=<词>&cnt=20&idx=1`
  2. 数字馆藏检索结果页（HTML/SPA，附 JSON 端点）：
     `https://dl.ndl.go.jp/search/searchResult?title=<词>&fullText=true&pageNum=0&pageSize=20&sortKey=SCORE&displayMode=list`
- 覆盖：NDL Search 聚合日本全国图书馆书目 + NDL 数字馆藏；数字馆藏含图书/杂志/报纸/古典籍/博士论文/官报/帝国议会/地図/歴史的音源等 20+ 集合；「満州」在 NDL Search 命中 **131,344** 条。
- 门槛：免费；NDL Search API 免登录。数字馆藏按资料的「閲覧方法」分三档：`internet` 免登录看、`ooc`（送信サービス，需图书馆）、`inlibrary` 仅馆内——**只有 `internet` 档能匿名取图像**。
- 实测：2026-10-03（浏览器内，见 `## 细节`）：`api/opensearch?any=満州&cnt=2` → `totalResults 131344`；`?title=満州` → 62,826；`?creator=東京` → 642,149；`+from=1900&until=1910` → 2,153；`idx=3` → `startIndex 3`；SRU `operation=searchRetrieve&query=title="満州"` → `numberOfRecords 62826`。`dl.ndl.go.jp/api/iiif/13706464/manifest.json` → ✅ 200 JSON。
- 上游：<https://ndlsearch.ndl.go.jp/>、<https://dl.ndl.go.jp/>

## 细节

> 探测纪律（本机实测 2026-10-03）：桌面 Chrome UA / 20s 超时。**本机 `curl` 解析 `ndlsearch.ndl.go.jp` 得到污染 IP → 超时（HTTP 000）；改用无头 Chromium 访问同一 URL 全部正常**——下列 NDL Search 数据均来自浏览器内实测。

### 1. NDL Search API

**OpenSearch（RSS 2.0 + `dcndl` 命名空间）**

| 参数 | 含义 | 实测 |
|---|---|---|
| `any` | 全字段 | `満州` → 131,344 |
| `title` | 题名 | `満州` → 62,826 |
| `creator` | 著者 | `東京` → 642,149 |
| `from` / `until` | 出版年区间 | `1900`–`1910` → 2,153 |
| `idx` | 起始序号（1 起） | `idx=3` → `startIndex 3` |
| `cnt` | 条数 | `2` / `20` |

- 固定入口：`https://ndlsearch.ndl.go.jp/api/opensearch?<参数>`；响应 `<link>` 指向真实后端 `ios-v2-prod-eks-alb.ndlsearch.ndl.go.jp`。
- 单条含 `<title>`、`<link>`（形如 `https://ndlsearch.ndl.go.jp/books/R100000136-I1970023484898351360`）、`<description>`（CDATA 内嵌书目字段）、`dcndl:` 属性。

**SRU（CQL 查询语法）**

`https://ndlsearch.ndl.go.jp/api/sru?operation=searchRetrieve&query=title%3D%22満州%22&maximumRecords=2` → ✅ 200，`numberOfRecords 62826`（`query` 用 `字段="值"` 且需 URL 编码，支持 `and`/`or`）。

### 2. 数字馆藏（dl.ndl.go.jp）

检索结果 URL 模板（无头浏览器点「検索」后落点，可用）：

```
https://dl.ndl.go.jp/search/searchResult?title=<词>&fullText=true&pageNum=0&pageSize=20&sortKey=SCORE&displayMode=list
```

可叠加 `collection=`（多选）与 `accessRestrictions=`（多选）。集合代码（页面复选框 id `query-category-code-<code>`，实测读取）：

| code | 集合 | code | 集合 |
|---|---|---|---|
| `A00001` | 図書 | `A00016` | 日本占領関係資料 |
| `A00002` | 雑誌 | `A00017` | 憲政資料 |
| `A00022` | 新聞 | `A00019` | プランゲ文庫 |
| `A00003` | 古典籍資料（貴重書等） | `A00121` | 録音・映像関係資料 |
| `A00014` | 博士論文 | `A00024` | 歴史的音源 |
| `A00015` | 官報 | `A00152` | 地図 |
| `A00188` | 帝国議会資料 | `A00173` | 日系移民関係資料 |
| `A00150` | 特殊デジタルコレクション | `B00000` | 電子書籍・電子雑誌 |

（未入表的还有：`A00122`＝他機関デジタル化資料，`A00162`＝パッケージ系電子出版物）

**端点表**（均 `https://dl.ndl.go.jp`）

| 用途 | 端点 | 实测 |
|---|---|---|
| 资料页 | `/pid/<pid>`（pid 是纯数字，如 `14704311`） | ✅ 200（SPA，`<title>` 固定为「国立国会図書館デジタルコレクション」） |
| 书目 JSON | `/api/item/search/info:ndljp/pid/<pid>` | ✅ 200 JSON |
| IIIF Manifest | `/api/iiif/<pid>/manifest.json` | ✅ 200（`internet` 档）；`inlibrary` 档 → 404 + `{"itemId":"…","checkResult":"NG"}` |
| 全文/画像检索 | `POST /api/item/search` | ⚠️ GET → 405、非预期 JSON body → 400（body schema 未探明） |
| 分面计数 | `/api/item/searchCollectionAggregations?keyword=<词>` | ✅ 200（**注意：返回全库 7,097,546 计数，未按词过滤，别当检索用**） |
| 权限判定 | `/api/check/allowedContents/<tier>/<view\|print\|download\|simview>` | ✅ 200 |
| 阅览令牌 | `/api/restriction/issue/token/info:ndljp/pid/<pid>` | ✅ 200 |
| 目次分面 | `/api/meta/search/toc/facet/<pid>` | ✅ 200 |
| 集合/地理/元数据 | `/api/collection/all`、`/api/geography`、`/api/master/metadata` | ✅ 200 |

- pid 与 DOI 对应：`info:ndljp/pid/13427891` ↔ `10.11501/13427891`。
- 缩略图相对路径形如 `contents/<pid>/thumb.jpg`；资料页有「一括ダウンロード」（整册 PDF/图像打包）。

## 坑

1. **本机 DNS**：`ndlsearch.ndl.go.jp` 在本机被解析到一串无关 IP（157.240.2.50 / 31.13.76.99 / 199.16.156.103 …），`curl` 一律超时；`iss.ndl.go.jp` 302 跳回该域后同样超时。**本机走浏览器；脚本化时先 `dig` 自检解析结果**。`dl.ndl.go.jp`（CloudFront）解析正常，`curl` 可用。
2. `dl.ndl.go.jp` 是 Vue SPA：**必须带完整参数**（`fullText`、`pageSize`、`sortKey`、`displayMode`）直接开 `searchResult` 才出结果；`/search?keyword=` 只是表单页，不会自动检索。
3. `/api/item/search` 只收 POST 且 body 结构未知，不要按 REST 直觉拼 GET。
4. 全文图像受「閲覧方法」限制：`inlibrary`（馆内限定）与 `ooc`（图书馆送信）**拿不到匿名图像**，只有 `internet` 档的 IIIF manifest 可用——检索时用 `accessRestrictions=internet` 先筛。
5. 界面日文；英文版可切（`dl.ndl.go.jp` 右上 English、NDL Search 亦有英文），但 API 字段名不变。
