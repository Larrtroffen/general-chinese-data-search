# CANDIDATES —— 外部 skill / 资源收编候选清单（backlog）

> 来源：2026-10-02 十路领域侦察（GitHub `gh search` + skills.sh 注册表 + 实际抓取 SKILL.md/README 核验）。
> 热度 / 更新日期 / 依赖均为侦察时实际返回；**未标注"本机实测"的均为未在本机跑通**。
> 状态词：`候选`（默认）/ `已验证` / `已收编→<目标文件>` / `放弃`。

## 收编流程（三步，慢慢来）

1. **本文件排队**：候选=链接+能提供什么+证据（已有）；你挑一批。
2. **本机验证**：跑最小可行样例（零依赖优先；确认 license、需不需要 key/登录/装东西；记录实测）。
3. **收编（不整仓拷贝）**：把「接口/方法/坑」写进对应 `references/<层>/<host>.md`；能脚本化的进 `scripts/`；
   更新层 `README.md` + 总索引；在文件尾写「来源：<repo>（已核验，日期）」。执行第三方代码前必须单独立项审查。

**纪律**：无 license 仓库只读用法不抄码；AGPL/非商用类只作参考；第三方 skill 默认只提取方法、用我们的零依赖方式重写。

## 首批收编进度（2026-10-03 完成）

> 7 个集成 agent 按「下载→挑选→落 source 卡」执行完毕；新增 **58 个文件**（source 卡 + 层 README 更新）。
> 全部为**来源卡**（去哪找/何时去/怎么取/覆盖/限制），未搬运数据本体、未执行第三方代码、未引入第三方源码。

| 层 | 新增卡 | 亮点 |
|---|---|---|
| `wechat/` | wewe-rss, wechat-download-api, wechat-digest-skill, wechat-article-extractor, wechat-downloaders | 后台凭证/客户端两类通道的"钥匙-能力-代价"对比；失败态码表 |
| `social/` | cn-scraper-mcp, chubbyskills, agent-reach, xiaohongshu-mcp | 登录态平台（小红书/B站/知乎/微博）通道卡 |
| `gov/` | china-policy-sites, gov_opendata, gov-policy-mcp | **80 部委入口全量内联**+省级索引+10 个城市政务公开存档仓；开放数据平台 41 个实测状态 |
| `stats/` | mcp-cnbs, cnstats, data_location, akshare, national-data-corpus, nbs-api-skills | NBS 新端点（`/query?search=`、daCid/cid 常量）；乡镇级离线码；1978–2014 年鉴 CSV 入口 |
| `legal/` | chinese-law-corpus, legal-cn-mcp-hub, cn-law-hub, lawtext-laws, yuandian-law-search | CC0 逐条法条+案例语料；**rmfyalk 案例库逆向 API**（补裁判文书空白）；flk 离线镜像 |
| `academic/` | paper-lookup, gs-skills, paper-search-mcp, papercash, zotero-cn, article-mcp | 18 个国际库 API 源表；28 连接器；GB/T 7714 引文；中文库（知网/万方/百度学术）接入点 |
| `media/` | rsshub, news-aggregator-skill, people-daily-crawler, xinwenlianbo-archive, gopup, redfox-community | RSSHub 中文路由表（公共实例实测）；新闻联播每日 raw；人民日报 URL 形态 |
| `archives/` | kanripo, cbdb, daizhige, ctext, shtong, local-search-tools | 汉籍 9355 书仓 raw 可取；CBDB 走 hf-mirror；**上海通发现免 key 全文 JSON API** |
| `tools/` | agent-browser, defuddle, playwright-cli, scrapling, glm-ocr, mineru, macos-vision-ocr | 抓取/清洗/OCR 能力卡；macOS Vision OCR 零依赖（本机实测） |
| `meta/` | **新建层**：awesome-china-mcp（87 仓库+91 项官方 API 全摘录）、awesome-lists、skills-discovery | 「找源的地方」；季度巡检机制 |

**待办（二/三梯队）**：GLM-OCR 本地版（需 Ollama）、MinerU 安装、scrapling/agent-browser 落地脚本化；需 key 的候选（redfox/元典/EasyScholar）作备选席；`wenshu` 替代、通用 epaper 引擎已确认不存在（不再找）。



## 第二批：源 + 搜索方法（2026-10-03）

第二轮按「找源、找搜索方法、不装东西」执行：16 张新来源卡 + 6 张方法卡（新增 `methods/` 层），并对全库做了**转写归一**（9 个 agent、约 150 个文件：标题去冗、七字段统一、层 README 三段式；lint 0 标题问题 / 0 缺字段）。

| 层 | 新增/更新 | 亮点 |
|---|---|---|
| `archives/` | modernhistory、guji.nlc.cn、shuge、cnbksy、dachengdata、sinica | **抗战平台匿名 JSON 检索 + IIIF 图像直取**（185,994 文件）；书格走 OpenList API；中研院人名权威/汉籍/档案检索 |
| `gov/` | credit-china、gsxt、ccgp-ggzy、chinanpo、ip-cnipa、sydj、renshi-sources | 公共资源交易 `getTradList` JSON 实测打通；人事任免源清单（人大网 2007→今静态列表、人民网任前公示聚合） |
| `stats/` | cnki-data、epsnet、cei-drc | 中经网必须 POST `highSearch.action`（GET 返回 0 篇）；EPS 指标联想匿名可 curl |
| `party/` | dswxyjy | 党史文献站内检索 JSON API（`search.peopletech.cn`，返回正文原文） |
| `methods/`（新层） | dataset-hubs、literature-delivery、search-syntax、historical-web、officials-research、osint-china | 免费数据集市 JSON 接口；**从书名/篇名到全文的文献传递路由**（NSTL 匿名检索接口实测、CALIS CQL-base64 JSON）；B 站检索 API 匿名可用；历史网页回捞现状（Web 信息博物馆已死、国内快照全下线） |
| `academic/` | nstl.gov.cn | NSTL 检索接口全文（期刊 4987/学位 965/会议 11 命中实测） |

