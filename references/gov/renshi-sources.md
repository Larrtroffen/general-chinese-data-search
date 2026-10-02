# 人事任免源清单 —— 中央与地方任免公示入口

- 去哪找：
  - 中央：人社部人事任免专栏 `https://www.mohrss.gov.cn/xxgk2020/fdzdgknr/bnrsgl/rsrm/`；中国政府网 `https://www.gov.cn/yaowen/liebiao/` + 国务院公报；中国人大网任免专栏 `http://www.npc.gov.cn/c2/c12435/c12490/`。
  - 聚合：人民网组织人事 `http://renshi.people.com.cn/`（任免 `GB/64096/`、**任前公示** `GB/139627/140763/`）。
  - 地方：各省委组织部/先锋网公示栏（江苏、安徽、山东、广东等，见 `## 细节`）。
- 什么时候用：按「单位名 + 年份」定位**领导干部任免/简历**（正职：书记 / 主任 / 镇长 / 乡长）；配合 `../methods/officials-research.md` 的检索流程。
- 怎么搜：逐源操作见 `## 细节`。**一句话结论**：中央看**人社部专栏 + 国务院公报 + 中国人大网**；地方看**省委组织部公示栏**（多为 JS，常需浏览器）+ **人民网「任前公示」聚合栏**（免登录、可翻页、覆盖各省，跨省首选）；人大任免看**中国人大网任免专栏**（2007→今，静态可爬）。
- 覆盖：中央（国务院/中办/全国人大常委会任免）、地方（省管干部任前公示与任免）；中国人大网 2007→2026，人民网索引至少到数年前；粒度=名单条目/单篇公示。
- 门槛：免费、免登录为主；**地方组织部栏目多为 JS 渲染或 WAF**（人社部瑞数、山东灯塔 SPA、广东 Cloudflare），需真实浏览器；新华网检索需浏览器。
- 实测：2026-10-03（逐源状态见 `## 细节` 末表）。`gov.cn /renshi/`→404；`/yaowen/liebiao/`→200；sousuo API `q=国务院任免` → `gongwen=1513 / zhongyangfile=237 / otherfile=1040`；人民网两栏→200（含条目）；中国人大网列表→200，`index_21.html`→200（2007-04）；安徽先锋网→200（8 页）；广东 gdzz.cn→403。
- 上游：<https://www.gov.cn/>、<http://renshi.people.com.cn/>、<http://www.npc.gov.cn/c2/c12435/c12490>、<https://www.mohrss.gov.cn/SYrlzyhshbzb/sydqjdxs/SYguowuyuanrenmian>

## 细节

> 探测纪律（本机实测）：≤3 请求/主机、间隔 ≥1.5s、20s 超时、桌面 Chrome UA。`✅` = 本机 curl 200；`⚠️` = 有但需浏览器/条件；`❌` = 不可达/被拦。**未 curl 的 URL 一律标注「搜索所得」**。

### 1. 中国政府网（www.gov.cn）—— 任免现无独立栏目，走要闻 + 国务院公报

- **去哪找**：无 `/renshi/` 栏目（实测 `https://www.gov.cn/renshi/`、`https://www.gov.cn/guoqing/renshi/` 均 **404**）。国务院任免现发在**要闻列表** `https://www.gov.cn/yaowen/liebiao/`（✅ 200，21 KB）与**国务院公报**「中华人民共和国国务院任免人员」（如 `https://www.gov.cn/gongbao/2026/issue_12746/202605/content_7069425.html`，搜索所得）。
- **什么时候用**：要**副部级以上、国务院任免**的官方原文；或要公报里的「任免人员」汇总条目。
- **怎么搜**：站内检索 API（同 `gov.cn.md`）`GET https://sousuo.www.gov.cn/search-gov/data?t=zhengce&q=%E5%9B%BD%E5%8A%A1%E9%99%A2%E4%BB%BB%E5%85%8D&timetype=timeqb&sort=score&sortType=1&searchfield=title%3Acontent&p=1&n=5`（✅ 本机实测返回 `catMap.gongwen/zhongyangfile/otherfile` 计数，含结果）。单篇任免正文 URL 形如 `https://www.gov.cn/yaowen/liebiao/YYYYMM/content_XXXXXXX.htm`。
- **覆盖**：国务院/中办任免，最新在首页；公报按期结集。粒度=部级及以上。
- **门槛**：免费、免登录。
- **实测**：2026-10-03。`/renshi/`→404；`/yaowen/liebiao/`→200；sousuo API `q=国务院任免` → `gongwen=1513 / zhongyangfile=237 / otherfile=1040`。
- **上游/出处**：https://www.gov.cn/ ；API/字段细节见 `gov.cn.md`。

