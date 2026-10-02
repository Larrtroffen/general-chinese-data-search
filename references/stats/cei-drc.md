# cei-drc —— 中经网与国研网经济数据检索

合并卡：**中经网（国家信息中心·中经网数据有限公司）** 与 **国研网（国务院发展研究中心）**。共同点：全文检索（标题/摘要级）**匿名可读**，**数值数据与全文下载要订阅+登录**。放在 `stats/` 是因为它们是"统计数值 + 研究报告"的替代通道；研究报告类用法也见 `../media/`。

- 去哪找：中经网 `https://www.cei.cn/`、检索 `POST https://www.cei.cn/d/search/highSearch.action`、统计库 `https://db.cei.cn/`、中经数据 `https://ceidata.cei.cn/`；国研网 `https://www.drcnet.com.cn/`、检索 `https://search.drcnet.com.cn/advancedSearch?fields=2,20556&keyword={关键词}`、统计库 `https://data3.drcnet.com.cn/statistical`。
- 什么时候用：查中经网自己的动态/数表/报告（政策解读、宏观形势分析）与国研网的研究报告/财经资讯/案例/政策（可先拿命中数定位题）；查宏观指标数值（需订阅）。
- 怎么搜：见下 A（中经网 `highSearch`，**必须 POST**）与 B（国研网 `getSearchString`，匿名只给命中数）。
- 覆盖：中经网全站资讯/数表/报告 + 中经数据（自述"专注中国宏观经济统计数据 30 年"：经济数据 / 区域对比 / 人口数据 / 另类数据 / 资料馆 / 数据商城 / 知识&工具）；国研网研究报告、财经资讯、论文、案例、政策 + 统计数据（`data3`：宏观/地区/行业统计库）。
- 门槛：`www.cei.cn` 检索**匿名可用**（标题+日期+摘要）；`db.cei.cn`/`ceidata.cei.cn` 与国研网全部子平台要**注册/登录 + 订阅**（`db.cei.cn/jsps/Home` 只有「登录」「注册」两个按钮）。
- 实测：2026-10-03，macOS arm64，curl 8.x + 无头 Chromium；明细见下 A/B。
- 上游：`https://www.cei.cn/`、`https://db.cei.cn/`、`https://ceidata.cei.cn/`、`https://www.drcnet.com.cn/`、`https://search.drcnet.com.cn/advancedSearch`、`https://data3.drcnet.com.cn/statistical`。

## 细节

### A. 中经网 CEI（www.cei.cn）

- 去哪找：
  - 综合版门户 `https://www.cei.cn/`
  - **站内全文检索（POST，匿名可用）**：`https://www.cei.cn/d/search/highSearch.action`
  - 统计数据库 `https://db.cei.cn/`（JS 跳 `https://db.cei.cn/jsps/Home`）
  - 现代数据平台「中经数据」`https://ceidata.cei.cn/`（注册走 `passport.cei.cn/Action/DoView.ashx?view=UserRegister&appid=10011040`）
- 什么时候用：查**中经网自己的动态/数表/报告**（政策解读、宏观形势分析）→ 走 `highSearch`；查**宏观指标数值**（GDP/CPI/人口/海关/财政…）→ `ceidata.cei.cn` 的库。
- 怎么搜：
  ```bash
  # 必须 POST；GET 带 keywords 返回 0 篇（实测）
  curl -X POST 'https://www.cei.cn/d/search/highSearch.action' \
    -H 'Content-Type: application/x-www-form-urlencoded' -H 'Referer: https://www.cei.cn/' \
    --data-binary 'keywords=%E4%BA%BA%E5%8F%A3&columnId=&columntype=&sort=&b_date=&e_date=&coulnmName='
  ```
  - 表单字段：`keywords`（+ `columnId` / `columntype` / `sort` / `b_date` / `e_date` / `coulnmName` / `currentMaxScore` / `currentsearch`，来自首页 4 个 `<form action="/d/search/highSearch.action" method="post">`）。
  - 分类标签：全部 / 动态 / 数表 / 报告（页内 `#search_1..4`）。
  - 中经数据接口（浏览器实测）：`POST /VerfyLogin`（登录校验）、`POST /getMenulist`（`type=cube&cubeType=<库码>`：`qydb` 区域对比、`rkpc` 人口普查、`llsj_sjrk` 世界人口、`llsj_dfcz` 地方财政、`llsj_ssgs` 上市公司、`llsj_yhwd` 银行信贷、`haiguan` 海关）、`POST /getQQ?ajax=1`。
- 覆盖：中经网全站资讯/数表/报告 + 中经数据（自述"专注中国宏观经济统计数据 30 年"：经济数据 / 区域对比 / 人口数据 / 另类数据 / 资料馆 / 数据商城 / 知识&工具）。
- 门槛：`www.cei.cn` 检索**匿名可用**（标题+日期+摘要）；`db.cei.cn` 与 `ceidata.cei.cn` 数值数据要**注册/登录 + 订阅**（`db.cei.cn/jsps/Home` 只有「登录」「注册」两个按钮）。
- 实测（2026-10-03，macOS arm64，curl 8.x + 无头 Chromium）：
  - `GET https://www.cei.cn/` → **200**，154,290 B，`<title>中国经济信息网</title>`。
  - `GET /d/search/highSearch.action?keywords=人口` → 200 但「找到 **0** 篇」「当前检索关键字为:」（空）→ 参数未生效。
  - `POST /d/search/highSearch.action`（body 同上）→ **200**，23,695 B，「当前检索关键字为: 人口」「找到 **235598** 篇」「第1页/共23560页」，条目含标题+日期+摘要。
  - `GET https://db.cei.cn/` → 200，243 B（`window.location="jsps/Home"`）；`GET https://db.cei.cn/jsps/Home` → **200**，14,163 B，`<title>中经网统计数据库</title>`，页内 `GoToLogin()` / `GoToRgister()`，引 `/css/ceidata_search.css`，外链 `https://ceidata.cei.cn`。
  - `GET https://ceidata.cei.cn/` → **200**，13,301 B，title `中经数据-专注中国宏观经济统计数据30年`；XHR 见上（均 200，匿名）。
