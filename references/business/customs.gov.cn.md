# customs.gov.cn —— 海关进出口统计（月报/快讯）

- 去哪找：总署门户 `https://www.customs.gov.cn/`；**统计月报** `http://tjs.customs.gov.cn/tjs/sjgb/tjyb/index.html`；**统计快讯/海关统计栏目** `http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/index.html`；**海关统计数据在线查询平台** `http://stats.customs.gov.cn/`。
- 什么时候用：要**进出口货物贸易统计**：月度总值、**国别（地区）总值**、**商品构成/类章**、主要商品量值、贸易方式；做外贸、产业、区域经济与"一带一路"研究。
- 怎么搜：**官网有 WAF，本机匿名直连返回 `412`**；需真实浏览器过挑战后取页面/附件。在线查询平台 `stats.customs.gov.cn` 支持按商品/国别/时间维度自助组合查询（页面服务，非公开 API）。
- 覆盖：月度/年度进出口统计；分国别、分商品类章、分贸易方式（美元值 + 人民币值）；快讯为初步汇总、月报为正式数据。
- 门槛：**需浏览器**（WAF：加速乐 `__jsluid` + `AV7KY…` Cookie，实测 412）；数据本身免费。
- 实测：2026-10-03，macOS arm64 curl 8.x（桌面 UA）——`GET http://www.customs.gov.cn/` 一次 `200/82 KB`、再次（带 Cookie jar）`412/1.9 KB`；`GET http://tjs.customs.gov.cn/tjs/sjgb/tjyb/index.html` → `412`；`GET http://stats.customs.gov.cn/` → `412`（`Set-Cookie: __jsluid_h=…; AV7KYchI7HHaS=…`）；`GET http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/index.html` → `412`。
- 上游：海关总署 `https://www.customs.gov.cn/`（统计分析司 `tjs.customs.gov.cn`）。

## 细节

### 入口一览（URL 经 web_search 上游核对；本机多被 412 拦）

| 内容 | URL |
|---|---|
| 统计月报（统计分析司） | `http://tjs.customs.gov.cn/tjs/sjgb/tjyb/index.html` |
| 某年统计月报 | `http://www.customs.gov.cn/customs/302249/zfxxgk/fdzdgknr/302274/302277/{id}/index.html` |
| 统计快讯（月度初步） | `http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/index.html` |
| 统计数据在线查询平台 | `http://stats.customs.gov.cn/` |

- 月报条目命名规律：`（N）{YYYY}年{M}月…`，如「进出口商品总值表」「进出口商品国别（地区）总值表」「进出口商品构成表」「进出口商品类章总值表」「出口/进口主要商品量值表」，各有**美元值**与**人民币值**两版。
- 快讯页提示：「快讯」为月度初步汇总，以更正后的月度正式数据为准。

### WAF 现象

```
HTTP/1.1 412 Precondition Failed
Set-Cookie: AV7KYchI7HHaS=…
Set-Cookie: SF_cookie_251=…
Set-Cookie: __jsluid_h=…
```
- 加速乐（jsl）JS 挑战：curl 不带有效 `__jsl_clearance` 时直接 412；首页偶发 200（缓存/CDN 命中），栏目页稳定 412。

## 坑

1. **不要用 curl 硬刷**：全程 412，且会触发 IP 封禁；批量取数请在浏览器/Playwright 里过挑战。
2. 门户口 `www.customs.gov.cn` 与统计分析司 `tjs.customs.gov.cn` 是两个主机，栏目结构不同。
3. 在线查询平台 `stats.customs.gov.cn` 是**表单式查询**（按商品/国别/时间组合），无公开 JSON API，导出为 Excel/CSV。
4. 月度初值与正式值有别：研究用**正式月报**，引文时注明口径（人民币值 vs 美元值）。
