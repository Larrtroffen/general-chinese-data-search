# china-trade-investment-stats —— 对外经贸官方统计

- 去哪找：**商务部·商务数据中心** `https://data.mofcom.gov.cn/`（有 POST JSON 接口，见「细节」）；商务部主站统计栏目 `https://www.mofcom.gov.cn/tj/sjtj/index.html`；海外综合服务平台 `https://fec.mofcom.gov.cn/`、中国投资指南网 `https://fdi.mofcom.gov.cn/`；**国家国际发展合作署** `http://www.cidca.gov.cn/`（对外援助政策/信息）。
- 什么时候用：要**商务部口径**的月度/年度对外经贸数字——非金融类对外直接投资、对外承包工程与劳务合作、货物进出口（按国别/贸易方式/企业性质）、实际使用外资、社会消费品零售总额；做对外投资/外贸简报、要免 key 的 JSON。
- 怎么搜：数据中心各页面本身是静态壳，真数据走**免 key 的 POST 接口**（`/datamofcom/front/…`，返回 JSON/JSON 数组）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # 非金融类对外直接投资：月度累计金额(亿美元)/企业家数/国家数/同比
  curl -s -A "$UA" -X POST -H 'Content-Type: application/x-www-form-urlencoded' \
    --data 'start_date=&end_date=' 'https://data.mofcom.gov.cn/datamofcom/front/tzhz/fordirinvest/dateQuery'
  # 对外承包工程：新签合同额/完成营业额(亿美元)+同比
  curl -s -A "$UA" -X POST --data '' 'https://data.mofcom.gov.cn/datamofcom/front/tzhz/forEngineerStac/dateQuery'
  # 进出口分国别（当月/累计，需给 date=YYYYMM）
  curl -s -A "$UA" -X POST --data 'date=202608' 'https://data.mofcom.gov.cn/datamofcom/front/totalbycountry/query'
  # 国别统计大表：逐国 GDP/CPI/进出口/广义货币等
  curl -s -A "$UA" -X POST --data '' 'https://data.mofcom.gov.cn/datamofcom/front/gbtj/allTable'
  ```
  结果形态：**JSON**（对象或 `[表格, 图表, 配置]` 三元数组）；`http://` 会 **301** 到 `https://`，POST 必须直接打 https。CIDCA 站点仅 **http:// 可用**（见「坑」）。
- 覆盖：商务部口径，月度（进出口/对外投资/承包工程）+ 年度公报/年鉴；分国别、分贸易方式、分企业性质、分省市（部分）；另含各国宏观大表。CIDCA 覆盖对外援助政策法规、项目咨询单位名录、预决算，**不发布项目级援助数据**。
- 门槛：**免费、无 key、无登录**；数据中心接口匿名可用。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA、20s）——`data.mofcom.gov.cn/` `200`；`POST …/tzhz/fordirinvest/dateQuery` `200` JSON，`202608` → 国家/地区 148、企业 8424 家、金额 866.8 亿美元、同比 −10.6%；`POST …/tzhz/forEngineerStac/dateQuery` `200`（202608 新签 1713.4/完成 1156.1 亿美元）；`POST …/totalbycountry/query` `200`（`rows[]` 含印度 `total_lj_value=1250.44`、`export_lj_value=1078.1`，`pageSize=10`、`maxPageNum` 分页）；`POST …/gbtj/allTable` `200`（阿根廷 GDP/CPI/进出口等字段）。CIDCA：`https://www.cidca.gov.cn/` **证书不匹配**（返回 `CN=www.baishan.com`）失败，`http://www.cidca.gov.cn/` `200`。❌ `hzs.mofcom.gov.cn`（对外投资合作司，公报原始发布页）连接超时。
- 上游：商务部 `https://www.mofcom.gov.cn/`；商务数据中心 `https://data.mofcom.gov.cn/`；国家国际发展合作署 `http://www.cidca.gov.cn/`。

## 细节

### 商务数据中心接口表（均 POST，`https://data.mofcom.gov.cn` 前缀）

接口路径 2026-10-03 取自各栏目页内 `js/<栏目>.js`；「实测」列 ✅ = 本机实际调用返回数据，— = 仅从 JS 读到未单独调用。