- 上游/出处：`https://www.cei.cn/`、`https://db.cei.cn/`、`https://ceidata.cei.cn/`。

### B. 国研网 DRCNet（drcnet.com.cn）

- 去哪找：
  - 综合版 `https://www.drcnet.com.cn/`（Vue SPA + fingerprintjs 指纹风控）
  - **研究检索**（由旧 `s1.drcnet.com.cn/search/SearchAdvanced.aspx` **302** 而来）：`https://search.drcnet.com.cn/advancedSearch?fields=2,20556&keyword={关键词}`
  - 统计数据库「国研网统计数据查询分析平台」：`https://data3.drcnet.com.cn/statistical`
  - 其他子平台：`report.drcnet.com.cn`（系列研究报告）、`expert.drcnet.com.cn`（专家）、`government/edu/trade/thinktank/carbon/caselib/company.drcnet.com.cn`、详情页域 `d.drcnet.com.cn`
- 什么时候用：查国研网的**研究报告/财经资讯/案例/政策**（`search.drcnet.com.cn`，可先拿到命中数定位题）；查**统计数据**（`data3.drcnet.com.cn`，登录后）。
- 怎么搜：
  ```bash
  curl -X POST 'https://search.drcnet.com.cn/search/getSearchString/' \
    -H 'Content-Type: application/json' -H 'Referer: https://search.drcnet.com.cn/' \
    --data-binary '{"attrIndex":"","curpage":1,"pagesize":"10","lisQuery":[{"queryBoolType":1,"queryItem":"1","queryOperator":2,"queryString":"人口"}],"startTime":"","endTime":"","catalogName":"","rootlm":"0","resultType":5,"lisLeafidCase":[],"chnId":0,"sortOrder":"desc","sortField":"_score"}'
  ```
  - `resultType`：实测取值 5 / 6（对应不同文献类型组，页面另有 全部/资讯/论文/报告/案例/政策 筛选）；分面接口 `POST https://search.drcnet.com.cn/search/getLeftTree/?chnId=0`。
  - 详情页形态：`https://d.drcnet.com.cn/eDRCnet.common.web/DocDetail.aspx?chnid=<n>&leafid=<n>&docid=<n>&uid=<n>&version=integrated`（从首页文章链接直接读到）。
- 覆盖：研究报告、财经资讯、论文、案例、政策 + 统计数据（`data3`：宏观/地区/行业统计库）。
- 门槛：**匿名只能拿到命中数与分面**（`hits.hits` 为空）；文档列表与全文要登录（`user.drcnet.com.cn/userapi/loginController/initLoginP`）+ 订阅；`data3` 统计平台整站需登录。
- 实测（2026-10-03，macOS arm64，curl 8.x + 无头 Chromium）：
  - `GET https://www.drcnet.com.cn/` → **200**，5,226 B，`<title>国研网-综合版</title>`；浏览器加载后首页搜索框（「搜索类型」下拉 + 「请输入关键词」），键入并回车**未**跳转（受控组件 + 指纹风控，脚本注入未触发）。
  - `GET http://s1.drcnet.com.cn/search/page.aspx?fields=0,20556&rootlm=20556&keyword=人口` → **404**（nginx；旧路径已废）。
  - `GET http://s1.drcnet.com.cn/search/SearchAdvanced.aspx?fields=2,20556&keyword=人口` → **200**（2,372 B，`<title>国研网检索</title>`），但 `curl` 报最终 URL 已是 `https://search.drcnet.com.cn/advancedSearch?…`（Vue SPA 需 JS）。
  - `POST https://search.drcnet.com.cn/search/getSearchString/`（body 同上，queryString=人口）→ **200**，761 B，ES 风格：`hits.total.value=21885`、`aggregations.sterms#classification1=14`、**`hits.hits=[]`**（登录后才有条目）。
  - `GET https://data3.drcnet.com.cn/statistical` → **200**，810 B（SPA 壳，`<title>国研网统计数据查询分析平台</title>`）；浏览器打开后 body 文本为空，仅见 `user.drcnet.com.cn/…/initLoginP`（登录探针）→ 需登录。
  - `GET https://iap.drcnet.com.cn/` → **200**，2,369 B，`<title>思政信息资源平台</title>`（原"统计资料库平台"入口已改，别按旧说明用）。
- 上游/出处：`https://www.drcnet.com.cn/`、`https://search.drcnet.com.cn/advancedSearch`、`https://data3.drcnet.com.cn/statistical`。

### 选型

- 只要**列表级线索**（有几篇、标题日期）：中经网 `highSearch`（匿名能出条目）优先；国研网 `getSearchString` 只有命中数。
- 要**数值**：先看 `data.stats.gov.cn.md`（官方免费）→ 不够再考虑 CEI/DRC/EPS/CNKI 四家订阅库（`epsnet.md`、`cnki-data.md`）。
- 要**研究报告全文**：国研网/中经网都要订阅；免费替代见 `../media/` 与 `../gov/`。
