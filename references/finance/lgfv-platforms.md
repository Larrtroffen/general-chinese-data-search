# lgfv-platforms —— 城投债与地方政府融资平台数据

- 去哪找：
  - **中债城投口径**：中国债券信息网 `https://www.chinabond.com.cn/`、中债价格指标 `https://yield.chinabond.com.cn/`（城投债收益率曲线/估值；站点与取数情况见 `../business/chinabond.com.cn.md`）；统计月报 `https://www.chinabond.com.cn/yjfx/yjfx_zzfx/zzfx_yb/`
  - **评级报告公开区**：中诚信国际 `https://www.ccxi.com.cn/creditrating/result`（Vue SPA；实际调用匿名 JSON `https://website-api.ccxi.com.cn/admin/content/rating/page`）；联合资信 `https://www.lhratings.com/lists/107.html`（初始评级）、`/lists/111.html`（定期跟踪评级，列表直出 PDF）；东方金诚 `http://www.dfjc.com.cn/`（**本机被 WAF 拦，见坑 1**）
  - **审计署全国政府性债务审计**：站内检索 `https://www.audit.gov.cn/searchweb/`（POST `/searchweb/searchPic`）；2013 年第 32 号公告原文副本见辽宁省审计厅 `https://sjt.ln.gov.cn/sjt/zfxxgk/fdzdgknr/sjxxggbg/1AD22B61CCAA447E993202A08654F77D/index.shtml`
  - **债务限额/余额**：财政部债务管理司 `http://zwgls.mof.gov.cn/tjsj/`（月度《地方政府债券发行和债务余额情况》）、预算司 `http://yss.mof.gov.cn/`（年度债务余额情况表）；分地区、逐只券信息见 `localgov-debt.md`
- 什么时候用：要**城投口径**的发债主体/债券数据——城投债估值与收益率曲线、发债主体**评级报告原文**、政府性债务审计（2011/2013 两次全国专项 + 年度审计工作报告）、地方**债务限额/余额**公示、城投债募集说明书与信息披露；做城投平台研究、化债政策、地方财力与债务率分析。
- 怎么搜：官方**没有「城投债」法定分类**，需按「评级报告 → 发债主体 → 债券披露」三路拼，再决定是否上商业库（Wind/企业预警通/DM）。三条最小可复现操作：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 中诚信国际 匿名评级 JSON（SPA 实际调用端点，含 companyName/ratingDate/reportFileList）
  curl -s -A "$UA" 'https://website-api.ccxi.com.cn/admin/content/rating/page?pageNo=1&pageSize=3'
  # ② 审计署站内全文检索（POST，返回 JSON {num,array[]}）
  curl -s -A "$UA" -X POST 'https://www.audit.gov.cn/searchweb/searchPic' \
    -H 'Referer: https://www.audit.gov.cn/searchweb/' -H 'X-Requested-With: XMLHttpRequest' \
    --data 'fullText=政府性债务审计&pageNow=1&pageSize=10&sortType=0&searchType=0&keyType=fullText'
  # ③ 财政部债务管理司月度（HTML 列表 → 文章页）
  curl -s -A "$UA" 'http://zwgls.mof.gov.cn/tjsj/'
  ```
  结果形态：**JSON**（①②）、**HTML 列表 + 文章页**（③）；评级 PDF 为 `/uploads/file/{YYYYMMDD}/{g…}.pdf`（联合资信）或报告名文本（中诚信，需再拼 URL）。
- 覆盖：评级报告 = 中诚信/联合资信公开区（2010s–2026，含城投「地方政府相关」行业）；审计 = 2011 年第 35 号、2013 年第 32 号全国政府性债务审计（原文）+ 历年中央预算执行审计工作报告；债务限额/余额 = 全国月度（债务管理司，近 12 个月滚动）+ 年度表（预算司）+ 省级年度（见「细节」抽查）；城投债估值/曲线以中债披露为准。
- 门槛：评级机构公开区与政府站点**免费、免登录**；中诚信匿名 API 本机仅返回极少数公开记录（见坑 2），完整评级库疑需注册/授权；**城投名单与城投债分类口径只在商业库**（Wind/企业预警通/DM 等，见 `../business/commercial-databases.md`）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `GET https://website-api.ccxi.com.cn/admin/content/rating/page?pageNo=1&pageSize=3` → `200 application/json`，`data.total=11`，`records[0]` 为 `test` 样例、`records[1].companyName=安徽国贸集团控股有限公司`、`reportFileList` 内 `reportUrl` 为报告名 ✅
  - `GET https://www.lhratings.com/lists/107.html` → `200`（`<title>非金融企业`），页内 PDF 直链如 `/uploads/file/20260930/g361c733d12.pdf` → `200 application/pdf` 1.57 MB ✅
  - `POST https://www.audit.gov.cn/searchweb/searchPic`（`fullText=政府性债务审计`）→ `200 text/json`，`num` 有值、`array[]` 含标题/URL（如 2011 年《关于地方政府性债务审计的思考》）；但检索「全国政府性债务审计结果」**未命中 2013 年第 32 号公告正文**（官网未索引/已下线）⚠️
  - `GET https://sjt.ln.gov.cn/sjt/zfxxgk/fdzdgknr/sjxxggbg/1AD22B61CCAA447E993202A08654F77D/index.shtml` → `200`，`<title>全国政府性债务审计结果（2013 年12 月30 日公告）`，正文全文 ✅
  - `GET http://zwgls.mof.gov.cn/tjsj/` → `200`，最新《2026年8月地方政府债券发行和债务余额情况》`./202609/t20260924_3998108.htm` ✅；`GET https://yss.mof.gov.cn/2025zyczys/202503/t20250324_3960454.htm` → `200`（2024 和 2025 年地方政府专项债务余额情况表）✅
  - 省级抽查：`https://czt.gd.gov.cn/czysjs/index.html` `200`（广东财政预算决算）、`https://yjsgk.czt.gd.gov.cn/guangdong/portal/index` `200`（广东省级预决算公开平台）；`https://yjsgk.jsczt.cn/` `200/538B`（江苏预决算公开统一平台，SPA 壳）、`http://czt.jiangsu.gov.cn/col/col7774/index.html` `200`（江苏政府债务管理处）；`https://czt.zj.gov.cn/col/col1229887714/index.html` `200`（浙江政府预决算，列表 JS 载入）；`https://czt.ln.gov.cn/czt/zfxxgk/fdzdgknr/czyjs/czyjsbg/2026050610365723366/index.shtml` `200`（辽宁《2025年地方政府一般债务余额情况表》**HTML 表直出**）✅
  - `http://www.dfjc.com.cn/` → `200` 但正文为 **403 Forbidden** 拦截页；`https://www.dfjc.com.cn/` → `000`（443 拒连）❌