**确认消亡/不可达（不再重复找）**：webinfomall（NXDOMAIN，域名待售）、国史馆 drnh（TCP 不通）、CASHL（本机网络边界）、旧党史网 zgdsw.org.cn、Bing/百度/360/搜狗 快照全下线。

## 第三批/第四批：学科数据全面扩容（2026-10-03）

第三批（8 路：地方志、近代报刊、标准、档案、海外港台、部委统计、人物库、教育科研）与第四批（8 路：调查微观、数据仓储、国际数据、企业市场、健康人口、语料、方法补卡、预印本）全部落地；**新增 6 个学科层**（`surveys/ repos/ intl/ business/ health/ corpora/`），卡片一律按 `meta/style.md` 终版格式书写，lint 0 标题问题 / 0 缺字段。

| 新层 | 卡片数 | 亮点 |
|---|---|---|
| `surveys/` | 11 | CFPS/CGSS/CHARLS/CHFS/CEPS… 的申请门槛与波次；**CNSDA 免登录检索**；统计局微观数据只能现场用 |
| `repos/` | 15 | **Dataverse/Zenodo/Dryad/DataCite/re3data API 全打通**；nbsdc/escience 国家科学数据中心体系 18 中心入口全可达 |
| `intl/` | 23 | **世行 API、WHO GHO、UNSDG、OECD/Eurostat/ILO/DBnomics ✅**；QoG 61MB 变量超市直下；Comtrade 全量需 key |
| `business/` | 11 | **巨潮公告检索 JSON 全流程 → PDF**；深交所公告 JSON；海关/北交所 WAF 记明 |
| `health/` | 10 | 疾控月报、**ncmi 1.9 万数据集接口**、WHO GHO、IPUMS/人口司；卫健委瑞数 |
| `corpora/` | 10 | **CCL 匿名检索**、BCC 下载、人民日报标注语料 DOI、CLUE/中文 NLP 仓、CBETA API |
| `methods/` 补卡 | +2 | 微观数据申请路线图；**国际数据 API 速查（8 库最小 curl）** |

第三批还产出：地方志 31 省总表（**浙/粤/鲁/湘可直连检索**）、近代报刊数据库目录（爱如生/瀚堂/繙云…）、**国家标准全文公开系统**与行标/地标 JSON 检索、**档案系统 13 省级馆**（一史馆 `/ess/` 匿名目录）、**JACAR/NDL/台湾/香港** 检索参数、部委统计 20 行总表（15 站可达）、**人物荣誉库**（英烈/院士/道德模范）、教育科研机构名录。

## 第五批：行业/区域/环境/教育心理/城市/地图/农业（2026-10-03）

| 新层 | 卡片数 | 亮点 |
|---|---|---|
| `industry/` | 19 | 17 家协会逐一实测「有没有数据栏目」；**汽车产销 ✅、PMI/物流指数 ✅、央企名录 ✅**；铁路/民航/城轨公报 PDF、住建年鉴 xls |
| `regional/` | 14 | 省级社科院 7 家 + 高校平台（**清华 TCDC 微观数据通道**、复旦 RDR、厦大共享）；省统计年鉴 URL 规律 |
| `env/` | 13 | **空气质量站点级 JSON ✅**（cnemc）、CEADs 碳核算、全球碳预算（Zenodo DOI）、**气象监测指数 txt ✅**、IPE 蔚蓝、resdc 栅格、EM-DAT |
| `stats/` +4 | — | 农村/农业：部委农业数据门户、**批发价 200 指数 JSON ✅**、成本收益汇编入口、固定观察点/CRRS；城市年鉴与市统计局规律 |
| `surveys/` +6 | — | CIEFR-HS、清华 CCSS、**PISA/TIMSS/PIRLS 国际测评直下 ✅**、**心理所数据平台 API ✅**、教育部统计公报、CLHLS |
| `archives/` +1 | — | 历史地图 GIS：**CHGIS（复旦镜像 + TGaz API ✅）**、中研院 GIS、观沧海/地图书 |

**新增消亡/受限**：广东省社科院（本机不可达）、复旦 dvn 已 502（改 rdr）、成都统计 WAF、城轨协会主站 504（OSS 附件可下）、中国纺织工联 ✖。

## 第六批：流动/慈善/文化/海外馆藏/招投标/地方问政（2026-10-03）

| 新层/扩展 | 卡片 | 亮点 |
|---|---|---|
| `civil/`（新） | 8 | **基金会中心网分面 API ✅**（匿名 13 分面/787 值）；腾讯/支付宝公益项目页；慈善中国/志愿平台登记门 |
| `culture/`（新） | 10 | **非遗名录 JSON ✅**（1557 项目+3994 传承人）、**宗教活动场所名录 API ✅**（42,440 处）、语保工程省点统计 ✅、国保单位名单 |
| `stats/` +2 | 24 | **百度迁徙 JSONP ✅（免 key，2019 起）** + 慧眼 64 期报告 PDF 直链；通勤/交通报告；邮政快递统计（服务端渲染可抓） |
| `industry/` +1 | 20 | 快递与物流统计（国家邮政局列表 + 交通运输部 xlsx） |
| `business/` +2 | 13 | **北京公共资源交易 ES 匿名 JSON ✅**、**千里马招标匿名 API ✅（历史 2012 起，37 万条）**；招标语料（CnOpenData/HF） |
| `social/` +1 | 8 | **问政平台**：领导留言板（签名 JSON）、**红网百姓呼声/胶东在线免登录 JSON ✅**、麻辣社区/大河号 |
| `media/` +1 | 16 | 地方融媒：**全国党媒平台 hubpd JSON ✅**、澎湃/闪电检索 API、封面/极目受限 |
| `academic/` +3 | 26 | **胡佛研究所**（两蒋日记馆内）、**哈佛燕京 LibraryCloud/IIIF ✅**、**欧洲：IDP/Gallica/TNA-BnF-SBB API ✅** |

