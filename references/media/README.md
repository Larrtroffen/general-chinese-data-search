# media/ —— 央媒·市媒·地方媒体检索与转载通道（索引）

用于「某稿的原发/转载页在哪」「按关键词放量找央媒、市媒、地方媒体、区县融媒报道」这类任务。央媒（人民网、新华网）有站内检索接口；市媒（新京报）有可直读的搜索 API；地方与区县稿走 `local-media.md`（党媒平台/澎湃/闪电等）；数字报/电子报见子目录 `epaper/`。每个 host 一个文件；`✅/⚠️/❌` 均为本机 curl 实测（各卡「实测」行标注日期，macOS + curl）。

## 文件一览

| 文件 | 来源 | 用途/何时用 | 状态 |
|---|---|---|---|
| `people.com.cn.md` | 人民网 | **站内检索 API（JSON）** + 北京频道文章/栏目 | ✅ 检索 API 直读（走 http，非 https）；索引约 2021 年至今 |
| `xinhuanet.com.md` | 新华网 | 总网/北京频道文章；站内检索 `so.news.cn` | ✅ 文章页直读；⚠️ 检索**仅在真实浏览器会话**内可用 |
| `bjnews.com.cn.md` | 新京报 | **搜索 API（标题/全文）** + 文章页 + 电子报 | ✅ 搜索 API 直读；电子报为图片版 |
| `sohu.com.md` | 搜狐转载 | 原文不可达时的替代引文源 | ✅（m.sohu 更稳） |
| `beijing.qianlong.com.md` | 千龙网（北京市属） | 市级/区级稿件 | ✅ |
| `news.china.com.md` | 中华网转载 | 替代引文源 | ✅ |
| `bj.wenming.cn.md` | 中国文明网·北京站 | 北京日报稿转载 | ✅ |
| `rmzxw.com.cn.md` | 人民政协网 | 新华社/政协报稿转载 | ✅ |
| `wenku-mirrors.md` | 文库类转载站（无忧文档/人人文库/豆丁/道客巴巴） | **方案/报告全文的"影子通道"**：官方未公开文本的转载 | ✅ 51jzrc.cn 可 curl 直取全文；人人文库脱敏；豆丁/道客受限 |
| `doc-sharing-sites.md` | 文库分享站矩阵（原创力/人人/金锄头/360文库/淘豆/豆丁建筑/蚂蚁/道客巴巴/夸克 + 已停运站） | **文库类"影子通道"扩展**：站内搜索模板 + 360搜索 `site:` 定位文档页；原创力/人人/金锄头 文档页可直读公开预览正文 | ⚠️ 多站已停运 |
| `rsshub.md` | RSSHub（自建/公共实例） | **统一 RSS 通道**：人民日报/澎湃/头条/新京报/财新/观察者/凤凰/北京市政府委办局 的路由表 + 参数 + 限流 | ⚠️ 公共实例限流严（实测 429）；`rsshub.ktachibana.party` ✅ |
| `news-aggregator-skill.md` | 44+ 源聚合 Skill（cclank） | 多源头条清单 + 源 URL + OPML 模板（国际/科技/财经/热榜） | ✅ 源清单可读（未跑其脚本） |
| `people-daily-crawler.md` | 人民日报电子版 + 老资料网 | 人民日报历年原文的 URL 形态（电子版近年；老资料网 1946–2003） | ✅ 电子版 200；⚠️ 老资料网本机超时 |
| `xinwenlianbo-archive.md` | 《新闻联播》文字稿归档 | 按日 raw 直取联播全文（2022-09 起，MIT） | ✅ raw 200 |
| `local-media.md` | 地方党媒·省市级客户端（党媒平台 hubpd / 澎湃 / 闪电·齐鲁 / 封面·极目·上游·红星） | **地方与区县新闻检索**：党媒平台聚合县级融媒号并给原文链接；澎湃/闪电有检索 API；封面/极目/上游匿名检索受限 | ✅ 党媒平台/澎湃/闪电 API 直读；⚠️ 封面 WAF、极目需 token、上游/红星仅浏览器 |
| `gopup.md` | gopup（Python 接口库） | 指数/宏观/热搜/新闻联播等另类数据接口清单 | ⚠️ 未本机跑；部分需 TOKEN |
| `redfox-community.md` | 红狐数据（RedFoxHub） | 公众号/微博/头条/抖音/小红书 等社媒检索 API（**付费 KEY**） | ❌ 需 key，未实测 |
| `forum-docs.md` | 12 个论坛（QZZN/环评爱好者/土木在线/小木虫/学法网…） | 公文·真题·报告·图纸附件集散地；站内搜索与 `site:` 检索法 | ⚠️ 多需注册；QZZN 本机不可达 |

