# references —— 中文公开资料源库（总索引）

**一个来源一个文件**，按领域分 13 个层；每层有 `README.md`（文件一览 / 选路 / 相关）。
每个来源卡字段固定：`去哪找 · 什么时候用 · 怎么搜/怎么取 · 覆盖 · 门槛 · 实测 · 上游`（写法见 `meta/style.md`）。
新增源 = 新增文件 + 各层 README 加一行 + 本页自动生成（维护方法见仓库根 `SKILL.md` 与 `scripts/probe.py`）。

> 状态标注纪律：✅/⚠️/❌ 均来自本机实测（文件内注明日期）；未探测的写「未验证」，不要猜。

## 分层

| 层 | 目录 | 内容 |
|---|---|---|
| 综合搜索引擎 | [`engines/`](engines/README.md) | 点查与补充召回；通道降级顺序见本层 README |
| 微信生态 | [`wechat/`](wechat/README.md) | 搜狗微信（关键词索引）→ 签名链接 → 正文；wechatspider 按号全量 |
| 政府网站 | [`gov/`](gov/README.md) | 中央/北京市级/16 区门户/人大/信息公开年报 |
| 党建与党史 | [`party/`](party/README.md) | 组工、党建网、共产党员网、党史 |
| 统计与区划 | [`stats/`](stats/README.md) | 统计口径、国家数据、区划名录（单位宇宙的底本） |
| 企业与市场 | [`business/`](business/README.md) | 上市公司/公告、交易所、债券、海关、商业数据库、企业资质、招投标 |
| 金融与财税 | [`finance/`](finance/README.md) | 央行/外汇/金融监管统计、财政预决算、地方债、税收 |
| 健康与人口 | [`health/`](health/README.md) | 疾控/卫健统计、人口健康科学数据、GBD/WHO、人口普查 |
| 调查与微观数据 | [`surveys/`](surveys/README.md) | CFPS/CGSS/CHARLS/CHFS 等大型调查与微观数据申请 |
| 数据仓储 | [`repos/`](repos/README.md) | 通用数据仓储与数据集检索（Dataverse/Zenodo/ICPSR/re3data/国家科学数据中心） |
| 国际组织与国际数据 | [`intl/`](intl/README.md) | 世行/UN/IMF/OECD/Eurostat/跨国调查与政治学指标 |
| 行业与协会 | [`industry/`](industry/README.md) | 国家级行业协会/主管部门侧数据、央企、行业年鉴 |
| 区域与地方数据 | [`regional/`](regional/README.md) | 省级社科院/高校数据平台、地方与区域研究数据、省统计年鉴 |
| 环境·能源·碳 | [`env/`](env/README.md) | 碳核算、生态环境监测、能源统计、资源环境栅格数据 |
| 公益与志愿服务 | [`civil/`](civil/README.md) | 慈善组织、基金会、志愿服务与社会组织（民政口径） |
| 文化·民族·宗教·语言 | [`culture/`](culture/README.md) | 民族宗教、方言与语言资源、非遗、文物与遗产 |
| 媒体与数字报 | [`media/`](media/README.md) | 央媒/市属媒体/地方融媒/转载通道；epaper/ 为数字报平台 |
| 学术文献 | [`academic/`](academic/README.md) | 期刊/论文/年鉴/皮书/图书馆 OPAC；cnki/ 为知网全套手册 |
| 语料与文本数据 | [`corpora/`](corpora/README.md) | 汉语语料库、中文 NLP 数据集、文本数据平台 |
| 法律与法规 | [`legal/`](legal/README.md) | 法律法规数据库、标准、党内法规、裁判文书、法宝 |
| 方志·年鉴·档案 | [`archives/`](archives/README.md) | 地方志、综合年鉴、档案、古籍、民国文献 |
| 社交平台 | [`social/`](social/README.md) | 微博/知乎/贴吧（多为线索源，检索普遍需登录） |
| 通用工具 | [`tools/`](tools/README.md) | 网页存档、阅读代理等跨站工具 |
| 检索方法 | [`methods/`](methods/README.md) | 跨源方法与流程（文献传递、检索语法、历史回捞、人物检索、数据集市、API 速查） |
| 元资源（找源的地方） | [`meta/`](meta/README.md) | MCP/技能目录、发现机制（含中国应用 MCP 索引） |

- 部分层没有独立 README 时，直接读层内文件。
- 跨层常用组合：单位名录 `stats/mca.gov.cn.md`（四级代码，含乡级）→ 政府站检索 `gov/beijing.gov.cn.md` → 微信放量 `wechat/weixin.sogou.com.md`。
- 找「某平台有没有现成接口」：先看 `meta/awesome-china-mcp.md`；找新技能/新源的方法见 `meta/skills-discovery.md`。

## engines —— 综合搜索引擎

- [`engines/baidu.com.md`](engines/baidu.com.md) — baidu.com —— 中文综搜兜底
- [`engines/chinaso.com.md`](engines/chinaso.com.md) — chinaso.com —— 国家权威检索（本机不可用）
- [`engines/cn.bing.com.md`](engines/cn.bing.com.md) — cn.bing.com —— 中文综搜 + RSS 纯文本流
- [`engines/m.sm.cn.md`](engines/m.sm.cn.md) — m.sm.cn —— 神马移动综搜（可翻页）
- [`engines/so.com.md`](engines/so.com.md) — so.com —— 标题级检索 + 日期参数
- [`engines/so.toutiao.com.md`](engines/so.toutiao.com.md) — so.toutiao.com —— 资讯检索（SSR + JSON 接口）
- [`engines/www.sogou.com.md`](engines/www.sogou.com.md) — www.sogou.com —— 网页索引（与微信通道互补）

## wechat —— 微信生态

- [`wechat/mp.weixin.qq.com.md`](wechat/mp.weixin.qq.com.md) — mp.weixin.qq.com —— 单篇文章正文与元数据抓取
- [`wechat/wechat-article-extractor.md`](wechat/wechat-article-extractor.md) — wechat-article-extractor —— 文章状态判定与元数据抽取
- [`wechat/wechat-digest-skill.md`](wechat/wechat-digest-skill.md) — wechat-digest-skill —— 后台凭证按号采集与断点续采
- [`wechat/wechat-download-api.md`](wechat/wechat-download-api.md) — wechat-download-api —— 后台凭证 API 与多格式导出
- [`wechat/wechat-downloaders.md`](wechat/wechat-downloaders.md) — wechat-downloaders —— 已有链接落地为本地文件
- [`wechat/wechatspider.md`](wechat/wechatspider.md) — wechatspider —— 客户端抓包按号全量采集
- [`wechat/weixin.sogou.com.md`](wechat/weixin.sogou.com.md) — weixin.sogou.com —— 公众号文章关键词检索
- [`wechat/wewe-rss.md`](wechat/wewe-rss.md) — wewe-rss —— 公众号订阅转 RSS 服务

## gov —— 政府网站

