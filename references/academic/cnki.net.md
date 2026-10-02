# cnki.net —— 知网论文·政报·年鉴主入口

中国知网主入口（论文/政报/年鉴）与验证码现状。**检索页需过滑块+拼图验证码，curl 与 headless 均不可用，须可见 Chrome 人工过码。** 完整操作手册（10 个子 skill）见本层 `cnki/` 子目录。

- 去哪找：检索 `https://kns.cnki.net/kns8s/search`；海外版 `https://chn.oversea.cnki.net`（实测页面不存在）；年鉴库总入口 `https://kns.cnki.net/res/cyfd`
- 什么时候用：知网专属内容（学位论文/政报/年鉴/期刊）；按来源类别（SCI/EI/CSSCI/北大核心/CSCD）筛选；导出 Zotero / GB/T 7714 引文
- 怎么搜：用可见浏览器打开 `https://kns.cnki.net/kns8s/search` 检索；验证码出现时检测 `#tcaptcha_transform_dy` 的 `getBoundingClientRect().top >= 0`，命中即暂停请人工过码（`browser.open({headed:true, persist:true})`）。各子 skill 的选择器与流程见下「细节」
- 覆盖：知网全库（期刊/学位/会议/报纸/年鉴/专利/标准…）
- 门槛：需登录或机构 IP 权限；页面带滑块+拼图验证码（`/verify/home?captchaType=blockPuzzle`）
- 实测：2026-10-03，macOS + curl（desktop UA）——`GET https://kns.cnki.net/kns8s/search` → 302 → `https://kns.cnki.net/verify/home?captchaType=blockPuzzle&ident=…&returnUrl=…`，`HTTP 200 size=2154`，`<title>安全验证</title>`
- 上游：`https://www.cnki.net/`；操作手册 `https://github.com/cookjohn/cnki-skills`

## 细节

### 本机状态速览

| 入口 | 状态 |
|---|---|
| `kns.cnki.net/kns8s/search` | ⚠️ 滑块+拼图验证码（`/verify/home?captchaType=blockPuzzle`），headless 过不去 |
| 海外版 `chn.oversea.cnki.net` | ❌ 页面不存在 |
| 万方/百度学术/维普/掌桥 | ⚠️ 各带滑块/登录验证码 |

### 迁移文档（来自 GitHub cookjohn/cnki-skills，Claude Code 版全套）

完整操作手册在本层 `cnki/` 子目录（一个子功能一个文件）：

| 文件 | 内容 |
|---|---|
| `cnki/README.md` | 上游总览：10 个子 skill、安装、依赖（Chrome DevTools MCP、Zotero） |
| `cnki/cnki-researcher.md` | 编排 agent：验证码检测（暂停请人工过码）、多标签管理、search→filter→export 流程 |
| `cnki/cnki-search.md` | 关键词基础检索（选择器表 + evaluate_script 代码） |
| `cnki/cnki-advanced-search.md` | 高级检索：作者/期刊/日期/来源类别（SCI/EI/CSSCI/北大核心/CSCD） |
| `cnki/cnki-parse-results.md` | 对已打开结果页重新解析 |
| `cnki/cnki-navigate-pages.md` | 翻页与排序 |
| `cnki/cnki-paper-detail.md` | 论文详情元数据（摘要/关键词等） |
| `cnki/cnki-journal-search.md` | 按刊名/ISSN/CN 找期刊 |
| `cnki/cnki-journal-index.md` | 期刊收录状态/影响因子 |
| `cnki/cnki-journal-toc.md` | 期刊目录浏览 |
| `cnki/cnki-download.md` | PDF/CAJ 下载（登录人工处理） |
| `cnki/cnki-export.md` | 导出 Zotero / GB/T 7714 引文 |
| `cnki/scripts/push_to_zotero.py` | Zotero 推送脚本（上游原件） |

### 工具映射（重要）

上游文档写的是 Claude Code 的 `mcp__chrome-devtools__*` 工具。在本 omp 环境用 **`browser` 工具**（eval 命名空间）等价替代：

| 上游调用 | 本环境等价 |
|---|---|
| `mcp__chrome-devtools__navigate_page` | `await tab.goto(url)`（先 `browser.open`） |
| `mcp__chrome-devtools__evaluate_script` | `await tab.evaluate(code)` 或 `tab.run({page})` 里的 `page.evaluate` |
| 上游 JS 里的 `document.querySelector…` | 原样可用（跑在真实页面） |
| 验证码处理 | 同样检测 `#tcaptcha_transform_dy` 的 `getBoundingClientRect().top >= 0`，出现即暂停请人工过码 |

上游全部选择器（`input.search-input`、`input.search-btn`、`.result-table-list tbody tr`、`td.name a.fz14` 等）与字段结构可直接复用，见各子文件"Verified selectors"表。

### 检索词经验（本类课题）

`吹哨报到`、`街乡吹哨 部门报到 试点 名单`、`"169个" 试点`、`孟天广 吹哨报到 145 名单`、`试点街乡镇 附录 名单`。学术文本通常只给数量（169）不给名单；论文附录需逐篇点开看。
