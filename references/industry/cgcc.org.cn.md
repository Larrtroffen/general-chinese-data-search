# cgcc.org.cn —— 零售业景气指数与消费市场

- 去哪找：`http://www.cgcc.org.cn/`；景气指数 `/hyfz/zglsyfzzs/`；月度报告 `/hyfz/zglsyfzzs/ydbg/`；消费市场分析 `/shdt/`
- 什么时候用：中国零售业景气指数（CRPI）月度值、消费市场运行分析、商贸流通形势判断。
- 怎么搜：静态编号页，直接取栏目或详情：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -A "$UA" 'http://www.cgcc.org.cn/hyfz/zglsyfzzs/ydbg/'      # 月度报告列表
  curl -sS -A "$UA" 'http://www.cgcc.org.cn/hyfz/zglsyfzzs/ydbg/53989.html'
  ```
- 覆盖：零售业景气指数月度分析（实测列表覆盖 2022-07 ~ **2025-09**）；消费市场月度运行分析（实测首页有 2026-08 条目）。
- 门槛：免费、无需登录。
- 实测：2026-10-03 `http://www.cgcc.org.cn/` → 200，98 KB，title「中国商业联合会」；`/hyfz/zglsyfzzs/ydbg/` → 200，34.5 KB，title「月度报告」，列表最新「2025年9月」（**未见 2026 年条目 ⚠️**）。
- 上游：中国商业联合会（数据分析专业委员会站点 `www.chinacpda.org`）。

## 坑

1. 景气指数「月度报告」栏目实测最新只到 2025-09，疑似迁移或改在其他频道发布；要当期值先看首页 `/shdt/` 与媒体转载。
2. 报告为 HTML 正文，指数值需自行从文中摘取，无表格附件、无 API。
3. 站内 URL 用纯数字 `.html`（如 `53989.html`），不能按年月规律拼，需逐页抓列表。
