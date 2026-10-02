# procurement —— 招投标与政采公告批量回溯

本卡聚焦**历史回溯与批量取数（语料化）**：国家级平台怎么绕、省级平台分几种血统、商业网各能回溯到哪一年。
**检索接口本身的字段细节见 `../gov/ccgp-ggzy.md`**（ccgp 检索 URL 模板与 ggzy `getTradList`），本卡不重复。

- 去哪找：
  - **中国招标投标公共服务平台**（国家发改委指导，2015 上线）：门户 `https://www.cebpubservice.com/`；**交易公开检索端 `https://ctbpsp.com/`**（首页搜索框直接跳 `https://ctbpsp.com/#/bulletinList?keyWords=<kw>`，详情 `#/bulletinDetail?uuid=<uuid>`）；公告公示/世行亚开行专区 `http://bulletin.cebpubservice.com/`；**付费「信息API服务」** `http://www.cebpubservice.com/webapi/index.html`。
  - **省级**（实测 6 省）：北京 `https://ggzyfw.beijing.gov.cn/`；上海 `https://www.zfcg.sh.gov.cn/`；浙江 `https://zfcg.czt.zj.gov.cn/`；广东 `https://gdgpo.czt.gd.gov.cn/`；江苏 `http://www.ccgp-jiangsu.gov.cn/`（必须 http）；湖北 `https://www.ccgp-hubei.gov.cn/`。
  - **商业招标网**：千里马 `https://www.qianlima.com/`（检索端 `https://search.qianlima.com/`）；中国采招网 `https://www.bidcenter.com.cn/`；比地招标 `https://mvip.bidizhaobiao.com/`。
- 什么时候用：
  - 要**某关键词的历史全量公告**（如"服务器""污水处理"）做语料/事件研究 → 千里马匿名 JSON 或北京 JSON 接口，再按年/省细分。
  - 要**某省某年某类的政采/工程公告** → 先查该省平台血统（政采云 / gpcms / 自建，见 `## 细节`）。
  - 要**国家级口径的项目/中标业绩覆盖统计** → 中国招标投标公共服务平台（含付费 API）。
  - 要**竞对中标历史/中标金额趋势** → 商业网（千里马/比地/知了标讯），免费额度极小。
  - 不适用：只要某一条公告的**接口字段规范** → `../gov/ccgp-ggzy.md`；要工商/信用主体 → `../gov/gsxt.md`、`../gov/credit-china.md`。
- 怎么搜：
  - **北京（实测打通的省级 JSON 接口）**——检索页 `https://ggzyfw.beijing.gov.cn/elasticsearch/index.jsp?searchAll=<kw>` 只是壳，真接口是：
    ```bash
    curl -sS -m 20 -A "$UA" -X POST \
      -H 'Referer: https://ggzyfw.beijing.gov.cn/elasticsearch/index.jsp' \
      --data-urlencode 'searchword=服务器' --data 'page=1' --data 'size=20' --data 'sort=' \
      'https://ggzyfw.beijing.gov.cn/elasticsearch/search'
    # → {"total":6023,"page":1,"result":"[{\"title\":…,\"releaseDate\":\"2026-09-30\",\"link\":\"/jyxxcggg/…\"}]"}
    # 注意 result 是「二次编码」的 JSON 字符串，要 json.loads 两次
    ```
    同族字段还有 `scope / channel_first…fourth / starttime / endtime / legislationType / ext`（来自页面内联 JS 的 `$.ajax`）。
  - **千里马（匿名 JSON，实测可翻页）**——`POST https://search.qianlima.com/api/v1/website/search?<查询串>`，body 传 `{}`：
    ```bash
    curl -sS -m 20 -A "$UA" -X POST -H 'Referer: https://search.qianlima.com/' -d '{}' \
      'https://search.qianlima.com/api/v1/website/search?keywords=服务器&currentPage=100'
    # → 200 {"code":200,"data":{"rowCount":372632,"pagesCount":18632,"data":[{contentid,progName,updateTime,url,originUrl,areaName,popTitle,…}]}}
    ```
    分页参数是 **`currentPage`**（不是 `page`/`pageSize`；实测 `page=100` 被忽略仍返第 1 页，`currentPage=100` 生效）；每页固定 20 条。同域另有 `api/v1/website/advance/search`（高级）、`api/v1/website/bid`（招标）、`api/v1/website/provider`。
  - **中国招标投标公共服务平台**：检索端 `ctbpsp.com` 为 Vue SPA，XHR 已从 `app.2457519d.js` 提取（`/cutominfoapi/searchkeyword?...`、`/cutominfoapi/bulletin/<uuid>/uid/<uid>/token/<v>`），**但本机 curl 被阿里云 WAF JS 挑战拦住（见实测），只能真浏览器**。
  - **政采云系省网**（上海/浙江等）：前端由 `zcycdn.com` / `luban.zcycdn.com` 组件拼装，公告列表 JS 渲染，本机未挖到匿名检索接口 → **仅浏览器**。
  - **gpcms 系省网**（广东/四川/江西/甘肃/黑龙江/海南/内蒙/陕西）：SPA + 网关 `/gateway/gpcms/rest/web/v2/…`（`info/selectInfoMoreChannel`、`info/getInfoById`、`index/selectInfoByOpenTenderCode`），需按页面参数调用。
  - **自建 CMS 省网**：江苏公告检索 `/jiangsu/cggg_search.html`（带图形验证码 `validateCode`）、湖北 `https://www.ccgp-hubei.gov.cn:9040/quSer/newSearch`（POST 本机 500，需按页面表单）。
