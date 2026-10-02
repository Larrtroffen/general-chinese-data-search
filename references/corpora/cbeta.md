# cbeta —— 中华电子佛典（汉文大藏经语料）

- 去哪找：在线全文阅读/检索 `https://cbetaonline.dila.edu.tw/`；**API**（Swagger）`https://cbdata.dila.edu.tw/stable`；XML 全集 `https://github.com/cbeta-org/xml-p5`；目录/缺字/作译者 metadata `https://github.com/DILA-edu/cbeta-metadata`；API 源码（含 MCP server）`https://github.com/DILA-edu/cbeta-api`。
- 什么时候用：做**佛教/宗教研究、中古汉语、古籍文本挖掘**；要**大藏经全文**（大正藏等历代藏经）而非单纯古籍；要**结构化 XML（TEI 式 P5）**做标注/检索/训练；要**缺字、作译者、朝代**等 metadata。
- 怎么取：
  ```bash
  # 在线：直接浏览器检索即可
  # XML 全集（约 1.4 GB，仓内 .xml 逐部）
  git clone --depth 1 https://github.com/cbeta-org/xml-p5
  # 元数据
  gh api repos/DILA-edu/cbeta-metadata/contents --jq '.[]|[.name,.type,.size]|@tsv'
  # API：Swagger UI 在 https://cbdata.dila.edu.tw/stable （v4.6.7）
  ```
- 覆盖：CBETA（中华电子佛典协会）汉文大藏经全文：以《大正新修大藏经》为主，并含历代藏经/新修续藏等，逐部 XML（含校勘、页行、缺字标记）；metadata 含**目类、部类、缺字、作译者、朝代**。规模与卷数以上游为准（未逐卷清点）。
- 门槛：**在线阅读免费**；XML 全集与 metadata 走 **GitHub**（免登录）；API 公开（无 key，实测可达）。**使用须遵守 CBETA 版权/引用条款**（见其站点公告）。
- 实测：2026-10-03，macOS arm64：`GET https://cbetaonline.dila.edu.tw/zh/` → **200** / 64,198 B，标题「CBETA 線上閱讀」；`GET https://cbdata.dila.edu.tw/stable` → **200**，页面标题「CBETA API 4.6.7」（Swagger）；`gh api repos/cbeta-org/xml-p5` → `size=1,448,704 KB`（≈1.38 GB）、无 license、`pushed 2026-09-05`；`gh api repos/DILA-edu/cbeta-api` → `pushed 2026-10-01`、README 确认含 **MCP Server**（`doc/mcp.md`）。
- 上游：CBETA 中华电子佛典协会 / 法鼓文理学院（DILA）。

## 细节

### 入口表

| 入口 | 地址 | 形态 |
|---|---|---|
| 在线阅读/全文检索 | `https://cbetaonline.dila.edu.tw/` | HTML（免登录） |
| API / Swagger | `https://cbdata.dila.edu.tw/stable` | JSON API，v4.6.7 |
| XML 全集（P5） | `https://github.com/cbeta-org/xml-p5` | ~1.4 GB 逐部 XML |
| 目录/缺字/作译者 metadata | `https://github.com/DILA-edu/cbeta-metadata` | CSV/JSON |
| API 源码 + MCP server | `https://github.com/DILA-edu/cbeta-api` | Ruby on Rails |

基于 CBETA 的第三方检索：DeerPark 汉文大藏经、RuShiWoWen 如是我闻（公开全文检索）、cbetar2 阅读器（上游 README 列出）。

## 坑

1. **版权/引用条款**：CBETA 语料有专门的使用声明，正式引用/再分发前必读官网公告；XML 仓**无 SPDX license**。
2. 与通用古籍库（`../archives/daizhige.md`、`../archives/ctext.md`、`../archives/kanripo.md`）分工：**佛典优先用 CBETA**（校勘与结构化最好），经史子集用那三者。
3. XML 全集体量约 1.4 GB，**别整包 clone 进工作区**；按需取分部文件或走 API。
4. API 有版本号（`stable`/`v1` 等），旧教程里的端点可能已变，以 Swagger 为准。
