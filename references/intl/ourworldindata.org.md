# ourworldindata.org —— 全球发展数据整编与图表

- 去哪找：门户 `https://ourworldindata.org/`；图表库 `https://ourworldindata.org/charts`；**图表 CSV 直链** `https://ourworldindata.org/grapher/{slug}.csv`。
- 什么时候用：快速拿到"已整合、已清洗、已注明来源"的跨国长序列（寿命、贫困、能源、CO₂、人口、教育、政治制度等）；要能直接喂 pandas/Excel 的 CSV；教学/综述配图，省去多源对齐。
- 怎么取：
  ```bash
  # 图表 CSV：{slug} 取自图表页 URL（/grapher/{slug}）
  curl -sL 'https://ourworldindata.org/grapher/gdp-per-capita-maddison.csv' -o gdppc.csv
  # 页面右上 "Download" 同源提供 CSV / JSON
  ```
  - CSV 列形如 `Entity,Code,Year,<指标名>,<指标名> (Annotations)`；`Code` 是 ISO3 / OWID 自定区划码。
  - 数据管道开源在 `github.com/owid/etl` 与 `owid/owid-datasets`（可整库复现）。
- 覆盖：数百个图表，每图年代各异（Maddison 起 1820，CO₂ 起 1750，多数社会指标 1950/1990 起）；含"OWID 自算"与"转引第三方（世行/UN/IHME/官方统计局）"两类。
- 门槛：图表与 CSV 免费、无注册（`api.ourworldindata.org` 指标 API 需鉴权，本机 404）。
- 实测：2026-10-03，macOS arm64，curl 8.x：`/grapher/gdp-per-capita-maddison.csv` → 200 `text/csv`，首行 `Entity,Code,Year,GDP per capita,...`（20 s 内下到 261 KB 后超时截断，正文正常）；`/grapher/life-expectancy.csv` → 20 s 连接超时（同站偶发慢）；`https://api.ourworldindata.org/v1/indicators/` → **404**。
- 上游：`https://github.com/owid`（ETL 与数据集仓库，上游声明）。

## 坑

1. 站点**从中国网络慢且偶发超时**：设 ≥60 s 超时，用 `-C -` 断点续传；必要时分次重试。
2. OWID 是**二次整编**，正式引用要回溯图页 "Sources" 里的原始来源，不要只引 OWID。
3. 图表 CSV 的列名会随图改版变化；脚本按列名读时先校验表头。
4. `api.ourworldindata.org` 指标目录需鉴权，本机未通；日常取数走 `/grapher/{slug}.csv` 即可。
