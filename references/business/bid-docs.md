# bid-docs —— 招标采购文档与附件源

聚焦**带附件（招标文件 / 需求书 / 资格预审文件）的公告源**：军队武器装备、铁路、代理机构平台与商业聚合站。
「历史回溯与批量取数」见 `procurement.md`；「国家级检索接口字段」见 `../gov/ccgp-ggzy.md`；「现成数据集」见 `tender-corpus.md`——本卡只讲**去哪儿翻到公告原文与附件**。

- 去哪找：
  - **全军武器装备采购信息网** `https://www.weain.mil.cn/`（军队/军工采购公告与需求，公开栏目）
  - **国铁采购平台** `https://cg.95306.cn/`（原「中国铁路采购网」，国铁集团及路局）
  - **中招联合招标采购平台** `https://www.365trade.com.cn/`（多家招标代理机构）
  - **中国采购与招标网** `https://www.chinabidding.cn/`（老牌行业网，含分省 `https://www.chinabidding.cn/sa/<省>/`）
  - **剑鱼标讯** `https://www.jianyu360.cn/`；**标找找** `https://www.biaozhaozhao.com/`（已并入企查查）；**招标雷达** `zhaobiaoleida.com`（本机不可达）
  - 已覆盖、不重复：中国政府采购网 / 北京公共资源交易 → `../gov/ccgp-ggzy.md`、`procurement.md`；千里马/采招/比地 → `procurement.md`。
- 什么时候用：
  - 要**军队/军工装备采购的公开公告标题、类型、截止日**（"无人机""车辆维修""信标光源"）→ weain 列表 API。
  - 要**铁路系统物资/工程采购公告与中标结果**（机车、路料、供电）→ 95306 检索 API。
  - 要**招标文件/需求书附件原文**（PDF/zip/Office）→ 进详情页，按本卡 `## 细节` 的附件规律取。
  - 只做**关键词巡检**、不要求附件 → 商业聚合站（剑鱼标讯等）更快，但多需浏览器/付费。
- 怎么搜：
  - **weain 列表 JSON（匿名可 curl）**：
    ```bash
    curl -sSk -m 20 -A "$UA" -H 'Referer: https://www.weain.mil.cn/cggg/jdgg/list.shtml' \
      'https://www.weain.mil.cn/api/front/list/cggg/list?LMID=1149231276155707394&pageNo=1&keyword=无人机'
    # → {"list":{"totalNum":18,"contentList":[{publishTime,pcUrl,ID,deadline,purchaseType,nonSecretTitle,secretGrade,LMID}]}}
    ```
    改 `LMID` 切栏目、`pageNo` 翻页；需求栏目把路径换成 `/api/front/list/cgxq/list`（见 `## 细节`）。
  - **国铁采购检索 API（匿名，自带 mhId）**：
    ```bash
    curl -sSk -m 25 -A "$UA" -X POST -H 'Referer: https://cg.95306.cn/baseinfor/notice/toBuyNoticeMore' \
      --data 'mhId=abcdef1234567890&projBidType=01&pageNum=1&sortCondition=0' \
      'https://cg.95306.cn/proxy/portal/elasticSearch/queryDataToEs'
    # → {"success":true,"data":{"resultData":{"totalCount":2049631,"pageSize":10,"result":[{id,notTitle,checkTime,bidTypeName,noticeTypeName,digest,…}]}}}
    ```
    `mhId` 前端用 FingerprintJS 生成，实测**任意字符串即放行**；`title=` 过滤实测未生效，改用结果内自筛或页面表单（见 `## 坑`）。
  - **其余站**：列表页直接 curl（365trade `/zbgg/index.jhtml`、chinabidding `/zbxx/`）取 HTML 再解析链接；详情页取正文 `<a href>` 找 `.pdf/.doc/.zip`。
  - 结果形态：weain、95306 为 **JSON**；365trade、chinabidding 为**服务端渲染 HTML**；剑鱼标讯为**混淆 JS 壳**（需真浏览器）。
