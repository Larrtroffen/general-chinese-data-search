# court-open —— 法院公开三站

最高法系的三个**免费官方**公开平台，合为一卡（**失信·限高·被执行人·公告·破产**）。本项目用途：查"某企业/某人是否为失信被执行人 / 限高 / 破产重整"、核对涉诉与破产状态。（裁判文书全文不在此，见 `wenshu.court.gov.cn.md`。）

- 去哪找：
  - 中国执行信息公开网 `https://zxgk.court.gov.cn/`（失信被执行人、被执行人、限制消费令（限高）、终本案件、司法拍卖）
  - 人民法院公告网 `https://rmfygg.court.gov.cn/`（法院公告，开庭/送达/裁判/破产/拍卖等 20+ 类公告正文）
  - 全国企业破产重整案件信息网 `http://pccz.court.gov.cn/` → `https://pccz.court.gov.cn/pcajxxw/index/xxwsy`（破产/强制清算案件、公开案件、公告、法律文书、债务人信息）
- 什么时候用：查"某企业/某人是否为失信被执行人 / 限高 / 破产重整"、核对涉诉与破产状态；要法院公告正文；要破产重整案件/公告。
- 怎么搜：
  - **失信/限高/被执行人** → zxgk（浏览器；后端参数已反查，直连受瑞数 WAF + 验证码限制）。
  - **法院公告正文** → rmfygg 的 `initNoticeList` JSON 接口（免验证码，最易程序化；需 Liferay 会话 `JSESSIONID`+`p_auth`）。
  - **破产重整案件/公告** → pccz 的 `qzss` 表单（结果需 JS 渲染）。
  - 详细端点、参数、curl 见「细节」。
- 覆盖：全国法院；失信名单实时（新增/撤销）；法院公告 20+ 类实时更新；破产/强制清算案件。
- 门槛：**免费、免登录**；但 zxgk 有图形/行为验证码 + 全站**瑞数（RiverSecurity）动态防护**；rmfygg 资源接口需 Liferay 会话并有频控（403）；pccz 结果需浏览器渲染。
- 实测：2026-10-03（详见各节）。zxgk：首页 200 / `/shixin/` 200，`getPersonList`（带 Referer+XHR）→ **412**（瑞数 token 页）。rmfygg：首页 200 / 列表页 200（下发 `JSESSIONID`、`Liferay.authToken`），`initNoticeList` 不带会话 → **403**，带会话 → **200 但空集**（部分验证）。pccz：`http://` → **302 → https 首页 200**，`POST /pcajxxw/searchKey/qzss?ssfs=1` → **200（结果需 JS 渲染，部分验证）**。
- 上游：
  - 中国执行信息公开网 <https://zxgk.court.gov.cn/>（页面内联 JS 反查接口；`/static/javascript/data.js` 法院名录）
  - 人民法院公告网 <https://rmfygg.court.gov.cn/>（列表页 JS 反查 `initNoticeList` / `searchCourtByName`）
  - 全国企业破产重整案件信息网 <https://pccz.court.gov.cn/pcajxxw/index/xxwsy>

## 细节

### 快速选路

- 要**失信/限高/被执行人** → 中国执行信息公开网（`zxgk`，浏览器；后端参数见下）。
- 要**法院公告正文** → 人民法院公告网（`rmfygg` 的 `initNoticeList` JSON 接口，免验证码，最易程序化）。
- 要**破产重整案件/公告** → 全国企业破产重整案件信息网（`pccz` 的 `qzss` 表单）。
- 要**裁判文书全文** → 不在本卡，见 `wenshu.court.gov.cn.md`（匿名被登录墙挡）。
- 要**企业工商登记** → `../gov/gsxt.md`；要**信用红黑名单** → `../gov/credit-china.md`。

### 一、中国执行信息公开网（zxgk.court.gov.cn）

**去哪找 / 反查到的后端接口**

