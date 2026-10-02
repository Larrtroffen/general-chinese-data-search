# ifis-projects —— 多边开发银行项目库检索

- 去哪找：**世界银行 Projects API** `https://search.worldbank.org/api/v3/projects?format=json`（人用列表页 `https://projects.worldbank.org/en/projects-operations/projects-list`）；**亚投行 AIIB** 全量数据文件 `https://www.aiib.org/en/projects/list/.content/all-projects-data.js`（检索页 `https://www.aiib.org/en/projects/list/index.html`）；**泛美开发银行 IDB** 开放数据 `https://data.iadb.org/api/3/action/package_search?q=project`（数据集 `idb-projects-dataset`）。
- 什么时候用：要**多边开发银行的项目级明细**——项目号、名称、借款国/经济体、批准日、部门、承诺额、状态；拼一国在多边银行受援/贷款/基建的项目清单；把中国对外项目与 IFI 项目对照；导出 JSON/CSV/xlsx 直接进 pandas。
- 怎么搜：世行/亚投行/IDB 开放数据均免费、免 key。世行是 GET JSON，亚投行取静态数据文件，IDB 走 CKAN API：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 世界银行：rows=每页条数、os=偏移、qterm=全文词、<分面>_exact=精确过滤、fl=字段裁剪
  curl -s -A "$UA" 'https://search.worldbank.org/api/v3/projects?format=json&rows=2&os=0&countryshortname_exact=China&fl=id,project_name,countryshortname,status,boardapprovaldate,totalamt'
  # ② 世界银行全量导出（数万项目，xlsx）
  curl -s -A "$UA" 'https://search.worldbank.org/api/v3/projects/all.xlsx' -o wb_projects.xlsx
  # ③ 亚投行：取数据文件后剥掉 "var data=" 与行尾 ";"，JSON.parse 即可
  curl -s -A "$UA" 'https://www.aiib.org/en/projects/list/.content/all-projects-data.js' -o aiib.js
  # ④ IDB：CKAN package_search / package_show，资源为 CSV 直链
  curl -s 'https://data.iadb.org/api/3/action/package_search?q=project&rows=5'
  ```
  - 结果形态：世行 = JSON（`{rows,os,page,total,projects:{项目号:{…}}}`）；亚投行 = JS 内嵌 JSON 数组；IDB = CKAN JSON + CSV 下载链。ADB/AfDB/IDB 主站与 EBRD/EIB 检索页多为浏览器交互（见「细节」）。
- 覆盖：世行 **28,166** 条在世/待批项目（IBRD+IDA，含 2027 财年管线），字段十余个（`fl=*` 取全），支持全文与分面检索；亚投行 **483** 条项目/管线（2026-10 快照）；IDB 项目清单为 2026 版数据集快照。ADB、AfDB、EBRD、EIB 的项目库规模见各自页面（上游声明，未本机实测）。
- 门槛：世行 Projects API、亚投行数据文件、IDB 开放数据**免费、无 key、无注册**；ADB（`adb.org`/`data.adb.org`）、AfDB（`afdb.org`/`mapafrica.afdb.org`）、IDB 主站（`iadb.org`）被 **Cloudflare 人机挑战**挡在 curl 外，需浏览器或换出口；EBRD/EIB 检索页可 curl 到 HTML，但结果由 JS 渲染。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA、`-L`、20 s 超时）：
  - 世行 `…/v3/projects?format=json&rows=2` → 200，`total=28166`；`&qterm=China` → `total=764`；`&countryshortname_exact=China&fl=…` → 200 且首条 `countryshortname=China`；`…/v3/projects/all.xlsx` → 206 `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`。
  - 亚投行 `…/.content/all-projects-data.js` → 200 `application/javascript`，214,052 B，`var data=[…]`，约 483 条。
  - IDB `data.iadb.org/api/3/action/package_search?q=project` → 200，`count=80`，含 `idb-projects-dataset`；`package_show?id=idb-projects-dataset` → 200，资源 `format=CSV`，`url=https://data.iadb.org/files/download/<uuid>`。
  - ❌ 本机不通：`www.adb.org/projects`、`data.adb.org` → **403 Cloudflare**（"Just a moment..."）；`www.afdb.org/en/projects-and-operations`、`mapafrica.afdb.org` → **403 Cloudflare**；`projectsportal.afdb.org`、`dataportal.afdb.org` → **DNS 不解析**；`www.iadb.org/en/projects` → 403 Cloudflare；EBRD `psd.model.json` → 404。
