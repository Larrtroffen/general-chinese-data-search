# archives-cn —— 国家与省级档案馆门户与查档入口

全国档案系统「门户 + 目录 + 查档」入口总表。核心事实：**绝大多数省级馆的开放档案目录只对实名/预约用户开放**，全网唯一能匿名程序化检索的中央级目录是**中国第一历史档案馆**（明清档案，含 API）；中央级民国档案在**第二历史档案馆**，只能预约到馆。

- 去哪找：
  - 国家档案局（中央档案馆）：`https://www.saac.gov.cn/`
  - 全国档案查询利用服务平台（国家档案局）：`https://cxly.saac.gov.cn/`
  - **中国第一历史档案馆**（明清档案目录检索）：`https://fhac.com.cn/search_entry.html`
  - 中国第二历史档案馆（民国档案）：`http://www.shac.net.cn/`
- 什么时候用：
  - 明清（内阁/军机处/宫中/内务府/宗人府…）档案**档号—题名—责任者**定位 → 一史馆；
  - 民国（1912–1949）中央机关档案、北洋/国民政府公报 → 二史馆（线上查目录有限，多需到馆/预约）；
  - 找**某省/市档案馆的开放档案目录**、跨馆查档、预约查档 → 全国平台或省馆门户；
  - 查档案法规、开放公告、全宗介绍、地方档案工作动态 → 国家档案局/省馆官网。
- 怎么搜：分三层，**只有第一层能匿名跑通**。
  1. **一史馆目录（匿名 JSON/HTML，宝藏）**：`GET https://fhac.com.cn/ess/catalogue.html`，参数 `tpl_file=search_catalogue&kw=<关键词>&p=<页>&pagesize=10&category_type=2&ck=1&has_image=0`，带 `X-Requested-With: XMLHttpRequest` 时返回**结果片段 HTML**（不带则返回整页外壳，含 `#datalist` 空壳）。返回 `档号`/`电子档号`/`题名`/`责任者`/`官职` 等字段（题名带 `<b style='font-weight: bold; color: #8f3d2c;'>` 高亮）；分页见片段内「共 N 页」。全文/专题走 `search_fulltext.html`、`search_subject.html` 两页（同一 `/ess/` 后端）。
  2. **全国档案查询利用服务平台**：SPA，接口 base `https://cxly.saac.gov.cn/api/pc/`；匿名可用的只有帮助/常见问题检索 `GET /api/pc/search?keyword=档案`（返回 24 条 FAQ）。**真正查档须注册登录**（网上查档/代查两种方式）。
  3. **省馆**：见下「细节」表，逐馆入口 + 门槛；能匿名查目录的极少，多数是登录/实名/预约。
- 覆盖：
  - 一史馆：馆藏明清档案 **77 个全宗、约 1000 余万件（册）**（明代 3000 余件，余为清代）；官网检索页自报「馆藏档案目录：4521813 条」（**上游声明，未本机核数**）；另上线《清实录》《清会典》全文库。
  - 二史馆：中华民国时期（1912–1949）历届中央政府及直属机构档案，约 **225 万卷 / 4500 万件**（上游声明）。
  - 全国平台：汇聚各级国家档案馆**已通过互联网开放的档案目录**，逐年扩。
  - 省级馆：各馆馆藏本地历史档案，开放目录深度差异极大（见「细节」逐馆实测）。
- 门槛：
  - **一史馆目录检索：匿名、免登录、无验证码**（本机裸 curl 通过）。
  - 国家档案局站内检索：匿名（`POST /cms-search/search.do`，`searchWord`+`siteId`）。
  - 全国平台查档：**注册/实名**；平台前置华为云 WAF（对本机 UA 返回 200 SPA 外壳，对爬虫 UA 曾返回 418）。
  - 二史馆：**预约/到馆**，线上无公众目录检索。
  - 各省：见「细节」表（登录/政务网实名/预约）。
