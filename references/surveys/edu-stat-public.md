# edu-stat-public —— 教育部统计公报与教育统计数据

- 去哪找：
  - **教育发展统计公报**（逐年正文）`http://www.moe.gov.cn/jyb_sjzl/sjzl_fztjgb/`
  - **教育统计数据**（全国 + 分省，逐年）`http://www.moe.gov.cn/jyb_sjzl/moe_560/{年}/`，下分「全国基本情况」`…/{年}/quanguo/` 与「各地基本情况」`…/{年}/gedi/`
  - 栏目总入口「文献 · 数据资料」`http://www.moe.gov.cn/jyb_sjzl/`
- 什么时候用：要**教育部口径**的年度教育数字——各级各类学校数、在校生/招生/毕业生、专任教师、毛入学率/升学率、生师比、办学条件、教育经费；做教育研究、区域比较、写报告时替换年鉴/统计公报口径；关键词：教育事业发展统计公报、教育统计数据、分省教育统计、在校生数、毛入学率、生师比。
- 怎么搜：**① 公报**——进 `sjzl_fztjgb/` 列表取当期文号，正文 HTML（2016 年及以后 `./{YYYYMM}/t…html`，2015 年及以前在 `srcsite/A03/s180/moe_633/{YYYYMM}/t…html`）；**② 数据**——进 `moe_560/{年}/quanguo/`（或 `gedi/`）列表，表页为 `…/{年}/{quanguo|gedi}/{YYYYMM}/t{YYYYMMDD}_{id}.html`（HTML 表格，个别为附件）。改 URL 年份即可直取。站内检索 `https://so.moe.gov.cn/s?qt=<词>`（结果页 JS 渲染）。
- 覆盖：教育事业发展统计公报 **2006–2025**（2025 年公报 2026-07-06 发布）；教育统计数据 **1997–2024**；全国 + 分省（各地基本情况）；粒度=指标 × 学段 × 省份 × 年度。
- 门槛：**免费、免登录**；页面为 HTML 表格，部分表/附件为 PDF、xls/xlsx。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA：`http://www.moe.gov.cn/jyb_sjzl/sjzl_fztjgb/` → 200（23 499 B，列出 2006–2025 公报，2025 年公报 `./202607/t20260706_1442870.html`）；`http://www.moe.gov.cn/jyb_sjzl/moe_560/2024/` → 200（21 823 B，列出 1997–2024 年度入口）；`http://www.moe.gov.cn/jyb_sjzl/moe_560/2024/quanguo/` → 200（25 218 B，含 `./202603/t20260319_*.html` 表页链接）。
- 上游：中华人民共和国教育部政府门户网站 `http://www.moe.gov.cn/`。

## 细节

### URL 规律

- 公报：`http://www.moe.gov.cn/jyb_sjzl/sjzl_fztjgb/{YYYYMM}/t{YYYYMMDD}_{id}.html`（2016+）；更早在 `http://www.moe.gov.cn/srcsite/A03/s180/moe_633/{YYYYMM}/t…html`。
- 数据：`http://www.moe.gov.cn/jyb_sjzl/moe_560/{年}/quanguo/`、`…/{年}/gedi/`；表页 `…/{年}/quanguo/{YYYYMM}/t{YYYYMMDD}_{id}.html`。示例：2024 年全国基本情况表 `…/2024/quanguo/202603/t20260319_1431434.html`。
- 站内检索：`https://so.moe.gov.cn/s?qt=<关键词>`（200，JS 渲染结果页；`/api/search` 404，勿依赖）。

### 与其他卡的分工

- 部委统计**总表**（教育列 + 财政/卫生/交通等）：[`../stats/ministry-stats.md`](../stats/ministry-stats.md) —— 本卡只做教育统计的细节与 URL 模板，不重复其他部委。
- **机构名录与资质核实**（高校名单/学位授权点/科研机构/医疗机构）：[`../gov/edu-research-institutions.md`](../gov/edu-research-institutions.md)。
- 国家统计局宏观口径与年鉴接口：[`../stats/data.stats.gov.cn.md`](../stats/data.stats.gov.cn.md)、[`../stats/README.md`](../stats/README.md)。

## 坑

- 教育部 `https` 专栏页常 **302 跳到 http** 同路径；脚本加 `-L` 或用 `http://` 直取。
- **公报与统计数据是两套口径**：公报是「快报+年度」，统计数据模块是细化表格（分省/分类）；同一指标数值偶有差异，引用时写明取自哪一套。
- 老年度公报 URL 在 `srcsite/A03/s180/moe_633/`，路径与新版不同，别硬套年份模板。
- `so.moe.gov.cn` 检索页为 JS 渲染，命令行拿不到结果列表；需要全文检索时改用站点目录 + 页面内锚点。
- 分省数据的「各地基本情况」按年度发布，个别年份仅全国未含分省，先看目录页再取表。
