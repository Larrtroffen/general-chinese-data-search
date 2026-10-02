# references/archives —— 方志·档案·古籍·人物库

本层收录方志与文献类来源：志书/年鉴在线平台、古籍全文库、**民国书刊报平台**、古人人物数据库、地方志官网，以及「本地检索」工具（把语料变成可查索引）。

## 文件一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `modernhistory.md` | **抗日战争与近代中日关系文献数据平台**（中国历史研究院近代史所） | 民国书/刊/报/档案**免费检索 + IIIF 图像** | ✅ 匿名可用 |
| `guji.nlc.cn.md` | **中华古籍智慧化服务平台**（国图） | 古籍书目/版本/收藏单位检索 | ✅ 检索可用 |
| `shuge.md` | **书格**（+ 存储 `shuge.hanjihebi.com`） | 公共版权古籍 **PDF 下载** | ✅ 检索可用 |
| `cnbksy.md` | 全国报刊索引（上海图书馆） | 晚清民国报刊**篇名/全文**索引 | ❌ 机构订阅 |
| `dachengdata.md` | 大成故纸堆 | 古旧文献综合库（老刊/民国图书/方志/家谱） | ⚠️ 登录墙 |
| `modern-press-databases.md` | 近代/民国报刊数据库目录（爱如生/瀚堂/国图/人民日报/光明日报/繙云等） | 晚清民国报刊**有哪些库、门槛与入口** | ⚠️ 多为订阅 |
| `bjdsdfz.cn.md` | 京网（北京市委党史研究室·市地方志办） | 北京区综合年鉴、志书在线版 | ⚠️ 需登录 |
| `bjsfzg.bjdsdfz.cn.md` | 北京市数字方志馆 | 志鉴检索、《北京年鉴》2012–2021、民国年鉴 | ⚠️ 需浏览器 |
| `difangzhi.cn.md` | **中国方志网**（中国地方志工作办公室） | 全国方志系统**全文检索**（`was5` 接口）、志书/年鉴选介 | ✅ 检索可用 |
| `local-gazetteers-cn.md` | **全国省级方志/省情网站总表**（31 机构+兵团） | 逐省入口 + 浙/粤/鲁/湘**可直连检索接口** | ✅ 多省检索可用 |
| `nlc.cn.md` | 国家图书馆 | 民国期刊/民国图书/古籍/地方文献**入口**；`mg.nlc.cn` API | ⚠️ 需登录 |
| `archives-cn.md` | **国家档案系统**（国家档案局 / 一史馆 / 二史馆 / 13 省级馆） | 档案目录检索（一史馆 `/ess/` 匿名可查）、查档平台门槛 | ⚠️ 多数需注册 |
| `shtong.md` | **上海通 / 上海数字方志** | 上海方志·年鉴·大事记·展览 | ✅ 开放 API |
| `kanripo.md` | **漢籍リポジトリ（Kanseki Repository）** | 汉文古籍**全文**（9355 个单书仓） | ✅ raw 直取 |
| `ctext.md` | 中国哲学书电子化计划 | 先秦两汉典籍原文/注疏 | ❌ 禁止爬 |
| `daizhige.md` | 殆知阁（daizhigev20） | 古代文献 txt **大全集**（约 2.1 GB） | ✅ 入口可用 |
| `cbdb.md` | **CBDB 中国历代人物传记资料库**（SQLite 版） | 历史人物/官職/亲属/社会关系**数据库** | ⚠️ 需镜像 |
| `sinica.md` | **中研院（Sinica）系**（史語所/近史所档案与人物库） | 人名權威檔 + 档案目录 + 漢籍全文 | ⚠️ 部分可用 |
| `person-databases.md` | 中华英烈网 / 两院院士 / 中国文明网荣誉 / 地方党史人物 / 图书馆人物图像 | 人物·荣誉·英烈名录检索 | ⚠️ 部分需浏览器 |
| `local-search-tools.md` | SQLite FTS5 / whoosh-reloaded / jieba | 抓完的语料建**本地全文索引** | ✅ 方案可用 |
| `historical-maps.md` | CHGIS / 中研院 GIS / 复旦镜像 / TGaz / 观沧海 | 历史地图与 GIS：政区沿革、地名查询、古地图 | ⚠️ 部分需浏览器 |

