# tools/ —— 取数能力层（浏览器 / 抓取 / 清洗 / OCR 工具）

与具体站点解耦的**能力层**：拿不到页面、页面太脏、文件是扫描件时，来这一层挑工具。原则：**先试零依赖/本机自带，再上要安装的重家伙**；每个工具卡都写明「何时用」与「本机实测到哪一步」。

## 文件一览

| 文件 | 来源 | 用途 | 状态 |
|---|---|---|---|
| `macos-vision-ocr.md` | Apple 系统框架 | 中文扫描件/图片 → 文本（Swift 6 行脚本） | ✅ 实测通过 |
| `mineru.md` | opendatalab | PDF/图片/Office → Markdown（云 API / 本地 CLI） | ⚠️ 输出为空 |
| `glm-ocr.md` | 智谱 zai-org | 中文表格/公式/手写 OCR（云需 key，本地需 GPU） | ⚠️ 未装未跑 |
| `defuddle.md` | kepano | HTML → 干净 Markdown / 元数据 | ⚠️ 未装未跑 |
| `scrapling.md` | D4Vinci | 反爬绕过（Cloudflare）、三级抓取、断点续爬 | ⚠️ 未装(Py3.10+) |
| `playwright-cli.md` | microsoft | 真实浏览器交互（ref 工作流）、会话/录屏/trace | ⚠️ 未装未跑 |
| `agent-browser.md` | vercel-labs | Native 浏览器 CLI；复用本机 Chrome 登录态 | ⚠️ 未装未跑 |
| `web.archive.org.md` | Internet Archive | 回捞已下线 / 改版的旧页面 | ❌ 本机不可达 |
| `r.jina.ai.md` | Jina | 第三方渲染网页 → Markdown | ❌ 本机不可达 |

> 「⚠️ 未装未跑」= 本轮只做只读侦察（不执行第三方安装），卡片里区分了「实测」「上游声明」；用之前**自己先探活**。

## 选路

### 按问题选（先看这张表）

| 你遇到的问题 | 用哪个 | 文件 |
|---|---|---|
| 扫描件/图片版 PDF/截图要转文字（最省事、零依赖、纯本地） | **macOS Vision OCR（首选）** | `macos-vision-ocr.md` |
| 中文表格→Markdown、公式→LaTeX、印章/复杂版式/手写（比 Vision 强） | GLM-OCR（需 key 或本地模型） | `glm-ocr.md` |
| 一份 PDF/Office/HTML 要整篇变 Markdown，且不想装东西（云端免 token 通道） | MinerU Agent 轻量 API | `mineru.md` |
| 抓回来的 HTML **只要正文**（去导航/广告/评论，省 token） | Defuddle | `defuddle.md` |
| 目标站有 **Cloudflare/强反爬**、要并发 + 断点续爬 | Scrapling | `scrapling.md` |
| 需要**真实浏览器点击/填表**、要留截图/trace 证据 | playwright-cli | `playwright-cli.md` |
| 要复用**本机 Chrome 已有登录态**，或要最省 token 地「读页面」 | agent-browser | `agent-browser.md` |
| 旧页面已下线/改版，要回捞 | Wayback（本机不可达，见下） | `web.archive.org.md` |
| 想用第三方渲染代理绕 JS | Jina Reader（本机不可达，见下） | `r.jina.ai.md` |

### 推荐流水线

`直连 curl（scripts/fetch.py，带编码处理）→ 被挡 → scrapling/浏览器 → HTML 脏 → defuddle → 是扫描件 → Vision OCR（不够用再 GLM-OCR/MinerU）→ 入库 → 本地检索（见 ../archives/local-search-tools.md）`。

### 本机网络限制速查（实测）

- `web.archive.org`：DNS 通、TCP 连不上 → CDX 枚举与快照抓取全废。
- `r.jina.ai` / `api.jina.ai` / `eu.r.jina.ai` / `s.jina.ai`：DNS 可解析、TCP 443 全超时；`curl` 表现为 `HTTP=000` + 45 s 空等。替代代理 `api.allorigins.win` → 500、`api.codetabs.com` → 522。
- **`huggingface.co` → HTTP 000（超时，不通）**；**`hf-mirror.com` → 200 且可下载**（CBDB 实测 302→206，见 `../archives/cbdb.md`）；`www.modelscope.cn` → 200。
- `github.com` 的 **git 协议不通**（`git clone` 75 s 超时）→ 改用 `gh api repos/<o>/<r>/tarball` 或 `raw.githubusercontent.com`（均实测可用）。
- npm：`registry.npmjs.org` 可达但慢（实测约 20 s）；Python：`pypi.org` 可达（`curl` 取 JSON 正常）。
- **判活顺序**：先 `nc -z -G 6 <host> 443`（几秒），通了再发 HTTP；不要用长超时硬等。

### 替代取数路径（本机可用，按优先级）

1. **直连 + 编码处理**：多数政府 / 媒体 / 数字报页面是静态 HTML（UTF-8 或 GBK/GB2312），`curl` 直取 + `iconv -f gb18030 -t utf-8` —— 见 `../gov/README.md`、`../media/README.md`。
2. **微信公众号正文**：签名链接直读 —— 见 `../wechat/README.md`。
3. **站内检索接口直调**：很多站点「检索页是壳、接口可用」，是比代理更稳的正路 —— 见 `../party/dangjian.cn.md`、`../party/cpc.people.com.cn.md`、`../media/people.com.cn.md`、`../academic/cnki/`；**SPA 站也能挖出开放 API**（范例见 `../archives/shtong.md`）。
4. **搜索引擎索引兜底**：`site:` 点查 —— 见 `../engines/README.md`（含内置 `web_search` 工具及其限流说明）。
5. **古籍/学术语料**：不要爬 `ctext.org`（见 `../archives/ctext.md`）→ 走 `../archives/kanripo.md`（raw 直取）。
6. **需要存档回捞**时：优先站内自存档（改版未删的旧文件）与数字报老 URL 规则直连；换网络环境后再试 Wayback / Jina。

## 相关

- 数据源总索引：仓库根 `SKILL.md`
- 本地检索（把抓到的东西变成可查索引）：`../archives/local-search-tools.md`
- 各层索引：`../engines/README.md`、`../gov/README.md`、`../party/README.md`、`../wechat/README.md`、`../social/README.md`、`../academic/README.md`、`../media/README.md`、`../archives/README.md`
