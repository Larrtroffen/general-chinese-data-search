# land-market —— 土地出让公告与成交公示

- 去哪找：
  - **中国土地市场网（全国汇总，首选）** 前端 `https://www.landchina.com/`（Vue SPA）；**检索 API 基址** `https://api.landchina.com`
  - 省级抽查①江苏：土地市场应用 `https://zrzy.jiangsu.gov.cn/gtapp/xxgk/tdsc_getTdcrxx.action?id={记录id}&xzqhdm={区划码}`；市级通知公告（例苏州）`https://zrzy.jiangsu.gov.cn/sz/gtzx/tzgg/`；省公共资源交易网 `http://jsggzy.jszwfw.gov.cn/jyxx/003013/003013001/{YYYYMMDD}/{id}.html`
  - 省级抽查②浙江：`https://zrzyt.zj.gov.cn/col/col1229452644/index.html`（土地出让公告）、`col1229453692`（成交公示）、`col1229457154`（协议出让结果）；省官方交易平台 `https://www.zjzrzyjy.com/landView/`
  - 省级抽查③广东：`https://nr.gd.gov.cn/zwgknew/zdlyxxgk/tdsc/`（土地市场）、`…/tdsc/cjgs/`（成交公示）
  - 商业库：中指云土地榜 `https://www.cih-index.com/rank/land.html`、土地数据 `…/data/land.html`；克而瑞 `https://www.cric.com/`
