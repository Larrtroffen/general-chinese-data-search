# gov-policy-mcp —— 政策检索封装三件套

三个第三方「中国政府网政策检索」实现的合并卡：**只记录它们支持的站点清单与接口要点**，供我们要自建检索时抄接口、抄站点白名单。**均未本机运行其代码**（未装依赖、未启动 MCP），仅做源码/README 阅读 + 对 gov.cn 官方接口自行 curl 验证。

- 去哪找：
  - 源 1：`https://github.com/guangxiangdebizi/China-Central-Policy-MCP`（Node/TS，stdio MCP）
  - 源 2：`https://github.com/wenyi3370-lgtm/chuance-policy-mcp`（Python MCP）
  - 源 3：`https://github.com/steambreadcuiyao/govcn-policy-query`（纯 Skill）
  - 官方数据入口：`GET https://sousuo.www.gov.cn/search-gov/data`（三源共同依赖；详见 `gov.cn.md`）
- 什么时候用：
  - 要**最省事地检索国务院政策全文**（关键词 + 日期 + 文号/发文机关）→ 抄 `中国中央政策 MCP` 的接口参数。
  - 要**站点白名单**（`site:` 定向哪几个权威站）→ 抄 `川策智行` 的 `SITE_SCOPES`。
  - 要**浏览器渲染版的政策文件库检索页 URL 形态** → 抄 `govcn-policy-query` 的 `policyDocumentLibrary`。
  - 不适用的场景：要非政策类数据 → 各自引用的只有政策站，见 `china-policy-sites.md`。
- 怎么搜：抄各源的接口参数（见 `## 细节` 逐源）。核心是 gov.cn `search-gov/data` 的 `t` 参数：
  - 综合检索直接用 `t=zhengcelibrary` 遍历 `catMap` 合并即可（`gov.cn.md` 已给完整模板）；想分桶用 `_gw`/`_bm`。
  - 三家对 `t` 取值不一致，源 2 的"`zhengcelibrary` 恒为空"是**误读**（它读的是顶层 `searchVO.listVO`，恒空），非 `catMap.*.listVO`。
- 覆盖：中国政府网政策文件库（三源共同覆盖）；源 2 另含国家法律法规数据库 `flk.npc.gov.cn`、国家数据局 `nda.gov.cn`、四川省 `sc.gov.cn`、国家发改委 `ndrc.gov.cn`、财政部 `mof.gov.cn`、中国人民银行 `pbc.gov.cn`、成都相关站（非国务院站走 Bing/百度 `site:` 定向 + 域名白名单过滤）；源 3 仅 gov.cn。
- 门槛：免费、无 API Key；源 1 Apache-2.0、源 2 MIT、源 3 无 LICENSE；需自备运行环境（Node/TS 或 Python≥3.10 / Agent Browser）；**本机均未运行其代码**。
- 实测：2026-10-02。raw/源码阅读三个 repo（未运行其代码）；gov.cn 接口 `t` 参数四值 curl 实测（见下表）；`https://sousuo.www.gov.cn/zcwjk/policyDocumentLibrary?t=zhengcelibrary&q=人工智能` → 200；`https://sousuo.www.gov.cn/zcwjk/advanceSearchPage` → 200。其余站点（nda.gov.cn/sc.gov.cn/flk.npc.gov.cn 等）**未逐一验证，上游声明**。
- 上游：<https://github.com/guangxiangdebizi/China-Central-Policy-MCP>、<https://github.com/wenyi3370-lgtm/chuance-policy-mcp>、<https://github.com/steambreadcuiyao/govcn-policy-query>

## 细节

### 源 1：guangxiangdebizi/China-Central-Policy-MCP（Apache-2.0）

- repo：`https://github.com/guangxiangdebizi/China-Central-Policy-MCP`（Node/TS，stdio MCP）
- **支持站点**：仅 `sousuo.www.gov.cn`（国务院政策文件库）+ `www.gov.cn` 正文页。数据入口 `https://www.gov.cn/zhengce/zuixin/`。
- 工具：`get_latest_policies`（检索列表）、`get_policy_fulltext`（按 URL 抽正文）。
- **接口要点**（`src/tools/getLatestPolicies.ts`）：`GET https://sousuo.www.gov.cn/search-gov/data`，参数 `t=zhengcelibrary_gw_bm_gb`、`q=<kw>`、`searchfield=title:content:summary`、`sort=score`、`sortType=1`、`p=1`、`n=100`、`timetype=timezd`、`mintime`/`maxtime`（`YYYY-MM-DD`）；头：桌面 UA + `Referer: https://sousuo.www.gov.cn/`；只请求第 1 页（不翻页）。解析：读 `searchVO.catMap.*.listVO`（README 自述兼容旧式 `results`）；输出 `policy_id/title/level/category/date/url/summary/issuing_agency/document_number/catalog`。
- 依赖：`@modelcontextprotocol/sdk@0.6.0`、`axios`、`cheerio`；`npm install && npm run build` 后 `node build/index.js`。
- 限制：README 声明仅供学习/研究，不得商业化或大规模抓取。

