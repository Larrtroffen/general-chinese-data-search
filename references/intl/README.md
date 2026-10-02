# intl/ —— 国际组织与跨国数据

本层放**中国以外、以国家为观测单位或跨国可比**的数据源：国际组织统计库、跨国调查、政治学指标、以及能把它们一次搜到的聚合接口。另收**中国对外**方向的源——中国海外发展融资（项目级）、一带一路官方与第三方数据、商务部对外经贸官方统计——便于与跨国库对照；以及跨机构与专题卡片：**多边开发银行项目库**（`ifis-projects.md`）、**国际组织报告全文库**（`io-report-libraries.md`）、**中国留学生**（`china-students-abroad.md`）与**华侨华人/移民**（`chinese-diaspora.md`）。查中国国内口径请回 `../stats/`、`../surveys/`。

## 文件一览

| 文件 | 来源 | 用途/何时用 | 状态 |
|---|---|---|---|
| `worldbank.org.md` | 世界银行开放数据 | 跨国宏观面板起步（GDP/人口/贸易/贫困/治理），免 key JSON API | ✅ 本机实测 |
| `dbnomics.world.md` | DBnomics | 一个接口跨库搜/取（WB、IMF、OECD、Eurostat…），"这指标哪个库有" | ✅ 本机实测 |
| `comtrade.un.org.md` | 联合国商品贸易统计 | 双边×分商品进出口（HS），免 key 预览 + 需 key 正式接口 | ⚠️ 部分需 key |
| `data.un.org.md` | 联合国数据门户 | UNdata 整合库；现代站无 JSON API，仅遗留 SDMX 可用 | ⚠️ 仅遗留接口 |
| `unstats.un.org.md` | 联合国 SDG 指标库 | SDG 官方口径指标 + 目标/具体目标元数据，免 key JSON | ✅ 本机实测 |
| `imf.org.md` | 国际货币基金组织 | BOP/CPI/财政/储备等 SDMX 库；老接口已下线 | ⚠️ 部分被封 |
| `oecd.org.md` | 经合组织统计 | 发达国家可比社会/经济指标，SDMX REST | ✅ 本机实测 |
| `eurostat.md` | 欧盟统计局 | 欧盟/EFTA 国别与 NUTS 区域数据，JSON/TSV | ✅ 本机实测 |
| `uis.unesco.org.md` | 教科文统计研究所 | 教育/科学 R&D/文化指标；批量需 token | ⚠️ 批量需 token |
| `who.int.md` | 世界卫生组织 | WHO 数据产品总览（GHO/WHS/IRIS）；取数详见 `../health/who-gho.md` | ✅ 本机实测 |
| `ilostat.ilo.org.md` | 国际劳工组织 | 就业/失业/工资/工时，免 key JSON | ✅ 本机实测 |
| `fao.org.md` | 联合国粮农组织 | 农业/粮食/土地/林业/渔业，bulk 免费、API 需 token | ⚠️ API 需 token |
| `ourworldindata.org.md` | Our World in Data | 现成整编长序列与图表 CSV，直接喂 pandas | ⚠️ 慢/易超时 |
| `v-dem.net.md` | V-Dem 民主多样性 | 1789 至今民主/治理指数，表单门控下载、无 REST | ⚠️ 表单门控 |
| `systemicpeace.org.md` | Polity5 / INSCR | `polity2` 等经典政体分值（覆盖到 2018） | ⚠️ 未下文件 |
| `freedomhouse.org.md` | 自由之家 | FIW/FOTN 评级；**本机不可达**，给了 QoG/OWID 替代路径 | ❌ 本机不可达 |
| `qogdata.pol.gu.se.md` | QoG 标准数据集 | 一张 61 MB 表含上千个治理/政治变量（FH/V-Dem/WGI/CPI…） | ✅ 本机实测 |
| `worldvaluessurvey.org.md` | 世界价值观调查 WVS/EVS | 公众价值观与态度跨波比较（WV1–WV7、EVS） | ⚠️ 需浏览器 |
| `issp.org.md` | 国际社会调查项目 ISSP | 主题轮换的跨国态度调查；实体数据在 GESIS | ⚠️ 下载站被挡 |
| `europeansocialsurvey.org.md` | 欧洲社会调查 ESS | 严格概率抽样的欧洲跨国态度数据；数据门户为 SPA | ⚠️ 需注册 |
| `asianbarometer.org.md` | 亚洲晴雨表 | 东亚/东南亚/南亚政治态度（老站，JS 注入） | ⚠️ 需浏览器 |
| `afrobarometer.org.md` | 非洲晴雨表 | 非洲 35+ 国政治态度与治理评价 | ⚠️ 需注册 |
| `cses.org.md` | 选举制度比较研究 | 选举层面的个体投票行为 + 选区/制度变量 | ⚠️ 需注册 |
| `china-overseas-finance.md` | BU GDP Center / AidData / CARI | 中国海外贷款·援助·投资项目级明细（金额/部门/坐标）；xlsx·CSV·GeoPackage 直链 | ⚠️ 部分源不通 |
| `bri-data.md` | 中国一带一路网 / CSIS / Lowy | 一带一路官方数据频道与第三方项目库（Reconnecting Asia、太平洋援助地图） | ⚠️ 第三方不通 |
| `china-trade-investment-stats.md` | 商务部商务数据中心 / CIDCA | 对外投资·承包工程·进出口·外资月度 JSON 接口与年度公报；对外援助政策 | ✅ 接口实测 |
| `china-students-abroad.md` | IIE Open Doors / IRCC / HESA / ABS / 教育部 | 中国留学生与他国国际学生统计（按国籍·学历·院校）；IRCC CSV 直链、美国仅浏览器 | ⚠️ 部分被挡 |
| `chinese-diaspora.md` | US Census ACS / StatCan / UN DESA / 侨研机构 | 各国华人人口与移民存量（血统·出生地·族裔多口径）；Census 需 key、StatCan/UN 直取 | ⚠️ 部分需 key |
| `ifis-projects.md` | 世行 / 亚投行 / IDB / ADB / AfDB / EBRD / EIB | 多边开发银行项目级明细（项目号·借款国·金额·状态）；世行与亚投行免 key | ⚠️ 部分被挡 |
| `io-report-libraries.md` | 世行 OKR / UN DL / IMF eLibrary / OECD iLibrary | 国际组织报告全文 PDF 与题录；OKR/UN DL 免 key | ⚠️ 部分订阅 |
| `wiood-eora.md` | WIOD / Eora / EXIOBASE / ADB MRIO / OECD TiVA | 全球投入产出与价值链数据（MRIO）入口、版本与门槛 | ⚠️ 部分需登录 |
| `unctad-wto-trade.md` | UNCTADstat / WTO Stats | 贸易与价值链分析数据；UNCTAD OData 可用、WTO 批量 zip、API 需 key | ⚠️ 部分需 key |

