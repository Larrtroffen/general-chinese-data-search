# RSSHub —— 中文媒体/政务站 RSS 通道

RSSHub 给「没有 RSS 的中文站点」生成 RSS/Atom/JSON feed，路由形如 `<实例域名>/<路由路径>`。它本身不存数据，是**实时生成器**：每条路由对应上游站点的某个列表页。对我们的价值 = 用统一 feed 接口**按源+栏目增量拉取**人民日报、澎湃、头条、新京报、财新、观察者、凤凰、北京市政府的最新条目（标题/链接/时间），省去逐个站点写爬虫。

- 去哪找：repo <https://github.com/DIYgod/RSSHub>；文档 <https://docs.rsshub.app>；路由源码 `lib/routes/<site>/...`；在线路由表 docs.rsshub.app/routes/…
- 什么时候用：要"订阅式"盯某个源的最新稿（定时/增量），而不是一次性关键词检索；或需要栏目 feed（头条/滚动/分类）。
- 怎么取：公共实例 `curl '<实例>/<route>'`；也可自建（见下）。路由参数从对应站点 URL 里抄。
- 覆盖：人民日报/澎湃/头条/新京报/财新/观察者/凤凰/北京市委办局等中文媒体/政务路由（见下源表）。
- 门槛：无（公共实例限流严；批量/定时建议自建）。
- 实测：2026-10-03，macOS + curl，桌面 UA：
  - 本机 `https://rsshub.app/people/paper` → HTTP 000（30s 超时）；`rsshub.rssforever.com`/`rsshub.liumingye.cn` → 503；`rsshub.pseudoyu.com`/`rsshub.henry.wang` → DNS 不存在。
  - `https://rsshub.ktachibana.party/people/paper` → 200/207,781B/30 items；`/thepaper/featured` → 200/75,165B/20 items；`/bjnews/cat/depth` → 200/350,669B/15 items；`/bjnews/column/204` → 200/134,641B/15 items（"新京报 - 栏目 - 政解"）；`/guancha/headline` → 200/83,026B/5 items；`/ifeng/news` → 200/92,586B；`/toutiao/channel/news_tech` → 200/286,706B。
  - `/caixin/latest`、`/gov/beijing/mhc/xwzx`、`/guancha` → **429**（同一实例连打 9 次后触发限流）。
  - 路由/参数值来自 GitHub raw 源码（`lib/routes/{people,thepaper,toutiao,bjnews,caixin,guancha,ifeng,gov/beijing}`），未运行其脚本。
- 上游：<https://github.com/DIYgod/RSSHub>（MIT）；文档 <https://docs.rsshub.app>

## 细节

### 源表（我们关心的中文媒体/政务路由，逐条）

