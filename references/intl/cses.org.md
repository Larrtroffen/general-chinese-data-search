# cses.org —— 选举制度比较研究

- 去哪找：门户 `https://cses.org/`；数据下载 `https://cses.org/data-download/`；选举研究清单 `…/data-download/download-data-documentation/election-studies/`；变量总表 `…/variable-table/`；桥接变量 `…/data-bridging/`。
- 什么时候用：要**选举层面的个体投票行为**（投票选择、政党认同、左右自我定位、政治效能、领袖评价、议题立场）；把全国选举调查与**选区/政党制度**变量拼起来；做比较选举研究。
- 怎么取：
  - `/data-download/` 提供各 Module（M1 1996–2001 → M5 2016–2021+）与整合文件，SPSS/Stata/CSV；需注册并同意条款。
  - 变量跨模块映射看 `/variable-table/`；跨模块比较用官方 `/data-bridging/` 变量。
  - 部分版本另发在 Harvard Dataverse / GESIS。
- 覆盖：1996–至今，Module 1–5，50+ 国家、200+ 次选举；个体级（选民）+ 选举级别；约 5 年一模块（上游声明，未本机实测）。
- 门槛：免费；**注册 + 同意数据使用条款后下载**。
- 实测：2026-10-03，macOS arm64，curl 8.x：`https://cses.org/data-download/` → 200 / 78 KB；页内实测含 `/data-download/download-data-documentation/election-studies/`、`…/variable-table/`、`/data-download/data-bridging/`、`/data-download/turnout-and-vote-choice-data-overview/` 等链接；本机未取到直接文件链接（下载需登录/表单）。
- 上游：`https://cses.org/`（CSES）。

## 坑

1. **微观投票数据受各国选举调查许可限制**，个别国家/模块需单独申请，不是一键全下。
2. CSES 的分析单位是**"选举"不是"国家-年"**；同一国家多年份对应多次选举，合并前先定单位。
3. 模块间变量名与量表会改版（如左右量表 0–10 vs 1–10），跨模块用官方 bridging 变量。
4. 选区层（constituency-level）数据在单独文件；个体层与选区层合并要按官方 ID 键。
5. 与 Comparative Study of Electoral Systems 同名的二手数据源很多，认准 `cses.org` 官方发布。
