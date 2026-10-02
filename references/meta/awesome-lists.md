# awesome-lists —— 技能与工具目录、市场入口

- 去哪找：主入口 `https://skills.sh/`、`https://github.com/anthropics/skills`、`https://modelscope.cn/brand/view/MCP`、`https://bailian.console.aliyun.com/?tab=mcp`；完整清单见「细节」两张表。
- 什么时候用：要新能力、要查「某平台有没有现成工具/接口」、或定期巡检生态时，从本表挑一个入口。
- 怎么搜：按「skills.sh（英文词）→ GitHub `gh search repos`（中英文）→ awesome 清单 / MCP 市场」顺序逛。与 `skills-discovery.md` 分工：本文件是**入口清单**（去哪逛），skills-discovery 是**命令流程**（怎么搜）。
- 覆盖：Agent Skills 目录与榜单、MCP 目录与市场、法律类专集；合计 20+ 入口。
- 门槛：多数入口免 key；魔搭 / 百炼 / clawhub 需登录或平台账号。
- 实测：2026-10-02，`gh api` / curl 侦察（星数 / 日期为当日快照）；⭐ 会漂移，仅作量级参考。
- 上游：各入口链接见「细节」两表。

## 细节

### 一、技能目录（Agent Skills）

| 入口 | 链接 | 里面有什么 | 怎么用 |
|---|---|---|---|
| anthropics/skills ⭐179k | https://github.com/anthropics/skills | 官方技能库：skill-creator、mcp-builder、pdf/docx/xlsx/pptx（source-available） | 读 `skills/<name>/SKILL.md`；学写法与参考实现 |
| vercel-labs/skills ⭐33k | https://github.com/vercel-labs/skills | `npx skills` 工具本体 + find-skills（3.7M 装） | 已装；`npx skills find/add` |
| obra/superpowers ⭐294k | https://github.com/obra/superpowers | 技能框架/方法论（生态事实标准之一） | 学 SKILL.md 结构与方法论 |
| skills.sh 榜单 | https://skills.sh/ | 全生态按安装量排行；单技能页可 curl | `npx -y skills@latest find <英文词>` |
| ComposioHQ/awesome-claude-skills ⭐76k | https://github.com/ComposioHQ/awesome-claude-skills | 社区 awesome 清单（最大） | 浏览 + 顺藤摸瓜 |
| travisvn / BehiSecc / VoltAgent / libukai / heilcheng 等 awesome-agent-skills | 各 repo（15k/10k/35k/5k/6k ⭐） | 多份并行社区清单（内容互有差异） | 交叉对照，找漏网技能 |
| lawve-ai/awesome-legal-skills ⭐763 | https://github.com/lawve-ai/awesome-legal-skills | 法律领域技能专集 | 法律类巡检入口 |
| agentskills.io | https://agentskills.io | Agent Skills 标准说明 | 写技能时对齐规范 |

### 二、MCP 目录与市场

| 入口 | 链接 | 里面有什么 | 备注 |
|---|---|---|---|
| **awesome-china-mcp** ⭐15 | https://github.com/zackchewa/awesome-china-mcp | 中国应用 MCP（87 仓库）+ 91 项官方 API gap map | **已摘录** → `awesome-china-mcp.md` |
| punkpeye/awesome-mcp-servers ⭐96k | https://github.com/punkpeye/awesome-mcp-servers | 全球 MCP 总目录 | 数量最大；中文条目少 |
| 魔搭 ModelScope MCP 广场 | https://modelscope.cn/brand/view/MCP | 1400+ servers（国内最大社区） | 闭源平台；需登录浏览 |
| 阿里百炼 MCP 市场 | https://bailian.console.aliyun.com/?tab=mcp | ~184 官方 + 2900+ 第三方 | 托管式（OAuth 代管）；闭源 |
| clawhub.ai | https://clawhub.ai/ | 官方 Agent Skill 分发（如 Flova 视频生成） | 新市场，条目尚少 |
| mcp.so / glama.ai / smithery.ai | mcp.so · glama.ai · smithery.ai | 第三方 MCP 搜索/托管 | 页面可 curl；无公开 JSON API |

### 三、用法建议

1. **先查已摘录**：`awesome-china-mcp.md`（中国平台）+ 各层 `README.md`（我们自己的源）。
2. **再逛市场**：找 MCP/技能时按「skills.sh（英文词）→ GitHub `gh search repos`（中英文）→ awesome 清单」顺序。
3. **核验再记录**：任何候选按 `skills-discovery.md` 的流程取元数据+正文，写进根目录 `CANDIDATES.md` 后再进入收编。