- 实测：2026-10-03，macOS 27（arm64），curl 8.x，桌面 Chrome UA，≤3 请求/主机。
  ① `https://www.saac.gov.cn/` → 200 / 54 KB（GB 码页面）；`POST /cms-search/search.do`（`searchWord=档案&siteId=1`）→ 200 / 2.8 KB「站内搜索」。
  ② `https://fhac.com.cn/search_entry.html` → 200 / 51 KB，含「馆藏档案目录：4521813 条」；`GET /ess/catalogue.html?...kw=军机处...&X-Requested-With: XMLHttpRequest` → 200 / 32 KB，返回 `03-0199-3836-056`（档号）、`军机处办理奏折清单`（题名）、「共1804页」，题名命中被拆成单字高亮标签。
  ③ `https://cxly.saac.gov.cn/` → 200 / 620 B SPA 外壳；`GET /api/pc/search?keyword=档案` → 200 JSON `{"code":0,"total":24,...}`（FAQ）；`GET /api/pc/index` → 404。
  ④ `http://www.shac.net.cn/` → 200 / 15 KB「中国第二历史档案馆」，导航仅 查档指南/现行查档范围/预约查档，无在线目录检索。
  ⑤ 上海 `https://www.shda.gov.cn/` → 200；检索系统 `https://kfda.shda.gov.cn:8088/szdagSystem/search/index.html` → 200（「数字档案公共查阅系统/智慧检索平台」），`GET /archive/info/getFindArchive` 匿名 → 200 XML 但**内容为空**（需登录）。
  ⑥ 北京 `https://www.bjma.gov.cn/` → 200；开放档案公告页 200（2021-06-09 推出「开放档案文件级目录查询」）；`POST /eportal/ui?pageId=314798&...`（`searchWord=档案`）→ 200 / 43 KB「搜索结果页」；数字档案馆走 `seas` 登录。
  ⑦ 浙江 `https://www.zjda.gov.cn/` → 200；查档跳 `zjdafw.gov.cn` → 302 至 `mapi.zjzwfw.gov.cn` **浙江政务服务网 SSO 登录**。
  ⑧ 广东 `https://da.gd.gov.cn/` → 200（JS 跳 `/portal_home`）；`/portal_home/archives/archiveslist` → 200（档案目录，页面含 登录/注册）；`/portal_home/search?keyword=存档` → 200 / 71 KB（站内搜索匿名）。
  ⑨ 山东 `https://cdpt.dag.shandong.gov.cn/` → 200「山东省档案查询利用平台（在鲁查档）」；`GET /kgcx/lankgcx/archive!openDataPage.json` → 200 JSON，仅 2 个分类（文书档案、红色档案）。
  ⑩ 四川 `https://www.scsdag.cn/home` → 200（Nuxt SPA）；开放目录页 → 200 但正文「暂无数据 / 共 0 条」。
  ⑪ 湖北 `https://hbda.gov.cn/` → 200；跨馆查档预约 `http://wx.hbda.gov.cn:8088/hbdaly/book!book.action`；⑫ 吉林 `http://jlsda.cn/` → 200，查档页 `G_DACXJG_W.jsp?...wbtreeid=1172`；⑬ 江苏 `https://www.dajs.gov.cn/` → 200（门户，未见匿名目录入口）。
- 上游：国家档案局 https://www.saac.gov.cn/ ；全国平台 https://cxly.saac.gov.cn/ ；一史馆 https://fhac.com.cn/ ；二史馆 http://www.shac.net.cn/ ；中国档案资讯网 http://www.zgdazxw.com.cn/ ；中国档案网 http://www.chinaarchives.cn/

## 细节

### 一史馆（中国第一历史档案馆）检索端点

| 用途 | URL / 端点 | 匿名 | 备注 |
|---|---|---|---|
| 检索入口页 | `https://fhac.com.cn/search_entry.html` | ✅ | 含馆藏总量、热词 |
| 目录搜索页 | `/search_catalogue.html?kw=` | ✅ | 前端壳，结果走 `/ess/` |
| 全文搜索页 | `/search_fulltext.html?kw=` | ✅ | 《清实录》《清会典》等 |
| 专题搜索页 | `/search_subject.html?kw=` | ✅ | |
| **目录结果接口** | `GET /ess/catalogue.html?tpl_file=search_catalogue&kw=<q>&p=<n>&pagesize=10&category_type=2&ck=1&has_image=0` | ✅ | 返回结果**片段 HTML**（带 `X-Requested-With: XMLHttpRequest`） |
| 结果字段 | `identifier`(档号)、`sub_identifier`(电子档号)、`title`(题名·带高亮)、`creator_a`(责任者)、`offical_title_a`(官职)、缩微号、备注 | — | 入库须剥 `<b style='font-weight: bold; color: #8f3d2c;'>` |
| 热词/联想 | 页面内联调用（`/archive/set_usersearch.html` 等） | ✅ | 非检索主链 |

请求示例：

```bash
curl -sS -A 'Mozilla/5.0 …Chrome/126' \
  -H 'X-Requested-With: XMLHttpRequest' \
  'https://fhac.com.cn/ess/catalogue.html?tpl_file=search_catalogue&pagesize=10&p=1&category_type=2&kw=%E5%86%9B%E6%9C%BA%E5%A4%84&ck=1&has_image=0'
```

### 省级馆入口与门槛（2026-10-03 实测）

| 省/市 | 入口 | 在线查档/目录 | 门槛 |
|---|---|---|---|
| 北京 | `https://www.bjma.gov.cn/` | 数字档案馆 `/bjma/330228/index.html`；开放档案文件级目录查询 | 站内检索匿名；查档走 `seas` 登录/预约 |
| 上海 | `https://www.shda.gov.cn/` | `https://kfda.shda.gov.cn:8088/szdagSystem/search/index.html` | 页面匿名，**数据需登录** |
| 江苏 | `https://www.dajs.gov.cn/` | 门户+查档资讯 | 未见匿名目录；走全国平台/预约 |
| 浙江 | `https://www.zjda.gov.cn/` | `zjdafw.gov.cn` → 浙江政务服务网 | **政务网 SSO 实名** |
| 广东 | `https://da.gd.gov.cn/portal_home` | `/portal_home/archives/archiveslist`；站内 `search?keyword=` | 档案目录需登录；站内搜索匿名 |
| 山东 | `https://cdpt.dag.shandong.gov.cn/` | 「在鲁查档」开放档案 | 分类接口匿名；详查需登录 |
| 四川 | `https://www.scsdag.cn/` | 开放目录 `/article/nav/51a9dcd4df0449758cea38a99d1271a8` | 页面匿名，当前 0 条 |
| 湖北 | `https://hbda.gov.cn/` | 跨馆查档预约 `wx.hbda.gov.cn:8088/hbdaly/` | 预约/登录 |
| 吉林 | `http://jlsda.cn/` | `G_DACXJG_W.jsp?...wbtreeid=1172`（开放档案） | 到馆/预约 |

