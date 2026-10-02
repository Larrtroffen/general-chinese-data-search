# worldbank.org —— 世界银行开放数据 API

- 去哪找：指标门户 `https://data.worldbank.org/`；指标详情页 `https://data.worldbank.org/indicator/NY.GDP.MKTP.CD`；**API 根** `https://api.worldbank.org/v2/`。
- 什么时候用：跨国宏观面板的"第一站"——GDP/人口/贸易/教育/卫生/基础设施/贫困/治理（WGI）；要免 key、免注册、JSON 直出、可脚本化的长序列；要世界银行自编口径（WDI）而非第三方整编。
- 怎么搜：全部 GET、无 key、`format=json` 返回 JSON。三条核心端点：
  ```bash
  # ① 时间序列：country/{ISO3，多国用分号}/indicator/{指标码}?date=起:止
  curl -s 'https://api.worldbank.org/v2/country/CHN;USA/indicator/NY.GDP.MKTP.CD?format=json&date=2020:2023&per_page=100'
  # ② 指标目录（逾 2.9 万条）：/indicator，分页 per_page/page
  curl -s 'https://api.worldbank.org/v2/indicator?format=json&per_page=100&page=1'
  # ③ 国家与聚合体元数据（295 条，含 region/incomeLevel/lendingType）
  curl -s 'https://api.worldbank.org/v2/country?format=json&per_page=300'
  ```
  - 返回是**二元数组** `[分页对象, 数据数组]`；单条含 `indicator{id,value}`、`country{id,value}`、`countryiso3code`、`date`、`value`、`decimal`。
  - 常用参数：`per_page`、`page`、`date=2010:2023`（冒号=闭区间）、多国分号 `CHN;USA`、`source=`（数据源 id）、`mrnev=1`（仅最近非空值）、`gapfill=Y`。
  - 整表下载：`https://api.worldbank.org/v2/en/indicator/{指标码}?downloadformat=csv`（zip 内含 data 与元数据 CSV）。
- 覆盖：WDI 为主（217 经济体 × 1960–2024，视指标有年/季/月）；`/indicator` 实测 **29,544 个指标**跨数十个来源（WDI、WGI、LAC Equity Lab…）；`/country` 295 条含地区聚合（如 `AFE` 东非、`HIC` 高收入）。
- 门槛：免费，**无 key、无注册**；未公布频控，请自设 ≥1.5 s 间隔。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20 s 超时）：`country/CHN;USA/indicator/NY.GDP.MKTP.CD?date=2020:2023&per_page=100` → 200，`total=8`，中国 2023 年 GDP `18270356654533.2`；`/indicator?per_page=2` → 200，`total=29544`；`/country?per_page=300` → 200，`total=295`（响应约 20 s 未下完）；`/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv` → 200 `application/zip`。
- 上游：`https://data.worldbank.org/`；API 说明 `https://datahelpdesk.worldbank.org/knowledgebase/articles/889392`（上游声明，未逐条实测）。

## 细节

### 常用指标码

| 指标 | 代码 |
|---|---|
| GDP（现价美元） | `NY.GDP.MKTP.CD` |
| GDP 增长率（不变价） | `NY.GDP.MKTP.KD.ZG` |
| 人均 GDP（现价） | `NY.GDP.PCAP.CD` |
| 总人口 | `SP.POP.TOTL` |
| 城镇化率 | `SP.URB.TOTL.IN.ZS` |
| 货物与服务出口 | `NE.EXP.GNFS.CD` |
| 政府治理六维（WGI） | `GE.EST` / `RQ.EST` / `RL.EST` / `CC.EST` / `VA.EST` / `PV.EST` |

指标码怎么找：逐页翻 `/v2/indicator`，或按 `source=` 过滤某数据源，或在 `data.worldbank.org/indicator/{code}` 页面直接读 URL 里的码。

## 坑

1. 返回为 `[meta, rows]`，`value` 为 `null` 表示无数据（别当 0）；`decimal=0` 只是显示精度，原始值是浮点。
2. 国家码用 ISO3（`CHN`）；聚合体（`WLD`/`EAP`/`HIC`）也在 `/country` 列表里，别混进个体国家样本。
3. 不传 `per_page` 默认 50 条，多国多年极易只拿到第一页。
4. 本机（中国网络）到 `api.worldbank.org` 往返 12–20 s，大响应常被 20 s 超时截断；脚本设 ≥30 s 超时并重试。