- 上游：`chinabond.com.cn`、`yield.chinabond.com.cn`（中债/中央结算公司）；`ccxi.com.cn`（中诚信国际）；`lhratings.com`（联合资信）；`dfjc.com.cn`（东方金诚）；`audit.gov.cn`（审计署）；`mof.gov.cn`（债务管理司 `zwgls`、预算司 `yss`）；各省财政厅（`czt.*.gov.cn`）。

## 细节

### 一、城投口径从哪来（三条路径）

| 路径 | 来源 | 得到什么 | 限制 |
|---|---|---|---|
| 中债行业分类 + 估值/曲线 | `chinabond.com.cn` / `yield.chinabond.com.cn` | 城投**类**发行人的债券估值、城投债收益率曲线、存量统计 | 取数接口本机未跑通（见 `../business/chinabond.com.cn.md`）；批量上商业库 |
| 评级报告 | 中诚信/联合资信/东方金诚官网 | 主体评级、评级方法（「政府相关」分类）、城投主体列表 | 东方金诚本机 WAF 拦；中诚信完整列表疑受限 |
| 债券披露 | 交易所（`bond.sse.com.cn` / 深交所债券披露）、银行间（`chinabond` / `shclearing.com.cn`）、交易商协会 | 募集说明书、发行文件、存续期披露（判断是否城投） | 无「城投」标签，需自建主体名单 |

**关键事实**：官方不发「城投名单」。研究常用口径：财政/银保监历史融资平台名单（未公开）、中债行业分类、评级机构「地方政府相关」分类，或商业库的城投债板块标签。

### 二、评级机构公开区

| 机构 | 入口 | 形态 | 实测 |
|---|---|---|---|
| 中诚信国际 | `https://www.ccxi.com.cn/creditrating/result`（评级结果发布）；`https://report.ccxi.com.cn/`（评级历史信息） | SPA + 匿名 JSON `https://website-api.ccxi.com.cn/admin/content/rating/page` | ✅ JSON 200（`total=11`，见坑 2） |
| 联合资信 | `/lists/107.html` 初始评级、`/lists/111.html` 定期跟踪、`/lists/48.html` 终止、`/lists/50.html` 主动 | HTML 列表 + **PDF 直链** `/uploads/file/{YYYYMMDD}/{g…}.pdf` | ✅ 200 / PDF 200 |
| 东方金诚 | `http://www.dfjc.com.cn/` | — | ❌ WAF 403（本机） |
| 大公国际 | `https://www.dagongcredit.com/` | HTML | ✅ 200（未深测） |
| 中证鹏元 | `https://www.pengyuan.com.cn/` | — | ❌ 本机 20 s 超时 |
| 新世纪评级 | `https://www.shxsj.com/` | — | ❌ 本机不可达（000） |

