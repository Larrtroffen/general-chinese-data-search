# nfra.gov.cn —— 银行业保险业监管统计

- 去哪找：门户 `https://www.nfra.gov.cn/`（meta 跳 `https://www.nfra.gov.cn/cn/view/pages/index/index.html`）；统计信息栏目形如 `https://www.nfra.gov.cn/cn/view/pages/ItemList.html?itemPId={父ID}&itemId={栏目ID}&itemUrl=ItemListRightList.html&itemName=统计信息`。
- 什么时候用：要**银行业保险业官方统计**——总资产/总负债、不良贷款余额与不良率、商业银行分机构类型指标、保费收入与赔付、保险公司经营情况、银行业保险业统计季报/年报。
- 怎么搜：**纯前端 SPA（AngularJS）**，页面 HTML 只是壳，列表与正文由 `/cn/static/data/...` 接口渲染。已知接口（从 `/cn/js/common/ItemList.js` 提取）：
  - `/cn/static/data/DocInfo/SelectDocByItemIdAndChild?itemId={栏目ID}&pageNum=&pageSize=`（栏目文档列表）
  - `/cn/static/data/DocInfo/SelectByDocId`（文档正文）
  - `/cn/static/data/item/getItemNameById`、`/item/getLeftMenuItem`、`/item/getItemBread`（栏目树）
  - 附件下载：`/cbircweb/download/downloadDoc`、`/cbircweb/download/downloadPdf`
  结果形态：JSON（需带会话）；**本机匿名直连接口被 WAF 拦**，须真实浏览器。
- 覆盖：栏目覆盖原银保监会/金融监管总局的统计信息、监管指标、行政处罚、政策法规；年份以站内列表为准（1998 年保监会以来沿革）。
- 门槛：浏览免费；**接口需浏览器会话**（X-WEB 拦截匿名请求）。
- 实测：2026-10-03，桌面 UA curl——`GET https://www.nfra.gov.cn/` `200/237 B`（仅 meta refresh）；`GET /cn/view/pages/ItemList.html?itemPId=923&itemId=925&itemUrl=ItemListRightList.html&itemName=统计信息` `200/4,012 B`（AngularJS 空壳）；`GET /cn/static/data/DocInfo/SelectDocByItemIdAndChild?itemId=925&pageNum=1&pageSize=10`（带 Referer）→ `403`（`X-WEB` WAF）；`GET /cn/js/common/ItemList.js?v=20200108` `200/19,502 B`（接口路径来源）。
- 上游：`https://www.nfra.gov.cn/`（国家金融监督管理总局，原中国银保监会）。

## 细节

### 站点架构

- 首页是 meta refresh 壳 → 真正的门户在 `/cn/view/pages/index/index.html`。
- 栏目列表页统一模板 `ItemList.html?itemUrl=ItemListRightList.html&…`，由 `jQuery` 注入 `<tpl src>` 后 AngularJS 渲染数据。
- 数据源基址在 `/cn/js/common/Script.js` 中为 `/cn/static/data`。
- 机构沿革：`cbirc.gov.cn`（银保监会）→ `nfra.gov.cn`（金融监管总局，2023 起），老接口路径仍带 `cbircweb` 前缀。

## 坑

1. **匿名 curl 拿不到数据**：`/cn/static/data/*` 一律 `403`（`X-WEB`），加 Referer/UA 无效——须浏览器（或用 `../tools/agent-browser.md`）。
2. 首页 `200` 但只有 237 字节，是**跳转壳**，别当成"网站很小/挂了"。
3. 栏目 ID（`itemId`/`itemPId`）站点改版会变，**不要写死**；从 `ItemList.js` + 真实浏览器抓包确证当前值。
4. 监管统计的**权威发布口径**也常在「新闻发布」「统计数据」文章里（而非纯表格）；银行/保险的年度总量另有央行（`pbc.gov.cn.md`）与统计局口径（`../stats/`）可交叉。
5. 原保监会/银保监会历史数据在同域旧文章页，按标题+日期引用；注意机构改制导致的口径断裂。