- [`gov/beijing-bureaus.md`](gov/beijing-bureaus.md) — 北京市级机构站群 —— 委办局·群团·党派名录
- [`gov/beijing-districts.md`](gov/beijing-districts.md) — 北京16区门户站群 —— 区级名录与任免检索
- [`gov/beijing-street-town.md`](gov/beijing-street-town.md) — 北京街乡镇 —— 16区街镇栏目定位
- [`gov/beijing-xxgk.md`](gov/beijing-xxgk.md) — 北京政府信息公开年报 —— 街乡镇正职线索树
- [`gov/beijing.gov.cn.md`](gov/beijing.gov.cn.md) — beijing.gov.cn —— 首都之窗市政府门户
- [`gov/bjchy.gov.cn.md`](gov/bjchy.gov.cn.md) — bjchy.gov.cn —— 朝阳区政府门户
- [`gov/bjdx.gov.cn.md`](gov/bjdx.gov.cn.md) — bjdx.gov.cn —— 大兴区政府门户
- [`gov/business-environment.md`](gov/business-environment.md) — business-environment —— 营商环境评价与民企500强
- [`gov/ccgp-ggzy.md`](gov/ccgp-ggzy.md) — ccgp-ggzy —— 招投标与政府采购公告检索
- [`gov/china-policy-sites.md`](gov/china-policy-sites.md) — china-policy-sites —— 全国政策发布站点总表
- [`gov/chinanpo.md`](gov/chinanpo.md) — chinanpo.mca.gov.cn —— 社会组织登记与年检查询
- [`gov/city-credit.md`](gov/city-credit.md) — city-credit —— 城市信用监测排名与信用政策
- [`gov/credit-china.md`](gov/credit-china.md) — 信用中国 —— 公共信用信息与红黑名单查询
- [`gov/defense-documents.md`](gov/defense-documents.md) — defense-documents —— 国防白皮书与涉军文件
- [`gov/disclosure-channels.md`](gov/disclosure-channels.md) — 政府信息公开渠道 —— 易漏文件的栏目类型总表
- [`gov/edu-research-institutions.md`](gov/edu-research-institutions.md) — edu-research-institutions —— 高校与科研机构名录核实
- [`gov/gov-policy-mcp.md`](gov/gov-policy-mcp.md) — gov-policy-mcp —— 政策检索封装三件套
- [`gov/gov.cn.md`](gov/gov.cn.md) — gov.cn —— 政策文件库与国务院公报检索
- [`gov/gov_opendata.md`](gov/gov_opendata.md) — gov_opendata —— 全国政府开放数据平台清单
- [`gov/gsxt.md`](gov/gsxt.md) — gsxt.gov.cn —— 企业工商登记官方公示库
- [`gov/ip-cnipa.md`](gov/ip-cnipa.md) — cnipa.gov.cn —— 专利与商标检索公告入口
- [`gov/professional-titles.md`](gov/professional-titles.md) — professional-titles —— 职称评审公示与职业资格
- [`gov/renshi-sources.md`](gov/renshi-sources.md) — 人事任免源清单 —— 中央与地方任免公示入口
- [`gov/sydj.md`](gov/sydj.md) — 事业单位登记平台 —— 法人登记与年报公示查询
- [`gov/talent-programs.md`](gov/talent-programs.md) — talent-programs —— 国家级人才计划名单
- [`gov/veterans-affairs.md`](gov/veterans-affairs.md) — veterans-affairs —— 退役军人事务与双拥

## party —— 党建与党史

- [`party/12371.cn.md`](party/12371.cn.md) — 12371.cn —— 共产党员网案例与课件
- [`party/bjdj.gov.cn.md`](party/bjdj.gov.cn.md) — bjdj.gov.cn —— 北京组工网文章
- [`party/cdcghy.com.md`](party/cdcghy.com.md) — cdcghy.com —— 顺义组工镜像站
- [`party/cpc.people.com.cn.md`](party/cpc.people.com.cn.md) — cpc.people.com.cn —— 人民网中国共产党新闻网
- [`party/dangjian.cn.md`](party/dangjian.cn.md) — dangjian.cn —— 党建网文章检索
- [`party/dswxyjy.md`](party/dswxyjy.md) — dswxyjy.org.cn —— 党史文献全文检索

## stats —— 统计与区划

- [`stats/agri-cost-benefit.md`](stats/agri-cost-benefit.md) — 农产品成本收益资料汇编 —— 成本收益数据入口
- [`stats/agri-price.md`](stats/agri-price.md) — 农产品价格 —— 批发市场价与 200 指数接口
- [`stats/agri-stat.md`](stats/agri-stat.md) — 农业农村统计 —— 部委数据门户与粮食储备
- [`stats/akshare.md`](stats/akshare.md) — akshare —— 中国宏观 / 金融数据总库
- [`stats/cei-drc.md`](stats/cei-drc.md) — cei-drc —— 中经网与国研网经济数据检索
- [`stats/china-io-table.md`](stats/china-io-table.md) — china-io-table —— 中国投入产出表
- [`stats/city-data-cn.md`](stats/city-data-cn.md) — city-data-cn —— 城市数据库与市统计局入口
- [`stats/city-stat-yearbook.md`](stats/city-stat-yearbook.md) — city-stat-yearbook —— 城市县域统计年鉴取数入口
- [`stats/cnki-data.md`](stats/cnki-data.md) — data.cnki.net —— 知网统计年鉴数据库
- [`stats/cnstats.md`](stats/cnstats.md) — cnstats —— 国家统计局取数 Python 包与 CLI
- [`stats/commute-city.md`](stats/commute-city.md) — commute-city —— 城市通勤与交通运行
- [`stats/county-stats.md`](stats/county-stats.md) — county-stats —— 县级面板与统计公报取数
- [`stats/data.stats.gov.cn.md`](stats/data.stats.gov.cn.md) — data.stats.gov.cn —— 国家数据指标数值 API
- [`stats/data_location.md`](stats/data_location.md) — data_location —— 省市县与乡镇街道静态 JSON 名录
- [`stats/digital-economy.md`](stats/digital-economy.md) — digital-economy —— 数字经济与电商统计
- [`stats/epsnet.md`](stats/epsnet.md) — epsnet.com.cn —— EPS 宏观与区域数据平台
- [`stats/geodata.md`](stats/geodata.md) — geodata —— 标准地图与地球科学数据
- [`stats/mca.gov.cn.md`](stats/mca.gov.cn.md) — mca.gov.cn —— 民政部行政区划代码
- [`stats/mcp-cnbs.md`](stats/mcp-cnbs.md) — mcp-cnbs —— 国家统计局新版 API 的 MCP 服务
- [`stats/ministry-stats.md`](stats/ministry-stats.md) — ministry-stats —— 中央部委数据与统计栏目总表
- [`stats/mobility.md`](stats/mobility.md) — mobility —— 人口迁徙与城际出行数据
- [`stats/national-data-corpus.md`](stats/national-data-corpus.md) — national-data-corpus —— 年鉴指标 CSV 语料仓
- [`stats/nbs-api-skills.md`](stats/nbs-api-skills.md) — nbs-api-skills —— NBS 新接口的两个 skill 实现
- [`stats/rural-surveys.md`](stats/rural-surveys.md) — 农村调查 —— 固定观察点与农村微观数据
- [`stats/stats.gov.cn.md`](stats/stats.gov.cn.md) — stats.gov.cn —— 统计用区划代码页面
- [`stats/tjj.beijing.gov.cn.md`](stats/tjj.beijing.gov.cn.md) — tjj.beijing.gov.cn —— 北京统计年鉴公报与月季度数据
- [`stats/xzqh.org.md`](stats/xzqh.org.md) — xzqh.org —— 区划地名网乡镇名录

## business —— 企业与市场