- 中诚信 JSON 记录字段：`id / companyName / creditLevel / ratingDate / issueDate / reportFileList`；`reportFileList` 为字符串化 JSON 数组，元素含 `reportType / isPay / reportUrl / ratingReportId`。
- 评级报告也在债券披露渠道留档：交易所债券公告、中国债券信息网、上清所披露页（可作为官网拿不到时的旁证）。

### 三、审计署站内检索

- 端点：`POST https://www.audit.gov.cn/searchweb/searchPic`，表单字段 `fullText / pageNow / pageSize / sortType / searchType / keyType(fullText|title)`；返回 `{num, array:[{name, url, showTime, summaries, jsfl}]}`。
- 门户检索页 `https://www.audit.gov.cn/searchweb/`（`var contextPath = "/searchweb"`）。
- 2013 年第 32 号公告、2011 年第 35 号公告在官网现行索引中**检不到**（旧链接 `…/n5/n25/c63642/content.html`、`…/c40850/content.html` 均已 `404`）；省审计厅与地方政府网转载副本仍在（辽宁样例见「去哪找」）。
- 现行对口栏目：`https://www.audit.gov.cn/n5/n25/index.html`（审计署公告及解读）、`https://www.audit.gov.cn/n5/n26/index.html`（审计工作报告及解读）。

### 四、地方「债务限额/余额」公示（抽查 3 省 + 直表样例）

| 省 | 入口 | 实测 |
|---|---|---|
| 广东 | 财政厅「财政预算决算」`https://czt.gd.gov.cn/czysjs/index.html`；省级预决算公开平台 `https://yjsgk.czt.gd.gov.cn/guangdong/portal/index` | ✅ 均 200 |
| 江苏 | 预决算公开统一平台 `https://yjsgk.jsczt.cn/`（SPA）；财政厅「政府债务管理处」`http://czt.jiangsu.gov.cn/col/col7774/index.html` | ✅ 200（平台为壳页，数据 JS 载入） |
| 浙江 | 财政厅「政府预决算」`https://czt.zj.gov.cn/col/col1229887714/index.html`（同层有「部门预决算」「预算执行」） | ✅ 200（列表 JS 载入） |
| 辽宁（直表样例） | 财政厅「财政预决算报告」`https://czt.ln.gov.cn/czt/zfxxgk/fdzdgknr/czyjs/czyjsbg/{id}/index.shtml` | ✅ 《2025年地方政府一般债务余额情况表》HTML 表直出 |

- 公示位置规律：省级多在**决算草案报告 / 预算调整方案报告的附件**（政府债务限额及余额情况表），栏目本身不单列；少数省份（如辽宁）把表直接发成 HTML。
- 全国口径优先：财政部**债务管理司**月度（`zwgls.mof.gov.cn/tjsj/`）+ **预算司**年度表（`yss.mof.gov.cn/`）；分地区指标走 `localgov-debt.md` 的 celma 平台。

### 五、只能从商业库拿的

| 需求 | 免费可得 | 商业库 |
|---|---|---|
| 城投主体名单 / 城投债标签 | 无官方名单 | Wind（城投债板块）、企业预警通 `qyyjt.cn`（✅ 200）、DM查债通 |
| 已清洗的城投债券面板（余额、到期、估值序列） | 逐只披露页自采 | Wind / CSMAR / CEIC；见 `../business/commercial-databases.md` |
| 中债城投债估值/曲线批量 | 页面可读、接口未跑通 | 中债数据服务、Wind |

## 坑

1. **东方金诚本机被 WAF 拦**：`http://www.dfjc.com.cn/` 返回 `403 Forbidden` 页（HTTP 200 但正文是拦截页），`https` 443 直接拒连；换 UA/协议无效，需真实浏览器（`../tools/agent-browser.md`），或改用其报告在交易所/银行间的披露副本。
2. **中诚信匿名 API 不是完整库**：`total=11` 且含 `test` 样例记录，疑为首页「最新评级」用的公开子集/测试租户；**不要据此判定「无某主体评级」**，完整列表需在浏览器抓真实分页参数或走官网注册。
3. **2013/2011 全国政府性债务审计原文已从审计署官网下线**（旧链 404、站内检索不命中）；引用时用省级审计厅/地方政府网转载副本，并注明转载来源与公告号，勿当官网原文。
4. **各省债务限额/余额藏在报告附件里**：不在独立栏目，且多为 PDF/附表；建议按「{省}财政厅 决算 政府债务限额及余额情况表」检索，并核对**预算数 vs 执行数**两列。
5. **口径三分别混**：中债（登记托管/估值）、上清所（清算托管/披露）、交易商协会（承销/发行统计）、交易所（上市债券披露）各管一段；城投债横跨银行间与交易所，缺一段会漏主体。
6. **`localgov-debt.md` 的平台是「地方政府债券」口径**（政府债），**不等于城投债**（企业信用债）；两者常被混称，引用前确认券种。
7. 审计署检索 `keyType=title` 对旧公告近乎无效（本机 `num=0`），用 `keyType=fullText` 更稳。