**新增消亡/受限**：旧志愿服务网（2026-07 关停→cvf.org.cn）、腾讯公益检索接口（param invalid）、ctbpsp/政采云（WAF）、封面/极目/红星（WAF/需 token）。

## 第七批：金融财税/人口社保/科学数据/一带一路/高校数据（2026-10-03）

| 新层/扩展 | 卡片 | 亮点 |
|---|---|---|
| `finance/`（新） | 13 | **央行调查统计 xls 直下 ✅**（1999–2026）、**外汇局时间序列 xlsx ✅**、**AMAC/中期协 JSON ✅**、**地方债 JSON API ✅**（governbond:4443，指标树+31 省行）；NFRA/上清所 WAF、大商所/郑商所 412 |
| `surveys/` +2 | 19 | CMDS 流动人口（转 ncmi 接口）、老龄中心五波调查；人社部（IP 镜像绕 JS）、医保局公报、社保基金年报 |
| `repos/` +2 | 17 | **科学数据中心 API 实测**（ngdc `?q=`、nmdc 分页、geodata `scidata`）；GBIF / NASA CMR / WorldClim |
| `intl/` +3 | 26 | **BU CODF 中国海外发展融资 ✅（xlsx/CSV 直链）**、AidData 走 GitHub Releases（本机 AidData 网不可达）、CARI 数据表；商务部 **data.mofcom POST JSON ✅**（月度 ODI 免 key） |
| `academic/` +2 | 28 | **软科排名 JSON API ✅**；高校信息公开 xxgk 抽查（年报/决算/就业质量报告 PDF 直链）；教育经费公告与部决算 |
| `methods/` +1 | 9 | 统计年鉴/公报 **URL 规律与 wget 批量配方**（国家卷 759 资源抽取实测） |

**新增消亡/受限**：AidData 官网（DNS 污染）、CSIS/Lowy（超时）、SAC 停机维护、NFRA 403、中国结算维护中、河南/上海年鉴格式差异。

## 第八批：供应链/环境执法/国企开发区/县级面板/IFI/文化市场/互联网（2026-10-03）

| 层 | 新增 | 亮点 |
|---|---|---|
| `stats/` +2 | 27 | **投入产出表 xls 直链 ✅**（2002–2023，分省规律）；**电商 JSON 接口 ✅**（免 key，商务部电商司） |
| `intl/` +4 | 30 | **世行 Projects API ✅（2.8 万项目，all.xlsx）**、**亚投行项目数据 ✅（483 条）**、IDB CKAN ✅；OKR DSpace/UN DL OAI ✅；WIOD/Eora/EXIOBASE/ADB MRIO 入卡；UNCTAD OData |
| `industry/` +3 | 23 | **双百/科改+考核 A 级名单 ✅**、**开发区名录与考核排名 PDF ✅**（232 经开区/552 国家级）、**CNNIC 历次报告 PDF ✅**、工信部通信月报（jpaas 接口） |
| `env/` +2 | 15 | **中央环保督察公告/反馈 ✅**、部省处罚专栏（省厅部分仅浏览器、湖北 412） |
| `culture/` +2 | 12 | **出版统计公报 PDF ✅**、电资办票房、文旅部数据接口 ✅；CIP 核发接口（AES 前端可解） |
| `regional/` +1 | 15 | 县级官网/统计局入口规律（11 例抽查）+ 公报定位四步法 |
| `stats/county-stats` | — | 县级公报三条发布位、免费/付费分界、县域年鉴知网 ID |

**新增消亡/受限**：ADB/AfDB/IADB 官网 CF 403（IDB 数据门户例外）、Zenodo 本机 403、火炬中心不可达、海关 412、信通院 412、ISBN 中心超时。

## 第九批：港航/人才/药监/国防/港澳台/城投/文旅体育（2026-10-03）

| 层 | 新增 | 亮点 |
|---|---|---|
| `industry/` +4 | 27 | **港口吞吐量 xlsx ✅**、**上海航交所 SCFI/CCFI 指数 ✅**、**OpenSky 航班轨迹（匿名 400 credits/日）✅**；旅游（旅游研究院）、体育（总局产业公告） |
| `gov/` +4 | 21 | **人才名单**：NSFC 杰青/优青清单 + kd.nsfc.cn 密文 API（DES 密钥已解）、长江学者/万人计划入口；**职称公示**：江苏 dataproxy XML、浙江 zcps JSON；**国防白皮书**（国防部检索 API ✅，国新办需浏览器）；双拥/退役军人名单 |
| `health/` +2 | 12 | **NMPA 数据查询平台迁移至 datasearch.nmpa.gov.cn**（60 子库 itemId 表、站内 pajax 签名、UDI 子站可 curl）；**集采中选/医保目录**（上海阳光采购静态站 + 国家医保局 downfile） |
| `regional/` +3 | 18 | **香港**：C&SD API（param LZ-string）+ data.gov.hk CKAN ✅；**澳门**：DSEC REST/SOAP + data.gov.mo JSON ✅；**台湾**：data.gov.tw 前端 API ✅（5.2 万数据集、CSV 全库导出），主计总处被 CF（仅浏览器） |
| `finance/` +2 | 15 | 城投/融资平台（评级公开区：中诚信 JSON、联合资信 PDF；审计署 2013 债务审计全文）；债券市场统计补充（上证债券信息网月报） |

