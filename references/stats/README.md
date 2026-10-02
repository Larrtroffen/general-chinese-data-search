# stats/ —— 统计与区划数据源

本层收录「代码/名录类」与「统计数据类」官方与半官方来源：行政区划代码、街道乡镇名录、统计年鉴、统计公报、月度/年度指标数值。

## 文件一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `stats.gov.cn.md` | 国家统计局 | 统计用区划代码（街道/镇/乡）历史页面 | ❌ 历史页下线 |
| `xzqh.org.md` | 区划地名网（非官方） | 逐区街道/镇/乡名录（转自统计用区划代码） | ⚠️ 转载 |
| `mca.gov.cn.md` | 民政部 | 行政区划代码：县以上静态表 + 四级（含乡级）查询接口（数据截止 2025-12-31） | ✅ 可用 |
| `data.stats.gov.cn.md` | 国家数据 | 指标数值 API：分省/全国/主要城市 月度·季度·年度 | ✅ 新接口 |
| `tjj.beijing.gov.cn.md` | 北京市统计局 | 北京统计年鉴（图片）/统计公报（HTML）/月季度数据（xls·xlsx） | ✅ 可用 |
| `ministry-stats.md` | 中央部委（教育/财政/生态环境/工信/人行…） | 各部委「数据/统计」栏目与年度公报入口总表（20+ 部委实测） | ✅ 15 站可用 |
| `geodata.md` | 自然资源部 / 各科学数据中心 | 标准地图 JSON 接口 + 天地图 key + 地球系统/气象/地震/海洋/青藏高原数据 | ✅ 含可 curl 接口 |
| `cnki-data.md` | 知网·中国经济社会大数据研究平台 | 年鉴/公报/普查表格的指标检索（`valueSearch` + `/api/csyd/*`）；匿名 471 | ⚠️ 需登录 |
| `epsnet.md` | EPS 数据平台 | 宏观/区域/城市/微观时间序列+统计表格；指标联想匿名可用 | ⚠️ 需订阅 |
| `cei-drc.md` | 中经网 / 国研网 | 资讯·数表·研究报告全文检索 + 统计数据库；列表匿名可读 | ⚠️ 条目需订阅 |
| `nbs-api-skills.md` | aahl cn-stats + openclaw-akshare skill | NBS 新接口增量：关键词搜索 `/query?search=`、大中城市 daCid、住宅价格 cid | ✅ 已验证 |
| `mcp-cnbs.md` | icen-ai/mcp-cnbs | NBS 新接口文档级洞见 + 跨源工具；`getEsDataByCidAndDt` 实测 404 | ⚠️ 未本机跑 |
| `akshare.md` | akfamily/akshare | Python 宏观/金融总库，含 NBS 新接口实现 | ⚠️ 只读参考 |
| `cnstats.md` | songjian/cnstats | 旧 `easyquery.htm` 的 dbcode/指标码语义字典 | ❌ 旧接口 403 |
| `data_location.md` | mumuy/data_location | 省市县 + 乡镇街道静态 JSON（乡级更新至 2026-09） | ✅ 可用 |
| `national-data-corpus.md` | yiyuezhuo/National-Data | 历史年鉴指标 CSV 语料（1852 文件，1978–2014，27 门类） | ⚠️ 无 license |
| `agri-stat.md` | 农业农村部 / 国家粮食和物资储备局 / 国家统计局 | 农业数据门户、粮食收购价与粮油市场周报、农村统计年鉴书目 | ✅ 栏目可用 |
| `agri-price.md` | 中国农业农村信息网 / 全国农产品批发市场价格信息系统 | 批发价格 200 指数（日·旬）与批发市场名录 JSON 接口 | ✅ curl 可用 |
| `agri-cost-benefit.md` | 国家发改委价格司 / 知网 / 商业年鉴站 | 《全国农产品成本收益资料汇编》入口（官方仅发布简报） | ⚠️ 全书需订阅 |
| `rural-surveys.md` | 农业农村部农研中心 / 中国农科院 / 社科院农发所 | 农村固定观察点、农村微观经济数据、CRRS 乡村振兴调查 | ⚠️ 申请/合作 |
| `city-stat-yearbook.md` | 国家统计局 / 知网 / 第三方年鉴站 | 《中国城市统计年鉴》《县域统计年鉴》取数入口与门槛 | ⚠️ 多需订阅 |
| `county-stats.md` | 各县统计局 / 地市统计局 / 红黑统计公报库 / 知网 | 县级公报·县级年鉴·县级财政的三条发布位与免费/付费分界 | ⚠️ 逐县拼、聚合库非官方 |
| `city-data-cn.md` | 各市统计局 / 知城数据 / 马克数据网 | 城市级数据库与市统计局入口规律 | ⚠️ 商业需登录 |
| `mobility.md` | 百度地图慧眼 / 腾讯位置大数据 | 百度迁徙 JSONP（城市间迁入迁出、迁徙指数，2019 起日度）+ 腾讯历史迁徙 | ✅ curl 可用 |
| `commute-city.md` | 中规院 / 高德 / 百度地图 / 交通运输部 | 通勤监测报告与交通报告 PDF 直链、拥堵指数、月度城市客运量 xlsx | ✅ PDF 可下 |
| `digital-economy.md` | 国家数据局 / 商务部电商司 / 信通院 | 数据要素与数字经济报告、**电商 JSON 接口**（免 key）；信通院 412 | ✅ 电商接口可用 |
| `china-io-table.md` | 国家统计局 / 各省统计局 / CEADs | 中国投入产出表（2002–2023 年份、xls 直链、分省表规律） | ✅ 年鉴 xls 可下 |

