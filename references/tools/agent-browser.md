# agent-browser —— 浏览器 CLI，复用 Chrome 登录态

`vercel-labs/agent-browser`（Apache-2.0，npm `agent-browser` v0.38.2）：单个原生命令行二进制（daemon 不需要 Playwright/Node），面向 AI Agent 的浏览器自动化：`open` → `snapshot`（拿无障碍树 + `@eN` ref）→ `click/fill/get` → `screenshot`。最实用的一点：**能直接复用你本机 Chrome 的既有登录态**（`--profile Default`），以及 `--auto-connect` 接管已开着的 Chrome。

- 去哪找：仓库（README 极全，含全部子命令）https://github.com/vercel-labs/agent-browser ；文档站源码（cdp-mode / snapshots / network / diffing / debugging / proxy 等专页）在仓库内 `docs/src/app/**/page.mdx`
- 什么时候用：需要**已登录态**才能看的页面（要登录才能检索的库、要会员/单位账号的站）；需要**可见浏览器**手工过验证码；想在 Agent 循环里**最省 token 地读页面**（`read`）；多会话并行（`--session a` / `--session b`）
- 怎么用：`npm install -g agent-browser` → `agent-browser install`（首次下载 Chrome for Testing）；核心命令 `agent-browser --profile Default open <url>`（复用登录态）、`agent-browser read <url>`（读 agent-readable 文本）、`snapshot` + `click @e2`
- 覆盖：通用网页；Chrome/Chromium 系（Chrome for Testing）；含 `console`/`network`/`diffing`/`recording`/`profiler` 等子命令；许可 Apache-2.0
- 门槛：npm 全局安装 + 首次下载 Chrome for Testing（几百 MB）；构建源码才需 Node 24+/pnpm 11+/Rust，**只跑 daemon 不需要**（另一路 `brew install agent-browser` / `cargo install agent-browser`）
- 实测：2026-10-02，macOS 27（arm64）——只读侦察（`gh api` 元数据、tarball 读 README/`package.json`、CfT 源可达性 200）；**未安装、未跑命令**
- 上游：https://github.com/vercel-labs/agent-browser

## 细节

### 安装

```bash
npm install -g agent-browser      # 推荐（装原生 Rust 二进制）
agent-browser install             # 首次：下载 Chrome for Testing（会先自动探测已有 Chrome/Brave/Playwright/Puppeteer）
# 也支持：brew install agent-browser ｜ cargo install agent-browser
agent-browser upgrade             # 自动识别安装方式并升级
```

### 命令集

```bash
agent-browser open example.com                 # 起浏览器并导航（别名 goto/navigate）
agent-browser open --headed                    # 可见窗口（人工过验证码/滑块）
agent-browser snapshot                         # 无障碍树 + ref（点击用 @e2 形式）
agent-browser click @e2
agent-browser fill @e3 "test@example.com"
agent-browser get text @e1
agent-browser read https://example.com/a.html  # 不点页面，直接取"agent 可读"文本
agent-browser screenshot page.png
agent-browser close
# 传统选择器同样支持：click "#submit" / find role button click --name "Submit"
```

### 复用本机 Chrome 登录态（核心用法）

```bash
agent-browser profiles                          # 列出可用 Chrome profile
agent-browser --profile Default open https://需要登录的站/    # 复制 profile 到临时目录（只读快照，不动原 profile）
agent-browser --profile /path/to/dir open …     # 传路径 = 持久化 profile，跨重启保留
# 或接管"已经开着"的 Chrome：
#   macOS: /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
agent-browser --auto-connect state save ./my-auth.json
agent-browser connect 9222                      # 直连 CDP 端口
agent-browser --session agent1 --cdp 9222 --pin-tab open site-a.com   # 多会话共享一个 Chrome，各绑自己的 tab
```

### 其它高频

`tab list --json`（含稳定 CDP `targetId`）、`console --json`、`network`、`diffing`、`recording`、`profiler`、`get cdp-url`；`--hide-scrollbars false` 保留滚动条。MCP 模式可选工具档位（默认 `core`，`--tools all` 全量，或 `core,network,react` 组合）。

> 分工：本工具 ≈「Chrome 复用 + 快照读页」；playwright-cli ≈「Playwright 生态 / 测试 / 录屏 / trace」；反爬绕过（Cloudflare）→ `scrapling.md`；只要 HTML→Markdown → `defuddle.md`。

### 实测记录（2026-10-02）

macOS 27（arm64）。`gh api repos/vercel-labs/agent-browser` → `size=24472 KB`、`license=Apache-2.0`、`pushed_at=2026-10-01`；tarball 解包读 README（安装方式、`--profile`/`--auto-connect`/`--cdp`/`--pin-tab` 用法、Chrome for Testing 说明）与 `package.json`（`version 0.38.2`、`bin=agent-browser`、`engines.node >=24` 仅用于构建）。可达性：`https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json` → **200**；`storage.googleapis.com/chrome-for-testing-public/` → 403（桶根，符合预期）。**未安装、未跑命令**（遵守「不执行第三方安装」纪律；上游声明，未本机实测）。

## 坑

- **`--remote-debugging-port` 会把整台浏览器暴露在 localhost**：任何本地进程都能连 —— 只在可信机器上用，用完关 Chrome（README 原文警告）。
- `--profile <name>` 是**复制快照**（不动原 profile）；Windows 上 Chrome 开着时可能文件被锁，需先关。
- `agent-browser install` 从 **Chrome for Testing** 下载几百 MB：本机 CfT 版本清单 JSON **可达**（200），`storage.googleapis.com/chrome-for-testing-public/` 根路径 403（正常，下具体包即可）；**未实际下载**。
- 点击被 consent 弹窗/遮罩挡住时 CLI 会提前报错并指出遮挡元素 → 处理后再 `snapshot` 取新 ref；二进制版更新快（0.38.x），命令细节以 README 为准。
