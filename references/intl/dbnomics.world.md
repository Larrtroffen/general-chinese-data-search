# dbnomics.world —— 多机构统计聚合 API

- 去哪找：门户 `https://db.nomics.world/`；**API v22** `https://api.db.nomics.world/v22/`。
- 什么时候用：**一个接口扫多个机构库**（World Bank、IMF、OECD、Eurostat、BIS、各国统计局、央行…）；要"同指标跨库对比"或不想逐个学 SDMX；探索"这个指标哪个库有"。
- 怎么搜：
  ```bash
  # ① 全库搜索（provider/dataset/series）
  curl -s 'https://api.db.nomics.world/v22/search?q=GDP&limit=2'
  # ② 数据集元数据 + 维度取值标签
  curl -s 'https://api.db.nomics.world/v22/datasets/WB/WDI?limit=2'
  # ③ 取序列观测值（序列码格式见「坑」）
  curl -s 'https://api.db.nomics.world/v22/series/WB/WDI/A-NY.GDP.MKTP.CD-CHN?observations=1'
  # ④ 列某数据集下的序列码（用来确认命名规则）
  curl -s 'https://api.db.nomics.world/v22/series/WB/WDI?limit=2&observations=0'
  ```
  - 定位三元组：`provider`（`WB`/`IMF`/`OECD`/`ESTAT`/`BIS`…）→ `dataset`（如 `WDI`）→ `series_code`。
  - 参数：`observations=1`（带回数值）、`format=json|csv`、`limit`/`offset`、`q`（搜索）。
  - 响应 `_meta.args` 会回显全部生效参数（调试利器）；序列观测在 `series.docs[0].period[]` / `value[]`。
- 覆盖：80+ 数据提供方、数万个数据集（DBnomics 自述）；随上游每日/定期镜像。
- 门槛：免费、**无 key、无注册**。
- 实测：2026-10-03，macOS arm64，curl 8.x：`/v22/search?q=GDP&limit=2` → 200（返回数据集命中）；`/v22/datasets/WB/WDI?limit=2` → 200 / 125 KB（含 `dimensions_codes_order` 与 `dimensions_values_labels`）；`/v22/series/WB/WDI/A-NY.GDP.MKTP.CD-CHN?observations=1` → 200 / 128 KB，64 期，末期 2023=`17794781986104.5`；`/v22/series/WB/WDI/NY.GDP.MKTP.CD?observations=1` → **404**（序列码必须完整）。
- 上游：`https://git.nomics.world/dbnomics`（上游声明）。

## 细节

### 序列码命名（以 WDI 为例）

`{频率}-{指标码}-{国家码}`，如 `A-NY.GDP.MKTP.CD-CHN`（A=annual）。其他 provider 的分隔符/段数不同，用 `/v22/datasets/{p}/{d}` 的 `dimensions_codes_order` 确认。

## 坑

1. `series_code` 必须**覆盖所有维度**；只给指标码 → 404。别猜，先 `/v22/series/{p}/{d}?limit=2&observations=0` 看真实码。
2. 维度连接符随 provider 不同（`-`、`.`、`/` 混用）；以数据集元数据为准。
3. DBnomics 是**镜像/再发布**，版本可能滞后原创库：实测同一 WDI 2023 年 GDP，DBnomics 给 `17.79e12`，世行 API 给 `18.27e12`——**正式引用回原机构**。
4. `format=csv` 便于批量但丢元数据；要口径/来源用 json。
