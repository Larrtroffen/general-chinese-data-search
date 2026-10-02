---
name: general-chinese-data-search
description: 中文公开资料检索总集（分级源库 + 可复用脚本）：综合搜索引擎、微信公众号（搜狗检索/正文抓取/客户端抓包）、政府网站（中央/北京/16区/信息公开年报）、统计与区划、媒体与数字报、学术文献（CNKI/万方/维普/NCPSSD/皮书/北大法宝）、方志年鉴与档案、党建、法律法规、社交平台。当用户要检索中文资料、找政策文件/单位名录/统计口径、搜微信公众号文章、爬取网站或文章正文、核对试点名单，或维护数据源清单时使用。触发词：搜狗微信、微信公众号、爬虫/爬站、政府网站、政策文件、统计年鉴、数字报、区划名录、CNKI、数据源清单、北京。
---

# 中文公开资料检索（分级源库 + 脚本）

**定位**：接任何中文资料检索需求 —— 先在分级源库里选通道，再按对应手册操作；点查用引擎，批量用脚本。

结构：
- `references/<层>/` —— 源库：**一个来源一个文件**，层内有 `README.md` 索引。共 25 层：`engines 综搜 · wechat 微信 · gov 政府 · party 党建 · stats 统计 · business 企业与市场 · finance 金融与财税 · health 健康与人口 · surveys 调查与微观数据 · repos 数据仓储 · intl 国际数据 · industry 行业与协会 · regional 区域与地方 · env 环境能源碳 · civil 公益与志愿服务 · culture 文化民族宗教语言 · media 媒体 · academic 学术 · corpora 语料 · legal 法律 · archives 方志档案 · social 社交（含问政） · tools 工具 · methods 方法 · meta 元资源`；来源卡字段固定：`去哪找 · 什么时候用 · 怎么搜/怎么取 · 覆盖 · 门槛 · 实测 · 上游`（写法见 `references/meta/style.md`）
- `scripts/` —— 可复用操作脚本（标准库 + 系统 curl，零依赖）；见 `scripts/README.md`
- 本文件 = 顶层工作流 + 分层总表 + 环境与体量纪律 + 汇总口径

## 顶层工作流

1. **拆需求 → 选层**：政策文件 → `gov/`+`legal/`；文章/报道 → `wechat/`+`media/`；数字/名录 → `stats/`；论文/书 → `academic/`；**研究数据 → `surveys/`（调查微观）·`repos/`（仓储）·`intl/`（国际）·`business/`（企业与市场）·`health/`（健康人口）·`corpora/`（语料文本）**；旧版页面 → `archives/`+`tools/`；**不知道去哪 → `meta/`；不知道怎么搜/怎么拿到全文 → `methods/`**。
2. **点查 → 引擎**：`web_search` 工具（短会话）+ `engines/`（头条/必应/神马/百度移动版，见 `engines/README.md` 的降级顺序）。
3. **批量 → 垂直通道**：搜狗微信（关键词放量）、站内检索 JSON API（如首都之窗、人民网、党建网、flk）、`site_crawl.py`（整站语料）。
4. **链接 → 正文**：搜狗 `/link` **现取现解析**（token 分钟级）→ 立刻抓正文（`mp_article.py`）；长任务分片 + JSONL 断点续跑。
5. **汇总**：按「数据口径」去重/分层/核对覆盖（见文末）。

## 分层总表

