# cninfo.com.cn —— 上市公司公告与年报全文检索

- 去哪找：**公告检索** `https://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice`；**全文检索** `https://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=年报`；**个股公告页** `https://www.cninfo.com.cn/new/disclosure/stock?stockCode=000001&orgId=gssz0000001`。
- 什么时候用：要 A股/B股/北交所/港股 上市公司的**公告、年报、半年报、招股书、问询函、风险提示**；要按关键词**跨公司全文检索**公告；要按"公司 + 日期范围"批量下 PDF；要现行股票代码/orgId/简称对照表。
- 怎么搜：三个**免登录 JSON 接口**（`https://www.cninfo.com.cn`，桌面 UA + `X-Requested-With`/`Referer`）——
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 全市场代码表（含 orgId，是查公告的前置）
  curl -s -A "$UA" 'https://www.cninfo.com.cn/new/data/szse_stock.json'
  # ② 公告检索（按公司 / 日期 / 分类）
  curl -s -A "$UA" -X POST -H 'X-Requested-With: XMLHttpRequest' \
    -H 'Referer: https://www.cninfo.com.cn/new/disclosure/stock?stockCode=000001&orgId=gssz0000001' \
    --data 'pageNum=1' --data 'pageSize=30' --data 'column=szse' --data 'tabName=fulltext' \
    --data 'stock=000001,gssz0000001' --data-urlencode 'seDate=2024-01-01~2024-12-31' \
    --data-urlencode 'searchkey=年报' \
    'https://www.cninfo.com.cn/new/hisAnnouncement/query'
  # ③ 全文检索（跨公司，含港股；页码式）
  curl -s -A "$UA" 'https://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=年报&sdate=&edate=&isfulltext=false&sortName=nothing&sortType=desc&pageNum=1'
  ```
  返回均为 JSON；`announcements[].adjunctUrl` 即 PDF 相对路径，拼 `http://static.cninfo.com.cn/` 直下。
- 覆盖：沪深北 A/B 股 + 港股公告；`szse_stock.json` 实测 6,259 条（A股 6,179 / B股 79 / CDR 1）；全文检索「年报」命中 **494,168** 条（含港股）。
- 门槛：免费、免登录、无验证码（实测）；PDF 直下。
- 实测：2026-10-03，macOS arm64 curl 8.x（桌面 UA）——首页 `200/110 KB`（title 巨潮资讯网）；`hisAnnouncement/query`（2024-01 全市场）`200` `totalAnnouncement=35678`；`stock=000001,gssz0000001&searchkey=年报` `200` `total=117`；`fulltextSearch/full` `200` `totalAnnouncement=494168`、`totalpages=49416`；`szse_stock.json` `200/592 KB`；`hke_stock.json` `200/276 KB`；公告详情页 `302 → http://static.cninfo.com.cn/finalpage/2024-01-31/1219056613.PDF`（`200 application/pdf 269 KB`）。
- 上游：`https://www.cninfo.com.cn/`（巨潮资讯网，深交所指定信息披露平台）。

## 细节

### URL 规律（公告 → PDF）

| 用途 | URL 形态 |
|---|---|
| 公告检索页 | `https://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice` |
| 个股公告页 | `https://www.cninfo.com.cn/new/disclosure/stock?stockCode={code}&orgId={orgId}` |
| 公告详情（自动跳 PDF） | `https://www.cninfo.com.cn/new/disclosure/detail?stockCode={code}&announcementId={id}&orgId={orgId}&announcementTime={YYYY-MM-DD}` |
| PDF 直链 | `http://static.cninfo.com.cn/finalpage/{YYYY-MM-DD}/{announcementId}.PDF` |
| 全市场代码表 | `https://www.cninfo.com.cn/new/data/szse_stock.json` |
| 港股代码表 | `https://www.cninfo.com.cn/new/data/hke_stock.json` |

- `announcementId` 即 PDF 文件名主体；`{YYYY-MM-DD}` 取 JSON 里的 `announcementTime`（毫秒时间戳）换算。
- 实测详情页 `302` 直接 `Location:` 到 static PDF，无需再解析 HTML。

### `/new/hisAnnouncement/query` 参数（POST，form-urlencoded）

| 参数 | 说明 |
|---|---|
| `pageNum` / `pageSize` | 分页；实测 `pageSize=30` 正常 |
| `column` | 交易所/板块：`szse`（实测）；`sse` 等 |
| `tabName` | 检索模式：`fulltext`（实测） |
| `stock` | 形如 `{code},{orgId}` 限定单只股票；跨市场留空 |
| `seDate` | `YYYY-MM-DD~YYYY-MM-DD`，两端闭区间 |
| `searchkey` | 标题关键词（可空） |
| `isHLtitle=true` | 标题高亮（返回 `<em>`） |
| `plate` / `secid` / `category` / `trade` | 板块/证券/分类/交易状态过滤，可空 |

- **响应字段**：`totalAnnouncement`、`totalRecordNum`、`totalpages`、`hasMore`、`categoryList`、`announcements[]`。
- `announcements[]` 每条：`secCode` `secName` `orgId` `announcementId` `announcementTitle` `announcementTime`(ms) `adjunctUrl` `adjunctSize`(KB) `adjunctType` `columnId` `pageColumn`(如 `SZZB`/`SZCY`/`HKZB`) `announcementType`。

### `/new/fulltextSearch/full` 参数（GET）

`searchkey` `sdate` `edate` `isfulltext`(true=正文检索) `sortName`(nothing) `sortType`(desc) `pageNum`。默认每页 10 条。返回结构与 `hisAnnouncement` 同构。

### 代码表字段

`{code, pinyin, category, orgId, zwjc}`。实测覆盖：沪 `600/601/603/605/688`、深 `000/001/002/003/300/301`、北 `430/83x/87x/920`、B 股、CDR——**一个文件拿全 A/B 股 + 北交所代码与 orgId**。

## 坑

1. 标题字段带 `<em>` 高亮标签（`isHLtitle=true` 时），入库前需去标签。
2. 全文检索结果**混入港股**（`pageColumn=HKZB`，`secName` 如「中华银科技」），按需用 `column`/`pageColumn` 过滤。
3. `announcementTime` 是**毫秒时间戳**，且大量记录落在当日 `23:59:xx`——按日聚合时注意。
4. `sse_stock.json` / `shse_stock.json` 实测 **404**，沪深北代码统一走 `szse_stock.json`；`topSearch/query`、`topSearch/detailOfQuery` 实测 **500**，不要用。
5. `pageSize` 上限未验证；大批量抓取建议按 `seDate` 分月切片 + ≥1.5s 间隔。
6. PDF 走 `static.cninfo.com.cn`（http 亦可），与主站同源不同主机。


