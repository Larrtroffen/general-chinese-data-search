# baidu.com —— 中文综搜兜底

百度网页搜索（桌面 + 移动两套端点）。结果直出 HTML（非 JS 渲染）：桌面版结构最好解析，但翻页/连发即 302 到图形验证码；移动版 `m.baidu.com` 无验证码且可翻页，代价是类名混淆 + 链接加密，精确 URL 提取成本高。

- 去哪找：`https://www.baidu.com/s?wd={q}`（桌面）· `https://m.baidu.com/s?word={q}`（移动）
- 什么时候用：中文网页兜底召回；按「年份词 + 单位名」放量找转载源；「已知某标题/某站有文，找网页版」的点查
- 怎么搜：桌面 `curl -s -m 20 -A "$UA" "https://www.baidu.com/s?wd=$Q&rn=50"`；移动 `curl -s -m 20 -A "$MUA" "https://m.baidu.com/s?word=$Q&pn=0"`。参数 `wd`（桌面）/`word`（移动）= 关键词，`pn` = 起始序号（移动有效，桌面触发验证），`rn` = 每页条数（桌面，不严格生效）。结果形态：直出 HTML
- 覆盖：中文互联网网页；索引内全时段（无稳定时间过滤参数）；粒度 = 网页条目
- 门槛：无（本次未带 cookie jar 即拿到结果）；触发验证后带 cookie / 换 UA / 等待数分钟
- 实测：2026-10-02，macOS + curl（Chrome 桌面 UA / iPhone UA）——桌面首查 200 无验证、桌面翻页 302 图形验证码、移动查询/翻页 200 无验证；完整记录见下
- 上游：站点自身入口（无 repo/Skill 出处）

## 细节

### 可用性矩阵（本机实测 2026-10-02）

| 通道 | URL | 状态 | 现象 |
|---|---|---|---|
| 桌面首页检索 | `https://www.baidu.com/s?wd={q}&rn=50` | ✅ | 200，1184022 B；`<title>{q}_百度搜索`；`div.result.c-container`×23，`c-container`×111；无验证 |
| 桌面翻页 | `https://www.baidu.com/s?wd={q}&pn=20&rn=20` | ❌ | **302** → `https://wappass.baidu.com/static/captcha/tuxing_v2.html?...`（图形验证码） |
| 移动检索 | `https://m.baidu.com/s?word={q}` | ⚠️ | 200，2157277 B；`<title>{q} - 百度`；`c-result`×11，无验证；**但类名混淆、链接加密（见解析）** |
| 移动翻页 | `https://m.baidu.com/s?word={q}&pn=10` | ✅ | 200，1772230 B，无验证码；`pn` 生效 |

结论：**桌面版只做单次点查**（解析最简单）；**批量/翻页走 `m.baidu.com`**（不会被验证码挡），但要有心理准备：移动版的逐条真实 URL 需额外解析。

### 请求模板

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
MUA='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
Q='%E8%A1%97%E4%B9%A1%E5%90%B9%E5%93%A8'   # 街乡吹哨
curl -s -m 20 -A "$UA"  "https://www.baidu.com/s?wd=$Q&rn=50"      # 桌面单次点查
curl -s -m 20 -A "$MUA" "https://m.baidu.com/s?word=$Q&pn=0"       # 移动，pn=0/10/20…
```

参数：`wd`（桌面）/ `word`（移动）= 关键词；翻页 `pn` = 起始序号（0、10、20…，移动实测有效；桌面 `pn` 触发验证）；`rn` = 每页条数（桌面，不严格生效）。
Cookie：**非必需**——本次未带 cookie jar 即拿到直出结果。触发验证后再带 cookie/换 UA/等待数分钟。

### 解析要点

- **结果页是直出 HTML**（SSR），非 JS 渲染。
- **桌面（易解析，推荐）**：结果项 `div.result.c-container`；标题链接 `h3.t > a[href]`，`href` = `http://www.baidu.com/link?url=…` **302 跳转**（真实 URL 需 `curl -L` 跟随）。部分条目 `mu=` 属性含真实 URL。
- **移动（能取到结果，但难拿精确 URL）**：
  - `m.baidu.com` 页面里出现的 `wappass.baidu.com` 是**登录链接**，不是验证码（勿误判为被封）。
  - 结果块 `div.c-result`，但**类名混淆**（`card_3LdYr`、`title_4utjm`、`result-item_4VP8G` 等带随机 hash 后缀），**选择器不稳定**，勿硬编码完整类名。
  - 结果链接是 `https://m.baidu.com/from=…/tc?…` **加密跳转**：本机 `curl -L` 实测**不返回 302**，而是返回一个 ~1.1 KB 的 `http-equiv="refresh"` 页（部分为 `recommend_list_san`，即「相关搜索」卡，非结果）→ 精确 URL 需浏览器渲染或解析该 refresh 页。
  - 页面几乎不含外站明文 URL（2.1 MB 里仅 1 处 `m.sohu.com`，且在 CSS 里）；`data-log` 的 `mu` 字段仅个别自有卡片（如百科）有，**不能作为通用目标 URL 源**。
- 结果里混入大量百度自有卡片：AI 总结（「总结全网 N 篇结果」）、相关搜索、百科、推荐 —— 统计条数/提 URL 前需过滤。

### 实测记录（2026-10-02）

macOS + curl（Chrome 桌面 UA / iPhone UA）：

- `www.baidu.com/s?wd=测试&rn=50` → 200，1184022 B，`c-container`×111，`<title>测试_百度搜索`。
- `www.baidu.com/s?wd=街乡吹哨&pn=20&rn=20` → 302 → `wappass.baidu.com/static/captcha/tuxing_v2.html`。
- `m.baidu.com/s?word=街乡吹哨` → 200，2157277 B，`c-result`×11，无验证；共约 1.7 万汉字 / 103 个 `<script>`。
- `m.baidu.com/s?word=街乡吹哨&pn=10` → 200，1772230 B，无验证。
- 抽查 3 条 `m.baidu.com/from=…/tc?…` 链接 `-L` 跟随：均 200、~1.1 KB，`http-equiv="refresh"` 跳回 `m.baidu.com/s?word=…`（相关搜索卡）。

## 坑

- 桌面版第二次请求（尤其带 `pn`）即 302 到 `wappass` 图形验证码；滑块/图形 headless 无法过。
- 桌面结果链接几乎都是 `baidu.com/link?url=` 跳转，去重与域名判定必须解析后再做（不能用跳转 URL 判源）。
- **移动版不适合做「精确 URL 采集」**：加密跳转 + 混淆类名，提取成本高于收益；需要真实链接时优先用头条/必应 RSS/神马。
- 无稳定时间过滤参数；时间范围只能用「年份词」放量（与搜狗微信同法）。
