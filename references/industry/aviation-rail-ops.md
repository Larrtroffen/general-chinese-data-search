# aviation-rail-ops —— 航班轨迹与铁路运行细项

- 去哪找：
  - **OpenSky Network REST API**（ADS-B 航班状态向量，匿名可用）`https://opensky-network.org/api/states/all`；接口文档 `https://openskynetwork.github.io/opensky-api/rest.html`
  - **民航局 统计报表平台** `https://stats.caac.gov.cn/ZHTJ`（DNA 报表引擎，需浏览器）
  - **中国民航网·正常率统计** `http://www.caacnews.com.cn/1/1/{YYYYMM}/t{YYYYMMDD}_{id}.html`（月度航空公司/主要机场放行正常率）
  - **国家铁路局 行业统计** `http://www.nra.gov.cn/xwzx/zlzx/hytj/`（月度《全国铁路主要指标完成情况》+ 年度《铁道统计公报》）；**国铁集团** 数据服务 `http://www.china-railway.com.cn/wnfw/sjfw/`
  - 铁路/民航/城轨的**基础入口（民航月度生产、年度公报、城轨年报）见 `rail-aviation.md`**；城市客运量见 `express-logistics.md`
- 什么时候用：要**航班实时状态/轨迹**（经纬度、高度、速度、呼号、ICAO24）；要**航班正常率 / 放行正常率**逐月分航司分机场；要铁路客货运量、里程、机辆的月度**细项**与年度公报明细；要城市轨道客运量。
- 怎么搜：OpenSky 直接 GET（经纬度 bbox）返回 **JSON**；民航局报表平台是 JS 会话 POST（脚本难）；正常率与铁路是静态 HTML 列表，改年月段即可：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① OpenSky 匿名取某框内实时航班状态向量（time 参数匿名被忽略）
  curl -sS -A "$UA" 'https://opensky-network.org/api/states/all?lamin=50.0&lomin=6.0&lamax=51.0&lomax=7.0'
  # ② 中国民航网月度正常率统计
  curl -sS -A "$UA" 'http://www.caacnews.com.cn/1/1/202603/t20260302_1393587.html'
  # ③ 国家铁路局月度主要指标 / 国铁集团月度指标
  curl -sS -A "$UA" 'http://www.nra.gov.cn/xwzx/zlzx/hytj/202609/t20260918_352059.shtml'
  curl -sS -A "$UA" 'http://www.china-railway.com.cn/wnfw/sjfw/202609/t20260909_159614.html'
  ```
  结果形态：OpenSky = **JSON**（`time` + `states[]`）；民航正常率/铁路 = HTML 正文表（民航公报常附 PDF）；民航局报表平台 = 需 JS 会话的 HTML。
- 覆盖：OpenSky 匿名**仅最近状态向量**（实时快照，10 s 分辨率，`time` 参数被忽略）；民航正常率**月度**（2026 各月，分航司与主要机场）；铁路 = 月度主要指标（近 12 个月滚动）+ 年度《铁道统计公报》与国铁集团《国家铁路主要指标完成情况》；城轨 = 年度。
- 门槛：OpenSky **匿名免费、无 key**（限额见下）；民航局报表平台 **需浏览器**（JS 会话）；正常率/铁路/国铁 **免费、免登录**。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `GET opensky-network.org/api/states/all?lamin=50.0&lomin=6.0&lamax=51.0&lomax=7.0` → **200**，951 B，`application/json`，`time=1790964278`，`states` **7 条**（含 `icao24/callsign/origin_country/longitude/latitude/baro_altitude/velocity/…`）✅
  - `GET openskynetwork.github.io/opensky-api/rest.html` → **200**，64 KB；文档载明匿名用户「仅最近状态向量、10 s 分辨率、400 credits/日」✅
  - `GET stats.caac.gov.cn/ZHTJ` → **200**，891 B（GBK），返回 JS 提交表单（隐藏 `sessionId`/`verificationCode`）；`POST /ZHTJ/` → **200**，1 490 B，返回 `dnaserver?serviceId=…` 的 DNA 报表引擎脚手架 ⚠️（需浏览器执行 JS）
  - `GET caacnews.com.cn/1/1/202603/t20260302_1393587.html` → **200**，62 KB，title《统计｜2026年1月国内客运航空公司、主要机场正常率统计结果》，正文含「平均放行正常率 95.95%（同比 +1.52 pp）」✅
  - `GET nra.gov.cn/xwzx/zlzx/hytj/` → 302→**200**，45 KB，title「行业统计_国家铁路局」，含月度《2026年8月份全国铁路主要指标完成情况》`./202609/t20260918_352059.shtml` 与《2025年铁道统计公报》`./202605/t20260529_351347.shtml` ✅
  - `GET china-railway.com.cn/wnfw/sjfw/`（**HTTP**）→ **200**，18 KB，列出 2026 各月《国家铁路主要指标完成情况》（如 1-8 月 `./202609/t20260909_159614.html`）✅
- 上游：OpenSky Network `opensky-network.org`；中国民用航空局 `caac.gov.cn` / 中国民航网 `caacnews.com.cn`；国家铁路局 `nra.gov.cn`；中国国家铁路集团 `china-railway.com.cn`；中国城市轨道交通协会见 `rail-aviation.md`。

## 细节

### 一、OpenSky Network（匿名 ADS-B）

- 主端点 `GET https://opensky-network.org/api/states/all`，参数：