### 2. 人力资源和社会保障部 · 人事任免专栏 —— 国务院任免国家工作人员的权威列表

- **去哪找**：`https://www.mohrss.gov.cn/xxgk2020/fdzdgknr/bnrsgl/rsrm/`（国务院任免国家工作人员，按日期倒序）。
- **什么时候用**：需要**每期国务院任免**的规整列表（比 gov.cn 要闻好翻）。
- **怎么搜**：直接浏览栏目；**本机 curl 被瑞数（RiverSecurity）JS 挑战拦**——返回 985 B 脚本（写 `EO_Bot_Ssid` cookie 后 `location.href=…`），**需真实浏览器**（Playwright/agent-browser）访问。
- **覆盖**：国务院任免（部长/副部长/局长级），含日期标题；更新至当期。
- **门槛**：免费；本机 curl ❌，浏览器 ✅。
- **实测**：2026-10-03，`/xxgk2020/fdzdgknr/bnrsgl/rsrm/` → **200 但 985 B 瑞数 JS**（非内容页）。
- **上游/出处**：搜索所得 `https://www.mohrss.gov.cn/SYrlzyhshbzb/sydqjdxs/SYguowuyuanrenmian`（国务院任免分栏）。

### 3. 人民网 · 组织人事 —— 人事任免 + **任前公示聚合**（免登录、可翻页）★

- **去哪找**：
  - 人事任免：`http://renshi.people.com.cn/GB/64096/index.html`（✅ 200）
  - **任前公示**（聚合各省！）：`http://renshi.people.com.cn/GB/139627/140763/index.html`（✅ 200）
  - 组织人事总表：`http://renshi.people.com.cn/indexN.html`（如 `index3.html`，搜索所得）
  - 文章页：`http://renshi.people.com.cn/n1/YYYY/MMDD/c139617-XXXXXXX.html`（如 `…/2026/0708/c139617-40755715.html`，搜索所得）
- **什么时候用**：**首选**——一次拿到「**某省/某市 任前公示**」标题+日期（山东/北京/宁夏/河南/吉林/山西…），再点进原文看拟任职务；也可跨省对比。
- **怎么搜**：curl 直读列表页；翻页 = 把 `index.html` 改成 `index2.html`、`index3.html`…（实测列到 `index7.html` 且仍有「下一页」，**页数未穷尽**）。列表项文本含 `[YYYY年MM月DD日]`，可直接 grep。
- **覆盖**：人民网+中国共产党新闻网转载的**全国组织人事**（任免+任前公示）；索引深度**至少到数年前**（页面日期实测 2026-06~10），老档需交叉人大网/新华网。文章 URL 用 `/n1/` 新式编号。
- **门槛**：免费、免登录、免 JS（列表/正文均静态 HTML）。
- **实测**：2026-10-03。`GB/64096/index.html`→200/19,936 B（标题《人事任免--组织人事--人民网》，日期 2026-06-19~10-01）；`GB/139627/140763/index.html`→200/20,101 B（标题《任前公示--组织人事--人民网》，条目含「中共山东省委组织部干部任前公示公告」等）。
- **上游/出处**：`http://renshi.people.com.cn/`（200，《组织人事》）；站内检索 API 见 `../media/people.com.cn.md`。

