# paper-search-mcp —— 28 源统一检索与 PDF 下载链

一个可当 **MCP server**、**CLI**、**Claude Code skill** 用的 Python 工具：把 28 个学术平台归一成一个 `Paper` 结构，并给出"**从 DOI 到 PDF**"的回退链。定位是**国际 OA 检索 + 全文获取的调度层**——要"一次查多库、再自动拿 PDF"，用它；只要单库元数据，直接 curl 更轻。

- 去哪找：repo `https://github.com/openags/paper-search-mcp`（1.9MB）；PyPI 包名同 repo；Claude Code skill 的 SKILL.md raw：`https://raw.githubusercontent.com/openags/paper-search-mcp/main/claude-code/SKILL.md`；连接器源码 `paper_search_mcp/academic_platforms/*.py`；能力矩阵/键表见 repo `README.md`
- 什么时候用：**多库并发检索 + 去重**（`search_papers`）、**DOI→OA PDF 回退下载**（`download_with_fallback`）、按引文数/日期排序、批量下载 DOI 清单；不想自己逐个 API 拼管道时
- 怎么取：CLI，先装一次。
```bash
uv tool install paper-search-mcp            # 或 uvx paper-search-mcp（免安装）
paper-search search "基层治理" -s all -n 20                       # 默认 broad
paper-search search "gender imbalance neuroscience" -s fast -n 3   # fast=OpenAlex+Crossref+arXiv+PubMed+EuropePMC
paper-search search "transformer attention" --sources arxiv,semantic --sort citations
paper-search download semantic DOI:10.1038/s41593-020-0658-y -o ./downloads
paper-search tool --list                    # 列出全部底层 MCP 工具与 schema
```
MCP 模式：`{"command":"uvx","args":["paper-search-mcp"]}`（stdio；亦支持 sse / streamable-http，默认只绑 `127.0.0.1`）。可选键放 `~/.config/paper-search-mcp/.env`（统一前缀 `PAPER_SEARCH_MCP_`）。
- **PDF 下载链**（`download_with_fallback`，逐级回退）：源站直链 → OpenAIRE / CORE / Europe PMC / PMC 发现 → **Unpaywall** 按 DOI 解析 → （显式开启才用）Sci-Hub。另：`extract_sections` 只对本地下好的 PDF 分节；arXiv 下载校验裸 ID、限 100MiB、查 `%PDF` 头
- 覆盖：2 亿+ 国际文献（Semantic Scholar/OpenAlex 口径）。更新随上游。许可：**MIT**（Python 3.10+）
- 门槛：多数源免 key；**Unpaywall 必须 email**（`..._UNPAYWALL_EMAIL`，否则整源被跳过）；IEEE Xplore（需 key，仅元数据）与 CORE（全文需免费 key）；MCP 默认只绑 `127.0.0.1`
- 实测：2026-10-02，macOS + curl（未安装/未运行本工具，按纪律只探其上游端点）——OpenAlex、Crossref、Semantic Scholar、Europe PMC、arXiv、PubMed、BioStudies、Zenodo 均 `HTTP 200` 返回预期结构；**CORE `https://api.core.ac.uk/v3/search/works?q=organoid` 无 key → `HTTP 429`**（印证"要 key"）；OpenAIRE 搜索 `200`。**工具本体与其 MCP 接口未本机实测（上游声明）**
- 上游：`https://github.com/openags/paper-search-mcp`（MIT）；同类 365-skills `paper-fetch` 见下「细节」

## 细节

### 源清单（28 个连接器）

| 类 | 源 |
|---|---|
| 元数据骨干 | Crossref、OpenAlex、Semantic Scholar、dblp、CiteSeerX、SSRN(OpenAlex 元数据)、Unpaywall(DOI 查 OA) |
| 学科专属 | arXiv、PubMed、PMC、Europe PMC、IACR ePrint、chemRxiv |
| OA 全文 | arXiv、PMC、CORE、OpenAIRE、DOAJ、BASE、Zenodo、HAL、bioRxiv、medRxiv |
| 发现/DOI 回填 | Google Scholar（仅发现，不作权威源）、OpenReview(匿名 v2)、ACM DL(Crossref `10.1145` 前缀) |
| 需 key/受限 | IEEE Xplore（需 key，仅元数据）、Unpaywall（**必须** `..._UNPAYWALL_EMAIL`）、CORE（全文需免费 key） |
| 可选合规外 | Sci-Hub（默认关，`use_scihub=true` 才用） |

上游自测能力矩阵要点：arXiv/bioRxiv/medRxiv/IACR/Zenodo/HAL `搜+下+读` 全 ✅；PMC/Europe PMC 仅 OA 部分 ✅；Crossref/OpenAlex/dblp/PubMed 搜索 ✅ 但下载 ❌；Google Scholar ⚠️（上游 bot 限流/CAPTCHA，失败会显式报错并 60s 起指数冷却至多 15min，**不代替解验证码**）；CORE 无 key 常 500/超时；BASE 的 OAI-PMH 需机构 IP 注册，否则优雅返回空。

### 同类参考：Agents365 `paper-fetch` 的 7 源下载链（另一条"DOI→PDF"路线）

若只想要**纯 stdlib 的单文件下载器**（无需装包），用 365-skills 的 `paper-fetch`（MIT，`plugins/paper-fetch/skills/paper-fetch/scripts/fetch.py`）。固定回退顺序：**Unpaywall**（`api.unpaywall.org/v2/{doi}?email=`，读 `best_oa_location.url_for_pdf`）→ **Semantic Scholar**（`openAccessPdf`）→ **arXiv**（由 `externalIds.ArXiv` 拼 `arxiv.org/pdf/{id}.pdf`）→ **PMC**（`ncbi.nlm.nih.gov/pmc/articles/{pmcid}/pdf/`）→ **bioRxiv/medRxiv**（DOI 前缀 `10.1101`，查 `api.biorxiv.org/details/{server}/{doi}`）→ **出版社直链**（`PAPER_FETCH_INSTITUTIONAL=1` 才开，用机构 IP/Cookie 授权 + 1 req/s 限速）→ **Sci-Hub 镜像**（**默认开**，`PAPER_FETCH_NO_SCIHUB=1` 关；默认镜像 `sci-hub.ru/.st/.su/.box/.red/.al/.mk/.ee`）。逐级 `%PDF` 魔数 + 50MB 上限校验，SSRF 防护；`--title` 走 Crossref→S2 解析 DOI；`--batch dois.txt`/`--stream`；退出码 0/1(未找到 OA)/3(参数错)/4(传输错)；可选 `PAPER_FETCH_CLOAK=1` 用 stealth Chromium 过 Cloudflare（仅操作者可开）。其 `semanticscholar-skill` 则封装 S2 三类端点：`api.semanticscholar.org/graph/v1`（检索/引文/作者）、`/recommendations/v1`（推荐）、`/datasets/v1`（快照 dump，供批量）。

## 坑

- Google Scholar/SSRN/ACM 依赖代理与出版社策略。
- PMC/Europe PMC 直下 PDF 在本机代理环境可能 `ProxyError`；Semantic Scholar 匿名 429；OpenAlex 匿名有日配额。
- **Unpaywall 无 email 则整源被跳过**；`dois` 里的 DOI 不会自动追加其它源。
- 人工核对不要把它当"全库穷尽"。