| 参数 | 含义 |
|---|---|
| `lamin`/`lomin`/`lamax`/`lomax` | 经纬度包围盒（**建议必给**，否则返回全量、耗额度） |
| `icao24` | 单机 24 位地址（可逗号多值） |
| `time` | Unix 秒；**匿名用户被忽略**，仅认证用户可用 |
| `extended=1` | 额外字段（见文档） |

- 返回：`{"time":<unix>,"states":[[icao24, callsign, origin_country, time_position, last_contact, longitude, latitude, baro_altitude, on_ground, velocity, true_track, vertical_rate, sensors, geo_altitude, squawk, spi, position_source], …]}`。
- 其他端点（文档声明）：`GET /states/own`（自有接收机，不计费）、`GET /flights/aircraft?icao24=&begin=&end=`、`GET /flights/arrival?airport=&begin=&end=`、`GET /flights/departure?airport=&begin=&end=`、`GET /tracks?icao24=&time=0`。
- **限额（上游文档，未本机压测）**：匿名 **400 credits/日**，标准用户 4 000/日；`/states/*`、`/tracks/*`、`/flights/*` 三个额度桶相互独立；匿名仅最近状态向量、分辨率 10 秒（`now - now mod 10`），认证后可达 1 小时历史、5 秒分辨率（`t < now-3600` 返回 400）。

### 二、民航正常率（中国民航网）

- 栏目 `民航局` = `http://www.caacnews.com.cn/1/1/`；月度《统计｜{年}月国内客运航空公司、主要机场正常率统计结果》，URL 形态 `/1/1/{YYYYMM}/t{YYYYMMDD}_{id}.html`。
- 内容：国内主要机场按旅客吞吐量分档（≥1%、0.2%–1%）给出平均放行正常率；分航空公司给出正常率；正文明细表（HTML）。
- 民航局官方月度生产指标（《中国民航{年}月份主要生产指标统计》）在 `caac.gov.cn/XXGK/XXGK/TJSJ/index_1215.html`；年度行业发展统计公报与机场生产公报见 `rail-aviation.md`。

### 三、铁路月度细项 URL 形态

| 主题 | 入口 | 文章 URL |
|---|---|---|
| 铁道月度主要指标（部委口径） | `nra.gov.cn/xwzx/zlzx/hytj/` | `…/hytj/{YYYYMM}/t{YYYYMMDD}_{id}.shtml`（正文表格） |
| 铁道统计公报（年度，含明细） | 同上 | `…/hytj/{YYYYMM}/t{YYYYMMDD}_{id}.shtml` + `P0….pdf` |
| 国家铁路主要指标（企业口径，累计） | `china-railway.com.cn/wnfw/sjfw/` | `…/sjfw/{YYYYMM}/t{YYYYMMDD}_{id}.html`（**仅 HTTP**） |

- 国铁集团列表首页只滚近 12 个月，历史翻页 `index_2.html`… 或按年月段拼 URL。
- 「细项」指公报正文/PDF 内的分指标表：客运量、旅客周转量、货运量、货物周转量、换算周转量、机车车辆与线路里程等。

### 四、城轨与城市客运

- 城轨年度《城市轨道交通统计和分析报告》见 `rail-aviation.md`（`camet.org.cn`，注意正文站本机 504、附件 OSS 可取）。
- 城市/城际客运量月度见交通运输部（`express-logistics.md`，正文附 xlsx）。

## 坑

1. **OpenSky 匿名取不到历史**：`time` 参数被匿名用户忽略，只能拿「最近 10 秒」快照；要历史轨迹/航班须注册账号（OAuth2 client credentials）提限额并解锁 1 小时状态与 `/tracks`。
2. **不给 bbox 会拉全量**：`/states/all` 无参数返回全球所有状态向量（响应巨大且消耗额度），抓取务必带 `lamin/lomin/lamax/lomax`。
3. **额度分桶**：`states`/`tracks`/`flights` 各自独立计费，`/states/own` 不计费；批量轮询前算好额度（匿名 400/日）。
4. **民航局报表平台非 HTTP 可取**：`stats.caac.gov.cn/ZHTJ` 先返回 JS 表单、POST 后返回 DNA 引擎脚手架，纯 `curl` 拿不到报表数据——只能浏览器渲染（或按「主要生产指标统计」文章口径走 `rail-aviation.md`）。
5. **正常率是分航司/分机场的月度统计**，与民航局《主要生产指标》（总量）口径不同；且机场分档按上年吞吐量划分，跨年比较先看分档。
6. **铁路月度是「完成情况」累计值**（1-N 月），拿单月须相邻两期相减；部委（国家铁路局）与企业（国铁集团）两套口径勿混用。
7. **国铁集团只认 HTTP**：`https://www.china-railway.com.cn/` 握手失败，用 `http://` 同域。
8. **勿在本卡重复 `rail-aviation.md` 已收的入口**（民航月度/公报、铁道公报、城轨年报）；本卡只补 ADS-B、正常率、报表平台与新 URL 形态。