## 选路

1. **要结构化、可翻页、可带日期** → 优先自建检索接口：人民网 `search-platform/front/search`、新京报 `s.bjnews.com.cn/bjnews/getlist`、澎湃 `api.thepaper.cn/search/web/news`、齐鲁网 `s.iqilu.com/api/search`（均 JSON）。
2. **要找地方/区县稿（含县级融媒）** → `local-media.md`：首选全国党媒信息公共平台 `api-m.hubpd.com/main_station/search`（聚合各级党媒与县级融媒号，结果带 `mpName` 与 `reprintedUrl` 原文链接）；省级客户端检索弱，封面/极目/上游/红星匿名受限（`site:` 点查或浏览器）。
3. **新华网站内检索**（`so.news.cn/getNews`）curl 被 WAF 拦（405/403），须在**真实浏览器**（Playwright/Chromium）里带同源 cookie 调用；否则退回 `web_search site:news.cn`。
4. **要拿正文** → 央媒/市媒文章页多为静态 HTML，`curl` 直读；搜狐/中华网等转载页作原文被删时的替代。
5. **要看报纸原版** → 见 `epaper/`（人民日报、光明日报、经济日报、北京日报、新京报、延庆报、密云报）。
6. **想"订阅式"增量拉某个源的最新稿** → 用 `rsshub.md`：把 RSSHub 路由当 feed 读（标题+链接+时间），比逐站爬稳。公共实例限流很凶（连打几次即 429，`rsshub.app` 本网络还不可达），**批量/定时优先自建**（`docker run -d -p 1200:1200 diygod/rsshub`）。
7. **要一批多源头条清单 / 某源的公开 JSON·RSS 接口 URL** → 抄 `news-aggregator-skill.md`（44+ 源含 36氪/华尔街见闻/腾讯/微博/V2EX/arXiv/BBC 等）。
8. **要人民日报历年原文** → `people-daily-crawler.md`（电子版 URL 形态）配合 `rsshub.md` 的 `/people/paper`；1946–2003 走老资料网（本机超时，需另想办法）。
9. **要《新闻联播》全文语料** → `xinwenlianbo-archive.md` 按日 raw 直取（2022-09 起）。
10. **要指数/热搜/舆情** → `gopup.md`（指数+热榜接口清单）；社媒检索（公众号/微博/头条）走 `redfox-community.md`（**需付费 KEY**）。
11. **要找文库站里被转载的方案/报告全文** → 先 `doc-sharing-sites.md` 的 **360搜索 `site:` 模板**定位文档页，再按站点挑通道：`51jzrc.cn` 可 curl 直取全文（`wenku-mirrors.md`）；原创力/金锄头/人人 文档页含公开预览正文，`read` 直读；豆丁/道客巴巴/夸克/百度 需浏览器且下载普遍要积分/VIP（半数站点已停运，见该卡矩阵）。

## 相关

- 数字报/电子报：`epaper/README.md`。
- 综合搜索引擎：`../engines/`；公众号主通道：`../wechat/weixin.sogou.com.md`。
- 地方民意/问政文本（群众诉求 + 官方回复）：`../social/voice-platforms.md`。
