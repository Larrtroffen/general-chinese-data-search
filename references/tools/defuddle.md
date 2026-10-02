# defuddle —— HTML 正文抽取（→ 干净 Markdown）

`kepano/defuddle`（MIT，v0.19.4，Node/TS）从网页里抽正文，返回清洗后的 HTML 或 **Markdown**。定位接近 Mozilla Readability 的替代品：更宽容（少删不确定元素）、脚注/数学公式/代码块输出一致、会读页面移动端样式来猜垃圾元素、抽更多元数据（含 schema.org）。它是 Obsidian Web Clipper 的引擎，也可独立用在 Node/CLI。

- 去哪找：仓库（CLI + 浏览器/Node 两套 API）https://github.com/kepano/defuddle ；SKILL 版本（kepano 自己写的用法卡）https://github.com/kepano/obsidian-skills → `skills/defuddle/SKILL.md`
- 什么时候用：抓回来的页面是**整页 HTML**，要的是正文（`<nav>/<aside>/<footer>/` 广告/评论全部去掉，**省 token**）；公众号/新闻/政府公告页取正文 → Markdown 归档；需要结构化元数据（title/author/domain/published）做去重键
- 怎么用：`npm install -g defuddle`（或用 `npx defuddle parse <url|file>`）；`defuddle parse <url> --md`（跑批一律加 `--md`）、`--json`、`--frontmatter`、`-p title`、`--user-agent`
- 覆盖：通用网页正文；**对 JS 渲染页无效**（它只处理你给它的 HTML —— URL 模式内部自己抓，仍受目标站反爬限制）；中文站无特殊适配，分栏/表格/PDF 嵌入未必理想；许可 MIT
- 门槛：需 Node（≥18 即可，无硬性版本声明）；本机 Node v24.21.0 可用
- 实测：2026-10-02，macOS 27（arm64）——只读侦察（`gh api` 元数据、tarball 读 `package.json`/README、读 obsidian-skills 的 SKILL.md）；**未 `npm i`、未跑 CLI**
- 上游：https://github.com/kepano/defuddle

## 细节

### 安装

```bash
npm install -g defuddle          # 全局装，得到 defuddle CLI
npx defuddle parse <url|file>    # 不想装就用 npx
```

### CLI（接受 URL / 本地文件 / stdin 管道）

```bash
defuddle parse https://example.com/article --md            # 输出 Markdown（跑批一律加 --md）
defuddle parse page.html --md -o content.md                # 落盘
curl -L https://stephango.com/saw | defuddle parse --markdown   # 先自己抓、再清洗（推荐：可复用本仓 fetch 脚本 + 编码处理）
defuddle parse page.html --json                            # 含元数据 + HTML/Markdown
defuddle parse page.html -p title                          # 只取某字段（title/description/domain…）
defuddle parse page.html --frontmatter                     # Markdown 前加 YAML frontmatter
defuddle parse <url> --user-agent "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) ..."   # 目标站 403 时换 UA
```

常用参数：`-o/--output`、`-m/--markdown|--md`、`-j/--json`、`-f/--frontmatter`、`-p/--property`、`--debug`。

### Node API

浏览器里 `new Defuddle(document).parse()`；Node 里 `import { Defuddle } from 'defuddle/node'`，先自己用 **linkedom / JSDOM / happy-dom** 造 DOM（注意 `package.json` 需 `"type": "module"`）。依赖仅 `commander` + `mathml-to-latex`，很轻。

### 实测记录（2026-10-02）

macOS 27（arm64）。`gh api repos/kepano/defuddle` → `size=4015 KB`、`license=MIT`、`pushed_at=2026-09-28`；tarball 解包读 `package.json`（`version 0.19.4`、`bin.defuddle=dist/cli.js`、deps `commander@^12.1.0` + `mathml-to-latex@^1.8.0`）与 README 全文；另读 `kepano/obsidian-skills` 的 `skills/defuddle/SKILL.md`（其推荐用法为 `defuddle parse <url> --md`）。**未 `npm i`、未跑 CLI**（遵守「不执行第三方安装」纪律；上游声明，未本机实测）。

## 坑

- ⚠️ 默认 UA 会被部分站 403 → 用 `--user-agent` 传浏览器 UA（和本仓 `scripts/fetch.py` 的 UA 一致）。
- 保真优先时用 `--json` 拿 HTML 再自行处理（分栏/表格/PDF 嵌入未必理想）。
- **许可 MIT**，可放心进流水线（但我们只记录用法，不把代码拷进本仓）。
