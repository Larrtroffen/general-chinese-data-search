# data.un.org —— 联合国数据门户

- 去哪找：门户 `https://data.un.org/`；探索/下载 `https://data.un.org/Explorer.aspx`；**遗留 SDMX 接口** `https://data.un.org/ws/rest/`（会 302 到 `https://data.un.org/legacy/ws/rest/`）。
- 什么时候用：跨机构拼口径的国家级年度序列（UNSD/UNCTAD/WHO/ILO/UNESCO…）；找 UNdata 里现成的整合表（人口、能源、国民账户、贸易、社会指标、性别、难民）；要 SDMX 结构化取数。
- 怎么搜：现代站点是 Next.js 前台、**无公开 JSON API**（实测 `/api/search` 404）；能用的是遗留 SDMX：
  ```bash
  # ① 数据流目录（SDMX 2.1 structure XML）
  curl -sL 'https://data.un.org/ws/rest/dataflow'
  # ② 取数：flow 见下，key 需与 DSD 维度数完全一致
  curl -sL 'https://data.un.org/ws/rest/data/{flow}/{key}'
  # ③ 页面取数：https://data.un.org/Explorer.aspx 选库 → 筛选 → Download（CSV）
  ```
  - `dataflow` 实测返回 20+ 个 Dataflow 的 `id`/`agencyID`/`Name`：`DF_UNData_UIS`(UIS/UNData 教育)、`DF_SDG_GLH`(IAEG-SDGs 全球 SDG)、`NA_MAIN`(ESTAT 国民账户主总量)、`DF_SEEA_AEA`、`DF_SEEA_ENERGY`、`NASEC_IDCFINA_A/Q`、`NASEC_IDCNFSA_A/Q` 等。
- 覆盖：UNdata 整合库为主（人口、能源、环境、国民账户、贸易、信息社会、性别、难民…）；年代随子库（人口/国民账户可回溯 1950 年代）；粒度=国家×年×指标。
- 门槛：免费、无 key；页面下载无需登录（部分子库跳转机构自站另论）。
- 实测：2026-10-03，macOS arm64，curl 8.x：`https://data.un.org/` → 200；`/ws/rest/data/UNdata/`（无 flow）→ 404 `Could not find Dataflow…`；`/ws/rest/dataflow` → 302 后 200 / 6.4 KB SDMX XML；`/ws/rest/data/NA_MAIN/.A.CHN.?startPeriod=2020` → **422** `Not enough key values in query, expecting 14 got 4`（服务在线，但 NA_MAIN 需 14 个维度值）；`/api/search?q=population` → 404；`https://data.un.org/ws/rest/dataflow/UNSD` → 200。
- 上游：`https://data.un.org/`（UNSD 维护）。

## 细节

### 部分数据流

| Dataflow id | agency | 名称 |
|---|---|---|
| `DF_SDG_GLH` | IAEG-SDGs | SDG Harmonized Global Dataflow |
| `DF_UNData_UIS` | UIS | SDMX_UIS_UNData（教育） |
| `NA_MAIN` | ESTAT | NA Main Aggregates（14 维） |
| `NASEC_IDCNFSA_A` / `_Q` | ESTAT | 年度/季度非金融账户 |
| `NASEC_IDCFINA_A` / `_Q` | ESTAT | 年度/季度金融账户 |
| `DF_SEEA_AEA` / `DF_SEEA_ENERGY` | ESTAT | 空气排放账户 / 能源实物量账户 |

维度顺序与码表要用 `https://data.un.org/ws/rest/datastructure/{agency}/{flow}` 查（本机未复测该路径）。

## 坑

1. **没有现代 JSON API**：`data.un.org/api/*` 404；程序化取数只能走 `/legacy/ws/rest/` 的 SDMX（XML/JSON），或退回页面导 CSV。
2. `/ws/rest/...` 会 302 到 `/legacy/...`，curl 必须 `-L`，否则拿到 0 字节。
3. key 的维度个数必须与 DSD 一致（`NA_MAIN` 要 14 段），否则 422——**先读 DSD 再拼 key**，别用"点号省略全部"。
4. 同一指标在 UNdata 与机构自站（WHO/ILO/UNESCO）可能是不同版本/年份，正式引用注明取数日期与来源机构。
