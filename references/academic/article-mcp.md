# article-mcp —— 期刊分级与影响因子核验

一个 MCP 文献服务器，价值不在"检索"（它复用的都是本层已有的 Europe PMC/PubMed/arXiv/CrossRef/OpenAlex），而在 **`get_journal_quality` 工具把中国的 EasyScholar 分级（影响因子、SCI 分区、中科院分区/TOP、JCI）接进来**。要判"这个刊是不是 CSSCI/北大核心/中科院一区"，用这条线（另一条免 key 线是 OpenAlex 的 h 指数/引用，或本层 `ncpssd.org.md` 行内 `range` 字段、维普结果页标记）。

- 去哪找：repo `https://github.com/gqy20/article-mcp`（1.7MB，MIT）；EasyScholar 官方 API 文档 `https://www.easyscholar.cc/open/getPublicationRank`；密钥在 `https://www.easyscholar.cc` 注册获取；同类可选（Agents365 的 365-skills）见下「细节」
- 什么时候用：**期刊分级**（"这个刊几区/影响因子多少/是不是 TOP"）→ EasyScholar；**免 key 的粗略影响力** → OpenAlex；**期刊缩写（ISO 4 / MEDLINE）** → journal-abbrev；**一篇论文的全量元数据（含 IF、通讯作者）** → journal-meta
- 怎么取：
  ```bash
  # EasyScholar：GET，secretKey + publicationName，限 2 req/s
  curl -s "https://www.easyscholar.cc/open/getPublicationRank?secretKey=<KEY>&publicationName=Nature"
  # 无 key 也返回 200，但 body 报错（见实测）
  uvx article-mcp                 # 跑 MCP 服务器；env EASYSCHOLAR_SECRET_KEY=<KEY>
  # 免 key 替代（365-skills，纯 stdlib，离线可跑）：
  python3 journal_if.py lookup "Nature Medicine"   # 内置 CSV ≈249 刊 → OpenAlex 兜底；--offline 可断网
  python3 jabbrv.py "Journal of the American Chemical Society"   # JabRef → ISO 4 → NLM 缩写
  ```
- 覆盖：EasyScholar 覆盖主流 SCI/SSCI/中文核心期刊的分级指标；OpenAlex 兜底 h 指数/引用。更新随 EasyScholar 年度更新。许可：article-mcp = **MIT**
- 门槛：**EasyScholar 必须密钥**（无 key 只会返回错误码 40005）；官方接口**限速 2 req/s**（批量要 `sleep 0.5`）；**要联网到 easyscholar.cc**；article-mcp 依赖 `aiohttp`（`uv sync`）
- 实测：2026-10-02，macOS + curl：
  - `https://www.easyscholar.cc/open/getPublicationRank?publicationName=Nature`（**不带 key**）→ **`HTTP 200`，body `{"code":40005,"msg":"密钥不能为空","data":null}`** —— 印证"HTTP 200 假成功、必须 key"。
  - OpenAlex（其 OpenAlex 兜底源）`https://api.openalex.org/works/doi:10.1038/s41586-021-03819-2` → `HTTP 200`（`W3177828909`）。
  - **article-mcp 本体与 `uvx` 启动未本机实测**（上游声明）；EasyScholar 带真实 key 的分级返回未验证。
- 上游：`https://github.com/gqy20/article-mcp`（MIT）；EasyScholar API `https://www.easyscholar.cc/open/getPublicationRank`；同类 `https://github.com/Agents365-ai/365-skills`（`plugins/journal-if`、`journal-abbrev`、`journal-meta`，MIT）

## 细节

- **EasyScholar 字段映射**：`sciif`→影响因子、`sci`→SCI 分区(Q1–Q4)、`jci`→JCI、`sciUp`→中科院升级版分区、`sciBase`→中科院基础版分区、`sciUpSmall`→升级版小类、`sciUpTop`→升级版 TOP。
- **article-mcp 的 5 个工具**：`search_literature`（多源检索）、`get_article_details`、`get_references`、`get_literature_relations`、`get_journal_quality`（EasyScholar + OpenAlex 双源，带本地缓存与批量评估）。
- **同类可选**（Agents365-ai/365-skills，MIT）：`journal-if`（内置 CSV 约 249 刊 + OpenAlex 兜底，`--offline` 可离线）、`journal-abbrev`（JabRef 约 2.5 万刊 → AbbrevISO(ISO 4) → NLM Catalog(MEDLINE) 级联）、`journal-meta`（OpenAlex 主 + Crossref 备，一次给出 IF/通讯作者/卷期页）。

## 坑

- 期刊质量数据缺失基本都是没配 key；EasyScholar 无 key 时是 **HTTP 200 假成功**（body 报 40005），别只看状态码。