| 子系统 | 页面 URL | 反查到的后端接口 |
|---|---|---|
| 首页 | `https://zxgk.court.gov.cn/` | — |
| **失信被执行人** | `/gkw/html/shixin/index.html`（= `/shixin/`） | `POST /gkw/sx/searchSX`；`GET /gkw/sx/getPersonList`；`GET /gkw/sx/getUnitList`；`POST /gkw/sx/disDetailNew` |
| 被执行人 | `/gkw/html/zhixing/index.html` | 同构，命名空间据页面 JS（`searchZX` 系列，**未逐一验证**） |
| 限制消费令（限高） | `/gkw/html/xgl/index.html` | 同构（**未逐一验证**） |
| 终本案件 | `/gkw/html/zhongben/index.html` | 同构（**未逐一验证**） |
| 终本执行公开 | `/gkw/html/zhzxgk/index.html` | 同构（**未逐一验证**） |
| 司法拍卖 | `/gkw/html/sfpm/index.html` | 跳转京东司法拍卖等 |
| 登录 | `/gkw/html/login/index.html` | — |
| 法院名录 JS（44 KB，免 WAF） | `/static/javascript/data.js` | 变量 `court_0` 起：`{id,sname}`，最高法+各省高院，可按需下钻 |
| 站点配置 | `/config.js` | `window.baseUrl = window.location.origin` |

**什么时候用**

- 关键词：**企业名称 / 自然人姓名 + 身份证号（可选）** → 失信被执行人名单（有/无、案号、执行法院、履行情况）。
- 关键词：企业名 → 被执行人记录（执行标的、立案时间）。
- 关键词：企业名/法人姓名 → 限制消费令（限高）。
- 关键词：企业名 → 终本案件。
- 注意：自然人在此查询会涉及身份证号字段，**请按合规要求使用**。

**怎么搜**

① 失信名单（POST 接口，源自页面内联 JS `search()`）：

```bash
curl -sS -m 20 'https://zxgk.court.gov.cn/gkw/sx/searchSX' \
  -H 'Referer: https://zxgk.court.gov.cn/shixin/' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --data 'pName=<名称>&pCardNum=<身份证/组织机构代码，可空>&pProvince=&currentPage=1&pCode=<图形验证码>&captchaId=<验证码id>'
```
表单字段（`#myform`）：`pName`、`pCardNum`、`pProvince`、`pCode`、`captchaId`、`currentPage`。
`searchSX` **需要图形验证码**：先取 `{baseUrl}/gkw/sx/captchaNew?captchaId=<32位随机串>&random=<rnd>`，再以 `checkyzm.do?captchaId=<id>&pCode=<码>` 校验（前端用 `TianaiCaptchaRestPage`，即 tianai 行为式验证码）。

② 页面自动加载的"公示名单"（无需验证码，GET）：

```
GET https://zxgk.court.gov.cn/gkw/sx/getPersonList   # 失信被执行人（自然人）公示
GET https://zxgk.court.gov.cn/gkw/sx/getUnitList     # 失信被执行人（法人/其他组织）公示
GET https://zxgk.court.gov.cn/gkw/sx/disDetailNew?id=<id>&caseCode=<案号>&pCode=&captchaId=
```
返回 `{"data":[{iname,cardNum,caseCode,id},…]}`（对应页首滚动的公示名单）。

**结果形态**：JSON（`searchSX`）/ JSON（`get*List`）；网页端为 jQuery + 表格分页。

**覆盖 / 门槛**：覆盖全国法院；失信名单实时（新增/撤销），公示名单为滚动展示的近期数据。门槛：**免费、免登录**；但① 图形/行为验证码；② 全站 **瑞数（RiverSecurity）动态防护**。

**实测（2026-10-03）**

| 请求 | 结果 |
|---|---|
| `GET http://zxgk.court.gov.cn/` | **301 → https**（`CWAP-waf`） |
| `GET https://zxgk.court.gov.cn/` | **200**，14 284 B，`<title>中国执行信息公开网</title>` |
| `GET https://zxgk.court.gov.cn/shixin/` | **200**，24 927 B，`<title>全国法院失信被执行人名单信息公布与查询</title>`；`Set-Cookie: lqWVdQzgOVyaO=…`（瑞数动态 cookie） |
| `GET /config.js` | **200**，`window.baseUrl = window.location.origin` |
| `GET /static/javascript/data.js` | **200**，44 597 B（全国法院名录） |
| `GET /gkw/sx/getPersonList`（带 Referer + XHR 头） | **412**，2 682 B（瑞数 token 页，meta `content="27PWFMb6TvjaN95lkC.pjgDB0tRNWRw…"`） |
| 再取 `/gkw/html/zhixing/index.html`、`/gkw/html/xgl/index.html` | **412**（同一会话内多次请求后，连 HTML 页也被 412） |

