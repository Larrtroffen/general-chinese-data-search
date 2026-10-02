# xiaohongshu-mcp —— 小红书检索/详情/评论

Go 写的 MCP Server（Apache-2.0，16k★，最新 release v2.5.5 / 2026-09-22，含 darwin-arm64 等 6 个二进制）。
**能力面**：搜索笔记、读笔记详情与评论、读用户主页——以及一批发布/互动工具（对研究无用）。
小红书**无匿名通道**，这是「有登录态才能检索」的现成实现。

- 去哪找：repo https://github.com/xpzouying/xiaohongshu-mcp ；登录器 `xiaohongshu-login-darwin-arm64`（Win/Linux 同名变体）；Docker `xpzouying/xiaohongshu-mcp`；另有零配置浏览器插件版 `xpzouying/x-mcp`（免部署，非技术用户首选）。
- 什么时候用：要**小红书按关键词检索 + 笔记正文 + 首屏/全量评论 + 用户主页**时（触发词：小红书、笔记、口碑、探店、事件爆料里的截图出处）。
  **别用于**：系统性按单位/年份的语料（小红书无时间维度全量导出）；发布/点赞/评论（研究不需要且更易触发风控）。
- 怎么取：
  ```bash
  # 1) 登录（先跑登录器，用手机小红书扫码，凭据落本地 cookie 文件）
  chmod +x xiaohongshu-login-darwin-arm64 && ./xiaohongshu-login-darwin-arm64
  # 2) 起 MCP 服务，再在 Claude Code / Cursor 里配置该 MCP Server
  # 3) 调工具
  ```
  结果形态：JSON（MCP 工具返回平台原生字段）。
- 覆盖：搜索（关键词，`publish_time` 仅粗粒度）、笔记详情 + 评论、用户主页；**无年份区间回溯**。
- 门槛：**需扫码登录真实小红书账号 + 本地/住宅 IP**（数据中心 IP 会被封）
- 实测：2026-10-02 **未部署、未登录、未调用 MCP**。证据：`gh api repos/xpzouying/xiaohongshu-mcp --jq '.license.spdx_id,.stargazers_count'` → `Apache-2.0 / 16082`；`gh api repos/xpzouying/xiaohongshu-mcp/releases --jq '.[0].tag_name'` → `v2.5.5`（2026-09-22，6 个 assets）；`curl -o raw_social/xiaohongshu-mcp-README.md https://raw.githubusercontent.com/xpzouying/xiaohongshu-mcp/main/README.md` → 47842 B（工具清单按 §2.3 抄录）。注：该 repo 83 MB，按纪律**未克隆**，只用 raw README。
- 上游：https://github.com/xpzouying/xiaohongshu-mcp （插件版：https://github.com/xpzouying/x-mcp）

## 细节

### MCP 工具面（README §2.3，共 13 个；研究相关的前 4 个）

- `search_feeds{keyword, filters}` —— `filters`：`sort_by`（综合/最新/最多点赞/最多评论/最多收藏）、`note_type`（不限/视频/图文）、**`publish_time`（不限/一天内/一周内/半年内 ← 只有粗粒度，没有年份区间）**、`search_scope`（不限/已看过/未看过/已关注）、`location`（不限/同城/附近）；
- `get_feed_detail{feed_id, xsec_token, load_all_comments, limit, click_more_replies, reply_limit, scroll_speed}` —— 互动数据 + 评论（默认只前 10 条一级评论）；
- `user_profile{user_id, xsec_token}`；
- `check_login_status`/`get_login_qrcode`/`delete_cookies`。
- 其余：`publish_content`/`publish_with_video`/`post_comment_to_feed`/`reply_comment_in_feed`/`like_feed`/`favorite_feed`。

### 关键约束

- 搜索返回的 `feed_id` 与 `xsec_token` **必须成对使用**才能取详情/评论（token 是访问凭证，不可复用/猜测）。
- 详情页互动数（点赞/收藏/评论）是它的强项——这是搜狗、公众号后台都拿不到的。

## 坑

- ① 必须**扫码登录真实小红书账号**，cookie 存本地。
- ② 需要**本地/住宅 IP**，数据中心 IP 会被封（云端服务器跑不稳）。
- ③ Docker 部署坑多（上游指向 Issues #56，建议直接用 `x-mcp` 插件版或 `xiaohongshu-mcp-skills`）。
- ④ 发布类工具有违禁词/限流风险，与检索混用同一个账号不划算。
- ⑤ 微博/知乎同理，小红书抓取受平台服务条款限制。
