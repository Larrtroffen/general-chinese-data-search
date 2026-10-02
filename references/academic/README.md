# references/academic —— 学术文献源（中文期刊/论文/图书检索 + 国际库/OA 全文/引文/期刊分级通道）

本层分两部分：**「源清单」= 一个站点一个文件**（中文社科文献的检索与元数据：谁可直接 curl、谁需浏览器、谁登录墙）；**「通道卡」= 跨站点的检索通道**（skills/MCP/下载链：18 个国际 API、Google Scholar、28 源 PDF 链、百度学术/知网/万方三源、GB/T 7714 引文与 Zotero 中文生态、期刊分级）。抓正文/全文时优先选能匿名 JSON/HTML 直取的源（NCPSSD、维普首页、OpenAlex/Crossref）。

## 文件一览

### 源清单（一个站点一个文件）

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `ncpssd.org.md` | 国家哲学社会科学文献中心 | 中文社科期刊全文库，**JSON API 直连** | ✅ 可匿名检索 |
| `cqvip.com.md` | 维普 | 中文期刊检索，结果页服务端渲染 | ⚠️ 仅首页 20 条 |
| `cnki.net.md` | 中国知网 | 论文/政报/年鉴主入口 | ⚠️ 需人工过码 |
| `navi.cnki.net.md` | 知网·年鉴导航 | 单卷年鉴元数据/目录 | ⚠️ 需人工过码 |
| `nstl.gov.cn.md` | NSTL 国家科技图书文献中心 | **外文**科技期刊/会议/学位/报告检索 + **全文传递（原文申请单）** | ✅ 可匿名检索 |
| `wanfangdata.com.cn.md` | 万方 | 期刊/学位/会议论文 | ❌ 滑块验证墙 |
| `duxiu.com.md` | 读秀 | 图书/章节检索 | ❌ 登录墙 |
| `chaoxing.com.md` | 超星 | 发现/超星期刊 | ❌ 登录墙 |
| `pishu.com.cn.md` | 皮书数据库 | 皮书系列（蓝/绿皮书）全文 | ⚠️ 检索需浏览器 |
| `opac.bac.gov.cn.md` | 北京市委党校 OPAC | 党内出版物书目/馆藏 | ✅ 静态可直取 |

### 海外与港台（近代中国研究的外文/境外馆藏）

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `jacar.md` | 日本亚洲历史资料中心 JACAR | 近代中日关系档案：件名目录 + 免登录 IIIF 图像 | ✅ 可匿名检索 |
| `ndl-japan.md` | 日本国立国会图书馆 | NDL Search API（书目）+ 数字馆藏检索/IIIF 图像 | ⚠️ 本机需浏览器 |
| `taiwan-libraries.md` | 台湾博硕士论文系统 / 華藝 / 臺灣記憶 | 台湾学位论文题录、期刊全文（订阅）、老照片地图 | ⚠️ 全文需登录 |
| `hk-libraries.md` | 香港公共图书馆數碼館藏 / 政府檔案處 | 香港旧报纸、政府档案、图像 | ⚠️ 需浏览器 |
| `hoover-institution.md` | 斯坦福胡佛研究所 | 民国档案、两蒋日记、20 世纪宣传品数字馆藏 | ⚠️ 本机需浏览器 |
| `harvard-yenching.md` | 哈佛燕京图书馆 + 费正清中心 | 中文善本/古籍、地方志、东亚书目；LibraryCloud/CURIOSity JSON | ⚠️ curl 429 需浏览器 |
| `european-china-collections.md` | IDP / 英国国档馆 / BnF Gallica / 柏林 SBB | 敦煌写本、吐鲁番文书、FO 系列、欧洲汉籍 | ⚠️ IDP 主站被墙 |

### 通道卡（工具/仓库，不是单一站点 —— 用来「路由到该去哪找」）

