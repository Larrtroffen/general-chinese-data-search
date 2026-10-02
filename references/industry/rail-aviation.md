# rail-aviation —— 铁路民航与城轨统计

- 去哪找：
  - 国家铁路局（部委口径，铁路权威）行业统计 `http://www.nra.gov.cn/xwzx/zlzx/hytj/`——月度《全国铁路主要指标完成情况》+ 年度《铁道统计公报》（附 PDF）
  - 国铁集团（企业口径）数据服务 `http://www.china-railway.com.cn/wnfw/sjfw/`——月度/年度《国家铁路主要指标完成情况》（**仅 HTTP 可达**）
  - 中国民航局 信息公开·统计数据 `http://www.caac.gov.cn/XXGK/XXGK/TJSJ/`——月度运输生产 `…/TJSJ/TJSJ_1/`、年度《民航行业发展统计公报》、年度机场生产公报 `…/TJSJ/index_1216.html`
  - 中国城市轨道交通协会 统计报告 `https://www.camet.org.cn/xytj/tjxx/`——年度《城市轨道交通统计和分析报告》（**正文站本机 504，附件 OSS 域可取**）
- 什么时候用：要铁路客运/货运量、里程、机辆，或民航运输总周转量/旅客吞吐量/机场排名，或城轨线路/客运量的**年度/月度官方数字与公报 PDF**；写交通基础设施、枢纽、客流分析需要行业主管部门口径时。
- 怎么搜：清一色「栏目列表 → 按年月目录 → 详情页（HTML 正文 + 附件）」的静态结构，改 URL 年月段即可直取；民航另有 WAS5 站内检索：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # 铁路局年度公报（示例）与附件
  curl -sS -A "$UA" 'http://www.nra.gov.cn/xwzx/zlzx/hytj/202605/t20260529_351347.shtml'
  # 民航局年度行业发展统计公报
  curl -sS -A "$UA" 'http://www.caac.gov.cn/XXGK/XXGK/TJSJ/TJSJ_1/202604/t20260417_230601.html'
  # 民航站内检索（channelid=278090 → HTML 结果页；channelid=268668 → JSONP）
  curl -sS -A "$UA" 'http://www.caac.gov.cn/was5/web/search?channelid=278090&sw=统计公报'
  ```
  结果形态：正文 HTML；**铁路局 / 民航局公报均附 PDF**；国铁集团为 HTML 正文（无附件）；城轨为 OSS 上的 PDF。
- 覆盖：铁路 = 月度指标（近 12 个月滚动）+ 年度铁道统计公报；民航 = 月度生产指标（2026 最新）+ 年度行业发展统计公报（2020–2025）+ 年度机场生产公报（2006–2025）；城轨 = 年度统计和分析报告（2022–2025）。
- 门槛：**免费、无登录**（四处均无需注册）；仅城市轨道交通协会正文站本机连不上（见坑 1）。
- 实测：2026-10-03，macOS arm64，curl 8.x，桌面 UA，20 s 超时，同主机 ≥1.5 s 间隔：
  - `nra.gov.cn/xwzx/zlzx/hytj/` → 200；《2025年铁道统计公报》`/xwzx/zlzx/hytj/202605/t20260529_351347.shtml` → 200，PDF `/xwzx/zlzx/hytj/202605/P020260529633504739062.pdf` → 200 `application/pdf` 2.21 MB ✅
  - `www.china-railway.com.cn/wnfw/sjfw/` → 200（HTTP）；`https://www.china-railway.com.cn/` → 000（HTTPS 不可达）；列表含《2025年国家铁路主要指标完成情况》`./202601/t20260108_151502.html` ✅
  - `caac.gov.cn/XXGK/XXGK/TJSJ/TJSJ_1/` → 200；《2025年民航行业发展统计公报》`…/TJSJ/202604/t20260417_230601.html` → 200，PDF 同目录 `P020260417665629030648.pdf` → 200 1.28 MB；`…/TJSJ/index_1215.html`（月度）、`…/TJSJ/index_1216.html`（机场公报）→ 200 ✅
  - `caac.gov.cn/was5/web/search?channelid=278090&sw=统计公报` → 200 HTML；`?channelid=268668&searchword=统计公报` → 200 JSONP `{"returnCode":"F20002","returnMsg":"查询数据为空"}` ⚠️
  - `www.camet.org.cn/xytj/tjxx/` → **504**（curl HTTP/2 挂起、HTTP/1.1 504；无头 Chromium 同为 504 Gateway Time-out）；附件域 `https://infosharingp2-oss.camet.org.cn/u/cms/www/202403/28125736mgzp.pdf`（2023 年度报告）→ 200 `application/pdf` 3.34 MB ✅
