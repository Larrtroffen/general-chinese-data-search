# finance/ —— 金融、财政与外汇数据源

本层收录**货币、外汇、银行保险、证券基金、期货贵金属**的官方与半官方统计/披露源，以及**财政预决算、税收、地方政府债券**的公开入口：央行调查统计口径、外汇局国际收支与外债、金融监管总局银行业保险业统计、行业协会（基金/证券/期货/交易商）与清算机构、支付体系统计与支付/银行业协会、期货与黄金交易所行情、财政部与税务总局数据。企业公告、交易所证券统计、货币市场行情见 `../business/`，本层不重复。

## 文件一览

| 文件 | 来源 | 用途/何时用 | 状态 |
|---|---|---|---|
| `pbc.gov.cn.md` | 中国人民银行·调查统计司 | 央行口径社融/货币供应/信贷收支/金融市场统计（年度 xls/pdf 直下） | ✅ 免登录直下 |
| `safe.gov.cn.md` | 国家外汇管理局 | 外汇储备/国际收支/国际投资头寸/外债/结售汇/汇率中间价 xlsx | ✅ 免登录直下 |
| `nfra.gov.cn.md` | 国家金融监督管理总局 | 银行业保险业统计（总资产/不良/保费）与监管公示 | ⚠️ 需浏览器 |
| `amac.org.cn.md` | 中国证券投资基金业协会 | 公募/私募资管规模、产品数（季度 JSON 接口） | ✅ JSON 接口 |
| `sac.net.cn.md` | 中国证券业协会 | 证券公司经营数据与行业统计 | ❌ 停机维护 |
| `shclearing.com.cn.md` | 银行间市场清算所（上清所） | 银行间债券发行披露 + 清算托管业务数据 | ⚠️ 统计需浏览器 |
| `cfachina.org.md` | 中国期货业协会 | 全国期货市场成交额、期货公司经营数据（JSON 检索） | ✅ JSON 接口 |
| `futures-exchanges.md` | 五家期货交易所 | 逐合约日行情/成交持仓排名/仓单（中金所 CSV 直链） | ⚠️ 部分 WAF |
| `sge.com.cn.md` | 上海黄金交易所 | 黄金白银现货/延期合约日行情（HTML 表） | ✅ 日期直取 |
| `nafmii.org.cn.md` | 银行间市场交易商协会 | 债务融资工具发行/主承/CRMW 统计（PDF） | ✅ PDF 直链 |
| `fiscal-open.md` | 财政部 / 各省财政厅 | 中央·部门·省级政府预决算原文（四本账、转移支付、三公） | ✅ 免登录直下 |
| `chinatax.md` | 国家税务总局 | 税收统计、分税种/分地区税收、《中国税务年度报告》 | ✅ HTML/PDF |
| `localgov-debt.md` | 中国地方政府债券信息公开平台 | 地方债限额/余额/发行偿还、逐只债券信息（JSON API） | ✅ JSON 接口 |
| `lgfv-platforms.md` | 中债 / 评级机构 / 审计署 / 财政部·省财政厅 | 城投口径：评级报告、政府性债务审计、债务限额余额（抽查 3 省） | ⚠️ 部分 WAF/需浏览器 |
| `bond-market-stats.md` | 上交所 / 深交所 / 中债 / 财政部债务管理司 | 债券市场统计补充入口：交易所成交、中债月报、地方债月度 | ✅ 免登录 |
| `payment-clearing.md` | 央行支付结算司 / 支付清算协会 / 网联 / 银联 | 支付体系季度报告、支付产业年报、银联新闻 JSON | ⚠️ 网联需浏览器 |
| `banking-industry.md` | 中国银行业协会 / 央行 / 金融监管总局 | 银行业百强与发展报告、区域金融运行报告、外资银行名录 | ✅ 免登录直下 |
| `insurance.md` | 中国保险行业协会 / 保险信息披露系统 / 精算师协会 | 保险业统计、信息披露（11 类栏目）、交强险经营、行业指数 | ✅ 接口可用 |
| `actuarial.md` | 精算师协会 / 保险保障基金 / 保险学会 | 精算研究、保障基金规模与名单、保险期刊（1980–2026） | ✅ 可抓 |

## 选路