- [`business/bid-docs.md`](business/bid-docs.md) — bid-docs —— 招标采购文档与附件源
- [`business/bse.cn.md`](business/bse.cn.md) — bse.cn —— 北交所信息披露与市场数据
- [`business/chinabond.com.cn.md`](business/chinabond.com.cn.md) — chinabond.com.cn —— 债券市场与中债收益率
- [`business/chinamoney.com.cn.md`](business/chinamoney.com.cn.md) — chinamoney.com.cn —— 货币市场利率与汇率数据
- [`business/cninfo.com.cn.md`](business/cninfo.com.cn.md) — cninfo.com.cn —— 上市公司公告与年报全文检索
- [`business/commercial-databases.md`](business/commercial-databases.md) — commercial-databases —— 商科研究商业数据库总卡
- [`business/csrc.gov.cn.md`](business/csrc.gov.cn.md) — csrc.gov.cn —— 证监统计信息与行政处罚
- [`business/customs.gov.cn.md`](business/customs.gov.cn.md) — customs.gov.cn —— 海关进出口统计（月报/快讯）
- [`business/enterprise-certifications.md`](business/enterprise-certifications.md) — enterprise-certifications —— 高企与专精特新名单
- [`business/neeq.com.cn.md`](business/neeq.com.cn.md) — neeq.com.cn —— 新三板挂牌与信息披露
- [`business/procurement.md`](business/procurement.md) — procurement —— 招投标与政采公告批量回溯
- [`business/sse.com.cn.md`](business/sse.com.cn.md) — sse.com.cn —— 上交所信息披露与市场统计
- [`business/szse.cn.md`](business/szse.cn.md) — szse.cn —— 深交所公告与市场统计
- [`business/tender-corpus.md`](business/tender-corpus.md) — tender-corpus —— 现成招标公告数据集与语料

## finance —— 金融与财税

- [`finance/actuarial.md`](finance/actuarial.md) — actuarial —— 精算与保险研究数据入口
- [`finance/amac.org.cn.md`](finance/amac.org.cn.md) — amac.org.cn —— 公募私募资管规模数据
- [`finance/banking-industry.md`](finance/banking-industry.md) — banking-industry —— 银行业行业数据与名录
- [`finance/bond-market-stats.md`](finance/bond-market-stats.md) — bond-market-stats —— 债券市场统计补充入口
- [`finance/cfachina.org.md`](finance/cfachina.org.md) — cfachina.org —— 期货市场成交与公司数据
- [`finance/chinatax.md`](finance/chinatax.md) — chinatax —— 税务统计与年度报告
- [`finance/fiscal-open.md`](finance/fiscal-open.md) — fiscal-open —— 财政预决算公开入口
- [`finance/futures-exchanges.md`](finance/futures-exchanges.md) — futures-exchanges —— 期货交易所行情与持仓
- [`finance/insurance.md`](finance/insurance.md) — insurance —— 保险业统计与公司披露入口
- [`finance/lgfv-platforms.md`](finance/lgfv-platforms.md) — lgfv-platforms —— 城投债与地方政府融资平台数据
- [`finance/localgov-debt.md`](finance/localgov-debt.md) — localgov-debt —— 地方政府债券信息平台
- [`finance/nafmii.org.cn.md`](finance/nafmii.org.cn.md) — nafmii.org.cn —— 债务融资工具市场统计
- [`finance/nfra.gov.cn.md`](finance/nfra.gov.cn.md) — nfra.gov.cn —— 银行业保险业监管统计
- [`finance/payment-clearing.md`](finance/payment-clearing.md) — payment-clearing —— 支付体系统计与行业报告
- [`finance/pbc.gov.cn.md`](finance/pbc.gov.cn.md) — pbc.gov.cn —— 央行调查统计口径数据
- [`finance/sac.net.cn.md`](finance/sac.net.cn.md) — sac.net.cn —— 证券公司行业数据
- [`finance/safe.gov.cn.md`](finance/safe.gov.cn.md) — safe.gov.cn —— 外汇储备与国际收支数据
- [`finance/sge.com.cn.md`](finance/sge.com.cn.md) — sge.com.cn —— 黄金白银现货与延期行情
- [`finance/shclearing.com.cn.md`](finance/shclearing.com.cn.md) — shclearing.com.cn —— 银行间清算统计与披露

## health —— 健康与人口

- [`health/chinacdc.cn.md`](health/chinacdc.cn.md) — chinacdc.cn —— 中国疾控中心疫情月报与健康数据
- [`health/chns.md`](health/chns.md) — chns —— 中国健康与营养调查
- [`health/drug-procurement.md`](health/drug-procurement.md) — drug-procurement —— 药品集采中选与目录
- [`health/healthdata.org.md`](health/healthdata.org.md) — healthdata.org —— IHME / 全球疾病负担 GBD
- [`health/ipums.org.md`](health/ipums.org.md) — ipums.org —— IPUMS 国际微观人口数据
- [`health/ncmi.cn.md`](health/ncmi.cn.md) — ncmi.cn —— 国家人口健康科学数据中心
- [`health/nhc.gov.cn.md`](health/nhc.gov.cn.md) — nhc.gov.cn —— 国家卫健委卫生统计年鉴与公报
- [`health/nmpa.md`](health/nmpa.md) — nmpa.gov.cn —— 药品器械化妆品注册备案库
- [`health/phsciencedata.cn.md`](health/phsciencedata.cn.md) — phsciencedata.cn —— 公共卫生科学数据中心
- [`health/population.un.org.md`](health/population.un.org.md) — population.un.org —— 联合国人口司 WPP 人口预测
- [`health/stats.gov.cn-census.md`](health/stats.gov.cn-census.md) — stats.gov.cn-census —— 国家统计局人口普查数据
- [`health/who-gho.md`](health/who-gho.md) — who-gho —— 世界卫生组织全球卫生指标 API

## surveys —— 调查与微观数据

- [`surveys/ceps.md`](surveys/ceps.md) — CEPS —— 初中队列教育追踪调查
- [`surveys/cfdb.md`](surveys/cfdb.md) — CFDB —— 浙大中国家庭大数据库
- [`surveys/cfps.md`](surveys/cfps.md) — CFPS —— 全国家庭与个人双年追踪面板
- [`surveys/cgss.md`](surveys/cgss.md) — CGSS —— 全国年度综合性社会调查
- [`surveys/charls.md`](surveys/charls.md) — CHARLS —— 中老年人健康与养老追踪
- [`surveys/chfs.md`](surveys/chfs.md) — CHFS —— 家庭金融与资产微观调查
- [`surveys/chip-chns-css.md`](surveys/chip-chns-css.md) — CHIP·CHNS·CSS —— 收入·营养·社会状况三调查
- [`surveys/ciefr-hs.md`](surveys/ciefr-hs.md) — ciefr-hs —— 家庭教育支出的全国固定样本追踪
- [`surveys/clds.md`](surveys/clds.md) — CLDS —— 劳动力/家庭/社区双年追踪
- [`surveys/clhls.md`](surveys/clhls.md) — clhls —— 高龄老人健康长寿追踪调查
- [`surveys/cnsda.org.md`](surveys/cnsda.org.md) — CNSDA —— 社科调查数据的检索与存档
- [`surveys/edu-stat-public.md`](surveys/edu-stat-public.md) — edu-stat-public —— 教育部统计公报与教育统计数据
- [`surveys/employment-data.md`](surveys/employment-data.md) — employment-data —— 招聘平台就业与薪酬报告
- [`surveys/ipums.org.md`](surveys/ipums.org.md) — IPUMS International —— 中国人口普查微数据
- [`surveys/microdata.stats.gov.cn.md`](surveys/microdata.stats.gov.cn.md) — microdata.stats.gov.cn —— 国家统计局微观数据申请
- [`surveys/pisa-timss-pirls.md`](surveys/pisa-timss-pirls.md) — pisa-timss-pirls —— 国际教育测评的中国数据
- [`surveys/population-surveys.md`](surveys/population-surveys.md) — population-surveys —— 人口与流动人口专项调查
- [`surveys/psych-data.md`](surveys/psych-data.md) — psych-data —— 心理学数据、预注册与存缴入口
- [`surveys/social-insurance.md`](surveys/social-insurance.md) — social-insurance —— 人社医保微观与统计
- [`surveys/tsinghua-ccss.md`](surveys/tsinghua-ccss.md) — tsinghua-ccss —— 大学生学情与发展的院校调查