- 上游：国家铁路局 `nra.gov.cn`；中国国家铁路集团 `china-railway.com.cn`；中国民用航空局 `caac.gov.cn`；中国城市轨道交通协会 `camet.org.cn`。

## 细节

### 入口与直链模板（2026-10-03 实测）

| 主题 | 栏目入口 | 文章 URL 形态 | 附件 |
|---|---|---|---|
| 铁道月度主要指标 | `nra.gov.cn/xwzx/zlzx/hytj/` | `…/hytj/{YYYYMM}/t{YYYYMMDD}_{id}.shtml` | 无（正文表格） |
| 铁道统计公报（年度） | 同上 | 同上 | `…/hytj/{YYYYMM}/P0{…}.pdf` |
| 国家铁路主要指标（企业口径） | `china-railway.com.cn/wnfw/sjfw/` | `…/sjfw/{YYYYMM}/t{YYYYMMDD}_{id}.html` | 无 |
| 民航月度生产指标 | `caac.gov.cn/XXGK/XXGK/TJSJ/TJSJ_1/`（列表 `…/TJSJ/index_1215.html`） | `…/TJSJ/{YYYYMM}/t{YYYYMMDD}_{id}.html` | 通常同目录 PDF |
| 民航行业发展统计公报（年度） | 同上 | 同上 | `…/TJSJ/{YYYYMM}/P0{…}.pdf` |
| 民航机场生产公报（年度） | 列表 `…/TJSJ/index_1216.html` | `…/TJSJ/{YYYYMM}/t{YYYYMMDD}_{id}.html` | 同目录 PDF |
| 城轨年度统计和分析报告 | `camet.org.cn/xytj/tjxx/`（列表 `…/tjxx/index_2.shtml` 分页） | `…/xytj/tjxx/{id}.shtml` | `infosharingp2-oss.camet.org.cn/u/cms/www/{YYYYMM}/{file}.pdf` |

- 民航 WAS5 检索：结果页参数为 `channelid=<栏目ID>&sw=<关键词>`（HTML），另有 JSONP 变体（`channelid=268668` 返回 `getHtml({…})`）；`index_1215.html` 与 `index_1216.html` 是 `TJSJ/` 目录下的两个子列表（月度 / 机场）。
- 国铁集团列表首页只滚动近 12 个月，历史需翻页（`index_2.html`…）或直接按年月段拼 URL。

## 坑

1. **城市轨道交通协会 `www.camet.org.cn` 本机 504**：HTTP/1.1、HTTP/2、无头 Chromium 全为 `504 Gateway Time-out`（CDN 边缘 `Via: kunlun…` 回源超时），换 UA/TLS 无效。但**附件域名 `infosharingp2-oss.camet.org.cn` 正常**——从搜索结果/页面拿 PDF 全链可直下；正文站能否访问视网络，不能连时用报告聚合站（如 `fxbaogao.com`）找同一报告。
2. **国铁集团只认 HTTP**：`https://www.china-railway.com.cn/` 握手失败（000），改用 `http://` 同域。
3. **民航 PDF 是文章相对路径**：详情页用 JS `window.location.href="./P0….pdf"` 跳附件，直链须按**文章所在年月目录**拼（`…/TJSJ/{YYYYMM}/P0….pdf`），写成域名根路径会 404。
4. **别把「铁道统计公报」记到国铁集团名下**：公报由国家铁路局发布；国铁集团只有《主要指标完成情况》。
5. **民航检索 `channelid` 要对栏目**：`268668` 是分类计数用的 JSONP 频道，`searchword=` 会返回「查询数据为空」；用 `278090&sw=` 或直接翻列表页更稳。
6. 月度数据也以「新闻稿」形式散见三站（如「前 8 个月发送货物…」），但**引用数字务必落公报原文**并记标题 + 日期。