**新增消亡/受限**：app1.nmpa.gov.cn 下线（迁 datasearch）、国新办 521 挑战、台湾主计总处 CF 403、鹏元/新世纪评级不可达、东方金诚 WAF、甘肃财政厅 412。

## 第十批：支付银行/房地产/就业/留学华侨/宗教/营商/保险（2026-10-03）

| 层 | 新增 | 亮点 |
|---|---|---|
| `finance/` +4 | 19 | **央行支付体系季度报告 PDF ✅**、支付清算协会年报；银行业百强/区域金融运行报告（33 省 PDF）/外资银行名单 ✅；**保险信息披露系统（11 类栏目 JSON + PDF 直链）✅**、保险保障基金/精算协会 |
| `industry/` +2 | 29 | **中国土地市场网 JSON API ✅**（出让公告/成交公示，面积+起始价+受让人字段，区划/日期过滤实测）；公积金年报 PDF 规律、房企数据商业门槛 |
| `surveys/` +1 | 20 | 招聘平台报告：**前程无忧 PDF 年链可枚举 ✅**（resource/resign）；智联/BOSS/猎聘受限已记 |
| `intl/` +2 | 32 | **加拿大IRCC CSV ✅ + StatCan WDS API ✅**、US Census 元数据/需 key、UN 移民存量 6MB xlsx、ICE SEVIS PDF；IIE/HESA 仅浏览器 |
| `gov/` +2 | 23 | **发改委搜索 JSON ✅**（营商环境 253 命中）、民企 500 强专题（2010–2026）、B-READY；城市信用监测（官方平台 WAF，地方镜像路径） |
| `culture/` +2 | 14 | 宗教院校名录 **JSON ✅**（94 所）、五大宗教团体官网栏目；宗教学术网期刊/学者库 |

**新增消亡/受限**：IIE/HESA/中银协部分 WAF、城市信用监测平台 412、智联 WAF/BOSS IP 风控、网联 ACL、ABS SDMX DNS 不通。

## 第十一批：北京地方源 + 非结构化文档源（2026-10-03，按"找文件"口径）

| 层 | 新增 | 亮点 |
|---|---|---|
| `gov/beijing-bureaus` | 1 卡（75 行机构表） | **北京市级 52 个委办局子站全部 200** + 群团 14 + 民主党派 8 + 特殊机构；含各站信息公开栏目 |
| `gov/beijing-street-town` | 1 卡 | **16 区街乡镇栏目定位法**（13/16 区有拼音缩写栏目规律；街镇独立域名已全部下线；区属部门以 J 码/拼音命名）；不穷举、给“目录页+URL 形态+单位数” |
| `gov/disclosure-channels` | 1 卡（162 行） | **易漏文件的 10 类政务栏目**：依申请公开（16 区入口全列）、公报、规范性文件、征集、听证、审计报告、事故调查、巡视反馈、规划公示、征收拆迁——约 65 条 URL |
| `env/eia` | 1 卡 | **环评公示**：全国平台 3 个 + 环评云/环评信息网（附件 PDF 直链，含 47MB 报告全本 rar）、北京 gzcx 8 栏目（JSL WAF 已记）、水利/节能/稳评公示 |
| `media/doc-sharing-sites` | 1 卡（27 站矩阵） | **文库分享站存活核查**：book118/金锄头/淘豆可取证，豆丁/道客/夸克/百度需浏览器，**半数已停运**；360 搜索 `site:` 是唯一 curl 可用的引擎通道 |
| `media/forum-docs` | 1 卡（12 论坛） | QZZN/环评爱好者（全本附件）/土木在线/小木屋/学法网等附件区与检索法 |
| `business/bid-docs` | 1 卡 | **全军武器装备采购网匿名 JSON ✅**（1326 公告）、**国铁采购平台 JSON ✅**（204 万条）、中招联合/中国采购与招标网附件规律 |

**新增消亡/受限**：街镇独立官网全下线、deliwenku/dugen/ishare/360doc 等文库停运、QZZN 本机不可达、剑鱼混淆壳、省级环评平台 412。

## 跨层 P0 速览（首批建议；多数已收编，余下作二/三梯队）

| # | 资产 | 归入 | 为什么先收 | 依赖 |
|---|---|---|---|---|
| 1 | **macOS Vision 零依赖 OCR 管线**（swift+PDFKit+Vision，参考 jiawood2006/doc-ocr） | `scripts/`+`tools/` | 扫描版年鉴/报纸/PDF 文本化，**侦察时已在本机跑通**（1.3s：文本层提取+栅格化+中文 OCR），零安装 | swift（已装） |
| 2 | **chinese-law-corpus**（446 部法律逐条 JSON + 278 指导案例 + 445 公报案例，CC0） | `legal/` | 免登录离线法条语料，补上我们案例侧空白 | 纯 JSON |
| 3 | **Kanseki Repository 漢籍**（9355 个 repo 的古籍 TXT，CC BY-SA） | `archives/` | raw 直取全文（实测《周易》可取）；补"可下线正文语料" | `raw.githubusercontent` |
| 4 | **CBDB 中国历代人物传记库 sqlite**（230★，含官员/关系/地址） | `archives/` | **与官员/人物研究直接相关**；官方主数据在 HF（本机不通），GitHub 镜像 86MB 可取 | 无（下载即用） |
| 5 | **china-policy-sites**（部委 65+15、地级市 294、直辖市 80 的政策发布源总表） | `gov/` | 直接扩我们的源库（每行=主页+信息公开+文件库） | 纯 md |
| 6 | **data_location**（民政口径区划 JSON，含 3220 个乡镇街道 JSON，MIT） | `stats/` | 单位宇宙底本（离线）；与 dmfw 接口互为校验 | 纯 JSON |
| 7 | **wechat-download-api**（1146★，公众号后台凭证→任意号全量列表+正文+RSS，AGPL） | `wechat/` | 现有通道的强补充（搜狗=索引子集）；需自有号扫码 | Docker/Python |
| 8 | **scrapling 官方 skill**（85k★，隐形浏览器 + `--solve-cloudflare`） | `tools/`+`scripts/` | 反爬站的升级通道；注意 Py≥3.10（uv 隔离） | pip + uv |