结论：**接口路径/参数完全可由静态 JS 反查（见上），但直连需瑞数动态 cookie + 验证码 → 实务上只能浏览器。**

### 二、人民法院公告网（rmfygg.court.gov.cn）

Liferay 门户。**公告正文与检索接口免登录**，是本组里最适合程序化取数的一个。

**去哪找**

| 用途 | URL |
|---|---|
| 首页 | `https://rmfygg.court.gov.cn/` |
| **最新公告列表** | `https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?noticeTypeCode=62` |
| 分类公告 | 同 URL 换 `noticeTypeCode`：`62`=裁判文书、`66`=执行文书·拍卖、`998`=海洋环境公益诉讼公告、`999`=公益诉讼案件公告（其余分类用页内"公告内容"筛选） |
| 公告详情 | `/web/rmfyportal/noticedetail`（列表项链接） |
| 公告办理 / 刊登 | `/web/rmfyportal/noticehandle`、`/noticeinfo?isWebCountNotice=1` |
| 客户端（媒体） | `https://rmfygg.court.gov.cn/client/media/index.html` |

**公告内容类别清单（页内 JS 全量，可直接用作筛选值）**：全部 / 起诉状副本、上诉状副本 / 开庭传票 / 裁判文书 / 公示催告 / 破产文书 / 宣告失踪、死亡 / 执行文书、拍卖 / 无主财产认领公告 / 起诉状副本及开庭传票 / 其他 / 更正 / 遗失声明 / 司法鉴定书 / 海事文书 / 仲裁文书 / 拍卖公告 / 清算公告 / 行政处罚通知书 / 版权公告 / 公益诉讼 / 送达公告 / 公益诉讼案件公告 / 海洋环境公益诉讼公告。

**怎么搜（Liferay resource 接口，已连通到 200 但未取到数据）**

```bash
# ① 先访问列表页，拿会话 cookie 与 p_auth（Liferay 资源请求需要）
curl -sS -m 20 -c jar.txt -A "$UA" \
  'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?noticeTypeCode=62' -o page.html
TOK=$(grep -oE 'authToken="[A-Za-z0-9]+"' page.html | head -1 | sed 's/.*"\(.*\)"/\1/')
# ② 再请求列表资源（p_auth 必带，否则 403）
URL="https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?p_p_id=noticelist_WAR_rmfynoticeListportlet\
&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=initNoticeList\
&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&p_auth=$TOK"
curl -sS -m 20 -b jar.txt -A "$UA" "$URL" \
  -H 'X-Requested-With: XMLHttpRequest' -H 'Referer: https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?noticeTypeCode=62' \
  --data '_noticelist_WAR_rmfynoticeListportlet_content=<公告内容关键词>' \
  --data '_noticelist_WAR_rmfynoticeListportlet_searchContent=' \
  --data '_noticelist_WAR_rmfynoticeListportlet_courtParam=' \
  --data '_noticelist_WAR_rmfynoticeListportlet_IEVersion=unIe' \
  --data '_noticelist_WAR_rmfynoticeListportlet_flag=init' \
  --data '_noticelist_WAR_rmfynoticeListportlet_noticeType=' \
  --data '_noticelist_WAR_rmfynoticeListportlet_noticeTypeVal=<分类名，如 裁判文书>' \
  --data '_noticelist_WAR_rmfynoticeListportlet_noticeSource=' \
  --data '_noticelist_WAR_rmfynoticeListportlet_sourceTypeVal=全部' \
  --data '_noticelist_WAR_rmfynoticeListportlet_isWebCountNotice=1' \
  --data 'sEcho=1&iColumns=1&iDisplayStart=0&iDisplayLength=15&iSortingCols=0'
```

- 参数（由页面 JS `fnServerData` / `searchNoticeList()` 反查）：`content`=公告内容关键词、`searchContent`=检索词、`courtParam`=法院、`noticeType`/`noticeTypeVal`=公告类型（值用上表中文名）、`noticeSource`/`sourceTypeVal`=来源（全部/法院报/非法院报），外加 DataTables 的 `sEcho/iDisplayStart/iDisplayLength`（服务端分页）。
- 法院名联想：同 URL 换 `p_p_resource_id=searchCourtByName`，字段 `_noticelist_WAR_rmfynoticeListportlet_courtName`。
- **结果形态**：JSON `{"iTotalRecords":n,"iTotalDisplayRecords":n,"data":[…]}`（DataTables 协议）。

