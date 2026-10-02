# unctad-wto-trade —— 贸易统计与价值链数据

- 去哪找：**UNCTADstat** 数据门户 `https://unctadstat.unctad.org/`（Data Centre `https://unctadstat.unctad.org/datacentre/`；API 基址 `https://unctadstat-api.unctad.org/`，数据服务文档 `…/datamart-api/{dataset}/cur`，批量下载 `…/bulkdownload/{dataset}/{reportInstanceId}/{file}.csv`；帮助 `https://unctadstat.unctad.org/EN/Help.html`）；**WTO Stats** 门户 `https://stats.wto.org/`、站内 REST `https://stats.wto.org/api/indicators/*`、官方 API `https://api.wto.org/timeseries/v1/`（注册 `https://apiportal.wto.org/`）、批量下载 `https://www.wto.org/english/res_e/statis_e/trade_datasets_e.htm`。
- 什么时候用：要**贸易/发展类跨国指标**——货物与服务贸易、贸易依存与 GVC 参与度、外资/FDI、海运与商品价格、关税与市场准入、服务贸易分项；做贸易结构、价值链参与、贸易政策评估。
- 怎么搜：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① UNCTADstat API：先取某数据集的服务文档（OData 实体集）
  curl -s -A "$UA" 'https://unctadstat-api.unctad.org/datamart-api/US.PCI/cur'
  # 批量文件（需 report instance id，从门户下载页/服务文档解析）
  curl -sLO -A "$UA" 'https://unctadstat-api.unctad.org/bulkdownload/US.PCI/{instanceId}/US_PCI.csv'
  # ② WTO 官方 API（须 subscription key）
  curl -s 'https://api.wto.org/timeseries/v1/data?i=ITS_MTV_AX&r=156&p=000&subscription-key=<KEY>'
  # ③ WTO 批量直链（免 key，zip/csv）
  curl -sLO -A "$UA" 'https://www.wto.org/english/res_e/statis_e/daily_update_e/Tismos_exports.zip'
  ```
  结果形态：JSON/CSV/xlsx/zip；UNCTADstat 门户与 `stats.wto.org` 是 SPA（多数交互**需浏览器**），批量文件与官方 API 可脚本化。
- 覆盖：UNCTADstat 门户自述「150+ 指标、覆盖几乎所有经济体」（贸易、投资、海运、商品价格、人口、GVC 派生等）；WTO Stats 覆盖货物/服务贸易、关税与贸易便利化等，服务贸易批量含 BATIS(BPM6)、TiSMoS，商品贸易有 IDB/Tariff 数据（以门户栏目为准）。
- 门槛：**免费**；UNCTADstat 免 key；**WTO 官方 API 需 subscription key**（`apiportal.wto.org` 免费注册），WTO 门户与 `www.wto.org/.../daily_update_e/*` 批量直链免 key。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA、`-L`、20 s）——`stats.unctad.org/` `200`→`unctadstat.unctad.org/EN/Index.html`（`21,098 B`）；`unctadstat.unctad.org/datacentre/` `200/43,347 B`（Angular SPA，`config/config.js` 暴露 `API_SERVICE_URL=https://unctadstat-api.unctad.org/datamart-api`、`STATS_API`、`USER_API`）。`unctadstat-api.unctad.org/` `200`「Api Works」；`…/datamart-api/US.PCI/cur` `200`（OData `$metadata`/实体集 `Years/Series/…`）；`…/datamart-api/`（无 path）`400`；`…/bulkdownload/US.PCI/US_PCI.csv` `400`「bulk file not available … report instance id」（须带正确实例 id）。`stats.wto.org/` `200/2,638 B`（Angular SPA；`Scripts/main.bundle.js` `200/522,315 B`，内含 `stats.wto.org/api/indicators/*`、`/api/downloadpivot/{csv,excel}`、`api.wto.org/timeseries/v1/`、`apiportal.wto.org`）；直接请求 `stats.wto.org/api/indicators/getindicators/`（GET/POST）均回落 SPA HTML（未取到 JSON）。`api.wto.org/timeseries/v1/data?i=ITS_MTV_AX&r=156&p=000` → **401**「missing subscription key」；`apiportal.wto.org/` `200`。WTO 批量页 `trade_datasets_e.htm` `200`，`…/daily_update_e/Tismos_exports.zip` → `206 application/x-zip-compressed`。
- 上游：UNCTADstat `https://unctadstat.unctad.org/`（UNCTAD 统计司）；WTO Stats `https://stats.wto.org/`、WTO API 门户 `https://apiportal.wto.org/`、批量数据 `https://www.wto.org/english/res_e/statis_e/trade_datasets_e.htm`。

## 细节

### UNCTADstat（现状：门户 SPA + 新 OData API）

| 端点 | 现象（2026-10-03） |
|---|---|
| `https://unctadstat.unctad.org/`（旧 `/EN/Index.html`） | `200`，Data Hub 首页 |
| `https://unctadstat.unctad.org/datacentre/` | `200`，新 Data Centre（Angular） |
| `https://unctadstat-api.unctad.org/` | `200`「Api Works」 |
| `…/datamart-api/{dataset}/cur` | `200`，OData 服务文档（实体集：Footnotes/MissingValues/Years/Series…） |
| `…/bulkdownload/{dataset}/{instanceId}/{file}.csv` | 需正确 dataset+instanceId，否则 `400` |
| `https://unctadstat.unctad.org/EN/Help.html` | 门户使用/账户帮助 |

- 旧教程的 `…/api/reportFolders/…` 已 404；现走 `datamart-api` OData 路径。数据集代码形如 `US.PCI`（商品价格指数）、`US.TradeInServices` 等，需从门户/服务文档取。

### WTO Stats

| 目标 | 端点 |
|---|---|
| 数据门户（查询/导出） | `https://stats.wto.org/`（SPA） |
| 站内 REST（门户自用） | `https://stats.wto.org/api/indicators/getindicators/`、`…/getallterritories/`、`/api/downloadpivot/{csv,excel}`、`/api/downloadinventory/excel` |
| 官方 API（需 key） | `https://api.wto.org/timeseries/v1/data?i={indicator}&r={reporter}&p={partner}&subscription-key=…` |
| key 申请 | `https://apiportal.wto.org/` |
| 批量下载（免 key） | 服务贸易：`…/statis_e/trade_datasets_e.htm` → `daily_update_e/{TiSMoS_*,OECD-WTO_BATIS_*}.{zip,csv}` |

## 坑

1. **不要当「UNCTADstat 挂了」**：门户与 API 都可达，难的是**拼出正确的 dataset + report instance id**；批量 URL 少一段就 `400`，先取 `datamart-api/{dataset}/cur` 或从门户「Bulk download」页解析。
2. **WTO 站内 REST 不是公开 API**：`stats.wto.org/api/*` 直接请求回落 SPA HTML（可能需要 AJAX/会话上下文），脚本化请用**官方 `api.wto.org` + key**，别硬爬站内接口。
3. **`api.wto.org` 无 key 一律 401**（「missing subscription key」），key 免费但要注册；调用量受订阅层限制。
4. **本机难点的历史记录**：这两家门户均为 JS SPA，早期教程里的 `wide/TableViewer`、`unctadstat.unctad.org/wds/…`、`stats.wto.org/#/…` 直链多已失效，以本卡端点为准。
5. **口径混用**：WTO 贸易额（货物/服务口径、BPM6）与 UNCTADstat、UN Comtrade（`comtrade.un.org.md`）口径不同；跨国面板拼接先对齐 HS/BPM 版本与报告国-伙伴国镜像。
6. UNCTADstat 部分 GVC/足迹派生指标源自 Eora 等 MRIO（见同层 `wiood-eora.md`），引用要追到原始 IO 库版本。
