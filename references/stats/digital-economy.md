# digital-economy —— 数字经济与电商统计

- 去哪找：国家数据局 `https://www.nda.gov.cn/sjj/index_pc.html`（数字中国/数据资源/数字经济频道）；全国电子商务公共服务网·数据中心 `https://dzswgf.mofcom.gov.cn/sjcx.html`；商务数据中心 `https://data.mofcom.gov.cn/`（社会消费品零售总额、服务贸易等，接口见 `../intl/china-trade-investment-stats.md`）；中国信通院 `https://www.caict.ac.cn/`（白皮书，curl 不可达，见「坑」）。
- 什么时候用：要《**数字中国发展报告**》《**全国数据资源调查报告**》原文与数字（数据生产总量、智能算力规模、数据交易/流通）；数字经济政策与试验区动态、全国数据资源统计调查制度；**全国电子商务交易额/网上零售额**时间序列；《中国电子商务报告》PDF。
- 怎么搜：分三路——
  - **国家数据局**：栏目列表 `/sjj/{频道}/list/index_pc_1.html`（翻页 `index_pc_N.html`）；正文 `/sjj/{频道}/{MMDD}/{23位数字串}_pc.html`（`YYYYMMDDHHMMSS`＋随机位）；报告 PDF 附件名为 `ff808081-…-{32位hex}.pdf`，**从正文页解析**。
  - **电商数据（JSON 接口）**：`dzswgf` 数据中心页是 echarts 壳，真数据走免 key 的 `/ecps/api/*`（页面 `<base href="/ecps/">`）；指标全名：`全国电子商务交易额`、`全国网上商品和服务零售额`、`全国网上零售额`。
    ```bash
    UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    # 时间轴（季度，返回 DATA_MONTH 列表）
    curl -s -A "$UA" 'https://dzswgf.mofcom.gov.cn/ecps/api/getSelectData'
    # 指标序列：POST JSON，indexName 用指标全名
    curl -s -A "$UA" -X POST -H 'Content-Type: application/json' \
      --data '{"indexName":"全国电子商务交易额"}' \
      'https://dzswgf.mofcom.gov.cn/ecps/api/getIndexData'
    # → {"code":200,"data":[{"dataMonth":"2017全年度","indication":"全国电子商务交易额","unit":"万亿元","curNum":"29.16","curYoy":"11.7","source":"国家统计局","sort":1}, …]}
    ```
  - **信通院**：`www.caict.ac.cn` 全站返回 **412**（WAF），curl 不可达，只能浏览器。
- 覆盖：国家数据局 2025–2026 政策/报告/动态（数字中国发展报告 2024·2025 年、全国数据资源调查报告 2024·2025 年、数据资源统计调查制度）；电商交易额序列 2017–2025 全年度（季度轴 2019Q2–2026Q2）；《中国电子商务报告》年度 PDF；信通院白皮书需浏览器。
- 门槛：无（NDA / `dzswgf` / `data.mofcom` 均免登录免 key）；信通院需浏览器会话。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA、`-L`、20s 超时），逐条见「细节」。
- 上游：国家数据局 `https://www.nda.gov.cn/`；全国电子商务公共服务网 `https://dzswgf.mofcom.gov.cn/`；商务部电子商务和信息化司 `http://dzsws.mofcom.gov.cn/`；中国信通院 `https://www.caict.ac.cn/`。

## 细节

### 国家数据局栏目与 URL 规律（2026-10-03 实测）

| 频道 | 路径前缀 | 内容 |
|---|---|---|
| 数字中国 | `/sjj/ywpd/sjzg/` | 《数字中国发展报告》发布页 |
| 数据资源 | `/sjj/ywpd/sjzy/` | 《全国数据资源调查报告》发布页 |
| 数字经济 | `/sjj/ywpd/szjj/` | 数字经济发展工作要点、座谈会 |
| 数字社会 / 政策规划 / 数字科技和基础设施 / 国际交流合作 | `/sjj/ywpd/{szsh,zcgh,szkjyjcss,gjjlhz}/` | 专题动态 |
| 通知公告 | `/sjj/zwgk/tzgg/` | 全国数据资源统计调查通知等 |
| 新闻发布 | `/sjj/swdt/xwfb/` | 与业务频道同稿重发（附件路径不同） |