| 栏目页 | 接口 | 表单参数 | 返回 | 实测 |
|---|---|---|---|---|
| `/tzhz/fordirinvest.shtml` 非金融类对外直接投资 | `/datamofcom/front/tzhz/fordirinvest/dateQuery` | `start_date`/`end_date` | 数组，行含 `time,num_enterprice,non_financial,yoy,country` | ✅ |
| `/tzhz/forengineerstac.shtml` 对外承包工程 | `/datamofcom/front/tzhz/forEngineerStac/dateQuery` | `start_date`/`end_date` | `newly_signed_contracts,turnover,*_yoy,project_time` | ✅ |
| `/tzhz/forlaborcoop.shtml` 对外劳务合作 | 页内 JS 为空壳 | — | 未抓到端点（实测 JS 仅 221 B） | — |
| `/hwmy/imexmonth.shtml` 货物进出口月度 | `/datamofcom/front/totalmonth/query` | `startDate`/`endDate` | 图表用数组 | — |
| `/hwmy/imexCountry.shtml` 分国别（地区） | `/datamofcom/front/totalbycountry/query` | `date=YYYYMM` | `{rows[],maxPageNum,pageNumber,pageSize}` | ✅ |
| `/hwmy/imexTradeMethod.shtml` 按贸易方式 | `/datamofcom/front/totaltrademethod/query` | 同月/日期 | 饼图用数组 | — |
| `/hwmy/imexComType.shtml` 按企业性质 | `/datamofcom/front/totalcomtype/query` | 同上 | 饼图用数组 | — |
| `/lywz/inmr.shtml` 实际使用外资 | `/datamofcom/front/lywz/direct/query` | 日期 | 图表用数组 | — |
| `/zhtj/gdp.shtml` 综合统计 | `/datamofcom/front/zhtj/gdp/query`、`/zhtj/gdp/dateQuery` | `type=1`（+日期） | 图表用数组 | — |
| `/gbtj/table.shtml` 国别统计 | `/datamofcom/front/gbtj/allTable` | 分页 | 逐国宏观大表 | ✅ |
| `/gnmy/shrzgm.shtml` 社会消费品零售总额 | `/datamofcom/front/gnmy/shrzgmQuery`、`shrzgmDateQuery` | 日期 | 图表用数组 | — |
| `/fwmy/overtheyears.shtml` 服务进出口 | 页内 JS 为空壳 | — | 未抓到端点 | — |

- 每个栏目页会加载同目录 `js/<栏目>.js`，`$.ajax({url:…, data:…})` 里就是真接口与参数——站点改版时按此法重新定位。
- 商务部**年度公报**：《中国对外直接投资统计公报》（商务部 + 国家统计局 + 国家外汇管理局联合发布）、《中国对外投资合作发展报告》；原发布页在合作司 `hzs.mofcom.gov.cn`（本机超时），可经主站 `www.mofcom.gov.cn`、`fec.mofcom.gov.cn` 或地方商务厅/一带一路网转载文取。
- **口径交叉引用**：双边×分商品贸易走 [`comtrade.un.org.md`](comtrade.un.org.md)；国际收支/直接投资存量流量（BOP/IIP 口径）走 [`imf.org.md`](imf.org.md) 与外汇局（`www.safe.gov.cn`，实测 200）；跨国宏观面板走 [`worldbank.org.md`](worldbank.org.md)；部委统计总表（含海关总署 412）走 [`../stats/ministry-stats.md`](../stats/ministry-stats.md)。
- **UNCTAD**：UNCTADstat 门户 `https://unctadstat.unctad.org/`（`/datacentre/?folders=31` 实测 200）提供 FDI/贸易/海运长期序列；`unctad.org` 主站本机 **403 Cloudflare**，`unctadstat-api.unctad.org` 主机存在但 `/api/datasets`、`/swagger/…` 等路径实测 **404**（API 路径未跑通，上游文档被 Cloudflare 挡）。

## 坑

1. **口径别混**：货物贸易有**海关总署**（报关口径）与**商务部**（国际收支/外贸业务口径）两套；对外直接投资有**商务部（非金融类）**、**外汇局（BOP/IIP）**两套；实际使用外资有商务部与央行/外汇局 BOP 口径——同一指标数字可能不同，引用必须写明发布机构与口径。
2. **CIDCA 只走 http**：`https://www.cidca.gov.cn/` 返回的是 `www.baishan.com` 证书（TLS 校验失败），必须用 `http://`；站点以政策/信息发布为主，**没有项目级援助数据**，对外援助金额请回 AidData / BU GDP（见 [`china-overseas-finance.md`](china-overseas-finance.md)）或国新办白皮书。
3. **`hzs.mofcom.gov.cn` 本机超时**：合作司（公报、专项统计原始页）不可达，公报数字改走主站/转载；这也是"为什么用 data.mofcom 接口"的原因。
4. 数据中心前端是 2013 年前后的 jQuery，字段名中英混排（`non_financial`=亿美元、`*_lj_value`=累计、`*_per`=同比%），**`null` 表示该月未发布**，别当 0。
5. 接口**未公布频控**，请自设 ≥1.5 s 间隔、桌面 UA；`http` 一律先 301 再打 `https`，省得 POST 体丢失。
6. UNCTAD 的官方统计门户在本机**可读入口、难取数**：`unctadstat.unctad.org` 200 但 API 路径未探到，`unctad.org` 403；要 UNCTAD 数字可经 DBnomics（`dbnomics.world.md`）或 World Bank 转引。
