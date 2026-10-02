# historical-web —— 历史网页与快照回捞

- 去哪找：国际网页档案 —— Wayback Machine `https://web.archive.org/`（CDX `https://web.archive.org/cdx/search/cdx?...`）、archive.today `https://archive.ph/`、Common Crawl `https://index.commoncrawl.org/`、Memento 聚合器、`https://arquivo.pt/wayback/`；搜索引擎快照（百度 / 搜狗 / 360 / 必应，**均已下线**）；目标站自己的旧 URL / 数字报（见 `../gov/`、`../media/`）。
- 什么时候用：页面被删 / 改版；要找改版前正文、已删内容；要枚举某 host 历史抓过的 URL、定「某页何时改过」（任免/机构调整时间点）。
- 怎么搜：三条回捞路 —— ① 国际网页档案（Wayback / archive.today / Common Crawl / Memento），② 搜索引擎快照（**国内三家已全下线**），③ 目标站自己的旧 URL / 数字报（往往最稳）。**本机网络对国际档案基本不通**（实测见「细节」），先读「本机可达性」再选路。
- 覆盖：Wayback Machine / CDX、archive.today、Memento 聚合器、Common Crawl、国内快照（已下线）；另含抓取前的存证做法（本地 WARC + 截图 + 抓取时间 UTC + sha256）。
- 门槛：读档案多免登录；本机对 archive.org / web.archive.org / archive.ph / archive.today **均不可达**，需换网络 / 代理；Common Crawl、`arquivo.pt` 本机可达。
- 实测：2026-10-03，macOS（arm64），curl 8.x（`-m 20`，桌面 UA，同主机间隔 ≥1.5 s）+ `host`/`dig`/`nc`。
- 上游：Wayback Machine、archive.today、Memento、Common Crawl、葡萄牙网页存档等（入口见「细节」）。

> 定位：这是「页面没了/变了之后去哪找」的方法卡，不重复各数字报/政务站的入口（那些在 `../media/`、`../gov/`）。

## 细节

### 本机可达性总表（2026-10-03 实测）

| 目标 | 实测 | 现象 |
|---|---|---|
| `www.webinfomall.org`（北大中国 Web 信息博物馆） | ❌ **NXDOMAIN** | `host` 无记录；`curl` 1 ms 即 000。`http`/`https` 都一样 |
| `www.infomall.cn`（该馆真身域名） | ❌ **域名待售** | `http://www.infomall.cn/` → **301 → `https://am.22.cn/ykj/buy/infomall.cn`**（22.cn 域名经纪页）；`https` 20 s 超时 |
| `timetravel.mementoweb.org`（Memento 聚合器） | ❌ **NXDOMAIN** | 本机 DNS 与 `dig @8.8.8.8` 均无记录；**旧入口已死** |
| `mementoweb.org`（项目主页） | ✅ 200 / 2826 B | 只剩介绍页；它指向的聚合器即上面那个已死域名 |
| `memgator.cs.odu.edu`（ODU MemGator 聚合器） | ⚠️ 首页 200 / 1960 B；API 404 | 首页给 ASCII banner + 端点文档；**按其文档调 `/timemap/link/…` 返回 `404 page not found`**（公开实例未开该路径） |
| `arquivo.pt/wayback/`（葡萄牙网页存档） | ✅ 302 → `https://arquivo.pt` | 带 `X-RateLimit: 1000/60s`；非中文站，仅零星中文页面 |
| `web.archive.org` | ❌ TCP 443 closed | DNS 可解析（108.160.166.142）但 6 s 超时；与 `../tools/web.archive.org.md` 一致 |
| `archive.org`（主站） | ❌ 000 / 6 s | 同上，不可达 |
| `archive.ph`（archive.today） | ❌ TCP 443 closed / 20 s 超时 | DNS 通（103.246.246.144），连接不通 |
| `archive.today` | ❌ 301 → `https://archive.ph/` | 即跳进上面那个不可达的域名；`archive.is` 亦 000 |
| `index.commoncrawl.org`（Common Crawl 索引） | ✅ 200 / 7391 B | 首页 title `Common Crawl Index Server`；**本机唯一通的国际 URL 索引**（具体查询未在本卡实测） |
| `swap.stanford.edu` | ❌ 403 | 拒绝访问 |