- 什么时候用：要**某一期挂牌/拍卖出让公告原文**（出让方案、宗地面积、用途、容积率、保证金、起始价）、**招拍挂成交公示**（受让人、成交价）、某市某月的供地与成交清单、地王/地价排行，或做土地财政、供地节奏、房企拿地研究时。
- 怎么搜：landchina 是 SPA，**别抓页面，直接 POST JSON**（参数在 body，不是 query）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  H=(-H 'Content-Type: application/json;charset=UTF-8' -H 'Referer: https://www.landchina.com/' -H 'Origin: https://www.landchina.com')
  # ① 出让（供应）公告列表：gyggBt=标题关键词，xzqDm=行政区码，startDate/endDate=YYYY-MM-DD（三者 AND）
  curl -sS -A "$UA" "${H[@]}" --max-time 60 -X POST \
    --data-binary '{"page":1,"pageSize":50,"gyggBt":"淄博"}' \
    'https://api.landchina.com/tGygg/transfer/list'
  # ② 公告详情（宗地级指标）
  curl -sS -A "$UA" "${H[@]}" --max-time 60 -X POST \
    --data-binary '{"gyggGuid":"gygg8bdb62a3-a1e4-42ed-85d8-21b8bd6c1167"}' \
    'https://api.landchina.com/tGygg/transfer/detail'
  # ③ 成交公示列表 / 详情（慢，必要时 --max-time 90）
  curl -sS -A "$UA" "${H[@]}" --max-time 90 -X POST \
    --data-binary '{"page":1,"pageSize":50}' 'https://api.landchina.com/tCjgs/deal/list'
  curl -sS -A "$UA" "${H[@]}" --max-time 60 -X POST \
    --data-binary '{"cjgsGuid":"90ea00b1-37e1-4f67-a775-61734eea06af"}' \
    'https://api.landchina.com/tCjgs/deal/detail'
  ```
  结果形态：纯 JSON `{msg,code,data:{total,list[]}}`，免登录；详情返回 `relate[]` 宗地级数组。字段见「细节」。
- 覆盖：土地市场网 = 全国（省/市/县到 6 位区划）× 出让公告 + 成交公示，含集体土地出让（`jt-` 前缀端点）、供地计划/结果、动态监测；滚动发布（实测当日已有当天数据）。省级站只覆盖本省，且多为 JS 渲染。商业库覆盖全国但明细付费。
- 门槛：土地市场网 **免费、免登录、无验证码**（有华为云 WAF，桌面 UA 即可）；江苏 JSP action **免费无登录**；浙江交易平台需浏览器（夜间维护）；中指 CREIS / 克而瑞 CRIC 数据库 **需注册/会员**。
- 实测：2026-10-03（宿主 2026-10-02 UTC 夜），macOS arm64，curl 8.x，桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `POST api.landchina.com/tGygg/transfer/list {"page":1,"pageSize":5}` → 200 `total=4911`，首条《高青县自然资源局国有土地使用权挂牌出让公告(高自然出告字[2026]12号)》`gygg8bdb62a3-…`，`fbSj=2026-10-02T12:10:05` ✅
  - 同端点筛选：`{"gyggBt":"淄博"}` → 200 `total=17`；`{"xzqDm":"370300"}` → `total=10`；`{"startDate":"2026-10-01","endDate":"2026-10-03"}` → `total=34`；`{"startTime":"2026-10-01","endTime":"2026-10-03"}` → 仍 `4911`（**该参数名无效**）；三条件 AND 生效（`{"xzqDm":"370300","startDate":"2026-10-01","endDate":"2026-10-03"}` → `total=0`）✅
  - `POST /tGygg/transfer/detail {"gyggGuid":"gygg8bdb62a3-…"}` → 200 `relate[]` 宗地：`zdBh=370322001001GB90141W00000000[…]`、`mj=18987`、`tdYt=商业服务业用地`、`qsj=4842`、`crBzj=969`、`minRjl/maxRjl` 等 ✅
  - `POST /tCjgs/deal/list {"page":1,"pageSize":5}` → 200 `total=3278`；**首查 20 s 无字节超时，重试约 30 s 才返回** ⚠️
  - `POST /tCjgs/deal/detail {"cjgsGuid":"90ea00b1-37e1-4f67-a775-61734eea06af"}` → 200 `srDw=湛江市赤坎华达塑料复合彩印有限公司`、`cjJg=928.5`、`qsj=928.5`、`mj=12380`、`tdYt=工矿用地` ✅
  - `POST /tGygg/index/statistics {}` → 200 `mapData[]`（如 `{"xzqDm":"32","num":30,"xzqName":"江苏省"}`），**耗时 30–45 s** ⚠️
  - `GET /bptFieldEnum/xzq` → 200 `{"msg":"发生错误！请联系系统管理员！","code":301}`（方法/参数不对）⚠️
  - `www.landchina.com/` → 200 5,152 B（SPA 外壳）；`/default.aspx` → 302 `https://www.landchina.com/#/404`；手机 UA 会跳 `m.landchina.com`
  - 江苏 `GET gtapp/xxgk/tdsc_getTdcrxxnew.action?id=7216188&lx=1&xsys=1&xzqhdm=320300` → 200 9,304 B HTML《邳州市自然资源和规划局国有土地使用权挂牌出让公告 邳州市挂[2025]4号》，正文含地块指标表 ✅
  - 浙江 `GET zrzyt.zj.gov.cn/col/col1229452644/index.html`（含 `?number=` 变体）与 `col1229453692` → 200 但**返回 150,770 B 的站点首页外壳、0 条目**；`/module/search/index.jsp?…`、`/module/jpage/dataproxy.jsp` → 404 (openresty)；`www.zjzrzyjy.com/landView/` → 200 **维护页**（2026-09-30~10-06 每日 20:00–08:00）❌
  - 广东 `GET nr.gd.gov.cn/zwgknew/zdlyxxgk/tdsc/`（14,366 B）与 `…/tdsc/cjgs/`、`…/cjgs/mindex.html`（10,094 B）→ 200 但正文列表 JS 渲染，HTML 仅面包屑+页脚，0 条目 ⚠️
  - 中指云 `GET www.cih-index.com/rank/land.html` → 200 120,715 B：榜名齐全（企业排行榜、城市土地成交宗数/面积、推出宗数/面积、城市地价排名/地王排行榜）但**页面无一个成交数字**，含「登录/注册/试用」⚠️
  - 克而瑞 `GET http://www.cricchina.com/research/` → 301 → `https://www.cric.com/` 200 4,777 B（Nuxt SPA + 阿里云验证码，无内容）⚠️
