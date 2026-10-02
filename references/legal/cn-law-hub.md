# cn-law-hub —— 十官方源法律法规检索

把**十个官方法律/法规/规章/条约/政策源**封装成脚本 + Skill 的仓库：主打「法条级」检索、效力状态核验、原文下载与批量采集。适合作为跨源"总路由"参考（我们自己的源卡覆盖其端点的细节）。

- 去哪找：`https://github.com/ZongziForu/cn-law-hub`
  - 上游仓内：`SKILL.md`（源清单 + 路由规则）、`scripts/*.py`、`references/api_reference.md`（flk 端点）、`references/{page_structure,batch_collection}.md`
  - 许可：仓库有 `LICENSE` 文件（GitHub 识别 NOASSERTION，含 `LICENSE-APACHE` + `NOTICE`，实为 Apache-2.0 系）——引用请以仓库文件为准。
- 什么时候用：
  - 需要在**多个官方源之间选路**（法规 / 部门规章 / 条约 / 国务院政策 / 党内法规 / 国防 / 税务 / 生态环境 / 法院发布），并按法条级检索或批量下载。
  - 需要"效力状态必须由官方字段给出、不得推断"的核验口径与输出模板。
- 怎么取：
  ```bash
  git clone https://github.com/ZongziForu/cn-law-hub && pip install -r requirements.txt
  python scripts/download.py --search "物业管理条例" --exact --download   # flk 精确检索+下载
  python scripts/download.py --preview <bbbs>                             # 目录概览
  python scripts/download.py --article <bbbs> "第三十八条"                 # 单条
  python scripts/article_search.py "从业禁止" --max-laws 20               # 跨法条检索
  # 各脚本通用 flags：--search/--info/--size/--output/--rate-limit/--no-cache/--cache-stats
  ```
- 覆盖：10 个官方源（见「细节」表）；法条级（`--article "第X条"`、`--grep`）；结果缓存（搜索 1h / 详情 24h / DOCX 7d）+ 自动限速（≤10 请求 off，11–100 固定 5 req/s，>100 自适应 1–8 req/s）。
- 门槛：免费；仓库脚本依赖第三方安装（本次按纪律未执行/未装依赖）；各源可用性单独实测（见 `- 实测`）。
- 实测：2026-10-02，macOS，curl 8.x，UA=Chrome/120。源可达：`flk` 200/552B、`gov.cn` 规章库 200/21KB、`treaty.mfa.gov.cn` 200/7KB、`sousuo.www.gov.cn/search-gov/data` 200/52KB、`xzfg.moj.gov.cn` 200/52KB、`www.12371.cn` 200/144KB、`fgk.chinatax.gov.cn` 200/50KB、`mee.gov.cn` 200/203KB；`court.gov.cn` **301**（跳转）；`mod.gov.cn` **HTTP 000**（本机超时/TLS 不通）。flk 额外端点：`index/aggregateData` 200/3,444B；`prompts/search?title=民法` 200/444B；`search/hitDisplay`（GET）→ `{"msg":"Request method 'GET' not supported"}`；`search/xgzlDetails?id=…` → `{"msg":"Required request parameter 'bbbs' …"}`。
- 上游：`https://github.com/ZongziForu/cn-law-hub`

## 细节

### 十个官方源（脚本 / 源站 / 方式）

| # | 数据库 | 脚本 | 源站 | 方式 |
|---|---|---|---|---|
| 1 | 国家法律法规数据库 | `download.py` | `flk.npc.gov.cn` | JSON API |
| 2 | 国家规章库 | `gov_rules_crawler.py` | `gov.cn/zhengce/xxgk/gjgzk` | Athena API + HTML |
| 3 | 外交条约库 | `treaty_crawler.py` | `treaty.mfa.gov.cn` | HTML |
| 4 | 国务院政策文件库 | `gov_policy_library.py` | `sousuo.www.gov.cn` | REST GET |
| 5 | 司法部行政法规库 | `moj_law_crawler.py` | `xzfg.moj.gov.cn` | HTML |
| 6 | 党内法规库 | `party_law_crawler.py` | `www.12371.cn` | HTML |
| 7 | 国防部法规文库 | `mod_law_crawler.py` | `www.mod.gov.cn` | HTTP |
| 8 | 税务法规库 | `tax_law_crawler.py` | `fgk.chinatax.gov.cn` | REST POST（session cookie） |
| 9 | 生态环境部法规规章 | `mee_law_crawler.py` | `mee.gov.cn` | HTML |
| 10 | 最高人民法院发布栏目 | `court_law_crawler.py` | `court.gov.cn` | HTML |

另有 `article_search.py`（跨法条级检索）、`region_classifier.py`（省/市分类）。

### flk 端点补充（上游仓内 `references/api_reference.md`）

- 该文档记录：`/law-search/index/aggregateData`、`/law-search/search/hitDisplay`、`/law-search/search/xgzl`、`/law-search/download/batch`、`/law-search/prompts/search`；并称 `orderByParam.sort` 可取 `gbrq`/`sxrq`/`sxx`/`flxz`/`zdjg`。
- 可用：`GET /law-search/prompts/search?title=<词>` **200**，返回补全候选（`titleHighlight` 带 `<em>`）。
- 可用：`GET /law-search/index/aggregateData` **200**（3,444 B，分类统计/推荐）。

## 坑

1. **文档里的端点已部分失效（实测）**：`search/highSearch`、`search/suggest` 现已 404；`search/xgzl`、`download/batch` 用文档给的 body 返回 `code:500`。flk 现行端点名请以 `flk.npc.gov.cn.md` 为准（`highSearch/highSearch`、`search/xgzlDetails`（参数名 `bbbs`）、`search/xgwjDetails`、`search/hitDisplay`（POST-only））。
2. **效力状态口径**：仅当官方页面/API 明确给出时才可标"现行有效/已废止/已修改/尚未生效"，否则写"官方页面未明确标注效力状态"。