- **要货币/信贷/社融的央行口径** → `pbc.gov.cn.md`：走「统计数据 → {年份} → 主题页」，取行尾 `xlsx`（社融增量/存量、货币统计概览、信贷收支表、金融市场、CGPI）；**主题页 URL 逐年不同**（新年份用 slug、旧年份用数字 ID），一律从 `/116319/` 解析。
- **要外汇储备/国际收支/外债** → `safe.gov.cn.md`：门户「统计数据」下拉 18 个专题，时间序列页给 `…/file/file/{YYYYMMDD}/{md5}.xlsx` 直链；汇率中间价与各币种折算率也在此。
- **要银行业保险业总量与不良/保费** → `nfra.gov.cn.md`：栏目是 AngularJS SPA，`/cn/static/data/*` 匿名 403，须浏览器（`../tools/agent-browser.md`）；历史口径跨银保监会改制，注意断裂。
- **要公募/私募/资管规模** → `amac.org.cn.md`：直接打 `POST /portal/front/home/findAssetsManageIndustry` 与 `getAllTimes`（匿名 JSON，季度）；产品/私募备案明细去子站 `gs.amac.org.cn`。
- **要期货全市场月度成交额** → `cfachina.org.md` 的 `GET /qx-search/api/wcmSearch/searchDocsByProgram?programName=月度交易数据`（JSON 正文含数字）；**要逐合约日行情/持仓/仓单** → `futures-exchanges.md`（中金所 CSV 免 JS，上期所/广期所需浏览器，大商所/郑商所 412）。
- **要银行间债券（债务融资工具）发行与承销统计** → `nafmii.org.cn.md`（PDF）；**要发行披露原文与清算托管数据** → `shclearing.com.cn.md`（披露页可抓，业务数据需浏览器）；国债/地方债与收益率曲线去 `../business/chinabond.com.cn.md`。
- **要黄金/白银行情** → `sge.com.cn.md`：`GET /sjzx/quotation_daily_new?start_date=&end_date=` 直出 HTML 表（现货 + T+D 延期，含成交量/持仓/交收）。
- **券商行业数据** → `sac.net.cn.md`（2026-10-07 前停机维护）；替代走巨潮（`../business/cninfo.com.cn.md`）与交易所市场统计。
- **要中央/部门/省级预决算原文与转移支付** → `fiscal-open.md`：「中央预决算公开平台 → 分层级 → 按年列表 → 附件」；省级是各家 CMS（路径逐年改版，先 probe）。
- **要税收收入与税务年报** → `chinatax.md`：总局「税收统计」栏目 + 年度报告 PDF；注意**税务口径 ≠ 财政口径**（`fiscal-open.md` 的一般公共预算税收）。
- **要地方政府债券限额/余额/发行明细** → `localgov-debt.md`：数据在 `www.governbond.org.cn:4443/api/loadBondData.action`（非标端口 GET JSON），页面可导出 Excel。
- **要城投债/地方政府融资平台口径** → `lgfv-platforms.md`：无官方「城投名单」——评级报告走中诚信匿名 JSON（`website-api.ccxi.com.cn/admin/content/rating/page`）/联合资信 PDF 直链（东方金诚本机被 WAF 拦）；中债城投债估值与曲线见 `../business/chinabond.com.cn.md`；2013 年全国政府性债务审计原文官网已下线，用省级审计厅转载；城投主体名单与城投债标签只能上商业库（Wind/企业预警通/DM）。
- **要债券市场统计汇总** → `bond-market-stats.md`：上交所 `bond.sse.com.cn`（现券交易月报/中证估值）、深交所 `market/bond/*`（成交概况/可转债转股）、中债统计月报（JS 渲染）、财政部债务管理司月度地方债数据；交易商协会与上清所见同层卡。
- **要支付体系运行数字（央行口径）** → `payment-clearing.md`：支付结算司「支付体系运行总体情况」列表 → 详情页**只挂 PDF**（数字全在 PDF，正文为空）；协会 `pcac.org.cn` 镜像同期报告并出《中国支付产业年报》；银联新闻走 `unionpay.com/upowweb/news/getNewsList`（JSON）；**网联官网数据文件 `403`，仅浏览器**。
- **要银行业行业级数据/榜单与名录** → `banking-industry.md`：中银协 `china-cba.net`（百强名单、年度发展报告、理财指数 docx）、央行《中国区域金融运行报告》栏目（2004–2024，一省一 PDF）；上市银行年报走 `../business/cninfo.com.cn.md`；外资银行名录用金融监管总局 `docfile` 静态 PDF（法人名单 + 外国及港澳台银行分行名单，绕开 SPA WAF）。

## 相关

- 债券/货币市场行情、交易所证券统计、企业公告与商业库：[`../business/`](../business/README.md)（`chinabond.com.cn.md` 中债、`chinamoney.com.cn.md` 外汇交易中心、`csrc.gov.cn.md` 证监会、`sse.com.cn.md` / `szse.cn.md`）。
- 宏观统计数值、部委统计总表与年鉴：[`../stats/ministry-stats.md`](../stats/ministry-stats.md)（人行/财政部行）、[`../stats/data.stats.gov.cn.md`](../stats/data.stats.gov.cn.md)、[`../regional/provincial-yearbooks.md`](../regional/provincial-yearbooks.md)。
- 需浏览器的 JS/加密站统一用：[`../tools/agent-browser.md`](../tools/agent-browser.md)。
- 上游总表与用法：仓库根 `SKILL.md`。
