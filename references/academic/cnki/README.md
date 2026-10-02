# cnki —— 知网检索手册索引

迁移自 [cookjohn/cnki-skills](https://github.com/cookjohn/cnki-skills) 的 Claude Code 全套操作手册（10 个子技能 + 1 个编排 agent）。本目录一个子功能一个文件，逐个给出页面入口、已验证选择器与 JS 片段。**知网整体入口与总卡见 [`../cnki.net.md`](../cnki.net.md)。**

## 文件一览

| 文件 | 用途 | 前置条件/状态 |
|---|---|---|
| `cnki-search.md` | 关键词基础检索，单次调用返回结果列表 | Chrome + DevTools MCP；⚠️ 未复测 |
| `cnki-advanced-search.md` | 高级检索：作者/期刊/日期/来源类别字段过滤 | 须用旧版 `kns/AdvSearch` 界面；⚠️ 未复测 |
| `cnki-parse-results.md` | 解析已打开的结果页为结构化数据 | 结果页需已打开；⚠️ 未复测 |
| `cnki-navigate-pages.md` | 结果翻页与排序 | 结果页；⚠️ 未复测 |
| `cnki-paper-detail.md` | 论文详情元数据（摘要/关键词/基金等） | 论文详情页；⚠️ 未复测 |
| `cnki-journal-search.md` | 按刊名/ISSN/CN 找期刊 | navi.cnki.net；⚠️ 未复测 |
| `cnki-journal-index.md` | 期刊收录状态与影响因子 | 期刊详情页；⚠️ 未复测 |
| `cnki-journal-toc.md` | 期刊目录浏览与原版目录下载 | 期刊详情页，下载需登录；⚠️ 未复测 |
| `cnki-download.md` | 下载论文 PDF/CAJ | 须登录知网且有下载权限；⚠️ 未复测 |
| `cnki-export.md` | 导出 Zotero / RIS / GB-T 7714 引文 | Zotero 桌面端 + Python 3；⚠️ 未复测 |
| `cnki-researcher.md` | 编排 agent：调度上述技能、验证码暂停、标签页管理 | Chrome + DevTools MCP；⚠️ 未复测 |
| `scripts/push_to_zotero.py` | Zotero Connector 推送脚本（上游原件） | Python 3；Zotero 需运行 |

## 与总卡的关系

- [`../cnki.net.md`](../cnki.net.md) 是知网**总卡**：总入口、本机验证码实测结论、以及 `mcp__chrome-devtools__*` 到本 omp 环境 **`browser` 工具**的等价映射。
- 本目录是**操作细节**：每个文件给页面路径、已验证选择器、可复制的 JS 片段与步骤顺序；总卡不重复这些细节。
- 上游文档写的是 Claude Code 的 `mcp__chrome-devtools__*` 调用；在本环境按总卡的映射表替换为 `browser` 下的 `tab.goto` / `tab.evaluate`，选择器与字段结构原样复用。

## 安装与前置

- 已安装 Claude Code CLI（或本 omp 环境）。
- Chrome + Chrome DevTools MCP：
  ```bash
  claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest
  ```
- 拉取上游技能本体：
  ```bash
  git clone https://github.com/cookjohn/cnki-skills.git
  cd cnki-skills && cp -r skills/ agents/ .claude/
  ```
- 启动带远程调试的 Chrome（下载与验证码需人工登录/过码）：
  ```bash
  # Windows
  "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
  # macOS
  /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
  # Linux
  google-chrome --remote-debugging-port=9222
  ```
- 可选：Zotero 桌面端（导出用）、Python 3（Zotero 推送脚本用）。

## 选路

- 关键词找论文 → `cnki-search`，再在结果页接 `cnki-parse-results` / `cnki-navigate-pages`。
- 要按作者、来源类别（SCI/EI/CSSCI/北大核心/CSCD）、年份精确过滤 → `cnki-advanced-search`。
- 看单篇元数据 → `cnki-paper-detail`；要存 PDF/CAJ → `cnki-download`。
- 期刊相关：找刊 → `cnki-journal-search`；查收录与影响因子 → `cnki-journal-index`；看目录/原版目录 → `cnki-journal-toc`。
- 把文献存进 Zotero 或导出 GB/T 7714 引文 → `cnki-export`（多篇用批量模式）。
- 多步流程（检索→筛选→详情→导出）、验证码暂停与标签页管理 → `cnki-researcher`。

## 设计要点（上游说明）

- 所有技能走 Chrome DevTools MCP 的异步 `evaluate_script`，无截图识别或 OCR；每步 1–2 次工具调用。
- 直接 `navigate_page` 而非点链接（知网会新开标签页）。
- 支持从结果页批量导出，免逐篇进详情页。
- 检测腾讯滑块验证码后暂停，等人工完成。

## 相关

- 知网总卡：[`../cnki.net.md`](../cnki.net.md)
- 邻近学术库：`../wanfangdata.com.cn.md`、`../cqvip.com.md`、`../chaoxing.com.md`
- 上游仓库：https://github.com/cookjohn/cnki-skills （License: MIT）
