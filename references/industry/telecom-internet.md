# telecom-internet —— 通信业与互联网官方统计

- 去哪找：工信部「通信业」`https://www.miit.gov.cn/gxsj/tjfx/txy/index.html`、「互联网」`https://www.miit.gov.cn/gxsj/tjfx/hlw/index.html`、「年度数据」`https://www.miit.gov.cn/gxsj/tjfx/ndsj/index.html`（列表均 JS 渲染，真数据走 `api-gateway` 接口，见「细节」）；CNNIC 统计报告库 `https://cnnic.cn/6/86/88/index.html`（`www.cnnic.net.cn` 同源镜像）；中国互联网协会「发展报告」`https://www.isc.org.cn/category/7356.html`。
- 什么时候用：要**电信业务总量/收入、移动电话与固定宽带用户、5G/千兆用户、移动数据流量、短信量**；通信业月度运行情况、**通信业统计公报**、通信业主要指标完成表；互联网和相关服务业收入；**网民规模/普及率/网民结构**（CNNIC 报告）；中国互联网企业百强/综合实力指数。
- 怎么搜：分三路——
  - **工信部列表**：栏目页只是 JS 壳，列表由 jpaas 接口吐 JSON。用页面里的 `webId/tplSetId/pageId` 发 GET（`pageNo` 翻页，每页 24 条，返回体带 `count` 总数）：
    ```bash
    UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    curl -s -A "$UA" -G \
      --data-urlencode 'parseType=buildstatic' \
      --data-urlencode 'webId=8d828e408d90447786ddbe128d495e9e' \
      --data-urlencode 'tplSetId=209741b2109044b5b7695700b2bec37e' \
      --data-urlencode 'pageType=column' \
      --data-urlencode 'tagId=右侧内容' \
      --data-urlencode 'editType=null' \
      --data-urlencode 'pageId=1434685f08314ae8ae78f78b6a5a7915' \
      'https://www.miit.gov.cn/api-gateway/jpaas-publish-server/front/page/build/unit'
    # → {"success":true,"data":{"html":"<li><a href=\"/gxsj/tjfx/txy/art/2026/art_….html\" …"}}
    ```
    `pageId` 逐栏目不同（见「细节」表），从栏目页 HTML 的 `<script id="…" … pageId='…'>` 里解析，别复用。
  - **文章 URL 规律**：`/gxsj/tjfx/{txy|hlw}/art/{YYYY}/art_{32位hex}.html`。「经济运行情况」= 正文＋图表（数字多在图片里）；「通信业主要指标完成情况（一）（二）」= **HTML 表格**（可机读）；年度「通信业统计公报」= 正文＋图。
  - **CNNIC**：报告库 `/6/86/88/index.html` … `index4.html`（共 4 页），详情页 `/n4/{YYYY}/{MMDD}/c88-{id}.html`，正文页内挂 PDF `/NMediaFile/{YYYY}/{MMDD}/MAIN{时间戳}{随机}.pdf`（路径含时间戳+随机串，必须从详情页解析）。结果形态：HTML 页 + PDF 直下。
  - **中国互联网协会**：分类页 `/category/7356.html`（发展报告）、`/category/7355.html`（企业综合实力/百强），条目即 `/article/{id}.html`。
- 覆盖：工信部通信业栏目 `count=816` 条（月/季/年，含 2026-08 最新月度运行情况、2026-01 发布的 2025 年统计公报、分季主要指标表、年度统计数据/通信统计年鉴入口）；CNNIC 统计报告第 43–57 次（2019-02 至 2026-02）+ 生成式 AI/数字消费/中小企业等专题报告；ISC 发展报告 2013–2026、企业综合实力 2014–2025。
- 门槛：无（三站均免登录、无验证码；CNNIC 与 ISC 报告 PDF 直下）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA、`-L`、20s 超时），逐条见「细节」。
- 上游：工业和信息化部运行监测协调局 `https://www.miit.gov.cn/gxsj/tjfx/index.html`；CNNIC `https://cnnic.cn/`；中国互联网协会 `https://www.isc.org.cn/`。

## 细节

### 工信部 jpaas 取数（2026-10-03 实测）

`webId=8d828e408d90447786ddbe128d495e9e`、`tplSetId=209741b2109044b5b7695700b2bec37e` 为「统计分析」栏目通用值。

| 子栏目 | 列表页 | `pageId` | 观察 |
|---|---|---|---|
| 通信业 | `/gxsj/tjfx/txy/index.html` | `1434685f08314ae8ae78f78b6a5a7915` | ✅ `count=816`、24 条/页；首条「2026年前7个月通信业经济运行情况」2026-08-28 |
| 互联网 | `/gxsj/tjfx/hlw/index.html` | `3047f3df89414d0ca8c6eef37a44088e` | ✅ 24 条/页；首条「2026年上半年互联网和相关服务业运行情况」 |
| 年度数据 | `/gxsj/tjfx/ndsj/index.html` | — | 页面内导航出现，未单独调接口 |
| 电子信息制造业 / 软件业 / 原材料 / 装备 / 消费品 | `/gxsj/tjfx/{dzxx,rjy,yclgy,zbgy,xfpgy}/index.html` | — | 同模板，`pageId` 各自不同 |

