# industry/ —— 行业与协会数据源

本层收录**国家级行业协会 / 行业主管部门侧**的公开数据入口：汽车、钢铁、机械、纺织、轻工、物流、房地产、医药、电子信息、商业零售，以及国资委央企名录与行业年鉴路径。协会站普遍「有新闻、缺数据」——本层逐家实测了「统计/数据/运行」栏目是否真的发布数据。

## 文件一览

| 文件 | 来源 | 用途/何时用 | 状态 |
|---|---|---|---|
| `caam.org.cn.md` | 中国汽车工业协会 | 汽车/摩托车月度产销、进出口、分国别数据 | ✅ 可抓 |
| `csteelnews.com.md` | 中国钢铁新闻网（中钢协主管） | 铁矿石价格指数（CIOPI）、钢市行情分析 | ⚠️ 指数栏陈旧 |
| `chinaisa.org.cn.md` | 中国钢铁工业协会 | 钢协「统计发布/环保统计/价格指数」栏目入口 | ⚠️ 列表 JS 渲染 |
| `mei.net.cn.md` | 中国机械工业联合会（机经网） | 机械工业经济运行资讯、频道分页规律 | ⚠️ 无数据栏 |
| `cntac.org.cn.md` | 中国纺织工业联合会 | 纺织「数据分析」栏目（URL 来自检索，未实测） | ❌ 本机不可达 |
| `clii.com.cn.md` | 中国轻工业联合会（轻工业信息网） | 轻工月度运行、《轻工业统计资料》目录 | ⚠️ 报告需登录 |
| `chinawuliu.com.cn.md` | 中国物流与采购联合会 | PMI、物流景气/仓储/电商物流指数月度 | ✅ 可抓 |
| `clic.org.cn.md` | 中国物流信息中心（中物联直属） | PMI/物流指数分类归档 + 各直报系统入口 | ✅ 可抓 |
| `fangchan.com.md` | 中国房地产业协会（中房网） | 房企业绩与市场数据、房地产年鉴频道 | ✅ 部分付费 |
| `yytj.org.cn.md` | 中国医药统计网（医药工业信息中心） | 医药工业统计制度、百强榜、《医药统计年报》 | ⚠️ 数值付费 |
| `cpema.org.md` | 中国医药企业管理协会 | 协会动态（**无统计栏目**） | ❌ 无数据 |
| `citif.org.cn.md` | 中国电子信息行业联合会 | 通知/公示（Vue SPA，仅浏览器） | ❌ 仅浏览器 |
| `cgcc.org.cn.md` | 中国商业联合会 | 中国零售业景气指数（CRPI）月度分析 | ⚠️ 更新停滞 |
| `cinic.org.cn.md` | 中国产业经济信息网 | 统计局/工信部口径月度数据转载汇总 | ⚠️ 二手转载 |
| `cia.org.cn.md` | 中国信息年鉴 | 信息化基础数据指标（1998 至今，近 60 项） | ⚠️ 表格需订阅 |
| `sasac.gov.cn.md` | 国务院国资委 | 央企名录（含官网）、国企经济运行月度 | ✅ 可抓 |
| `soe.md` | 国务院国资委 / 财政部资产管理司 | 央企专项名单（双百/科改）、业绩考核 A 级名单、社会责任、国企月度财务 | ✅ 可抓 |
| `industry-yearbooks.md` | 各协会/年鉴编辑部 | 行业年鉴「官网入口 / 付费 / 不可达」分级路径 | ⚠️ 多为付费 |
| `rail-aviation.md` | 国家铁路局 / 国铁集团 / 民航局 / 城轨协会 | 铁路民航城轨的月度·年度统计与公报 PDF | ✅ 公报可下 |
| `aviation-rail-ops.md` | OpenSky / 民航局 / 中国民航网 / 铁路 | 航班 ADS-B 状态向量、航班正常率、铁路月度细项 | ✅ OpenSky 可调 |
| `ports-shipping.md` | 交通运输部 / 上海航运交易所 / 中国港口协会 | 港口货物·集装箱吞吐量（xlsx）、SCFI/CCFI 等运价指数 | ✅ 吞吐量可下 |
| `construction-realestate.md` | 住建部统计栏目 | 建设统计年鉴（xls）、城乡建设统计年鉴、城建状况公报 | ✅ 年鉴可下 |
| `express-logistics.md` | 国家邮政局 / 交通运输部 / 中物联 | 快递业务量与收入（月·年·全国）、快递发展指数、货运与城市客运量 | ✅ 可抓 |
| `development-zones.md` | 商务部 / 发改委 / 火炬中心 / 海关总署 | 经开区·高新区·自贸区·综保区名录与考核排名、开发区审核目录 | ✅ 部分可抓 |
| `telecom-internet.md` | 工信部 / CNNIC / 中国互联网协会 | 通信业与互联网运行月报、CNNIC 历次发展报告 PDF、互联网企业榜单 | ✅ 可抓 |
| `tourism.md` | 中国旅游研究院 / 各省文旅厅 | 旅游统计与年度报告、省级旅游统计栏目 | ✅ 部分可抓 |
| `sports.md` | 国家体育总局 / 体育用品业联合会 | 体育产业总规模公告、场地统计、协会数据 | ✅ 可抓 |
| `land-market.md` | 中国土地市场网 / 苏浙粤自然资源厅 / 中指·克而瑞 | 土地出让公告与成交公示（JSON API）、省级抽查路径、商业库门槛 | ✅ API 可调 |
| `realestate.md` | 住建部 / 国家统计局 / 中指·克而瑞 | 公积金年报 PDF、房地产投资与销售、房企销售榜 | ✅ 部分可抓 |

