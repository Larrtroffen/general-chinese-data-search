# mo-statistics —— 澳门统计暨普查局与数据平台

- 去哪找：
  - **统计暨普查局（DSEC）** `https://www.dsec.gov.mo/`——统计数据入口 `https://www.dsec.gov.mo/zh-MO/Statistic`、**统计数据资料库**（时间序列）`https://www.dsec.gov.mo/ts/#!/step1/zh-MO`、统计年鉴 `https://www.dsec.gov.mo/zh-MO/Home/Publication/YearbookOfStatistics`
  - **DSEC REST API（TimeSeriesApi）** `https://www.dsec.gov.mo/TimeSeriesApi/App/Indicatorv3`（指标树，JSON）；**SOAP/WSDL** `https://www.dsec.gov.mo/TimeSeriesDatabase.asmx?WSDL`
  - **澳门特别行政区政府数据开放平台** `https://data.gov.mo/`——**数据目录 API** `https://api.data.gov.mo/datadir/search`
- 什么时候用：要澳门官方口径的**人口／旅客／酒店业／博彩收入／消费物价／零售／本地生产总值／对外商品贸易／劳动力**等时间序列；要按指标 ID 批量取数的脚本化流程；要澳门开放数据集清单；写澳门经济、旅游博彩、粤港澳大湾区澳门侧分析时。
- 怎么搜：统计数据数值走 **REST/SOAP API**（先拉指标树拿 `IndicatorID`，再取指标值）；数据开放平台目录走 `api.data.gov.mo` 的 JSON 检索。结果形态：DSEC 指标树/指标值 = **JSON**（REST），另 SOAP 返回 `{Status,Value}`；DSEC 网页可导出 CSV/Excel；data.gov.mo = **JSON**（检索）与 **XLSX**（下载清单）。
- 覆盖：DSEC 时间序列库按「指标树」组织，覆盖人口、社会、劳动力、旅游会展博彩、分销价格、建筑及不动产、贸易投资、行业概况、国民经济等主题；数值含月度/季度/年度，年份随各指标。data.gov.mo 目录含 **1376** 个数据集/资源（含 API 类与文件类）。
- 门槛：**免费、无登录、无 key**；DSEC REST 与 SOAP 均公开；data.gov.mo 目录 API 公开（下载部分资源或需登录，见坑）。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `https://www.dsec.gov.mo/zh-MO/` → `200/9337`；`/zh-MO/Statistic/Database` → `200`；`/zh-MO/Service/WebService` → `200`（正文给出 WSDL 链接）；`/zh-MO/Home/Publication/YearbookOfStatistics` → `200/8089`；`/ts/` → `200/1004` ✅
  - `GET https://www.dsec.gov.mo/TimeSeriesApi/App/Indicatorv3` → `201` `application/json`，`{"Debug_msg":"","Value":[{"IndicatorID":19001,"Description":"人文發展指數","DescriptionEngl":"Human development index","Parent":0.0,"IsLeafNode":"False",…}]}`；加 `?Language=zh-MO` 同结构 ✅
  - `GET https://www.dsec.gov.mo/TimeSeriesDatabase.asmx?WSDL` → `200 text/xml 47012B`，含 `getIndicatorID`、`getIndicatorValue`、`getIndicatorLatestValues`、`getKeyIndicatorList`、`getChart` 等操作 ✅
  - `POST https://api.data.gov.mo/datadir/search`，JSON `{"key":"","page":0,"rows":2,"orderBy":"asc","sortBy":"name","url":false}` → `200` `{"data":{"page":1,"rows":2,"total":1376,"pageTotal":688,"items":[{"id":"…","name":"…","deptName":"行政公職局,…","isFile":1,"isApi":0,…}]}}` ✅
  - `GET https://api.data.gov.mo/datadir/search/download?key=&page=0&rows=2&…` → `200 application/x-msdownload`（实为 **XLSX**，`PK…` 头）✅；`GET /datadir/search` → `405`（须 POST）；`GET /datadir/search/download` → 需较长时间（本机曾超时，重试成功）
  - `https://data.gov.mo/` → `200/1599`（React SPA `index.js`）；`https://api.data.gov.mo/swagger-ui.html` → `200`，但 `/v2/api-docs`、`/swagger-resources` → `404` ⚠️
- 上游：統計暨普查局 `dsec.gov.mo`；澳門特別行政區政府數據開放平台 `data.gov.mo` / `api.data.gov.mo`。

## 细节

### 一、DSEC 时间序列数据库（统计数据库）

