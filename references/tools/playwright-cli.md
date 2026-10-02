# playwright-cli —— 真实浏览器交互 CLI（ref 工作流）

`microsoft/playwright-cli`（Apache-2.0，npm 包名 **`@playwright/cli`**，v0.1.22，Node ≥18）：把 Playwright 包成 CLI + Skill。官方定位：**CLI + Skills 比 MCP 更省 token**（不把大 tool schema 和整棵无障碍树塞进上下文），适合「Agent 自己点页面、拿 ref 互动」的高吞吐场景。默认 headless，`--headed` 可见（用于人工过验证码）。

- 去哪找：仓库 https://github.com/microsoft/playwright-cli ；技能文件（安装后落到本地，可读）`skills/playwright-cli/SKILL.md` + `skills/playwright-cli/references/*.md`（test-generation / element-attributes / running-code / session-management / storage-state / tracing / video-recording / request-mocking / playwright-tests / pr-attachments）
- 什么时候用：需要**真实浏览器渲染 + 点击/填表/翻页**（检索结果要 JS 渲染、要点「下一页」、要选日期控件）；**需要人工介入的验证码**（`--headed` 起可见窗口）；要**保持登录态**跨多次调用（`--persistent`）或多会话并行（`-s=<name>`）；需要截图/PDF/录屏/trace 作**证据留档**
- 怎么用：`npm install -g @playwright/cli@latest` → `playwright-cli open <url>` → `snapshot`（拿 ref）→ `click e15` / `fill e5 "…"`；会话用 `--persistent` / `-s=<name>`；附件用 `screenshot --filename=…`
- 覆盖：真实浏览器（Chromium 系，`--browser=chrome` 指定通道）；命令集见下；含会话/录屏/trace/storage 管理；许可 Apache-2.0
- 门槛：Node ≥18（本机 `node -v` = v24.21.0，满足）；浏览器二进制 README 未写步骤（首次若报缺 Chromium，按 Playwright 常规 `npx playwright install chromium`，**本机未验证**）
- 实测：2026-10-02，macOS 27（arm64）——只读侦察（`gh api` 元数据、tarball 读 README/SKILL.md、npm registry 200）；**未 `npm i -g`、未实际驱动浏览器**
- 上游：https://github.com/microsoft/playwright-cli

## 细节

### 安装

```bash
npm install -g @playwright/cli@latest
playwright-cli --help
playwright-cli install --skills      # 给 Claude Code / Copilot 等装本地技能（可选）
```

### ref 工作流

```bash
playwright-cli open https://example.com --headed   # 起浏览器并导航；--browser=chrome 指定通道
playwright-cli snapshot                            # 拿无障碍树 + ref（e1/e2/e15…）
playwright-cli click e15
playwright-cli fill e5 "海淀区" --submit            # --submit 填完回车
playwright-cli find "下一页"                        # 在快照里搜文本（--regex，支持 /i）
playwright-cli eval "document.title"               # 任意 JS；eval "el => el.id" e5
playwright-cli screenshot --filename=page.png      # 也支持 pdf / --hires
playwright-cli close
```

### 会话与持久化

```bash
playwright-cli open https://playwright.dev --persistent      # profile 落盘，cookies/storage 保留
playwright-cli -s=proj2 open https://example.com             # 具名会话；PLAYWRIGHT_CLI_SESSION 环境变量可预设
playwright-cli list | close-all | kill-all
playwright-cli show                                          # 可视化面板：实时看/接管所有会话（含 screencast + 远程控制）
playwright-cli attach / detach                               # 接管已开的外部浏览器会话
```

其它：`go-back/go-forward/reload`、`press/keydown/keyup`、`mousemove/mousedown/mouseup/mousewheel`、`select/hover/drag/drop/upload/check`、`tab-list/tab-new/tab-select/tab-close`、`storage`（cookies/localStorage）、`recording-start`、`resize`、`dialog-accept/dismiss`。headless 会话空闲 1 小时自关（`open --idle-timeout=<ms>` 可调，0 = 不关）。

**不需要写测试时**：`running-code.md` 参考里给了「用 CLI 直接跑 Playwright 代码片段」的做法；需要回归用例时再看 `playwright-tests.md` / `test-generation.md`。

### 实测记录（2026-10-02）

macOS 27（arm64）。`gh api repos/microsoft/playwright-cli` → `size=1025 KB`、`license=Apache-2.0`、`pushed_at=2026-09-28`；tarball 解包读 README + `skills/playwright-cli/SKILL.md`（命令集与 ref 工作流如上）；`npm registry` 可达：`curl https://registry.npmjs.org/@playwright/cli/latest` → **HTTP 200**，`version 0.1.22`、`engines.node >=18`；本机 `node -v` = v24.21.0（满足）。**未 `npm i -g`、未实际驱动浏览器**（遵守「不执行第三方安装」纪律；上游声明，未本机实测）。

## 坑

- **浏览器二进制**：README 未写「装浏览器」步骤（skills/CLI 只提 `install --skills`）。首次跑若报缺 Chromium，按 Playwright 常规做法 `npx playwright install chromium`（**本机未验证**）。
- 版本标签：npm 上 `@playwright/cli@0.1.22` 依赖 `playwright@1.64.0-alpha-*`（alpha 版），升级别锁死。
- `eval` 能跑任意 JS → 只在可信页面上用；`--persistent` 会把 cookie 落盘，敏感站点注意文件权限。
- headless 仍可能被目标站识别（与 `--headless=new` 同级问题）；过验证码必须 `--headed` + 人工。
- 长任务注意 1 h 空闲超时。

> 分工：只要可见浏览器 + ref 交互 → 本工具；要复用**本机 Chrome 的既有登录 cookie**、或要更省事的快照读取 → `agent-browser.md`；反爬封 IP/Cloudflare → `scrapling.md`。