- 覆盖：国家级 + 31 省 + 央企/部委；类型含招标公告、资格预审、中标候选人公示、中标/成交结果、更正、终止、合同；领域政采/工程/土地/矿业权/产权等（ggzy 口径见 `../gov/ccgp-ggzy.md`）。粒度=单条公告，正文静态/半静态 HTML。更新按日。
- 门槛：**公共平台免费但门槛在"能不能过反爬"**——ctbpsp 阿里云 WAF、政采云/gpcms JS 渲染、江苏图形验证码；北京与千里马检索端可匿名 curl。**历史库、Excel 打包、API 均属商业付费**（千里马 7999–21999 元/年，或议价）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA。`GET https://www.cebpubservice.com/` → **200/168 447 B**（`<title>中国招标投标公共服务平台</title>`，http/https 同）；`POST https://ctbpsp.com/cutominfoapi/searchkeyword?keyword=服务器&…` 与 `GET /cutominfoapi/recommand/type/5/pagesize/10/currentpage/1` → 均 **200 但 26 913 B 阿里云 WAF JS 挑战页**（`text/html`，`function M(){var GH=[…]}`）；`GET http://www.cebpubservice.com/webapi/index.html` → 200/20 192 B（「信息API服务」页，宣称 3000 万+ 公告公示）。北京 `POST /elasticsearch/search` → **200 JSON `total=6023`**，首条「北京市海淀区…公开招标公告」、`releaseDate=2026-09-30`、`link=/jyxxcggg/20260930/5735005.html`。省级首页：上海 200/133 860 B、浙江 200/105 260 B（均政采云前端）、广东 200/2 104 B（SPA）、四川 200（`data-tag=…gpcms-center-web`）、江苏 http 200/76 676 B、湖北 200/111 436 B；山东 `ggzyjy.shandong.gov.cn` → **502**。千里马 `POST search.qianlima.com/api/v1/website/search?keywords=服务器&currentPage=100` → **200 JSON `rowCount=372 632`、`pagesCount=18 632`**，20 条/页，条目含 `contentid=635987583`、`updateTime=2026-09-30`、`url=https://www.qianlima.com/bid-<id>.html`。中国采招网检索 `https://search.bidcenter.com.cn/search?keywords=服务器&type=0&mod=0` → **被跳转 `shuju.bidcenter.com.cn/HumanMachineVerificationTest4.shtml`（人机验证）**。比地 `POST https://api.bidizhaobiao.com/bidList.do` → 200 `{"status":"20000","info":"传参错误！"}`（接口活着、参数未解）。详见 `## 细节`。
- 上游：中国招标投标公共服务平台 <https://www.cebpubservice.com/>；千里马会员服务页 <https://vip.qianlima.com/tradeCenter_Service.html>；北京市公共资源交易服务平台 <https://ggzyfw.beijing.gov.cn/>。

## 细节

### 省级平台三种血统（实测 6 省）

