# mobility —— 人口迁徙与城际出行数据

三家合为一卡：**百度迁徙**（百度地图慧眼，公开 JSONP 接口，可直接取数）是主力；
**腾讯位置大数据**（`heat.qq.com`，仅存历史迁徙存档）；**腾讯位置服务 LBS**（`lbs.qq.com`，需 key）作补充。
春运/节假日出行预测报告同属百度慧眼报告中心（报告清单 API 见 `commute-city.md`）。

- 去哪找：
  - **百度迁徙（前端）** `https://qianxi.baidu.com/`（SPA，title「百度迁徙-百度地图慧眼」，数值由 JS 填）
  - **百度迁徙数据 API** 走慧眼主域：`https://huiyan.baidu.com/migration/historycurve.jsonp`（指数时间序列）、`.../cityrank.jsonp`（来源城市排行）；同族还有 `provincerank.jsonp` / `provincecityrank.jsonp` / `lastdate.jsonp`（未逐一实测）
  - **百度慧眼报告中心** `https://huiyan.baidu.com/reports`（迁徙/出行预测/交通/通勤报告）
  - **腾讯位置大数据** `https://heat.qq.com/`（入口，JS 跳 `/bigdata/index.html`）；历史迁徙 JSON `https://heat.qq.com/api/getLbsMigrateDataByBeijing.php`
  - **腾讯位置服务（需 key）** `https://lbs.qq.com/`，JS API 迁徙文档 `https://lbs.qq.com/webApi/javascriptV2/jsDoc/Migration`
- 什么时候用：要**城市/省之间的迁入迁出规模、来源地排行、迁徙规模指数日序列**（春运、节假日、日常）；做人口流动、城际联系、返工返岗、疫情/假期出行分析；要「百度/腾讯迁徙数据」的原始接口而非转述图表时。
- 怎么搜：全为 **GET JSONP / JSON**，免 key、免登录（`cb({...})` 包裹，去掉 `cb(`/`)` 即标准 JSON）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 迁徙规模指数日序列（2019-01 起；dt=city 须给城市码，dt=province 给省码）
  curl -sS -A "$UA" 'https://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id=420000&type=move_in'
  # ② 某日「迁入来源城市」排行（dt=city 时 id 必须是城市码，如 420100=武汉）
  curl -sS -A "$UA" 'https://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=420100&type=move_in&date=20260929'
  # ③ 腾讯历史迁徙（城市→城市：迁入人数 + 三类占比）；2026 年日期返回空
  curl -sS -A "$UA" 'https://heat.qq.com/api/getLbsMigrateDataByBeijing.php?city=%E5%8C%97%E4%BA%AC&date=2020-09-23&direction=1&type=6'
  ```
  结果形态：**JSONP**（百度，`{"errno":0,"data":{...}}`）与 **JSON**（腾讯，`{"status":0,"data":[[城市,人数,占比…]]}`）；网页端 `qianxi.baidu.com` 为 JS 渲染，勿解析 HTML。
- 覆盖：百度迁徙 = 全国省/市粒度，**日度，2019-01-12 起**，实测 2026-09-29 仍有数（`type` 分 `move_in/move_out`）；腾讯位置大数据 = 城市历史迁徙存档（实测 2020-09 有数，2026 年日期为空）；慧眼报告中心含 2016 年以来的出行/交通类报告（历年春运与五一/十一/春节假期出行预测，2019Q3 起为季度交通报告）。
- 门槛：**免费、免登录、无 key**（百度慧眼 API）；腾讯 `heat.qq.com` 页面免费，历史 API 无鉴权但数据已停更；`lbs.qq.com` 迁徙 JS API 需注册申请 key。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `GET https://qianxi.baidu.com/` → **200**，2.2 KB，`<title>百度迁徙-百度地图慧眼</title>`
  - `GET huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id=420000&type=move_in` → **200**，23.7 KB，`data.list` 为 `{YYYYMMDD: 指数}`，首值 `20190112: 4.3625304`
  - `GET huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=420100&type=move_in&date=20260929` → **200**，8.7 KB，首条「孝感市 / 湖北省 / 13.05」；同参数用**省码** `id=420000` → `"list":[]`（故 `dt=city` 必须给城市码）
  - `GET heat.qq.com/` → **200**，title「腾讯位置大数据」，JS 跳 `/bigdata/index.html`；`GET /bigdata/index.html` → **200**「产品介绍」；`GET /bigdata/qianxi.html` → **404**（迁徙工具不在该路径）
  - `GET heat.qq.com/api/getLbsMigrateDataByBeijing.php?city=北京&date=2020-09-23&direction=1&type=6` → **200** `{"status":0,"data":[["上海","194568","0.1186","0.4567","0.4248"],…]}`；同接口 `date=2026-09-29` → **200** `{"status":0,"data":[]}`