### 4. 新华网 · 人事任免 —— 文章可直读，列表是混合专题

- **去哪找**：`http://www.news.cn/renshi/` = `http://www.xinhuanet.com/renshi/`（✅ 200，69,911 B，标题《人事任免_新华网》）。文章：`http://www.xinhuanet.com/renshi/YYYY-MM/DD/c_<id>.htm`。
- **什么时候用**：已知标题/关键词后取**新华网原文**；或补 2015 前后的老任免稿（页面里能见到 2015-01/2015-03、2020-12 的文章链接）。
- **怎么搜**：列表页**不是按时间倒序的稳定栏目**（混排 2015/2020 的专题/推荐），逐条翻页不可靠 → 改用站内检索（`so.news.cn/getNews`，**curl 405，需浏览器页面内 fetch**，见 `../media/xinhuanet.com.md`）或 `web_search site:news.cn …`。
- **覆盖**：全国人事任免（含「全国人大常委会任免名单」受权发布转载）；范围宽但列表形态差。
- **门槛**：文章页免费免登录；检索需浏览器。
- **实测**：2026-10-03。`/renshi/`→200；页面抽取到 `www.xinhuanet.com/renshi/2020-12/26/c_1126911649.htm`（受权发布·人大常委会任免名单）等。
- **上游/出处**：见 `../media/xinhuanet.com.md`。

### 5. 中国人大网 · 任免专栏 —— 全国人大常委会任免名单（静态、可爬、2007→今）★

- **去哪找**：`http://www.npc.gov.cn/c2/c12435/c12490/`（✅ 200，7,493 B，标题《任免_中国人大网》）。翻页：`index_2.html` … **`index_21.html`**（共 21 页）。文章：`http://www.npc.gov.cn/c2/c30834/YYYYMM/tYYYYMMDD_XXXXXX.html`（如 `…/202608/t20260828_457229.html`）。
- **什么时候用**：要**国家层面人大任免名单**原文（任命名单/免职名单/决定免职名单/决定任免的名单），或做「某部委主官更替」时间线。
- **怎么搜**：`curl 'http://www.npc.gov.cn/c2/c12435/c12490/'` 取当页 20 条，按 `index_N.html` 翻到 `index_21`（最旧实测 **2007-04/2007-06**）。
- **覆盖**：第十/十一…届至十四届全国人大常委会任免，**2007→2026**，粒度=名单条目（含法检、部委、驻外）。
- **门槛**：免费、免登录、静态 HTML。
- **实测**：2026-10-03。列表 200；`index_21.html`→200（日期 2007-04-27 / 2007-06-07）；文章 `c30834/202608/t20260828_457229.html`→200，标题《全国人民代表大会常务委员会决定免职的名单》。
- **坑**：URL **不要带 `/npc` 前缀**——`http://www.npc.gov.cn/npc/c2/c30834/` 会被 WAF 挡（403 / 454 B 空壳）；`/c2/c30834/…` 才通。
- **上游/出处**：搜索所得入口 `http://www.npc.gov.cn/c2/c12435/c12490`。

### 6. 北京组工网（bjdj.gov.cn）

- 已有专卡 `../party/bjdj.gov.cn.md`（北京市委组织部；无站内检索；`/article/{id}.html` 可小范围枚举）。
- **用法**：北京市管干部**任前公示**的市级权威原发；发现靠搜狗微信 / `web_search site:bjdj.gov.cn` / ID 枚举。

### 7. 江苏省委组织部 · 江苏先锋网 —— 干部任免栏（JS 列表）

