# banking-industry —— 银行业行业数据与名录

- 去哪找：
  - **中国银行业协会**：门户 `https://www.china-cba.net/`；行业报告 `https://www.china-cba.net/Index/lists/catid/358.html`；研究报告 `…/catid/268.html`；理财市场指数报告 `…/catid/279.html`（明细 `…/catid/280.html`）
  - **央行·《中国区域金融运行报告》**：`https://www.pbc.gov.cn/zhengcehuobisi/125207/125227/125960/126049/index.html`（2004–2024，年度，附分省 PDF）
  - **上市银行年报/公告**：巨潮 `../business/cninfo.com.cn.md`
  - **外资银行名录**：金融监管总局静态文件（`docfile` 域）——银行业金融机构法人名单、外国及港澳台银行分行名单（见「细节」）
- 什么时候用：要**银行业行业级数据与榜单**（中银协「中国银行业前100名单」/百强、年度《中国银行业发展报告》、《中国理财市场指数报告》）；要**分省金融运行**（各省存贷款、社会融资、金融生态）；要**上市银行年报/招股书**；要**外资法人银行与外国银行分行名录**。
- 怎么搜：
  - 中银协是自建 Java CMS：列表 `/Index/lists/catid/{栏目}.html`（翻页 `…/p/{n}.html`），文章 `/Index/show/catid/{栏目}/id/{文章}.html`；正文在 `<div id="neirong">`，附件在 `/Uploads/ueditor/file/{YYYYMMDD}/{哈希}.{docx|xlsx|pdf}`。
  - 区域金融运行报告：栏目页 → 年度文章 → 页内**一省一 PDF**（2024 报告含 33 个 PDF：全国全文 + 各省摘要）。
  - 外资银行名录：总局 `docfile` 静态件直下，`/chinese/docfile/{YYYY}/{哈希}.pdf`；栏目入口是信息公开 SPA（需浏览器，见 `nfra.gov.cn.md`）。
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS --compressed -A "$UA" 'https://www.china-cba.net/Index/lists/catid/358.html'   # 行业报告
  curl -sS --compressed -A "$UA" 'https://www.pbc.gov.cn/zhengcehuobisi/125207/125227/125960/126049/index.html'  # 区域金融运行报告
  curl -sSI -A "$UA" 'https://www.nfra.gov.cn/chinese/docfile/2025/9f4f220df20d4e1badab4ef406674f3b.pdf'         # 外国及港澳台银行分行名单
  ```
  结果形态：列表/文章 HTML 可直抓、正文静态；附件 PDF/docx/xlsx；总局名录 PDF 直下。
- 覆盖：中银协行业报告（百强名单、年度发展报告、城商行/农商行报告）与理财市场指数报告（2022–2026）；央行区域金融运行报告 2004–2024；上市银行公告/年报全量（走巨潮）；银行业金融机构法人名单与外国及港澳台银行分行名单（总局，半年/年度更新）。
- 门槛：中银协、央行、总局 `docfile` PDF = 免费免登录；总局栏目 SPA 需浏览器（静态件不受影响）。
- 实测：2026-10-03，macOS arm64 curl 8.x，桌面 UA，20s 超时，同主机 ≥1.5s 间隔：
  - `china-cba.net/` → `200/15,077 B`（`<title>中国银行业协会`）；`/Index/lists/catid/358.html` → `200/5,196 B`（3 条行业报告）；`/Index/lists/catid/279.html`、`/catid/280.html` → `200/5,384 B`（理财指数按年）；`/Index/show/catid/280/id/46763.html` → `200/7,877 B`，附件 `/Uploads/ueditor/file/20260616/6a30ad0904c3b.docx` 等 6 个 docx；`/Index/show/catid/14/id/45489.html`（2025 百强榜）→ `200`，正文静态 `#neirong`、无附件；翻页 `/Index/lists/catid/358/p/2.html` → `200/5,055 B`。
  - `pbc.gov.cn/zhengcehuobisi/125207/125227/125960/126049/index.html` → `200/11,726 B`（`<title>区域金融运行报告`，条目 2004–2024）；2024 文章 `…/126049/5415491/73300d7391b844e5958cfd6fd8d18f59/index.html` → `200/9,752 B`，含 33 个 PDF（锚文本为「《中国区域金融运行报告（2024）》」「《北京市金融运行报告（2024）》摘要」…）。
  - `nfra.gov.cn/chinese/docfile/2025/e80bc363856b4032901e40a79d6a8486.pdf`（银行业金融机构法人名单）→ `200 application/pdf 1,249,351 B`；`…/9f4f220df20d4e1badab4ef406674f3b.pdf`（外国及港澳台银行分行名单）→ `200 application/pdf 132,146 B`。