上表是"一个站点一个文件"；下表是**跨站点的检索通道**（skill / MCP / 插件链），每张卡写明 18 个 API、28 源、下载链或中文三源的取法。

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `paper-lookup.md` | K-Dense `scientific-agent-skills` | **18 个国际学术 API** 端点表（用途/端点/是否要 key），免 key 检索总入口 | ✅ 多数免 key |
| `gs-skills.md` | `cookjohn/gs-skills` | **Google Scholar** 6 技能：URL 参数/选择器/`data-cid`/BibTeX→Zotero | ❌ 需 Chrome+代理 |
| `paper-search-mcp.md` | `openags/paper-search-mcp`（+365-skills `paper-fetch`） | **28 源**统一检索 + **OA 优先 PDF 下载链**；附 `paper-fetch` 7 源链与 semanticscholar-skill | ✅ 多数源免 key |
| `papercash.md` | `Jesseovo/PaperCash` | **百度学术/知网/万方**三源接入端点与真实可用性 | ❌ 需 Cookie |
| `zotero-cn.md` | `jasminum`+`translators_CN`+`zotero-chinese/styles` | **GB/T 7714 引文 + 中文库元数据抓取 + 落 Zotero** | ✅ 样式可直取 |
| `article-mcp.md` | `gqy20/article-mcp`（+365-skills 期刊件） | **期刊分级/影响因子**（EasyScholar+OpenAlex） | ⚠️ 需 key |

### 专题卡（多源检索/定位 —— 一个主题跨多个站点）

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `preprints-cn.md` | ChinaXiv + NSTRS + 中国科技论文在线 | **中文预印本**与**国家科技报告**检索；NSTRS 浏览 API 匿名 JSON | ⚠️ NSTRS 可匿名浏览 |
| `econ-papers.md` | RePEc/IDEAS + NBER + CEPR + SSRN | **经济学工作论文**检索（NBER JSON API 实测可用） | ⚠️ SSRN 本机不通 |
| `institutional-repos.md` | OpenDOAR + ROAR + OpenAIRE + CALIS ETD | **按国家/学校定位机构知识库与学位论文** | ⚠️ OpenDOAR 本机 403 |
| `universities-open-data.md` | 各校 xxgk 信息公开专栏 + 软科 + 校友会 | **单校公开数据**（年度报告 / 预决算 / 就业质量报告）与**高校排名** | ✅ 软科 JSON 可直取 |
| `edu-finance.md` | 教育部 + 财政部 | **全国教育经费 / 教育部部门预决算 / 财政决算的教育支出** | ✅ 公告与 PDF 可直下 |

### 子目录

- `cnki/` —— 来自 GitHub `cookjohn/cnki-skills` 的知网操作手册全套（10 个子 skill + `push_to_zotero.py`）。**这些文档写的是 Claude Code 的 `mcp__chrome-devtools__*` 工具，本环境用 `browser`（eval 命名空间）等价替代**，映射表见 `cnki.net.md`。

### 待补/未验证