## A. 微信公众号 → `wechat/`

| 名称 | 仓库 | 提供 | 热度/更新 | 依赖·可用性 | 归入 | 优先级 | 状态 |
|---|---|---|---|---|---|---|---|
| wechat-download-api | tmwgsicp/wechat-download-api | 后台凭证→任意号全量(列表+正文+7 格式导出+RSS+内置 MCP) | 1146★ / 2026-07-27 | Docker/Python；**需自有号扫码**（凭证~4天）；AGPL | wechat/ | P0 | 已收编→`references/wechat/wechat-download-api.md` |
| wechat-digest-skill | Jackychen-12/wechat-digest-skill | Skill：appmsg 按号全量+时间过滤，频控/断点/去重，离线 HTML | 81★ / 2026-08-04 | Python(requests)；**需 mp 后台 token**；MIT | wechat/ | P0 | 已收编→`references/wechat/wechat-digest-skill.md` |
| wechatDownload | qiye45/wechatDownload | 公众号批量下载（评论/合集/html/md/pdf/csv）+MCP/Skill | 9633★ / 2026-10-02 | macOS 客户端；无 license | wechat/ | P0(竞品对照) | 已收编→`references/wechat/wechat-downloaders.md` |
| wechat-article-extractor | freestylefly/wechat-article-extractor-skill | URL→元数据+正文 HTML+封面；删除/受限态判定 | 135★/3.8K 装 / 2026-02-19 | Node+cheerio；**无需登录** | wechat/ | P1 | 已收编→`references/wechat/wechat-article-extractor.md` |
| wechat-article-to-markdown | jackwener/wechat-article-to-markdown | 文章→干净 MD；Camoufox 反检测；图片本地化；代码围栏 | 1042★ / 2026-03-22 | uv tool；浏览器较重 | wechat/ | P1 | 已收编→`references/wechat/wechat-downloaders.md` |
| crawl-wechat | gxcsoccer/wechat-article-crawler | crawl4ai 抓 mp 文章（微信 UA、懒加载图、防盗链） | 13★ / 2026-03-23 | pip crawl4ai | wechat/ | P1 | 已收编→`references/wechat/wechat-downloaders.md` |
| sogou-weixin-mcp-server | ptbsare/sogou-weixin-mcp-server | 搜狗微信检索 MCP（uvx） | 9★ / 2026-05-12 | uvx；受搜狗反爬 | wechat/ | P2 | 候选 |
| WechatSogou | Chyroc/WechatSogou | 搜狗微信 Python 库（6.4k★，自认接口被屏蔽） | 6394★ | pip | wechat/ | P2(对照) | 候选 |
| （停更/下架）wechat-spider 系（striver-ing/bowenpay/lqqyt2423）、wuyanwuyan(2018 死)、wx-cli(DMCA 451) | — | 中间人抓包路线 | — | — | 只作历史参考 | P3 | 放弃/参考 |
| wewe-rss | cooderl/wewe-rss | **公众号 RSS**（含历史文章，OPML） | 9657★ / 2026-10-02 | Docker + 微信读书账号 | wechat/ | **P0(增量监控)** | 已收编→`references/wechat/wewe-rss.md` |

## B. 政府/政策 → `gov/`

| 名称 | 仓库 | 提供 | 热度/更新 | 依赖·可用性 | 优先级 |
|---|---|---|---|---|---|
| china-policy-sites | changwu/china-policy-sites | **政策发布源总表**（部委 65+15、地级市 294、直辖市 80；主页+信息公开+文件库） | 52★ / 2026-09-22 | 纯 md；无 license（只读用链接） | P0 |
| china-policy-opening-html 镜像系列 | changwu/{putian,fuzhou,...}-policy-opening-html | 市级政务公开**全量语料镜像**（莆田 5.9 万篇、福州 10.8 万篇，带 index.tsv） | 各 0★ / 2026-09 | 纯文本 | P2 |
| China-Central-Policy-MCP | guangxiangdebizi/China-Central-Policy-MCP | gov.cn 政策检索+正文结构化（4 工具） | 26★ / 2026-09-18 | Node/TS 读源码 | P1 |
| 政策检索 JSON 参考 | steambreadcuiyao/govcn-policy-query | sousuo.www.gov.cn/zcwjk 检索页形态（SKILL.md） | 0★ / 2026-07-17 | 纯提示词 | P2 |
| chuance-policy-mcp | wenyi3370-lgtm/chuance-policy-mcp | 多站政策检索 MCP（gov.cn/数据局/四川/发改委…）+正文解析+法条核验 | 0★ / 2026-08-30 | Python | P1 |
| GovDoc-CN | RuilinXu/GovDoc-CN | 公文多模态数据集 1371 篇/6816 页（PDF+txt+BIO+VOC） | 46★ / 2026-09-23 | 数据在微云 | P1 |
| gov_opendata | LuMitchell/gov_opendata | 全国开放数据平台入口清单（30+，含下线标注） | 10★ / 2024-08 | md 清单 | P1 |
| policy-collector | pangxiaoda/policy-collector | 部委列表页采集配置模板（16+ 部委） | 0★ / 2026-08 | 标准库脚本 | P1 |

