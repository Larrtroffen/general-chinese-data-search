# paper-lookup —— 18 个学术 API 检索路由

免 key、可 curl 的**国际**学术检索通道总集。它本身是一份 skill 文档（不是数据集）：每个 API 一份 `references/<api>.md`，写明端点、参数、返回形状与**"HTTP 200 却失败"的坑**。凡"要国际库元数据/引文/OA 全文、又不想碰四大中文库"的活，先来这里挑通道。

- 去哪找：repo `https://github.com/k-dense-ai/scientific-agent-skills`（**仓库 462MB，勿全量克隆**）。SKILL.md：raw 路径 `https://raw.githubusercontent.com/k-dense-ai/scientific-agent-skills/main/skills/paper-lookup/SKILL.md`；单 API 参考：`.../skills/paper-lookup/references/<api>.md`（共 18 份）；无 gh 时用 `gh api repos/k-dense-ai/scientific-agent-skills/contents/skills/paper-lookup/references/<api>.md --jq .content | base64 -d`
- 什么时候用：要**免 key 国际库检索** → OpenAlex（全领域 2.5 亿+）/Crossref（DOI 元数据）/Europe PMC（生物医学+预印本）/Semantic Scholar（引文图、推荐）；要**OA 全文 PDF** → Unpaywall（按 DOI 给 `best_oa_location`）→ CORE / PMC / Europe PMC；要**引文边** → OpenCitations / Semantic Scholar；要**机构 ID** → ROR；要**撤稿核验** → Crossref `update-type:retraction`；要**生物医学实体标注** → PubTator3。中文库（知网/万方/维普）不在这里——见本层其余文件
- 怎么取：curl 直连，无需安装。

```bash
curl -s --get 'https://api.openalex.org/works' --data-urlencode 'search=基层治理' --data-urlencode 'per-page=10'
curl -s 'https://api.crossref.org/works/10.1038/s41586-021-03819-2'                 # DOI 元数据
curl -s 'https://api.unpaywall.org/v2/10.1038/s41586-021-03819-2?email=you@x.org'   # OA 状态/PDF
curl -s 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1038/nature12373?fields=title,year,citationCount,openAccessPdf'
curl -s --get 'https://www.ebi.ac.uk/europepmc/webservices/rest/search' --data-urlencode 'query=(SRC:"PPR" AND PUBLISHER:"bioRxiv" AND "organoid")' --data-urlencode 'format=json'
curl -s 'http://export.arxiv.org/api/query?id_list=1706.03762'                     # Atom XML，限 1 req/3s
```

- 覆盖：全学科国际文献；更新为各库自身节奏（Crossref/OpenAlex 近实时，预印本数小时）。许可：该 repo 为 **MIT**
- 门槛：多数 API 免 key（curl）即可；少数要 key/真实 email——CORE 全文与 Unpaywall（**要真实 email**）需凭证；各库有自身限速
- 实测：2026-10-02，macOS + curl（本机直连，无 key）——Crossref/OpenAlex/Semantic Scholar/Unpaywall(真邮箱)/Europe PMC/arXiv/DOAJ/Zenodo/ROR/PubMed esearch/BioStudies/OpenCitations(需 `-L` 跟随 301)/PubTator3/PMC efetch 全部 `HTTP 200` 且返回预期 JSON/XML；`CORE` → `429`（要 key）；`Figshare` GET **与 POST 均 `403`**（本机 IP 被挡，改用带 `Authorization: token` 或换出口）；`dblp`/`hal`/`base` 在本机被 bot 墙或超时（`HTTP 000`），非本表 18 源但常被同时提及。example.com 占位邮箱 → Unpaywall `422`（实测）
- 上游：`https://github.com/k-dense-ai/scientific-agent-skills`（子目录 `skills/paper-lookup/`，版本 2.4，2026-09-30 核对；MIT）

## 细节

### 源表（18 个 API：用途 / 端点 / 是否要 key）