- 上游：中国土地市场网 `landchina.com`（自然资源部主管）；江苏省自然资源厅 `zrzy.jiangsu.gov.cn`；浙江省自然资源厅 `zrzyt.zj.gov.cn`；广东省自然资源厅 `nr.gd.gov.cn`；中指研究院「中指云」`cih-index.com`；克而瑞 `cric.com`。

## 细节

### landchina API 端点（`https://api.landchina.com`，全部 **POST + JSON body**）

| 端点 | body | 用途 | 状态 |
|---|---|---|---|
| `/tGygg/transfer/list` | `{"page","pageSize","gyggBt","xzqDm","startDate","endDate"}` | 出让（供应）公告列表 | ✅ 实测 |
| `/tGygg/transfer/detail` | `{"gyggGuid"}` | 公告详情（宗地级 `relate[]`） | ✅ 实测 |
| `/tCjgs/deal/list` | `{"page","pageSize",…}` | 成交公示列表 | ✅ 实测（慢） |
| `/tCjgs/deal/detail` | `{"cjgsGuid"}` | 成交明细（受让人/成交价） | ✅ 实测（慢） |
| `/tGygg/index/statistics` | `{}` | 各省供应/出让计数 `mapData[]` | ✅ 实测（30–45 s） |
| `/tGygg/index/supplyCount` | 无 | 供应计数（GET） | ❓ 未实测 |
| `/tGygg/other/list` `/tGygg/other/detail` | 同上 | 其他公告 | ❓ 未实测 |
| `/tGyggZd/transfer/list` `/tGyggZd/land/detail` | 同上 | 宗地级供应明细 | ❓ 未实测 |
| `/tCjgsZd/deal/list` `/tCjgs/supplyCount` | 同上 | 宗地级成交 | ❓ 未实测 |
| `/tGdxm/result/list` `/tGdxm/result/detail` | 同上 | 供地项目结果 | ❓ 未实测 |
| `/jt-gygg/transfer/list` `/jt-cjgs/deal/list` | 同上 | **集体土地**出让/成交 | ❓ 未实测 |
| `/epstBulletin/{announcement,market,macro,report,theoretical}/list` | 同上 | 公告/市场/宏观/报告/理论 | ❓ 未实测 |
| `/landRecommend/recommend/{index,list,detail}` | 同上 | 推荐地块 | ❓ 未实测 |
| `/bptFieldEnum/{xzq,keyCity,tdytTreeList}` | — | 行政区/重点城市/土地用途树 | ⚠️ GET 报 code 301 |

- 端点名来自前端 `https://www.landchina.com/js/app.53354695.js`（31363 B）；`api.landchina.com` 在该文件里写死为 base。
- 前端路由另有 `/advancedSearch`、`/givingNotice`、`/publicDeal`、`/resultNotice`、`/supplyPlan`、`/proposedSupply`、`/renewContract`、`/collectiveGivingNotice` 等页面。

### 列表字段（数组项）

- 出让列表：`gyggGuid`（详情主键，带 `gygg` 前缀）、`gyggBt`（公告标题）、`xzqDm`（6 位区划码）、`xzqFullName`（省市区全名）、`fbSj`（发布时间 ISO）、`ggLx`（公告类型，如「挂牌」）。
- 成交列表：`cjgsGuid`、`gsbt`（公示标题）、`xzqDm`、`xzqFullName`、`fbSj`、`jzrq`（截止日期）、`gyFs`（供应方式，如「挂牌出让」）。
- 详情 `relate[]`：`zdBh`（宗地编号）、`zdZl`（坐落）、`mj`（面积）、`gyFs`、`tdYt`（用途）、`gpSjS`/`gpSjE`（挂牌起止，毫秒时间戳或 `YYYY-MM-DD`）、`qsj`（起始价）、`cjJg`（成交价，成交详情才有）、`crBzj`（保证金）、`srDw`（受让人，成交详情才有）、`minRjl`/`maxRjl`、`minLhl`/`maxLhl`、`zdZt`（宗地状态码）。

