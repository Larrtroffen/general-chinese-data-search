# hk-statistics —— 香港统计处与资料一线通

- 去哪找：
  - **政府统计处（C&SD）** 统计数字入口 `https://www.censtatd.gov.hk/en/`——網上統計表 `https://www.censtatd.gov.hk/en/web_table.html?id={表格ID}`、互動統計資料庫 `https://www.censtatd.gov.hk/en/Interactive_Statistics.html`；**JSON API** `https://www.censtatd.gov.hk/api/get.php?id={表格ID}&lang={en|tc|sc}&param={系统生成串}`
  - **data.gov.hk（資料一線通）** `https://data.gov.hk/en/`——**CKAN 目录 API** `https://data.gov.hk/en-data/api/3/action/{package_search|package_list|package_show}`；**API 规范页** `https://data.gov.hk/en/help/api-spec`（含数据过滤、历史档案、就近设施 API）
  - **香港年報** `https://www.yearbook.gov.hk/`——章节目录 `https://www.yearbook.gov.hk/{年份}/en/index.html`
- 什么时候用：要香港官方口径的**人口／GDP／CPI／失业率／对外商品贸易／零售／薪金**等月度与年度数字；要**开放数据集（CSV/JSON）**及其 API；要引用**《香港年報》**叙述香港年度发展；写港澳经济、跨境贸易、大湾区城市比较时需港方权威数字。
- 怎么搜：C&SD 表格用「網上統計表」页（`web_table.html?id=` 直取，右上角 API 按钮给出 GET 链）；data.gov.hk 目录走 CKAN 3 个 action 直调；数据集文件过滤走 `api.data.gov.hk/v2/filter`。结果形态：C&SD = **JSON**（另有网页内嵌 XLSX/CSV 客户端导出）、CKAN = **JSON**、年報 = **HTML + PDF**。
- 覆盖：C&SD 網上統計表覆盖人口、劳工、贸易、物价、国民经济、行业等约数百张表（表号 `AAA-BBBBB`，如 `110-01001` 人口、`310-31001` GDP）；data.gov.hk 目录含 530+ 条以 census 检索命中的数据集（部门/公共机构/私营机构），年份随各源；年報按年出版。
- 门槛：全部**免费、无登录**；CKAN 与 data.gov.hk API **无需 key**；C&SD `get.php` 的 `param` 为系统生成串（见坑 1），须从网页取用。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `https://www.censtatd.gov.hk/en/` → `200/6115`；`/en/web_table.html?id=110-01001` → `200`；`/en/Interactive_Statistics.html` → `200/4373` ✅
  - `GET /api/get.php?id=110-01001&lang=en&param=` → `200` `application/json`（`"name":"Fail"`，提示 `Table ID is not defined`）；`…&param=1` → `200` 但 `dataSet:[]` ⚠️；带网页生成的 `param`（如 `id=110-02001&param=N4Igxgbi…`）→ `200`，`param` 解出 `{cv,sv,l}` 结构、标题《Land area, land population and population density by District Council district》，`lang=TC` 同样 `200` ✅
  - `https://www.censtatd.gov.hk/datagovhk/WT_data_dict_en.pdf` → `200 application/pdf 587702B`（C&SD 官方 API 说明 PDF，2023-03-08 更新）✅
  - `GET https://data.gov.hk/en-data/api/3/action/package_search?q=census` → `200` JSON `success:true`，`count:530`；`?q=census&rows=1` 返回 `hk-censtatd-highlights-highlights` 及 RSS 资源链；`package_show?id=cc-complaints-complaints-statistics` → `200` 数据集元数据 ✅
  - `GET https://app.data.gov.hk/v1/historical-archive/list-files`（规范页端点）；`GET https://api.data.gov.hk/v1/historical-archive/list-file-versions?url=…&start=20260901&end=20261001` → `200` JSON `{"version-count":0,…}`（日期须 `YYYYMMDD`；传 `2026-09-01` 报 `400 invalid start parameter`）✅
  - `https://www.yearbook.gov.hk/` → `200`；`/2024/en/index.html` → `200/4313`，标题《Hong Kong Yearbook》✅
- 上游：政府統計處 `censtatd.gov.hk`；資料一線通 `data.gov.hk` / `api.data.gov.hk` / `app.data.gov.hk`；香港年報 `yearbook.gov.hk`。

## 细节

### 一、C&SD 網上統計表 JSON API

`GET https://www.censtatd.gov.hk/api/get.php`，三参数（据官方 PDF `datagovhk/WT_data_dict_en.pdf`）：