- `https://www.nationaldata.cn/`（国家数据）本机 `HTTP 000`（连接失败/DNS 不通），**未纳入**，需要时另起文件重探。
- NCPSSD 检索表达式字段码仅验证 `IKTE`（题名）与 `IKST`（主题词）；作者字段名、`sType` 其他取值尚未探明。
- **本机网络边界（通道卡相关，2026-10-02 实测）**：`scholar.google.com` → `HTTP 000`（不通，需代理）；`dblp`/`hal`/`base` → bot 墙或超时；`api.figshare.com` GET/POST 均 `403`；`api.core.ac.uk` 无 key `429`；百度学术匿名 `403`。用通道卡前先按这些现状选路。
- **专题卡本机边界（2026-10-03 实测）**：`www.ssrn.com`/`papers.ssrn.com` **超时**；`cepr.org/publications` **403**（但 `/publications/discussion-papers` 200）；`v2.sherpa.ac.uk`（OpenDOAR）全站 **403** Jisc WAF、`opendoar.org` TLS 握手失败，`roar.eprints.org` 检索 bot 墙（首页/RSS 可直取）；`www.irgrid.ac.cn` 超时、`ir.pku.edu.cn` 超时、`ir.whu.edu.cn` 403、多校 IR 域名 DNS 不解析；`chinaxiv.org/user/search.htm` **403「系统正在维护中」**（但 `/abs/`、`/user/preprintlist.htm` 200）；`paper.edu.cn` 全站维护；NSTRS `searches`/`searchtotal` 匿名 **302**（仅浏览 `listFilde` 可用）。
- `paper-search-mcp` 本体、`paper-fetch` 脚本、`gs-skills` 技能、`article-mcp` 的 `uvx` 启动均**未本机运行**（纪律：只读研究、不装第三方依赖），其行为为上游声明；端点层已用 curl 逐条探活。
- **海外源本机边界（2026-10-03 实测）**：`www.loc.gov`（含 `?fo=json` API）→ **403 Cloudflare**「Just a moment...」（curl 与无头 Chromium 均被拦）；`catalog.hathitrust.org` → **超时 HTTP 000**；`toyo-bunko.or.jp` → 200 但未探到数字检索入口，**均未纳入**。`ndlsearch.ndl.go.jp` 本机 **DNS 被解析到无关 IP**（157.240.2.50 / 31.13.76.99 …）导致 curl 超时，**NDL Search 必须走浏览器**。
- 未解项：`dl.ndl.go.jp` 的 `POST /api/item/search` 请求体结构未探明（GET 405 / 猜测体 400）；`taiwan-libraries.md` 里华艺（airitilibrary）**公开检索 URL 未探到**（全站跳机构认证页）；香港 GRS 的繁中 `/tc/` 路径与「網上目錄」独立系统未实测。
- **欧美馆藏本机边界（2026-10-03 实测）**：`www.hoover.org`/`digitalcollections.hoover.org` DNS 被解析到无关 IP（`128.242.240.149`/`104.244.46.21`）→ curl HTTP 000，**浏览器正常**；`searchworks.stanford.edu` curl 000、`hoover.aeon.atlas-sys.com` curl 403；`api.lib.harvard.edu`/`iiif.lib.harvard.edu` curl **429**（浏览器正常）、`curiosity.lib.harvard.edu` curl 202 空体；`idp.bl.uk` curl 与无头 Chromium 均被 Cloudflare「Just a moment...」拦（镜像 `idp.nlc.cn`/`idp.bbaw.de` 仅 http 可用）；大英图书馆旧入口 `www.bl.uk/manuscripts` → 404。以上未纳入的 LoC/HathiTrust 见上一条。
- `european-china-collections.md` 中 TNA Discovery 的下载/订购流程、Gallica 高清下载条款、SBB 检索站（Meteor SPA）的匿名 JSON 接口均**未探明**，卡片按「目录/API 可用」层面记录。
- **高校/教育财政本机边界（2026-10-03 实测）**：`xxgk.tsinghua.edu.cn`、`xxgk.zju.edu.cn`、`xxgk.whu.edu.cn` **DNS 不解析**（HTTP 000），`xxgk.sjtu.edu.cn` 302 → `restrict.sjtu.edu.cn` 反爬页——**不代表没有信息公开专栏**，换出口/浏览器重试；南大 `/16401/list.htm` 等列表页条目由 JS 渲染，简单 `href` 抓取会漏。软科 `bcur_type` 仅实测 `11`（主榜 594 所）与 `21`（医药类 84 所），其余分类码未探明；校友会站**仅 HTTP + GBK**，`https://www.cuaa.net/`、`https://www.chinaxy.com/` 均连接失败。教育部 `jyb_xxgk/xxgk/neirong/caizheng/` 列表为脚本渲染（curl 只见导航），财务数据以 `…/xxgk_cwxx/cwxx_jfgl/` 静态专栏为准。

## 选路

