# io-report-libraries —— 国际组织报告全文库

- 去哪找：**世界银行 Open Knowledge Repository（OKR）** `https://openknowledge.worldbank.org/`，检索 API `https://openknowledge.worldbank.org/server/api/discover/search/objects?query=<词>&size=<n>`，OAI-PMH `https://openknowledge.worldbank.org/server/oai/request`；**联合国数字图书馆（UN Digital Library）** `https://digitallibrary.un.org/`，批量元数据 OAI-PMH `https://digitallibrary.un.org/oai2d`；**IMF eLibrary** `https://www.elibrary.imf.org/`。
- 什么时候用：要国际组织**报告/工作论文/年度刊的全文 PDF 或题录**——世行《World Development Report》《China Economic Update》、UN 文件与决议、IMF 出版物；按主题/国家/年份检索并批量取 handle/DOI 与 PDF；爬全文喂 RAG 或做文献综述。
- 怎么搜：OKR 与 UN DL 免费、免 key。OKR 是 DSpace 7 REST（检索 → item → bundle → bitstream → PDF），UN DL 走 OAI-PMH 批量拉元数据：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① OKR 检索：取 _embedded.searchResult._embedded.objects[]._embedded.indexableObject.{uuid,handle,name,metadata}
  curl -s -A "$UA" 'https://openknowledge.worldbank.org/server/api/discover/search/objects?query=china&size=5&page=0'
  # ② 顺链取全文 PDF：item → bundles(ORIGINAL) → bitstreams → content
  curl -s -A "$UA" 'https://openknowledge.worldbank.org/server/api/core/items/<uuid>/bundles'
  curl -s -A "$UA" 'https://openknowledge.worldbank.org/server/api/core/bundles/<bundleUuid>/bitstreams'
  curl -sL -A "$UA" 'https://openknowledge.worldbank.org/server/api/core/bitstreams/<bitstreamUuid>/content' -o report.pdf
  # ③ UN DL：OAI-PMH 拉元数据（oai_dc 或 marcxml；按日期窗分页用 resumptionToken）
  curl -s 'https://digitallibrary.un.org/oai2d?verb=ListRecords&metadataPrefix=oai_dc&from=2024-01-01&until=2024-01-03'
  ```
  - 结果形态：OKR = HAL JSON（`_embedded` 逐层嵌套）；UN DL OAI = XML（`<record>` / `<identifier>oai:digitallibrary.un.org:…`）；IMF eLibrary = 网页（JS 站）。
- 覆盖：OKR 收录世行出版物与研究产出（专著、工作论文、期刊、国别报告），handle 前缀 `10986/…`，正文以 PDF + 提取 TXT 双 bitstream 提供；UN DL 收录**联合国系统**文件/出版物/**表决记录**，元数据为 DC/MARC（覆盖与 1946 起为上游声明，未本机实测）；IMF eLibrary 覆盖 IMF 图书/期刊/工作论文（部分开放、部分订阅，上游声明）；OECD iLibrary 覆盖 OECD 报告/期刊/统计（订阅，上游声明）。
- 门槛：OKR、UN DL **免费、无 key、无注册**；UN DL **网页检索接口对 curl 返回 202 空响应**（正文靠 OAI-PMH 或浏览器）；OECD iLibrary、UN iLibrary、ADB Publications 为**订阅/机构 IP**，且本机被 Cloudflare 挑战。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA、`-L`、20 s 超时）：
  - OKR `…/api/discover/search/objects?query=china&size=1` → 200 `application/hal+json`，命中《China Economic Update, June 2025》，`uuid=f87ebe01-4eb7-4443-adbc-f9180fc01efc`、`handle=10986/43431`，`totalElements=1640`；`/server/oai/request?verb=Identify` → 200，`repositoryName=Open Knowledge Repository`。
  - OKR `/api/core/items/f87ebe01-…/bundles` → 200，含 `ORIGINAL`（`uuid=cb7ba0c8-…`）、`LICENSE`、`THUMBNAIL`；`/api/core/bundles/cb7ba0c8-…/bitstreams` → 200，含 `IDU-….pdf`、`….txt`，下载链 `/api/core/bitstreams/43f4bc2c-…/content`。
  - UN DL `oai2d?verb=ListRecords&metadataPrefix=oai_dc&from=2024-01-01&until=2024-01-03` → 200 `text/xml`，返回多条 `<record>`（如 `oai:digitallibrary.un.org:4014438`）；空窗日期 → `noRecordsMatch`；`ListMetadataFormats` → 200（`marcxml` + `oai_dc`）；`/search?p=china`、`/api/records` → **202 空体 / 404 Unresolvable route**。
  - ❌ 本机被 Cloudflare 挡（403 "Just a moment..."）：`www.oecd-ilibrary.org`、`www.oecd.org/en/publications.html`、`www.un-ilibrary.org`、`www.adb.org/publications`；`researchrepository.ilo.org` → 302 → `/esploro/`（Ex Libris 门户，200）。
- 上游：世行 `https://openknowledge.worldbank.org/` ｜ UN `https://digitallibrary.un.org/` ｜ IMF `https://www.elibrary.imf.org/`。