## 选路

- **按行业直奔对应协会卡**：汽车→`caam.org.cn.md`；钢铁→`csteelnews.com.md`（可抓）+`chinaisa.org.cn.md`（栏目地图）；机械→`mei.net.cn.md`；纺织→`cntac.org.cn.md`；轻工→`clii.com.cn.md`；房地产→`fangchan.com.md`；医药→`yytj.org.cn.md`（数据）+`cpema.org.md`（动态）；电子信息→`citif.org.cn.md`；商业零售→`cgcc.org.cn.md`。
- **要 PMI / 物流景气 / 仓储 / 电商物流 / 运价指数** → 先 `clic.org.cn.md`（分类归档全、有 `code/category` 参数表），门户新闻与最新简报看 `chinawuliu.com.cn.md`。
- **要央企名单或国有经济运行月度数字** → `sasac.gov.cn.md`：名录页给全部央企官网，运行数据在 `/n16582853/n16582888/`（全国口径，含地方国企）。
- **要国企改革专项名单、央企业绩考核 A 级、央企社会责任/月度财务** → `soe.md`：双百/科改名单在国资委专题库（附件 docx/doc，2025-04-15 版）；考核 A 级名单发布页正文是图片；国企月度财务在财政部 `zcgls.mof.gov.cn` 专栏（全国口径）。
- **要行业年鉴** → `industry-yearbooks.md` 的三级路径：官网解读（免费）→ 付费征订 → `../stats/cnki-data.md` / `../stats/epsnet.md`。
- **协会站只有新闻、没有数据栏目时**（`cpema.org.md`、`mei.net.cn.md`、`citif.org.cn.md`）→ 行业运行数字改走行业主管部门（工信部各司、`../stats/ministry-stats.md`）或国家统计局口径。
- **要快递业务量/收入、快递发展指数、邮政行业统计公报** → `express-logistics.md`：国家邮政局 `c100276`（公报+运行情况汇总）与 `c100278`（发展指数）列表页服务端渲染，月度正文含全国表；货运/城市客运量转交通运输部 xlsx，物流指数仍走 `clic.org.cn.md`。
- **要港口货物/集装箱吞吐量或水运运价指数** → `ports-shipping.md`：吞吐量取交通运输部综合规划司 xlsx 附件（`xxgk.mot.gov.cn/jigou/zhghs/…`），SCFI/CCFI 等走上交所 `sse.net.cn/index/singleIndex?indexType=`；中国港口协会是转载镜像，波罗的海 BDI 本机被 WAF 拦。
- **要航班 ADS-B 轨迹、航班正常率或铁路月度细项** → `aviation-rail-ops.md`：实时轨迹走 OpenSky 匿名 API（bbox + 400 credits/日），正常率看中国民航网月度统计，铁路月度/公报与城轨年报的入口仍以 `rail-aviation.md` 为准（本卡只补新接口）。
- **要开发区/园区名录（经开区·高新区·自贸区·综保区·边境合作区）或经开区考核排名** → `development-zones.md`：名录以商务部外资司导航页 + 发改委《2018 年版开发区审核公告目录》PDF 为骨架，考核排名取 `fdi.mofcom.gov.cn` 附件 PDF；高新区名单在火炬中心（本机不可达），海关特殊监管区域名单在海关总署 `zms`（本机 412）。
- **要土地出让公告/成交公示原文或清单、供地节奏** → `land-market.md`：全国先打 `api.landchina.com` 的 `tGygg/transfer/list`+`/detail`、`tCjgs/deal/list`+`/detail`（**POST + JSON body**，成交与统计接口较慢）；省级独立公告只有江苏省厅 JSP action 本机可直取，浙江/广东为 JS/SPA，拿不到就回落土地市场网同宗地公告。
- **要 70 城房价指数、房地产开发投资与销售、公积金年报、房企销售榜** → `realestate.md`：房价指数与投资销售走 `../stats/`（`nbs-api-skills.md` 常量 + `data.stats.gov.cn.md` 取数），公积金年报取住建部 `api-gateway` 附件或 gov.cn 的 `P0*.pdf`，房企榜单看中指云/克而瑞（明细需注册/付费）。
- **抓取姿势**：本层多数站**只认 http + 桌面 UA**（`caam`/`sasac`/`fangchan`/`clii` 的 https 会超时、证书不匹配或拒绝连接）；列表页多为「栏目 + `list_N.html`」或「年月目录」，先取栏目首页再归纳 URL 规律。

## 相关

- 部委行业运行数据（工信部统计分析、消费品/原材料/装备工业司口径）：[`../stats/ministry-stats.md`](../stats/ministry-stats.md)。
- 年鉴/数表的订阅库（知网经济社会大数据、EPS、中经网/国研网）：[`../stats/cnki-data.md`](../stats/cnki-data.md)、[`../stats/epsnet.md`](../stats/epsnet.md)、[`../stats/cei-drc.md`](../stats/cei-drc.md)。
- 央企/行业龙头的财务与债券披露（补协会口径的空白）：[`../business/chinabond.com.cn.md`](../business/chinabond.com.cn.md)、[`../business/cninfo.com.cn.md`](../business/cninfo.com.cn.md)。
- 企业主体核验（协会会员名单反查）：[`../gov/gsxt.md`](../gov/gsxt.md)。
- 上游总表与用法：仓库根 `SKILL.md`。