已实测（均 `200`）：`/` 193 B JS 壳 → `/sjj/index_pc.html`（71,446 B）；`/sjj/ywpd/sjzy/list/index_pc_1.html`（11,113 B）。
- 数字中国发展报告（2025年）：正文 `/sjj/ywpd/sjzg/0608/20260608193210077440494_pc.html`（5,540 B）→ PDF `/sjj/ywpd/sjzg/0608/ff808081-9e81e847-019e-a7020a06-00a9.pdf`。
- 全国数据资源调查报告（2025年）：正文 `/sjj/ywpd/sjzy/0429/20260429164803571173880_pc.html`（10,419 B）→ PDF `/sjj/ywpd/sjzy/0429/ff808081-9b5e8626-019d-d86d1ac9-115b.pdf`。
- 《全国数据资源统计调查制度》PDF `/sjj/xxgk/gknr/qtzc/0305/ff808081-93de5a43-0195-6407db65-12ba.pdf`（上游声明，未本机实测）。

### 电商 JSON 接口（取自 `/ecps/static/js/visual/common.js`）

| 接口 | 方法 | 参数 | 用途 |
|---|---|---|---|
| `/ecps/api/getIndexData` | POST | JSON `{"indexName":"全国电子商务交易额"}` | 指标年度序列（✅ 实测） |
| `/ecps/api/getSubData` | POST | JSON（子指标/分时间） | 子类数据 |
| `/ecps/api/getSelectData` | GET | — | 季度时间轴（✅ 实测） |
| `/ecps/api/getSelectDataBySort` | GET | `beginSort`/`endSort` | 按 sort 取时间轴 |
| `/ecps/api/getLastDate`、`/ecps/api/getLastDateBySort` | GET | `beginSort`/`endSort` | 最新数据时间 |
| `/ecps/api/getLastDateByNewIndex` | GET | `indexName` | 新指标最新月度时间 |

数值口径见返回字段 `source`（电商交易额返回 `国家统计局`）。
《中国电子商务报告》PDF：研究报告页 `/news/5/{YYYY}/{MM}/{id}.html` → 附件 `https://dzswgf.mofcom.gov.cn/news_attachments/{md5}.pdf`（实测：`/news/5/2025/11/1762844725887.html` → `news_attachments/edaa82d0267dff264ea2269bf1260712ce54e3ae.pdf`，为 2024 年报告页）。

### 商务数据中心

`https://data.mofcom.gov.cn/`（`200`，14 KB）：`/zhtj/trs.shtml` 社会消费品零售总额、`/zhtj/cpi.shtml` 居民消费价格指数、`/fwmy/overtheyears.shtml` 服务贸易，另有国别统计大表；POST JSON 接口清单见 `../intl/china-trade-investment-stats.md`。商务部电商口径并入 `dzswgf` 与 `dzsws.mofcom.gov.cn`。

## 坑

1. `nda.gov.cn` 首页是 **JS 跳转壳**（仅 193 B，`window.location.href='/sjj/index_pc.html'`），别把壳当空页。
2. 国家数据局**无站内检索入口**（首页未见 search 表单）；找历史报告只能翻 `list/index_pc_N.html` 或用外部检索。
3. 报告附件名为 `ff808081-…`（UUID 变体）**不可拼接**；同一报告在业务频道与新闻发布频道的附件名不同。
4. 中国信通院 `www.caict.ac.cn`（http/https、根路径与 `/kxyj/qwfb/bps/` 均同）返回 **412**，需浏览器；白皮书常被第三方转载可作备胎。
5. `dzswgf` 页面 HTML **不含数值**（echarts 壳），必须打 `/ecps/api/*`；`indexName` 要精确匹配（如「全国电子商务交易额」），否则空数组。
6. 商务部口径电商交易额与统计局「网上零售额」**口径不同**，交叉引用时以接口 `source` 字段为准并注明。
7. `dzswgf` 服务器为 Tomcat，页面内相对资源要加 `<base href="/ecps/">` 前缀（`/static/…` 直取会 404）。
