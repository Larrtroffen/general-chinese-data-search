# meta/ —— 元资源层（找「源」的地方）

本层不放具体数据源，放**目录、索引与发现机制**：当你要找的东西还不明确「去哪找」时，先来这一层。

## 文件一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `awesome-china-mcp.md` | `zackchewa/awesome-china-mcp`（CC0） | 中国应用 MCP 索引（87 仓库 + 91 项官方 API 入口，已摘录） | ✅ 已摘录 |
| `awesome-lists.md` | 自编（GitHub / skills.sh / MCP 市场等入口） | 技能目录 / 市场 / 榜单入口清单 | ✅ 自编 |
| `skills-discovery.md` | 自编（skills.sh / GitHub Search API） | 发现机制与命令流程（检索 / 核验 / 记录） | ✅ 自编 |
| `style.md` | 自编（全库规范） | 源卡与索引的写法规范（新增 / 转写都按此） | ✅ 规范 |

## 选路

- 要查「某国内平台 / 服务有没有 MCP 或官方 API」（小红书、地图、A股、企业信息、翻译 OCR…） → `awesome-china-mcp.md`。
- 要找技能 / 工具、巡检生态（skills.sh、ModelScope、百炼…） → `awesome-lists.md`。
- 要系统性地发现新 skill / 新源、给 `CANDIDATES.md` 补货 → `skills-discovery.md`。
- 写 / 改卡前对齐文件名、字段顺序、标题与索引规范 → `style.md`。

## 相关

- 收编候选池（含热度 / 依赖 / 证据 / 优先级）：仓库根 `CANDIDATES.md`。
- 发现到的东西的归宿：能当**源**的写进对应领域层（`../gov/`、`../stats/` …）；能当**能力**的写进 `../tools/`。
- 维护节奏：每季度按 `skills-discovery.md` 重跑一次，把新候选追加到 `CANDIDATES.md`。
