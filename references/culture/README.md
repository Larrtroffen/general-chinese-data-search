# culture/ —— 民族·宗教·语言·遗产数据源

本层收录民族、宗教、语言与文化遗产方向的**官方名录库、统计公报与检索入口**：国家民委与宗教事务口径、语保工程采录数据、非遗与文保名录、宗教团体官网、世界遗产名录；另收**文化市场统计**（电影/出版/文旅/演出/视听）与**图书书目核发**入口。

## 文件一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `neac.gov.cn.md` | 国家民族事务委员会 | 民族地区统计公报、民族政策文献、教育基地/示范单位名录、少数民族古籍；开普云站内检索 | ✅ 检索可用 |
| `mzb.com.cn.md` | 中国民族宗教网（中国民族报社） | 民族宗教资讯检索（TRS WAS5，需 Cookie） | ✅ 需 Cookie |
| `zhongguoyuyan.cn.md` | 中国语言资源保护工程采录展示平台 | 方言/少数民族语言调查点坐标与工程统计（匿名 JSON） | ⚠️ 明细需登录 |
| `ihchina.cn.md` | 中国非物质文化遗产网 | 国家级非遗项目名录、代表性传承人（JSON 接口） | ✅ JSON 接口 |
| `ncha.gov.cn.md` | 国家文物局 | 全国重点文物保护单位名单、博物馆年度报告系统入口 | ⚠️ 仅 http |
| `sara.gov.cn.md` | 国家宗教事务局 | 全国宗教活动场所名录（匿名 JSON，约 4.2 万条） | ✅ 匿名 JSON |
| `religious-bodies.md` | 五大宗教团体官网 + 国家宗教事务局院校查询 | 全国宗教院校名录（94 所 JSON）、伊协/天主教/基督教两会组织人事与站内检索 | ✅ 匿名 JSON |
| `religion-publications.md` | 中国宗教学术网（世界宗教研究所） | 宗教期刊逐年逐期目录、学者库、站内 WAS5 检索 | ✅ 检索可用 |
| `chinabuddhism.com.cn.md` | 中国佛教协会 | 协会新闻、制度法规、发布位（WAF，需浏览器） | ⚠️ 需浏览器 |
| `taoist.org.cn.md` | 中国道教协会 | 协会/组织机构/理事会/学院栏目（须用裸域） | ⚠️ www 被拦 |
| `whc.unesco.org.md` | UNESCO 世界遗产中心 | 世界遗产名录 GeoJSON（含中国 61 项） | ⚠️ 需浏览器 |
| `zytzb.gov.cn.md` | 中共中央统一战线工作部 | 宗教工作与政策口径；站内检索（中新网托管） | ✅ 可用 |
| `market-stats.md` | 电影局/新闻出版署/文旅部/广电总局/演出协会 | 文化市场统计公报、票房、广电视听、演出数据 | ✅ 多源可用 |
| `publishing-isbn.md` | 国家版本数据中心/联合编目/开卷等 | 图书 ISBN/CIP 核发、馆藏书目、零售榜 | ⚠️ 检索多需登录 |

## 选路

