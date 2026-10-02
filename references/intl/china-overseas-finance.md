# china-overseas-finance —— 中国海外发展融资项目库

- 去哪找：**BU GDP Center**「全球中国数据库」`https://www.bu.edu/gdp/research/databases/global-china-databases/`（CODF、中非贷款 CLA，直链 xlsx/csv 见「细节」）；**AidData** GeoGCDF `https://github.com/aiddata/gcdf-geospatial-data/releases/latest`（表数据门户 `https://www.aiddata.org/datasets`，本机不可达）；**CARI 中非研究倡议** `https://www.sais-cari.org/data`。
- 什么时候用：要**项目级**的中国对外贷款/援助/投资明细（借款人、贷款方、年份、金额、部门、经纬度）；做中国对非融资、一带一路债务、能源/交通项目、GIS 落点；要可直接进回归或画图的点线面板。
- 怎么取：三家都**免 key、免登录**，但入口不同——BU 与 CARI 是静态文件直链，AidData 表数据在官网（本机不通）而 GIS 数据在 GitHub Releases：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① BU GDP：xlsx 直链 + 交互 App 背后的全量 CSV
  curl -sLO -A "$UA" 'https://www.bu.edu/gdp/files/2025/06/CODF-Database-Dataset-2025-EN.xlsx'
  curl -sL -A "$UA" 'https://www.bu.edu/gdp/chinas-overseas-development-finance/static/media/projects-06-06-25_adjusted.c93d5f54.csv' -o codf_2025.csv
  curl -sL -A "$UA" 'https://www.bu.edu/gdp/chinese-loans-to-africa-database/static/media/ChinaLoansToAfrica_2025.d6bf877a4df94565ae87.csv' -o cla_2025.csv
  # ② AidData GeoGCDF：先取最新 release 的资产 URL（版本/文件名会变，勿写死）
  curl -s 'https://api.github.com/repos/aiddata/gcdf-geospatial-data/releases/latest'
  # ③ CARI：/s/*.xlsx 直链
  curl -sLO -A "$UA" 'https://www.sais-cari.org/s/TradeData_Nov2025.xlsx'
  ```
  结果形态：**xlsx / CSV / GeoPackage(zip)**；BU 交互 App 与 AidData 站点是 React/JS 页面，浏览器里能筛选，取全量以上面的文件为准。
- 覆盖：项目级，时间跨度随库——BU CODF 为 2025 版数据文件、CLA 覆盖 2000–2024（页面标题所载）、CARI 贸易/合同/劳工为 2025 版快照、GeoGCDF v3.0.1（2024-06）对应 GCDF 2.0；全球 + 分国别，含部门/金额/坐标。具体起止年份以各库 read-me 为准。
- 门槛：**免费、无需注册**（BU/CARI 直链文件）；AidData 官网数据一般需在其数据页登记后下载（上游惯例，因该站本机超时，未本机实测）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA、`-L`、20s）——BU `CODF-Database-Dataset-2025-EN.xlsx` `206`（`-r 0-200`）`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`；CODF App CSV 首行 25 列（`BU ID,Project name,Country,Region,Borrower,Lender,Year,Loan Amount (USD M),Sector,…,Rep_lat,Rep_lon,precision,…`）；CLA App CSV 命中 `ChinaLoansToAfrica_2025…csv`；CARI `/s/TradeData_Nov2025.xlsx` `206` xlsx 类型（`302 → static1.squarespace.com`；该 CDN 主机随后一次调用变为不可达，见「坑」）；`api.github.com/…/gcdf-geospatial-data/releases/latest` `200`，资产 `all_combined_global.gpkg.zip`(≈496 MB)、`OSM_grouped.zip`(≈551 MB)。❌ 本机不通：`www.aiddata.org`/`api.aiddata.org`/`docs.aiddata.org` 连接超时（20 s，无响应），`sais.jhu.edu/cari` → `403 Cloudflare`，`aei.org`/`heritage.org` 超时。
- 上游：BU Global Development Policy Center `https://www.bu.edu/gdp/research/databases/global-china-databases/`；AidData `https://www.aiddata.org/china`；CARI `https://www.sais-cari.org/`。

## 细节

