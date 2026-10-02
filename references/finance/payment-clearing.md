# payment-clearing —— 支付体系统计与行业报告

- 去哪找：
  - **央行·支付结算司**：支付体系 `https://www.pbc.gov.cn/zhifujiesuansi/128525/index.html`；统计数据与分析 `https://www.pbc.gov.cn/zhifujiesuansi/128525/128545/index.html`；**支付体系运行总体情况**（季度/年度，列表）`https://www.pbc.gov.cn/zhifujiesuansi/128525/128545/128643/index.html`
  - **中国支付清算协会**：门户 `https://www.pcac.org.cn/`；行业数据 `http://www.pcac.org.cn/eportal/ui?pageId=595055`；行业报告 `http://www.pcac.org.cn/eportal/ui?pageId=595143`
  - **网联清算** `https://www.nucc.com/`；**中国银联** `https://www.unionpay.com/`
- 什么时候用：要**央行口径的支付体系运行数字**（非现金支付业务量、银行卡/贷记转账/票据、支付系统业务量、特约商户与受理终端、电子支付）；要《中国支付产业年报》《中国银行卡产业发展报告》等**行业报告**；做支付清算、银行卡、第三方支付、移动支付、预付卡研究。
- 怎么搜：两条主线——
  ① **央行季度报告**：`支付体系运行总体情况` 列表页每行一条（标题含「YYYY年第N季度」），详情页 URL 形如 `…/128643/{时间戳或旧ID}/index.html`；**正文为空，数字全在 PDF 附件**，须从详情页 HTML 解析 `.pdf` 链接直下。
  ② **协会 eportal**：列表与文章统一走 `/eportal/ui?pageId={页}&articleKey={文章}&columnId={栏目}`；附件形如 `/eportal/fileDir/pcac/resource/cms/article/{columnId}/{articleKey}/{时间戳}.pdf`。
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS --compressed -A "$UA" 'https://www.pbc.gov.cn/zhifujiesuansi/128525/128545/128643/index.html'  # 央行季度列表
  curl -sS --compressed -A "$UA" 'http://www.pcac.org.cn/eportal/ui?pageId=595055'                     # 协会·行业数据
  curl -sS --compressed -A "$UA" 'http://www.pcac.org.cn/eportal/ui?pageId=595143'                     # 协会·行业报告
  ```
  银联另有新闻 JSON 接口（见「细节」）。结果形态：列表/文章 HTML 可直抓 + PDF 附件；银联新闻为 JSON。
- 覆盖：央行季度/年度报告列表首页含 2022 Q1–2026 Q2（更早年份翻页方式未实测）；协会「行业数据」镜像支付体系报告（本机见 2023–2026）；协会「行业报告」《中国支付产业年报》2019–2023；银联新闻列表合计 1,183 条（含《中国银行卡产业发展报告》发布稿）。全国口径。
- 门槛：央行、协会 = 免费免登录；银联新闻 JSON = 免登录；**网联官网为 Vue SPA 且数据 JSON 返回 `403 denied by IP ACL`，仅浏览器**。
- 实测：2026-10-03，macOS arm64 curl 8.x，桌面 UA，20s 超时，同主机 ≥1.5s 间隔：
  - `pbc.gov.cn/zhifujiesuansi/128525/index.html` → `200/67,739 B`（`<title>支付结算司`）；`…/128545/index.html` → `200/36,613 B`（`统计数据与分析`）；`…/128545/128643/index.html` → `200/39,496 B`（列表，含 2022Q1–2026Q2）；详情 `…/128643/2026090219081087604/index.html` → `200/26,530 B`，正文无数据、仅附件 `…/2026090219081087604/2026090219072950269.pdf`；`…/128643/index_2.html` → `404`。
  - `pcac.org.cn/eportal/ui?pageId=595055` → `200/41,809 B`（行业数据，含 2013–2026 支付体系报告）；`?pageId=595143` → `200/32,231 B`（《中国支付产业年报》2019–2023）；文章 `?articleKey=623166&columnId=595055&pageId=598168` → `200/34,402 B`，附件 `…/article/595055/623166/2025022114470536223.pdf`。
  - `nucc.com/` → `200/1,006 B`（Vue 壳，`<title>网联清算有限公司`）；`/env.js` → `200/1,444 B`；`/webGlobal.json`、`/article/home.json` → `403`（`denied by IP ACL = blacklist`，Tengine/CDN）。
  - `unionpay.com/upowweb/news/getNewsList?menuId=01017&page=1`（带 Referer）→ `200/21,401 B` JSON，`state=true`、`pageModel.total=1183`。
- 上游：中国人民银行支付结算司 `pbc.gov.cn`；中国支付清算协会 `pcac.org.cn`；网联清算有限公司 `nucc.com`；中国银联 `unionpay.com`。

## 细节

### 一、央行「支付体系运行总体情况」

| 页面 | URL |
|---|---|
| 支付结算司 | `https://www.pbc.gov.cn/zhifujiesuansi/128525/index.html` |
| 统计数据与分析 | `https://www.pbc.gov.cn/zhifujiesuansi/128525/128545/index.html` |
| 支付体系运行总体情况（列表） | `https://www.pbc.gov.cn/zhifujiesuansi/128525/128545/128643/index.html` |
| 详情页（例：2026Q2） | `…/128643/2026090219081087604/index.html` → 附件 `…/2026090219081087604/2026090219072950269.pdf` |

