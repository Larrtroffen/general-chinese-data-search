# population.un.org —— 联合国人口司 WPP 人口预测

- 去哪找：WPP 门户 `https://population.un.org/wpp/`；批量下载 `https://population.un.org/wpp/downloads?folder=Standard%20Projections&group=CSV%20format`；Data Portal `https://population.un.org/dataportal/`；**API 文档（Swagger）** `https://population.un.org/dataportalapi/index.html`。
- 什么时候用：要**世界人口展望（WPP）**的中长期人口预测（分年龄/性别，1950–2100）；要各国生育率/死亡率/迁移/人口结构；要跨国人口分母或与中国口径对照。
- 怎么搜：Data Portal 提供**开放 REST API**（基址 `https://population.un.org/dataportalapi/api/v1/`）——
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 指标目录（免 token）
  curl -s -A "$UA" 'https://population.un.org/dataportalapi/api/v1/Indicators'
  # ② 国家/地区码（免 token，ISO2/ISO3/经纬度）
  curl -s -A "$UA" 'https://population.un.org/dataportalapi/api/v1/locations'
  # ③ 取数（需 token，见 Swagger 的 Generate Token）
  curl -s -A "$UA" -H "Authorization: Bearer $TOKEN" \
    'https://population.un.org/dataportalapi/api/v1/data/indicators/49/locations/156/start/2020/end/2030?pagingInHeader=false&format=json'
  ```
  批量文件走 `/wpp/downloads?folder=…&group=CSV format`（Excel/CSV zip）；单个直链如
  `https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_TotalPopulationBySex.csv.gz`。
  形态：目录接口 JSON（`data[]`），数据接口 JSON / 下载为 zip·csv.gz。
- 覆盖：WPP 2024 修订版（1950–2100，中方案及各变体）；国家/地区 × 年龄 × 性别；指标含总人口、生育、死亡、迁移；`/locations` 实测 300 个国家/地区。
- 门槛：批量文件下载免费；**Data Portal API 的目录/国家列表免 token，取数需免费注册生成 token**。
- 实测：2026-10-03，macOS arm64，curl 8.x 匿名：`/dataportalapi/api/v1/Indicators` 200（98,515 B，`total:86`）；`/api/v1/locations` 200（11,693 B，`total:300`）；`/api/v1/data/indicators/49/locations/156/start/2020/end/2021?pagingInHeader=false&format=json` → **401**；Swagger 规范 `…/dataportalapi/swagger/DataPortalOpenAPISpecificationv1.0/swagger.json` 200（136,179 B，含 `/api/v1/data/indicators/{indicators}/locations/{locations}/start/{startYear}/end/{endYear}` 等路径）；`WPP2024_TotalPopulationBySex.csv.gz` **200**（`content-type: application/x-gzip`）。
- 上游：United Nations, Department of Economic and Social Affairs, Population Division。

## 细节

### API 端点（从 Swagger 规范提取）

| 端点 | 说明 |
|---|---|
| `/api/v1/Indicators`、`/api/v1/Indicators/{codes}` | 指标目录 |
| `/api/v1/locations`、`/api/v1/locations/{codes}`、`/api/v1/locationsWithAggregates` | 国家/地区及聚合 |
| `/api/v1/topics`、`/api/v1/topics/{codes}` | 主题 |
| `/api/v1/data/indicators/{indicators}/locations/{locations}/start/{startYear}/end/{endYear}` | 取数（token） |
| `/api/v1/metadata/ages|sexes|variants|categories/{indicatorIds}` | 维度元数据 |
| `/api/v1/sources` | 数据来源 |

- 目录接口分页参数 `pageNumber`/`pageSize`（默认 100）；返回 `{pageNumber,pageSize,pages,total,data[]}`。
- 指标字段：`id / name / shortName / dimAge / dimSex / dimVariant / dimCategory`。

## 坑

1. **取数要 token**（实测无 token 401）：按 Swagger 页的「Generate Token」注册生成，元数据/国家列表则开放。
2. `/wpp/downloads` 直连可能返回 404（SPA 路由），但带 `?folder=…&group=CSV format` 的完整参数即可用；文件名与目录见 bundle。
3. WPP 修订版之间（2022/2024…）预测值差异大，引用必须标版本与基准年。
4. 大批量取数优先用 zip 下载（csv.gz），别逐个走 API。

## 相关

- 全球卫生指标对照见 `who-gho.md`；中国人口普查口径见 `stats.gov.cn-census.md`。