## repos —— 数据仓储

- [`repos/bio-global-apis.md`](repos/bio-global-apis.md) — bio-global-apis —— 国际生物与地学数据接口
- [`repos/csdata.org.md`](repos/csdata.org.md) — csdata.org —— 数据论文与配套数据集期刊
- [`repos/datacite.org.md`](repos/datacite.org.md) — datacite.org —— 全球数据集 DOI 总检索
- [`repos/datadryad.org.md`](repos/datadryad.org.md) — datadryad.org —— 论文配套数据的 DOI 仓储
- [`repos/dataverse.harvard.edu.md`](repos/dataverse.harvard.edu.md) — dataverse.harvard.edu —— 社科数据集与 DOI 检索
- [`repos/escience.org.cn.md`](repos/escience.org.cn.md) — escience.org.cn —— 科技资源与数据中心总入口
- [`repos/figshare.com.md`](repos/figshare.com.md) — figshare.com —— 全学科成果与附件仓储
- [`repos/gesis.org.md`](repos/gesis.org.md) — gesis.org —— 德国社科数据与变量检索
- [`repos/hf-mirror.com.md`](repos/hf-mirror.com.md) — hf-mirror.com —— HF Hub 数据集镜像检索
- [`repos/icpsr.umich.edu.md`](repos/icpsr.umich.edu.md) — icpsr.umich.edu —— 社科数据档案与变量级检索
- [`repos/kaggle.com.md`](repos/kaggle.com.md) — kaggle.com —— 竞赛与社区数据集市场
- [`repos/national-data-centers.md`](repos/national-data-centers.md) — national-data-centers —— 国家科学数据中心 20 家入口
- [`repos/nbsdc.cn.md`](repos/nbsdc.cn.md) — nbsdc.cn —— 基础学科数据与 CSTR 检索
- [`repos/osf.io.md`](repos/osf.io.md) — osf.io —— 研究项目与预注册检索
- [`repos/re3data.org.md`](repos/re3data.org.md) — re3data.org —— 数据仓储目录与资质核对
- [`repos/science-data-apis.md`](repos/science-data-apis.md) — science-data-apis —— 七大科学数据中心检索接口
- [`repos/zenodo.org.md`](repos/zenodo.org.md) — zenodo.org —— 全学科开放仓储与 DOI 记录

## intl —— 国际组织与国际数据

- [`intl/afrobarometer.org.md`](intl/afrobarometer.org.md) — afrobarometer.org —— 非洲晴雨表调查
- [`intl/asianbarometer.org.md`](intl/asianbarometer.org.md) — asianbarometer.org —— 亚洲晴雨表调查
- [`intl/bri-data.md`](intl/bri-data.md) — bri-data —— 一带一路数据与项目库
- [`intl/china-overseas-finance.md`](intl/china-overseas-finance.md) — china-overseas-finance —— 中国海外发展融资项目库
- [`intl/china-students-abroad.md`](intl/china-students-abroad.md) — china-students-abroad —— 中国学生出国留学统计
- [`intl/china-trade-investment-stats.md`](intl/china-trade-investment-stats.md) — china-trade-investment-stats —— 对外经贸官方统计
- [`intl/chinese-diaspora.md`](intl/chinese-diaspora.md) — chinese-diaspora —— 华侨华人与国际移民统计
- [`intl/comtrade.un.org.md`](intl/comtrade.un.org.md) — comtrade.un.org —— 联合国商品贸易统计
- [`intl/cses.org.md`](intl/cses.org.md) — cses.org —— 选举制度比较研究
- [`intl/data.un.org.md`](intl/data.un.org.md) — data.un.org —— 联合国数据门户
- [`intl/dbnomics.world.md`](intl/dbnomics.world.md) — dbnomics.world —— 多机构统计聚合 API
- [`intl/europeansocialsurvey.org.md`](intl/europeansocialsurvey.org.md) — europeansocialsurvey.org —— 欧洲社会调查
- [`intl/eurostat.md`](intl/eurostat.md) — eurostat —— 欧盟统计局
- [`intl/fao.org.md`](intl/fao.org.md) — fao.org —— 联合国粮农组织统计
- [`intl/freedomhouse.org.md`](intl/freedomhouse.org.md) — freedomhouse.org —— 自由之家自由度评级
- [`intl/ifis-projects.md`](intl/ifis-projects.md) — ifis-projects —— 多边开发银行项目库检索
- [`intl/ilostat.ilo.org.md`](intl/ilostat.ilo.org.md) — ilostat.ilo.org —— 国际劳工组织劳动统计
- [`intl/imf.org.md`](intl/imf.org.md) — imf.org —— 国际货币基金组织数据
- [`intl/io-report-libraries.md`](intl/io-report-libraries.md) — io-report-libraries —— 国际组织报告全文库
- [`intl/issp.org.md`](intl/issp.org.md) — issp.org —— 国际社会调查项目
- [`intl/oecd.org.md`](intl/oecd.org.md) — oecd.org —— 经合组织统计 SDMX API
- [`intl/ourworldindata.org.md`](intl/ourworldindata.org.md) — ourworldindata.org —— 全球发展数据整编与图表
- [`intl/qogdata.pol.gu.se.md`](intl/qogdata.pol.gu.se.md) — qogdata.pol.gu.se —— QoG 政府质量标准数据集
- [`intl/systemicpeace.org.md`](intl/systemicpeace.org.md) — systemicpeace.org —— Polity5 政体数据
- [`intl/uis.unesco.org.md`](intl/uis.unesco.org.md) — uis.unesco.org —— 教科文组织统计研究所
- [`intl/unctad-wto-trade.md`](intl/unctad-wto-trade.md) — unctad-wto-trade —— 贸易统计与价值链数据
- [`intl/unstats.un.org.md`](intl/unstats.un.org.md) — unstats.un.org —— 联合国 SDG 指标库 API
- [`intl/v-dem.net.md`](intl/v-dem.net.md) — v-dem.net —— V-Dem 民主多样性数据库
- [`intl/who.int.md`](intl/who.int.md) — who.int —— 世卫组织数据总入口
- [`intl/wiood-eora.md`](intl/wiood-eora.md) — wiood-eora —— 全球投入产出与价值链数据
- [`intl/worldbank.org.md`](intl/worldbank.org.md) — worldbank.org —— 世界银行开放数据 API
- [`intl/worldvaluessurvey.org.md`](intl/worldvaluessurvey.org.md) — worldvaluessurvey.org —— 世界价值观调查

## industry —— 行业与协会

