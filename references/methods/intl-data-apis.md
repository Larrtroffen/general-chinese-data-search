# intl-data-apis —— 国际统计库的开放 API 速查

- 去哪找：World Bank `https://api.worldbank.org/v2/`；WHO GHO `https://ghoapi.azureedge.net/api/`；Eurostat `https://ec.europa.eu/eurostat/api/dissemination/`；OECD `https://sdmx.oecd.org/public/rest/`；IMF `https://api.imf.org/external/sdmx/2.1/` 与 `https://www.imf.org/external/datamapper/api/v1/`；UN Comtrade `https://comtradeapi.un.org/`；UN Data `https://data.un.org/WS/rest/`；Our World in Data `https://ourworldindata.org/grapher/{slug}.csv`。
- 什么时候用：要**跨国 / 跨年可比口径**的宏观数字（GDP、人口、贸易、健康、教育、能源、性别…），并且想直接进脚本/入库，而不是手抄年鉴表格；也用来给中文统计口径做对照（`../stats/`）。
- 怎么搜：**每个库给 URL 模板 + 最小 curl**（见「细节」），返回 JSON / JSON-stat / SDMX-CSV / CSV；维度过滤写在查询参数或 SDMX key 里，分页看各库的 meta。多数免 key；IMF 有 UA 门；UN Comtrade 全量需订阅 key。
- 覆盖：8 个机构（World Bank / WHO / Eurostat / OECD / IMF / UN Comtrade / UN Data / OWID）；全球国别 × 年/月/季；粒度到国别-指标-时间点（微观层面不在这里，见 `microdata-access.md`）。
- 门槛：多数**免费无 key**（World Bank / WHO / Eurostat / OECD / OWID / UN Data 免 key）；UN Comtrade 预览免 key、全量需免费注册的 `subscription-key`；IMF 需裸 curl UA；IPUMS/ICPSR/GESIS 这类微观库另见 `microdata-access.md`。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，同主机间隔 ≥1.5 s；逐库结果见「探测记录」。
- 上游：各机构开发者/API 文档（入口见上）。

> 数据以各库官方口径为准；跨国对比前先核单位、购买力口径（PPP vs 现价美元）与基准年，别把不同库的数字直接相减。

## 细节

### 速查表

| 库 | 端点 | 认证 | 过滤方式 | 返回 | 本机 |
|---|---|---|---|---|---|
| World Bank | `api.worldbank.org/v2/country/{c}/indicator/{i}` | 无 | 路径 + `date=` | JSON 数组 | ✅ |
| WHO GHO | `ghoapi.azureedge.net/api/{IndicatorCode}` | 无 | OData `$filter` | OData JSON | ✅ |
| Eurostat | `ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{ds}` | 无 | 每维一个查询参数 | JSON-stat 2.0 | ✅ |
| OECD | `sdmx.oecd.org/public/rest/data/{flowRef}/{key}` | 无 | SDMX 点号 key | SDMX-CSV / JSON | ✅ |
| IMF DataMapper | `www.imf.org/external/datamapper/api/v1/{IND}` | 无（**需裸 UA**） | 路径 | JSON | ✅ |
| IMF SDMX | `api.imf.org/external/sdmx/2.1/{path}` | 无 | SDMX | XML | ✅ |
| UN Comtrade | `comtradeapi.un.org/public/v1/preview/{t}/{f}/{cl}` | 免 key（预览） | 查询参数 | JSON | ✅ |
| UN Data | `data.un.org/WS/rest/{dataflow,data}/…` | 无 | SDMX key | XML / JSON | ⚠️ 仅结构端点 |
| Our World in Data | `ourworldindata.org/grapher/{slug}.csv` | 无 | `csvType=filtered&country=~ISO3` | CSV | ✅ |

### 1. World Bank（`api.worldbank.org/v2`）—— 世界发展指标

```bash
# 单指标单国：中国人均 GDP（现价美元）2020–2022
curl -s 'https://api.worldbank.org/v2/country/CHN/indicator/NY.GDP.PCAP.CD?format=json&date=2020:2022&per_page=100'
# 指标检索（source=2 即 WDI）
curl -s 'https://api.worldbank.org/v2/indicator?format=json&source=2&per_page=3'
# 国别表
curl -s 'https://api.worldbank.org/v2/country?format=json&per_page=2'
```