| 层（目录） | 里面有什么 | 首选通道（状态速记） |
|---|---|---|
| `engines/` 综合搜索 | 百度/必应中国/头条/神马/360/搜狗网页/中国搜索 | 头条 ✅、神马 ✅、必应 ⚠️(需预热 cookie)、百度 ⚠️(移动版稳)、360 ⚠️、搜狗网页 ⚠️、中国搜索 ❌(IP 管控) |
| `wechat/` 微信生态 | 搜狗微信（关键词索引）、mp.weixin 正文、wechatspider（按号全量+阅读数） | 搜狗 wap ✅ 主通道；正文 ✅（签名链接 ~8 分钟）；wechatspider 工具可用（macOS+微信客户端） |
| `gov/` 政府网站 | 中国政府网、首都之窗、区门户/人大、年报树、人才/职称、国防/退役军人、营商环境/城市信用 + **北京委办局站群/街乡镇栏目/公开渠道** | gov.cn/首都之窗 ✅；**北京 52 委办局子站全 200**；**10 类易漏文件栏目（依申请/审计/事故/规划/征收）** |
| `party/` 党建 | 共产党员网、北京组工、党建网、中国共产党新闻网、顺义组工镜像 | 北京组工 ✅、党建网检索 ✅（标题级）、12371 ✅、人民网党员网检索 ✅ |
| `stats/` 统计与区划 | 国家统计局、国家数据、民政区划、部委统计、地理数据、**迁徙/通勤**、**农业价格**、**县域/投入产出/电商** | **民政四级代码 ✅**；**百度迁徙 JSONP ✅**；农产品 200 指数 ✅；**投入产出表 xls ✅**；电商 JSON ✅ |
| `business/` 企业与市场 | 巨潮资讯、沪深北交所、证监会、中债、海关、CSMAR/CNRDS/CEIC/Wind、高企/专精特新、**招投标历史** | **巨潮公告检索 JSON ✅**；深交所公告 JSON ✅；**千里马招标匿名 API ✅**（历史 2012 起）；海关 ❌ WAF |
| `finance/` 金融与财税 | 央行/外汇局/监管总局、行业协会、期交所/上金所/上清所、财政预决算、地方债城投、税收 + **支付/银行/保险业** | 央行/外汇局 ✅；AMAC/中期协 ✅；地方债 JSON ✅；**支付体系 PDF ✅、保险信息披露 JSON ✅**；NFRA 403 |
| `health/` 健康与人口 | 疾控、卫健委、ncmi、IHME/GBD、WHO、人口普查 + **药监注册库/药品集采** | ncmi ✅、WHO GHO ✅；**NMPA 数据查询迁移至 datasearch（UDI 子站可 curl）**；上海阳光采购集采 PDF ✅ |
| `surveys/` 调查与微观数据 | CFPS/CGSS/CHARLS/CHFS 等、CNSDA、IPUMS、统计局微观 + **招聘平台就业报告** | CNSDA 免登录 ✅；前程无忧 PDF 年链 ✅；CHARLS/CFPS 需注册；智联/BOSS 受限 |
| `repos/` 数据仓储 | Dataverse/Zenodo/Dryad/OSF/Figshare/Kaggle/DataCite/re3data/ICPSR/GESIS + 国家科学数据中心体系 | **Dataverse/Zenodo/Dryad/DataCite/re3data API ✅**；nbsdc 检索 JSON ✅；ICPSR ❌ Cloudflare |
| `intl/` 国际数据 | 国际组织统计/跨国调查/IFI 项目库/报告全文库/MRIO + **留学生与华侨华人** | 世行 API ✅、项目库 ✅、OKR/UN DL ✅；**IRCC CSV + StatCan API ✅**；IIE/HESA ⚠️ CF |
| `industry/` 行业与协会 | 行业协会、央企、铁路民航城轨、住建、快递物流、开发区、通信、港口航运/旅游/体育 + **土地与房地产** | 汽车/PMI ✅、央企/开发区 ✅、CNNIC ✅、港口+SCFI ✅、OpenSky ✅、**土地市场 JSON API ✅** |
| `regional/` 区域与地方 | 省级社科院、高校平台、地方/区域数据、省年鉴、县级入口 + **港澳台统计** | **data.gov.hk CKAN ✅、DSEC API ✅、data.gov.tw 前端 API ✅**；清华 TCDC ✅；广东社科院 ❌ |
| `env/` 环境能源碳 | CEADs、生态环境统计、空气质量、排污许可、IPE、能源局、resdc、气象、EM-DAT + **执法处罚/督察** | **空气质量 JSON ✅**、气象指数 txt ✅；**中央环保督察公告/反馈 ✅**、部处罚专栏 ✅、省厅专栏部分仅浏览器 |
| `civil/` 公益与志愿服务 | 慈善中国、基金会中心网、志愿服务协同平台、腾讯/支付宝公益、中慈联、基金会论坛 | **基金会中心网检索分面 API ✅**（匿名）；慈善中国/志愿平台登记门；腾讯公益检索需浏览器 |
| `culture/` 文化民族宗教语言 | 国家民委、语保工程、非遗网、文物局、宗教局、UNESCO 遗产 + **文化市场统计**（电影/出版/文旅/视听） | **非遗名录 JSON ✅**、**宗教场所 API ✅**；**出版统计公报 PDF ✅**、电资办票房、CIP 核发（AES 可解） |
| `media/` 媒体与文档 | 央媒/市媒/地方融媒/数字报 + **文库分享站/论坛附件区** | 人民网/新京报 API ✅；**book118/金锄头可取证、360 搜索 site: 定位文库**；论坛多需注册 |
| `academic/` 学术 | CNKI 全套、NCPSSD、NSTL、预印本/工作论文、海外港台馆藏（JACAR/NDL/台湾/香港/**胡佛/哈佛燕京/欧洲敦煌**） | **NSTL 匿名检索 ✅**；哈佛 LibraryCloud/IIIF ✅；IDP/Gallica/TNA API ✅；CNKI/万方 ⚠️ 滑块 |
| `corpora/` 语料文本 | BCC/CCL 语料库、人民日报标注语料、中文 NLP 数据集（CLUE 等）、HF 镜像、CBETA | **CCL 匿名检索 ✅**；CLUE 仓 ✅；BCC 下载 ✅（检索需验证码）；《人民日报》标注语料有 DOI |
| `legal/` 法律 | flk、法宝、裁判文书网、标准体系、rmfyalk 案例库 | flk ✅（POST + 原件下载）；**国家标准全文公开系统 ✅**、行标/地标检索 JSON ✅；法宝 ⚠️ 需 Token |
| `archives/` 方志档案 | 京网、数字方志馆、中国方志网、省方志总表、抗战文献平台、国图古籍、档案系统、民国报刊目录 | **modernhistory 匿名检索 + IIIF ✅**；国图古籍检索 ✅（需 Referer）；一史馆档案目录 ✅；地方志 4 省直连检索 ✅ |
| `social/` 社交与问政 | 微博/知乎/贴吧 + **问政平台（领导留言板/百姓呼声/网上民声）** | 微博热搜、**百姓呼声/网上民声 JSON ✅**、领导留言板（需签名）✅；知乎/贴吧 ❌ 需登录 |
| `tools/` 工具 | Wayback、Jina Reader | Wayback ⚠️ 间歇可达；r.jina.ai ❌ 本机不可达 |
| `methods/` 检索方法 | 文献传递路由、各站高级检索语法、历史网页回捞、官员检索法、免费数据集市 | **跨源方法卡**：不知"怎么搜/怎么拿到全文"时先看这层 |
| `meta/` 元资源 | MCP/技能目录、发现机制；**中国应用 MCP 索引**（87 仓库+91 项官方 API） | 不知道「去哪找」时先来这层；找新源方法见 `meta/skills-discovery.md` |

## 脚本（scripts/）

| 脚本 | 用途 |
|---|---|
| `sogou_wechat.py` | 搜狗微信检索 + `/link` 现取现解析（分片、断点续跑） |
| `mp_article.py` | 微信文章正文 → Markdown/JSON（含 biz/mid/idx 身份、deleted/blocked 判定） |
| `bjgov_search.py` | 首都之窗统一搜索 JSON 接口（北京市/区政府站内检索） |
| `site_crawl.py` | 站内 BFS 爬取（分页穷尽、robots、主机限速、断点） |
| `fetch.py` / `probe.py` | 单请求抓取/探活；批量 URL 体检（维护源库用） |

```bash
python3 scripts/sogou_wechat.py search queries.txt --out crawl.jsonl --resolve 2018
python3 scripts/mp_article.py batch --in crawl.jsonl --out-dir articles --limit 50
python3 scripts/bjgov_search.py 吹哨报到 --filter bjchy.gov.cn
python3 scripts/site_crawl.py --host www.bjdx.gov.cn --budget 20
python3 scripts/probe.py urls.txt --out status.csv
```

## 维护源库（加新源 = 加文件）

1. 新源写成 `references/<层>/<host>.md`，**先读 `references/meta/style.md`**：标题 `# <规范名> —— <定位≤18字>`（无 owner 前缀、无括号渠道标签），字段顺序固定 `去哪找 → 什么时候用 → 怎么搜/怎么取 → 覆盖 → 门槛 → 实测 → 上游`，细节表格放 `## 细节`。
2. **状态必须来自实测**：跑一条最小请求（`scripts/fetch.py --probe` 或 `probe.py`），把命令与结果写进文件；没探到的写「未验证」，不要猜。
3. 同层 README.md 同步加一行；跨层引用用相对路径。
4. 定期用 `scripts/probe.py` 批量体检，状态变了就地更新（例：Wayback 从「不可达」→「间歇可达」）。
5. **外部候选池**：`CANDIDATES.md` —— GitHub / skills.sh 侦察到的可收编 skill 与资源（含热度、依赖、证据、优先级）。
   收编后把该项状态改为 `已收编→<目标文件>`；每季度按文末「检索方法备忘」重跑并追加新候选。

## 环境与体量纪律（本机）

- **运行环境**：macOS；`python3` 3.9 **无 requests/bs4/lxml** → 脚本一律标准库 + `curl` 子进程。政府站常见自签/证书错配（`curl -k`）、GB18030/GB2312 编码（iconv/chardet 兜底）。
- **浏览器**：本机可用的是 **headless** daemon；需要可见浏览器过验证码的站点（CNKI、必应交互页）要人工介入。headless 也会被搜狗/必应识别。
- **`web_search` 工具**：短点查可用，但实测约 25 次调用后全 provider 429（且偶发 bot challenge）→ 批量任务不要依赖它。
- **长任务**：单条命令硬上限 **3600s**，超时被杀；`nohup … &` 在工具调用返回时也会被杀 → 用后台任务机制跑，脚本必须带断点（JSONL 标记）。
- **并发写盘**：多进程不要 append 同一个 JSONL（会撕裂行）→ 按主机/分片一文件。
- **主会话体量**：DeepSeek 对超长中文上下文会直接 400 `Content Exists Risk`（无自动重试，实测）→ 大体量爬取文本**不要灌进主会话**；分片交子代理、结果落盘，主会话只读统计。
- **kernel**：eval/kernel 可能被强杀 → 中间产物随手 flush 到磁盘。

## 数据口径（汇总通用）

- 去重键：`(date, title, account)`（微信文章可用 `__biz/mid/idx` 更稳）。
- 来源层级（市/区/乡镇/官方媒体/自媒体/企业/学校/外省）**逐个人工判定**，不要用正则冒充；账号池大时先建映射表再复用。
- **索引上限 = 语料上限**：搜狗每条检索式最多 100 条（10 页×10），主题词饱和后新增趋零；不要幻想用主题词穷尽。
- 时间：搜狗 `data-lastModified` 是**发布日**（本地时区换算）；`tsn/ft/et` 时间过滤已封死 → 用「年份词 + 主题词」放量。
- 覆盖核对：按单位/来源出「有语料/零命中」清单（零命中要回看单位名变体与匹配规则是否过严）。
