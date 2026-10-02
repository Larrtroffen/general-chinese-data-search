# imf.org —— 国际货币基金组织数据

- 去哪找：新数据门户 `https://data.imf.org/`；**SDMX 2.1 接口** `https://api.imf.org/external/sdmx/2.1/`（结构 `.../dataflow`，取数 `.../data/{flow}/{key}`）。
- 什么时候用：要 IMF 自编口径的国际收支（BOP）、CPI/PPI、国民账户（NEA）、财政（GFS）、货币金融（MFS）、汇率、COFER 官方储备币种构成、直接投资（DIP/CDIS）；做跨国金融与宏观面板。
- 怎么搜：
  ```bash
  # ① 数据流目录（SDMX structure XML，实测 300+ 个 flow）
  curl -s 'https://api.imf.org/external/sdmx/2.1/dataflow'
  # ② 取数：flow=CPI，key=CN（国家维度），限定期间避免超时
  curl -s 'https://api.imf.org/external/sdmx/2.1/data/CPI/CN.?startPeriod=2024-01&endPeriod=2024-03'
  ```
  - 从 `dataflow` 找 flow id（实测见下），再从 `/datastructure/{flow}`（或 `datastructure/all`）读维度顺序与码表，才能正确拼 `{key}`。
  - 返回默认 SDMX-XML（`StructureSpecificData`）；可用 `dimensionAtObservation=AllDimensions`。
- 覆盖：IMF 全部统计库——IFS、BOP、GFS、MFS、CPI/PPI、COFER、DIP、AEA、区域展望（APDREO/AFRREO）、性别统计（GS）等；年代随库（IFS 回溯 1948），月/季/年，国家 + 聚合体；另有各期 vintage（如 `CPI_2026_APR_VINTAGE`）。
- 门槛：免费、无 key、无注册。
- 实测：2026-10-03，macOS arm64，curl 8.x：`https://api.imf.org/external/sdmx/2.1/dataflow` → 200 / 448 KB（含 `CPI`/`BOP`/`NEA`/`GFS`/`COFER`/`DIP`/`PPI`/`AEA`/`AFRREO` 等及 vintage 变体）；`.../data/CPI/CN.?startPeriod=2024-01&endPeriod=2024-03` → 200 / 8.2 KB SDMX-XML；`.../data/CPI/.?startPeriod=2024-01` → 200 但 20 s 只下到 811 KB（全省查询过大）；`dataservices.imf.org` → **DNS 解析失败**；`www.imf.org/external/datamapper/api/v1/indicators` → **403 Access Denied**（Akamai）。
- 上游：`https://data.imf.org/`；SDMX 文档 `https://data.imf.org/en/Resource-Pages/SDMX`（上游声明）。

## 细节

### 实测可见的部分 flow id

`CPI`（消费者价格）、`PPI`、`BOP`、`BOP_AGG`、`NEA`、`GFS`、`MFS`、`COFER`、`DIP`、`AEA`、`CPI_WCA`、`AFRREO`、`APDREO`、`ANEA`、`WoRLD`、`FA`；另有大量 `{FLOW}_{YYYY}_{MMM}_VINTAGE` 的期次快照（做实时数据/修订研究用）。

## 坑

1. 老教程的 `dataservices.imf.org/REST/SDMX_JSON.svc/...` **已死**（本机 DNS 不解析），别再照抄。
2. IMF DataMapper（WEO 增长/通胀预测）本机被 Akamai 403 拦；要 WEO 数字请走 `data.imf.org` 页面导出或换网络。
3. `api.imf.org` 默认返回 XML；维度 key 必须与 DSD 维度数/顺序一致，先用 `.` 占位再逐段收紧。
4. 全库 `.` 查询会拉爆超时——务必给 flow + 国家 key + `startPeriod`/`endPeriod`。
5. 同一指标有多个 vintage flow，常规分析取主 flow，做"当时可得的数"才用 vintage。
