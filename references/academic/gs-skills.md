# gs-skills —— Google Scholar 浏览器抓取 6 技能

Google Scholar **没有公开 API**；本 repo 把"搜论文 / 引文追踪 / 全文链接 / 翻页 / 导出 Zotero"做成 6 个 skill，靠**可见 Chrome + 远程调试**（Chrome DevTools MCP）注入 JS 解析 DOM。对我们的价值：它给出了 Google Scholar 的 **URL 参数表、结果页 CSS 选择器、`data-cid` 主键、BibTeX→Zotero 全链路**——本环境把 `mcp__chrome-devtools__*` 换成 eval 的 `browser` 命名空间即可复用（映射思路同 `cnki.net.md`）。

- 去哪找：repo `https://github.com/cookjohn/gs-skills`（约 0.4MB，可 `git clone --depth 1`；本机直连 github.com:443 被墙，改用 `gh api repos/cookjohn/gs-skills/tarball | tar xz`）。技能：`skills/gs-search|gs-advanced-search|gs-cited-by|gs-fulltext|gs-navigate-pages|gs-export/SKILL.md`，编排 agent：`agents/gs-researcher.md`，Zotero 推送脚本：`skills/gs-export/scripts/push_to_zotero.py`
- 什么时候用：要**谷歌学术**这一路（国际文献、被引次数、`cited by` 引文链、BibTeX/导出 Zotero、找 OA/Sci-Hub 链接）时。中文库（知网/万方/维普）走本层其他文件
- 怎么取：
  - 搜索页 URL 模板（`hl=en` 固定、`num=10` 降验证码风险）：
    `https://scholar.google.com/scholar?q=<关键词>&hl=en&num=10`
  - 高级检索参数：`as_sauthors`(作者) `as_publication`(期刊) `as_ylo`/`as_yhi`(起止年) `as_epq`(精确短语) `as_oq`(OR) `as_eq`(排除) `as_occt=title`(仅标题) `num`(≤20) `hl`。
  - 结果选择器：容器 `#gs_res_ccl .gs_r.gs_or.gs_scl`；题名 `a`（在 `.gs_rt`）；作者/刊/年 `.gs_a`（按 `" - "` 切段）；被引 `.gs_fl a[href*="cites"]`；全文/PDF `.gs_ggs a`（或 `.gs_or_ggsm a`）；摘要 `.gs_rs`；总数 `#gs_ab_md`；**主键 = 条目属性 `data-cid`**（集群 ID，跨技能复用）。
  - 被引链：`scholar?cites=<data-cid>`；引用弹窗：`scholar?q=info:<data-cid>:scholar.google.com/&output=cite`（取 `#gs_citi a` 的 BibTeX 链接）。
  - BibTeX 内容在 `scholar.googleusercontent.com`（CORS 挡 fetch）→ 必须**导航到该 URL 再读 `document.body.innerText`**。
  - 推送 Zotero：脚本打本机 `http://127.0.0.1:23119/connector`，头 `X-Zotero-Connector-API-Version: 3`，三步 `saveItems`→下载 PDF→`saveAttachment`（201=成功，409=已存在视作成功）。
  - 安装（上游）：`claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest` + `cp -r skills/ agents/ .claude/` + `chrome --remote-debugging-port=9222`。
- 覆盖：Google Scholar 索引的全学科（含中文文献的英文记录、被引数、版本聚类）。更新随 Google 实时索引。许可 **MIT**
- 门槛：**必须可见 Chrome**（本机只有 headless daemon，谷歌学术会识别并给验证码）；**大陆直连 scholar.google.com 不通**（需代理）
- 实测：2026-10-02，macOS + curl。`https://scholar.google.com/scholar?q=organoid&hl=en` → **连接失败 `HTTP 000`**（本机/本地区不可达，需代理）；`https://scholar.cnki.net/` → `HTTP 200`（3300B，仅登录页壳）。**本机未跑 gs-skills 脚本**（未装 Chrome DevTools MCP / 无可见 Chrome），选择器与 URL 参数为**上游声明**
- 上游：`https://github.com/cookjohn/gs-skills`（MIT）

## 细节

### 6 个技能（对应「要什么」）

`gs-search`（关键词搜索，返回题名/作者/刊年/被引/全文链接/`data-cid`）、`gs-advanced-search`（作者/期刊/年份/精确短语/仅标题过滤）、`gs-cited-by`（按 `data-cid` 找引用者）、`gs-fulltext`（PDF/DOI/出版商/Sci-Hub 链接）、`gs-navigate-pages`（翻页）、`gs-export`（BibTeX → Zotero）；`agents/gs-researcher.md` 负责编排与验证码检测。

## 坑

- **CAPTCHA 无法自动解**：技能的做法是检测 `#gs_captcha_ccl` / "unusual traffic" 后暂停等人工。
- 无 API、无 OCR，改版即选择器失效；频率高会被限流。
- `gs-fulltext` 会给 `sci-hub.ru/<doi>` 链接（合规与版权风险自担）。