- **要中文期刊论文列表/摘要** → 先 `ncpssd.org`（curl JSON，最省事）；再 `cqvip.com`（首页 HTML）交叉。
- **要核心/CSSCI 收录核验 / 期刊分级** → NCPSSD 行内 `range`、维普结果页"北大核心 CSSCI CSTPCD"标记；要影响因子/中科院分区 → `article-mcp.md`（EasyScholar，**需 key**）。
- **要 GB/T 7714 引文 / 中文引文样式** → `zotero-cn.md`（`zotero-chinese/styles`，343 个样式，raw 可直取，CC BY-SA 3.0）。
- **要中文库（知网/万方/维普/读秀/NCPSSD/人民网/数字报）元数据抓取规则** → `zotero-cn.md`（`translators_CN` 99 个 translator + `jasminum` 知网抓取，AGPL 只读不抄）。
- **要免 key 国际库检索（OpenAlex/Crossref/Europe PMC/Semantic Scholar…）** → `paper-lookup.md`。
- **要一次查多库 + 自动拿全文 PDF** → `paper-search-mcp.md`（28 源下载链 + 同类 `paper-fetch` 7 源链：Unpaywall→S2→arXiv→PMC→bioRxiv/medRxiv→出版社→Sci-Hub）。
- **要谷歌学术（被引链/BibTeX）** → `gs-skills.md`（需可见 Chrome + 能连 scholar.google.com）。
- **要百度学术**：`papercash.md` —— 但匿名 curl 被"安全验证"，需真 Cookie。
- **要知网专属内容（政报/年鉴/学位论文）** → `cnki.net.md` + `navi.cnki.net.md`，走浏览器人工过码。
- **万方/读秀/超星**：默认放弃 curl，需机构 IP 或人工登录；详见各自文件（`papercash.md` 有万方未登录实测）。
- **图书书目** → `opac.bac.gov.cn.md`；图书全文一般做不到匿名抓取。
- **要外文科技期刊/会议/学位论文/科技报告（含开放获取标识与「可否原文传递」）** → `nstl.gov.cn.md`（检索接口匿名 JSON，字段是短码+数组+`<em>` 高亮）。
- **要中文预印本 / 国家科技报告（立项、承担单位、摘要）** → `preprints-cn.md`（ChinaXiv 详情/浏览可直取、检索需浏览器；NSTRS 浏览 `POST /rest/kjbg/wfKjbg/listFilde` 匿名 JSON）。
- **要经济学工作论文（NBER WP / CEPR DP / RePEc 系列）** → `econ-papers.md`（NBER `api/v1/...search` JSON、IDEAS `POST /cgi-bin/htsearch2`；SSRN 本机不通，元数据退 OpenAlex）。
- **不知道某校/某所的机构知识库在哪，或要找该校学位论文** → `institutional-repos.md`（OpenDOAR 国家页 → ROAR/OpenAIRE 备用 → CALIS ETD 学位论文；中国 IR 域名无统一规律）。
- **要某校的年度报告 / 财务预决算 / 招生就业 / 毕业生就业质量报告** → `universities-open-data.md`（`xxgk.<校域名>` 信息公开专栏，附件 PDF 可直下；个别校被 WAF/DNS 挡，见卡片「坑」）。
- **要高校排名且想整表取数** → `universities-open-data.md`（软科 `api/pub/v1/bcur?bcur_type=11&year=` 返回 JSON；校友会仅 GBK HTML、无 API）。
- **要全国教育经费 / 教育部部门预决算 / 财政决算里的「教育支出」** → `edu-finance.md`（教育经费公告 + `.doc` 统计表、部门预/决算 PDF 直链、财政部 `{年}zyjs` 决算 HTML 表）。
- **只有书名/篇名，要判断「谁能免费给全文 / 藏在哪个馆」** → 跨站路由卡 [`methods/literature-delivery.md`](../methods/literature-delivery.md)（CALIS 联合目录 → 国图读者云门户 / NCPSSD → NSTL 原文传递 → 馆际互借）。
- **要近代中日关系的一手档案（含免登录图像）** → `jacar.md`：检索 URL 必须带全 `kl0`+`ks0`+`kw0`+`rows`+`sf`，图像在 `digital.archives.go.jp` 的 IIIF（有速率限制）。
- **要日文近代中国文献的书目/数字馆藏** → `ndl-japan.md`：先用 NDL Search OpenSearch/SRU API 拿书目，再用数字馆藏的 `searchResult` URL 定位；只有「インターネット公開」档能匿名取图。
- **要台湾学位论文题录 / 台湾图像** → `taiwan-libraries.md`（NDLTD 永久链接可 curl；臺灣記憶 GET 参数可用）；**华艺需机构 IP**。
- **要香港旧报纸、政府档案** → `hk-libraries.md`（GRS 可 curl；香港公共图书馆數碼館藏需过 Queue-it）。
- **要民国/近代中国档案、两蒋日记、20 世纪宣传品** → `hoover-institution.md`（本机必须浏览器；两蒋日记仅馆内阅览+预约+协议，不能下载）。
- **要中文善本/古籍、地方志、东亚书目** → `harvard-yenching.md`（LibraryCloud `items.json` 与 CURIOSity `catalog.json` 是 JSON，但本机 curl 429/202，走浏览器；IIIF 经 `nrs.lib.harvard.edu`）。
- **要敦煌写本/吐鲁番文书、清代 FO 外交档案、欧洲汉籍** → `european-china-collections.md`：IDP 走北京/柏林镜像（主站 Cloudflare 拦）、TNA Discovery API 免 key、Gallica SRU+IIIF、SBB OAI+IIIF。

## 相关

- [`methods/literature-delivery.md`](../methods/literature-delivery.md) —— 跨站文献获取路由（CALIS 联合目录 → 国图读者云门户 / NCPSSD → NSTL 原文传递 → 馆际互借）。
- `references/archives/bjdsdfz.cn.md`、`references/archives/bjsfzg.bjdsdfz.cn.md` —— 京网/数字方志馆，区级年鉴的另一官方渠道。
- `references/wechat/weixin.sogou.com.md` —— 搜狗微信检索流程（「皮书说」公众号原文）。
