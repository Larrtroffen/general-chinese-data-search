# zhihu.com —— 检索与专栏均需登录

知乎的问答、专栏、搜索接口对**无 cookie 请求一律拒绝**：返回的不是验证码，而是「请登录」型 403/302。本机（无浏览器 cookie）实测：**检索、专栏正文都拿不到**，只能当「线索源（标题/URL）」用。

- 去哪找：首页 `https://www.zhihu.com/`、搜索页 `https://www.zhihu.com/search?type=content&q={kw}`、搜索 API `https://www.zhihu.com/api/v4/search_v3?t=general&q={kw}&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0`、专栏 `https://zhuanlan.zhihu.com/p/{id}`。
- 什么时候用：要知乎问答/专栏的**线索**（标题、URL、时间）；事件传播/民间讨论的补充交叉验证。
- 怎么搜：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
  Q='%E8%A1%97%E4%B9%A1%E5%90%B9%E5%93%A8'   # 街乡吹哨

  curl -s -o /dev/null -w '%{http_code} %{redirect_url}\n' -m 20 -A "$UA" 'https://www.zhihu.com/'
  curl -s -m 20 -A "$UA" -H 'x-requested-with: fetch' \
    "https://www.zhihu.com/api/v4/search_v3?t=general&q=$Q&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0"
  # → 403 {"error":{"need_login":true,...,"code":40353}}
  curl -s -o /dev/null -w '%{http_code}\n' -m 20 -A "$UA" 'https://zhuanlan.zhihu.com/p/454719522'   # → 403
  ```
  结果形态：403/302（需登录）；唯一可用路径见「细节·可用路径」。
- 覆盖：本机匿名**全不可用**；登录后可及搜索/问答/专栏正文（未本机验证）。
- 门槛：**需登录 cookie**（如 `z_c0`）及 v4 接口签名头（`x-zse-96` 一类）；无 cookie 一律 403/302
- 实测：2026-10-02，macOS（arm64），curl 8.x（`-m 20`，桌面 Chrome UA）：`www.zhihu.com/` → 302 `/signin?next=%2F`；`www.zhihu.com/search?type=content&q=街乡吹哨` → 403/694 B；`api/v4/search_v3?t=general&q=街乡吹哨&...` → 403，body `code:40353, need_login:true`；`zhuanlan.zhihu.com/p/454719522` → 403/694 B。另用内置 `web_search` 的 `site:zhuanlan.zhihu.com` 能取回标题/URL 列表（工具层，非直连）。
- 上游：https://www.zhihu.com/

## 细节

### 可用性矩阵（本机实测 2026-10-02，macOS + curl）

| 通道 | URL | 状态 | 现象 |
|---|---|---|---|
| 首页 | `https://www.zhihu.com/` | ❌ 302 | → `https://www.zhihu.com/signin?next=%2F`（`SIZE=47`） |
| 搜索页 | `https://www.zhihu.com/search?type=content&q={kw}` | ❌ 403 | 694 B 反爬页；去掉标签后正文只有「知乎，让每一次点击都充满意义 —— 欢迎来到知乎，发现问题背后的世界」 |
| 搜索 API | `https://www.zhihu.com/api/v4/search_v3?t=general&q={kw}&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0` | ❌ 403 | `{"error":{"need_login":true,"redirect":"https://www.zhihu.com/account/unhuman?type=U4E3Z1&need_login=true&session=…&next=%2Fsignin","code":40353,"message":"请您登录后查看更多专业优质内容。"}}` |
| 专栏文章页 | `https://zhuanlan.zhihu.com/p/{id}` | ❌ 403 | 694 B 同款反爬页 → **专栏也不能匿名读** |

### 为什么判「需登录」而不是「被封 IP」

- 403 响应体是明确的登录门：`error.need_login=true`、`error.code=40353`、`message="请您登录后查看更多专业优质内容。"`；另有 `redirect` 指向 `/account/unhuman?type=U4E3Z1`（风控判定页）。
- 首页 302 的目标是 `/signin`，不是验证码页。
- 因此换 IP 未必解决，缺的是**登录 cookie**（如 `z_c0`）以及 v4 接口所需的**签名头**（`x-zse-96` 一类）。

### 可用路径（按可行性排序）

1. **搜索引擎索引点查**：用内置 `web_search`（本次实测 `site:zhuanlan.zhihu.com 街道 吹哨报到` 能返回 5 条标题+URL）或 `../engines/` 里的引擎做 `site:zhihu.com {kw}` —— 但**落地页仍需登录才能读全文**，所以只能拿标题/时间/URL 做线索。
2. **人工登录 + 导出 cookie 再 curl**（至少 `z_c0`，配合 `x-zse-96` 等签名头）：**未验证**，本机无账号未尝试；headless 直连成功率通常很低。
3. **浏览器人工阅读**（登录态下）后手工摘录——量大时不现实。
4. 移动端/其他域名接口（如 `www.zhihu.com/api/v4/…` 之外的入口）：**未探测**。

## 坑

1. **403 ≠ 限流 ≠ 站点故障**：知乎给的是登录门 JSON（`need_login`/`code 40353`），重试无意义。
2. `www.zhihu.com/` 首页 302 到 `/signin`，容易被误判成「目标站挂了」。
3. 专栏 `zhuanlan.zhihu.com/p/{id}` 同样 403 → **不能靠专栏页绕过搜索登录门**；不要为「抓知乎专栏」设计流水线。
4. 内容与机构归属都不可靠（匿名答主、转载、情绪化表述）→ 若是为「官员/单位」语料做证据，知乎优先级应低于政府网站与官方媒体。
5. 未验证：cookie+签名方案是否有效、`api/v4/search_v3` 的完整参数（`t`/`correction`/`offset`/`limit`/`lc_idx`/`show_all_topics`）语义、返回结构与频率限制。