| API | 用途 | 端点（基址） | key |
|---|---|---|---|
| PubMed | 3700 万+ 生物医学引文/摘要/MeSH（无全文） | `eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch\|esummary.fcgi?db=pubmed` | 否；`NCBI_API_KEY` 3→10 req/s |
| PMC | 1000 万+ 生物医学**全文 JATS XML** / ID 转换 | `eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id=` | 否（同上） |
| Europe PMC | PubMed+PMC+预印本一个索引；全文关键词检索、引文、诚实 404 | `www.ebi.ac.uk/europepmc/webservices/rest/search` | 否（全开放，连 email 都不要） |
| bioRxiv | 生物学预印本（**只能按日期/DOI，无关键词检索**） | `api.biorxiv.org/details/biorxiv/{doi}` | 否 |
| medRxiv | 医学预印本（同上，无关键词） | `api.biorxiv.org/details/medrxiv/{doi}` | 否 |
| arXiv | 物理/数学/CS/量化生物**预印本**，Atom XML | `export.arxiv.org/api/query` | 否（1 req/3s） |
| OpenAlex | 2.5 亿+ 作品/作者/机构/主题/引文，全领域 | `api.openalex.org/works` | 否；`OPENALEX_API_KEY` 抬配额 |
| Crossref | 1.5 亿+ DOI 元数据、期刊、基金、参考文献、撤稿 | `api.crossref.org/works/{doi}` | 否；带 `mailto` 进 polite pool |
| Semantic Scholar | 2 亿+ 论文、引文图、AI TLDR、推荐、批量快照 | `api.semanticscholar.org/graph/v1`、`/recommendations/v1`、`/datasets/v1` | 否（匿名常 429）；`S2_API_KEY` |
| OpenCitations | 开放引文边/计数（COCI、索引两套） | `opencitations.net/index/coci/api/v1/citations/{doi}` | 否（180 req/min/IP） |
| PubTator3 | 全文文本挖掘：基因/化学物/疾病/变异/关系 | `www.ncbi.nlm.nih.gov/research/pubtator3-api/publications/export/biocjson?pmids=` | 否（3 req/s） |
| CORE | 3700 万+ 跨库 OA 全文 | `api.core.ac.uk/v3/search/works` | **全文要 key**（免费注册） |
| Unpaywall | 任意 DOI 的 OA 状态与最佳 PDF 链接 | `api.unpaywall.org/v2/{doi}?email=` | **要真实 email**（占位邮箱 422） |
| DOAJ | 开放获取**期刊**目录及其注册文章 | `doaj.org/api/search/articles/{query}` | 否；key 抬限速 |
| Zenodo | 存档的论文/软件/数据（concept DOI ≠ version DOI） | `zenodo.org/api/records` | 否（30 req/min） |
| Figshare | 存档的图/数据/媒体（**搜索是 POST，不是 GET**） | `api.figshare.com/v2/articles/search` | 否 |
| BioStudies | EBI 研究包与跨库链接（ArrayExpress 等） | `www.ebi.ac.uk/biostudies/api/v1/search` | 否 |
| ROR | 机构名/署名串 → ROR ID | `api.ror.org/organizations?query=` | 否（2000 req/5min） |

标识符：DOI / PMID / PMCID / arXiv ID / OpenAlex `W…` / ORCID / ISSN / ROR / OCI / Zenodo record / BioStudies accession。跨库用前缀写法：Semantic Scholar 收 `DOI:`/`PMID:`/`ARXIV:`，OpenAlex 收 `doi:`/`pmid:`；PMID↔PMCID↔DOI 用 PMC ID Converter。

### 配套脚本（stdlib，Python 3.11+）

`scripts/paginate.py`（bioRxiv/medRxiv/EuropePMC/OpenAlex/Crossref 确定性翻页+计数核对，退出码 4=记录缺失）、`jats_to_text.py`（JATS→正文，退出码 2=无 `<body>`，即只有元数据没有全文）、`arxiv_atom.py`、`openalex_abstract.py`。

## 坑

**核心风险 = "HTTP 200 假成功"**：PMC eFetch 对不可再分发文章返回无 `<body>` 的 200；arXiv 参数错返回 `totalResults:1` 且条目名为 `Error`，未知字段前缀被静默改写成 `all:`；Europe PMC 把 `errCode` 藏在 200 body；bioRxiv 游标是**绝对偏移**，步长错会跳记录；Figshare `GET /articles?search_for=` **忽略查询仍 200**；OpenCitations 未知 DOI 返回 `[{"count":"0"}]`。判断"返回形状"而非状态码。