## 细节

### OKR（DSpace 7）端点链

| 步骤 | 端点 |
|---|---|
| 检索 | `/server/api/discover/search/objects?query=&size=&page=&sort=` |
| 单条 | `/server/api/core/items/{uuid}` |
| 文件包 | `/server/api/core/items/{uuid}/bundles`（`ORIGINAL` 含正文） |
| 比特流 | `/server/api/core/bundles/{uuid}/bitstreams` |
| 下载 | `/server/api/core/bitstreams/{uuid}/content` |
| 元数据收割 | `/server/oai/request?verb=ListRecords&metadataPrefix=oai_dc&set=` |

- handle 形如 `10986/43431`，等价人用页 `https://openknowledge.worldbank.org/handle/10986/43431`；`indexableObject.metadata` 为 `dc.*` 字段（含 `dc.date.issued`、`dc.identifier.doi`、`dc.type` 等）。

### UN Digital Library

- 站点为 Invenio（1.x 风格）：`/oai2d`（OAI-PMH）可用，`metadataPrefix=oai_dc` / `marcxml`（两者均已实测列出）；网页检索 `/search?p=<词>` 需浏览器。单条标识 `oai:digitallibrary.un.org:<id>`。

### 相关已收

- WHO 报告/指南全文（IRIS，DSpace 7，其 REST API 匿名 403）→ `who.int.md`；卫生取数 → `../health/who-gho.md`。
- ILO 劳动统计 → `ilostat.ilo.org.md`；ILO 研究门户（Ex Libris Esploro）`https://researchrepository.ilo.org/` 需浏览器。
- OECD **统计**（SDMX，免 key）→ `oecd.org.md`、`https://data-explorer.oecd.org/`；OECD iLibrary 是**出版物**订阅平台，两者不同。
- 世行**统计指标**（`api.worldbank.org`）→ `worldbank.org.md`，与本卡的报告库（OKR）是两套系统。

## 坑

1. **OKR 是 DSpace 7**：旧的 `/rest/` API 已废，必须走 `/server/api/…`；`bitstreams/{uuid}/content` 要带 UA 并 `-L`，否则可能 403/404。
2. **UN DL 网页检索对非浏览器 UA 返回 202 空体**：别当"接口挂了"，批量元数据走 OAI-PMH，全文/浏览用浏览器。
3. **商业库判据**：OECD iLibrary、UN iLibrary 是**订阅制**（题录/摘要可见，全文按机构 IP）；本机链路另有 Cloudflare 挑战，二者叠加。
4. **Cloudflare 挑战 ≠ 无内容**（ADB Publications / OECD）：换出口或浏览器可过。
5. **域名迁移**：世行旧文档域 `wds.worldbank.org` 已并入 `openknowledge.worldbank.org`（上游声明，未本机实测）；引用 handle 比引用旧 URL 稳。
6. 引用报告时写全 **handle/DOI + 版本年份 + 访问日**；同一报告的 PDF 与 TXT 是两条 bitstream，别重复计数。
