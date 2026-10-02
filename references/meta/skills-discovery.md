# skills-discovery —— 持续发现新 skill 与新源

- 去哪找：
  - **skills.sh 注册表**：`npx -y skills@latest find "<英文关键词>"`（技能市场，含安装量）；榜单 `https://skills.sh/`；单体页 `https://skills.sh/<owner>/<repo>/<skill>`（可 curl）。
  - **GitHub**：`gh search repos '<中/英关键词>' --limit 20 --json fullName,description,stargazersCount,updatedAt,license,url`（已登录，最有效）；`gh search repos --topic claude-skills <kw>`；仓库元数据 `gh api repos/<o>/<r>`；技能正文 `curl -s https://raw.githubusercontent.com/<o>/<r>/HEAD/SKILL.md`。
  - **目录类**：`references/meta/awesome-china-mcp.md`（中国 MCP）、awesome-mcp-servers（punkpeye）、anthropics/skills、vercel-labs/skills、obra/superpowers、chubbyskill 等（见 `awesome-lists.md`）。
- 什么时候用：需要新能力/新源时的第一步；每季度给 `CANDIDATES.md` 补货时。
- 怎么取（一次完整巡例）：
  ```bash
  # 1) 注册表（只认英文词）
  npx -y skills@latest find "scraping"        # → owner/repo@skill + 安装量
  # 2) GitHub 仓库（中英文都行）
  gh search repos '政策文件 爬虫' --limit 20 --json fullName,stargazersCount,updatedAt,url
  gh search repos 'bookmark' --limit 5 | cat  # 主题/星数可用 --json 细化
  # 3) 核实正文与元数据
  gh api repos/<owner>/<repo> --jq '{stars:.stargazers_count,updated:.updated_at,size_kb:.size,license:.license.spdx_id}'
  curl -s https://raw.githubusercontent.com/<owner>/<repo>/HEAD/SKILL.md | head -60
  # 4) 记录到 CANDIDATES.md（含证据、依赖、优先级），挑中的进入收编流程
  ```
- 覆盖：技能注册表、GitHub 仓库与技能正文（`SKILL.md`）、候选池 `CANDIDATES.md`；注册表只认英文词，中文一律零命中。
- 门槛：本地已装并登录 `gh`；`npx -y skills@latest` 可用；无 key。
- 实测：2026-10-02，十路领域侦察即按此流程跑通（结果见根目录 `CANDIDATES.md`）。
- 上游：机制说明（find-skills skill / skills.sh / GitHub Search API）。

## 坑

- GitHub 搜索 API 共享限流：并发 403 时错峰 / 重试。
- `gh search code 'filename:SKILL.md 中文词'` 基本失效。
- skills.sh 页面无公开 JSON API。
