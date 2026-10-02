# env/ —— 环境·能源·碳数据

本层放**环境、能源、碳与气象灾害**类数据源：中国官方环境统计与监测、企业环境信息、碳核算与能源统计、资源环境空间数据，以及国际能源/碳/灾害口径。要中国国内统计口径的宏观数字请先看 `../stats/`；要纯国际组织面板看 `../intl/`。

## 文件一览

| 文件 | 来源 | 用途/何时用 | 状态 |
|---|---|---|---|
| `ceads.net.md` | CEADs 中国碳核算数据库 | 中国分省/城市/县级 CO₂ 与能源清单、省级投入产出表；学术碳核算首选 | ⚠️ 需注册下载 |
| `globalcarbonproject.org.md` | Global Carbon Project / 全球碳预算 | 全球与各国碳收支、海洋碳汇，数据在 Zenodo（CC-BY） | ✅ 本机实测 |
| `mee.gov.cn.md` | 生态环境部 | 生态环境统计年报 / 生态环境状况公报（污染物排放、治理投入） | ✅ 本机实测 |
| `cnemc.cn.md` | 中国环境监测总站 | 全国城市/点位空气质量实时、24 小时与日序列，匿名 JSON | ✅ 匿名 JSON |
| `permit.mee.gov.cn.md` | 全国排污许可证管理信息平台 | 排污许可证受理/批准公告（匿名）与企业许可信息（需登录） | ⚠️ 详情需登录 |
| `ipe.org.cn.md` | IPE 公众环境研究中心（蔚蓝地图） | 企业环境监管记录、供应链 CITI/CATI、城市双碳指数 | ⚠️ 检索需登录 |
| `enforcement.md` | 环境行政处罚与执法公示 | 部省两级处罚专栏 + 企业环境信息依法披露；查企业/某地被处罚 | ⚠️ 部分省级仅浏览器 |
| `inspection.md` | 中央生态环境保护督察（部站专栏） | 督察公告、典型案例、反馈意见全文、整改问责 | ✅ 本机实测 |
| `eia.md` | 建设项目环评公示（部 / 京 / 第三方） | 环评报告书全本、公参、验收、水保、节能公示；查某项目的环境文件 | ⚠️ 部分需浏览器/登录 |
| `nea.gov.cn.md` | 国家能源局 | 能源月度数据（电力/绿证/充电设施），站内检索 JSON | ✅ 本机实测 |
| `resdc.cn.md` | 中科院资源环境科学数据中心 | 中国土地利用/植被/土壤/人口等栅格与矢量（WebShield + 登录） | ⚠️ 下载需登录 |
| `data.cma.cn.md` | 中国气象数据网（国家气象信息中心） | 地面/高空/雷达/卫星/再分析气象数据检索下载 | ⚠️ 需实名登录 |
| `ncc-cma.net.md` | 国家气候中心（cmdp） | 环流指数、160 站气温降水、ENSO/季风/积雪监测、气候公报 | ✅ 匿名文件 |
| `emdat.be.md` | EM-DAT / CRED·UCLouvain | 全球灾害事件级面板（灾种×国家×伤亡×损失） | ⚠️ 需注册 |
| `iea.org.md` | 国际能源署 | 世界能源平衡表与能源统计（免费区小、多数付费） | ⚠️ Cloudflare 拦 |
| `eia.gov.md` | 美国能源信息署 | 美国 + 国际能源序列，API v2 免 key 可试（DEMO_KEY） | ✅ 本机实测 |

## 选路

- **要中国碳排放/能源清单（分省、城市、县级）** → `ceads.net.md`：清单页看元数据匿名，取数需注册登录；全球/各国口径另走 `globalcarbonproject.org.md`（Zenodo，CC-BY）。
- **要中国空气质量的数值** → `cnemc.cn.md` 的 `/CityData/*` 与 `/HourChangesPublish/*`（匿名 JSON，实时 + 24h）；要年度/历史另见 `mee.gov.cn.md` 的公报年报。
- **要企业环保是否合规** → 先 `permit.mee.gov.cn.md`（许可证公告，匿名）再看 `ipe.org.cn.md`（环境监管记录，需登录）；IPE 是整合方，正式引用回链原公告。
- **要环境行政处罚 / 执法公示** → `enforcement.md`：部级「执法制度与行政处罚」+ 省级专栏（山东静态 HTML、江苏双公示接口 `sgsXzcfGsList`、广东/浙江 JS、湖北 WAF）+ 各省「企业环境信息依法披露系统」；许可/处罚「双公示」另见 `../gov/credit-china.md`。
- **要中央生态环保督察的公告、典型案例、反馈意见** → `inspection.md`（`mee.gov.cn/ywgz/zysthjbhdc/` 下 `dcjl`/`dcjz`/`dczg` 三子栏，静态分页，覆盖约 2016 年至今）。
- **要某个建设项目的环评报告书全本 / 公参说明 / 验收报告** → `eia.md`：部批走 MEE 三栏（受理/拟审查/已批准），全国范围聚合查 `eiacloud.com/gs/`（匿名可搜、下载需登录）与 `hjxxgs.com`（附件直链），北京审批结果走 `gzcx.sthjj.beijing.gov.cn`（列表受 WAF 拦，需浏览器）；配套许可与处罚见 `permit.mee.gov.cn.md`、`enforcement.md`。
- **要中国能源月度数字** → `nea.gov.cn.md` 的检索 JSON（`getNewsFromAllData`）；长期能源平衡表/年鉴走 `../stats/cnki-data.md` 与国家统计局口径。
- **要空间栅格/土地利用** → `resdc.cn.md`（需先过 WebShield 再登录下载）；CLCD（武大 30 m 土地覆盖）不在该站，托管在 figshare（本机 403，需浏览器）。
- **要气象观测与再分析** → `data.cma.cn.md`（需实名登录）；只要环流指数与气候监测产品 → `ncc-cma.net.md`（匿名文件）；底图/地理数据回 `../stats/geodata.md`。
- **要灾害事件面板** → `emdat.be.md`（全球，需注册）；中国灾害统计走应急管理部公报（见 `../stats/ministry-stats.md`）。
- **要跨国能源对比** → 优先 `eia.gov.md`（美国能源信息署，**非环评**；免费 API + 国际数据）；IEA 完整数据集多付费且被 Cloudflare 拦，用浏览器；世界银行能源指标码见 `../intl/worldbank.org.md`。

## 相关

- 部委数据栏目总表与站内检索：`../stats/ministry-stats.md`（含生态环境部、应急管理部同口径入口）。
- 空间数据与地图底图：`../stats/geodata.md`（标准地图、天地图、地震/海洋/青藏高原等分平台）。
- 年鉴/公报表格数值（含《中国环境统计年鉴》《中国能源统计年鉴》）：`../stats/cnki-data.md`、`../stats/data.stats.gov.cn.md`。
- 国际组织面板与聚合接口：`../intl/`（`worldbank.org.md`、`oecd.org.md`、`comtrade.un.org.md`、`ourworldindata.org.md`）。
- 数据仓储/DOI 托管（Zenodo、figshare、Dataverse）：`../repos/`。
- 第三方数据集市与检索方法：`../methods/dataset-hubs.md`、`../methods/intl-data-apis.md`。
- 行政许可/行政处罚「双公示」与信用信息：`../gov/`（`credit-china.md`）。
- 论坛/社区里流转的环评报告全本与考试真题附件：`../media/forum-docs.md`（`eiafans`、`bbs.eiacloud.com`）。
- 卡片与索引写法：`../meta/style.md`。
