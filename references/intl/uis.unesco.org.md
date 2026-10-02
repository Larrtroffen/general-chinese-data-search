# uis.unesco.org —— 教科文组织统计研究所

- 去哪找：门户 `https://uis.unesco.org/`；**UIS Data API** `https://api.uis.unesco.org/api/public/`；Swagger UI `https://api.uis.unesco.org/api/public/documentation/`。
- 什么时候用：教育（入学/识字/完成率/师资/教育经费）、科学与 R&D、文化与传播信息指标；要联合国教科文口径的跨国可比数据；做教育公平、创新投入研究。
- 怎么搜：GET + JSON，公开查询端点无 key，但**必须带 `geoUnit` 或 `indicator`**：
  ```bash
  # ① 取数：中国 2018 年起的小学完成率（CR.1）
  curl -s 'https://api.uis.unesco.org/api/public/data/indicators?geoUnit=CHN&indicator=CR.1&start=2018'
  # → {"hints":[],"records":[{"indicatorId":"CR.1","geoUnit":"CHN","year":2018,"value":97.75927734375,...}],"indicatorMetadata":[]}
  ```
  - 参数：`geoUnit`（ISO3 或 UIS 地区码，多值逗号）、`indicator`（如 `CR.1` 小学完成率，多值逗号）、`start`/`end`（年）、`page`/`pageSize`。
  - 元数据端点：`/api/public/meta/...`（本机 `meta/indicators`、`meta/` 均 404，实际路径以 Swagger 为准）；**批量全库下载**走 `/api/public/files/`，需先申请 **API token**（上游声明，未本机实测）。
- 覆盖：全球 200+ 国家/地区；教育全阶段 + 理工/研发/文化传播；1960s 起（视指标），年度。
- 门槛：查询端点免费无 key；**批量/订阅读取需 token**（在 `api.uis.unesco.org` 免费申请）。
- 实测：2026-10-03，macOS arm64，curl 8.x：`/api/public/data/indicators?geoUnit=CHN&indicator=CR.1&start=2018` → 200 / 254 B，`records` 含 2018=97.759、2020=99.19；`/api/public/data/indicators`（无参数）→ **400** `At least one geoUnit or indicator query parameter value must be provided`；`/api/public/documentation/` → 200（Swagger UI，title "UIS Data API"）。
- 上游：`https://uis.unesco.org/en/uis-data-api`（上游声明）。

## 坑

1. **必须带 `geoUnit` 或 `indicator`**，否则 400；不能"一把拉全库"（全库走 bulk + token）。
2. `indicator` 码区分大小写与点号（`CR.1`）；正确清单以 Swagger 的 definitions 为准（本机未取到 meta 列表端点）。
3. bulk zip 需注册取 token；免费但要走申请流程。
4. UIS 口径（如识字率定义、ISCED 层级）与中国国内统计口径不同，跨国比较前读 `indicatorMetadata`。
