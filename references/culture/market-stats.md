# market-stats —— 文化市场统计公报与票房入口

- 去哪找：**中国电影数据信息网**（国家电影专资办）`https://www.zgdypw.cn/sc/sjbg/`（票房周报/月报）、`https://www.zgdypw.cn/sc/scxx/`（新片预告、新建影院）；**国家电影局** `https://www.chinafilm.gov.cn/`；**国家新闻出版署·统计信息** `https://www.nppa.gov.cn/xxgk/fdzdgknr/tjxx/`（新闻出版统计公报 PDF）；**文化和旅游部·统计信息** `https://zwgk.mct.gov.cn/zfxxgkml/447/465/index_3081.html`、**公报** `https://zwgk.mct.gov.cn/zfxxgkml/503/506/index_3081.html`；**广电总局** 年度统计公报 `https://www.nrta.gov.cn/art/2026/5/13/art_113_73265.html`；**中国网络视听协会** `http://www.cnsa.cn/`；**中国演出行业协会** `https://www.capa.com.cn/`。
- 什么时候用：要**电影票房**（周/月/档期、场次、人次、新建影院）；要**新闻出版、图书发行业**统计公报与产业分析报告；要**文化产业/旅游业**统计公报、季度出游数据、文物与非遗可视化数据；要**广播电视与网络视听**行业总收入、广告收入、CVB 收视规模；要**演出市场**年度收入与票房。
- 怎么搜：多为「列表页 → 详情页」静态结构，改 URL 年份/日期即可直取，公报常为 **PDF** 或 **HTML 正文**：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  # 出版统计公报（PDF 直下；P{17位} 文件名不可猜，须从列表页解析）
  curl -sL -A "$UA" -o nppa-2024.pdf 'https://www.nppa.gov.cn/xxgk/fdzdgknr/tjxx/202512/P020251218382424228218.pdf'
  # 文旅部数据服务栏目（Nuxt SPA）背后的匿名 JSON
  curl -sL -A "$UA" 'https://sjfw.mct.gov.cn/api/marker/province/list'
  ```
  结果形态：**HTML（正文/图表图片）+ PDF**；文旅部数据服务为 **JSON**；演出协会、开卷等为 **SPA（需浏览器）**。
- 覆盖：电影票房 2026 年起周/月报（栏目往前连续盘点）；新闻出版统计公报 2019–2024、产业分析报告/基本情况 2019–2021；文旅统计公报 2011–2025（含国家旅游局时期）、季度出游数据 2025–2026；广电行业统计公报 2020–2025；网络视听研究报告逐年（2024–2026 大会发布）；演出市场年度报告逐年（协会票务采集平台测算）。全国口径为主。
- 门槛：**免费、免登录**为主（公报/PDF/新闻稿）；文旅部数据服务 API 匿名可用；演出协会官网为 SPA、无开放接口；广电统计直报系统不对外。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA、`-L`、20s）——`GET https://www.zgdypw.cn/sc/sjbg/` → 200，列表含「全国电影票房周报（2026.09.14-09.20）」「全国电影票房月报（2026年8月）」；`GET https://www.nppa.gov.cn/xxgk/fdzdgknr/tjxx/` → 200，8 个 PDF（2024/2023 年新闻出版统计公报、2019–2021 产业分析报告/基本情况），`P020251218382424228218.pdf` → 206 `application/pdf`；`GET https://zwgk.mct.gov.cn/zfxxgkml/tjxx/202606/t20260602_966073.html` → 200《2025年文化和旅游发展统计公报》（发布时间 2026-06-02）；`GET https://sjfw.mct.gov.cn/api/marker/province/list` → 200 JSON（`code:20000`）；`GET https://www.nrta.gov.cn/art/2026/5/13/art_113_73265.html` → 200《2025年全国广播电视行业统计公报》；`GET http://www.cnsa.cn/` → 200（**https 000 不通**）；`GET https://www.capa.com.cn/` → 200 SPA；`GET http://gdtj.nrta.gov.cn/` → 200「系统维护中」。
- 上游：各主管门户（见「细节」表内链接）。

## 细节

### 一、源与入口（均为官方/协会口径）

