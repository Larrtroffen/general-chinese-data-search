# cn-scraper-mcp —— 本地登录态收割与多平台检索

MIT，Python 3.11+，本地跑的 MCP Server（`pip install cn-scraper-mcp`，PyPI 0.5.0）。
**它的价值不是数据本身，而是「通道钥匙管理」**：用本机 Chrome（CDP）替你收割 Cookie/登录态，
把本来「必须登录」的中文平台变成 agent 可直接调用的检索工具。正好补 `social/README.md` 里「匿名全挂」的缺口。

- 去哪找：repo https://github.com/goesByhc/cn-scraper-mcp （49★，MIT）；Docker `ghcr.io/goesbyhc/cn-scraper-mcp:latest`（远程 HTTP 模式）；Cookie 存本机 `~/.cn-scraper-cookies/`，京东用持久化 Chrome Profile。
- 什么时候用：要**按关键词检索社交/电商平台**时（触发词：小红书 笔记/口碑、知乎 搜索/回答、微博 搜索/时间线、B站 视频/评论、知识星球、豆瓣、大众点评、淘宝/京东）。
  **别用于**：要某单位/年份的系统性语料（仍应走政府网站 + 公众号）；没本机浏览器/Chrome 的服务器环境（除 B站/知乎/微博 API 类）。
- 怎么取：
  ```bash
  pip install cn-scraper-mcp && cn-scraper-mcp        # stdio MCP
  # 客户端配置（Claude Code/.mcp.json、Cursor、Codex config.toml）
  {"mcpServers":{"cn-scraper":{"command":"cn-scraper-mcp","args":[]}}}
  # 第一步永远是拿钥匙 → 让 Agent 调：
  guided_login(platform="weibo")   # 打开本地 Chrome 官方登录页，你扫码/输密码，CDP 自动收割（含 HttpOnly）
  # 或已有登录好的 Chrome：harvest_cookies(platform="weibo")；再 check_cookies / verify_login / diagnose
  ```
  结果形态：JSON（MCP 工具返回平台原生字段）。
- 覆盖：搜索列表 + 详情 + 评论（均带平台原生字段，如小红书笔记带 `noteId/xsec_token`、微博带分页评论）；**无历史回溯保证**（平台搜什么给什么）。
- 门槛：**需本机 Chrome**（部分平台仅需 REST/登录态，见「细节」）；Cookie 文件敏感
- 实测：2026-10-02 **未安装、未调用任何工具**。证据：`curl https://pypi.org/pypi/cn-scraper-mcp/json` → 存在，version `0.5.0`；`gh api repos/goesByhc/cn-scraper-mcp --jq '.license.spdx_id,.default_branch'` → `MIT / master`；`curl -o raw_social/goesByhc-README.md https://raw.githubusercontent.com/goesByhc/cn-scraper-mcp/master/README.md` → 14410 B（工具清单/平台表按原文抄录）。
- 上游：https://github.com/goesByhc/cn-scraper-mcp

## 细节

### 工具面（按平台）

`taobao_search|taobao_product`、`jd_search|jd_product`、`pdd_search|pdd_product_detail`、
`xiaohongshu_search|xiaohongshu_note|xiaohongshu_comments`（详情要 `noteId`+`xsec_token`）、
`zhihu_search|zhihu_hot_list|zhihu_answer|zhihu_question_answers|zhihu_comments`、
`weibo_search|weibo_hot_list|weibo_user_timeline|weibo_post|weibo_comments`、
`douyin_search|douyin_hot_list|douyin_video|douyin_comments`（⚠️实验性，需人工过滑块）、
`bilibili_search|bilibili_popular|bilibili_video|bilibili_comments`、`douban_*`、`dianping_*`、`zsxq_topics|zsxq_article`。

### 钥匙与平台门槛（上游自述，决定可行性）

- **无需浏览器**：知乎（REST v4，需登录态）、微博（需 SUB token；热搜游客可访问）、知识星球、B站（公开 Web API，无需登录）、豆瓣/大众点评（可能风控）。
- **需本地 Chrome**：京东（headful + 动态签名）、小红书（**只允许住宅 IP**，数据中心 IP 直接封）、抖音（人工验证码，120s 等待）。
- **不推荐**：拼多多（每个浏览器会话只放行第一次搜索）。淘宝走 `curl_cffi`+MTOP 签名，无硬限流但不建议高频。

## 坑

- 需本机 Chrome（macOS 可行）。
- Cookie 文件敏感勿外传；远程 HTTP 模式会通过网络访问本机 Cookie，**勿裸奔公网**。
- 上游声明「仅学习研究，批量抓取可能违反平台 ToS」。