## C. 学术文献 → `academic/`

| 名称 | 仓库 | 提供 | 热度/更新 | 依赖 | 优先级 |
|---|---|---|---|---|---|
| paper-lookup | k-dense-ai/scientific-agent-skills | 18 个学术 API 检索总纲（PubMed/arXiv/OpenAlex/Crossref/S2/Unpaywall…） | repo 47356★ / 2026-10-01 | 脚本 stdlib 但 Py≥3.11（本机 3.9→uv） | P0 |
| gs-skills | cookjohn/gs-skills | Google Scholar 搜索/高级检索/被引/导出 Zotero（Chrome DevTools MCP） | 520★ / 2026-03-13 | 零 py 依赖 | P0 |
| paper-search-mcp | openags/paper-search-mcp | 24+ 源统一检索+PDF 下载+正文抽取 | 2731★ / 2026-10-02 | `uv tool install` | P0 |
| PaperCash | Jesseovo/PaperCash | 8 源含**百度学术/CNKI/万方** + GB/T 7714 + docx | 145★ / 2026-04-07 | requests…→uv venv；CNKI 需 Cookie | P1 |
| paper-fetch / semantic-scholar 系 | agents365-ai/365-skills | PDF 获取链（Unpaywall→S2→arXiv→PMC→Sci-Hub）+S2 检索 | 3.3K 装 / 2026-10-02 | python3 | P1 |
| claude-code-zotero-skill | shoei05/claude-code-zotero-skill | 纯 curl 操作 Zotero 本地 API（localhost:23119） | 248 装 / 2026-02-12 | 零额外依赖 | P2 |
| zotero-mcp / jasminum / translators_CN / zotero-chinese/styles | 54yyyu/zotero-mcp(5221★)、l0o0/jasminum(7268★，抓 CNKI)、l0o0/translators_CN(4761★)、zotero-chinese/styles(6326★，GB/T 7714) | Zotero 生态：MCP/中文元数据/中文引文样式 | 均活跃 | 插件/uvx | P2 |
| article-mcp | gqy20/article-mcp | 中文文献检索 MCP + EasyScholar 期刊分级 | 16★ / 2026-07-26 | uvx | P2 |

## D. 法律 → `legal/`