### 各源怎么用（能通的写操作，不通的写「换环境后怎么用」）

#### 1. Wayback Machine / CDX（**本机不通，但方法最值钱**）

- 入口：`https://web.archive.org/web/*/{url}`（人看）；`https://web.archive.org/cdx/search/cdx?...`（机读）。
- **CDX 才是真工具**（枚举该 host 历史上被抓过的每一个 URL）：
  ```bash
  curl -s 'http://web.archive.org/cdx/search/cdx?url=example.gov.cn/*&output=json&fl=original&collapse=urlkey'
  curl -s 'http://web.archive.org/cdx/search/cdx?url=example.gov.cn/ldjg&output=json&collapse=digest&fl=timestamp,digest,statuscode'
  ```
  四个参数够用：`matchType=domain`（含子域，能翻出 staging/旧子域）、`filter=statuscode:200`（或 `!mimetype:text/html` 挑文档）、`from=20180101`（任意精度时间前缀）、`collapse=urlkey|digest`。
- **`collapse=digest` = 只看「内容真正变过」的抓取**：400 次抓取坍缩成 6 行，这 6 个日期就是「某页何时改过」——用来定**任免/机构调整的时间点**非常好用。
- 抓「未加工」原件：时间戳后缀 `id_`（`/web/20190412093000id_/http://…`），拿原始响应再做解析/diff/引用。
- **本机不可达**：需换网络环境（或代理）后再跑；先 `nc -z -G 6 web.archive.org 443` 判活别硬等。
- 证据性：只证明「该 URL 当时向该爬虫返回了该内容」，不证明发布日；域名易主后的抓取不算原主内容。

#### 2. archive.today（`archive.ph`）—— **本机不通**

- 用法：`https://archive.ph/{完整URL}` 查已存快照；`https://archive.ph/newest/{URL}` 最新一份；提交新存档在首页输入框。
- 长处：**抓的是渲染后的 DOM**（JS 重的页、社交贴），且不受 Wayback 的 robots 排除影响 → Wayback 说「被排除」时来这。
- **本机不可达**（DNS 通、443 不通）；换网络再试。

#### 3. Memento 聚合器 —— 原入口已死

- **旧入口 `timetravel.mementoweb.org` 已 NXDOMAIN**（本机+DNS 双重确认）。
- 活着的替代：`mementoweb.org`（介绍页）、`memgator.cs.odu.edu`（MemGator 服务，**首页可读、API 本机 404**）。
- 价值在它列出的**上游存档清单**（可用作「还能去哪找」的索引）：Archive.today、葡萄牙 Web Archive、Perma.cc、BAnQ（魁北克）、日本国立国会图书馆 WARP、Archive-It、冰岛/澳洲/加拿大/苏格兰/UK Web Archive、UK Parliament Web Archive。注：**首页显示 Internet Archive 连续失败 7374 次、UK Web Archive 1015954 次**——上游本身也在掉线。

#### 4. Common Crawl（**本机 ✅，本卡未做具体查询**）

- 入口：`https://index.commoncrawl.org/`（首页 200）；索引名形如 `CC-MAIN-2024-33`。
- 用法（换环境/本机都可）：`https://index.commoncrawl.org/CC-MAIN-2024-33-index?url=example.gov.cn%2F*&output=json` → 返回 `urlkey/timestamp/status/mime`。
- 定位：Wayback 从未抓过、或被排除的 URL，来这里；不同种子 → 不同结果。中文覆盖弱于国内站，但**是国际档案里仅剩的本机可达者**。

#### 5. 国内快照：**三家全下线（实测）**

