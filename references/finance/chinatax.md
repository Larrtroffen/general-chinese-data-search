# chinatax —— 税务统计与年度报告

- 去哪找：**税收统计** `https://www.chinatax.gov.cn/chinatax/n810214/n810631/index.html`；**数说税收 / 税收数据** `https://www.chinatax.gov.cn/chinatax/n810214/c102374/c102380/c101729b/zfxxgks.html`；**中国税务年度报告** `https://www.chinatax.gov.cn/chinatax/n810219/n810744/c103068/ndbg2024.html`；站内检索 `https://www.chinatax.gov.cn/search5/html/searchResult.html?siteCode=bm29000002&searchWord={词}`。
- 什么时候用：要**国家税务总局口径**的税收数据——年度/月度税收收入、分税种/分地区税收、宏观税负、减税降费规模；要《中国税务年度报告》《中国税务年鉴》原文；要省级税务局的分省税收统计。
- 怎么搜：栏目页**服务端渲染 HTML**，无公开 JSON 接口；按 **URL 规律**取：列表 `…/n810214/n810631/index.html`，文章 `…/n810214/n810631/c{id}/content.html`；年度报告挂 PDF 附件（`…/{id}/{id}/files/{hash}.pdf`）。站内检索用 `search5/html/searchResult.html?siteCode=bm29000002`。省级：`{城市}.chinatax.gov.cn/col/col{NNNNN}/index.html?number={栏目码}`。
- 覆盖：全国税收收入及分税种/分月/分地区（栏目按年累积，多为 2015 年前后至今）；年度报告逐年（PDF）；省局统计栏目覆盖本省年度/季度税收。税务总局年鉴/公报级更细数据以纸质/年报刊载。
- 门槛：免费、无需登录、无验证码；文章正文与 PDF 可直接取。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA——税收统计栏目 `200/7616B`；文章 `…/n810214/n810631/c5165806/content.html` `200/7982B`（title「2021年前4个月全国累计新办涉税市场主体达413万户」）；数说税收栏目 `200/17996B`；年度报告页 `200/1955B`，含 PDF 附件直链；大连市局 `col/col2923/index.html` `200/6945B`。
- 上游：国家税务总局（`chinatax.gov.cn`）。

## 细节

### 一、栏目与 URL 规律

| 内容 | URL | 实测 |
|---|---|---|
| 税收统计（总局） | `https://www.chinatax.gov.cn/chinatax/n810214/n810631/index.html` | ✅ 200 / 7616 B |
| 统计文章页 | `…/chinatax/n810214/n810631/c{id}/content.html` | ✅ 200 / 7982 B |
| 数说税收/税收数据 | `…/chinatax/n810214/c102374/c102380/c101729b/zfxxgks.html` | ✅ 200 / 17996 B |
| 中国税务年度报告 | `…/chinatax/n810219/n810744/c103068/ndbg{年}.html` | ✅ 200 / 1955 B |
| 年度报告 PDF 附件 | `…/chinatax//n810219/n810744/c103068/c{id}/{id}/files/{hash}.pdf` | ✅ 页面内出现（如 `bc5411a12ccd4e428da0449a6a6431f8.pdf`） |
| 省级税收统计 | `{城市}.chinatax.gov.cn/col/col{NNNNN}/index.html?number={栏目码}` | ✅ 大连 `col2923` 200 / 6945 B |

- 站内检索接口：`https://www.chinatax.gov.cn/search5/html/searchResult.html?siteCode=bm29000002&searchWord={URL编码词}&left_right_index=0&searchSource=0`（`siteCode=bm29000002` 为税务总局站点码）。
- 年度报告页把全年报告拆成多份 PDF（正文/附表），**数据表在 PDF 附件里**，不是 HTML 表格。

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
# 税收统计栏目列表
curl -s -A "$UA" 'https://www.chinatax.gov.cn/chinatax/n810214/n810631/index.html' | grep -oE 'href="[^"]*c[0-9]+/content.html"'
# 年度报告的 PDF 附件直链
curl -s -A "$UA" 'https://www.chinatax.gov.cn/chinatax/n810219/n810744/c103068/ndbg2024.html' | grep -oE 'href="[^"]*\.pdf"'
```

### 二、相关

- **财政部**税收/财政收支口径见 `../stats/ministry-stats.md`（`mof.gov.cn/gkml/caizhengshuju/`）与 `fiscal-open.md`：税务总局口径为「税收收入」，财政部口径为「一般公共预算收入中的税收」，两者**不完全相等**。
- **分省税收**：优先用各省税务局统计栏目，再用《中国税务年鉴》/各省统计年鉴核对。
- 中国税务年鉴官方电子版入口较弱，实际取书多用年鉴聚合站（见 `../regional/provincial-yearbooks.md`、`../stats/ministry-stats.md`）。

## 坑

1. 栏目页 HTML 里混有大量**导航/热词链接**，抓数据要按 `n810214/n810631/c{id}/content.html` 精确过滤，否则混入新闻。
2. **无公开 JSON API**：本机未发现 `loadData`/`.json` 类取数端点；数据只能从 HTML 正文或 PDF 附件里取。
3. 「税收收入」**逐年修订**（汇算清缴/口径调整），引用务必落到对应年度的报告原文并记标题+日期，不要用新闻稿数字。
4. 年度报告 PDF 路径含**双斜杠**（`/chinatax//n810219/…`），直接复制时保留原样、或用 `-L` 跟随。
5. 分税种/分地区明细在**省局栏目**更全，总局栏目以全国汇总与解读为主；跨省比较要逐省取。
6. 站内检索 `siteCode` 写死为 `bm29000002`，改成地方站码无效；查地方局用其自身检索入口。