- [`industry/aviation-rail-ops.md`](industry/aviation-rail-ops.md) — aviation-rail-ops —— 航班轨迹与铁路运行细项
- [`industry/caam.org.cn.md`](industry/caam.org.cn.md) — caam.org.cn —— 汽车工业产销月度数据
- [`industry/cgcc.org.cn.md`](industry/cgcc.org.cn.md) — cgcc.org.cn —— 零售业景气指数与消费市场
- [`industry/chinaisa.org.cn.md`](industry/chinaisa.org.cn.md) — chinaisa.org.cn —— 钢铁协会统计发布入口
- [`industry/chinawuliu.com.cn.md`](industry/chinawuliu.com.cn.md) — chinawuliu.com.cn —— 物流与 PMI 月度指数
- [`industry/cia.org.cn.md`](industry/cia.org.cn.md) — cia.org.cn —— 中国信息年鉴在线指标
- [`industry/cinic.org.cn.md`](industry/cinic.org.cn.md) — cinic.org.cn —— 产业经济统计数据汇编
- [`industry/citif.org.cn.md`](industry/citif.org.cn.md) — citif.org.cn —— 电子信息行业联合会入口
- [`industry/clic.org.cn.md`](industry/clic.org.cn.md) — clic.org.cn —— 物流与 PMI 指数源站
- [`industry/clii.com.cn.md`](industry/clii.com.cn.md) — clii.com.cn —— 轻工业运行与月度报告
- [`industry/cntac.org.cn.md`](industry/cntac.org.cn.md) — cntac.org.cn —— 纺织行业数据分析栏目
- [`industry/construction-realestate.md`](industry/construction-realestate.md) — construction-realestate —— 住建部建设统计年鉴与公报
- [`industry/cpema.org.md`](industry/cpema.org.md) — cpema.org —— 医药企业管理协会动态
- [`industry/csteelnews.com.md`](industry/csteelnews.com.md) — csteelnews.com —— 钢铁行业指数与行情
- [`industry/development-zones.md`](industry/development-zones.md) — development-zones —— 开发区名录与考核排名
- [`industry/express-logistics.md`](industry/express-logistics.md) — express-logistics —— 快递与物流统计
- [`industry/fangchan.com.md`](industry/fangchan.com.md) — fangchan.com —— 房地产企业与市场数据
- [`industry/industry-yearbooks.md`](industry/industry-yearbooks.md) — industry-yearbooks —— 行业年鉴在线入口分级
- [`industry/land-market.md`](industry/land-market.md) — land-market —— 土地出让公告与成交公示
- [`industry/mei.net.cn.md`](industry/mei.net.cn.md) — mei.net.cn —— 机械工业运行信息网
- [`industry/ports-shipping.md`](industry/ports-shipping.md) — ports-shipping —— 港口与水运运价指数统计
- [`industry/rail-aviation.md`](industry/rail-aviation.md) — rail-aviation —— 铁路民航与城轨统计
- [`industry/realestate.md`](industry/realestate.md) — realestate —— 房地产指标与住房数据
- [`industry/sasac.gov.cn.md`](industry/sasac.gov.cn.md) — sasac.gov.cn —— 央企名录与国资经营数据
- [`industry/soe.md`](industry/soe.md) — soe —— 国企专项名单与国资运行数据
- [`industry/sports.md`](industry/sports.md) — sports —— 体育产业与场地统计
- [`industry/telecom-internet.md`](industry/telecom-internet.md) — telecom-internet —— 通信业与互联网官方统计
- [`industry/tourism.md`](industry/tourism.md) — tourism —— 旅游统计与研究院口径
- [`industry/yytj.org.cn.md`](industry/yytj.org.cn.md) — yytj.org.cn —— 医药工业统计数据与年报

## regional —— 区域与地方数据

- [`regional/county-portals.md`](regional/county-portals.md) — county-portals —— 县级政府网与统计局入口
- [`regional/econpub.xmu.edu.cn.md`](regional/econpub.xmu.edu.cn.md) — econpub.xmu.edu.cn —— 厦大经济学科研究共享平台
- [`regional/gdass.org.md`](regional/gdass.org.md) — gdass.org —— 广东省社会科学院（本机不可达）
- [`regional/hk-statistics.md`](regional/hk-statistics.md) — hk-statistics —— 香港统计处与资料一线通
- [`regional/jsass.org.cn.md`](regional/jsass.org.cn.md) — jsass.org.cn —— 江苏省社会科学院与院内数据库导航
- [`regional/local-research-platforms.md`](regional/local-research-platforms.md) — local-research-platforms —— 地方社科研究平台总表
- [`regional/mo-statistics.md`](regional/mo-statistics.md) — mo-statistics —— 澳门统计暨普查局与数据平台
- [`regional/provincial-yearbooks.md`](regional/provincial-yearbooks.md) — provincial-yearbooks —— 各省统计年鉴在线入口与规律
- [`regional/rdr.fudan.edu.cn.md`](regional/rdr.fudan.edu.cn.md) — rdr.fudan.edu.cn —— 复旦大学社会科学数据平台
- [`regional/regional-data-cn.md`](regional/regional-data-cn.md) — regional-data-cn —— 长三角/粤港澳区域数据入口
- [`regional/sass.cn.md`](regional/sass.cn.md) — sass.cn —— 四川省社会科学院
- [`regional/sass.org.cn.md`](regional/sass.org.cn.md) — sass.org.cn —— 上海社会科学院研究资源入口
- [`regional/sdass.net.cn.md`](regional/sdass.net.cn.md) — sdass.net.cn —— 山东社会科学院
- [`regional/sdssdc.com.md`](regional/sdssdc.com.md) — sdssdc.com —— 山东社会科学数智服务平台
- [`regional/sky.zj.gov.cn.md`](regional/sky.zj.gov.cn.md) — sky.zj.gov.cn —— 浙江省社会科学院
- [`regional/tcdc.sem.tsinghua.edu.cn.md`](regional/tcdc.sem.tsinghua.edu.cn.md) — tcdc.sem.tsinghua.edu.cn —— 清华经济社会数据研究中心
- [`regional/tw-statistics.md`](regional/tw-statistics.md) — tw-statistics —— 台湾主计总处与政府资料开放平台
- [`regional/university-ss-data.md`](regional/university-ss-data.md) — university-ss-data —— 高校社科数据平台总表

## env —— 环境·能源·碳

- [`env/ceads.net.md`](env/ceads.net.md) — ceads.net —— 中国多尺度碳排放清单
- [`env/cnemc.cn.md`](env/cnemc.cn.md) — cnemc.cn —— 空气质量实时与历史
- [`env/data.cma.cn.md`](env/data.cma.cn.md) — data.cma.cn —— 气象观测数据检索
- [`env/eia.gov.md`](env/eia.gov.md) — eia.gov —— 美国与国际能源 API
- [`env/eia.md`](env/eia.md) — eia —— 建设项目环评公示与全本 PDF
- [`env/emdat.be.md`](env/emdat.be.md) — emdat.be —— 国际灾害事件数据库
- [`env/enforcement.md`](env/enforcement.md) — 环境行政处罚与执法公示 —— 部省两级入口与检索
- [`env/globalcarbonproject.org.md`](env/globalcarbonproject.org.md) — globalcarbonproject.org —— 全球碳预算数据集
- [`env/iea.org.md`](env/iea.org.md) — iea.org —— 国际能源统计与平衡表
- [`env/inspection.md`](env/inspection.md) — 中央生态环境保护督察 —— 公告、典型案例与反馈意见
- [`env/ipe.org.cn.md`](env/ipe.org.cn.md) — ipe.org.cn —— 企业环境监管记录
- [`env/mee.gov.cn.md`](env/mee.gov.cn.md) — mee.gov.cn —— 生态环境统计与公报
- [`env/ncc-cma.net.md`](env/ncc-cma.net.md) — ncc-cma.net —— 气候监测指数与公报
- [`env/nea.gov.cn.md`](env/nea.gov.cn.md) — nea.gov.cn —— 能源月度数据与统计
- [`env/permit.mee.gov.cn.md`](env/permit.mee.gov.cn.md) — permit.mee.gov.cn —— 排污许可证信息公开
- [`env/resdc.cn.md`](env/resdc.cn.md) — resdc.cn —— 资源环境栅格数据

