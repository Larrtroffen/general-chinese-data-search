# data.cnki.net —— 知网统计年鉴数据库

知网旗下的**统计数据**平台（不是论文库；论文库见 `../academic/cnki.net.md`）：收录统计年鉴、统计公报、普查资料、资料汇编、分析报告的**表格级**数据，按指标检索/组配/可视化。**订阅制 + 强制登录**：匿名只能看首页，检索接口直接 471（登录态专用状态码）。

- 去哪找：
  - 门户 `https://data.cnki.net/`（SPA，React；接口前缀 `/api/csyd/`，全 POST JSON）
  - 检索结果页 `https://data.cnki.net/valueSearch/index?ky={URL编码关键词}`
  - 分区：统计资料 `./yearBook`（统计年鉴）、`./censusBulletin`（普查公报）、分析报告/资料汇编/调查资料/统计摘要/统计公报（首页导航同级）；数据分析 `./yearData`（年度）、`./seasonOrMonth`（进度）、`./internationalData`（国际）、`./themeAnalysis/analysis`（专题）；决策支持 `./decision/methods/{regressionAnalysis|timeSeriesTrendPredict|ahp|zoneDecision}`；AI 知数 `./aidata`、`./aidata/dataAsk`
  - 行业版 `./trade/home?zcode=Z001…Z031`；地域版 `./area/home`
  - 另一条产品线：`https://apidata.cnki.net/ds`（API 数据服务）、`https://zhifou.cn/`（知否）
- 什么时候用：要**年鉴表格里的具体数值**（"分省 GDP 1978–2024""城镇单位就业人员平均工资""人口普查分年龄性别"）、要按**指标名**跨年鉴检索、要"某指标在全国各省历年"的组配表。要论文本身 → `../academic/cnki.net.md`。
- 怎么搜：
  1. **人读**：`https://data.cnki.net/valueSearch/index?ky=%E4%BA%BA%E5%8F%A3` → 匿名会被 302 到 `login.cnki.net`。
  2. **接口（登录态下）**：
     ```bash
     curl -X POST 'https://data.cnki.net/api/csyd/ValueSearch/GetOneBoxSearch' \
       -H 'Content-Type: application/json' -H 'Referer: https://data.cnki.net/valueSearch/index' \
       --data-binary '{"kd":"人口","area":"","dataType":"year","endYear":0,"beginYear":0,"searchModeOne":0,"sort":0,"groupSearchCon":"","groupType":"","currentPage":1,"pageSize":20,"albumCode":"","type":""}'
     ```
     同一 body 还有分面接口 `POST /api/csyd/ValueSearch/GetGroupList`。
  3. **指标名联想**（首页搜索框即走这个）：`POST /api/csyd/Home/GetIndicateList`，body `{"ky":"人口"}` → 匿名 200 但 `count:0`、`searchPointOutItems:[{"indicate":"Null"}]`；登录后返回指标候选。
- 覆盖：统计年鉴 / 统计公报 / 普查资料 / 调查资料 / 资料汇编 / 分析报告 + 国际数据 + 专题库（能源、科技、数字经济、卫生健康、乡村振兴、环境、县域、金融、城市、财政…）；粒度=指标×地区×年（月/季/年）；更新=随年鉴出版与月度进度数据。
- 门槛：**订阅 + 登录**。机构登录（单位名+密码）与个人登录（用户名/密码或手机+短信验证码）两条路，登录页 `https://login.cnki.net/login/?returnurl=…`；未登录请求检索接口返回 **HTTP 471**（自定义"需登录"码），前端随即跳登录页。机构 IP 直连可免密（上游通例，本机未验证）。
- 实测：2026-10-03，macOS arm64，curl 8.x + 无头 Chromium，桌面 UA，同主机间隔 ≥1.5s：首页 200/11,409 B；浏览器首页 XHR 全为 POST `/api/csyd/*`（`Version/GetVersion`、`Navs/IndustryPartial`、`Home/BannerPicList`、`Home/GetNewOnline`、`Home/GetThemeList`、`Home/GetMessageCenterList`，均 200）；搜索框键入「人口」→ `POST /api/csyd/ValueSearch/GetOneBoxSearch` **HTTP 471**，页面转 `login.cnki.net`；`POST /api/csyd/Home/GetIndicateList` body `{"ky":"人口"}` → 200 `{"count":0,…}`（匿名无指标数据）；`GET /yearBook` → 200/4,266 B（SPA 壳）。
- 上游：`https://data.cnki.net/`（产品自述：多源异构统计大数据、统计年鉴/公报、指标抽取、组配分析、可视化驾驶舱）；接口名与参数取自首页 bundle 与实际 XHR（本机实测）。

## 细节

### 实测明细（2026-10-03，macOS arm64，curl 8.x + 无头 Chromium）

- `GET https://data.cnki.net/` → **200**，11,409 B，`<title>中国经济社会大数据研究平台</title>`（SPA 壳，含 antd chunk `/static/js/home/home.*.chunk.js`）。
- 浏览器加载首页 → XHR 全为 POST `/api/csyd/*`：`Version/GetVersion`、`Navs/IndustryPartial`、`Home/BannerPicList`、`Home/GetNewOnline`、`Home/GetThemeList`、`Home/GetMessageCenterList`（200）。
- 首页搜索框键入「人口」回车 → 浏览器跳到 `https://data.cnki.net/valueSearch/index?ky=%E4%BA%BA%E5%8F%A3`，随即 `POST /api/csyd/ValueSearch/GetOneBoxSearch` → **HTTP 471**（空 body），`POST …/GetGroupList` 同，页面转 `login.cnki.net`。
- `POST /api/csyd/Home/GetIndicateList` body `{"ky":"人口"}` → **200**，`{"count":0,"isSuccess":true,"data":[{"name":"统计指标","searchPointOutItems":[{"indicate":"Null"}]}]}`（查询串形式 `?ky=人口` 同结果）→ 匿名无指标数据。
- `GET https://data.cnki.net/yearBook` → **200**，4,266 B（SPA 壳，title 同首页；内容需 JS+登录）。

## 坑

1. 与论文库 `cnki.net` 同域不同产品，别混用检索式。
2. 接口是 POST + `/api/csyd/` 前缀，GET 变体一律回落 SPA HTML。
3. 471 不是标准码，脚本要单列判断。
4. 搜索框是 React 受控组件，脚本注入值需用原生 value setter + Enter 才会触发（实测）。
5. 年鉴表格是**平台结构化数据**，不是扫描图，登录后可直接导表（`api/search/excel` 类接口在同域 EPS/CNKI 均有，未在本平台实测）。