- 上游：百度地图慧眼 <https://huiyan.baidu.com/>（入口 <https://qianxi.baidu.com/>）；腾讯位置大数据 <https://heat.qq.com/>；腾讯位置服务 <https://lbs.qq.com/>。

## 细节

### 百度迁徙 JSONP 端点与参数（前端 `qianxi.baidu.com` 实际调用）

| 端点（`https://huiyan.baidu.com`） | 关键参数 | 返回 |
|---|---|---|
| `/migration/historycurve.jsonp` | `dt=city\|province`、`id=<区划码>`、`type=move_in\|move_out` | `data.list` = `{YYYYMMDD: 指数}`（**本机实测**） |
| `/migration/cityrank.jsonp` | 同上 + `date=YYYYMMDD` | `data.list` = `[{city_name, province_name, value}]`（**本机实测**） |
| `/migration/provincerank.jsonp` | `dt=province`、`id`、`type`、`date` | 省际来源排行（同族，未逐一实测） |
| `/migration/provincecityrank.jsonp` | `dt=province`、`id`、`type`、`date` | 省内城市排行（同族，未逐一实测） |
| `/migration/lastdate.jsonp` | `dt=city\|province`、`id`、`type` | 最新可用日期（同族，未逐一实测） |

- 区划码 = 国标行政区划码（`420000` 湖北省、`420100` 武汉市）；`type=move_in` 表示「迁入本地的来源地排行」。
- 响应固定包一层 `cb(...)`；若需纯 JSON，用 `sed 's/^[^(]*(//; s/)[[:space:]]*$//'` 或前端脚本剥离。

### 腾讯位置大数据

| 端点 | 说明 |
|---|---|
| `https://heat.qq.com/` → `/bigdata/index.html` | 官网/产品介绍（区域热度、位置流量、人口迁徙、市政/商业/旅游应用） |
| `https://heat.qq.com/api/getLbsMigrateDataByBeijing.php` | 历史迁徙 JSON：`city=<城市名URL编码>`、`date=YYYY-MM-DD`、`direction=1`、`type=6`；`data` 每行 `[目的城市, 迁入人数, 占比1, 占比2, 占比3]`（**本机实测**，2020 有数） |
| `https://heat.qq.com/heatmap_result.php` | 区域热力图数据（搜索引擎收录，**未本机实测**） |

- 腾讯另有官方 **位置大数据 MCP**（腾讯云 `cloud.tencent.com/developer/mcp/server/11760`）与位置数据可视化 API（`lbs.qq.com/visualization_api/`），面向商业合作。

### 春运 / 城际出行公开报告

- 百度慧眼报告中心 `https://huiyan.baidu.com/reports` 的清单 API：`https://huiyan.baidu.com/hycms/home/reports.jsonp?issue=true`（不传 `role` 返回全部 64 期，含「春节/十一/五一假期出行预测报告」「春运出行提示」）；字段与 id 表见 `commute-city.md`。
- 高德「中国主要城市迁徙意愿排行榜」：`https://report.amap.com/migrate/index.do`（title「中国主要城市迁徙排名」，页面 meta 标注 春运交通播报·交通运输部运输服务司；数据/图表由 JS 渲染，CLI 直取受限——见 `commute-city.md` 坑 3）。

## 坑

1. **`dt` 与 `id` 必须匹配**：`dt=city` 却传省码（如 `420000`）会返回 `"list":[]` 而非报错，容易误判为「接口挂了」；城市用市码、省用省码。
2. **日期格式**：百度为 `YYYYMMDD`（如 `20260929`）；腾讯为 `YYYY-MM-DD`。跨天/当天查询时索引数据可能尚未生成，返回空先换前一天再判断。
3. **是 JSONP 不是纯 JSON**：百度 `migration/*.jsonp` 外层是 `cb(...)`，直接 `json.loads` 会失败；腾讯 `heat.qq.com` 那支是纯 JSON。
4. **腾讯迁徙 API 已停更**：实测 2026-09-29 返回空、2020-09-23 有数；该接口适合取历史（含 2016 年起的老数据），追新须回百度迁徙或商业接口。`heat.qq.com/bigdata/qianxi.html` 为 404，官网迁徙工具的当前路径未定位（页面为 SPA）。
5. **口径提醒**：百度/腾讯迁徙均基于自家地图/LBS 的定位 SDK 抽样，不是普查或运营商全量；跨年、跨平台绝对值不可直接比，引用须写明「百度地图慧眼迁徙数据」+ 抓取日。
6. **`lbs.qq.com` 的迁徙 JS API 需 key**：走控制台申请，属开发接口而非开放数据；量级与粒度受配额限制。