| 名称 | 仓库 | 提供 | 热度/更新 | 依赖 | 优先级 |
|---|---|---|---|---|---|
| chinese-law-corpus | lttxzmj/chinese-law-corpus | **CC0 离线语料**：446 部法律逐条 JSON+278 指导案例+445 公报案例 | 23★ / 2026-10-02 | 纯 JSON | P0 |
| chinese-law-mcp | lttxzmj/chinese-law-mcp | 法条检索 MCP（search_laws/get_article/search_in_law） | 2★ / 2026-09-26 | `npx -y github:` 免 key | P1 |
| legal-cn-mcp-hub | hygiene-12/legal-cn-mcp-hub | flk + **人民法院案例库 rmfyalk 逆向 API**（cpwsAl/*） | 0★ / 2026-05-27 | 需 Cookie `faxin-cpws-al-token` | P1 |
| legal-ai-skills | neu-zha/legal-ai-skills | 29 个法宝相关 skill（我们的 pkulaw-mcp-installer 即其件） | 65★ / 2026-09-17 | 需法宝 Token | P1 |
| yuandian-law-search | cat-xierluo/legal-skills | 元典检索（法规/案例/企业画像，20 endpoint） | 707★ / 2026-10-02 | **需 YD_API_KEY（付费）** | P1(备选) |
| lawtext/laws + law-flk-vol* | lawtext/laws | flk 全量离线镜像（2000+ 法规 markdown，自动更新） | 107★ / 2026-10-01 | 纯文本；无 license | P2 |
| cn-law-hub | ZongziForu/cn-law-hub | 中国法律法规检索 Agent Skill（10 官方源、法条级、现行有效核验） | 79★ / 2026-09-21 | 纯 Skill | P1 |
| 裁判文书网替代 | — | 侦察结论：**无可用免登录替代**；rmfyalk 需 token | — | — | 放弃(记录) |

## E. 统计/数据 → `stats/`

| 名称 | 仓库 | 提供 | 热度/更新 | 依赖 | 优先级 |
|---|---|---|---|---|---|
| mcp-cnbs | icen-ai/mcp-cnbs | MCP：NBS 月/季/年+分省、世行/IMF/OECD/BIS、人口经济农业普查 | 8★ / 2026-09-26 | `npx mcp-cnbs`，无 key | P0 |
| cn-stats | songjian/cnstats | Python/CLI 直查 stats.gov.cn（含 regcode/zbcode 映射） | 157★ / 2026-09-25 | pip(requests/pandas) | P0 |
| data_location | mumuy/data_location | 行政区划 JSON（**含乡镇街道 3220 个**），GB/T 2260 | 3196★ / 2026-10-02 | 纯 JSON/curl | P0 |
| akshare | akfamily/akshare | 财经/宏观数据接口库（含统计局 macro_china_nbs） | 22811★ / 2026-10-02 | pip 重依赖 | P0 |
| National-Data | yiyuezhuo/National-Data | **1978–2016 年鉴指标 CSV 语料**+抓取器 | 204★ / 2026-09-08 | 静态 CSV | P1 |
| openclaw-akshare-skill | succ985/openclaw-akshare-skill | AKShare 用法的 SKILL.md（1.8K 装） | 11★ / 2026-09-08 | 纯文本 | P1 |
| cnstatbook | Nanji-Huaji/cnstatbook | 年鉴 AI 取数（语义找指标+复合指标沙箱） | 1★ / 2026-04-15 | 需 LLM key | P1 |
| GIS 边界 | GaryBikini/ChinaAdminDivisonSHP(1000★)、thedavidweng/china-village-boundaries(CC0, 村级) | 行政边界 SHP（区县级/村级） | 活跃 | 静态文件 | P2 |
| aahl/skills@cn-stats（注册表 1.5K 装） | skills.sh | NBS 新接口 curl+jq 全流程 | 1.5K 装 | 纯 curl | P1 |

## F. 媒体/数字报 → `media/`

| 名称 | 仓库 | 提供 | 热度/更新 | 依赖 | 优先级 |
|---|---|---|---|---|---|
| RSSHub | DIYgod/RSSHub | 通用 RSS 生成（含 `/people/paper` 人民日报、`/thepaper/gov`、头条、新京报、财新、`/gov/beijing/*`） | 46393★ / 2026-10-02 | Node/Docker 或公共实例 curl | **P0** |
| news-aggregator-skill | cclank/news-aggregator-skill | 44+ 源（含微博/华尔街见闻等）聚合+中文简报 | 1290★ / 2026-10-02 | Py(playwright…) | P1 |
| 人民日报爬虫 | caspiankexin/people-daily-crawler-date | 人民网电子版(2021-)+老资料网(1946-2003) | 163★ / 2026-10-02 | requests；**老资料网本机不可达** | P1 |
| 新闻联播文字稿归档 | DuckBurnIncense/xin-wen-lian-bo | 每日 Markdown（2022-09 至今 1464 篇）+Actions | 200★ / 2026-10-01 | **curl raw 直取** | P1 |
| gopup | justinzm/gopup | 百度/微博/搜狗指数、新闻联播文字稿 | 2545★ / 2026-10-02 | pip | P2 |
| redfox-community | redfox-data/redfox-community | 微博/头条/公众号/抖音检索+全网热榜+舆情报告 | 421★ / 2026-10-02 | **付费 REDFOX_API_KEY** | P1(备选) |
| 舆情系统 | stonedtman/stonedt-yuqing(311★)、javabloger/yuqing(628★) | 自部署舆情采集分析 | 活跃 | Java 全栈（重） | P3 |
| 结论 | — | **无通用中文数字报引擎**；epaper 仍以逐站为主（现有 media/epaper/）+RSSHub 补监控 | — | — | 记录 |

## G. 抓取/浏览器 → `tools/` + `scripts/`

| 名称 | 仓库 | 提供 | 热度 | 依赖·本机 | 优先级 |
|---|---|---|---|---|---|
| agent-browser | vercel-labs/agent-browser | CDP 浏览器 CLI；`read <url>` 直取 MD；探测已装 Chrome/Playwright | 43,449★ / 934K 装 | `npm -g`；**本机已缓存 chromium-1208** | ★★★ |
| defuddle | kepano/obsidian-skills@defuddle（kepano/defuddle） | HTML→干净 Markdown（离线） | 9,584★ / 70.8K 装 | npm，依赖极轻 | ★★★ |
| playwright-cli | microsoft/playwright-cli | 官方 Playwright CLI（snapshot/click/fill/eval） | 13,732★ / 172K 装 | npx；复用已缓存 chromium | ★★★ |
| scrapling（官方 skill） | d4vinci/scrapling | 三级抓取（静态/动态/隐形）+`--solve-cloudflare` | 85,151★ | pip；Py≥3.10（uv） | ★★★ |
| crawl4ai skill | brettdavies/crawl4ai-skill | 动态页→MD、批量、结构化抽取 | 48★/1K 装 | 重依赖 | ★★ |
| liarjs | liarjsdev/liarjs-skills | 度量自动化浏览器指纹（不自相矛盾检测） | 73.5K 装 | npm，零依赖 | ★★ |
| html2text | PyPI | HTML→MD，零依赖，py≥3.9 | — | 可直接进本机 3.9 | ★★ |
| firecrawl/tavily | firecrawl/cli、tavily-ai/skills | 云端抓取（需 key） | 102.5K/15.7K 装 | **需 API key** | ★（备选） |

## H. 文档解析/OCR → 建议新增 `tools/parse/`

| 名称 | 仓库 | 提供 | 热度 | 依赖 | 优先级 |
|---|---|---|---|---|---|
| **macOS Vision 管线** | 参考 jiawood2006/doc-ocr | PDF 文本层+扫描件中文 OCR（**侦察时本机 1.3s 跑通**） | — | **零安装**（swift 已装） | **P0** |
| GLM-OCR skill | zai-org/GLM-OCR（skills/glmocr*） | 中文 OCR/表格/公式/手写→MD；OmniDocBench 第 1 | 7483★ / 304 装 | API 需 ZHIPU key；本地版需 Ollama(未装) | P0 |
| MinerU skill | opendatalab/MinerU（skills/mineru） | PDF/扫描件/Office→MD，flash/basic/standard/advanced | 80988★ | pip+模型；云 flash 免 token | P1 |
| appautomaton/document-SKILLs | appautomaton/document-SKILLs | **Anthropic pdf/docx/xlsx 技能的 MIT 重写**，PEP723 `uv run` | 165★ / 2026-09-29 | uv；建议 brew poppler/tesseract | P1 |
| claude-office-skills 解析族 | claude-office-skills/skills | pdfplumber/OCR/camelot/docling 六件套 | 495★ | **强依赖 office-mcp** | P1 |
| anthropics/skills@pdf/docx/xlsx/pptx | anthropics/skills | 官方文档技能（**source-available，非开源**） | 179379★ | 需 poppler/tesseract/qpdf（本机缺） | P1(参考) |
| LT2MD | libnyx/LT2MD | PDF→可审计 Markdown（reading order/公式/页级溯源） | 109★ | — | P2 |

## I. 古籍/方志/本地检索 → `archives/`

| 名称 | 仓库/站 | 提供 | 热度 | 依赖 | 优先级 |
|---|---|---|---|---|---|
| Kanseki Repository | github.com/orgs/kanripo + kanripo.org | 先秦至清汉籍全文 TXT（9355 repo，CC BY-SA） | — | raw 直取（实测可取《周易》） | 高 |
| CBDB sqlite | cbdb-project/cbdb_sqlite | **历代人物/官员/关系/地址库**（SQLite） | 230★ / 数据 2026-09-26 | 主数据 HF（**本机不通**）；GitHub 镜像 86MB | 高 |
| 殆知阁 | garychowcmu/daizhigev20 | 古籍 txt 大合集 | 3442★ | 大下载；无许可 | 中 |
| ctext / 中研院漢籍 / 上海通 | ctext.org / hanchi.ihp.sinica.edu.tw / shtong.gov.cn | 汉籍/二十五史/上海地方志全文站 | — | ctext API 有 turnstile | 中 |
| 本地检索工具 | Sygil-Dev/whoosh-reloaded + fxsjy/jieba | 纯 Python 索引+中文分词（3.9 兼容，脱网） | 237★ / 35172★ | pip；离线 | 高 |
| OCR（备选） | DayBreak-u/chineseocr_lite(12.3k★, 竖排, 4.7M 模型)、RapidAI/RapidOCR | 轻量中文 OCR | 活跃 | pip/onnx；本机 3.9 兼容 | 高 |
| MinerU / docling | 见 H 节 | 扫描年鉴/方志→MD | 80.9k / 68.3k | 重 | 中 |
| ZincSearch | zincsearch/zincsearch | 单二进制，内置简体中文分词 | 17896★ | 单文件 | 中 |
| 已装兜底 | `rg 15.1.0` | 小语料正则检索 | — | **本机已装** | 高 |

## J. 生态与「持续发现」机制 → `meta`

| 名称 | 仓库/入口 | 用途 | 热度 |
|---|---|---|---|
| awesome-china-mcp | zackchewa/awesome-china-mcp | **中国应用 MCP 索引**（微信/知乎/微博/小红书/CNKI/法律/A股/地图） | 15★ / 2026-09-28 |
| awesome-mcp-servers | punkpeye/awesome-mcp-servers | MCP 总目录 | 95756★ |
| anthropics/skills | anthropics/skills | 官方技能库（含 skill-creator、mcp-builder） | 179379★ |
| vercel-labs/skills | vercel-labs/skills | `npx skills` 本体 + find-skills（3.7M 装） | 32972★ |
| superpowers | obra/superpowers | 技能框架/方法论 | 294261★ |
| chubbyskills | chubbyguan/chubbyskills | 14 个中文内容采集 Skill（抖音/B站/小红书/公众号/播客） | 1160★ / 2026-10-02 |
| Agent-Reach | Panniantong/Agent-Reach | 多平台搜索/读取 CLI（含 B站/小红书） | 88110★ |
| cn-scraper-mcp | goesByhc/cn-scraper-mcp | 中文平台搜索 MCP（淘宝/知乎/微博/B站…） | 49★ |
| agent-search-mcp | lennney/agent-search-mcp | 中英双语搜索 MCP，零 key 起步 | 111★ |
| 定期复跑 | `npx -y skills@latest find <英文词>`；`gh search repos '<词>'`；skills.sh/trending；本文件按季度追加 | 发现新 skill | — |

## 检索方法备忘（复现/续跑用）

- **skills.sh 注册表**：`npx -y skills@latest find "<kw>"` —— 只认英文词/技能名；**中文关键词一律失效**；
  返回安装量可用于热度排序；页面 `https://skills.sh/<owner>/<repo>/<skill>` 可 curl。
- **GitHub**：`gh search repos '<kw>'` 最有效（中英文均可）；`gh search repos --topic claude-skills <kw>` 覆盖有限；
  `gh search code 'filename:SKILL.md <kw>'` 中文基本失效；`gh api repos/<r>` 取 star/license/更新。
- **验证正文**：`curl -s https://raw.githubusercontent.com/<owner>/<repo>/HEAD/SKILL.md`（或 /main/、/master/、README.md）；
  文件树：`https://data.jsdelivr.com/v1/packages/gh/<repo>@HEAD`。
- **注意**：兄弟 agent 并发会共享 GitHub search 限流（403），检索要错峰/重试；中文领域在注册表里几乎空白，
  增量主要在 GitHub 仓库层（语料、工具、API 封装）。

## 放弃/降级记录（避免重复侦察）

- 微信公众号「搜狗接口库」类（Chyroc/WechatSogou 等）自认接口已屏蔽 → 只作对照，不主力收编。
- wuyanwuyan/wechat-articles-crawler（2018 停更）、bowenpay/wechat-spider（2021 停更）、wx-cli（DMCA 451）→ 放弃。
- 裁判文书网免登录 API：**不存在**（rmfyalk 需 token；wenshu 登录墙）→ 记录，不再找。
- 通用中文 epaper 引擎：**不存在**（逐站维护 + RSSHub 补监控）。
- r.jina.ai 家族：本机网络层不通 → 放弃（tools/ 已记录）。
- 需付费 key 的云抓取（Firecrawl/Tavily/Brave/REDFOX/元典）→ 备选席，不默认收编。