## 选路

- **要某个区/街道的官方代码**（含乡级）→ `mca.gov.cn.md` 的 `dmfw.mca.gov.cn/xzqh/getList`。
- **要区划「变更沿革」**（新设/撤销/更名）→ `mca.gov.cn.md` 的年度「县以下代码变更情况」。
- **要北京等分省的经济指标数值**（GDP、CPI…）→ `data.stats.gov.cn.md` 的 `stream/esData`；先用 `nbs-api-skills.md` 的 `GET /query?search=<关键词>` 定位 cid，比逐层翻树快。
- **要北京年鉴/公报的官方口径表** → `tjj.beijing.gov.cn.md`（注意年鉴是扫描图片，公报是 HTML，月季度数据才有 xls）。
- **要农产品批发价格 200 指数（日/旬）、批发市场名录、品种目录** → `agri-price.md`：`pfsc.agri.cn` 的 `/price_portal/*` 与 `/api/priceQuotationController/marketPageList` 免 key 直出 JSON（POST-only 注意）；200 指数十日报在 `www.agri.cn/nyb/getIndexByTenDay`（带页面 token）。
- **要粮食收购价/粮油市场周报、夏秋粮收购进度** → `agri-stat.md` 的粮食和物资储备局「粮食数据」栏目（`lswz.gov.cn/html/zmhd/lysj/`）；注意周报正文是 PNG 图片，取结构化数字改用 `agri-price.md`。
- **要农业农村部口径的年度/月度农业数字，或《中国农村统计年鉴》** → `agri-stat.md`：数据门户 `data.moa.gov.cn` 目录需浏览器；农村统计年鉴只有**书目页**，免费全文只到《中国统计年鉴》（`stats.gov.cn/sj/ndsj/`），跨部委口径另见 `ministry-stats.md`。
- **要每亩成本收益（稻谷/小麦/玉米/生猪…）** → `agri-cost-benefit.md`：发改委只有《农产品成本调查简报》，全书走知网（`cnki-data.md`）或商业年鉴站。
- **要农户/村庄层级追踪微观数据** → `rural-surveys.md`：全国农村固定观察点需**与农研中心合作署名**，CRRS 走社科院云桌面申请；家庭金融/资产类（CHFS、CFDB）转 `../surveys/`。
- **要某部委口径的年度/月度数字或年鉴·公报** → `ministry-stats.md`：先查总表定位栏目（教育/环境/人行/交通可拼年份 URL；财政/自然资源/民航/医保有站内全文检索）；卫健委、海关总署为瑞数 412，需浏览器。
- **要标准地图/审图号、行政区划底图或 POI/地理编码检索** → `geodata.md`：标准地图 `searchPicture.do` 免 key JSON，天地图需注册取 `tk`。
- **要 DEM/土地利用/气象/地震/海洋/地质等科研空间数据** → `geodata.md` 的分平台表（geodata/earthquake/nmdis/tpdc/agridata，目录多匿名可读，**下载多需实名注册**）。
- **海关口径数字被 412 拦住时** → 改用海关总署「统计月报」或国家统计局口径侧取（见 `ministry-stats.md` 坑 1）。
- **要年鉴/公报里的「表格数值」且免费路径拿不到** → `cnki-data.md`（知网经济社会大数据平台：按指标检索+组配，需机构/个人登录，匿名检索接口返回 471）。
- **要县级（县/县级市/市辖区）的 GDP·人口·财政等年度值** → `county-stats.md`：没有全国统一免费 API，走**逐县统计公报**（地市统计局「区县公报」栏一次列全下辖县区最省事）或聚合库 `tjgb.hongheiku.com` 全文搜（非官方、完整度不一）；全国口径《县域统计年鉴》县市卷/乡镇卷在知网（付费，乡镇卷是乡镇级唯一系统来源）；县级财政走各县「财政预决算公开」专栏 PDF。
- **要定位某个县的官网/统计局栏目** → `../regional/county-portals.md`：域名主流是 `www.<县名拼音>.gov.cn`，但安徽加省缩写（`ahfeixi`）、湘川缩拼（`csx`）；先按区划码取名再逐县验，WAF 站点换 http/去 www/移动域名。
- **要长历史时间序列（尤其城市/产业面板）** → `epsnet.md`：先用匿名的 `/search/recommendIndicator.do?keyword=` 确认指标名，再走订阅取数（OLAP 在 `olap.epsnet.com.cn`）。
- **要"某话题有几篇 / 有哪些数表"的线索** → `cei-drc.md`：中经网 `POST /d/search/highSearch.action` 匿名能出条目；国研网 `getSearchString` 匿名只给命中数（人口=21885）。
- **要中经网/国研网的「数值」** → `ceidata.cei.cn`（中经数据，`getMenulist` 按库码）与 `data3.drcnet.com.cn/statistical`，均需登录订阅。
- **要乡镇街道代码且想离线缓存/整表反查** → `data_location.md` 的 `list.json`（省市县）+ `code/<区县码>.json`（乡级）；要**官方**口径仍回 `mca.gov.cn.md`。
- **要 1978–2014 历史年度指标的长表底表** → `national-data-corpus.md`（1852 个 CSV，无 API 直取）。
- **要现成 pandas/行情类，或抄 NBS 新接口标准实现** → `akshare.md`（`macro_china_nbs_nation/region`）。
- **想用 MCP/想读新版接口文档** → `mcp-cnbs.md`（`api_introduce.md`；注意其 `getEsDataByCidAndDt` 端点实测 404）。
- **旧 `easyquery.htm` 的代码语义（dbcode/指标码）参照** → `cnstats.md`（该接口已 403，仅作字典）。
- **要城市间人口迁入迁出/迁徙规模指数**（日度，2019 起）→ `mobility.md`：`huiyan.baidu.com/migration/*.jsonp` 免 key 直出 JSONP（`dt=city` 须给城市码）；腾讯 `heat.qq.com` 那支已停更、只作历史。
- **要城市通勤监测报告、交通拥堵/健康指数报告 PDF、月度城市客运量** → `commute-city.md`：慧眼 `reports.jsonp` 定位报告 id → 按模板下 PDF（勿用 HEAD 判活）；交通运输部月度客运量附分省 xlsx。
- 第三方名录（`xzqh.org.md`、`data_location.md`、`national-data-corpus.md`）仅作补充，正式引用请标注「转自国家统计局/民政部」。
- 国家统计局「统计用区划代码」历史页面已下线（见 `stats.gov.cn.md`），乡级代码请改走民政部 `dmfw` 平台，或离线用 `data_location.md`（非官方）。
- 旧 `easyquery.htm` 接口已全站 403（UrlACL），**凡仍打该域名的第三方包（如 `cnstats`）均已失效**，改用 `data.stats.gov.cn.md` 的 `/dg/website/publicrelease/web/external/*`。
- 新增的第三方仓库卡（`mcp-cnbs`/`akshare`/`cnstats`/`data_location`/`national-data-corpus`/`nbs-api-skills`）**只作来源线索**：不整仓拷贝代码、不装依赖；取用一律走 raw/npm/PyPI，正式引用须换回官方站口径。
- 第三方许可：`data_location`=MIT、`akshare`=MIT、`cnstats`=MIT、`aahl/skills`=MIT、`openclaw-akshare-skill`=MIT、`mcp-cnbs` 仓库根为 Apache-2.0（npm 包却标 MIT，需核）、`national-data-corpus` **无 license**（仅作线索，勿再分发）。
- **订阅制商业库四家**（`cnki-data.md` / `epsnet.md` / `cei-drc.md` 里的中经网与国研网）自述口径与规模只作「上游声明」；本机实测只覆盖到**入口 URL + 匿名可达的接口 + 登录/订阅门槛**，登录态下的取数流程未验证。要数值优先走官方免费源（`data.stats.gov.cn.md` / `tjj.beijing.gov.cn.md`）。
- 中文官方/半官方站抓取建议 ≥1.5s 间隔、桌面 UA；`/query?search=` 关键词搜索 `pageSize` 用 15（实测 2 时返回空）。

## 相关

- 免费数据集市（天池/和鲸/ScienceDB/ModelScope/HF-Mirror，带 JSON 检索接口）：[`../methods/dataset-hubs.md`](../methods/dataset-hubs.md) —— 与官方统计口径互补，但**许可与质量需逐条核**。
- 农户/村庄层级追踪微观数据（固定观察点、CRRS）与家庭金融调查：[`rural-surveys.md`](rural-surveys.md) + [`../surveys/`](../surveys/README.md) —— 宏观统计口径之外的个体级数据，均为申请/合作制。
- 上游总表与用法：仓库根 `SKILL.md`。
