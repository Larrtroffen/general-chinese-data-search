# social —— 社交平台源（索引）

微博 / 知乎 / 贴吧这类 UGC 平台：事件传播、地方讨论的补充线索。**本机匿名实测结论偏悲观**：三家的检索与正文几乎都要登录态或过安全验证，能匿名直取的只有微博热搜榜。把它们当「线索源」，**不要当语料主源**。

另有一类**问政/民生平台**（领导留言板、百姓呼声、网上民声等）是**可直接取一手民意与官方回复文本**的源，入口与检索方式见 `voice-platforms.md`，与上表的 UGC 平台定位不同，优先用它做「群众诉求 + 回复」语料。

## 平台一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `weibo.com.md` | 新浪微博（weibo.com / s.weibo.com / m.weibo.cn） | 事件传播/舆情线索；热搜榜 JSON 匿名可取（**必须带 `Referer`**），检索需真实登录 cookie（访客 cookie 无效） | ✅ 热搜榜可用 |
| `zhihu.com.md` | 知乎（zhihu.com / zhuanlan.zhihu.com） | 问答/专栏线索（标题/URL）；搜索页与专栏页均需登录 | ❌ 匿名 403/302 |
| `tieba.baidu.com.md` | 百度贴吧 | 地方话题/民间讨论线索 | ❌ 本机被安全验证 |
| `voice-platforms.md` | 问政/民生平台（人民网领导留言板 / 红网百姓呼声 / 胶东在线网上民声 / 麻辣社区 / 大河号） | **一手民意 + 官方回复文本**：按关键词检索「群众诉求」与答复；领导留言板/百姓呼声/网上民声均有免登录 JSON 接口 | ✅ 留言板(需签名)、百姓呼声、网上民声 API 直读；⚠️ 麻辣/大河检索需登录 |
| `xiaohongshu-mcp.md` | 小红书（xpzouying MCP） | 关键词搜索 + 笔记详情 + 评论 + 用户主页 | ❌ 需登录+住宅 IP |

## 登录态工具箱（把上表的「❌ 需登录」变成可调用工具）

上面几家卡在**登录态**上。以下四个都是「**自带钥匙管理**」的通道卡：它们不提供数据本体，
而是把「本机浏览器/账号的登录态」变成 agent 可调用的检索工具。**均未本机安装/运行**，只读文档与仓库元数据。

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `cn-scraper-mcp.md` | goesByhc/cn-scraper-mcp（MIT，PyPI 0.5.0，49★） | 本地 MCP Server：`guided_login(平台)` 打开本机 Chrome 官方登录页 → CDP 自动收割 Cookie（含 HttpOnly），存 `~/.cn-scraper-cookies/`；覆盖淘宝/京东/小红书/知乎/微博/B站/抖音/知识星球/豆瓣/大众点评 | ⚠️ 未安装 |
| `xiaohongshu-mcp.md` | xpzouying/xiaohongshu-mcp（Apache-2.0，16k★，Go 二进制） | 小红书 MCP：搜索/笔记详情/评论/用户主页（+发布类）；**`feed_id`+`xsec_token` 必须成对用**；只允许住宅 IP | ⚠️ 未部署 |
| `chubbyskills.md` | chubbyguan/chubbyskills（MIT，1.1k★） | 14 个采集/转录 Skill：链接→Markdown 知识库（公众号/小红书/X/微博/知乎/抖音/B站/播客/YouTube）；含**平台可用性速查表** | ⚠️ 未安装 |
| `agent-reach.md` | Panniantong/Agent-Reach（MIT，88k★） | Agent 上网能力安装器/路由层（中文侧：小红书/B站/V2EX/雪球/小宇宙/Boss直聘）；`agent-reach doctor` 体检 | ⚠️ 未安装 |

## 使用建议

1. **先问是否必要**：按单位/年份的系统性语料，优先政府网站 + 公众号（`../gov/README.md`、`../wechat/README.md`）；社交平台只用于补舆情、补民间讨论、交叉验证事件时间点。
2. **要「群众诉求 + 官方回复」的一手文本** → 用 `voice-platforms.md`（领导留言板/百姓呼声/网上民声均有免登录 JSON 接口），比在本层 UGC 平台找线索更直接；领导留言板需按卡内规则自签 JSON 请求。
3. **顺序**：先用 `../engines/README.md` 的 `site:` 点查判断「这个平台上到底有没有这条线索」→ 有，再决定是否值得开登录态工具箱去取结构化数据。
4. **微博**：只用热搜榜接口取**当前**热榜（无登录、需 Referer、无历史回溯）；检索要么真实登录 cookie（`weibo.com.md`），要么走 `cn-scraper-mcp.md` 的 `weibo_search`（后者帮管登录态）。
5. **知乎**：匿名只能靠搜索引擎取标题/URL 线索；要正文就得上 `cn-scraper-mcp.md` 的 `zhihu_*` 工具（知乎 REST v4 需登录态，但**无需浏览器**）。
6. **小红书**：**只有登录 + 住宅 IP 一条路**（`xiaohongshu-mcp.md` 或 `agent-reach.md`）；`publish_time` 只有「一天/一周/半年」粗粒度，做不了按年份回溯。
7. **贴吧**：本机 IP 已被百度安全验证拦死；要采就得换网络/人工过码（未验证），否则放弃。
8. **频率与合规**：≤3 次/主机、间隔 ≥1.5s、timeout 20s、桌面 UA；所有通道都受平台 ToS 约束，登录态 cookie 会过期并触发风控；
   工具箱里的 Cookie 文件按「已登录浏览器」同等敏感度保护（勿入 git、勿外传）。

## 相关

- 综合搜索引擎（`site:` 点查、替代召回）：`../engines/README.md`
- 问政/民生平台（一手民意 + 官方回复）：`voice-platforms.md`
- 微信公众号（真正的主力 UGC 通道）：`../wechat/README.md`
- 通用代理/存档工具（本机多不可达）：`../tools/README.md`
- 数据源总索引：仓库根 `SKILL.md`
