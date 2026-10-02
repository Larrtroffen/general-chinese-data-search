# unstats.un.org —— 联合国 SDG 指标库 API

- 去哪找：数据库门户 `https://unstats.un.org/sdgs/indicators/database/`；**API 根** `https://unstats.un.org/sdgapi/v1/`；Swagger `https://unstats.un.org/sdgapi/swagger/`。
- 什么时候用：要 **SDG 官方口径**（1.1.1 贫困、2.x 粮食、3.x 卫生、4.x 教育、8.x 就业、13.x 气候…）；要"目标—具体目标—指标—系列"的层级元数据；做可持续发展与国别进展分析。
- 怎么搜：REST + JSON，GET，无 key、无注册：
  ```bash
  # ① 指标全表（含 goal/target/code/description/tier/series）
  curl -s 'https://unstats.un.org/sdgapi/v1/sdg/Indicator/List'
  # ② 单指标取数（areaCode=156 中国，startYear 起）
  curl -s 'https://unstats.un.org/sdgapi/v1/sdg/Indicator/Data?indicator=1.1.1&areaCode=156&startYear=2015'
  # ③ 地理区域字典（M49）
  curl -s 'https://unstats.un.org/sdgapi/v1/sdg/GeoArea/List'
  ```
  - 取数参数：`indicator=`（逗号多值）、`areaCode=`（M49 数字码，逗号多值）、`startYear`/`endYear`、`pageSize`/`pageNumber`、`seriesCode`、`dimensions`（是否回传维度标签）、`includeNonDiscontinuedSeries`。
  - 元数据端点：`/sdg/Indicator/{code}`、`/sdg/Goal/List`、`/sdg/Target/List`、`/sdg/Series/List`、`/sdg/GeoArea/List`、`/sdg/DataSource/List`。
  - 取数响应为分页对象：`{size,totalElements,totalPages,pageNumber,attributes[],dimensions[],data[]}`。
- 覆盖：17 目标 / 200+ 全球指标（tier I–III）；`areaCode` 覆盖 200+ 国家与区域聚合（M49）；多数序列 2000 年至今，年度；全球数据库按季更新。
- 门槛：免费、**无 key、无注册**。
- 实测：2026-10-03，macOS arm64，curl 8.x：`/sdgapi/v1/sdg/Indicator/List` → 200 / 256 KB（首条 `1.1.1`，含 `tier`/`series`/`uri`）；`/sdgapi/v1/sdg/Indicator/Data?indicator=1.1.1&areaCode=156&startYear=2015` → 200 / 30 KB，`totalElements=158`、`totalPages=7`、`attributes` 含 `Nature`/`Reporting Type`/`Units` 等码表。
- 上游：`https://unstats.un.org/sdgapi/swagger/`（UNSD）。

## 细节

### 数据里的 `attributes` 是什么

响应顶层 `attributes[]` 给的是**维度码表**（如 `Nature`：C=国家数据、CA=国家调整、E=估计值、G=全球监测…；`Reporting Type`；`Units`），`data[]` 每行用码引用。取数时加 `dimensions=true` 会带回更完整的维度标签。

## 坑

1. 指标码是"点分"SDG 码（`1.1.1`、`8.5.2`），不是 `SDG_1_1_1` 之类；从 `/Indicator/List` 复制。
2. `areaCode` 是 **M49 数字码**（中国 156），与 ISO3 不同；区域聚合体也在 `GeoArea/List` 里，注意剔除。
3. 分页默认较小，`totalElements` 上百时要翻页（`pageNumber`）；`pageSize` 有上限。
4. 同一指标可能有多个 `series`（按性别/年龄/城乡分解），不筛 `seriesCode` 会混在一起。
5. 与 UNdata 的 `DF_SDG_GLH` 是同一批数据的两种入口；SDG API 是官方首选。