已实测正文（`200`）：`/gxsj/tjfx/txy/art/2026/art_5c99d65350f7452f999e8efcb1ee2d6a.html`（2025年通信业统计公报，26,866 B，含 1 个 `<table>`＋19 张图）；`/gxsj/tjfx/txy/art/2025/art_72e07f4c2cdb46f693f52d53d3ba612f.html`（2024年1－12月通信业主要指标完成情况（二），19,595 B，HTML 表：固定电话用户合计 16651 万户、移动电话用户合计 178960 万户…）。
另：列表页出现 `https://www.miit.gov.cn/txnj2024/tx_index.html`（2024年通信业年度统计数据，未单独实测）。

### CNNIC 统计报告页（`/6/86/88/index.html` 第 1 页，2026-10-03）

| 日期 | 详情页 | 报告 |
|---|---|---|
| 2026-02-05 | `/n4/2026/0304/c88-11549.html` | 第57次《中国互联网络发展状况统计报告》 |
| 2025-07-21 | `/n4/2025/0721/c88-11328.html` | 第56次 |
| 2025-01-17 | `/n4/2025/0117/c88-11229.html` | 第55次 |
| 2024-08-29 | `/n4/2024/0829/c88-11065.html` | 第54次 |
| 2024-03-22 | `/n4/2024/0322/c88-10964.html` | 第53次 |
| 2023-08-28 | `/n4/2023/0828/c88-10829.html` | 第52次 |
| 2023-03-02 | `/n4/2023/0303/c88-10757.html` | 第51次 |
| 2022-08-31 | `/n4/2022/0914/c88-10226.html` | 第50次 |
| 2022-02-25 | `/n4/2022/0401/c88-1131.html` | 第49次 |
| 2021-09-15 | `/n4/2022/0401/c88-1132.html` | 第48次 |
| 2021-02-03 | `/n4/2022/0401/c88-1125.html` | 第47次 |
| 2020-09-29 | `/n4/2022/0401/c88-1124.html` | 第46次 |
| 2020-04-28 | `/n4/2022/0401/c88-1088.html` | 第45次 |
| 2019-08-30 | `/n4/2022/0401/c88-1116.html` | 第44次 |
| 2019-02-28 | `/n4/2022/0401/c88-838.html` | 第43次 |

同页还有《数字消费发展报告（2025）》`/n4/2025/1226/c88-11445.html`、《生成式人工智能应用发展报告（2025）》`/n4/2025/1021/c88-11391.html` 等专题报告。翻页：`/6/86/88/index2.html`…`index4.html`（`PageNo=4`）。
PDF 实例：第57次 → `/NMediaFile/2026/0304/MAIN1772588317069TUXN3827X8.pdf`；第56次 → `/NMediaFile/2025/0730/MAIN1753846666507QEK67ZS9DH.pdf`。

### 中国互联网协会报告

`/category/7356.html`：《中国互联网发展报告2026》`/article/29644081141641216.html`（2026-07-10）、2025 `/article/25680490231623680.html`、2024 `/article/21390688419704832.html`、2023 `/article/17333342358990848.html`、2022 `/article/13848794657714176.html`，再早为 `/article/{40203,37989,37331,36441}.html`（2018–2021）。
`/category/7355.html`：《中国互联网企业综合实力指数（2024）》`/article/22500319628488704.html`、2022 `/article/14404172954071040.html`、2021 `/article/109057518522838505.html`、2020 `/article/38550.html`、2019 百强 `/article/36993.html`。

## 坑

1. **工信部栏目页 curl 只拿到 ~5 KB JS 壳**，不调 `api-gateway` 接口会被误判为「空栏目」；接口必须带 `Referer` 有时更稳，返回 JSON 里的 `html` 字段才是列表。
2. `pageId` 逐栏目不同，**必须从栏目页 HTML 解析**；`tplSetId`/`webId` 在「统计分析」下通用。
3. 通信业「统计公报」的分项数字多为**图片**，要机读数字请取同栏目「通信业主要指标完成情况（一）（二）」的 HTML 表，或「年度数据」与通信统计年鉴。
4. CNNIC PDF 路径 `/NMediaFile/{年}/{月日}/MAIN{毫秒时间戳}{随机}.pdf` **不可拼**；2021 年及以前的报告被重挂到 `/n4/2022/0401/c8x-*.html`，年份目录≠发布年。
5. 子域 `www3.cnnic.cn` 已废（302→404），用主域 `cnnic.cn` 或 `www.cnnic.net.cn`。
6. 中国互联网协会站规范域名为 `https://www.isc.org.cn`（`:443` 直连），早期简版直链 `http://isc.org.cn/download/*.pdf`（2013–2015）为旧站路径，**未本机验证**，可能已失效。
7. 中国互联网发展报告 2016–2026 多为**发布会新闻**，正文 PDF 需从 `/article/{id}.html` 内解析；部分年份（2016–2017）只有招商/征订通知，无免费全文。