| 源 | 入口 | 口径 · 形态 |
|---|---|---|
| 中国电影数据信息网（国家电影专资办） | `https://www.zgdypw.cn/sc/sjbg/` | 全国电影票房周报/月报；**HTML 图表** |
| 国家电影局 | `https://www.chinafilm.gov.cn/` | 通知公示 `/xxgk/gsxx/`、行业资讯 `/xwzx/hyzx/`（档期票房新闻）；**无独立数据栏目** |
| 国家新闻出版署 · 统计信息 | `https://www.nppa.gov.cn/xxgk/fdzdgknr/tjxx/` | 新闻出版统计公报、产业分析报告、基本情况；**PDF** |
| 文化和旅游部 · 统计信息 | `https://zwgk.mct.gov.cn/zfxxgkml/447/465/index_3081.html` | 年度公报 + 季度国内出游数据；**HTML** |
| 文化和旅游部 · 公报 | `https://zwgk.mct.gov.cn/zfxxgkml/503/506/index_3081.html` | 年度《文化和旅游发展统计公报》 |
| 文化和旅游部数据服务栏目 | `https://sjfw.mct.gov.cn/site/dataservice/culture` | 文物/非遗/景区/人物可视化；**Nuxt SPA + `/api/` JSON** |
| 国家广播电视总局 | `https://www.nrta.gov.cn/` | 公告公示 `art_113`（年度统计公报）、工作动态 `art_114`（CVB 收视报告） |
| 中国网络视听协会 | `http://www.cnsa.cn/` | 《中国网络视听发展研究报告》/微短剧白皮书发布新闻；**仅 http** |
| 中国演出行业协会 | `https://www.capa.com.cn/` | 演出市场年度报告、票务采集平台测算；**Vue SPA** |

### 二、可直接拼的 URL 规律

- 文旅部公报正文：`https://zwgk.mct.gov.cn/zfxxgkml/tjxx/{YYYYMM}/t{YYYYMMDD}_{id}.html`
- 出版统计 PDF：`https://www.nppa.gov.cn/xxgk/fdzdgknr/tjxx/{YYYYMM}/P{17位}.pdf`
- 电影票房报告：`https://www.zgdypw.cn/sc/sjbg/{YYYYMM}/{DD}/t{YYYYMMDD}_{id}.shtml`
- 广电统计公报：`https://www.nrta.gov.cn/art/{Y}/{M}/{D}/art_113_{id}.html`（`art_114` 为 CVB 收视报告）
- 文旅部数据服务 API：`/api/marker/province/list`（省市点位计数，匿名）；`/api/article/list`、`/api/relic/stats/`、`/api/spot/grouped/`、`/api/person/stats/`（`article/list` 需有效 `categoryId`）

## 坑

1. **文旅部信息公开目录是多级 JS 跳转**：`https://www.mct.gov.cn/zwgk/tjsj/` → `zwgk.mct.gov.cn/?classInfoId=360` → `./zfxxgkml/`，curl 只到中转页；直接请求栏目/正文 URL。
2. **中国网络视听协会 https 不通**（本机 `000`），须用 `http://www.cnsa.cn/`。
3. **演出协会是 Vue SPA**，列表经 `https://capa.com.cn/api` 取数；实测 `/api/index/*`、`/api/client/news/search` 均 **404**（`/index/*` 是前端路由名，非接口路径），无开放接口，抓报告须浏览器。
4. **广电统计直报系统不对外**：`gdtj.nrta.gov.cn` 对公网是「系统维护中」页；广电数字走年度统计公报与 CVB 收视报告（`art_113`/`art_114`）。
5. **电影票房周/月报正文是图表图片**，无结构化表格；要结构化数字须从新闻稿正文抓，或用商业平台（猫眼/灯塔专业版，另计）。
6. 出版统计栏目目前仅 8 条（截至 2024 年公报），更早年份往《中国出版年鉴》《中国新闻出版广电报》找。
7. 文旅部「统计信息」= 季度数据快报，「公报」= 年度汇总，两栏目别混；国家旅游局时期的旅游统计公报也在 `tjxx/` 下。
8. 电影票房另有源头系统——全国电影票务综合信息管理系统 `https://www.gjdyzjb.cn/`（SPA，需影院/发行方账号），公开数据仍回 `zgdypw.cn`。