### 省级抽查路径对照（2026-10-03 实测）

| 省 | 入口 | 本机结果 |
|---|---|---|
| 江苏 | `zrzy.jiangsu.gov.cn/gtapp/xxgk/tdsc_getTdcrxx.action?id=&xzqhdm=`（及 `…new.action?…&lx=1&xsys=1`） | ✅ 200，直接是公告正文 HTML（含地块指标表） |
| 江苏（市级） | `…/sz/gtzx/tzgg/{YYYYMM}/t{YYYYMMDD}_{id}.htm` | ✅ 静态文章 |
| 浙江 | `/col/col1229452644/index.html` 等栏目 | ❌ 返回站点首页外壳，0 条目；检索/JSP 数据接口 404 |
| 浙江（交易系统） | `www.zjzrzyjy.com/landView/`（SPA） | ⚠️ 夜间维护页；数据在 SPA 的 XHR 内，仅浏览器 |
| 广东 | `/zwgknew/zdlyxxgk/tdsc/`、`…/tdsc/cjgs/` | ⚠️ 200 但列表 JS 渲染，HTML 空 |

- 浙江站点通用列表数据端点（首页引用）：`https://www.zj.gov.cn/module/freshnews/getinfo/getinfo.jsp?type=0&num=5&limit=24&column={栏目号}&webid=1`（返回 JS 片段，`column` 号需从页面解析）。

## 坑

1. **接口是 POST + JSON body，参数放 body**：对同一路径用 GET 或把参数拼成 query 会 404/301；`Content-Type: application/json;charset=UTF-8` 必带。
2. **慢接口**：`tCjgs/deal/list` 与 `tGygg/index/statistics` 实测 30–45 s，首查可能 20 s 零字节超时——`--max-time 60`~`90`，并做一次重试。
3. **华为云 WAF**（响应头 `Server: CW`、`Set-Cookie: HWWAFSESID`）：桌面 UA 可通过；手机 UA 会被 302 到 `m.landchina.com`（另一套前端，接口未验证）。
4. **日期参数名**：只用 `startDate`/`endDate`（`YYYY-MM-DD`）；`startTime`/`endTime` 会被静默忽略（total 不变）。
5. **行政区码两套**：列表用 6 位 `xzqDm`（如淄博 `370300`），`index/statistics` 用 2 位省级码（如江苏 `32`）。
6. **Guid 原样回传**：`gyggGuid` / `cjgsGuid` 带前缀（`gygg…`/`cjgs…`），截断或重拼会查不到。
7. **省级站别指望直抓**：抽查三省只有江苏能脱离浏览器拿到公告正文；浙江是「栏目→跳首页」「检索→404」「交易系统→SPA/维护」，广东列表纯 JS。拿不到就用土地市场网同一宗地的公告兜底（土地市场网是全国汇总口径，编号/内容与省级公告一致）。
8. **商业库门槛**：中指云榜单页只给榜名与登录/试用入口，数字要注册；CREIS 中指数据库、克而瑞 CRIC 数据库为付费产品。克而瑞官网 `cric.com` 是 Nuxt SPA + 阿里验证码，榜单 PDF 走 `res1.cric.com/cricbiz/…pdf`，月度 TOP100 也常由媒体转载（中房网 `fangchan.com`、东方财富研报 `pdf.dfcfw.com`）。
9. 出让公告的**价格以公告原文为准**；土地市场网列表不返回价格，必须打 `/transfer/detail`（成交价在 `/tCjgs/deal/detail` 的 `cjJg`）。
