# european-china-collections —— 欧洲敦煌与汉籍馆藏

- 去哪找：
  - 国际敦煌项目 IDP：`https://idp.bl.uk/`（主站，本机被 Cloudflare 拦）；可用镜像 `http://idp.nlc.cn/`（北京·国图）、`http://idp.bbaw.de/`（柏林）
  - 大英图书馆数字手稿入口：`https://www.bl.uk/collection/digitised-manuscripts-archives`（旧 `www.bl.uk/manuscripts` 已 404）
  - 英国国家档案馆 Discovery：`https://discovery.nationalarchives.gov.uk/`
  - 法国国家图书馆 Gallica：`https://gallica.bnf.fr/`
  - 柏林国立图书馆数字馆藏：`https://digital.staatsbibliothek-berlin.de/`
  - 柏林·数字吐鲁番档案（BBAW）：`https://turfan.bbaw.de/dta/index.html`
- 什么时候用：找**敦煌写本/吐鲁番文书**（斯坦因、伯希和收集品）图像与目录、清代中国外交档案（英国 FO 系列）、欧洲所藏汉籍善本与敦煌文献。
- 怎么搜：四馆取法不同，端点表见「细节」。
  - IDP：两步 POST + cookie 检索（`search_wait.a4d` → 等待页 JS 跳 `search_results.a4d?uid=…`），图像经 `image.a4d?id=<n>` 直取。
  - TNA：`https://discovery.nationalarchives.gov.uk/API/search/records?sps.searchQuery=<词>&sps.recordSeries=<系列>&sps.resultsPageSize=<n>` → JSON，免 key。
  - Gallica：SRU `https://gallica.bnf.fr/SRU?operation=searchRetrieve&version=1.2&query=gallica all "<词>"&maximumRecords=<n>` → XML；IIIF `https://gallica.bnf.fr/iiif/<ark>/manifest.json`。
  - SBB：OAI-PMH `https://oai.sbb.berlin/?verb=…`；IIIF `https://content.staatsbibliothek-berlin.de/dc/<PPN>/manifest`；检索站是 SPA，仅浏览器。
- 覆盖：敦煌写本（英藏 Stein Or. 系列、法藏 Pelliot、中/俄/日藏，IDP 联邦库）；柏林吐鲁番文书；英国 FO 系列中国外交档案（FO 371 中国相关 `count` 15,102）；欧洲汉籍善本。年代 4—20 世纪。
- 门槛：IDP 镜像免登录；TNA 检索/详情 API 免 key（数字化下载/订购按记录页，未本机实测）；Gallica 免登录，官方使用条款允许下载图像（上游条款，未本机实测下载）；SBB OAI/IIIF 免登录；Turfan DTA 静态页免登录。
- 实测：2026-10-03，`POST http://idp.nlc.cn/database/search_wait.a4d`（`-F f_quickSearchValue=dunhuang`）→ 200 等待页 → GET `search_results.a4d?uid=…` → 200 结果页；`image.a4d?id=920` → 200 `image/jpeg`。`https://discovery.nationalarchives.gov.uk/API/search/records?sps.searchQuery=China&sps.recordSeries=FO%20371&sps.resultsPageSize=3` → 200 JSON `count 15102`；`https://discovery.nationalarchives.gov.uk/API/records/v1/details/C2880913` → 200 JSON。`https://gallica.bnf.fr/SRU?…query=gallica all "Pelliot chinois"…` → 200 XML `numberOfRecords 11310`；`https://gallica.bnf.fr/iiif/ark:/12148/btv1b10099927x/manifest.json` → 200 JSON，label「Pelliot sanscrit Dunhuang 11」。`https://oai.sbb.berlin/?verb=ListSets` → 200 XML；`https://content.staatsbibliothek-berlin.de/dc/PPN867445300/manifest` → 200 `application/ld+json` `sc:Manifest`。`https://turfan.bbaw.de/dta/index.html` → 200「Digitales Turfan Archiv」。`https://idp.bl.uk/`（curl 与无头 Chromium）→ Cloudflare「Just a moment...」❌。
- 上游：<https://idp.bl.uk/>、<https://www.nationalarchives.gov.uk/>、<https://gallica.bnf.fr/>、<https://staatsbibliothek-berlin.de/>、<https://turfan.bbaw.de/>

## 细节

> 探测纪律（本机实测 2026-10-03）：桌面 Chrome UA、20s 超时、≥1.5s 间隔。`✅`=200、`❌`=被拦。

### IDP（国际敦煌项目，老 .a4d 应用）

