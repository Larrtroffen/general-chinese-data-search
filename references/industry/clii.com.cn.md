# clii.com.cn —— 轻工业运行与月度报告

- 去哪找：`http://www.clii.com.cn/`（中国轻工业信息网）；月度报告 `/ydbg/index.html`；经济运行 `/jingjiyunxing/index.html`
- 什么时候用：轻工业月度/季度运行、分省分行业运行监测报告、《轻工业统计资料》《中国轻工行业进出口报告》《中国轻工业竞争力报告》的线索。
- 怎么搜：静态栏目页 + 新闻目录 `/{栏目}/{YYYYMM}/t{YYYYMMDD}_{id}.html`；报告类入口多为 `#`（JS/登录），需浏览器：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -A "$UA" 'http://www.clii.com.cn/jingjiyunxing/index.html'
  curl -sS -A "$UA" 'http://www.clii.com.cn/ydbg/index.html'
  ```
- 覆盖：月度经济运行信息（实测有 2026-08）；月度报告栏目列出行业报告与 20+ 个省市行业运行监测报告，多为定制/纸本。
- 门槛：栏目与新闻免费；报告本体（《轻工业统计资料》等）入口为 `#`，疑需登录/订阅（**未验证**）。
- 实测：2026-10-03 `http://www.clii.com.cn/` → 200，60.5 KB，title「中国轻工业信息网——全国轻工行业门户」；`/ydbg/index.html` → 200，33 KB，title「月度报告」✅；`https://www.clii.com.cn/` → **443 连接失败 ❌**。
- 上游：中国轻工业联合会 / 中国轻工业信息中心。

## 坑

1. 只有 http 通，https 直接 connection refused。
2. 这里不是免费表格库：报告类入口基本是 `#` 或定制采购；用新闻稿取数量级时务必标注为「协会口径快报」。