## 选路

- **民国书/刊/报取数优先级（2026-10 实测口径）**：
  1. **`modernhistory.md`** —— 免费、免登录、JSON 检索 + IIIF 图像直取；1931–1945 及抗日主题最厚（总量 18.6 万种/册），**首选**；
  2. **`guji.nlc.cn.md`** —— 古籍书目与收藏单位（`POST /api/resource/list` 匿名可用）；书影阅读器另说；
  3. **`shuge.md`** —— 需要「整本古籍 PDF」时，直接去 `shuge.hanjihebi.com` 的 OpenList API 搜文件、`/d/` 直下；
  4. **`cnbksy.md`**（全国报刊索引）—— 报刊面最宽（1816 至今 / 晚清民国全文 / 近代报纸），但**机构订阅 + WAF**，作为"知道去哪找、知道要什么权限"的通道；
  5. **`dachengdata.md`**（大成故纸堆）—— 老刊/民国图书/方志/家谱，机构登录制；
  6. 国图民国期刊全文（`read.nlc.cn`，读者卡）与民国图书（`mg.nlcpress.com`，付费）见 `nlc.cn.md`。
- **古籍全文取数优先级**（合规 + 稳定性）：
  1. **Kanripo**（`kanripo.md`）：raw 直取、按卷分文件、无墙 → 首选；
  2. **殆知阁**（`daizhige.md`）：要「一次拿全、离线 grep」时整包下（2.1 GB），版本杂、要核对；
  3. 订阅制 API（ctext 订阅、中华经典古籍库等商业库，见 `../academic/`）；
  4. ⛔ **不要**绕 Cloudflare 抓 `ctext.org`（`ctext.md`：作者已明确拒绝，且会返回被故意污染的数据）。
- **志书/年鉴全文的常见获取路径优先级**：
  1. 地方志官网（京网 `bjdsdfz.cn`、上海通 `shtong.gov.cn`、江苏 `jssdfz.jiangsu.gov.cn`…，`difangzhi.cn` 首页友情链接有 30+ 条清单）；
  2. 数字方志馆（多需注册）；
  3. 商业库（CNKI 年鉴库、中国历史文献总库·民国图书 `mg.nlcpress.com`）。
- **人物数据**：本层 `cbdb.md` 是人物身份/官職的权威底板；与方志、登科录交叉核对时以 `c_personid` 为锚；民国人物补充 `sinica.md`（人名權威檔 + 近史所档案）。
- **建本地索引**：抓完的语料要反复查 → `local-search-tools.md`（FTS5 + trigram 实测可用）。

## 相关

- 来源站细节（接口/字段/坑）见各卡片；商业古籍论文库见 `../academic/`。
- 法律/文书类：`../legal/`（裁判文书、案例库）。
- 抓取与清洗工具：`../tools/`（`macos-vision-ocr.md`、`mineru.md`、`defuddle.md`、`agent-browser.md` 等）。
- 人物/官员检索方法：`../methods/officials-research.md`。
- 官方数据/政策：`../gov/`。
- 跨库候选清单与进度：`../../CANDIDATES.md`。
- **高亮标签要剥**：`modernhistory` 用 `<span style='color:#981722'>`，`guji.nlc.cn` 用 `<font color='red'>`；不清洗会造成同一文献重复计数。
- **域名更正**：任务书中的 `dfz.org.cn` 不存在（NXDOMAIN）；中国方志网实际为 `www.difangzhi.cn`（见 `difangzhi.cn.md`）。
- 中国方志网的「全文检索」只覆盖本站文章（新闻/选介），**不是志书正文库**，勿误用。
- **SPA 站点挖接口**的通法（`shtong.md` 是完整范例，`guji.nlc.cn.md` / `modernhistory.md` / `nlc.cn.md` 是新增三例）：首页 → 入口 JS（`/static/index-*.js`、`app.*.js`、`index.*.js`）→ 动态 chunk → `grep 'baseURL'`、`grep '"/api/…"'`、`grep 'url:"/…"'` → 直调 JSON 接口，比驱动浏览器便宜得多。本层 SPA 大多是 **5–6 KB 外壳 + 匿名 JSON 后端**，别看到壳就放弃。
