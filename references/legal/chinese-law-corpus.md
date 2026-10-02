# chinese-law-corpus —— 法条案例逐条离线语料

把 flk 官方 docx 与最高法案例解析成干净 JSON 的开源语料库：**446 部法律/司法解释（逐条，26,000+ 条）+ 278 件指导性案例 + 445 件公报案例**，带效力状态与公布/施行日期。含配套只读 MCP。

- 去哪找：
  - 仓库：`https://github.com/lttxzmj/chinese-law-corpus`（克隆或按需取件）
  - **jsDelivr CDN（推荐，免鉴权/CORS/HTTPS）**：`https://cdn.jsdelivr.net/gh/lttxzmj/chinese-law-corpus@master/<path>`
  - raw：`https://raw.githubusercontent.com/lttxzmj/chinese-law-corpus/master/<path>`
  - 目录：`laws/index.json`（446 部索引：slug/title/articleCount）、`laws/<slug>.json`（单部逐条）、`guiding-cases/guiding-<n>.json` + `manifest.json`、`gazette-cases/gazette-<年>-<期>-<hash>.json`
  - 配套 MCP：`https://github.com/lttxzmj/chinese-law-mcp`（`search_laws` / `get_article` / `search_in_law`，只读 CDN）
- 什么时候用：
  - 要**法条逐条原文 / 离线 / 可入库**：精确到「第 X 条」的文本、做 RAG 切块、citation-grounded 生成。
  - 要**稳定跨版本条号**（如 `civil-code-0577` = 民法典第 577 条）而非网页抓取。
  - 要**指导性/公报案例文本**做批量分析（时效要求不高时）；要最新、要原文核验请回 flk / 官网。
- 怎么取：
  ```bash
  # 索引（446 部）
  curl -s 'https://cdn.jsdelivr.net/gh/lttxzmj/chinese-law-corpus@master/laws/index.json'
  # 民法典全文（逐条）
  curl -s 'https://cdn.jsdelivr.net/gh/lttxzmj/chinese-law-corpus@master/laws/civil-code.json'
  # 取单条：民法典第 577 条
  curl -s '.../laws/civil-code.json' | jq '.articles[] | select(.id=="civil-code-0577")'
  # 指导性案例 / 公报案例（按文件名，见 manifest）
  curl -s 'https://cdn.jsdelivr.net/gh/lttxzmj/chinese-law-corpus@master/guiding-cases/guiding-1.json'
  ```
  MCP 配置：`{"mcpServers":{"chinese-law":{"command":"npx","args":["-y","github:lttxzmj/chinese-law-mcp"]}}}`
- 覆盖：
  - `laws/`：446 部（法律 313 + 司法解释 133；含 4 部已公布尚未生效）＝447 个 blob 去掉 `index.json`。
  - `guiding-cases/`：278 件（279 blob 去掉 `manifest.json`）；`gazette-cases/`：445 件。
  - 更新：法律季度更新，案例随官方发布；仓库 2026-09-29 有提交。
- 门槛：许可 **CC0 1.0**（整理/结构化部分，可商用免署名）；法条与司法文书依《著作权法》第五条不受著作权保护。非官方整理，正式引用以 flk / 最高法公布文本为准；**无地方性法规**；无裁判文书网全量（只有指导性 + 公报案例）。全量约 8.5 MB，按需 CDN 取件即可；`@master` 可换 commit/tag 锁定版本。
- 实测：2026-10-02，macOS，curl 8.x。① `GET laws/index.json` → **HTTP 200**，111,296 B（JSON 数组，含 slug/title/articleCount）。② `GET laws/civil-code.json` → **HTTP 200**，671,072 B；`articleCount=1260`、`len(articles)=1260`；`articles[576].id="civil-code-0577"`，`text` 为民法典第 577 条原文；顶层 `status="effective"`。③ `GET guiding-cases/manifest.json` → **HTTP 200**，`caseCount=278`，`source=https://www.court.gov.cn/shenpan/gengduo/77.html`，`generatedAt=2026-08-14`。④ `GET guiding-cases/guiding-1.json` → **HTTP 206**（range 截取）；`GET LICENSE` → **HTTP 200**（CC0 全文）。
- 上游：`https://github.com/lttxzmj/chinese-law-corpus` ｜ MCP：`https://github.com/lttxzmj/chinese-law-mcp`

## 细节

### 结构（实测字段，README 示例已过时）

- `laws/*.json`：`id / officialId / title / category / issuingAuthority / promulgationDate / effectiveDate / status / paragraphCount / sectionCount / articleCount / sections[] / articles[]`
- `articles[]`：`{id, articleNumber, displayNumber, path[], text, order}`（`path` = 编/章/节；`status="effective"` 等英文枚举）
- `guiding-cases/guiding-<n>.json`：`number / title / keywords[] / gist[] / facts[] …`；`manifest.json` 含 `caseCount=278` 与 `source`（`court.gov.cn/shenpan/gengduo/77.html`）
- `gazette-cases/*.json`：公报裁判文书正文 + 客观元数据（**不含**编辑加工的「裁判摘要」）
- README 里的 JSON 示例与真实字段不一致（`status` 实际是英文 `effective`），已按实测更正。