- 返回恒为 `[meta, rows]` 两元素数组：`meta={page,pages,per_page,total,sourceid,lastupdated}`；`rows[]={indicator{id,value},country{id,value},countryiso3code,date,value,unit,obs_status,decimal}`。
- 国别码可用 `iso3`（`CHN`）或 `all` 取全球；`date=2000:2022` 支持区间；`per_page`/`page` 翻页；缺测值的 `value` 是 `null`。
- 实测：`country/CHN/indicator/NY.GDP.PCAP.CD?date=2020:2022` → 200，`total=3`、`lastupdated=2026-07-13`、2022 值 `12970.6056414327`；`/v2/indicator?source=2` → `total=1498, pages=500`；`/v2/country` → `total=295, pages=148`。无 key，但跨境慢（本机 11–15 s，建议 `-m 60`）。

### 2. WHO GHO（`ghoapi.azureedge.net/api`）—— 全球卫生观测站

```bash
# 指标检索
curl -s "https://ghoapi.azureedge.net/api/Indicator?\$filter=contains(IndicatorName,'life')&\$top=2"
# 取数：出生期望寿命（WHOSIS_000001）中国
curl -s "https://ghoapi.azureedge.net/api/WHOSIS_000001?\$filter=SpatialDim%20eq%20'CHN'"
```

- OData v4：`$filter` / `$top` / `$skip` / `$orderby` / `$select` 可用；返回 `{"@odata.context":…,"value":[…]}`。
- 字段：`IndicatorCode`、`SpatialDimType`（`COUNTRY`/`REGION`/`GLOBAL`）+ `SpatialDim`、`ParentLocation`、`TimeDim`（年）、`Dim1`（性别 `SEX_BTSX`…）、**`NumericValue`**（数值）、`Low`/`High`、`Value`（带置信区间字符串，如 `"78.2 [76-80.6]"`）、`TimeDimensionBegin/End`。
- 元数据：`/api/Dimension`、`/api/IndicatorDimension`、`/api/{code}/$metadata`。
- 实测：`WHOSIS_000001` + `SpatialDim eq 'CHN'` → 200，1.2–1.5 s，免 key；2022 年 `Dim1=SEX_BTSX`（男女合计）`NumericValue=78.2`，**同一响应还含分性别行（81.4 等），取数前先按 `Dim1` 过滤**。

### 3. Eurostat（`ec.europa.eu/eurostat/api/dissemination`）—— 欧盟统计

```bash
curl -s 'https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp?format=JSON&lang=EN&geo=EU27_2020&time=2022&unit=CP_MEUR&na_item=B1GQ'
# 数据集目录（TSV，~2 MB）
curl -s 'https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt?lang=en'
```

- 每个维度一个查询参数（维名见目录或数据集页），`time=2022` 或 `time=2020:2022`；`format=JSON`（默认 JSON-stat 2.0），另有 `SDMX-CSV` 等格式（上游声明）。
- JSON-stat 结构：`value` 是**稀疏扁平索引**（`{"0":16194128.9}`）→ 用 `id`（维度顺序）、`size`（各维基数）、`dimension.{dim}.category.index`（码→位置）做 row-major 还原（第一维变化最慢）。
- 实测：`nama_10_gdp` + `geo=EU27_2020&time=2022&unit=CP_MEUR&na_item=B1GQ` → 200，`value["0"]=16194128.9`，`updated=2026-10-02T11:00:00+0200`；目录 TSV 1,967,686 B（列 `title/code/type/last update of data/data start/data end`）。免 key，0.7 s。

### 4. OECD（`sdmx.oecd.org/public/rest`）—— SDMX 2.1

```bash
# 综合领先指标（CLI）：中国，月度，2023-01 起
curl -s 'https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_STES@DF_CLI,4.1/CHN.M.LI...AA...H?startPeriod=2023-01&format=csvfilewithlabels'
# 数据流目录
curl -s 'https://sdmx.oecd.org/public/rest/dataflow/all?format=jsondata'
```