## civil —— 公益与志愿服务

- [`civil/cfforum.org.cn.md`](civil/cfforum.org.cn.md) — cfforum.org.cn —— 基金会论坛与《基金会蓝皮书》
- [`civil/charityalliance.org.cn.md`](civil/charityalliance.org.cn.md) — charityalliance.org.cn —— 中慈联官网与慈善行业资讯
- [`civil/cszg.mca.gov.cn.md`](civil/cszg.mca.gov.cn.md) — cszg.mca.gov.cn —— 慈善组织信息公开与年报平台
- [`civil/cvf.org.cn.md`](civil/cvf.org.cn.md) — cvf.org.cn —— 志愿服务协同平台与志愿者数据
- [`civil/foundationcenter.org.cn.md`](civil/foundationcenter.org.cn.md) — foundationcenter.org.cn —— 基金会数据库与透明指数接口
- [`civil/gongyi.qq.com.md`](civil/gongyi.qq.com.md) — gongyi.qq.com —— 腾讯公益乐捐项目库
- [`civil/gongyishibao.com.md`](civil/gongyishibao.com.md) — gongyishibao.com —— 公益时报网与数字报
- [`civil/love.alipay.com.md`](civil/love.alipay.com.md) — love.alipay.com —— 支付宝公益平台项目页

## culture —— 文化·民族·宗教·语言

- [`culture/chinabuddhism.com.cn.md`](culture/chinabuddhism.com.cn.md) — chinabuddhism.com.cn —— 佛教协会资讯与发布
- [`culture/ihchina.cn.md`](culture/ihchina.cn.md) — ihchina.cn —— 非遗名录与传承人检索
- [`culture/market-stats.md`](culture/market-stats.md) — market-stats —— 文化市场统计公报与票房入口
- [`culture/mzb.com.cn.md`](culture/mzb.com.cn.md) — mzb.com.cn —— 民族宗教资讯检索
- [`culture/ncha.gov.cn.md`](culture/ncha.gov.cn.md) — ncha.gov.cn —— 国保单位与博物馆年报
- [`culture/neac.gov.cn.md`](culture/neac.gov.cn.md) — neac.gov.cn —— 民族统计·政策与名录
- [`culture/publishing-isbn.md`](culture/publishing-isbn.md) — publishing-isbn —— 图书书目核发与零售榜单入口
- [`culture/religion-publications.md`](culture/religion-publications.md) — religion-publications —— 宗教期刊目录与学术检索
- [`culture/religious-bodies.md`](culture/religious-bodies.md) — religious-bodies —— 五大宗教团体官网与院校名录
- [`culture/sara.gov.cn.md`](culture/sara.gov.cn.md) — sara.gov.cn —— 宗教活动场所名录接口
- [`culture/taoist.org.cn.md`](culture/taoist.org.cn.md) — taoist.org.cn —— 道教协会官网栏目
- [`culture/whc.unesco.org.md`](culture/whc.unesco.org.md) — whc.unesco.org —— 世界遗产名录与中国项目
- [`culture/zhongguoyuyan.cn.md`](culture/zhongguoyuyan.cn.md) — zhongguoyuyan.cn —— 方言与民族语言采录数据
- [`culture/zytzb.gov.cn.md`](culture/zytzb.gov.cn.md) — zytzb.gov.cn —— 统战部宗教工作与政策

## media —— 媒体与数字报

- [`media/beijing.qianlong.com.md`](media/beijing.qianlong.com.md) — beijing.qianlong.com —— 千龙网市级/区级稿
- [`media/bj.wenming.cn.md`](media/bj.wenming.cn.md) — bj.wenming.cn —— 中国文明网北京站转载
- [`media/bjnews.com.cn.md`](media/bjnews.com.cn.md) — bjnews.com.cn —— 新京报搜索 API
- [`media/doc-sharing-sites.md`](media/doc-sharing-sites.md) — doc-sharing-sites —— 文库分享站取材通道
- [`media/epaper/xepaper.com.md`](media/epaper/xepaper.com.md) — xepaper.com —— 密云报等数字报
- [`media/epaper/yqb.bjyq.gov.cn.md`](media/epaper/yqb.bjyq.gov.cn.md) — yqb.bjyq.gov.cn —— 延庆报 PDF 数字报
- [`media/forum-docs.md`](media/forum-docs.md) — forum-docs —— 公文·真题·报告·图纸集散地
- [`media/gopup.md`](media/gopup.md) — gopup —— 指数/热榜/新闻联播接口库
- [`media/local-media.md`](media/local-media.md) — 地方融媒体与区县新闻 —— 党媒平台·澎湃·闪电·封面
- [`media/news-aggregator-skill.md`](media/news-aggregator-skill.md) — news-aggregator-skill —— 44+ 源新闻聚合
- [`media/news.china.com.md`](media/news.china.com.md) — news.china.com —— 中华网转载通道
- [`media/people-daily-crawler.md`](media/people-daily-crawler.md) — people-daily-crawler —— 人民日报电子版/老资料网取数
- [`media/people.com.cn.md`](media/people.com.cn.md) — people.com.cn —— 人民网站内检索 API
- [`media/redfox-community.md`](media/redfox-community.md) — redfox-community —— 红狐数据社媒检索 API
- [`media/rmzxw.com.cn.md`](media/rmzxw.com.cn.md) — rmzxw.com.cn —— 人民政协网转载
- [`media/rsshub.md`](media/rsshub.md) — RSSHub —— 中文媒体/政务站 RSS 通道
- [`media/sohu.com.md`](media/sohu.com.md) — sohu.com —— 搜狐转载通道
- [`media/wenku-mirrors.md`](media/wenku-mirrors.md) — wenku-mirrors —— 文库类转载站取全文
- [`media/xinhuanet.com.md`](media/xinhuanet.com.md) — xinhuanet.com —— 新华网文章直读/检索
- [`media/xinwenlianbo-archive.md`](media/xinwenlianbo-archive.md) — xinwenlianbo-archive —— 《新闻联播》每日文字稿归档

## academic —— 学术文献

