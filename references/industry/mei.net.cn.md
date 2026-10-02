# mei.net.cn —— 机械工业运行信息网

- 去哪找：`https://www.mei.net.cn/`（机经网）；联合会官网入口 `http://cmif.mei.net.cn/`（598 B 跳转页）；`http://www.cmif.org.cn/` 亦 301 到机经网
- 什么时候用：机械工业经济运行情况（季度/年度）、行业与产经资讯、企业动态；找中国机械工业联合会口径表述时。
- 怎么搜：频道分页模板 `/recommend/more/index/{channel}/pages/{N}.html`：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -A "$UA" 'https://www.mei.net.cn/'
  curl -sS -A "$UA" 'https://www.mei.net.cn/recommend/more/index/syhydt112/pages/1.html'   # 行业资讯
  ```
- 覆盖：行业资讯 / 产经资讯 / 企业资讯 / 行业分析等频道，实测最新 2026-09 条目；**未见独立统计/数据栏目与取数接口**。
- 门槛：免费、无需登录（二级导航由 JS 展开，看全栏目需浏览器）。
- 实测：2026-10-03 `https://www.mei.net.cn/` → 200，65 KB，title「中国机械工业联合会机经网」；`http://www.cmif.org.cn/` → 301 至 mei.net.cn ✅；`/recommend/more/index/sytjxx11/pages/1.html` → 200，48 KB，title「通知公告」（频道码含 `tjxx` 但内容是通知公告，**不是统计数据**）。
- 上游：中国机械工业联合会。

## 细节

### 频道码（实测自首页导航）
| 频道码 | 栏目 |
|---|---|
| `syhydt112` | 行业资讯 |
| `syzcfg11` | 产经资讯 |
| `syqydt11` | 企业资讯 |
| `sycpsc11` | 工作动态 |
| `sytjxx11` | 通知公告（码含 tjxx，实际非统计） |
| `syhyfx11` | 领导活动 / 行业分析 |

## 坑

1. 结论：**机经网无统计数据栏目**。机械工业统计数字以「经济运行」新闻稿形式发布（目录形如 `/jxgy/{YYYYMM}/{id}.html`）；要月度数据走国家统计局或工信部装备工业一司口径（`../stats/ministry-stats.md`）。
2. 首页导航是 JS 菜单，curl 只拿到 6–9 个频道，完整栏目请用浏览器。
3. 频道码命名不直观（`tjxx` ≠ 统计信息），别按拼音猜内容。