| 路由 | 示例 URL | 上游站点 | 限制 |
|---|---|---|---|
| `/people/paper` | `/people/paper` | 人民日报电子版 `paper.people.com.cn/rmrb/pc/layout` | 当日版面全部文章（实测 30 条），非历史检索 |
| `/people/:site?/:category?` | `/people` | 人民网首页头条 | site/category 随站点栏目 |
| `/people/liuyan/:id/:state?` | `/people/liuyan/…` | 人民网领导留言板 | 需板块 id |
| `/people/xjpjh/:keyword?/:year?` | `/people/xjpjh` | 习近平系列重要讲话库 `jhsjk.people.cn` | 可选关键词/年份 |
| `/thepaper/featured` | `/thepaper/featured` | 澎湃新闻首页头条 | 实测 20 条 |
| `/thepaper/channel/:id` | `/thepaper/channel/<id>` | 澎湃频道 | id 从 thepaper.cn 频道 URL 取 |
| `/thepaper/list/:id` | `/thepaper/list/<id>` | 澎湃栏目 | 同上 |
| `/thepaper/gov/:pphId`、`/thepaper/user/:pphId` | `/thepaper/gov/<pphId>` | 澎湃政务号 / 澎湃号 | 需 pphId（从主页 URL） |
| `/thepaper/factpaper/:status?` | `/thepaper/factpaper` | 澎湃明查 `factpaper.cn` | 事实核查 |
| `/toutiao/channel/:category` | `/toutiao/channel/news_tech` | 今日头条频道 | **反爬**；category∈recommend/news_hot/news_tech/news_finance/news_world/… |
| `/toutiao/user/token/:token` | `/toutiao/user/token/<t>` | 头条号主页 | 需 token |
| `/bjnews/cat/:cat` | `/bjnews/cat/depth` | 新京报分类页 `www.bjnews.com.cn/<cat>` | cat 从站点 URL 取（depth 等） |
| `/bjnews/column/:column` | `/bjnews/column/204` | 新京报栏目 | column 为栏目 ID（204=政解），从手机版 URL 取 |
| `/caixin/latest`、`/caixin/article` | `/caixin/latest` | 财新最新/首页新闻 | 财新多为付费墙，feed 只给标题+链接 |
| `/caixin/:column/:category` | `/caixin/finance/regulation` | 财新分类 | column∈economy/finance/china/science/international/opinion/culture/weekly |
| `/caixin/weekly`、`/caixin/database`、`/caixin/k` | `/caixin/weekly` | 财新周刊/数据通/财新一线 | 需订阅才能看正文 |
| `/guancha/headline` | `/guancha/headline` | 观察者网头条 | 实测 5 条 |
| `/guancha/:category?` | `/guancha` | 观察者网首页 | category∈all/review/story/fengwen/redian/gundong |
| `/guancha/topic/:id/:order?`、`/guancha/personalpage/:uid` | `/guancha/topic/<id>` | 风闻话题/个人主页 | — |
| `/ifeng/news/:path{.+}?` | `/ifeng/news`、`/ifeng/news/shanklist/3-305565-` | 凤凰网资讯 | path = news.ifeng.com 后路径 |
| `/ifeng/feng/:id/:type` | `/ifeng/feng/<id>/<type>` | 凤凰大风号 | — |
| `/gov/beijing/mhc/:caty` | `/gov/beijing/mhc/xwzx` | 北京市卫健委新闻中心 | caty 从站点取 |
| `/gov/beijing/bjedu/gh/:urlPath?` | `/gov/beijing/bjedu/gh` | 北京市教委 | — |
| `/gov/beijing/bphc/:caty` | `/gov/beijing/bphc/announcement` | 北京保障房中心 | — |
| `/gov/beijing/jw/tzgg` | `/gov/beijing/jw/tzgg` | 北京市经信局通知公告 | — |
| `/gov/beijing/kw/:channel` | `/gov/beijing/kw/col736` | 北京市科委/中关村 | channel 从官网取 |

> 北京**市政府门户**（beijing.gov.cn）本层另有卡片 `gov/beijing.gov.cn.md`；RSSHub 的 `gov/beijing/*` 是各**委办局**子路由，二者互补。

### 两种用法

1. **公共实例**：`https://rsshub.app/<route>`（官方默认，但本网络不可达且限流严）；社区实例如 `rsshub.ktachibana.party`（实测可用）、`rsshub.rssforever.com`（实测 503）、`rsshub.liumingye.cn`（实测 503）。公共实例**限流很凶**，批量抓取易 429。
2. **自建（推荐做批量/定时）**：官方 `docker run -d -p 1200:1200 diygod/rsshub`；或仓库 `docker-compose.yml`（含 redis；需 Playwright 的路由用 `diygod/rsshub:chromium-bundled` + browserless）。自建后本地 `http://127.0.0.1:1200/<route>`，无第三方限流。

## 坑

- 公共实例：单 IP 连打几次即 **429**；`rsshub.app` 从本机 30s 超时（网络层不可达）。要稳就自建。
- `toutiao/*` 标记 **antiCrawler**（需伪造 `a_bogus` 签名），自建也可能失效。
- 财新/多数付费源 feed 只有标题+链接，正文有付费墙。
- 路由时效性跟着上游改版走；以 `lib/routes/<site>/namespace.ts` + 具体路由文件为准。
