# preprints-cn —— 中文预印本与国家科技报告

- 去哪找：ChinaXiv `https://chinaxiv.org/`（中文预印本主站）；国家科技报告服务系统 `https://www.nstrs.cn/`；中国科技论文在线 `https://www.paper.edu.cn/`（**2026-10-03 全站维护中**）
- 什么时候用：找**未正式发表的中文预印本**（ChinaXiv：中科院系统及合作高校投稿）；找**国家财政资助项目的科技报告**（NSTRS：进展/最终报告，按部门·地方·学科·地域导航）；核验某篇论文有无预印本版本；要"项目名/承担单位/负责人/经费"这类**立项侧字段**
- 怎么搜：
  - **ChinaXiv**：检索 `/user/search.htm?field=title&value=<词>`（`field` 取 `title`/`author`/`domain`…），高级检索表单 `/user/advancesearch.htm`，浏览 `/user/preprintlist.htm`，论文详情 `/abs/<ID>`（ID 形如 `202605.00198`）。结果全是 HTML，**无公开 JSON API 实据**
  - **NSTRS 浏览 API（匿名 JSON，实测可用）**：`POST https://www.nstrs.cn/rest/kjbg/wfKjbg/listFilde`，表单 `pageNo=1&pageSize=10&competentOrg=&jihuaId=&fieldCode=&classification=&kjbgRegion=&kjbgType=&grade=`（留空=全部）；同形另有 `POST /rest/kjbg/wfKjbg/list`。返回 `{"CODE":"0","RESULT":{"count":N,"list":[…]}}`
  - **NSTRS 关键词检索**：`POST /rest/kjbg/wfKjbg/searches` / `searchtotal`（表单含 `q='"TM":"词"'`）——本机 **302**（需会话/登录），网页端检索页 `/kjbg/SearchResult?wd=<词>&q=<双重编码检索式>` 可匿名打开但结果由上述 REST 拉取
  - 中国科技论文在线：无可用接口（见「坑」）
- 覆盖：ChinaXiv = 中科院系统+合作高校预印本，ID 按月分段（`YYMM.NNNNN`），生命/医学/心理/物理等；NSTRS = 公开科技报告 **68 万+** 条（浏览口径 `count=680330`，另一口径 `551644`），含国家部门与地方项目，字段有题名、作者、单位、摘要中英、关键词、项目名、计划、地区、类型、公开范围等；中国科技论文在线 = 历史存量暂不可访问
- 门槛：ChinaXiv **浏览页与详情页免登录**（检索页本机 403）；NSTRS **浏览 API 免 key 免登录**，关键词检索与详情下载需登录/机构；中国科技论文在线 全站暂停
- 实测：2026-10-03，macOS + curl（桌面 UA）——ChinaXiv：`/home.htm` 200、`/abs/202605.00198` 200、`/user/preprintlist.htm` 200、`/user/advancesearch.htm` 200；`/user/search.htm?field=author&value=伍珍` GET **403** 且 POST 同路径 **403**（正文标题「系统正在维护中」，带 Referer 亦然）。NSTRS：首页 200；`POST /rest/kjbg/wfKjbg/listFilde` 200 JSON `count=680330`；`POST /rest/kjbg/wfKjbg/list` 200 `count=551644`，且 `searchWord=量子` **不改变 count**（该参数被忽略）；`POST /rest/kjbg/wfKjbg/searches`、`searchtotal` 均 **302**。`https://www.paper.edu.cn/` 200 但正文为「网站维护升级提示…暂停所有线上服务」
- 上游：ChinaXiv（中国科学院文献情报中心，`eprint@mail.las.ac.cn`）；国家科技报告服务系统（中国科学技术信息研究所）；中国科技论文在线（教育部科技发展中心）

## 细节

### NSTRS 检索式字段码（取自 `searchChange.js`，用于 `searches`/`SearchResult` 的 `q`）

| 码 | 含义 | 码 | 含义 |
|---|---|---|---|
| `TM` | 题名 | `ZY` | 摘要 |
| `ZZ` | 作者 | `KTXM` | 课题名称 |
| `ZZDW` | 作者单位 | `KTXMBH` | 课题编号 |
| `BGID` | 报告编号 | `JH` | 计划名称 |
| `keyword` | 关键词 | `LXND` | 立项年度 |

检索式拼法：`"TM":"芯片"`，多项用 `&&`（与）/`||`（或）/`!=`（非）连接；搜索页把该串**双重 encodeURI** 后放进 `q`，明词另放 `wd`。浏览侧过滤参数（`listFilde`）：`competentOrg`（主管部门）、`jihuaId`（计划）、`fieldCode`（学科）、`classification`、`kjbgRegion`（地域）、`kjbgType`（类型）、`grade`。

### NSTRS 记录字段（`RESULT.list[]`，节选）

`id`、`title`、`alternativeTitle`、`creator`、`creatOrorganization`、`prepareOrganization`、`publicScope`、`publicDate`、`abstractCn`、`keywordsCn`、`abstractEn`、`keywordsEn`、`projectName`、`jihuaId`、`competentOrg`、`cooperationUnit`、`responsiblePerson`、`startDate`、`endDate`、`classification`、`kjbgType`、`kjbgRegion`。详情页为 `/kjbg/detail?id=<id>`。

### ChinaXiv 入口清单

`/user/search.htm`（检索）· `/user/advancesearch.htm`（高级检索）· `/user/preprintlist.htm`（浏览）· `/abs/<YYMM.NNNNN>`（详情）· `/user/authorregister.htm`（作者注册）。

## 坑

- **ChinaXiv 检索页 curl 拿不到**：`/user/search.htm` GET/POST 均 403「系统正在维护中」，而浏览/详情/高级检索表单页 200——即"首页能开"≠"检索能用"，看检索结果要用浏览器。
- **NSTRS 关键词检索要登录**：匿名仅浏览/分面可用；`searches`、`searchtotal` 直接 302 跳首页。别拿 `searchWord` 当关键词参数——`/rest/.../list` 对该参数**静默忽略**（count 不变、返回不相关记录），易造成"搜了但有结果全是错的"。
- NSTRS 公开范围 `publicScope` 决定可下载性；`delaypubliclyYears` 表示延期公开，未到期只有元数据。
- **中国科技论文在线 2026-10-03 处于全站维护**，暂停所有线上服务；历史论文不可访问，需另找镜像或等恢复。
- ChinaXiv 详情页 `abs` 对不存在 ID 不报错（返回 200 空壳），用页面里的题名/作者判断是否命中。

## 相关

- 中文正式期刊/学位论文：`ncpssd.org.md`、`cnki.net.md`、`wanfangdata.com.cn.md`。
- 国际预印本（arXiv/bioRxiv/medRxiv）与科技报告：`nstl.gov.cn.md`、`paper-lookup.md`。