- **去哪找**：`https://www.jsxf.gov.cn/gbrm/index.html`（标题《干部任免》；✅ 200 但仅 6,068 B **无静态条目 → JS 渲染**）。镜像/同源域：`https://www.jszzb.gov.cn/`（标题《江苏先锋》；文章 `https://www.jszzb.gov.cn/gbrm/art/2026/art_<hash>.html`，搜索所得）。文章：`https://www.jsxf.gov.cn/gbrm/art/YYYY/art_<hash>.html`。
- **什么时候用**：查**江苏省管干部任职前公示**原文（标题如《江苏省省管领导干部任职前公示》）。
- **怎么搜**：**列表现为 JS，curl 看不到条目**；首页静态 HTML 里有「干部任免」栏目区（`title="干部任免"` 及若干 `gbrm/art/…` 直链）→ 从首页抓最新；翻页/历史需浏览器，或改走「中共江苏省委新闻网」（见下）。
- **覆盖**：江苏省管干部任前公示 + 任免。
- **门槛**：免费；列表需浏览器。
- **实测**：2026-10-03。`/gbrm/index.html`→200/6,068 B（0 条 `art/` 直链）；`/gbrm/index_1.html`、`index_2.html`→200 但**回退成首页（121,721 B）**，即无静态翻页。
- **上游/出处**：搜索所得 `https://www.jszzb.gov.cn/index.html`。

### 8. 中共江苏省委新闻网 · 受权发布›任免发布 —— 江苏任免静态列表 ★

- **去哪找**：`https://www.zgjssw.gov.cn/fabuting/renmian/`（✅ 200，32,081 B，标题《任免发布_中共江苏省委新闻网》）。文章：`https://www.zgjssw.gov.cn/fabuting/renmian/YYYYMM/tYYYYMMDD_XXXXXXX.shtml`（如 `…/202606/t20260630_8580853.shtml`，搜索所得）。
- **什么时候用**：替代江苏先锋的 JS 列表，取江苏**省管干部任职前公示**（来源标注「中共江苏省委组织部」）与任免。
- **怎么搜**：curl 直读列表，页面含日期；`t<日期>` 文件名可直接构造/过滤。
- **覆盖**：江苏省管干部公示/任免，按发布时间倒序。
- **门槛**：免费、免登录、静态。
- **实测**：2026-10-03。列表 200（日期 2026-09-20~09-30 区段）。
- **上游/出处**：搜索所得条目页 `https://www.zgjssw.gov.cn/fabuting/renmian/202606/t20260630_8580853.shtml`。

### 9. 安徽先锋网（安徽省委组织部）· 公示公告 —— 省级公示列表（静态、8 页）★

- **去哪找**：`https://www.ahxf.gov.cn/Home/List/?Id=236`（✅ 200，27,932 B，标题《公示公告 安徽先锋网_中共安徽省委组织部》）。翻页：`…?Id=236&page=2` … **共 8 页**。文章：`https://www.ahxf.gov.cn/Home/Content/<id>?ClassId=236`（如 `1193004`）。另有栏目 `皖组动态 /Home/List/6226`、`人事考试 /Home/List/6622`。
- **什么时候用**：查**安徽省管干部任前公示公告**，或安徽省委领导任免（如「X 任安徽省委副书记」）。
- **怎么搜**：curl 直读列表（含日期标题），`page=` 递增翻页到 8。
- **覆盖**：安徽省管干部任前公示 + 省委/市委主要领导任免。
- **门槛**：免费、免登录、静态 ASP.NET（`/Home/List/`）。
- **实测**：2026-10-03。列表 200；条目含「干部任前公示公告（2026年9月18日）」「王东伟任安徽省委副书记…代理省长」；分页 `page=2..8`、共 8 页。
- **上游/出处**：`https://www.ahxf.gov.cn/`（200，标题《安徽先锋网_中共安徽省委组织部》）。

### 10. 山东「灯塔·党建在线」（省委组织部）

- **去哪找**：`https://www.dtdjzx.gov.cn/`（✅ 200，716 KB）。
- **什么时候用**：山东省管干部公示/任免。
- **怎么搜**：**首页为整站 JS SPA，静态 HTML 无栏目直链（0 条可 grep 的 `公示` 链接）→ 仅浏览器**。退路：`web_search site:dtdjzx.gov.cn 任前公示`、或人民网「任前公示」聚合栏。
- **门槛**：免费；仅浏览器。
- **实测**：2026-10-03。首页 200/716,431 B，无静态栏目链接。
- **上游/出处**：https://www.dtdjzx.gov.cn/