| 省 | 站点 | 血统 | 检索 | 本机 curl |
|---|---|---|---|---|
| 北京 | `ggzyfw.beijing.gov.cn` | 自建 CMS + Elasticsearch | `POST /elasticsearch/search` | ✅ JSON（`total`/`result` 二次编码） |
| 江苏 | `www.ccgp-jiangsu.gov.cn`（**http**） | 自建 CMS | `/jiangsu/cggg_search.html` + 图形验证码 | ⚠️ 页面可达、检索需验证码 |
| 湖北 | `www.ccgp-hubei.gov.cn` | 自建 CMS（`gpmispub` JSP） | `:9040/quSer/newSearch`；列表 `:8090/gpmispub/*List.jsp` | ⚠️ POST 500 |
| 广东 | `gdgpo.czt.gd.gov.cn` | **gpcms 政府采购智慧云平台** | `/gateway/gpcms/rest/web/v2/…` | ⚠️ SPA，需按页面参数 |
| 四川 | `www.ccgp-sichuan.gov.cn` | **gpcms**（`data-tag` 同款） | 同上 | ⚠️ 同上 |
| 上海 | `www.zfcg.sh.gov.cn` | **政采云（zcygov）SaaS** | 前端 `zcycdn.com`/`luban.zcycdn.com` 组件 | ❌ JS 渲染 |
| 浙江 | `zfcg.czt.zj.gov.cn` | **政采云 SaaS** | 同上 | ❌ JS 渲染 |

- gpcms 系（同一套 Web 应用多省复用，`app.js` 路由里直接带 **广东/甘肃/黑龙江/海南/江西/内蒙/陕西** 各省栏目名）：基址 `APIBaseUrl_noGetWay` + `rest/web/v2/info/selectInfoMoreChannel`（列表）、`info/getInfoById`、`index/selectInfoByOpenTenderCode`；网关前缀 `/gateway/`（`config.js` 里 `GATE_WAY_KEY:"gateway"`）。
- 政采云系：省网只是壳，公告正文/列表由 `middle.zcygov.cn` / 站内 XHR 提供；`middle.zcygov.cn/front/search/noAuth/searchByCategory` 实测 **404**（端点已变），需按真实浏览器抓 XHR。
- 湖北另有 `http://jczy.ccgp.gov.cn/gs1/gs1agentreg/pubListIndex.regx?provinceCode=<区划码>` 代理机构名录。

### 中国招标投标公共服务平台：检索只在 ctbpsp，且是纯浏览器

- 门户 `www.cebpubservice.com` 只是 CMS；真正的信息公开检索是 **`ctbpsp.com`**（旧入口 `http://www.cebpubservice.com/ctpsp_iiss/searchbusinesstypebeforedooraction/getSearch.do` 会跳过来）。
- 从 `https://ctbpsp.com/assets/js/app.2457519d.js` + `common.js` 提取（`common.httpUrl = https://ctbpsp.com`）：
  - 列表：`POST /cutominfoapi/searchkeyword?keyword=<kw>&uid=<uid|0>&PageSize=10&CurrentPage=<n>&searchType=<0|1>&bulletinType=<类型>`（第 1 页 Header 需 `Necaptcha-Validate: <id>`，翻页用 `V-Token/V-Knock/V-Dfu`，来自 `verifyvaptcha`）。
  - 详情：`GET /cutominfoapi/bulletin/<uuid>/uid/<uid>/token/<vToken>`（Header 同 vaptcha；PDF 走 `/cutominfoapi/BulletinPDF/…`）。
  - 推荐流：`GET /cutominfoapi/recommand/type/5/pagesize/<n>/currentpage/<n>?province=&industry=`。
  - 反爬：页面内联 **阿里云 `antidom.js` / `interfaceacting.js`**；本机 curl 命中 JS 挑战 → **必须真浏览器 + 过 vaptcha 人机验证**。
- **付费 API（信息API服务）**：`/webapi/index.html`，宣称汇聚 300 万+ 市场主体、1000 万+ 招标项目、3000 万+ 公告公示、700 万+ 中标业绩；提供交易拓展 / 供求资源 / 企业业绩 / 行业分析等 API，另有邮件方式；**需商务开通**，电话 010-88484118-860/853。

### 商业招标网：门槛与历史回溯年限

