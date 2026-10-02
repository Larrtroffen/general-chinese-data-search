# econ-papers —— 经济学工作论文四源

- 去哪找：RePEc/IDEAS `https://ideas.repec.org/`；NBER `https://www.nber.org/`；CEPR `https://cepr.org/`；SSRN `https://www.ssrn.com/`
- 什么时候用：找**经济学未刊工作论文/讨论稿**（NBER WP、CEPR DP、RePEc 各系列）；按**作者/主题**追经济学前沿；要**编号+DOI/JEL 码+摘要**；查某经济学家被收录了哪些工作论文（RePEc 作者页 / EDIRC 机构页）
- 怎么搜：
  - **RePEc/IDEAS**：`POST https://ideas.repec.org/cgi-bin/htsearch2`，表单 `q=<词>`（页面搜索框即 POST 到此）；结果 HTML，页内报命中数（如 `34 results`）。按系列浏览 `https://ideas.repec.org/s/<系列码>.html`，机构目录 EDIRC `http://edirc.repec.org/`
  - **NBER（JSON API，实测可用）**：`GET https://www.nber.org/api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=10&sortBy=public_date&q=<词>`——返回 `{"totalResults":N,"results":[{"title","authors","displaydate","abstract",…}]}`；论文页 `https://www.nber.org/papers/w<编号>`
  - **CEPR**：检索页 `https://cepr.org/publications/discussion-papers?search_api_fulltext=<词>`（Drupal 全文本参数），结果页含 `/dp<编号>` 链接
  - **SSRN**：见「坑」，本机直连不通；元数据退路走 OpenAlex/Crossref（`paper-lookup.md`）
- 覆盖：RePEc/IDEAS = 全球最大的经济学工作论文聚合（数万系列、含期刊与作者档案，更新随各系列投稿）；NBER WP = 美国国家经济研究局工作论文（`totalResults` 约 3.6 万条，含摘要）；CEPR DP = 欧洲经济政策研究中心讨论稿；SSRN = 社科预印本库（含大量未刊稿）
- 门槛：**IDEAS 检索、NBER API、CEPR 检索页均免 key 免登录**；RePEc 官方 API（`api.repec.org`）需注册代码；SSRN 本机被网络层阻断
- 实测：2026-10-03，macOS + curl（桌面 UA）——IDEAS `POST /cgi-bin/htsearch2` `q=基层治理` → 200，页内「34 results」，含真实 `/p/pra/mprapa/…html` 链接；NBER `GET /api/v1/working_page_listing/contentType/working_paper/_/_/search?page=1&perPage=10&sortBy=public_date` → 200 JSON `totalResults=36309`，加 `&q=inflation` → `totalResults=3610`（确认 `q` 生效）；`https://www.nber.org/papers/w34000` → 200；CEPR `/publications/discussion-papers?search_api_fulltext=inflation` → 200（含 `/dp22009` 等），但 `/publications` → **403 Cloudflare**；`api.repec.org/call.cgi?code=getauthors` → 200 `[{"error":2}]`（未带注册码）；`www.ssrn.com` 与 `papers.ssrn.com/sol3/results.cfm` 均 **超时（HTTP 000）**
- 上游：RePEc（`https://repec.org/`，IDEAS 为其门户）；NBER（`https://www.nber.org/`）；CEPR（`https://cepr.org/`）；SSRN（Elsevier）

## 细节

### NBER API 参数

基址 `https://www.nber.org/api/v1/working_page_listing/contentType/<类型>/<…>/<…>/search`；查询串：`page`、`perPage`、`sortBy`（`public_date`）、`q`（关键词）。`contentType` 取 `working_paper`；返回项的 `authors` 是**HTML 片段**（`<a href="/people/…">`），需去标签。列表页 HTML 另有 `https://www.nber.org/search?q=<词>`。

### RePEc 取数补充

- IDEAS 搜索表单动作是 `/cgi-bin/htsearch2`（不是 `htsearch`，后者只渲染搜索框）。
- RePEc 自身不是数据库，而是**各系列 OAI 元数据的聚合**；批量取数走各系列自己的 RePEc 归档，或用 `paper-lookup.md` 的 OpenAlex/Crossref 按 DOI/作者补引文。
- 机构/作者标识：EDIRC（机构）、RePEc Author Service（作者短名 `p/xxxxx`，即 IDEAS URL 形如 `/e/pabc1.html`、`/p/xxxx/yyy.html`）。

## 坑

- **SSRN 本机直连超时**（`www.ssrn.com`、`papers.ssrn.com` 均 HTTP 000）：要么换出口，要么只取元数据（OpenAlex 收录 SSRN 记录，见 `paper-search-mcp.md` 的 "SSRN(OpenAlex 元数据)"）。
- **CEPR 走 Cloudflare**：同站不同路径策略不一，实测 `/publications` 403、`/publications/discussion-papers` 200 且响应很慢（>20s）——换姿势/重试，别把一次 403 当永久封禁。
- IDEAS 搜索结果页只给命中数与链接，**无结构化字段**；要摘要/DOI 得进详情页或改用 OpenAlex。
- NBER API 的 `q` 对**题名+摘要**匹配，按日期排序才有意义；`perPage` 过大可能被限。
- RePEc 官方 API 无注册码一律 `[{"error": 2}]`，不是"免费开放 API"。

## 相关

- 国际元数据/引文/OA 全文：`paper-lookup.md`（OpenAlex、Crossref、Unpaywall）。
- 多源统一检索与 PDF 下载链：`paper-search-mcp.md`。
- 中文社科期刊/工作论文：`ncpssd.org.md`；外文科技期刊/报告：`nstl.gov.cn.md`。