- 覆盖：军队/军工装备公开采购（weain）；国铁集团及 18 路局采购（95306，`totalCount` 实测 200 万+）；代理机构货物/服务/工程招标（365trade）；全行业招标信息 + 各省分站（chinabidding）。粒度=单条公告，正文/附件多在详情页。更新按日。
- 门槛：**列表/检索免费**——weain 与 95306 可匿名 curl；365trade、chinabidding 详情页可读；**weain 详情正文与附件需注册登录（装备采购资质）**；剑鱼标讯强反爬 + 订阅；商业聚合站历史库/导出另付费（见 `procurement.md`）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA。weain `GET /api/front/list/cggg/list?LMID=1149231276155707394&pageNo=1` → **200 JSON** `totalNum=1326`；加 `keyword=无人机` → **200** `totalNum=18`；`/api/front/list/cgxq/list?LMID=HZ287281676ce46401676cf0975c000e` → **200** `totalNum=97`；详情 `/cggg/jdgg/<id>.shtml` → **302 → `/nologin.html`**。95306 `POST /proxy/portal/elasticSearch/queryDataToEs`（`mhId=abcdef1234567890`）→ **200** `totalCount=2049631`、`pageSize=10`；`GET /proxy/portal/baseinfor/public/indexBaseInforMationById?id=<es-id>` → **200 但 `success:false`「查询通用信息详情失败」**（id 空间不一致）。365trade `GET /zbgg/index.jhtml` → **200/77 620 B**，11 条；`GET /zhwzb/878895.jhtml` → **200/112 008 B**。chinabidding `GET /zbxx/` → **200/205 282 B**；`GET /zbgg/U-vzB7YjP.html` → **200/209 755 B**，标题「吐鲁番市高昌区主城区供水管网…资格预审公告」。剑鱼标讯 `GET /` → 200/353 576 B，`GET /list/` 与详情 `/nologin/content/<token>.html` → **200 但仅 3 663 B 混淆 JS 壳**。`GET https://www.biaozhaozhao.com/` → **302 → `qcc.com/web/syncSid?domain=TENDERDOMAIN…`**。`zhaobiaoleida.com`（含 www/`m.`）→ **000**（连接失败/超时）。
- 上游：全军武器装备采购信息网 <https://www.weain.mil.cn/>；国铁采购平台 <https://cg.95306.cn/>；中招联合 <https://www.365trade.com.cn/>；中国采购与招标网 <https://www.chinabidding.cn/>；剑鱼标讯 <https://www.jianyu360.cn/>。

## 细节

### weain.mil.cn —— 栏目、LMID 与 API

| 栏目 | 列表页 | 接口 / LMID |
|---|---|---|
| 采购公告 · 军队公告 | `/cggg/jdgg/list.shtml` | `GET /api/front/list/cggg/list`，`LMID=1149231276155707394` |
| 采购公告 · 军工公告 | `/cggg/jggg/list.shtml` | 同上，`LMID=1149231318006472705` |
| 采购需求 · 军队需求 | `/cgxq/jdxq/list.shtml` | `GET /api/front/list/cgxq/list`，`LMID=HZ287281676ce46401676cf0975c000e` |
| 采购需求 · 军工需求 | `/cgxq/jgxq/list.shtml` | 同上，`LMID=HZ287281676ce46401676cf59ca5001b` |
| 通用装备 / 试验鉴定 | `/tyzb/list.shtml`、`/zbsy/list.shtml` | 普通栏目页（非上两套 API） |
| 法规标准 | `/fgbz/bzh/gjbz/list.shtml`（国军标）、`/fgbz/fgzc/gjbbfg/list.shtml` | 栏目页 |
| 军委机关专栏 | `/api/militaryColumn/<N>?type=notice`（N=1–13） | 返回专栏 HTML 页（非 JSON） |

- 列表查询参数（来自页面内联 JS `getParams()`）：`LMID`、`pageNo`、`keyword`、`nonSecretTitle`、`purchaseType`、`publicUnit`、`startTime`、`endTime`、`serialNumber`、`isValid`、`majorField`（可重复）。
- 返回字段：`publishTime`、`pcUrl`、`ID`、`deadline`、`purchaseType`（公开招标/邀请招标/询价/竞争性谈判/单一来源/中标公告/更正公告/废标公告…）、`nonSecretTitle`、`secretGrade`（公开）、`freeTime`（剩余天数）、`LMID`。
- 详情与附件：`pcUrl` 形如 `/cggg/jdgg/<雪花ID>.shtml`，实测 **302 跳 `/nologin.html`**——公开栏目只给标题，**正文与附件须注册登录**（军队装备采购需资质）。

### cg.95306.cn —— 国铁采购平台

| 用途 | 入口 |
|---|---|
| 公告列表 | `/baseinfor/notice/toBuyNoticeMore?bidType=&noticeType=&transactionType=01&wzType=&title=&bidding=&navigation=` |
| 采购公告 / 结果 | `/baseinfor/notice/procurementNotice`、`/baseinfor/notice/procurementResults` |
| 检索 API | `POST /proxy/portal/elasticSearch/queryDataToEs`（`base_server=/proxy/portal`） |
| 详情页 | `/baseinfor/public/baseInformationDetail?id=<id>`（Vue 模板 + `{{item.filename}}` 附件区） |
| 附件下载 | `GET /proxy/portal/forwardFile/downloadFileForCommon?fileId=<id>`（来源：详情页 `onDownLoad` 函数） |

