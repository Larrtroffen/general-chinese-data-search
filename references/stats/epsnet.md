# epsnet.com.cn —— EPS 宏观与区域数据平台

商业统计数据库群：EPS 数据平台（时间序列 + 统计表格）、中国微观经济数据查询系统、中国区域研究数据支撑平台、知图平台等。**订阅制 + 登录**（登录用阿里云验证码）；但**指标名联想接口匿名可用**，是"探指标口径/找指标名"的便宜入口。

- 去哪找：
  - 门户（hash 路由）`https://www.epsnet.com.cn/` → `https://www.epsnet.com.cn/index.html#/Index`；登录 `https://www.epsnet.com.cn/index.html#/Login`
  - 子平台（同一供应商、不同库）：`olap.epsnet.com.cn`（EPS 数据平台/OLAP 分析）、`kdd.epsnet.com.cn`、`crod.epsnet.com.cn`、`edp.epsnet.com.cn`、`zhitu.sozdata.com`（知图）、`microdata.sozdata.com`（中国微观经济数据查询系统）、`cnrrd.sozdata.com`（中国区域研究数据支撑平台）、`yreb.sozdata.com`、`www.dfinder.net`
  - 首页搜索框分「时间序列数据 / 统计表格数据」两类；热搜词：GDP、城镇新增就业人数、城镇调查失业率、CPI、粮食产量、单位GDP能耗
- 什么时候用：要**宏观时间序列**（GDP/CPI/财政/劳动/投资/房地产…）、**中国城市与区域面板**、**微观企业/住户调查数据**，或要先确认"这个指标在 EPS 里叫什么名字/什么口径"。
- 怎么搜：
  - **指标名联想（匿名可用，实测）**：
    ```bash
    curl -X POST 'https://www.epsnet.com.cn/search/recommendIndicator.do?keyword=GDP' \
      -H 'Referer: https://www.epsnet.com.cn/index.html'
    # → {"code":200,"message":"查询文档","data":{"hits":[{"indicatorName":"GDP","indicatorNameLen":3}, ...]}}
    ```
  - **检索页**：`https://www.epsnet.com.cn/searchPage.do`（前端 `urlMap.getEpsSearchPage`；直连无参 **500**，需会话/参数，本机未还原出可用参数）。
  - 其他前端接口（`https://www.epsnet.com.cn/`）：`GET /api/cubeStatNums?<rand>`、`GET /api/comgedata?sp=EPSZH_HOMEPAGE_2020&p=&v=`、`GET /api/comgedata?sp=News_GetList&p=PageIndex;newsitem&v=1;7`、`GET /ruoyi/cms/hotMenu/getAll`、`GET /ruoyi/cms/banner/getAll`、`GET /getDownloadTop?year=2026`；记账/导表类 `api/search/excel`、`api/custom/data`（需登录）。
- 覆盖：宏观经济、产业经济、贸易外经、区域经济、中国城市、城乡建设、能源环境、财政税收、劳动经济、住户调查、残疾人事业…；粒度=年度/季度/月度时间序列 + 统计表格；自述规模 **300 亿+ 时间序列、100 万+ 统计表格**（上游声明，首页）。更新频率随源库。
- 门槛：**订阅 + 登录**（`#/Login`；登录组件加载 `olap.epsnet.com.cn/send/alicdn/captcha-frontend/aliyunCaptcha/AliyunCaptcha.js`，即阿里云滑块/验证码）；机构账号为主。匿名仅首页与指标联想。
- 实测：2026-10-03，macOS arm64，curl 8.x + 无头 Chromium：`GET /` → 200/4,063 B（Vue SPA，最终 title `EPSDATA官网-宏观经济数据|区域经济数据|城市数据|微观经济数据`）；浏览器 XHR `/ruoyi/cms/hotMenu/getAll`、`/ruoyi/cms/banner/getAll`、`/api/cubeStatNums`、`/api/comgedata?...`、`/getDownloadTop?year=2026` 均 200；`POST /search/recommendIndicator.do`（无 keyword）→ 200 `{"code":500,"message":"请输入关键词"}`，带 `?keyword=GDP` → 200/14,246 B；`GET /searchPage.do` → **500**/626 B（服务端 bean 装配失败）。
- 上游：`https://www.epsnet.com.cn/`；接口清单来自 `https://www.epsnet.com.cn/js/app.*.js` 的 `urlMap`（本机实测读取）。

## 细节

### 实测明细（2026-10-03，macOS arm64，curl 8.x + 无头 Chromium）

- `GET https://www.epsnet.com.cn/` → **200**，4,063 B → 最终 `…/index.html`（Vue SPA，`<title>` 空，由 JS 填）；浏览器加载后 `location = https://www.epsnet.com.cn/index.html#/Index`，title = `EPSDATA官网-宏观经济数据|区域经济数据|城市数据|微观经济数据`。
- 浏览器抓到的 XHR：`/ruoyi/cms/hotMenu/getAll`、`/ruoyi/cms/banner/getAll`、`/api/cubeStatNums`、`/api/comgedata?...`、`/getDownloadTop?year=2026`（均 200）。
- `POST /search/recommendIndicator.do`（无 keyword）→ 200 `{"code":500,"message":"请输入关键词"}`；带 `?keyword=GDP` → **200**，14,246 B，返回 `hits[].indicatorName`（GDP/国内生产总值（GDP)/地区生产总值/本地生产总值…）。
- `GET https://www.epsnet.com.cn/searchPage.do` → **500**，626 B，`{"status":500,"error":"Internal Server Error","message":"Error creating bean with name 'pageSearchController'…"}`（服务端 bean 装配失败；非 UA/WAF 问题）。
- 首页搜索框由自定义组件包裹（`document.querySelectorAll('input')` 只返回 3 个无 placeholder 的隐藏项），脚本注入未触发检索 → 检索页参数**未在本机落实**。

## 坑

1. 站点是 hash 路由 SPA，深链要带 `index.html#/…`。
2. 登录网关与数据走同一域，但 OLAP 分析在 `olap.epsnet.com.cn`（若拿到机构账号，取数入口多半在那边，本机未验证）。
3. `searchPage.do` 现为服务端 500，别把它当"检索入口"写死。
