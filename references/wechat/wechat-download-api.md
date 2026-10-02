# wechat-download-api —— 后台凭证 API 与多格式导出

自托管 FastAPI 服务：用**自有公众号后台管理员扫码**拿登录态，然后对**任意公众号**做搜索→列历史→抓正文→出 RSS→多格式导出。
是「后台 Cookie+Token 路线」的工程化封装（与 `wechat-digest-skill.md` 同源，但提供 HTTP 接口 + MCP）。⚠️ **AGPL-3.0：只作品路参考，不直接引入我们的仓库/产品**（对外提供网络服务需开源修改代码）。

- 去哪找：repo https://github.com/tmwgsicp/wechat-download-api ；镜像 `tmwgsicp/wechat-download-api:latest`；SaaS 托管版 `https://wechatrss.waytomaster.com`；接口文档 `http://localhost:5000/api/docs`（Swagger）、`/api/health`。
- 什么时候用：要**按号全量历史 + 号内关键词搜索 + 结构化导出（Markdown/Excel/EPUB…）+ RSS 订阅**时；比搜狗强的地方是 `appmsg` 按号真历史（不受索引子集限制）、支持分页 `begin/count`（上限 100）、能出 RSS 让 agent 增量消费。
  **不适合**：要阅读数/点赞数（README 未提供该能力）、没有公众号账号的人。
- 怎么取：
  ```bash
  docker run -d -p 5000:5000 -v $(pwd)/data:/app/data -v $(pwd)/.env:/app/.env --name wechat-api tmwgsicp/wechat-download-api:latest
  # 浏览器 http://localhost:5000/login.html 用「公众号管理员微信」扫码
  curl 'http://localhost:5000/api/public/searchbiz?query=人民日报'            # → fakeid（如 MzA1MjM1ODk2MA==）
  curl 'http://localhost:5000/api/public/articles?fakeid=<FID>&begin=0&count=100'
  curl 'http://localhost:5000/api/public/articles/search?fakeid=<FID>&query=关键词'
  curl -X POST http://localhost:5000/api/article -H 'Content-Type: application/json' -d '{"url":"https://mp.weixin.qq.com/s/xxx"}'
  curl 'http://localhost:5000/api/rss/<FID>'                                  # RSS 2.0
  curl -OJ 'http://localhost:5000/api/export/account/<FID>.epub?since=<unix>' # 多格式打包
  ```
  增量同步：`/api/feed/articles.json?since=<next_since>&limit=200` + `/api/feed/article/{id}.md`（带 YAML frontmatter，直接进 Obsidian）。结果形态：**JSON / RSS / 文件**。
- 覆盖：按号历史分页（≤100/次）+ 号内关键词搜索 + 多格式导出（上限 3000/500/200）+ RSS + MCP 6 工具；**不含阅读数/点赞数**。
- 门槛：需**一个自己的公众号**并由管理员扫码（cookie 约 4 天）；⚠️ AGPL-3.0，只作品路参考
- 实测：2026-10-02 **未本地部署、未实测任何接口**。已做证据：`gh api repos/tmwgsicp/wechat-download-api --jq '.license.spdx_id,.stargazers_count'` → `AGPL-3.0 / 1146`；`curl -o /dev/null -w '%{http_code}' -L https://wechatrss.waytomaster.com/` → **200**（2.04s，SaaS 在线）。
- 上游：https://github.com/tmwgsicp/wechat-download-api

## 细节

### 接口面

`/api/article`、`/api/public/searchbiz|accountinfo|articles|articles/search`、`/api/rss/*`（含聚合源、分类源、历史 RSS）、
`/api/export/account/{fakeid}.{zip|html|xlsx|json|docx|pdf|epub}`（上限 3000/500/200）、`/api/image`（微信 CDN 图片防盗链代理）、
`/api/login/*`、`/api/admin/status`。业务响应统一 `{success,data,error}`（登录态失效为 HTTP 200 + `success:false`）。

### MCP

`/mcp`（静态 Bearer `MCP_TOKEN`，需同时设 `ENABLE_MCP=1`）6 工具：`search_accounts`/`subscribe_account`/`unsubscribe_account`/`list_subscriptions`/`get_recent_articles`/`read_article`。

## 坑

- ① 需**一个自己的公众号**并由管理员扫码，cookie 约 **4 天**过期（每 6h 自检 + Webhook 预警）；② 单账号，多号要部署多实例；
- ③ 触发风控要人工过验证 + 等 30 分钟 + 降频；④ 反风控靠 curl_cffi TLS 指纹 + SOCKS5 代理池（README 强烈建议配代理）；⑤ 只导「已抓正文」的文章。
