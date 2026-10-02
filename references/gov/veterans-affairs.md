# veterans-affairs —— 退役军人事务与双拥

- 去哪找：
  - 退役军人事务部 `https://www.mva.gov.cn/`——**通知公告** `/sy/xx/tzgg/`、**部内信息** `/sy/xx/bnxx/`、**政府信息公开平台** `/gongkai/zfxxgkpt/`（规范性文件 `/zhengce/gfxwj/`、法律法规 `/fdzdgknr/fgzc/`、财务信息（部门决算）`/fdzdgknr/cwxx/`）、**英烈褒扬** `/fuwu/xxfw/bybz/`、**优待抚恤** `/sy/qjd/qjdfw/qjdydfx/`
  - **中国双拥网**（全国双拥办官方门户）`https://sy.mva.gov.cn/`——通知公告 `/tzgg/`、双拥头条 `/sytt/`、先进典型 `/xjdx/`、专题报道 `/zyzt/`
  - 部站内检索 `https://www.mva.gov.cn/so/s?keyword=<词>`（结果页 JS 渲染）；JSON 后端 `https://api.so-gov.cn/query/s`（POST，`siteCode=bm84000001`）
  - 名单直链：全国双拥模范城（县）名单 `https://sy.mva.gov.cn/tzgg/202504/t20250423_491118.html`；全国模范退役军人名单（401 名，PDF）`http://www.mva.gov.cn/sy/zt/qgtyjrgzhy/yw/201907/P020190726639607265552.pdf`；第七批国家级烈士纪念设施名单（正文内嵌）`https://www.mva.gov.cn/gongkai/zfxxgkpt/zhengce/gfxwj/202502/t20250226_481573.html`
- 什么时候用：要退役军人/优抚对象优待与抚恤政策文件、抚恤和生活补助标准调整通知、双拥模范城（县）与模范退役军人等**表彰名单**、国家级烈士纪念设施名录、烈士褒扬法规、部门决算时。
- 怎么搜：栏目为**静态 HTML**，文章形态 `/{栏目}/{YYYYMM}/t{YYYYMMDD}_{id}.html`，附件多为同目录 `P0{…}.pdf`；**站内检索须调 JSON API**（页面 `/so/s` 只给空壳）：
  ```bash
  # 部站检索（POST，表单编码）；返回 ok/totalHits/resultDocs
  curl -sS -X POST 'https://api.so-gov.cn/query/s' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode 'siteCode=bm84000001' --data-urlencode 'tab=' \
    --data-urlencode 'qt=双拥模范城' --data-urlencode 'page=1' --data-urlencode 'pageSize=10'
  ```
  结果条在 `resultDocs[].data`：`title`/`titleO`、`url`、`summary`、`docDate`、`siteLabel`、`dbName`；名单类文件正文多为内嵌 HTML 列表，部分为 PDF 附件。