### 已实测的直链与入口（2026-10-03）

| 数据 | 入口页 | 取数直链 |
|---|---|---|
| BU CODF（中国海外发展融资，项目级） | `…/gdp/chinas-overseas-development-finance-database-data-download/` | `…/gdp/files/2025/06/CODF-Database-Dataset-2025-EN.xlsx`（另有 `-CN.xlsx`）、`…/CODF-Footprint-Map-and-Spatial-Data-DUA.pdf` |
| BU CODF 交互 App（全量 CSV） | `…/gdp/chinas-overseas-development-finance/` | `…/chinas-overseas-development-finance/static/media/projects-06-06-25_adjusted.c93d5f54.csv` |
| BU 中非贷款 CLA（2000–2024） | `…/gdp/chinese-loans-to-africa-database/` | `…/chinese-loans-to-africa-database/static/media/ChinaLoansToAfrica_2025.d6bf877a4df94565ae87.csv` |
| AidData GeoGCDF v3.0.1 | `github.com/aiddata/gcdf-geospatial-data` | `github.com/aiddata/gcdf-geospatial-data/releases/download/v3.0.1/all_combined_global.gpkg.zip`、`…/OSM_grouped.zip` |
| CARI 中非贸易 | `sais-cari.org/data-china-africa-trade` | `sais-cari.org/s/TradeData_Nov2025.xlsx` |
| CARI 中非承包合同 | `sais-cari.org/data-chinese-contracts-in-africa` | `sais-cari.org/s/ContractData_Nov2025.xlsx` |
| CARI 中国全球援助 | `sais-cari.org/data-chinese-global-foreign-aid` | `sais-cari.org/s/ForeignAid_May2025.xlsx` |
| CARI 中非劳工 | `sais-cari.org/data-chinese-workers-in-africa` | `sais-cari.org/s/LaborData_Nov2025-9kw8.xlsx` |

- BU 与 CARI 的落地页是**静态 HTML**（可 curl），交互图是 React SPA；数据文件名里带**内容哈希/月份**（如 `Nov2025`、`06-06-25`），站点更新即失效——脚本应抓落地页再解析，别硬编码哈希。
- BU GDP 站另可走 WordPress JSON：`https://www.bu.edu/gdp/wp-json/wp/v2/pages/{id}`。
- AidData 表数据（GCDF 2.0，含项目 ID/融资类型/是否官方口径等字段，规模上万条——上游声明，未本机核）只在官网与第三方 R 包（`felixhaass/aiddata`、`t-emery/chinadevfin2`）里分发。

## 坑

1. **本机网络**：`aiddata.org`、`csis.org`、`lowyinstitute.org`、`aei.org`、`heritage.org` 等均为连接超时（DNS 还被污染成 Facebook/Dropbox 段），**不代表站点挂了**；能走的替代是 GitHub Releases（GeoGCDF）、Harvard Dataverse API（`dataverse.harvard.edu/api/search`，实测可用）。
2. **同名不同源**：CARI 的「Chinese Loans to Africa」数据库**已移交 BU GDP Center 续更**（CARI 页面 `/data-chinese-loans-to-africa` 已无直链），引用 CLA 数据请认 BU 的 2000–2024 版，别再引 CARI 旧版。
3. **金额单位不统一**：BU 列名写 `Loan Amount (USD M)`（百万美元），CARI 表多为百万/十亿美元按表头，混用前先读表头与 read-me。
4. **口径非官方**：这些是**研究机构自建**的媒体/公开源汇编（AidData 有「官方融资 vs 商业融资」旗标），与商务部/统计局口径不可直接相加；正式引用要写清库名 + 版本 + 访问日。
5. GeoGCDF 是**地理特征**（点/线）而非金额明细，量级数百 MB，需配 GDAL/GeoPandas；金额与属性仍回 GCDF 表数据。
6. **CARI 直链要过 Squarespace CDN**：`sais-cari.org/s/*.xlsx` 会 `302` 到 `static1.squarespace.com`，本机该 CDN 主机**间歇不可达**（实测一次 206、一次连接失败）——下不动时重试、改用 `curl -L` 且设足超时，或在浏览器里点落地页的下载按钮。