| 参数 | 说明 | 取值 |
|---|---|---|
| `id` | 表格编号 | 如 `110-01001`、`310-31001` |
| `lang` | 文本语言 | `en` / `tc` / `sc` |
| `param` | 查询选择串 | **系统自动生成（加密串）**，`web_table` 页「API」按钮给出完整 GET 链 |

- 返回 `{header:{status,title,tablenote,source,count}, dataSet:[…]}`；`status.name` = `Success`/`Fail`，`code` = `0`/`1`。
- **最省事取 param 的做法**：打开 `https://www.censtatd.gov.hk/en/web_table.html?id={表格ID}`，勾选期间/变量后点右上「API」→ 复制动态生成的 GET 链。
- 表格下载（XLSX / CSV / CSV-Tabular / XML / SDMX）由页面 JS（SheetJS）**客户端生成**，无独立下载 URL。
- 相关入口：`/en/scode{整数}.html` 为专题页（如 `scode150` = Population Estimates）；`/en/Interactive_Statistics.html` 为互动统计资料库。

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
# 元数据/校验（不带有效 param 时 dataSet 为空）
curl -s -A "$UA" 'https://www.censtatd.gov.hk/api/get.php?id=310-31001&lang=en&param='
# 正常取数（param 从网页 API 按钮获得）
curl -s -A "$UA" 'https://www.censtatd.gov.hk/api/get.php?id=110-02001&lang=tc&param=N4IgxgbiBcoMJwJqJqAjDEB2A…'
```

### 二、data.gov.hk（資料一線通）

| 用途 | 端点 | 方法 | 说明 |
|---|---|---|---|
| 数据集检索 | `https://data.gov.hk/en-data/api/3/action/package_search?q={关键词}&rows={N}` | GET | CKAN；返回 `result.count`、`result.results[]`（含 `name`/`title`/`resources[]`） |
| 全部数据集名 | `…/package_list` | GET | 返回 dataset `name` 字符串数组 |
| 数据集详情 | `…/package_show?id={name或UUID}` | GET | 含各 `resources[].format/url`（可下 CSV/JSON/PDF…） |
| 数据过滤 | `https://api.data.gov.hk/v2/filter` | POST | 见 API 规范页「API for Data Filtering」 |
| 就近设施 | `https://api.data.gov.hk/v1/nearest-schools?lat=&long=&max=` | GET | 「API to Find Nearest Facilities」 |
| 历史档案 | `https://app.data.gov.hk/v1/historical-archive/list-files?...` / `https://api.data.gov.hk/v1/historical-archive/list-file-versions?url=&start=YYYYMMDD&end=YYYYMMDD` | GET | 取某文件的历史版本时间戳 |

- CKAN action 前缀固定 `/en-data/api/3/action/`；`package_show` 传 `id` 用 `name`（如 `cc-complaints-complaints-statistics`）最稳。
- 规范化 API 文档在 `https://data.gov.hk/en/help/api-spec`，内含 category / provider ID 全表（如 `hk-censtatd` = 政府统计处）。

### 三、香港年報

- 根 `https://www.yearbook.gov.hk/`；各年 `https://www.yearbook.gov.hk/{YYYY}/en/index.html` 与 `/tc/`、`/sc/`。
- 结果形态 HTML 章节网 + 章内 PDF；正文为叙述性年度回顾（非统计数据主源，数字请回 C&SD）。

## 坑

1. **C&SD `param` 不是普通查询串**：它是系统生成的加密串（页面加载 `js/lz-string.min.js`，解出为 `{cv,sv,l}` 选择结构），**不能手工拼**；离线/脚本取数须先在网页勾好条件、点「API」复制链。`param=`（空）或 `param=1` 会返回 `200` 但 `dataSet:[]`，**不能据此判定无数据**。
2. **data.gov.hk 有两个 API 域**：目录用 `data.gov.hk/en-data/api/3/action/`；过滤/就近/历史档案用 `api.data.gov.hk` 与 `app.data.gov.hk`，别混。
3. 历史档案端点**日期格式为 `YYYYMMDD`**；用 `YYYY-MM-DD` 会 `400 invalid start parameter`。
4. `package_show` 传入不存在的 `id` 会回落到 SPA 的 HTML（HTTP 200，非 JSON），**须先 `package_search`/`package_list` 取得正确 `name`**。
5. C&SD 表格的 XLSX/CSV 下载按钮是**纯前端生成**，无 `/download` 直链；要机器取数只能走 `get.php`。
6. C&SD 站是 SPA 壳（直接 `curl` 只得到框架 HTML），列表与按钮均 JS 渲染；文献引用务必落 `get.php` 的 `header.title` + 表号 + 期别。
