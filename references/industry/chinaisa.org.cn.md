# chinaisa.org.cn —— 钢铁协会统计发布入口

- 去哪找：门户 `https://www.chinaisa.org.cn/gxportal/xfgl/portal/index.html`（旧首页 `/` 仅 meta refresh 到此）；协会媒体中国钢铁新闻网 `http://www.csteelnews.com/`（见 `csteelnews.com.md`）
- 什么时候用：找钢协「统计发布 / 行业分析 / 环保统计 / 市场价格分析 / 钢材价格指数」栏目入口，或核实协会口径表述时。
- 怎么搜：门户由通用产品「gxportal」渲染，栏目列表形如
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -sS -A "$UA" 'https://www.chinaisa.org.cn/gxportal/xfgl/portal/index.html'
  curl -sS -A "$UA" 'https://www.chinaisa.org.cn/gxportal/xfgl/portal/list.html?columnId=2e3c87064bdfc0e43d542d87fce8bcbc8fe0463d5a3da04d7e11b4c7d692194b'   # 统计发布
  ```
  `columnId` 为 64 位 hex，只在页面里出现；条目链接多为 `javascript:void(0)`，正文由 `list.js` 渲染。
- 覆盖：栏目（实测自首页）：统计发布、行业分析、环保统计、市场价格分析、钢材价格指数、综合价格指数、会员动态；**门户内容明显偏旧**。
- 门槛：免费、无需登录。
- 实测：2026-10-03 `https://www.chinaisa.org.cn/` → 200 但仅 **286 B**（只有 `<meta http-equiv=refresh>`）；门户 `index.html` → 200，40.5 KB，title「中国钢铁工业协会」；`list.html?columnId=2e3c…`（统计发布）→ 200，26 KB，页面条目为 2019 年旧闻且链接为 `javascript:void(0)`，**未取到真实统计列表 ⚠️**。
- 上游：中国钢铁工业协会。

## 细节

### 门户栏目 columnId（实测自首页，均为 64 位 hex）
| 栏目 | columnId |
|---|---|
| 统计发布 | `2e3c87064bdfc0e43d542d87fce8bcbc8fe0463d5a3da04d7e11b4c7d692194b` |
| 行业分析 | `1b4316d9238e09c735365896c8e4f677a3234e8363e5622ae6e79a5900a76f56` |
| 环保统计 | `619ce7b53a4291d47c19d0ee0765098ca435e252576fbe921280a63fba4bc712` |
| 市场价格分析 | `a44207e193a5caa5e64102604b6933896a0025eb85c57c583b39626f33d4dafd` |
| 钢材价格指数 | `17b6a9a214c94ccc28e56d4d1a2dbb5acef3e73da431ddc0a849a4dcfc487d04` |
| 综合价格指数 | `63913b906a7a663f7f71961952b1ddfa845714b5982655b773a62b85dd3b064e` |
| 会员动态 | `268f86fdf61ac8614f09db38a2d0295253043b03e092c7ff48ab94290296125c` |

首页共出现 26 个 `columnId`，上表是能与栏目名对应的 7 个。

## 坑

1. **不要用旧首页 URL**：只返回 286 B 的 meta refresh，脚本会以为拿到空页面。
2. 门户列表页看似静态，条目实际靠 JS 补全；curl 拿到的可能是模板占位内容（实测为 2019 年旧闻），**别把占位当数据**。
3. 要当期钢铁数据优先用 `csteelnews.com.md`（同协会媒体，静态可抓）或工信部原材料工业司运行数据（`../stats/ministry-stats.md`）。