## 选路

- **只知道指标名，不知道哪个库有** → 先 `dbnomics.world.md` 跨库搜（provider/dataset/series 三元组），再去原库取正式版本。
- **要标准跨国宏观时间序列**（GDP/人口/贸易/通胀/财政） → `worldbank.org.md` 起步；要 IMF/OECD/Eurostat 专库再分别走 `imf.org.md`、`oecd.org.md`、`eurostat.md`。
- **要"双边×分商品"贸易** → `comtrade.un.org.md`（preview 免 key，全量需订阅 key）。
- **要 SDG / 卫生 / 教育 / 劳工 / 农业的专项口径** → `unstats.un.org.md` / `who.int.md`（取数见 `../health/who-gho.md`）/ `uis.unesco.org.md` / `ilostat.ilo.org.md` / `fao.org.md`。
- **要政治制度、治理质量、民主/威权变量** → `v-dem.net.md`（长时段首选）+ `qogdata.pol.gu.se.md`（变量超市，含 Freedom House 派生列）+ `systemicpeace.org.md`（Polity5，止于 2018）；`freedomhouse.org.md` 本机不可达，走其中列出的转引路径。
- **要公众态度/投票行为的微观数据** → 全球价值观 `worldvaluessurvey.org.md`；欧洲 `europeansocialsurvey.org.md`；主题制 `issp.org.md`；区域制 `asianbarometer.org.md`、`afrobarometer.org.md`；选举制 `cses.org.md`。
- **只想快速画一张跨国趋势图** → `ourworldindata.org.md` 的 `/grapher/{slug}.csv`（注意回溯其 Source）。
- **要中国对外贷款/援助/投资的项目级明细（金额、部门、坐标）** → `china-overseas-finance.md`：BU GDP Center（CODF、中非贷款 CLA）与 CARI 有直链 xlsx/CSV，AidData 的 GeoGCDF 走 GitHub Releases（`aiddata.org` 本机不通）。
- **要一带一路官方数据频道，或第三方基建/援助项目库** → `bri-data.md`：官网 `dataChart` 及各专题页可 curl；CSIS Reconnecting Asia、Lowy Pacific Aid Map 本机超时，需浏览器（后者有 SPC 镜像 `sdd.spc.int`）。
- **要商务部口径的月度对外投资/对外承包/进出口/外资数字** → `china-trade-investment-stats.md` 的 `data.mofcom.gov.cn` POST JSON 接口；年度公报与对外援助（CIDCA）见同卡。
- **要某家多边开发银行的项目级明细（项目号·借款国·承诺额·状态）** → `ifis-projects.md`：世行走 `search.worldbank.org/api/v3/projects`（配 `countryshortname_exact`）、亚投行取 `.content/all-projects-data.js`、IDB 走 `data.iadb.org` CKAN，均免 key；ADB/AfDB 本机被 Cloudflare 挡、EBRD/EIB 仅浏览器。
- **要国际组织报告的全文 PDF 与题录（世行/UN/IMF…）** → `io-report-libraries.md`：OKR 走 DSpace 7 REST 顺链取 PDF（handle `10986/…`），UN DL 走 OAI-PMH；OECD iLibrary 订阅、ADB Publications 本机被挡。
- **要中国留学生在某国的官方人数** → `china-students-abroad.md`：加拿大 IRCC 走 open.canada.ca 的 CKAN API + `ircc.canada.ca/opendata-donneesouvertes/data/ODP-TR-Study-IS_CITZ.csv`（免 key）；美国 Open Doors、英国 HESA 被 WAF 挡、仅浏览器；美国另可下 ICE SEVIS 年度 PDF；中国口径 MOE 明细止于 2019。
- **要各国华人人口/华裔规模或联合国移民存量** → `chinese-diaspora.md`：美国 ACS 走 `api.census.gov`（需免费 key，变量元数据免 key，用 `B02015_002E`/`B05006_050E`）；加拿大走 StatCan WDS（免 key，GET 列清单 + POST 取数 + `/n1/tbl/csv/{PID}-eng.zip` 整表）；全球走 UN DESA 移民存量 xlsx（含原籍×目的地矩阵）。

