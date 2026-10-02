# fangchan.com —— 房地产企业与市场数据

- 去哪找：`http://www.fangchan.com/`（中房网，中国房地产业协会官网）；数据研究 `/data/`；年鉴频道 `/yearbook/`
- 什么时候用：房地产企业销售/业绩榜、市场月度与专题分析、政策解读、中国房地产年鉴（年鉴解读 / 历年年鉴 / 年鉴查询）。
- 怎么搜：静态栏目 + 日期目录：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -A "$UA" 'http://www.fangchan.com/data/'                    # 数据研究列表
  curl -sS -A "$UA" 'http://www.fangchan.com/data/14/2026-08-31/7500163555736752132.html'
  ```
  结果形态：HTML 报告/解读正文；**无 PDF、无 API**。
- 覆盖：数据研究栏实测含 2026-09/08 企业业绩与市场分析；年鉴频道含「年鉴解读 / 历年年鉴 / 年鉴查询」三区块。
- 门槛：报告免费阅读；**《中国房地产年鉴》需购买**（年鉴频道给出微店购买链接）。
- 实测：2026-10-03 `http://www.fangchan.com/` → 200，45 KB，title「中房网_中国房地产业协会官方网站」；`/data/` → 200，32.8 KB；`/yearbook/` → 200，34 KB（页面 `.pdf` 命中 0，购买入口指向微店）✅。
- 上游：中国房地产业协会 / 中房网。

## 坑

1. `https://www.fangchan.com/` 证书主机名不匹配 → 用 http。
2. 年鉴正文不在线，线上只有解读与目录；要表格数据走 `../stats/cnki-data.md` 或纸本/商业年鉴库。
3. `/data/` 列表里部分 href 含模板变量残留（形如 `/$ {path}/…`），复制 URL 前先用页面上的实际链接。