### 11. 广东组织工作（gdzz.cn）—— ❌ 本机受限

- **实测**：2026-10-03。`https://www.gdzz.cn/` → **403**（Cloudflare「Just a moment...」JS 挑战）；`http://` → **连接重置（000）**。换 https/Referer 各试 1 次仍失败 → **本机受限**，需浏览器过 Cloudflare 或用人民网聚合栏替代。
- **上游/出处**：https://www.gdzz.cn/

### 12. 地方组织部「任前公示」栏目 —— URL 命名规律（供猜路径后探测）

| 形态 | 例子（实测来源） |
|---|---|
| `/{gbrm\|gbgz}/index.html`（干部任免/干部工作） | 江苏先锋 `jsxf.gov.cn/gbrm/index.html`（JS） |
| `/Home/List/?Id=<栏目id>`（ASP.NET MVC） | 安徽先锋 `ahxf.gov.cn/Home/List/?Id=236`（✅ 静态） |
| `/fabuting/renmian/`、`/zwgk/rsrm/`、`/gsgg/`、`/tzgg/` | 江苏省委新闻网 `zgjssw.gov.cn/fabuting/renmian/`（✅ 静态） |
| `/col/col<id>/index.html`（浙江系 CMS） | 搜索所得形如 `zjzzgz.gov.cn/col/col1413011/art/…`（**站点身份未终核**，勿当组织部断言） |
| 北京 | 引用 `../party/bjdj.gov.cn.md` |

> 通用：省委组织部门户 = `www.<省简称>zzb.gov.cn` / `www.<省简称>xf.gov.cn`（先锋网）/ `www.<省简称>dj.gov.cn`；栏目多为 **JS 或需浏览器**，**人民网「任前公示」聚合栏（§3）是跨省最稳的免登录入口**。

### 汇总：本机实测状态（2026-10-03）

| 源 | 状态 | 形态 |
|---|---|---|
| gov.cn `/renshi/` | ❌ 404 | — |
| gov.cn `/yaowen/liebiao/` | ✅ 200 | HTML 列表 |
| sousuo.www.gov.cn `t=zhengce&q=国务院任免` | ✅ 200 | JSON |
| 人社部 rsrm 专栏 | ⚠️ 瑞数 JS | 需浏览器 |
| 人民网 人事任免 `GB/64096/` | ✅ 200 | HTML（indexN 翻页） |
| 人民网 任前公示 `GB/139627/140763/` | ✅ 200 | HTML（indexN 翻页）★ |
| 新华网 `/renshi/` | ✅ 200 | HTML（混排） |
| 中国人大网 `/c2/c12435/c12490/` | ✅ 200 | HTML（index_1..21，2007→2026）★ |
| 江苏先锋 `/gbrm/` | ⚠️ JS | 列表需浏览器 |
| 江苏省委新闻网 任免发布 | ✅ 200 | HTML 静态 |
| 安徽先锋网 `/Home/List/?Id=236` | ✅ 200 | HTML 静态（8 页） |
| 山东灯塔 | ⚠️ SPA | 需浏览器 |
| 广东 gdzz.cn | ❌ 403 | Cloudflare |

## 坑

1. 中国人大网文章 URL **不要带 `/npc` 前缀**（会被 WAF 挡 403），用 `/c2/c30834/…`。
2. gov.cn 已无独立任免栏目（404），任免内容走要闻与公报。
3. 地方组织部栏目多为 JS/SPA/Cloudflare，本机 CLI 不可用，跨省退人民网聚合栏。
4. 探测本站群建议 ≤3 请求/主机、间隔 ≥1.5s（本卡实测纪律）。