- [`academic/article-mcp.md`](academic/article-mcp.md) — article-mcp —— 期刊分级与影响因子核验
- [`academic/chaoxing.com.md`](academic/chaoxing.com.md) — chaoxing.com —— 超星发现与期刊检索
- [`academic/cnki.net.md`](academic/cnki.net.md) — cnki.net —— 知网论文·政报·年鉴主入口
- [`academic/cnki/cnki-advanced-search.md`](academic/cnki/cnki-advanced-search.md) — cnki-高级检索 —— 知网高级检索流程
- [`academic/cnki/cnki-download.md`](academic/cnki/cnki-download.md) — cnki-文献下载 —— 下载/导出流程
- [`academic/cnki/cnki-export.md`](academic/cnki/cnki-export.md) — cnki-导出 —— Zotero 入库与引文导出
- [`academic/cnki/cnki-journal-index.md`](academic/cnki/cnki-journal-index.md) — cnki-收录查询 —— 期刊收录与影响因子
- [`academic/cnki/cnki-journal-search.md`](academic/cnki/cnki-journal-search.md) — cnki-期刊检索 —— 按刊名/ISSN/CN 找刊
- [`academic/cnki/cnki-journal-toc.md`](academic/cnki/cnki-journal-toc.md) — cnki-期刊目录 —— 目录浏览与原版下载
- [`academic/cnki/cnki-navigate-pages.md`](academic/cnki/cnki-navigate-pages.md) — cnki-翻页排序 —— 结果翻页与排序
- [`academic/cnki/cnki-paper-detail.md`](academic/cnki/cnki-paper-detail.md) — cnki-论文详情 —— 论文元数据提取
- [`academic/cnki/cnki-parse-results.md`](academic/cnki/cnki-parse-results.md) — cnki-结果解析 —— 结果页结构化提取
- [`academic/cnki/cnki-researcher.md`](academic/cnki/cnki-researcher.md) — cnki-编排 —— 检索到导出的编排流程
- [`academic/cnki/cnki-search.md`](academic/cnki/cnki-search.md) — cnki-基础检索 —— 关键词文献检索
- [`academic/cqvip.com.md`](academic/cqvip.com.md) — cqvip.com —— 中文期刊论文检索
- [`academic/duxiu.com.md`](academic/duxiu.com.md) — duxiu.com —— 读秀图书与章节检索
- [`academic/econ-papers.md`](academic/econ-papers.md) — econ-papers —— 经济学工作论文四源
- [`academic/edu-finance.md`](academic/edu-finance.md) — edu-finance —— 教育经费与部门预决算
- [`academic/european-china-collections.md`](academic/european-china-collections.md) — european-china-collections —— 欧洲敦煌与汉籍馆藏
- [`academic/gs-skills.md`](academic/gs-skills.md) — gs-skills —— Google Scholar 浏览器抓取 6 技能
- [`academic/harvard-yenching.md`](academic/harvard-yenching.md) — harvard-yenching —— 哈佛燕京汉籍与中文善本检索
- [`academic/hk-libraries.md`](academic/hk-libraries.md) — hk-libraries —— 香港公共图书馆数码馆藏与政府档案
- [`academic/hoover-institution.md`](academic/hoover-institution.md) — hoover-institution —— 民国档案与两蒋日记馆藏
- [`academic/institutional-repos.md`](academic/institutional-repos.md) — institutional-repos —— 机构知识库与学位论文定位
- [`academic/jacar.md`](academic/jacar.md) — jacar —— 日本近代亚洲关系档案检索与图像
- [`academic/navi.cnki.net.md`](academic/navi.cnki.net.md) — navi.cnki.net —— 知网年鉴卷详情页
- [`academic/ncpssd.org.md`](academic/ncpssd.org.md) — ncpssd.org —— 中文社科期刊检索与摘要
- [`academic/ndl-japan.md`](academic/ndl-japan.md) — ndl-japan —— 日本国立国会图书馆检索与数字馆藏
- [`academic/nstl.gov.cn.md`](academic/nstl.gov.cn.md) — nstl.gov.cn —— 外文科技文献检索与原文传递
- [`academic/opac.bac.gov.cn.md`](academic/opac.bac.gov.cn.md) — opac.bac.gov.cn —— 北京市委党校图书馆 OPAC
- [`academic/paper-lookup.md`](academic/paper-lookup.md) — paper-lookup —— 18 个学术 API 检索路由
- [`academic/paper-search-mcp.md`](academic/paper-search-mcp.md) — paper-search-mcp —— 28 源统一检索与 PDF 下载链
- [`academic/papercash.md`](academic/papercash.md) — papercash —— 百度学术/知网/万方接入要点
- [`academic/pishu.com.cn.md`](academic/pishu.com.cn.md) — pishu.com.cn —— 皮书系列全文数据库
- [`academic/preprints-cn.md`](academic/preprints-cn.md) — preprints-cn —— 中文预印本与国家科技报告
- [`academic/taiwan-libraries.md`](academic/taiwan-libraries.md) — taiwan-libraries —— 台湾学位论文、华艺与国图数字资源
- [`academic/universities-open-data.md`](academic/universities-open-data.md) — universities-open-data —— 高校信息公开与排名
- [`academic/wanfangdata.com.cn.md`](academic/wanfangdata.com.cn.md) — wanfangdata.com.cn —— 万方期刊/学位/会议论文
- [`academic/zotero-cn.md`](academic/zotero-cn.md) — zotero-cn —— 中文元数据与 GB/T 7714 引文

## corpora —— 语料与文本数据

- [`corpora/ChineseDiachronicCorpus.md`](corpora/ChineseDiachronicCorpus.md) — ChineseDiachronicCorpus —— 中文历时语料库
- [`corpora/bcc.blcu.edu.cn.md`](corpora/bcc.blcu.edu.cn.md) — bcc.blcu.edu.cn —— 北语 BCC 多领域语料库
- [`corpora/cbeta.md`](corpora/cbeta.md) — cbeta —— 中华电子佛典（汉文大藏经语料）
- [`corpora/ccl.pku.edu.cn.md`](corpora/ccl.pku.edu.cn.md) — ccl.pku.edu.cn —— 北大 CCL 语料库检索
- [`corpora/chinese-nlp-corpora.md`](corpora/chinese-nlp-corpora.md) — chinese-nlp-corpora —— 中文 NLP 语料聚合仓
- [`corpora/cluebenchmarks.md`](corpora/cluebenchmarks.md) — cluebenchmarks —— 中文 NLP 评测集与预训练语料
- [`corpora/hf-chinese-datasets.md`](corpora/hf-chinese-datasets.md) — hf-chinese-datasets —— HF 镜像的中文数据集
- [`corpora/nclds.xmu.edu.cn.md`](corpora/nclds.xmu.edu.cn.md) — nclds.xmu.edu.cn —— 教育教材语言资源中心语料库
- [`corpora/rmrb-corpus.md`](corpora/rmrb-corpus.md) — rmrb-corpus —— 人民日报标注语料库（公开版本）
- [`corpora/yuliao.people.cn.md`](corpora/yuliao.people.cn.md) — yuliao.people.cn —— 人民网语料社区

## legal —— 法律与法规

- [`legal/chinese-law-corpus.md`](legal/chinese-law-corpus.md) — chinese-law-corpus —— 法条案例逐条离线语料
- [`legal/cn-law-hub.md`](legal/cn-law-hub.md) — cn-law-hub —— 十官方源法律法规检索
- [`legal/court-open.md`](legal/court-open.md) — court-open —— 法院公开三站
- [`legal/flk.npc.gov.cn.md`](legal/flk.npc.gov.cn.md) — flk.npc.gov.cn —— 国家法律法规数据库
- [`legal/lawtext-laws.md`](legal/lawtext-laws.md) — lawtext-laws —— flk 全量离线镜像
- [`legal/legal-cn-mcp-hub.md`](legal/legal-cn-mcp-hub.md) — legal-cn-mcp-hub —— 中国法律 MCP 连接器中心
- [`legal/npc-gov-regulations.md`](legal/npc-gov-regulations.md) — npc-gov-regulations —— 法规与党内法规聚合索引
- [`legal/pkulaw.com.md`](legal/pkulaw.com.md) — pkulaw.com —— 北大法宝
- [`legal/standards-cn.md`](legal/standards-cn.md) — standards-cn —— 国标/行标/地标检索与全文
- [`legal/wenshu.court.gov.cn.md`](legal/wenshu.court.gov.cn.md) — wenshu.court.gov.cn —— 中国裁判文书网
- [`legal/yuandian-law-search.md`](legal/yuandian-law-search.md) — yuandian-law-search —— 元典智库付费法律检索