- 检索请求字段：`mhId`、`Authorization`、`projBidType`（交易方式，`01`=招标）、`disposalMethod`、`bidType`、`noticeType`、`unitType`、`wzType`、`title`、`inforCode`、`startDate`、`endDate`、`pageNum`、`projType`、`professionalCode`、`createPeopUnit`、`sortCondition`。
- 响应：`data.resultData.result` 每项含 `id/key/notTitle/checkTime/digest/bidTypeName/projTypeName/noticeTypeName/professionalName/regionOrigin`（`notCont` 列表里为空，正文在详情页）。
- 字典随响应返回：`dictBidTypeList`（招标/竞价采购/询价采购/谈判采购/单一来源/需求信息/直接采购）、`dictProjTypeList`、`dictNoticeTypeList`、`dictUnitTypeList`、`dictDomainList`、`dictBureauList`。

### 代理机构与行业平台

| 站 | 列表入口 | 详情页形态 | 附件 |
|---|---|---|---|
| 中招联合 `365trade.com.cn` | `/zbgg/index.jhtml`（招标公告）、`/jggs/index.jhtml`（结果）、`/bggg/index.jhtml`（变更）、`/ggtz/`（公告通知） | `/zhwzb/<id>.jhtml`、`/zfwzb/<id>.jhtml`、`/ggtz/<id>.jhtml`（服务端 HTML） | 无独立下载区，链接在正文 |
| 中国采购与招标网 `chinabidding.cn` | `/zbxx/`（招标信息）、`/zbxx/zbgg/`（公告）、`/zbxx/zbgs/`（中标）、`/zbxx/zbyg/`（资审）；分省 `/sa/<省>/`；搜索页 `/public/yjsc/html/zbcg_search.html` | `/zbgg/U-<token>.html`、`/zbgs/…`、`/zbyg/…` | 附件在详情正文；页内多处登录入口 |
| 剑鱼标讯 `jianyu360.cn` | `/list/`、`/jylab/entSearch|purSearch|supsearch` | `/nologin/content/<token>.html` | 详情为混淆 JS 壳，**须真浏览器** |
| 标找找 | `https://www.biaozhaozhao.com/` | 302 跳转 `qcc.com/web/syncSid?domain=TENDERDOMAIN` → 企查查招标频道 | 随企查查 |
| 招标雷达 | `zhaobiaoleida.com`（www / m. 子域） | 本机不可达（curl 000） | 未验证 |

### 附件获取规律（公告页附件 PDF/zip）

1. **先列表、后进详情**：两个 JSON 源（weain、95306）只给标题/日期/链接；**招标文件附件都在详情页**。
2. **详情页解析法**：抓详情 HTML，正则/解析 `<a href>` 与脚本里的下载函数，命中 `.pdf/.doc/.docx/.xls/.xlsx/.zip/.rar` 或含 `download/attach/file/ufile/oss` 的 URL 即附件。
3. **已知附件端点**：
   - 国铁：`GET /proxy/portal/forwardFile/downloadFileForCommon?fileId=<附件id>`（`fileId/filename` 来自详情 `ForwardFile` 列表）。
   - 公开平台（ccgp/北京 ggzy/省级）：附件多为正文内直链（静态文件服务器/CDN），同 `procurement.md` 的详情页说明。
4. **军队/军工（weain）**：详情 302 到 `/nologin.html`——**附件须登录**且涉密/敏感信息分级，公开栏目多为「XX」「某」脱敏标题。
5. **代理机构附件**：365trade / chinabidding 附件直接挂在正文 HTML，无独立 API；批量按需下，别整站镜像。

## 坑

1. **weain 详情要登录**：列表/检索 API 匿名可用，但 `pcUrl` 点开即 302 到 `/nologin.html`；不要据此判断"栏目失效"，是权限门。
2. **95306 的 mhId 与 id 空间**：检索 API 用任意 `mhId` 字符串即通过（前端是 FingerprintJS 访客指纹，未做校验）；但详情接口 `indexBaseInforMationById` 用检索返回的 `id` 会报「查询通用信息详情失败」——**检索 id ≠ 详情 id**，正文/附件要另按详情页 ID 取。
3. **`title=` 过滤未必生效**：95306 传 `title=机车` 返回空 `data`，换 `projType/professionalCode` 等字段或直接拉列表自筛更稳。
4. **参数名不可跨站套用**：weain 是 `LMID/pageNo/keyword`；95306 是 `mhId/pageNum/projBidType`；别混。
5. **剑鱼标讯强反爬**：站点用 `jsencrypt`、`fid-sdk`、`antiRes/mainHook.js`、`go-captcha` 滑块，`/list/` 与详情页对 curl 只回 ~3.6 KB 混淆壳——**必须真浏览器**，别硬刷。
6. **域名变更/合并**：`biaozhaozhao.com` 已 302 到企查查招标；`zhaobiaoleida.com` 本机 000，可能是机房封锁或域名已换，**引用前先复核官方域名**。
7. **拦截礼**：`www.95306.cn` 主站实测 **503**（不是采购平台 `cg.95306.cn`，两者不同域）；采购入口只认 `cg.95306.cn`。
8. **合规**：军队/铁路公告含脱敏与涉密分级，勿将脱敏标题当原始项目名；商业站条款多禁止二次分发，落库/发布前查 robots 与 license。