- 人读入口：`https://www.dsec.gov.mo/ts/#!/step1/zh-MO`（Angular 单页；分「单表/跨表」步骤，`/ts/?footer=ts` 为带页脚版）。指标释义随页加载 `https://www.dsec.gov.mo/js/data/wiki.js`（含 `key/title/content` 的繁体术语解释）。
- 同域另有专题库：`/CensosWebDB/`（人口普查）、`/TourismDBWeb/`（旅游）、`/EMTS.aspx`（对外商品贸易统计）、`/Intercensos2026/`（中期人口统计）。
- 页面用 **LZ-string**（`LZString.compressToUTF16`）承载所选指标状态，并有导出 CSV/Excel 功能。

### 二、DSEC REST API（TimeSeriesApi）

页面脚本（`https://www.dsec.gov.mo/ts/scripts/scripts-*.js`）定义的常量，主机 `https://www.dsec.gov.mo/TimeSeriesApi`：

| 端点 | 参数 | 用途 |
|---|---|---|
| `/App/Indicatorv3` | `Language`（可选） | 指标树（`Value[]`：`IndicatorID`/`Description`/`DescriptionEngl`/`Parent`/`IsLeafNode`…） |
| `/App/Indicatorv3/{IndicatorID}` | `Language` | 单个指标元数据 |
| `/App/IndicatorValue/LatestSameStartPeriod` | 指标等 | 最新同起点观察值 |
| `/App/KeyIndicatorv3/1/{Language}/{KeyIndicatorID}` | — | 关键指标 |
| `/App/Latest5Indicatorv3/1/{Language}/{Latest5IndicatorID}` | — | 最近 5 期 |
| （内部）`/Api/User/AddReport` | — | 保存自订报表 |

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
# 1) 拉指标树，找 IndicatorID
curl -s -A "$UA" 'https://www.dsec.gov.mo/TimeSeriesApi/App/Indicatorv3'
# 2) 取某指标值（具体子路径以 ts 站 XHR 为准；亦可走 SOAP）
```

### 三、DSEC SOAP Web Service（WSDL）

`https://www.dsec.gov.mo/TimeSeriesDatabase.asmx?WSDL`，操作名：`getIndicatorByID`、`getIndicatorID`、`getIndicatorLatestValue`、`getIndicatorLatestValues`、`getIndicatorValue`、`getChart`（含 `WithSize` 变体）、`getCommonChartList`、`getCommonChart`、`getKeyIndicatorList`、`getKeyIndicatorValue`。返回 `{Status, Value}`（SPA 判 `t.Status` 后取 `t.Value`）。

### 四、澳门数据开放平台（data.gov.mo）

- 前端 `https://data.gov.mo/` 为 React SPA，后端 **`https://api.data.gov.mo`**（Spring Boot，JSON）。
- 数据集检索（**POST**）：`https://api.data.gov.mo/datadir/search`，JSON 体示例：

  ```bash
  curl -s -A "$UA" -X POST -H 'Content-Type: application/json' \
    -d '{"key":"人口","page":0,"rows":10,"orderBy":"asc","sortBy":"name","url":false}' \
    'https://api.data.gov.mo/datadir/search'
  ```

  返回 `data.total`（总数）与 `data.items[]`（`id`/`name`/`deptName`/`deptId`/`updateTime`/`isFile`/`isApi`/`isUrl`/`description`/`visits`）。
- 下载清单：`GET https://api.data.gov.mo/datadir/search/download?...` → XLSX。
- 其他前缀（脚本内出现）：`/datadir/downloadSingleFile?fileId=`、`/datadir/downloadMultiFiles`、`/dataMenu_download`、`/download/list`、`/category/icon/`、`/platform/visit/analysis`。

## 坑

1. **REST 返回码非标准**：`TimeSeriesApi/App/Indicatorv3` 正常返回却带 **HTTP 201**，勿以状态码判断成败，须解析 JSON（`Debug_msg` / `Value`）。
2. **DSEC 主站新旧并存**：统计数据库为 SPA（`/ts/`），数值接口在 `TimeSeriesApi`（REST）与 `TimeSeriesDatabase.asmx`（SOAP）两套；页面 XHR 才是权威参数，REST 子路径可能随版本变化，取不到时以浏览器抓包为准。
3. **data.gov.mo 目录 API 的 GET/POST 分工**：`/datadir/search` 只接受 **POST**（GET 报 405）；`/datadir/search/download` 只接受 **GET**（POST 报 405）。`/datadir/search/download` 偶发**响应缓慢/超时**（本机一次 20 s 超时、重试即通），脚本需设长超时并重试。
4. **api.data.gov.mo 无公开文档**：`/swagger-ui.html` 存在但 `/v2/api-docs`、`/swagger-resources` 均 404，接口清单从 SPA `index.js` 提取；部分资源（脚本提示「须登记才能下载」）**下载需登录**。
5. 部分数据集 `name` 字段把简繁/英多语言以 `☯` 分隔（例 `…☯…☯…Domain Name`），检索与去重时注意。
6. 澳门数据开放平台与 DSEC 是两套系统：**数值以 DSEC 为准**，`data.gov.mo` 主要是目录与资源分发。