## archives —— 方志·年鉴·档案

- [`archives/archives-cn.md`](archives/archives-cn.md) — archives-cn —— 国家与省级档案馆门户与查档入口
- [`archives/bjdsdfz.cn.md`](archives/bjdsdfz.cn.md) — bjdsdfz.cn —— 京网 北京地方志
- [`archives/bjsfzg.bjdsdfz.cn.md`](archives/bjsfzg.bjdsdfz.cn.md) — bjsfzg.bjdsdfz.cn —— 北京市数字方志馆
- [`archives/cbdb.md`](archives/cbdb.md) — CBDB —— 中国历代人物传记资料库
- [`archives/cnbksy.md`](archives/cnbksy.md) — cnbksy.com —— 全国报刊索引
- [`archives/ctext.md`](archives/ctext.md) — ctext.org —— 中国哲学书电子化计划
- [`archives/dachengdata.md`](archives/dachengdata.md) — dachengdata.com —— 大成故纸堆
- [`archives/daizhige.md`](archives/daizhige.md) — daizhige —— 殆知阁古籍 txt 全库
- [`archives/difangzhi.cn.md`](archives/difangzhi.cn.md) — difangzhi.cn —— 中国方志网
- [`archives/guji.nlc.cn.md`](archives/guji.nlc.cn.md) — guji.nlc.cn —— 中华古籍书目检索平台
- [`archives/historical-maps.md`](archives/historical-maps.md) — historical-maps —— 历史地图与历史 GIS
- [`archives/kanripo.md`](archives/kanripo.md) — kanripo —— 漢籍リポジトリ 古籍全文
- [`archives/local-gazetteers-cn.md`](archives/local-gazetteers-cn.md) — local-gazetteers-cn —— 全国省级方志省情站总表
- [`archives/local-search-tools.md`](archives/local-search-tools.md) — local-search-tools —— 本地全文检索工具
- [`archives/modern-press-databases.md`](archives/modern-press-databases.md) — 近代报刊数据库总览 —— 民国报刊库入口与权限一览
- [`archives/modernhistory.md`](archives/modernhistory.md) — modernhistory.org.cn —— 抗战与近代中日文献平台
- [`archives/nlc.cn.md`](archives/nlc.cn.md) — nlc.cn —— 国家图书馆数字资源入口
- [`archives/person-databases.md`](archives/person-databases.md) — person-databases —— 人物·荣誉·英烈名录库
- [`archives/shtong.md`](archives/shtong.md) — shtong.gov.cn —— 上海通 上海数字方志
- [`archives/shuge.md`](archives/shuge.md) — shuge.org —— 书格 公共版权古籍 PDF
- [`archives/sinica.md`](archives/sinica.md) — sinica —— 中研院档案与人物库

## social —— 社交平台

- [`social/agent-reach.md`](social/agent-reach.md) — agent-reach —— Agent 上网能力安装与路由
- [`social/chubbyskills.md`](social/chubbyskills.md) — chubbyskills —— 链接转 Markdown 的采集技能集
- [`social/cn-scraper-mcp.md`](social/cn-scraper-mcp.md) — cn-scraper-mcp —— 本地登录态收割与多平台检索
- [`social/tieba.baidu.com.md`](social/tieba.baidu.com.md) — tieba.baidu.com —— 地方讨论线索检索
- [`social/voice-platforms.md`](social/voice-platforms.md) — 问政与民生平台 —— 领导留言板·百姓呼声·网上民声
- [`social/weibo.com.md`](social/weibo.com.md) — weibo.com —— 热搜匿名可取，检索需登录
- [`social/xiaohongshu-mcp.md`](social/xiaohongshu-mcp.md) — xiaohongshu-mcp —— 小红书检索/详情/评论
- [`social/zhihu.com.md`](social/zhihu.com.md) — zhihu.com —— 检索与专栏均需登录

## tools —— 通用工具

- [`tools/agent-browser.md`](tools/agent-browser.md) — agent-browser —— 浏览器 CLI，复用 Chrome 登录态
- [`tools/defuddle.md`](tools/defuddle.md) — defuddle —— HTML 正文抽取（→ 干净 Markdown）
- [`tools/glm-ocr.md`](tools/glm-ocr.md) — GLM-OCR —— 中文表格/公式/手写 OCR
- [`tools/macos-vision-ocr.md`](tools/macos-vision-ocr.md) — macos-vision-ocr —— 系统自带中文 OCR（零依赖）
- [`tools/mineru.md`](tools/mineru.md) — MinerU —— 文档解析 OCR（云 API / 本地 CLI）
- [`tools/playwright-cli.md`](tools/playwright-cli.md) — playwright-cli —— 真实浏览器交互 CLI（ref 工作流）
- [`tools/r.jina.ai.md`](tools/r.jina.ai.md) — r.jina.ai —— 网页转 Markdown 代理（本机不可达）
- [`tools/scrapling.md`](tools/scrapling.md) — Scrapling —— 反爬绕过 + 三级抓取
- [`tools/web.archive.org.md`](tools/web.archive.org.md) — web.archive.org —— 网页存档回捞（间歇可达）

## methods —— 检索方法

- [`methods/dataset-hubs.md`](methods/dataset-hubs.md) — dataset-hubs —— 免费数据集市的 JSON 检索接口
- [`methods/historical-web.md`](methods/historical-web.md) — historical-web —— 历史网页与快照回捞
- [`methods/intl-data-apis.md`](methods/intl-data-apis.md) — intl-data-apis —— 国际统计库的开放 API 速查
- [`methods/literature-delivery.md`](methods/literature-delivery.md) — literature-delivery —— 从书名/篇名到全文的传递路由
- [`methods/microdata-access.md`](methods/microdata-access.md) — microdata-access —— 微观调查数据获取路线图
- [`methods/officials-research.md`](methods/officials-research.md) — officials-research —— 官员/干部检索方法卡
- [`methods/osint-china.md`](methods/osint-china.md) — osint-china —— 英文 OSINT 方法的中文迁移
- [`methods/search-syntax.md`](methods/search-syntax.md) — search-syntax —— 引擎操作符与站内检索参数速查
- [`methods/stat-yearbook-download.md`](methods/stat-yearbook-download.md) — stat-yearbook-download —— 统计年鉴与公报批量下载

## meta —— 元资源（找源的地方）

- [`meta/awesome-china-mcp.md`](meta/awesome-china-mcp.md) — awesome-china-mcp —— 中国应用 MCP 索引
- [`meta/awesome-lists.md`](meta/awesome-lists.md) — awesome-lists —— 技能与工具目录、市场入口
- [`meta/skills-discovery.md`](meta/skills-discovery.md) — skills-discovery —— 持续发现新 skill 与新源
- [`meta/style.md`](meta/style.md) — style —— 源卡与索引的写法规范

