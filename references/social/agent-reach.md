# agent-reach —— Agent 上网能力安装与路由

MIT，Python 3.10+（`gh api` 报 88k★ / 2026-09 更新）。**它不是数据源，而是一层平台接入路由器**：
每个平台「首选 + 备选多后端」，装上后由 agent 用命令行调。对中文研究真正有用的只有其中几行（小红书/B站/V2EX/雪球/小宇宙/Boss直聘），其余（YouTube/Reddit/Facebook/Instagram/LinkedIn/X）是英文场景。

- 去哪找：repo https://github.com/Panniantong/Agent-Reach ；安装/更新语料 `docs/install.md`、`docs/update.md`（把 raw URL 丢给 agent 让它自己装）；诊断命令 `agent-reach doctor`。
- 什么时候用：要在**本机（macOS 桌面）**把 agent 接到「小红书（搜索/阅读/评论）、B站（搜索+详情+字幕）、V2EX（热门/节点/帖子+回复）、雪球（行情/热帖）、小宇宙播客（Whisper 转录）、Boss直聘（岗位+JD）」时；也适合当**「某平台还能不能用」的体检器**（doctor）。
  **别用于**：指望它做系统性语料采集（它是通道，不是索引）。
- 怎么取（交给 agent，而非手工）：
  ```text
  帮我安装 Agent Reach：https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
  帮我配 B站 / 帮我配小宇宙播客 / 帮我配雪球        # 按平台引导配置
  agent-reach doctor                                # 一条命令看哪个通、哪个不通、怎么修
  ```
  结果形态：命令行输出 / 平台原生粒度。
- 覆盖：平台原生粒度（帖子/视频/字幕/行情/岗位），**无历史全量保证**；订阅类只有 RSS/YouTube 频道。
- 门槛：装好即可用一批（网页/YouTube/RSS/GitHub/V2EX）；其余需配置（Chrome 会话或手工导 Cookie）
- 实测：2026-10-02 **未安装、未跑 doctor、未调用任何平台**。证据：`gh api repos/Panniantong/Agent-Reach --jq '.license.spdx_id,.default_branch,.stargazers_count'` → `MIT / main / 88131`；`curl -o raw_social/agent-reach-README.md https://raw.githubusercontent.com/Panniantong/Agent-Reach/main/README.md` → 22830 B（平台表按原文抄录）。
- 上游：https://github.com/Panniantong/Agent-Reach

## 细节

### 平台与钥匙（上游自述「装好即用 / 配置后解锁」）

- **装好即用**：任意网页阅读、YouTube 字幕+搜索、任意 RSS/Atom、GitHub 公开仓库、V2EX 热门/节点/帖子详情+回复。
- **需配置**：小红书（`OpenCLI` 复用用户已有 Chrome 会话；或用 Cookie-Editor 导出手工配置 xiaohongshu-mcp）、B站字幕（OpenCLI）、雪球、小宇宙播客（Whisper，免费 Key）、Boss直聘（专用 Chrome 手动登录 CDP）、Twitter/X（必须 Cookie-Editor 手工导出，且运行前需显式设 `TWITTER_AUTH_TOKEN`/`TWITTER_CT0`）。
- **无零配置路径**：Reddit（匿名接口已封）、Facebook、Instagram（需 OpenCLI 复用 Chrome 登录态）。

### 何时优于搜狗/原生匿名访问

- 小红书、B站字幕、雪球、Boss直聘这些**搜狗索引不到、匿名又打不开**的站，它是「先用浏览器登录一次、之后命令行随时取」的最低成本路径。
- 反之，只为拿知乎/微博的标题线索时，直接 `site:` 点查（`../engines/README.md`）更快，不必开这套工具箱。

## 坑

- ① Cookie 只存本地、不上传，但需用户自己完成平台登录（工具**不代登录**小红书，也不读取其浏览器 Cookie）。
- ② 依赖 agent 有 shell 执行权限（OpenClaw 需 `openclaw config tools.profile "coding"`）。
- ③ 服务器部署才需要代理（约 $1/月，本地不需要）。
- ④ 上游自述「某接入方式失效就换代」（例：2026-06 yt-dlp 被 B站风控封 → 换 bili-cli），意味着**接口会漂移**。
