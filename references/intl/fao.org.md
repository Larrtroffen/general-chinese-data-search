# fao.org —— 联合国粮农组织统计

- 去哪找：门户 `https://www.fao.org/faostat/`；**批量下载** `https://fenixservices.fao.org/faostat/static/bulkdownloads/`；新 API `https://faostatservices.fao.org/api/v1/`（需 token）。
- 什么时候用：农业产量/面积/单产、粮食平衡表、农产品贸易、生产者价格、土地利用、林业、渔业、农业温室气体、粮食安全（FAO 口径）；要 1961 年以来的长时段国别面板。
- 怎么取：
  ```bash
  # ① 免费：整套 bulk zip（示例＝作物与畜产品产量，含 Normalized CSV）
  curl -sLO 'https://fenixservices.fao.org/faostat/static/bulkdownloads/Production_Crops_Livestock_E_All_Data_(Normalized).zip'
  # ② 需 token：新 API 无鉴权头 → 401
  #   curl -H 'Authorization: Bearer <TOKEN>' \
  #     'https://faostatservices.fao.org/api/v1/en/data/QCL?area_code=351&item_code=15&year=2022'
  ```
  - bulk 命名规律：`{Domain}_{E|C}_All_Data.zip` 或 `…(Normalized).zip`；域码如 `Production_Crops_Livestock`、`Trade_Crops_Livestock`、`FoodBalanceSheets`、`LandUse`、`Emissions_Agriculture`、`Forestry`、`Fishery`。
  - 新 API 用 FAOSTAT 域码（`QCL` 作物、`TCL` 贸易、`FBS` 粮食平衡…），参数 `area_code`/`item_code`/`element_code`/`year`；token 在 FAO 开发者门户免费申请。
- 覆盖：全球 245+ 国家/地区（FAO M49 三位码）；多数域自 1961 年，年度；bulk 有英/中两版（`_E_`/`_C_`）。
- 门槛：bulk 下载免费、无注册；**新 API 需 token**（免费申请）。
- 实测：2026-10-03，macOS arm64，curl 8.x：`.../static/bulkdownloads/Production_Crops_Livestock_E_All_Data_(Normalized).zip` → 200 / **33.9 MB** `application/zip`（13 s）；`https://faostatservices.fao.org/api/v1/en/definitions/domain/QCL` → **401** `Missing Authorization Header`；`https://fenixservices.fao.org/faostat/api/v1/en/definitions/domain/QCL` → 20 s 超时（老 API 路径已不作为）。
- 上游：`https://www.fao.org/faostat/en/#data`；API 门户 `https://faostatservices.fao.org/`（上游声明）。

## 坑

1. 老教程里的 `fenixservices.fao.org/faostat/api/v1/...` 已不可用（超时）；程序化取数改走 `faostatservices.fao.org` + token，或直接下 bulk。
2. bulk 文件名含空格/括号，shell 里必须加引号或 URL 编码。
3. `(Normalized)` 版是长表（Area/Item/Element/Year/Value/Flag），比宽表好解析；`Flag` 要留（A=官方、E=估计、X=外部）。
4. 国家码用 FAO 三位 M49（中国=351），不是 ISO3。
5. 单域数十 MB、全量数百 MB，注意磁盘与下载超时（本机 33.9 MB 用 13 s）。