- 路径 = `/{flowRef}/{key}`：`flowRef` 形如 `AGENCY,DSD_XXX@DF_YYY,版本`；`key` 是**点号分隔的维度位置**，空位 = 通配（`CHN.M.LI...AA...H`）。
- `format=csvfilewithlabels` → 首两行结构注释 + 数据行，列名同时给 `CODE` 与 `Label`；`format=jsondata`（SDMX-JSON）+ `dimensionAtObservation=AllDimensions` 更适合脚本。
- 实测：CLI 请求 → 200，`13716 B`，`REF_AREA=CHN`、`FREQ=Monthly`、`MEASURE=LI` 行存在；免 key，2 s。

### 5. IMF —— 旧域已退役，用新 SDMX + DataMapper

```bash
# 新 SDMX 2.1（结构）
curl -s 'https://api.imf.org/external/sdmx/2.1/dataflow'
# DataMapper JSON —— 注意：必须裸 curl UA，否则 403
curl -s -A 'curl/8.7.1' 'https://www.imf.org/external/datamapper/api/v1/NGDPD'
curl -s -A 'curl/8.7.1' 'https://www.imf.org/external/datamapper/api/v1/indicators'
```

- ⚠️ **UA 门**：浏览器 UA 访问 `www.imf.org/external/datamapper/…` → **403 `Access Denied`（Akamai）**；换 `-A curl/8.7.1` 即 200。这是访问 IMF 的关键一步。
- ⚠️ 旧 `dataservices.imf.org` **DNS 已不可解析**（curl error 6），勿再用。
- DataMapper 返回 `{"values":{"{IND}":{"{ISO3}":{"1980":9.095,…}}…}}`；实测 `-A curl/8.7.1` 下 `/NGDPD` → 200，229 个国家/地区（157 KB）；指标清单 `/indicators` → 200（48 KB）；`/NGDPD/CHN` 仍返回 229 国（**按国过滤未生效，未确认**）；新 SDMX `dataflow` → 200，`447,683 B` SDMX-ML。

### 6. UN Comtrade（`comtradeapi.un.org`）—— 贸易流

```bash
# 免 key 预览：中国 2022 年 HS85 进口
curl -s 'https://comtradeapi.un.org/public/v1/preview/C/A/HS?reporterCode=156&period=2022&cmdCode=85&flowCode=M&maxRecords=3'
# 参考表（国家/伙伴/HS 编码）
curl -s 'https://comtradeapi.un.org/files/v1/app/reference/Reporters.json'
```

- 预览路径 `/{typeCode C|S}/{freqCode A|M}/{clCode HS|…}`；查询参数 `reporterCode`、`period`、`cmdCode`、`flowCode`（`M`/`X`）、`partnerCode`。
- 实测：预览 → 200，`{"elapsedTime":"0.02 secs","count":205,"data":[…]}` —— **`maxRecords` 未生效**（仍返 205 条），且 preview 里 `reporterDesc`/`partnerDesc` 为 `null`（只有码）。
- `Reporters.json` → 200 / 80,831 B，`results[]={id,text,reporterCode,reporterDesc,reporterCodeIsoAlpha2,…}`；同目录还有 `partnerAreas.json`、`ClassificationHS.json`、`TradeRegimes.json`。
- **全量**：`https://comtradeapi.un.org/data/v1/get/{type}/{freq}/{cl}` 需 `subscription-key` 头（免费注册，有量级限额）（上游声明，未本机实测）；旧 `comtrade.un.org/api/get` 已退役（上游声明）。

### 7. UN Data（`data.un.org/WS/rest`）—— SDMX 2.1（NSI Web Service v8.15）

```bash
# 数据流目录（SDMX-ML）
curl -s 'https://data.un.org/WS/rest/dataflow/UNSD'
```

- 实测 → 200，`application/vnd.sdmx.structure+xml`，含 `DF_UNDATA_COUNTRYDATA`、`DF_UNDATA_ENERGY`、`DSD_ENERGY`、`DSD_ENERGY_BALANCE_UNDATA`、`DSD_GHG_UNDATA`。
- ⚠️ 取数端点 `GET /WS/rest/data/{flowRef}/{key}?startPeriod=&format=jsondata|csv` —— 实测 `DF_UNDATA_COUNTRYDATA/all?startPeriod=2022&format=jsondata` → **404 `NoRecordsFound`**（`all` 不适用）；应先用 `/WS/rest/datastructure/UNSD/{flowRef}` 拿维度顺序，再给具体 key。**本机未打通**，表格页自带的 Download 处理器取 CSV 更稳。
- 免 key。