- 上游：世界银行 `https://projects.worldbank.org/` ｜ 亚投行 `https://www.aiib.org/en/projects/list/index.html` ｜ IDB 开放数据 `https://data.iadb.org/`。

## 细节

### 世界银行 Projects API（v3）

| 参数 | 作用 |
|---|---|
| `rows` / `os` / `page` | 每页条数 / 偏移（0 起）/ 页码 |
| `qterm` | 全文关键词（实测 `China` → 764） |
| `countryshortname_exact` | 借款国精确过滤（`China` → 712）；同族 `status_exact`、`sector_exact`、`regionname_exact`、`projectfinancialtype_exact`、`themev2_level*_exact` |
| `fct` | 要返回计数的分面列表（逗号分隔） |
| `fl` | 返回字段裁剪（逗号分隔） |
| `srt` / `order` | 排序字段 / `asc`\|`desc` |

- 返回骨架：`{"rows":2,"os":"0","page":"1","total":"28166","projects":{"P518248":{…}}}`；单条含 `id`、`proj_id`、`countryshortname`、`boardapprovaldate`、`status`、`totalamt`、`curr_ibrd_commitment`、`grantamt`、`idacommamt`、`lendprojectcost`、`borrower`、`impagency`、`project_name`、`regionname`、`closingdate`、`project_abstract` 等。
- 旧接口：`v2/projects?format=json&countrycode=CN`（`total=542`，字段名不同，如 `countryname` 为数组）；归档库 `v2/projectsarchives?format=json&srt=start_date&order=desc`。列表页自身用 `fct=…&fl=…` 拼 URL。

### 亚投行 AIIB

- 数据文件：`https://www.aiib.org/en/projects/list/.content/all-projects-data.js`（`var data=[…]`）。
- 字段：`date, pos, economy, sector, financing_type, project_type, name, approved_funding, committed_funding, proposed_funding, special_funding, status, path`；`path` 即详情页 `/en/projects/details/YYYY/…html`。
- 列表页筛选：`?status=Approved|Proposed|On%20Hold|Terminated%20/%20Cancelled`、`?financing_type=Sovereign|Nonsovereign`。

### 其余 IFI 入口与状态

| 机构 | 入口 | 本机 |
|---|---|---|
| ADB 亚洲开发银行 | `https://www.adb.org/projects`、数据 `/what-we-do/data` | ❌ Cloudflare；子站 `kidb.adb.org/api`（SDMX 统计）200 |
| AfDB 非洲开发银行 | `https://www.afdb.org/en/projects-and-operations`、`https://mapafrica.afdb.org/en/projects` | ❌ Cloudflare / DNS；未见公开文档 API（上游声明，未本机实测） |
| IDB 泛美开发银行 | `https://data.iadb.org/`（CKAN）、主站 `https://www.iadb.org/en/projects` | ✅ CKAN / ❌ 主站 |
| EBRD 欧洲复兴开发银行 | `https://www.ebrd.com/projects.html`、PSD 检索 `/work-with-us/projects/psd.html` | ⚠️ HTML 200，无 JSON API（AEM 站） |
| EIB 欧洲投资银行 | `https://www.eib.org/en/projects/index.htm`、管线 `/projects/pipelines/index`、开放数据 `/publications-research/eib-open-data` | ⚠️ HTML 200；机器可读走 `data.europa.eu` 数据集 `projects-financed-by-the-european-investment-bank` |

## 坑

1. **世行分面参数带 `_exact` 后缀**：`countryshortname_exact=China` 才过滤；`countrycode=CN` 在 **v3 不生效**（`total` 仍 28166），那是 **v2** 的参数。
2. **世行 `total` 是字符串**、`projects` 是以项目号为 key 的**对象**而非数组；`rows`/`os` 分页，默认条数小，抓全量优先用 `all.xlsx` 或逐页翻。
3. **亚投行数据文件在 `.content/` 下、常带 `?t=` 缓存戳**，站点改版即换路径；抓列表页 HTML 的 `<script src>` 再解析最稳。
4. **Cloudflare 人机挑战 ≠ 站点无接口**：ADB/AfDB/IDB 主站在本机链路是 JS 挑战页（403 "Just a moment..."），浏览器可过；不代表数据不存在，记录时注明"仅浏览器"。
5. **同名不同库**：世行项目数据（`search.worldbank.org`）与世行**统计**指标（`api.worldbank.org`，见 `worldbank.org.md`）是两套接口，别混。
6. 中国对外项目级融资另见 `china-overseas-finance.md`（BU/AidData/CARI）与 `bri-data.md`，与 IFI 项目库口径不同（前者含商业/非官方融资）。