- **要民族地区/自治州的经济社会统计数字或民族政策原文** → `neac.gov.cn.md`：统计栏目聚合国家与自治州公报（HTML），政策与名录在 `/seac/xxgk/`、`/seac/ziliao/`；找站内某文用开普云 `/s?siteCode=bm08000014`。
- **要民族/宗教领域的新闻与深度报道** → `mzb.com.cn.md`：TRS WAS5 检索，**先取首页 Cookie** 再带 `channelid=259355`；仅作媒体补充，正式引用回 `neac.gov.cn.md` / `sara.gov.cn.md`。
- **要方言/少数民族语言的调查点分布或工程规模** → `zhongguoyuyan.cn.md`：`POST /api/mongo/query/latestSurveyMongo`（总量统计）与 `indexLocations`（点位坐标）匿名可用；省/点明细与语料须注册登录。
- **要国家级非遗项目名录 / 代表性传承人** → `ihchina.cn.md`：`/getProject.html` 与 `/art/representative.html` 直出 JSON，按关键词/门类/地区/时间筛；UNESCO 非遗项目页为 HTML。
- **要全国重点文物保护单位名单或博物馆年报口径** → `ncha.gov.cn.md`：国保名单在 `col/col2284–2289`（HTML，**必须 http**）；博物馆明细在 `nb.ncha.gov.cn/museum.html`（填报系统，需登录）。
- **要某地有哪些宗教活动场所（佛教/道教/伊斯兰教/天主教/基督教及其派别）** → `sara.gov.cn.md`：`api.sara.gov.cn/mis//web/religionPlace/list` 匿名 JSON，`total:42440`；教职人员页需登录。
- **要全国宗教院校名录（五大宗教，含主办单位/院校名/地址/负责人）** → `religious-bodies.md`：`api.sara.gov.cn/mis//web/religionInstitution/list` 匿名 JSON（`total:94`；先取 `getAllReligion` 拿 `religionTypeId`）。
- **要伊斯兰教/天主教/基督教团体自身的组织人事、制度与站内文章** → `religious-bodies.md`：伊协 `/cms/custom/query_yixie_wangzhan.jsp`（JSON）、基督教两会 `/search?title=`（HTML）；⚠️ 各官网「信息查询」是**需登录**的宗教基础信息查询系统。
- **要宗教团体（佛教/道教协会）自身的资讯与制度** → `chinabuddhism.com.cn.md`（WAF，需浏览器）与 `taoist.org.cn.md`（用裸域）；团体口径，政策原文回 `zytzb.gov.cn.md` / `sara.gov.cn.md`。
- **要宗教学期刊逐期目录或世界宗教研究所的学者/研究领域** → `religion-publications.md`：`iwr.cass.cn/qknj/<slug>/` 目录页；检索走 `iwr.cssn.cn/was5/web/search?channelid=218937`（HTML）。
- **要世界遗产名录（含中国项目、类别、濒危、坐标）** → `whc.unesco.org.md`：Cloudflare 拦 CLI，需浏览器内取 `?cid=31&l=en&mode=geojson`，按 `component_state` 过滤后按 `id_no` 去重。
- **要中央口径的宗教工作/政策法规** → `zytzb.gov.cn.md`：站内检索外包给中新网，参数是 `q`（不是 `keyword`）。
- **要电影票房、出版/文旅/广电视听/演出市场统计** → `market-stats.md`：电影票房到 `zgdypw.cn/sc/sjbg/`（专资办周/月报，图表），出版统计到国家新闻出版署 `xxgk/fdzdgknr/tjxx/`（PDF 公报），文旅到 `zwgk.mct.gov.cn/zfxxgkml/{447/465,503/506}/`，广电到 `nrta.gov.cn/art/…/art_113_*.html`；演出协会为 SPA，无开放接口。
- **要某本书的 ISBN/CIP 书目、新书核发或零售榜** → `publishing-isbn.md`：全国新书目 `/api/index/hfList`（AES 解密）取最新 CIP；检索需登录；零售数据（开卷/中金易云）订阅制，馆藏书目走 `opac.nlc.cn/F`（仅 http）。

## 相关

- 行政区划代码、统计年鉴与部委统计公报：[`../stats/README.md`](../stats/README.md)（民族地区数字与文旅统计的原始口径在 `stats`/`ministry-stats`）。
- 政府政策文件与部委导航：[`../gov/README.md`](../gov/README.md)（政策原文、机构入口；新闻出版/电影/广电口径亦见本层 `market-stats.md`）。
- 古籍与地方文献（少数民族古籍、方志）：[`../archives/README.md`](../archives/README.md)（馆藏书目另见 `../archives/nlc.cn.md`）。
- 国际组织统计与公约类数据：[`../intl/README.md`](../intl/README.md)（UNESCO/世行等口径）。
- 上游总表与用法：仓库根 `SKILL.md`。
