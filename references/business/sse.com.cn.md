# sse.com.cn —— 上交所信息披露与市场统计

- 去哪找：门户 `https://www.sse.com.cn/`；**上市公司公告** `https://www.sse.com.cn/disclosure/listedinfo/announcement/`；**定期报告** `https://www.sse.com.cn/disclosure/listedinfo/regular/`；**股票数据总貌/月报** `https://www.sse.com.cn/market/stockdata/statistic/`；数据接口域 `https://query.sse.com.cn/`。
- 什么时候用：要上交所的**上市公司公告/定期报告**栏目、**市场成交与市值的统计月报**、**股票/债券发行与上市**公开信息；作为 cninfo 的官方旁证（公告栏目结构以交易所为准）。
- 怎么搜：公告栏目页为静态 HTML 可直读；**批量取公告走 `query.sse.com.cn`**（JSONP），但本机未测出可用参数组合，见「坑」。统计栏目页可直读后取内链。
- 覆盖：沪市上市公司公告、定期报告；股票/市场统计（总貌、月报）。具体年份/指标以栏目页为准（未逐项枚举）。
- 门槛：浏览免费、免登录；`query.sse.com.cn` 需带桌面 UA + `Referer: https://www.sse.com.cn/`。
- 实测：2026-10-03，macOS arm64 curl 8.x——门户 `200/66 KB`（`<title>首页 | 上海证券交易所>`）；公告栏目 `200/28 KB`；定期报告 `200/27 KB`；数据总貌 `200/27 KB`（`<title>股票数据总貌 | 上海证券交易所>`）；`query.sse.com.cn/security/stock/queryCompanyBulletinNew.do` 无参数 → `200 {"success":"false","error":"系统繁忙...","errorType":"ExceptionInterceptor"}`；带 `productId=600000&securityType=0101,...&reportType=ALL&pageHelp.*` → `200` 合法 JSONP 但 `pageHelp.total=0`、`result=[]`。
- 上游：`https://www.sse.com.cn/`（上海证券交易所）。

## 细节

### 已实测可直读的栏目

| 栏目 | URL | 状态 |
|---|---|---|
| 首页 | `https://www.sse.com.cn/` | ✅ 200 |
| 上市公司公告 | `https://www.sse.com.cn/disclosure/listedinfo/announcement/` | ✅ 200 |
| 定期报告 | `https://www.sse.com.cn/disclosure/listedinfo/regular/` | ✅ 200 |
| 股票数据总貌 | `https://www.sse.com.cn/market/stockdata/statistic/` | ✅ 200 |

- 公告/统计栏目页的列表项由页面内 JS 调用 `//query.sse.com.cn/` 填充（页面源码里 `var sseQueryURL = "//query.sse.com.cn/";`）；直接抓 HTML 拿不到条目。

### `query.sse.com.cn` JSONP 端点（形态已确认，参数未跑通）

```
https://query.sse.com.cn/security/stock/queryCompanyBulletinNew.do
  ?jsonCallBack=jsonpCallback&isPagination=true&productId=600000
  &keyWord=&reportType2=&reportType=ALL
  &beginDate=2024-01-01&endDate=2024-03-31
  &pageHelp.pageSize=25&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.endPage=1&_=1
```
- 返回 `jsonpCallback({..., "pageHelp":{"data":[],"total":0}, "result":[]})`——**能连上但按上述参数拿不到数据**；参数名/取值需再核（可能已迁移到新接口）。
- 该域无 `Referer` 时可能返回「系统繁忙」。

## 坑

1. **不要当作公告批量源**：要批量取沪深北公告请走 `../business/cninfo.com.cn.md`（免登录 JSON，实测可翻页）；上交所栏目页仅作**官方口径与栏目结构**参照。
2. `query.sse.com.cn` 的公告 JSONP **参数未跑通**（实测 total=0），须在真实浏览器里抓包确认现有参数或用新接口。
3. 上交所公告栏目/统计栏目均为 JS 渲染，`curl` 只得壳页，条目需另找接口。