- 详情页末段**新旧混杂**：新条目为 `YYYYMMDDHHMMSS…` 时间戳，旧条目为数字 ID 或哈希，一律从列表页解析，别套模板。
- 报告正文**不落 HTML**，数据仅在 PDF；PDF 内含非现金支付业务量、银行卡、票据、支付系统等分项表。
- 列表含季度报告与「YYYY年支付体系运行总体情况」年度报告两类。

### 二、中国支付清算协会（eportal CMS）

| 栏目 | URL |
|---|---|
| 行业数据（columnId=595055） | `http://www.pcac.org.cn/eportal/ui?pageId=595055` |
| 行业报告（columnId=595143） | `http://www.pcac.org.cn/eportal/ui?pageId=595143` |
| 行业研究（columnId=595052） | `http://www.pcac.org.cn/eportal/ui?pageId=595052` |
| 会员业务统计系统 | `https://mbuss.pcac.org.cn/`（会员登录） |

- 文章：`/eportal/ui?pageId={页}&articleKey={key}&columnId={col}`；附件：`/eportal/fileDir/pcac/resource/cms/article/{col}/{key}/{时间戳}.{pdf|xls}`。
- 「行业数据」= 央行季度报告的**协会镜像**；「行业报告」= 《中国支付产业年报》等自家年报（2019–2023）。

### 三、银联新闻 JSON 接口

```bash
curl -sS --compressed -A "$UA" -H 'Referer: https://www.unionpay.com/upowhtml/cn/templates/newsList-01017/newsList-01017.html?menuId=01017' \
  'https://www.unionpay.com/upowweb/news/getNewsList?menuId=01017&page=1'
```

- 返回 `{state:true, menuId, pageModel:{total, pageSize:6, endPgNo, results:[{contentHtmlPath, synopsis, …}]}}`；`contentHtmlPath` 拼站内相对路径即新闻稿页，《中国银行卡产业发展报告》发布稿在内。无结构化统计数字，只有新闻稿文本。

## 坑

1. **央行详情页正文是空的**：`支付体系运行总体情况` 页面只剩壳，数字全在 PDF 附件；脚本别按「页面无表格」判空，要解析 `.pdf` 链接。
2. **网联官网 curl 拿不到数据**：`/webGlobal.json`、`/article/home.json` 返回 `403 denied by IP ACL = blacklist`（Tengine/CDN），而 HTML/JS 可正常取——数据文件仅对浏览器放行，须 `../tools/agent-browser.md`。
3. **协会 eportal 的 pageId 是渲染层参数，不等于栏目**：同一栏目不同文章 `pageId` 可能不同（文章常用 `598168`/`598368`/`598261`），**以 `columnId` 判栏目**更稳。
4. **网联无公开业务统计**：官网只有公司新闻/简介路由，未见支付业务量等公开数据；网联的支付业务数字不在本源，别与央行口径混用。
5. **央行季度报告口径 ≠ 协会年报口径**：前者是支付结算司统计，后者是协会产业年报（含调研汇编），引用时注明出处。
6. 与 `pbc.gov.cn.md` 分工：**本卡** = 支付结算司「支付体系」；`pbc.gov.cn.md` = 调查统计司社融/货币/信贷/金融市场。同域不同司，勿混。