### 全国平台内嵌的省级档案站点清单

来源：`https://cxly.saac.gov.cn/static/js/app.*.js` 内静态列表（2026-10-03 提取），用于按省找入口：

```
安徽 http://www.ahda.gov.cn/          北京 http://www.bjma.gov.cn/
重庆 http://jda.cq.gov.cn/            福建 http://www.fj-archives.org.cn/
甘肃 http://www.cngsda.net/           广东 https://www.da.gd.gov.cn/
广西 http://www.gxdag.org.cn/         贵州 http://www.gzdaxx.gov.cn/
海南 http://www.hainan.gov.cn/szfbgt/sdaj/
河北 http://www.hebdaj.gov.cn/        河南 http://www.hada.gov.cn/
黑龙江 http://www.hljdaj.gov.cn/      湖北 http://www.hbda.gov.cn/
湖南 http://sdaj.hunan.gov.cn/        吉林 http://www.jilinda.gov.cn/
江苏 http://www.dajs.gov.cn/          江西 http://www.jxdaj.gov.cn/Index.shtml
辽宁 http://www.lndangan.gov.cn/lnsdaj/index.html
内蒙古 http://www.archives.nm.cn/     宁夏 http://www.nxda.gov.cn/
青海 http://www.qhda.gov.cn/          山东 http://www.sdab.gov.cn/daj/index.htm
山东共享 http://gxda.dag.shandong.gov.cn
山西 http://www.sxsdaj.gov.cn/        陕西 http://daj.shaanxi.gov.cn/index.aspx
上海 http://www.archives.sh.cn/（现用 https://www.shda.gov.cn/）
四川 http://www.scsdaj.gov.cn/scda/default/index.jsp
天津 http://www.tjdag.gov.cn/         西藏 http://da.xzdw.gov.cn/
云南 http://www.ynda.yn.gov.cn/       浙江 http://www.zjda.gov.cn/
```

> 注：`www.archives.sh.cn`（上海）、`www.scsdaj.gov.cn`（四川）在本机 DNS 实测已无 A 记录/不可达，实际在用的是 `shda.gov.cn`、`scsdag.cn`——清单仅供找站名，落 URL 前先解析。

### 地方档案资讯门户（非查档）

| 站 | URL | 状态 |
|---|---|---|
| 中国档案资讯网（国家档案局主管） | `http://www.zgdazxw.com.cn/` | ✅ http 可达（1.7 MB）；**https 本机不通** |
| 中国档案网（《中国档案》杂志社） | `http://www.chinaarchives.cn/` | ✅ 200 / 66 KB，期刊稿约为主体 |

## 坑

1. **省级馆「开放档案目录」≠ 匿名可查**：上海、广东、浙江、湖北等即便页面能匿名打开，数据接口一律返回空或跳登录——写卡/取数前先用一个已知档号试接口，不要看到页面就以为能抓。
2. **一史馆接口是 HTML 片段不是 JSON**：`/ess/catalogue.html` 默认（无 `X-Requested-With`）返回整页外壳（88 KB，`#datalist` 为空）；要结果必须带该头，按 `class="item"` 解析，别按 JSON 解析。
3. 一史馆题名/官职是**逐字高亮**（每个字一个 `<b>`），去标签后需拼接，直接 `strip tags` 会得到正确文字但计数/去重前务必清洗。
4. 全国平台有**华为云 WAF**：本机桌面 UA 得 200，爬虫式请求可能 418「疑似攻击行为」；且核心查档接口需登录态，匿名只有 FAQ 检索。
5. 二史馆**没有公众在线目录**，只有现行查档范围/开放专题的文字说明 + 邮件/电话预约（`esg@shac.net.cn`、025-84800747）；不要预期能在线拉民国档案目录。
6. 域名易变：`archives.sh.cn`、`scsdaj.gov.cn` 等旧域名已失效；`da.gd.gov.cn` 根路径是 116 B 的 `window.location.href="/portal_home"` 跳转壳，直接抓根路径会拿到空页。
7. `zgdazxw.com.cn` 仅 http 可达，https 握手失败；批量抓取走 http。
8. `cxly` 省级清单是**硬编码在前端 JS 里的友链**，会随版本更新；用前重新 grep `app.*.js` 的 `http(s)://…` 提取。