### 源 2：wenyi3370-lgtm/chuance-policy-mcp（MIT，Python）

- repo：`https://github.com/wenyi3370-lgtm/chuance-policy-mcp`（`mcp`+`httpx`+`beautifulsoup4`+`lxml`，需 Python≥3.10）
- **支持站点**（`source_catalog()` / `SITE_SCOPES`）：中国政府网政策文件库（官方接口）、国家法律法规数据库 `flk.npc.gov.cn`、国家数据局 `nda.gov.cn`、四川省 `sc.gov.cn`、国家发改委 `ndrc.gov.cn`、财政部 `mof.gov.cn`、中国人民银行 `pbc.gov.cn`、成都相关 `chengdu.gov.cn`/`cddata.gov.cn`/`gxt.sc.gov.cn`。非国务院站一律走 **Bing/百度 `site:` 定向 + 域名白名单过滤**。
- 工具：`search_gov_policy`、`fetch_page_text`、`verify_law_article_tool`（法名+条号核验原文）、`batch_verify_citations`、`check_freshness`、`source_catalog`。
- **接口要点**（`clients.py`）：官方接口同上 `sousuo.www.gov.cn/search-gov/data`，但**主张拆两桶**：`t=zhengcelibrary_gw`（国务院文件）+ `t=zhengcelibrary_bm`（部门文件）合并去重；注释称 `t=zhengcelibrary`（综合）"恒为空"。参数另有 `bmfl=""`、`inpro=""`；`searchfield` 默认 `title`。命中字段取自 `wenhao`（文号）、`shixiao`（时效性）、`pubtimeStr`、`pubtime`。正文抽取：`_parse_best` 用 lxml，遇到 gov.cn 正文挂在 body 之外的畸形 HTML 会丢节点 → 回退 html.parser。
- 运行：`uvx --from git+https://github.com/wenyi3370-lgtm/chuance-policy-mcp chuance-policy-mcp`（stdio）；或 `--http --port 8931`（端点 `/mcp`）。无需 API Key。
- 环境变量：`CHUANCE_TIMEOUT`(20s)、`CHUANCE_MAX_CHARS`(6000)、`CHUANCE_PROXY`（默认**不**用系统代理）。

### 源 3：steambreadcuiyao/govcn-policy-query（无 LICENSE，纯 Skill）

- repo：`https://github.com/steambreadcuiyao/govcn-policy-query`（只有 `SKILL.md`+`README.md`，WorkBuddy 平台技能）
- **支持站点**：仅中国政府网政策文件库。**URL 形态**（实测 200，见下）：
  - 检索页：`https://sousuo.www.gov.cn/zcwjk/policyDocumentLibrary?t=zhengcelibrary&q=<URL编码>`
  - 高级检索页：`https://sousuo.www.gov.cn/zcwjk/advanceSearchPage`（字段 title/content/puborg/pubdate/docno）
  - 正文页：`https://www.gov.cn/zhengce/zhengceku/YYYYMM/content_*.htm`
- 依赖：**Agent Browser**（`agent-browser`）驱动真实浏览器——其 README 明确「JS 动态渲染，不能用 WebFetch 直取搜索结果」。
- 限制：无 license；须浏览器自动化，成本高；仅覆盖 gov.cn。

### 交叉发现：gov.cn 检索 API 的 `t` 参数（本机实测）

**本机 curl 实测（2026-10-02，`q=人工智能`，`n=3`）**：

| `t` 值 | 顶层 `searchVO.totalCount` | `catMap` 命中 | 结论 |
|---|---|---|---|
| `zhengcelibrary` | 0（**恒 0，别用顶层**） | gongwen 742 / bumenfile 2000 / otherfile 2381 / gongbao 1879 | ✅ 可用，结果在 `catMap.<类>.listVO` |
| `zhengcelibrary_gw` | 742 | 仅 gongwen | ✅ 单桶可用 |
| `zhengcelibrary_bm` | 2000 | 仅 bumenfile | ✅ 单桶可用 |
| `zhengcelibrary_gw_bm_gb` | 0 | gongwen / bumenfile / gongbao（无 otherfile） | ✅ 可用 |

- 源 2 所谓"恒为空"是**误读**：它读的是顶层 `searchVO.listVO`（恒空），而非 `catMap.*.listVO`。与 `gov.cn.md` 的结论一致。

## 坑

1. 三源均未本机运行，参数与端点属「源码/README 阅读」结论，取用前先自测。
2. 顶层 `totalCount` 恒 0，别据此判定空结果（见 `gov.cn.md` 坑 1）。
3. 源 1 只取第 1 页；源 2 的 lxml 解析对畸形 HTML 会丢节点（回退 html.parser）。
4. 源 3 依赖 Agent Browser，成本高且无 license。
