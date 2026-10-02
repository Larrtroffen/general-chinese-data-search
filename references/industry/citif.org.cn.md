# citif.org.cn —— 电子信息行业联合会入口

- 去哪找：`http://www.citif.org.cn/` → 跳 `https://www.citif.org.cn/CFEII/miit/`
- 什么时候用：查中国电子信息行业联合会通知/公示（信息系统集成能力授予、行业大会等）时；**统计数值请另找**。
- 怎么搜：Vue SPA，内容全由 JS 渲染，curl 只拿到外壳：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -A "$UA" 'http://www.citif.org.cn/'    # 6.4 KB，仅 <div id=app> 与静态资源引用
  ```
  静态资源挂在 `https://download.yxybb.com/project/ZYJY/CFEII/`（`static/js/app.59e9f33c.js` 等），入口 JS 内未见可读的 REST 基址 → **仅浏览器**。
- 覆盖：联合会动态、公示公告（未能实测内容）。
- 门槛：免费；需浏览器。
- 实测：2026-10-03 `http://www.citif.org.cn/` → 200，6.4 KB，title「中国电子信息行业联合会」，页面为 Vue 构建产物（`static/js/app.59e9f33c.js`、`chunk-elementUI.*.js`），无可 curl 的栏目 ⚠️。
- 上游：中国电子信息行业联合会（CITIF）。

## 坑

1. **无可 curl 的数据接口**：需要电子信息行业数据时改用工信部电子信息司运行数据（`../stats/ministry-stats.md`）或 `cinic.org.cn.md`（转载汇总）。
2. 站点托管在第三方资源域 `download.yxybb.com`，主体域名变更/失效风险高，引用前先确认可访问。
