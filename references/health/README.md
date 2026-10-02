# references/health —— 健康与人口数据源索引

本目录收录**疾病/公共卫生、卫生统计、药品与医疗器械注册备案及药品集采目录、人口与人口普查**的数据与检索入口。原则：优先取**开放机器接口**（WHO GHO、UN Data Portal），无接口的疾控/卫健委/药监门户按 HTML/PDF 抓；国际微观数据（IPUMS、CHNS）只记取用路径与门槛，**不搬运数据副本**。

## 文件一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `chinacdc.cn.md` | 中国疾控中心 | **全国传染病疫情月报**（HTML）、中国/全球突发事件风险评估（PDF）、烟草调查；英文周报 `weekly.chinacdc.cn` | ✅ 免登录 |
| `nhc.gov.cn.md` | 国家卫健委 | **卫生健康统计年鉴**、统计公报、医疗服务月报；栏目 URL 与年鉴 PDF | ⚠️ 需浏览器 |
| `nmpa.gov.cn.md` | 国家药监局 | **药品批准文号/国产·进口药品**、医疗器械注册备案、化妆品、UDI 数据库；数据查询平台 JSON 接口与子库 itemId 清单 | ⚠️ 仅浏览器 |
| `drug-procurement.md` | 上海阳光医药采购网 / 国家医保局 | **国家组织药品集采中选结果**（PDF）、国家医保药品目录、基本药物目录 | ✅ 免登录 |
| `ncmi.cn.md` | 国家人口健康科学数据中心 | 人口健康**科研数据集**浏览/检索（人体成分、影像标注、环境暴露…），含 JSON 检索接口与参数表 | ⚠️ 检索可浏览 |
| `phsciencedata.cn.md` | 公共卫生科学数据中心 | 公共卫生专题库（法定报告传染病、营养与健康调查、寄生虫病…）；JSP 页面检索 | ✅ 页面可达 |
| `healthdata.org.md` | IHME / GHDx | **全球疾病负担 GBD**（DALY/病因/风险，含中国）；GBD Results 工具 + GHDx 记录 + 公开编码本 | ⚠️ 下载需登录 |
| `who-gho.md` | WHO GHO | **3099 个全球卫生指标** OData JSON API，免 key，按国家/年份/性别取数 | ✅ API 可用 |
| `population.un.org.md` | 联合国人口司 | **世界人口展望 WPP**（1950–2100）+ Data Portal REST API（目录免 token、取数需 token） | ⚠️ 取数需 token |
| `ipums.org.md` | IPUMS International | 跨国**人口普查微观数据**（含中国 1982/1990/2000），网页检索 + API（需 key） | ⚠️ 需注册 |
| `stats.gov.cn-census.md` | 国家统计局 | **人口普查**数据与《中国人口普查年鉴》（JS 页 + 扫描 JPG 表） | ⚠️ 图片表 |
| `chns.md` | UNC CHNS | **中国健康与营养调查**长期面板（1989–2015，10 轮）微观数据 | ⚠️ 需注册 |

## 选路

- **要传染病发病/死亡月度数字** → `chinacdc.cn.md` 的 `jksj01`（HTML 正文，免费直取）；要风险评估/事件趋势 → `jksj02`/`jksj03`（PDF）。
- **要卫生机构/床位/费用/健康指标等年鉴数字** → `nhc.gov.cn.md`（注意全站 412 WAF，**须浏览器**）；备选各省卫健委或 `../stats/cnki-data.md`。
- **要药品批准文号/注册证号、医疗器械注册备案、化妆品批件、UDI 产品标识** → `nmpa.gov.cn.md`（数据查询平台是瑞数 WAF + 需 `sign` 签名，**仅浏览器**；UDI 子站可 `curl`，用 `getDeviceList.html` 取 JSON）。
- **要国家组织药品集采中选结果/中选价、国家医保药品目录、基本药物目录** → `drug-procurement.md`（集采原始件落 smpaa 附件 PDF；目录走 nhsa `downfile.jsp` 直下）。
- **要国内可引用的科研数据集（含数据凭证）** → `ncmi.cn.md`（`browse.html?type=2&searchField=keyword&keyword=…`）；公共卫生专题再叠加 `phsciencedata.cn.md`。
- **要免 key 的跨国卫生指标 JSON** → `who-gho.md`（先用 `/Indicator` 定位代码，再带 `$filter=SpatialDim eq 'CHN'` 取中国）。
- **要 GBD 口径的 DALY/病因负担（含分省）** → `healthdata.org.md`（无开放 API；登录 + 条款后在 GBD Results / GHDx 下载，公开编码本可直下）。
- **要跨国人口预测/人口分母** → `population.un.org.md`（批量走 `/wpp/downloads?…CSV format`；取数走 Data Portal API + token）。
- **要人口普查汇总口径** → `stats.gov.cn-census.md`（年鉴表为扫描图，需 OCR）；年度人口数值改走 `../stats/data.stats.gov.cn.md`。
- **要可自行交叉制表的微观人口/健康数据** → 国际 `ipums.org.md`，中国本土 `chns.md`（及 `../surveys/` 其他调查）。

## 相关

- 官方统计与区划口径：`../stats/`（`data.stats.gov.cn.md`、`mca.gov.cn.md`）。
- 国际统计/卫生对照源：`../intl/`（与 `who-gho.md`、`population.un.org.md` 交叉）。
- 微观调查数据（CFPS/CHARLS/CHIP 等）：`../surveys/`（与本层 `ipums.org.md`、`chns.md` 交叉）。
- 医保制度与统计口径：`../surveys/social-insurance.md`（nhsa 统计公报、医保数智库、jrobot 检索）、`../stats/ministry-stats.md`（医保局「统计数据」栏目）。
- 卫健政策/机构查询：`../gov/edu-research-institutions.md`（卫健委基本药物目录查询、医疗机构查询，与 `nmpa.gov.cn.md`、`drug-procurement.md` 交叉）。
- 论文/年鉴文献入口：`../academic/`；抓取与 OCR 工具：`../tools/`。
- 卡片写法与索引规范：`../meta/style.md`。
- 本层所有状态码、端点、字段均来自 2026-10-03 本机实测；来自检索结果的 URL（如 nhc 栏目路径）已在卡内逐条标注。