### 8. Our World in Data（`ourworldindata.org`）—— 图表即接口

```bash
# 只取中国（~ISO3）的期望寿命，短列名
curl -s 'https://ourworldindata.org/grapher/life-expectancy.csv?csvType=filtered&country=~CHN&useColumnShortNames=true'
# 图表元数据（含引用）
curl -s 'https://ourworldindata.org/grapher/life-expectancy.metadata.json'
```

- **`csvType=filtered` 是关键**：不加则返回全量（life-expectancy 全量 605 KB，本机 15–20 s 没下完）；加了只返选中项。
- 国家用 `~ISO3`（`~CHN`）；`useColumnShortNames=true` → 列名 `entity,code,year,life_expectancy_0`，否则是完整标题列名。
- 实测：filtered+`~CHN` → 200 / 1,814 B，首行 `China,CHN,1930,32`；`metadata.json` → 200，`chart{title,citation,originalChartUrl,selection}` + `columns`。
- 大批量目录走 `https://catalog.ourworldindata.org/`（上游声明）。

### 探测记录（2026-10-03，macOS arm64，curl 8.x，桌面 UA，同主机间隔 ≥1.5 s）

| host | 状态码 | 观察 |
|---|---|---|
| api.worldbank.org | 200 / 200 / 200 | 指标值、指标目录(1498)、国别表(295)；11–15 s |
| ghoapi.azureedge.net | 200 / 200 | OData 指标检索与取数；1.2–1.5 s |
| ec.europa.eu | 200 / 200 | JSON-stat 取数 `value["0"]=16194128.9`；目录 TSV 1.97 MB |
| sdmx.oecd.org | 200 | `csvfilewithlabels` 出 CSV（13716 B） |
| www.imf.org | 403 / 200 | 浏览器 UA → 403 Access Denied；`-A curl/8.7.1` → 200 |
| api.imf.org | 200 | SDMX 2.1 dataflow，447 KB XML |
| dataservices.imf.org | 000 | DNS 不可解析（已退役） |
| comtradeapi.un.org | 200 / 200 | 预览 205 条（maxRecords 失效）；Reporters.json 80 KB |
| data.un.org | 200 / 404 | dataflow 结构 OK；`/data/…/all` → 404 NoRecordsFound |
| ourworldindata.org | 200 / 200 / 200(超时) | filtered CSV 1.8 KB；metadata OK；全量 CSV 未在 20 s 内下完 |

### 用法建议

1. **先定口径再选库**：同一指标的默认口径不同（WB 现价美元 vs OECD PPP），跨国比较先统一单位与基准年。
2. **批量入库优先 SDMX**：OECD / IMF SDMX 2.1 / Eurostat 都支持一次拉整个 dataflow，比逐指标循环快。
3. **中文本地口径对照**：`../stats/` 的国家/省统计年鉴与这里的国际口径互为校验。
4. **微观数据不在此层**：个体/家户级数据要申请，见 `microdata-access.md`。

## 坑

- **IMF 的 UA 门**：带浏览器 UA 一律 403；脚本里显式 `-A curl/8.7.1`。旧 `dataservices.imf.org` 域名已死。
- **OWID 不加 `csvType=filtered`** 会拉全量，几百 KB 起，慢链路上直接超时；务必加 `-m 60` 与 filter。
- **Comtrade 预览的 `maxRecords` 不可靠**，按 `count` 预估体积再决定要不要转全量 API；preview 无描述字段。
- **Eurostat JSON-stat 的 `value` 是稀疏扁平索引**，不按 `id`/`size` 还原会张冠李戴。
- **WHO GHO 的 `Value` 是字符串**（带置信区间），数值字段是 `NumericValue`。
- **World Bank 跨境慢**（10 s+）且 `per_page` 有上限，翻页按 `meta.pages` 走。
- SDMX key 的空位（`...`）表示通配，位置错一个维度就 404/空结果——先拉 dataflow 结构再拼 key。
