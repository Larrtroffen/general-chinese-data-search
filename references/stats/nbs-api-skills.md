# nbs-api-skills —— NBS 新接口的两个 skill 实现

两家把 NBS 新版 API 封装成 skill 的仓库：`succ985/openclaw-akshare-skill` 与 `aahl/skills` 的 `cn-stats`（均 MIT）。**本卡只记它们相对 `data.stats.gov.cn.md` 的增量：新端点、请求头差异、可直接抄的 cid/daCid 常量。** 上游声明未本机逐条实测的，均标「未实测」。

- 去哪找：`https://github.com/succ985/openclaw-akshare-skill`；`https://github.com/aahl/skills` → `skills/cn-stats/SKILL.md`。
- 什么时候用：要给 NBS 新接口补端点/常量（关键词全局搜索、大中城市 daCid、住宅价格 cid）；或想要一份 akshare 用法摘要时。
- 怎么搜：见下 A（openclaw-akshare-skill）与 B（aahl cn-stats）——B 直接 curl NBS 新 `external` 接口，增量最多。
- 覆盖：NBS 新版 `external` 接口的增量端点与常量；B 另含取数主流程。
- 门槛：两个上游 repo 均 MIT；本项目未安装、未运行。
- 实测：2026-10-02，macOS arm64，curl 8.x：`GET …/external/query?search=CPI&pagenum=1&pageSize=15` → 200 `count=221`；`GET …/external/getDasByDaCatalogId?daCid=44016f1bffeb4ea49fe34e100c6415fb` → 200（首条 `110000000000 / 北京`）；`GET …/external/new/queryIndicatorsByCid?cid=3eb43764c74741469b745c396cf002d1` → 200 `total=35`。
- 上游：https://github.com/succ985/openclaw-akshare-skill ；https://github.com/aahl/skills → `skills/cn-stats/SKILL.md`。

## 细节

### A. succ985/openclaw-akshare-skill —— 面向 akshare 的通用技能（**未直接打 NBS 新接口**）

- 去哪找：`https://github.com/succ985/openclaw-akshare-skill`；入口 `SKILL.md`，细目（上游仓内）`references/akshare_api.md`、`references/common_functions.md`（scripts/ 里是 akshare 安装与示例脚本）。
- 内容：akshare 的用法摘要——A 股/港股/美股/期货/基金行情 + 宏观三件套 `ak.macro_china_gdp()`、`ak.macro_china_cpi()`、`ak.macro_china_pmi()`。
- 触发场景：用户问「中国股票/期货行情」「GDP/CPI/PMI」时。
- 与 NBS 的关系：**它不含 NBS 新接口的 curl 流程**，宏观走 akshare 的函数封装（口径见 `akshare.md`）。要用 NBS 官方数值请走 `data.stats.gov.cn.md` 或下节 B。
- 实测：2026-10-02 通读 `SKILL.md`（raw）；**未安装 akshare、未跑脚本**。

### B. aahl/skills 的 skills/cn-stats —— **直接 curl NBS 新 external 接口**（增量最多）

- 去哪找：`https://github.com/aahl/skills` → `skills/cn-stats/SKILL.md`（161★，MIT，2026-09 仍更新）。
- 触发场景：查 GDP/CPI/人口/房价指数等**国家统计局**数据。
- **比我们 `data.stats.gov.cn.md` 多出的端点/常量（沿用其 base）**：

  | 增量项 | 值 / 用法 | 我们的实测 |
  |---|---|---|
  | **关键词全局搜索** | `GET /query?code=&pagenum=1&pageSize=15` 且 `-G --data-urlencode 'search=<中文词>'`，带 `client: pc` 头；返回 `{types, count, data[]}`，每条含 `show_name/indic_id/type_text/da/dt/value/explain` | ✅ 200（见下） |
  | **大中城市 daCid** | `daCid=44016f1bffeb4ea49fe34e100c6415fb`（主要城市价格库的地区组） | ✅ 200，返回「北京/天津…」 |
  | 分省省份 daCid | `a10dceae75d245008bf4b9a0e6fe1d55`（与我们旧卡一致） | 已有卡已记 |
  | **住宅销售价格指数 cid** | `new/queryIndicatorsByCid?cid=3eb43764c74741469b745c396cf002d1`（70 大中城市） | ✅ 200，35 个指标 |
  | 多地区取数 | `stream/esData` 的 `showType` 用 **`"3"`**（我们旧卡记 `"1"`） | [INFERENCE] 未逐条实测差异 |
  | 请求头 | 发 `Referer: …/dg/website/page.html` + `Content-Type: application/json;charset=UTF-8` | 旧卡实测**不带** Referer 也通；带上更稳 |
  | `getDasByDaCatalogId` | 支持额外 `&rootId=$ROOT_ID` 参数 | ✅ 带/不带均可返回 |

- 取数主流程与字段解释与我们 `data.stats.gov.cn.md` 一致（`queryIndexTreeAsync` 下钻 → `queryIndicatorsByCid` → `stream/esData`）。
- 限制：SKILL.md 里写了 mcp-cnbs 文档提到的 `getEsDataByCidAndDt` 同名族端点**并未出现**；B 卡自身未给频率限制说明，仍按 ≤3 req/s 礼貌抓取。
- 实测（2026-10-02，macOS arm64，curl 8.x）：
  - `GET …/external/query?search=CPI&pagenum=1&pageSize=15` → **200**，`state=20000`，`count=221`，`data[]` 有记录。
  - `GET …/external/query?code=&pagenum=1&pageSize=15 --data-urlencode 'search=居民消费价格'` → 200，`count=237`。
  - 注意：`pageSize=2` 时**返回 `data:[]`（空）**——小 pageSize 可能取不到，稳妥用 15。
  - `GET …/external/getDasByDaCatalogId?daCid=44016f1bffeb4ea49fe34e100c6415fb` → 200，首条 `name_value=110000000000 / show_name=北京`。
  - `GET …/external/new/queryIndicatorsByCid?cid=3eb43764c74741469b745c396cf002d1` → 200，`total=35`。

### 选型（本项目）

- **要 NBS 月/季/年或分省数值** → 用 `data.stats.gov.cn.md` 的新接口；关键词定位优先用本卡的 `/query?search=`（比逐层翻树快）。
- **要现成 pandas / 行情类** → 参考 `akshare.md`；**要一句 curl 抄走** → 抄本卡 B。
- 三家对同一 NBS 库的 `code`（1–14）理解一致，可互相印证。
