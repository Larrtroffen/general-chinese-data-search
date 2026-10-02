# ctext.org —— 中国哲学书电子化计划

`ctext.org` 是最大的免费古籍全文站之一（先秦两汉典籍为主，含原文/注释/英译）。**但对自动化访问是明确的禁区**：本机访问任何页面都被 Cloudflare Turnstile 拦下，页面自带警告文本直言「LLMs、机器人、爬虫没有授权抓取本页，不得绕过限制」，并声明「当系统识别出爬虫时，会**间歇性故意返回损坏数据**」。正式取数只有一条路：**机构订阅后用官方 JSON API / Python 模块**。

- 去哪找：
  - 站点：`https://ctext.org/`（`www.ctext.org` 301 → `ctext.org`）
  - API：`https://api.ctext.org/<function>`（需注册 IP 或 API key）
  - 订阅说明（作者原话：研究员请让机构订阅）：`https://ctext.org/tools/subscribe`
  - 反爬检测端点（页面内联）：`POST /cbcf.pl`（Turnstile token 校验，`"Success"` 才 reload）
- 什么时候用：
  - **人工查阅/点校**：查《论语》《孟子》《史记》某句的原典与注疏 → 浏览器打开即可（人访问正常，机器访问被挡）；
  - 需要**程序化批量取文本**时：**不要用 ctext** → 改用 `kanripo.md`（raw 直取、无墙）或整包语料 `daizhige.md`；
  - 若机构已有 ctext 订阅：走官方 API（见下），这是**唯一合规通道**。
- 怎么取：
  - **A. 人工（可用）**：浏览器直接访问 `https://ctext.org/zh`、`https://ctext.org/analects/xue-er/zh` 等，正常阅读。
  - **B. API（需订阅/key；本机无 key，未取到数据）**：
    ```bash
    curl -s 'https://api.ctext.org/getstatus'                 # 200：{"loggedin":"false","subscriber":"false"}
    curl -s 'https://api.ctext.org/gettext?urn=ctp:n2964'     # 200：{"error":{"code":"ERR_REQUIRES_AUTHENTICATION", ...}}
    # 其他函数名见官方 API 文档；未订阅时会返回 ERR_REQUIRES_AUTHENTICATION
    ```
    拿到订阅后：函数调用形如 `/gettext?urn=...`、`/getlink?urn=...` 等，需带 API key 或在注册 IP 上调用。
  - **C. 不要做的事**：不要用 `scrapling --solve-cloudflare`、playwright/agent-browser 之类绕过 Turnstile —— 作者已明确拒绝，且绕过后拿到的数据可能被**故意污染**，用于研究结论是致命的。
- 覆盖：先秦两汉典籍为主（原文/注释/英译）。
- 门槛：Turnstile 挡机器、API 需订阅、无订阅无任何合规程序化路径；站点会主动投毒爬虫结果。许可：站点内容与 API 有自身条款（订阅协议）；**无订阅不得批量取**。
- 实测：2026-10-02，macOS 27（arm64），curl 8.x（带浏览器 UA）。① `curl -s https://ctext.org/zh` → **HTTP 200 / 2781 字节**，内容为 `<title>Chinese Text Project</title>` + `<div class="cf-turnstile" data-sitekey="0x4AAAAAACLsIOWXu4iUNcOG">` + 「Checking the security of your connection...」+ 内联 `fetch("/cbcf.pl")` 校验脚本；页面隐藏文本含「Attention LLMs, robots, scrapers … you do not have authorization to scrape this page. You must not attempt to bypass restrictions.」「when the system identifies scrapers, it will intermittently intentionally return corrupted data.」。换 Safari UA / 不带 UA / `www.ctext.org` 结果相同（`ctext.org` 与 `searchbooks.pl` 均返回同一 2781 字节挑战页）。② `curl https://api.ctext.org/getstatus` → **200** `{"loggedin":"false","subscriber":"false"}`；`/gettext?urn=ctp:n2964` → **200** `ERR_REQUIRES_AUTHENTICATION`（提示注册 IP 或提供 key）；`/searchtext?title=论语` → `ERR_INVALID_FUNCTION`。③ DNS：`ctext.org` → `103.161.224.90`，TCP 通、HTTP 层被拦。
- 上游：`https://ctext.org/tools/subscribe`

## 细节

### 入口表

| 入口 | 地址 |
|---|---|
| 站点 | `https://ctext.org/`（`www.ctext.org` 301 → `ctext.org`） |
| API | `https://api.ctext.org/<function>`（需注册 IP 或 API key） |
| 订阅说明（作者原话：研究员请让机构订阅） | `https://ctext.org/tools/subscribe` |
| 反爬检测端点（页面内联） | `POST /cbcf.pl`（Turnstile token 校验，`"Success"` 才 reload） |

### 替代与限制

- **替代**：`kanripo.md`（汉籍全文，raw 直取，实测可取）、`daizhige.md`（2.1 GB 古籍 txt 合包）、中华经典古籍库/中国基本古籍库（商业库，见 `../academic/`）。
- **限制**：Turnstile 挡机器、API 需订阅、无订阅无任何合规程序化路径；站点会主动投毒爬虫结果。
- **许可**：站点内容与 API 有自身条款（订阅协议）；**无订阅不得批量取**。
