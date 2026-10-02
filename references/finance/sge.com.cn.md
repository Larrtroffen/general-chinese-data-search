# sge.com.cn —— 黄金白银现货与延期行情

- 去哪找：门户 `https://www.sge.com.cn/`；每日/历史行情 `https://www.sge.com.cn/sjzx/quotation_daily_new`；行情月报 `/sjzx/hqyb`、行情周报 `/sjzx/hqzb`；黄金资管统计数据 `/sjzx/hjzgtjsj`。
- 什么时候用：要**上海黄金交易所口径**的黄金/白银行情——Au99.99/Au99.95/Au100g、Au(T+D)/Ag(T+D) 延期合约的**开高低收、加权平均价、涨跌幅、成交量、成交金额、市场持仓、交收量**；上海金基准价、黄金 ETF、黄金资管统计、会员名录。
- 怎么搜：**GET + 日期区间参数**，返回**服务端渲染 HTML 表格**（非 JSON）：
  ```
  https://www.sge.com.cn/sjzx/quotation_daily_new?start_date=2026-09-30&end_date=2026-09-30
  ```
  同族带参页面：`/sjzx/goldEtf?start_date=&end_date=`（黄金 ETF）、`/sjzx/shanghaiAuAuto?start_date=&end_date=`（上海金）、`/sjzx/goldoptionsqxcx`（黄金期权）。结果形态：HTML 表格（可 `pandas.read_html`）；周报/月报为页面/附件。
- 覆盖：上金所现货与延期合约日行情（日频）；黄金资管、ETF、基准价；全国（上海）口径。
- 门槛：无（免登录、免 key）。
- 实测：2026-10-03，桌面 UA curl——`GET https://www.sge.com.cn/` `200/71,913 B`；`GET /sjzx/quotation_daily_new?start_date=2026-09-30&end_date=2026-09-30`（带 Referer）→ `200/90,031 B`，正文含 15 列表格：`2026-09-30 | Au99.99 | 899.00 | 909.00 | 897.50 | 907.32 | 9.79 | 1.09% | 903.69 | 6722.32 | 6074953450`、`Au99.95`、`Au100g` 等（页内 18 行）。
- 上游：`https://www.sge.com.cn/`（上海黄金交易所）。

## 细节

### 日行情表列（`quotation_daily_new`）

`序号 · 日期 · 合约 · 开盘价 · 最高价 · 最低价 · 收盘价 · 涨跌（元） · 涨跌幅 · 加权平均价 · 成交量（kg） · 成交金额（元） · 市场持仓（手） · 交收方向 · 交收量（手）`

### 相关栏目

| 栏目 | URL |
|---|---|
| 行情走势 | `/sjzx/mrhq` |
| 历史行情数据 | `/sjzx/quotation_daily_new` |
| 行情周报 / 月报 | `/sjzx/hqzb`、`/sjzx/hqyb` |
| 黄金资管统计数据 | `/sjzx/hjzgtjsj` |
| 保证金询价市场数据 | `/sjzx/bzjxjsc` |
| 黄金 ETF | `/sjzx/goldEtf?start_date=&end_date=` |
| 会员名录与查询 | `/hyzq/mlycx` |

## 坑

1. **单位不统一**：成交量（kg）、成交金额（元）、市场持仓（手）、交收量（手）——直接算均价/换手要换算，别混用。
2. 日期参数**必须成对**（`start_date` + `end_date`）；区间过长可能被截断，按日/周小批循环。
3. 是 **HTML 表格**不是 JSON：用 `pandas.read_html` 时页面含多张表，按列名（`合约`/`收盘价`）定位，别取第 0 张。
4. 合约命名含 `(T+D)` 延期与现货（Au99.99）两类，研究口径要区分；`-` 表示无交收方向。
5. 与央行/外汇无关的**黄金储备**数字在 SAFE（`safe.gov.cn.md`）的官方储备资产里，别与上金所成交量混。