- 上游：中国银行业协会 `china-cba.net`；中国人民银行（货币政策司栏目）`pbc.gov.cn`；国家金融监督管理总局 `nfra.gov.cn`；上市公司公告 `cninfo.com.cn`。

## 细节

### 一、中国银行业协会栏目

| 栏目 | URL | 内容 |
|---|---|---|
| 行业报告 | `/Index/lists/catid/358.html` | 《中国银行业发展报告》、《城市商业银行30年发展报告》、农村中小银行行业报告 |
| 研究报告 | `/Index/lists/catid/268.html` | 专题研究 |
| 理财市场指数报告 | `/Index/lists/catid/279.html` → `/Index/lists/catid/280.html` | 按年份（2022-2023 / 2024 / 2025 / 2026） |
| 百强名单（协会动态） | `/Index/show/catid/14/id/{id}.html` | 「中国银行业前100名单」（按核心一级资本净额排序） |

- 文章正文容器 `#neirong`；附件在 `/Uploads/ueditor/file/{YYYYMMDD}/{哈希}.{ext}`（理财指数为 docx）。
- 2025 百强榜新闻稿（`/Index/show/catid/14/id/45489.html`）只给榜单说明，`#neirong` 内**无表无附件**；明细排名常由财经媒体转载成表。

### 二、央行《中国区域金融运行报告》

| 项 | 值 |
|---|---|
| 栏目 | `https://www.pbc.gov.cn/zhengcehuobisi/125207/125227/125960/126049/index.html` |
| 覆盖 | 2004–2024（年度） |
| 文章形态 | `…/126049/{ID}/{哈希}/index.html`（2021 及更早为 `…/126049/1260xx/{ID}/index.html`） |
| 附件 | 页内一省一 PDF，锚文本标省份，如「《北京市金融运行报告（2024）》摘要」 |
| 2024 另见入口 | `https://www.pbc.gov.cn/goutongjiaoliu/113456/113469/2025092212554119884/index.html` |

### 三、外资银行名录（金融监管总局静态文件）

| 名单 | 2025 版 PDF（本机实测直下） |
|---|---|
| 银行业金融机构法人名单 | `https://www.nfra.gov.cn/chinese/docfile/2025/e80bc363856b4032901e40a79d6a8486.pdf` |
| 外国及港澳台银行分行名单 | `https://www.nfra.gov.cn/chinese/docfile/2025/9f4f220df20d4e1badab4ef406674f3b.pdf` |

- 2024 版（来源为公开检索、未逐个 HEAD）：法人名单 `…/docfile/2024/e63ebdc69ab94e5d91eaf6b46151a552.pdf`；分行名单 `…/docfile/2024/8433fa45825243b782a33ec68a18978e.pdf`。
- 哈希文件名不可猜，从栏目或搜索结果取；`docfile` 静态件走 nginx，**不受** `nfra.gov.cn.md` 所述 `/cn/static/data/*` WAF 影响。
- 上海监管局另有「直接监管的银行业机构名单」等同域 PDF（`big5.nfra.gov.cn` 亦镜像）。

## 坑

1. **中银协百强榜不给可计算附件**：新闻稿 `#neirong` 只有文字说明，无表格、无 xlsx；排名数字须从媒体转载或逐条新闻整理，别假设有附件。
2. **中银协列表分页写法**：翻页为 `/Index/lists/catid/{id}/p/{n}.html`（实测 200）；但多数栏目条目很少（行业报告仅 3 条），常一页到底。
3. **区域金融运行报告是「一省一 PDF」**：一篇文章挂 20–33 个附件，文件名为时间戳，须按锚文本（省份名）对应，不能只看顺序。
4. **总局名录「栏目页与文件分离」**：栏目页是 SPA（`/cn/static/data/*` 匿名 403，见 `nfra.gov.cn.md`），但 `chinese/docfile/*.pdf` 静态可直下——不要因栏目打不开就放弃名单。
5. **上市银行年报不在本卡取**：年报/招股书/问询函走 `../business/cninfo.com.cn.md`（巨潮 JSON + PDF 直链）；本卡只给协会/央行/总局的**行业级与名录级**数据。
6. **理财市场指数报告附件是 docx**（非 PDF/xlsx），需 docx 解析；文件名时间戳对应发布日。