| 家 | 入口（历史） | 2026-10-03 实测 |
|---|---|---|
| 百度快照 | `cache.baiducontent.com/c?m=…` | **301 → `https://m.baidu.com/error.jsp?url=cache.baiducontent.com&from=rec&m=…`**（错误页）→ 入口已废（快照 2022 年下线） |
| 搜狗快照 | `www.sogou.com/snapshot?url=…` | **404**，title「搜狗——您的访问出现了一个错误」 |
| 360 快照 | `cache.haosou.com/query?q=…` | **000**（DNS/连接失败） |
| 必应快照 | `cc.bingj.com/cache.aspx?…` | **400**，body「Our services aren't available right now」 |

- **结论**：国内**没有**可用的公共「网页回放库」——北大 webinfomall/infomall.cn 已消亡（域名待售），引擎快照全线关停。
- **实际替代（优先于国际档案）**：目标站自己的**旧 URL 直连**（改版常留旧路径）、**数字报老 URL 规则**（见 `../media/epaper/`）、`site:` 命中后若 404 再去档案找快照。方志/年鉴类旧页在 `../archives/`。

#### 6. 抓之前先存证（本机做法）

- Wayback 的 Save Page Now 与 archive.today 本机都不可达 → 我们改用：**本地 WARC + 截图 + 记录抓取时间（UTC）+ sha256**：
  ```bash
  wget --warc-file=evidence-001 --page-requisites --no-parent https://example.gov.cn/pic >/dev/null 2>&1
  shasum -a 256 evidence-001.warc.gz
  ```
- 引用规范：档案 URL + 时间戳 + 原 URL + 抓取时间（UTC）+ 取得方式；**截图不是证据**，能被伪造。

### 实测

2026-10-03，macOS（arm64），curl 8.x（`-m 20`，桌面 UA，同主机间隔 ≥1.5s）+ `host`/`dig`/`nc`：`webinfomall.org`、`www.webinfomall.org`、`timetravel.mementoweb.org` → **NXDOMAIN**；`http://www.infomall.cn/` → 301 `Location: https://am.22.cn/ykj/buy/infomall.cn`；`https://www.infomall.cn/` → 000/20 s；`https://mementoweb.org/` → 200/2826 B；`https://memgator.cs.odu.edu/` → 200/1960 B，`https://memgator.cs.odu.edu/timemap/link/http://www.beijing.gov.cn/` → 404/19 B；`https://arquivo.pt/wayback/` → 302 → `https://arquivo.pt`（`X-RateLimit-limit: 1000`）；`web.archive.org:443`、`archive.ph:443` → `nc` closed；`https://archive.org/` → 000/6 s；`https://archive.ph/` → 000/20 s；`https://archive.today/` → 301 → `https://archive.ph/`；`https://archive.is/` → 000；`https://index.commoncrawl.org/` → 200/7391 B（title `Common Crawl Index Server`）；`https://swap.stanford.edu/` → 403；`http://cache.baiducontent.com/c?m=xxx` → 301 → `https://m.baidu.com/error.jsp?...`；`https://www.sogou.com/snapshot?url=…` → 404（title「搜狗——您的访问出现了一个错误」）；`http://cache.haosou.com/query?q=…` → 000；`https://cc.bingj.com/cache.aspx?q=…&d=1` → 400（「Our services aren't available right now」）。

## 坑

1. **本机对国际档案整体不通**（archive.org / web.archive.org / archive.ph / archive.today 全部 TCP 不通）——别在默认网络下反复重试，先 `nc -z` 判活，改用直连旧 URL 或换网络。
2. **「没有快照」≠「页面不存在」**：可能只是没被抓、被 robots 排、在登录后、或太冷门；换两个档案再下结论。
3. **`robots.txt` 追改历史**：站点上一条 `Disallow` 可能一次性抹掉历年抓取（易被用来「洗白」域名过往）→ 遇「历史太干净」换 archive.today/Common Crawl。
4. **回放页是重建的**：Wayback 会用「最近的资源抓取」拼页面，渲染出来的页未必真实存在过；要解析就抓 `id_` 原始响应。
5. **抓取时间 ≠ 发布时间**：只能给上界。
6. **合规**：读档案是被动；拿回捞到的路径去访问**活站**不是被动，会留痕——先决定你是在读档案还是探目标。