**实测（2026-10-03）**

- `GET https://rmfygg.court.gov.cn/` → **200**，40 028 B，`<title>首页 - 人民法院公告网</title>`（HTTP/2）。
- `GET …/noticeinfo?noticeTypeCode=62` → **200**，`<title>最新公告 - 人民法院公告网</title>`；页面下发 `JSESSIONID`，页内 `Liferay.authToken="<8位>"`。
- `POST …initNoticeList`（**不带**会话/`p_auth`）→ **403 Forbidden**（nginx）。
- 带列表页 `JSESSIONID`（+ `p_auth=<authToken>`）后 → **200**，但 body 恒为 `{"iTotalRecords":0,"iTotalDisplayRecords":0,"data":[]}`：试过 `content=破产/法院/`、`searchContent=破产/法院/拍卖`、`noticeTypeVal=全部/裁判文书/执行文书、拍卖`、完整 DataTables 参数集，**均 0 条**；后续连发请求又转 403（会话/频控）。→ **接口路径与参数已确定、可返回 200 合法 JSON，但本机未取到记录，标注"部分验证"；实际取数建议用浏览器观察一次真实请求的参数，或改走网页浏览。**

**覆盖 / 门槛**：覆盖全国法院公告，20+ 类（开庭/送达/裁判/破产/拍卖/清算/公益诉讼…）；列表实时更新。门槛：免费、**免登录**；但资源接口需 Liferay 会话（`JSESSIONID` + `p_auth`），并有频控（403）。

### 三、全国企业破产重整案件信息网（pccz.court.gov.cn）

**去哪找**

| 用途 | URL |
|---|---|
| 首页 | `http://pccz.court.gov.cn/` → **302** → `https://pccz.court.gov.cn/pcajxxw/index/xxwsy` |
| 全文检索（表单） | `POST https://pccz.court.gov.cn/pcajxxw/searchKey/qzss?ssfs=1` |
| 高级检索（表单） | `POST https://pccz.court.gov.cn/pcajxxw/searchKey/qzss?ssfs=2` |
| 债权人/管理人办事 | `https://zxfw.court.gov.cn/zxfw/index.html#/pagesGrxx/pc/login/index` |

**怎么搜**

```bash
# 全文检索（表单 action，target=_blank）
curl -sS -m 20 'https://pccz.court.gov.cn/pcajxxw/searchKey/qzss?ssfs=1' \
  -H 'Referer: https://pccz.court.gov.cn/pcajxxw/index/xxwsy' \
  --data-urlencode 'search=破产'
```

- **全文检索**字段：`search`（关键词，页内回显为 `gjz`）。
- **高级检索**字段（`?ssfs=2`）：`search`（关键字）、`fbrlx`（发布人身份）、`fbr`（发布人）、`ajlx`（案件类型：破产审查/破产/强制清算申请审查/强制清算/强制清算上诉/破产上诉/破产监督/强制清算监督）、`nrlb`（内容类别）、`fbkssj` / `fbjssj`（发布起止日期）。
- 结果形态：服务端页面（HTML）+ 页内 JS；实测结果区为空/加载中，**需浏览器确认渲染**。

**实测（2026-10-03）**

- `GET http://pccz.court.gov.cn/` → **302 → `https://pccz.court.gov.cn/pcajxxw/index/xxwsy`** → **200**，30 445 B，`<title>全国企业破产重整案件信息网</title>`。
- 该页含两个表单：`<form action="searchKey/qzss?ssfs=1" method="post">`（字段 `search`）、`<form action="searchKey/qzss?ssfs=2" method="post">`（字段 `search,fbrlx,fbr,ajlx,nrlb,fbkssj,fbjssj`）。
- `POST …/searchKey/qzss?ssfs=1`（`search=破产`）→ **200**，6 180 B，页面**回显了关键词**（`value="破产"`），但结果列表为空 → 接口可用、**结果渲染需 JS/浏览器（部分验证）**。
