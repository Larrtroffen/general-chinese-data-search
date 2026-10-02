# cnemc.cn —— 空气质量实时与历史

- 去哪找：中国环境监测总站 `https://www.cnemc.cn/`；**全国城市空气质量实时发布平台** `https://air.cnemc.cn:18007/`（城市/点位/24 小时变化三个面板）。
- 什么时候用：要**匿名、可脚本**的全国城市空气质量数据——AQI、PM2.5/PM10/SO₂/NO₂/CO/O₃（含 24h 均值、O₃-8h）、首要污染物、空气质量等级；做空气质量时序、城市对比、污染事件复盘；要点位级（站点）数据。
- 怎么搜：`air.cnemc.cn:18007` 是 ASP.NET 站点，面板与数据接口都在 `Content/Scripts/Map/TDMap.js` 里（源码可读），**全部匿名 GET/POST，返回 JSON**：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # 省份列表（含 Id / ProvinceCode / ProvinceJC）
  curl -sS -A "$UA" 'https://air.cnemc.cn:18007/CityData/GetProvince'
  # 某省城市列表（pid 取上一步 Id）
  curl -sS -A "$UA" 'https://air.cnemc.cn:18007/CityData/GetCitiesByPid?pid=1'
  # 城市点位实时数据（cityName 用中文市名，如 北京市）
  curl -sS -A "$UA" 'https://air.cnemc.cn:18007/CityData/GetAQIDataPublishLive?cityName=%E5%8C%97%E4%BA%AC%E5%B8%82'
  # 24 小时逐时序列（POST，citycode 为 6 位城市代码）
  curl -sS -A "$UA" -X POST 'https://air.cnemc.cn:18007/HourChangesPublish/GetCityRealTimeAqiHistoryByCondition?citycode=110000'
  # 逐日序列（同上，换 GetCityDayAqiHistoryByCondition）
  curl -sS -A "$UA" -X POST 'https://air.cnemc.cn:18007/HourChangesPublish/GetCityDayAqiHistoryByCondition?citycode=110000'
  ```
  结果形态：JSON 数组，字段如 `StationCode/PositionName/TimePoint/AQI/PM2_5/PM10/SO2/NO2/CO/O3/O3_8h/PrimaryPollutant/Quality/Measure`。
- 覆盖：全国 31 省级单位 → 城市 → 监测点位 · 实时（整点）+ 近 24 小时逐时 + 日序列 · 站点级。
- 门槛：**免费、匿名、无需 key**。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）——`/CityData/GetProvince` → 200 `application/json`（2,516 B，含北京 `Id:1/ProvinceCode:110000`…）；`/CityData/GetCitiesByPid?pid=1` → 200（`CityCode 110000 北京市`）；`/CityData/GetAQIDataPublishLive?cityName=北京市` → 200（站点级，万寿西宫站 `AQI 57 / PM2_5 25 / Quality 良`）；`POST /HourChangesPublish/GetCityRealTimeAqiHistoryByCondition?citycode=110000` → 200（8,538 B，24 条逐时）。`www.cnemc.cn/` → 200（首页含 `/getIndexData.do` POST 接口，**未单独实测**）。
- 上游：中国环境监测总站（发布单位页脚署名）；总站官网另有水质、土壤等栏目。

## 细节

- 站点结构：`/CityPublish/Index`（城市面板）、`/StationPublish/Index`（点位面板）、`/HourChangesPublish/Index`（24 小时趋势）由主页面 AJAX 载入；真正的数据端点在 `/CityData/*` 与 `/HourChangesPublish/*`。
- 时间字段是 .NET 格式 `/Date(1790874000000)/`（毫秒时间戳，UTC+8），另有 `TimePointStr`（如「02日01时」）可直接用。
- 总站官网 `www.cnemc.cn` 首页有 `POST /getIndexData.do`（参数 `localPlace`）返回 JSON，做站点检索辅助，**未单独实测**。

## 坑

1. **只有实时与近 24 小时/日序列**，没有长历史库；要年度/月度空气质量历史，改走生态环境部公报/年报（[`mee.gov.cn.md`](mee.gov.cn.md)）或第三方（如 aqistudy）。
2. 城市名参数是**中文市名**（`北京市`），不是代码；先 `GetCitiesByPid` 拿 `CityCode` 与 `CityName`。
3. URL 带非标准端口 **18007**，部分网络/代理会拦；证书记载日期较早的镜像地址可能失效。
4. 返回的是**监测点位**（一个城市多点位），城市值需自行聚合（取各点位均值或国控点），别把第一条当城市值。
5. 无官方频控声明，采集请自设 ≥1.5 s 间隔；整点后数分钟内数据才刷新。
