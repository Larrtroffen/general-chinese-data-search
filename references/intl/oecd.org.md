# oecd.org —— 经合组织统计 SDMX API

- 去哪找：数据门户 `https://data-explorer.oecd.org/`；**SDMX REST** `https://sdmx.oecd.org/public/rest/v1/`。
- 什么时候用：OECD 国家 + 主要新兴经济体的可比社会/经济指标（就业、教育、税负、健康、创新、贸易、金融、福祉、环境）；要 SDMX 结构化、可脚本化的面板；做发达国家横向对比。
- 怎么搜：
  ```bash
  # ① 数据流目录（structure 格式名与数据格式不同！）
  curl -s 'https://sdmx.oecd.org/public/rest/v1/dataflow/all?format=json-structure-2.0.0'
  # ② 取数：{agency},{flow}@{df_id},{version}/{key}
  curl -s 'https://sdmx.oecd.org/public/rest/v1/data/OECD.SDD.STES,DSD_STES@DF_FINMARK,4.0/.?startPeriod=2024-01&format=jsondata'
  ```
  - 路径三段：`{agency},{dataflow}@{df_id},{version}/{key}`；`key` 里 `.` 分维度、`+` 多值、省略某段=该维度全选。
  - 数据参数：`startPeriod`/`endPeriod`、`firstNObservations=1`（只取最新一期）、`dimensionAtObservation=AllDimensions`、`format=jsondata|csvfile|xml`。
  - 结构端点：`/dataflow/{agency}`、`/datastructure/{agency},{flow}@{ver}`、`/codelist/{agency}/{id}`。
- 覆盖：OECD 38 国 + 伙伴国/新兴经济体；十余个统计域（农业、教育、能源、环境、金融、卫生、创新、劳工、税、贸易、福祉…）；年代视库（部分 1950s 起），月/季/年。
- 门槛：免费、**无 key、无注册**。
- 实测：2026-10-03，macOS arm64，curl 8.x（≥25 s 超时）：`/public/rest/v1/data/OECD.SDD.STES,DSD_STES@DF_FINMARK,4.0/.?startPeriod=2024-01&format=jsondata` → 200 / 353 KB JSON（含 `data.dataSets`）；`/dataflow/all?format=json-structure-2.0.0` → 200（响应大，25 s 只下到 404 KB）；`/dataflow/OECD.SDD.STES?format=jsondata` → **406**，提示 structure 只接受 `structure,xml-structure-3.0.0,sdmx-3.0,json-structure-2.0.0`。
- 上游：`https://data-explorer.oecd.org/`；API 说明 `https://www.oecd.org/en/data/insights/data-explainers/2024/09/api.html`（上游声明）。

## 坑

1. **结构与数据的 `format` 取值不同**：structure 端点用 `json-structure-2.0.0`（或 `structure`/`sdmx-3.0`），数据端点用 `jsondata`；写错 → 406。
2. agency/flow/version 三段不能缺；旧教程的 `stats.oecd.org/SDMX-JSON/...` 是上一代接口，已迁移。
3. `key` 里维度顺序由 DSD 决定，写错段数会 400/404；先读 `/datastructure/...`。
4. 全库查询响应数百 KB–MB，务必给 key 与期间（或 `firstNObservations=1`）。