| 用途 | 端点 | 形态 |
|---|---|---|
| 快速检索 | `POST http://idp.nlc.cn/database/search_wait.a4d`，body `f_quickSearchValue=<词>` | ✅ 200 等待页，JS 跳 `search_results.a4d?uid=<uid>;random=<n>` |
| 结果页 | `GET http://idp.nlc.cn/database/search_results.a4d?uid=<uid>;random=<n>`（带同一 cookie） | ✅ 200 HTML；翻页 `;bst=<起始>` |
| 记录页 | `…/database/oo_scroll_h.a4d?uid=<uid>;recnum=<n>;index=<n>` | ✅ 200 HTML，含编号（如 `Or.8210/S.5979`）、机构、遗址、语言 |
| 图像查看器 | `…/database/oo_loader.a4d?pm=<编号>;img=1` | ✅ 200 HTML |
| 图像 | `http://idp.nlc.cn/image.a4d?id=<n>`（`;format=jpg` 可加） | ✅ 200 `image/jpeg` / `image/png` |
| 高级/目录/书目检索 | `…/database/database_search.a4d`、`catalogue_search.a4d`、`bibliography_search.a4d` | ✅ 200 HTML 表单 |

- 镜像同为老 IDP 应用：`http://idp.nlc.cn/`（北京）、`http://idp.bbaw.de/`（柏林，含 `pages/china_server.a4d` 链接）；主站 `idp.bl.uk` 被 Cloudflare 拦。

### 英国国家档案馆 Discovery（TNA）

| 用途 | 端点 | 形态 |
|---|---|---|
| 记录检索 | `https://discovery.nationalarchives.gov.uk/API/search/records?sps.searchQuery=<词>&sps.recordSeries=<系列>&sps.resultsPageSize=<n>` | ✅ 200 JSON；`count` 总数、`records[]`（`reference`/`title`/`coveringDates`/`id`） |
| 记录详情 | `https://discovery.nationalarchives.gov.uk/API/records/v1/details/<id>`（id 如 `C2880913`） | ✅ 200 JSON（`heldBy`/`closureStatus`/`catalogueLevel`…） |

- 免 key。FO 系列示例：`sps.recordSeries=FO 371`（英国外交部中国通函，China 命中 `count 15102`）。Discovery 是**目录**，不等同于数字化全文。

### Gallica（法国国家图书馆）

- SRU 检索：`https://gallica.bnf.fr/SRU?operation=searchRetrieve&version=1.2&query=gallica all "<词>"&maximumRecords=<n>` → ✅ 200 XML（`numberOfRecords`、`dc:` 元数据、`ark:/12148/…`）。
- IIIF：`https://gallica.bnf.fr/iiif/<ark>/manifest.json` → ✅ 200 JSON（IIIF Presentation 2，含 `label`、`license`）。
- 量级：`Pelliot chinois` → 11,310；`dunhuang` → 154；Pelliot 敦煌稿本已入 Gallica IIIF（label 例「Pelliot sanscrit Dunhuang 11」）。
- 首页：`https://gallica.bnf.fr/accueil/fr/content/accueil-fr?mode=desktop`。

### 柏林国立图书馆（SBB）与吐鲁番

- OAI-PMH：`https://oai.sbb.berlin/?verb=ListSets`（`metadataPrefix=oai_dc` 或 `mets`；`set=all`/`historische.drucke` 等）→ ✅ 200 XML。
- IIIF：`https://content.staatsbibliothek-berlin.de/dc/<PPN>/manifest`（`PPN867445300` 实测）→ ✅ 200 JSON `sc:Manifest`。
- 检索站 `https://digital.staatsbibliothek-berlin.de/` 是 Meteor **SPA**，服务端只回壳 → **仅浏览器**；本机未探到匿名 JSON 检索 API。
- 数字吐鲁番档案：`https://turfan.bbaw.de/dta/index.html`（按语种/出土地分目录 `dta/u/`、`dta/ch_u/`…，静态 HTML）；主站 `https://turfan.bbaw.de/`（Plone，含 `idp-berlin.html`）。

## 坑

1. **IDP 主站 `idp.bl.uk` 被 Cloudflare 挑战拦**（curl 与无头 Chromium 均停在「Just a moment...」）→ 改用北京/柏林镜像；镜像**仅 http 通，https 不通**。
2. **IDP 检索是两步**：先 POST 得等待页，再按页内 `window.location.href` 带同一 cookie GET 结果页；直接 GET `search_results.a4d`（无 `uid`）无效。
3. Gallica SRU 主路径是 `https://gallica.bnf.fr/SRU`；`/services/engine/search/sru` 返回的是 HTML 壳。`.texteBrut` 需**真实 ark**，假 ark → 400。
4. SBB 检索站是 SPA，服务端检索不可 curl；用 OAI-PMH + IIIF 定位，或直接开浏览器。
5. TNA Discovery 只给目录与开放状态，**下载/订购**按记录页决定（`closureStatus` 标开放/封闭）。
6. 大英图书馆旧「Digitised Manuscripts」入口 `www.bl.uk/manuscripts` → **404**（2023 年网络攻击后未恢复），当前入口为 `/collection/digitised-manuscripts-archives`；斯坦因敦煌图像主要仍经 IDP。
