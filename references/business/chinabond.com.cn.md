# chinabond.com.cn —— 债券市场与中债收益率

- 去哪找：门户 `https://www.chinabond.com.cn/`；**中债价格指标/收益率曲线** `https://yield.chinabond.com.cn/`（跳 `/cbweb-mn/`）；中债估值数据同域 `yield.chinabond.com.cn/cbweb-mn/…`。
- 什么时候用：要**债券市场**官方口径：债券发行/托管/结算统计、**国债收益率曲线（到期/即期）**、中债估值、中债指数、债券市场分析月报；做利率/期限结构/Bond-CDS 类研究。
- 怎么搜：门户与 `yield.chinabond.com.cn` 页面可直读；**收益率曲线取数接口为 POST**（GET 报 405），但本机匿名返回**空数组**，参数/会话未跑通（见「坑」）。
- 覆盖：债券市场一级/二级、中债收益率曲线与估值（按交易日、按券种）；具体年份以平台为准。
- 门槛：浏览免费；收益率曲线接口**需带页面会话 Cookie**（实测补 Cookie 后仍为空数组，疑参数变更）。
- 实测：2026-10-03，macOS arm64 curl 8.x——门户 `GET https://www.chinabond.com.cn/` `200/415 KB`（`<title>中国债券信息网`）；`GET https://yield.chinabond.com.cn/` `302 → /cbweb-mn/`，`/cbweb-mn/` `200/73,940 B`；`GET …/cbweb-mn/yc/searchYc?xyzSelect=txy10&workTime=…` → `405`；改 `POST`（带 `Referer`、表单体）→ `200` 但正文 `[]`；先访问 `yield_main` 存 Cookie 再 POST → 仍 `[]`。
- 上游：`https://www.chinabond.com.cn/`（中央国债登记结算有限责任公司 / 中债金融估值中心）。

## 细节

### 已确认可直读的页面

| 页面 | URL | 状态 |
|---|---|---|
| 中国债券信息网首页 | `https://www.chinabond.com.cn/` | ✅ 200 / 415 KB |
| 中债价格指标（收益率曲线） | `https://yield.chinabond.com.cn/cbweb-mn/yield_main` | ✅ 200 / 74 KB |
| 该平台首页 | `https://yield.chinabond.com.cn/cbweb-mn/` | ✅ 200 / 74 KB |

- 页面内引用 `/js/yc/bondyields`、`/js/yc/commonBondYields`、`/js/yc/xyBondYields`、`/js/yc/xyzBondYields`、`/js/yc/yzBondYields`、`/yc/ycDetail` 等资源（原为各类券种曲线）。
- 取数端点形态：`https://yield.chinabond.com.cn/cbweb-mn/yc/searchYc`，参数含 `xyzSelect`（券种，如 `txy10`）、`workTime`（交易日 `YYYY-MM-DD`）、`dxbj`、`qxll`、`yqqxN/yqqxK`、`paras`、`selectMode`。

## 坑

1. `searchYc` **GET → 405**，必须 `POST`；但本机 POST 返回 `[]`（空数组，HTTP 200）——**取数未跑通**，不要据此判定"该日无曲线"。
2. `yield.chinabond.com.cn/` 与 `/cbweb-mn/` 同页（302）；脚本直接写 `/cbweb-mn/` 省一跳。
3. 需要收益率曲线/中债估值的**正式取数**时，建议：先在真实浏览器打开 `yield_main` 抓包确证当前接口与参数，或用中债官网发布的**分析月报/Excel** 附件；也可经 Wind/CSMAR 等商业库取（见 `commercial-databases.md`）。
4. 债券**发行/托管统计**也可从中国货币网（`chinamoney.com.cn.md`）与中央结算公司公告交叉获取。