- 覆盖：通知公告 2025–2026 滚动（抚恤补助标准调整等）；双拥模范城（县）名单（最新为 2025-04 命名）；全国模范退役军人（2019 起，401 名）；国家级烈士纪念设施（第一批至第七批，第七批 2025-02 公布）；部门决算按年公开；烈士褒扬法规（《烈士褒扬条例》2024 修订，2025-01-01 施行）。
- 门槛：**免费、无登录**；站内检索经 `api.so-gov.cn`，无需 key。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `mva.gov.cn/sy/xx/tzgg/` → 200/36 513；`mva.gov.cn/sy/xx/bnxx/…` 详情 → 200；`mva.gov.cn/so/s?keyword=双拥模范城` → 200/**47 685 但结果 JS 渲染**（正文仅页脚）⚠️
  - `POST https://api.so-gov.cn/query/s`（`siteCode=bm84000001`，`qt=双拥模范城`）→ 200 `ok:true`、`totalHits:10182`、`currentHits:15`，`resultDocs[]` 含标题/URL/摘要 ✅
  - `sy.mva.gov.cn/` → 200/47 569；`sy.mva.gov.cn/tzgg/` → 200/22 242，列表含《全国双拥模范城（县）名单》；`/tzgg/202504/t20250423_491118.html` → 200/32 878，**正文内嵌各省市名单**（北京、天津、河北…）✅
  - `mva.gov.cn/sy/zt/qgtyjrgzhy/yw/201907/P020190726639607265552.pdf` → 200 `application/pdf` 820 602 B（全国模范退役军人名单 401 名）✅
  - `mva.gov.cn/gongkai/zfxxgkpt/zhengce/gfxwj/` → 200/49 020；`/zhengce/gfxwj/202502/t20250226_481573.html`（第七批国家级烈士纪念设施）→ 200，名单内嵌 ✅；`/fuwu/xxfw/bybz/` → 200/38 314（英烈褒扬）；`/gongkai/zfxxgkpt/` → 200 但仅 **365 B 空壳**（SPA）⚠️
- 上游：退役军人事务部 `mva.gov.cn`；中国双拥网 `sy.mva.gov.cn`（全国双拥工作领导小组办公室）；站内检索 `api.so-gov.cn`（so-gov 政府搜索平台）。

## 细节

### 一、栏目入口（2026-10-03 实测）

| 栏目 | URL | 内容 |
|---|---|---|
| 通知公告 | `https://www.mva.gov.cn/sy/xx/tzgg/` | 抚恤补助标准调整等 |
| 部内信息 | `https://www.mva.gov.cn/sy/xx/bnxx/` | 部领导活动、政策发布 |
| 规范性文件 | `https://www.mva.gov.cn/gongkai/zfxxgkpt/zhengce/gfxwj/` | 部发文件、名单类通知 |
| 法律法规 | `https://www.mva.gov.cn/gongkai/zfxxgkpt/fdzdgknr/fgzc/` | 保障法、条例 |
| 财务信息 | `https://www.mva.gov.cn/gongkai/zfxxgkpt/fdzdgknr/cwxx/` | 部门预决算 PDF |
| 英烈褒扬 | `https://www.mva.gov.cn/fuwu/xxfw/bybz/` | 褒扬条例、烈士纪念设施 |
| 优待抚恤 | `https://www.mva.gov.cn/sy/qjd/qjdfw/qjdydfx/` | 优待抚恤政策 |
| 中国双拥网·通知公告 | `https://sy.mva.gov.cn/tzgg/` | 双拥模范城命名、慰问信 |
| 中国双拥网·先进典型 | `https://sy.mva.gov.cn/xjdx/` | 双拥典型 |
| 专题报道 | `https://sy.mva.gov.cn/zyzt/` | 命名大会等专题 |

### 二、表彰/名录直链

| 名单 | URL | 形态 |
|---|---|---|
| 全国双拥模范城（县）名单（2025-04） | `https://sy.mva.gov.cn/tzgg/202504/t20250423_491118.html` | 正文内嵌分省名单 |
| 全国模范退役军人名单（401 名，2019） | `http://www.mva.gov.cn/sy/zt/qgtyjrgzhy/yw/201907/P020190726639607265552.pdf` | PDF |
| 第七批国家级烈士纪念设施名单（2025-02） | `https://www.mva.gov.cn/gongkai/zfxxgkpt/zhengce/gfxwj/202502/t20250226_481573.html` | 正文内嵌名单 |
| 烈士褒扬条例（2024 修订） | `https://www.mva.gov.cn/fuwu/xxfw/bybz/202410/t20241009_446982.html` | 正文 |

### 三、站内检索 API（so-gov 平台）

`https://api.so-gov.cn/query/s`，**POST**，`Content-Type: application/x-www-form-urlencoded`：

| 参数 | 值 |
|---|---|
| `siteCode` | `bm84000001`（退役军人事务部本站；`www.mva.gov.cn` 页内 `#siteCode`） |
| `tab` / `qt` | 栏目（可空）/ 检索词（URL 编码，如 `qt=双拥模范城`） |
| `page` / `pageSize` | 分页 |
| `ie` | 可选用户标识，可省 |

返回 JSON：`ok`、`totalHits`、`currentHits`、`resultDocs[].data{title,titleO,url,summary,docDate,siteLabel,dbName}`；`dbName=gov_buwei`（该平台按部委建库）。缺 `siteCode` 会报「不存在的站点[null]」；用 GET 报「Request method 'GET' not supported」。

## 坑

1. **`/gongkai/zfxxgkpt/` 门户是 SPA**：直接 curl 只得到 365 B 空壳；其子栏目（`/zhengce/gfxwj/`、`/fdzdgknr/cwxx/` 等）却是静态 HTML，**直接拼子栏目 URL** 即可绕开门户。
2. **站内检索结果页 `/so/s?keyword=` 由 JS 渲染**，curl 拿不到结果；必须调 `api.so-gov.cn/query/s`，且**只能 POST 表单编码**（GET / JSON 均报错）。
3. **双拥名单在子域 `sy.mva.gov.cn`**（中国双拥网，全国双拥办主办），不在 `www.mva.gov.cn`；两站同属退役军人事务部体系，检索 `siteCode` 仍用 `bm84000001`。
4. **区分「全国」与省级双拥模范城**：全国双拥模范城（县）由全国双拥工作领导小组命名（约每 4 年一批），各省另有省级命名，引用务必注明届次与公布日期。
5. **名单形态不一**：有的正文内嵌（双拥名单、烈士纪念设施名单），有的是 PDF 附件（模范退役军人名单）；抓取时既要取 HTML 正文，也要扫同目录 `P0{…}.pdf`。
6. `sy.mva.gov.cn` 部分频道（如 `/gdyx/`、`/jyjl/`）为占位/跳转，主内容在 `/sytt/`、`/tzgg/`、`/xjdx/`；栏目名偶有更名，以站内导航为准。
