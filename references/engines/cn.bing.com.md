# cn.bing.com —— 中文综搜 + RSS 纯文本流

必应中国站。返回直出 HTML/RSS，但**必须先预热 cookie**，否则结果被降级（只用首个词、返回通用结果）。本环境下 `first=` 翻页参数无效。

- 去哪找：`https://cn.bing.com/search?q={q}`（HTML）· 同 URL 加 `&format=rss`（RSS）；国际站 `https://www.bing.com/search?q={q}` 会 302 回中国站
- 什么时候用：中文综搜；要纯文本流做管道解析时用 RSS；标题/站内点查（`site:`）
- 怎么搜：先预热 cookie 再检索——`curl -s -m 20 -A "$UA" -c "$J" -o /dev/null 'https://cn.bing.com/'`，再 `curl -s -m 20 -A "$UA" -H 'Accept-Language: zh-CN,zh;q=0.9' -b "$J" -c "$J" 'https://cn.bing.com/search?q=…'`；RSS 加 `&format=rss`。参数 `q` 关键词（空格用 `+` 或 `%20`）、`count`（实测仍返回 10 条/页）、`first`（**实测无效**）、`format=rss`、`mkt`/`setlang`（未验证）。结果形态：直出 HTML 或 XML
- 覆盖：中文必应索引（按 IP 强制中国站，国际索引不可达）；粒度 = 网页条目；每页固定 10 条
- 门槛：需预热 cookie（**无 cookie 静默降级为「只匹配首词」**）
- 实测：2026-10-02，macOS + curl（Chrome 桌面 UA）——冷启降级、预热后相关、`first` 无效、RSS 直读；完整记录见下
- 上游：站点自身入口（无 repo/Skill 出处）

## 细节

### 可用性矩阵（本机实测 2026-10-02）

| 通道 | URL | 状态 | 现象 |
|---|---|---|---|
| 冷启（无 cookie）检索 | `https://cn.bing.com/search?q={q}&count=30` | ⚠️ | 200，102942 B；`b_algo`×10；结果**只匹配首词**（查「街乡吹哨」返回全是「街」的百科/字典） |
| 预热 cookie 后检索 | 同上（先 GET 首页建 cookie jar） | ✅ | 200，103937 B；结果相关（`12371.cn` 2019-07-18、`beijing.gov.cn`、`zt.bjcc.gov.cn`） |
| 翻页 | `&first=11` / `&first=31` / `&FORM=PERE` | ⚠️ | 200，但**返回与首页完全相同的 10 条**（首词 URL 级对比一致）；`first` 无效 |
| RSS | `&format=rss` | ✅ | 200，`text/xml`，6864 B，`<item>`×10；`first=11` 同样无效（内容逐字节相同） |
| 国际站 | `https://www.bing.com/search?q={q}` | ❌ | **302** → `https://cn.bing.com/search?q={q}`（按 IP 强制跳中国站；加 `&cc=US` 仍 302） |

结论：**先 `curl -c jar` 打一次 `https://cn.bing.com/`，再带 jar 检索**；RSS 是最省事的解析通道，但每页固定 10 条且翻不了页。

### 请求模板

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
J=/tmp/bing.ck
curl -s -m 20 -A "$UA" -c "$J" -o /dev/null 'https://cn.bing.com/'      # 预热 cookie（必需）
curl -s -m 20 -A "$UA" -H 'Accept-Language: zh-CN,zh;q=0.9' -b "$J" -c "$J" \
  'https://cn.bing.com/search?q=%E8%A1%97%E4%B9%A1%E5%90%B9%E5%93%A8+%E9%83%A8%E9%97%A8%E6%8A%A5%E5%88%B0'
# 纯文本通道（推荐做管道解析）
curl -s -m 20 -A "$UA" -b "$J" 'https://cn.bing.com/search?q=%E8%A1%97%E4%B9%A1%E5%90%B9%E5%93%A8&format=rss'
```

Cookie：**必需**（`MUID`/`SRCHHPGUSR`/`_EDGE_S` 等，jar 预热即得）；无 cookie 时降级为「只匹配首词」。

### 解析要点

- **HTML 直出**，无需 JS。
- 结果项：`li.b_algo`；标题 `h2 > a[href]`（**真实 URL 直链，无跳转**）；摘要 `div.b_caption p`；总条数 `span.sb_count`（如「约 106,000 个结果」）。
- **RSS 通道**：`<rss><channel>`，逐 `<item>` 取 `<title>` / `<link>` / `<description>`；注意 `<link>` 字段里除条目外还有 channel 级的 2 条（首页/logo），解析时只取 `<item>` 内节点，或按首尾过滤。
- 中文查询建议带 `Accept-Language: zh-CN,zh;q=0.9`。

### 实测记录

**2026-10-02**，macOS + curl（Chrome 桌面 UA）：

- 冷启 `cn.bing.com/search?q=街乡吹哨&count=30` → 200，102942 B，`b_algo`×10，结果仅匹配「街」。
- 预热 cookie 后 `?q=街乡吹哨+部门报到` → 200，103937 B，命中 `12371.cn`/`beijing.gov.cn`/`zj.bjcc.gov.cn`。
- `&first=11`、`&first=31`、`&FORM=PERE` → 与首页 URL 集合完全相同。
- `&format=rss` → 200，6864 B，`text/xml`，`<item>`×10；`&format=rss&first=11` 逐字节相同。
- `www.bing.com/search?q=…`（`cc=US`）→ 302 → `cn.bing.com`。

**2026-10-01**（历史实测）：

- `read` 工具抓 `cn.bing.com/search?q=…` 被降级为 `application/feed`（即 RSS 流），无可用结果；微软必应对非浏览器请求曾返回空壳（316 B）。——与本次 curl 结果一致：**必须带浏览器头 + cookie**。

## 坑

- **不预热 cookie 会静默降级**（仍是 200，不报错），只用到第一个词 —— 最容易踩的坑。
- `first=` 在本环境无效，不要指望翻页；需要更多结果时改用 RSS + 多组关键词，或走其他引擎。
- `www.bing.com` 一定 302 到 `cn.bing.com`，`cc=US` 也无效；国际索引取不到。
- RSS 的 `<link>` 含 channel 级干扰项，机械按行 grep `<link>` 会多算 2 条。