## 相关

- 中国官方统计与区划口径：`../stats/`（`data.stats.gov.cn.md`、`stats.gov.cn.md`、`mca.gov.cn.md`）。
- 中国微观调查（CFPS/CGSS/CHARLS 等）：`../surveys/`；本层是**跨国**调查，二者互补。
- 卫生与人口：`../health/`（`who-gho.md` 是本层 WHO 卡的取数详版、`population.un.org.md` 提供全球人口分母）。
- 数据仓储与 DOI 托管（Harvard Dataverse / GESIS / Zenodo / ICPSR…）：`../repos/`——跨国调查的原始文件常落在这里。
- 项目库与报告库的交叉：`ifis-projects.md`（IFI 项目级）与 `china-overseas-finance.md`、`bri-data.md`（中国对外项目）互为对照；`io-report-libraries.md` 中的 WHO IRIS 详版见 `who.int.md` 与 `../health/who-gho.md`。
- 跨站检索方法（数据集市 JSON 接口等）：`../methods/dataset-hubs.md`。
- 卡片写法与索引规范：`../meta/style.md`。
- 中国对外经贸的口径交叉：双边×分商品贸易 `comtrade.un.org.md`、国际收支/直接投资 `imf.org.md`、跨国宏观面板 `worldbank.org.md`；海关与部委统计（含海关总署 412）`../stats/ministry-stats.md`；中国国内宏观 `../stats/data.stats.gov.cn.md`。
- 留学/移民口径交叉：中国教育统计（公报、教育统计数据）见 `../stats/ministry-stats.md`；全球人口分母 `../health/population.un.org.md`；人口普查与抽样微观数据仓储 `../repos/`。
