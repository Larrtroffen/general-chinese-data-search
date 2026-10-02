# chinaso.com —— 国家权威检索（本机不可用）

中国搜索（新华社背景的国家权威搜索引擎）。站点可达，但检索页是纯 Vue 单页应用（HTML 内无结果），其内部 API 对本机 IP 返回 `ip control` —— 本环境程序化取不到结果。

- 去哪找：`https://www.chinaso.com/`（首页）· `https://www.chinaso.com/newssearch/index.html?q={q}`（检索页，需 JS 渲染）
- 什么时候用：需要国家权威源（新华社背景）检索 —— 但本机取不到结果，仅作留档
- 怎么搜：`curl -s -m 20 -A "$UA" 'https://www.chinaso.com/'` 可达；检索页 `.../newssearch/index.html?q={q}` 只返回 67 KB SPA 外壳；内部 API `https://www.chinaso.com/v5/general/v1/web/search?q={q}&pn=1&ps=10` 对本站 IP 返回 `ip control`。结果形态：SPA 空壳 / API 被 IP 管控
- 覆盖：国家权威源索引；年代/粒度依站点（本机不可用，未测）
- 门槛：需可见浏览器渲染 + 非受限出口 IP（本机 IP 被 `ip control`）；备用域名 `so.chinaso.com` 不可达
- 实测：2026-10-02，macOS + curl —— 首页 200、检索页 SPA 空壳、内部 API 返回 `ip control`、备用域 000；完整记录见下
- 上游：站点自身入口（无 repo/Skill 出处）

## 细节

### 可用性矩阵（本机实测 2026-10-02）

| 通道 | URL | 状态 | 现象 |
|---|---|---|---|
| 首页 | `https://www.chinaso.com/` | ✅ | 200，48074 B，`<title>中国搜索-国家权威搜索引擎` |
| 检索页 | `https://www.chinaso.com/newssearch/index.html?q={q}` | ❌ | 200，67941 B，但为 Vue SPA（`chunk-vendors.js`/`app.js`），HTML 内 `{q}` 出现 0 次、无结果 DOM |
| 结果页变体 | `https://www.chinaso.com/newssearch/all/allResults?q={q}` | ❌ | 200，67941 B，同样是 SPA 空壳 |
| 内部 API | `https://www.chinaso.com/v5/general/v1/web/search?q={q}&pn=1&ps=10` | ❌ | 200，41 B，`{"status":2,"msg":"ip control","data":{}}`；加 `Referer`/`Origin`/`X-Requested-With`/Cookie 后**仍同** |
| 备用域名 | `https://so.chinaso.com/` | ❌ | status 000（连接失败/不存在） |

### 请求模板（仅供浏览器路线参考）

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
curl -s -m 20 -A "$UA" -o /dev/null -w '%{http_code}\n' 'https://www.chinaso.com/'
# 检索页（需浏览器渲染）
open "https://www.chinaso.com/newssearch/index.html?q=$(python3 -c 'import urllib.parse;print(urllib.parse.quote("街乡吹哨"))')"
```

### 逆向后发现的接口（本机被封，留档）

从 `https://www.chinaso.com/newssearch/js/app.7e0625c2.js` 提取到：

- API 基址 `https://www.chinaso.com/v5`；资讯搜索端点 `GET /general/v1/web/search`（前端名 `searchNews`）。
- 其余端点：`/general/v1/search/{app,baike,blockchain,en,game,image,story,suggest,video,youlist}`、`/general/v1/search/ipaccess/verifyres/`（IP 准入校验）。
- 请求参数名未从前端包中确定（包内未见 `ps/pn/page/size` 字面量），**未验证**。

### 结论

本环境 **❌ 不可用**（SPA + API IP 管控）。若确需中国搜索，走可见浏览器（chrome-devtools MCP）人工/半自动化检索。

### 实测记录（2026-10-02）

macOS + curl：

- `www.chinaso.com/` → 200，48074 B。
- `www.chinaso.com/newssearch/index.html?q=街乡吹哨` → 200，67941 B，SPA 外壳，`街乡吹哨` 出现 0 次。
- `www.chinaso.com/newssearch/all/allResults?q=街乡吹哨` → 200，67941 B，同上。
- `www.chinaso.com/v5/general/v1/web/search?q=街乡吹哨&pn=1&ps=10` → 200，`{"status":2,"msg":"ip control","data":{}}`。
- `so.chinaso.com/` → status 000。

## 坑

- 页面 200 ≠ 有结果：`newssearch` 是 SPA，`curl` 拿到的永远是 67 KB 外壳，必须 JS 渲染。
- 内部 API 有 **IP 管控**，带全套浏览器头/Cookie 仍返回 `ip control`；换出口 IP 或走浏览器 MCP 是唯一路径。
- 备用域名 `so.chinaso.com` 不可达，不要按历史资料尝试。