| 站 | 域名 | 免费额度 | 付费 | 历史回溯 |
|---|---|---|---|---|
| 千里马 | `qianlima.com` / `search.qianlima.com` | 注册后每天 5 条，且限 **7–30 天前** 信息 | 普通 7999 / 高级 12999 / VIP 21999 元/年 | **招标类历史库 2012 年起**、**项目类 2014 年起**；数据超市「近 10 年招中标 Excel 打包」（议价）；标准 API 近十年（议价） |
| 中国采招网 | `bidcenter.com.cn` | 首页可读 | 会员（费率见站点公示页） | 未取到（站点对非浏览器一律人机验证） |
| 比地招标 | `bidizhaobiao.com` / `mvip.` | 会员制 | 会员 | 站点自称「每日更新 30 万条」（上游声明，未本机实测） |

> 千里马免费额度与历史库年限出自其会员服务页文案（**上游声明，本机仅验证该页 200 与 API 可达**）。匿名 JSON 检索端 `search.qianlima.com/api/v1/website/search` 未登录即返回全量计数（`rowCount`），**是否等同于会员可见范围未验证**——引用深页前先自测条数上限。

### 历史公告的批量获取/语料化做法（实测能到哪一步）

1. **首选有 JSON 的入口**：北京 `POST /elasticsearch/search`（`page`/`size`）与千里马 `search.qianlima.com/api/v1/website/search`（`currentPage`）——两者都支持深翻页、返回结构化条目（标题/日期/链接/地区），可循环分页落库。千里马每页 20 条、北京每页 `size` 可调；**注意 20 s 超时 + ≥1.5 s 间隔 + 桌面 UA**。
2. **按时间窗细分**：对无深翻页上限的站点（如 ccgp，见 `../gov/ccgp-ggzy.md` 的 `start_time/end_time` 冒号分隔写法；ggzy `DEAL_TIME=06` + `TIMEBEGIN/TIMEEND`），改「关键词 × 年（甚至月）」多轮查询，绕 `total` 1000 条上限。
3. **详情页/附件**：公告正文多为静态 HTML，附件（招标文件 PDF/Excel）在详情页链接；批量落库时只存字段 + 正文，附件按需下。
4. **商业历史库/API 兜底**：中国招标投标公共服务平台付费 API、千里马「标准 API/数据超市」、比地 `api.bidizhaobiao.com/*.do`（含 `searchDataExport.do` 导出，疑会员态）——适合要**跨年全量 + 结构化**时直接买。
5. **现成语料**：不想自己爬，见 `tender-corpus.md`（CnOpenData 2013 起 1700 万条、Hugging Face 微调集等）。

## 坑

1. **反爬分三档**：ctbpsp 是**阿里云 WAF JS 挑战**（curl 必挂，换 UA 无用，必须真浏览器 + vaptcha）；采招网是**人机验证跳转**（`shuju.bidcenter.com.cn/HumanMachineVerification*.shtml`）；比地是 **NGINX 校验页**（`.bidizhaobiao.com` 首页 870 B 空壳，真站在 `mvip.` 与 `api.` 子域）。别用 curl 硬刷，会封 IP。
2. **http/https 与端口是硬约束**：江苏必须 **http**（https 不通）；湖北检索在 **`:9040`**、列表库在 **`:8090`**（非 443），本机 POST 返 500 不一定是站挂了，多半是表单字段没给全。
3. **参数名按站而异**：千里马分页是 `currentPage`（`page` 会被静默忽略，容易误判"翻页无效"）；北京请求字段是 `searchword`/`page`/`size`；gpcms 是 `selectInfoMoreChannel` 一类的具名接口。**别跨站套用参数名**。
4. **响应体可能二次编码**：北京 `result` 是 JSON **字符串**（要 `json.loads` 两次）；千里马 `popTitle` 里含 `<font color='red'>` 高亮标签与转义，入库前要清洗。
5. **免费额度≠匿名额度**：千里马明写"免费 5 条/天（7–30 天前）"，但匿名 API 返回全量计数——**以接口实际返回为准，引用前自测**；商业网条款禁止二次分发，落库/发布前查 license 与 robots。
6. **同名不同源**：`中国政府采购网`(ccgp) / `中国采购与招标网`(chinabidding) / `中国招标投标公共服务平台`(cebpubservice) 是三套东西，商业测评常混用；引用口径要写清平台名。
7. 个别省级站会**临时不可用**（本次山东 `ggzyjy.shandong.gov.cn` 502），按 ggzy/ccgp 国家级源兜底，勿据一次失败判定站点下线。
