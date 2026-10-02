# pbc.gov.cn —— 央行调查统计口径数据

- 去哪找：调查统计司 `https://www.pbc.gov.cn/diaochatongjisi/116219/index.html`；**统计数据（年度总入口）** `https://www.pbc.gov.cn/diaochatongjisi/116219/116319/index.html`；最新年度 `https://www.pbc.gov.cn/diaochatongjisi/116219/116319/2026ntjsj/index.html`。
- 什么时候用：要**央行口径**的社会融资规模（增量/存量）、货币供应量（M0/M1/M2）、金融机构信贷收支表、金融业机构资产负债统计、金融市场统计、金融账户、企业商品价格（CGPI）指数、景气调查指数；做货币/信贷/社融/银行资产负债表研究。
- 怎么搜：三层目录——`统计数据` → `{年份}年统计数据` → 主题页。主题页是一个表格，每行数据尾部给 `htm / xls / pdf` 三个附件，链接形如 `https://www.pbc.gov.cn/diaochatongjisi/attachDir/{YYYY}/{MM}/{时间戳}.{ext}`（时间戳不可猜，**必须从主题页 HTML 解析**）。结果形态：HTML 表格 + xlsx/pdf 附件，均可直下。
- 覆盖：1999–2026 年度节点（每年 6–8 个主题）；社融增量/存量、货币统计概览、信贷收支、金融市场、金融账户、CGPI、景气指数；全国口径；附件按发布日滚动更新。
- 门槛：无（免登录、无验证码）。
- 实测：2026-10-03，macOS arm64 curl 8.x，桌面 UA、`-L`、20s 超时——`GET /diaochatongjisi/116219/index.html` `200/57,168 B`；`GET …/116319/index.html` `200/89,073 B`（含 1999–2026 全部年度节点）；`GET …/116319/2026ntjsj/index.html` `200/34,997 B`（6 个主题）；`GET …/2026ntjsj/shrzgm/index.html` `200/26,144 B`，正文含 `…/attachDir/2026/09/2026091418125322850.xlsx`、`…/2026091418130886928.pdf`、`…/2026091417323857622.htm`（仅解析链接，未下载本体）。`http://` 入口 301 → `https://`。
- 上游：`https://www.pbc.gov.cn/diaochatongjisi/116219/index.html`（中国人民银行调查统计司）。

## 细节

### 栏目结构（2026-10-03 实测）

| 栏目 | URL |
|---|---|
| 调查统计司 | `https://www.pbc.gov.cn/diaochatongjisi/116219/index.html` |
| 统计数据（年度总入口） | `https://www.pbc.gov.cn/diaochatongjisi/116219/116319/index.html` |
| 数据解读 | `https://www.pbc.gov.cn/diaochatongjisi/116219/116225/index.html` |
| 问卷调查 | `https://www.pbc.gov.cn/diaochatongjisi/116219/116227/index.html` |

### 年度主题页 slug（2026 年节点 `/116319/2026ntjsj/`）

| slug | 栏目 |
|---|---|
| `shrzgm` | 社会融资规模（增量统计表 / 存量统计表） |
| `hbtjgl` | 货币统计概览（货币供应量、储备货币） |
| `jryjgzcfztj` | 金融业机构资产负债统计 |
| `jrjgxdsztj` | 金融机构信贷收支统计 |
| `jrsctj` | 金融市场统计 |
| `qyspjgcgpizs` | 企业商品价格（CGPI）指数 |

- **2025 及更早年份**的主题页 URL 用**数字节点 ID**，不是 slug：如 2025 = `/116319/5570903/5570885/index.html`（社融）、`…/5570886/`（货币概览）；2024 = `/116319/5225358/5225359/` …；2007 年及以前无子主题（直接 `/116319/116369/index.html`）。
- 一行数据三件套：`htm`（网页版表）、`xls/xlsx`（可计算，优先）、`pdf`（定稿版）。

## 坑

1. **附件时间戳不可猜**：`attachDir/{年}/{月}/{YYYYMMDDHHMMSSmmm}.{ext}` 必须从主题页 HTML 抓，别按规律拼。
2. 主题页属性用**单引号**（`href='…'`），解析器要单/双引号都认；导航区也有大量 `href='…'` 噪声，按 `attachDir` 过滤最稳。
3. 年度主题 slug（`2026ntjsj/shrzgm`）与旧年份数字 ID 混用；**永远从 `/116319/` 列表页解析当层链接**，别套模板。
4. 利率/汇率等政策类数字**不在**本栏目：LPR、再贷款利率见货币政策司；Shibor、人民币汇率中间价、CFETS 指数走中国货币网（`../business/chinamoney.com.cn.md`）。
5. 央行口径的年度总表/公报另见 `../stats/ministry-stats.md`（人行行）；月度经济指标兜底用 `../stats/data.stats.gov.cn.md`。
6. 页面编码 UTF-8 为主，老页面可能 GB2312；抓正文按 `<meta charset>` 判定。
