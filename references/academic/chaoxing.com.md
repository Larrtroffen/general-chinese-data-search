# chaoxing.com —— 超星发现与期刊检索

超星数字资源平台（含超星期刊 `qikan.chaoxing.com`、发现系统）。**主站首页可匿名打开，但检索功能一律跳登录墙，curl 不可用。**

- 去哪找：门户首页 `https://www.chaoxing.com/`；超星期刊检索 `https://qikan.chaoxing.com/search?sw={关键词}`
- 什么时候用：超星期刊 / 超星发现系统的中文期刊检索；已有学习通或机构账号时要看超星全文
- 怎么搜：检索入口 `https://qikan.chaoxing.com/search?sw={关键词}` —— 未登录会 302 → `https://fxlogin.chaoxing.com/findlogin.jsp?backurl=…&product=qikan`；有账号时用可见浏览器登录（`headed: true, persist: true` 保活），再在站内检索
- 覆盖：超星期刊 + 发现系统；详情/全文需登录
- 门槛：首页免费；检索/全文需学习通账号或机构权限
- 实测：2026-10-02，macOS + curl 8.x（desktop UA）：
  - `GET https://www.chaoxing.com/` → `HTTP 200 size=579828`，`<title>超星</title>`（门户首页，非检索）
  - `GET https://qikan.chaoxing.com/search?sw=基层治理` → 最终 `url=https://fxlogin.chaoxing.com/findlogin.jsp?backurl=https%3A%2F%2Fqikan.chaoxing.com%2Fsearch%3Fsw%3D…&product=qikan`，`HTTP 200 size=98`，正文"您好，请查看您的浏览器是否已经禁用cookie功能…"
- 上游：`https://www.chaoxing.com/`

## 细节

| 入口 | 状态 | 现象 |
|---|---|---|
| `https://www.chaoxing.com/` | ✅ | HTTP 200（`<title>超星</title>`，门户首页，非检索） |
| `https://qikan.chaoxing.com/search?sw={关键词}` | ❌→登录 | 302 → `https://fxlogin.chaoxing.com/findlogin.jsp?backurl=…&product=qikan`，正文提示"请查看您的浏览器是否已经禁用cookie功能"（登录跳转壳） |
| 全文阅读/下载 | ❌ | 需登录（学习通账号）或机构权限 |

- 中文论文的公开检索优先用 `references/academic/ncpssd.org.md`（JSON API 直连）与 `references/academic/cqvip.com.md`（首页结果 curl 可读）。

## 坑

- 首页 200 会误导；实际检索入口 `qikan.chaoxing.com` 必然跳登录，别在首页上浪费时间。
- 跳转壳页正文只说"检查 cookie"，但这其实是登录重定向后的提示，**不要误判为 cookie 问题**——判据是最终 URL 落在 `fxlogin.chaoxing.com`。
