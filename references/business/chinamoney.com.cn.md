# chinamoney.com.cn —— 货币市场利率与汇率数据

- 去哪找：门户 `https://www.chinamoney.com.cn/chinese/index.html`；**汇率数据（SDDS）** `https://www.chinamoney.com.cn/chinese/sddshl`；**数据接口服务** `https://www.chinamoney.com.cn/chinese/dataInterfaceService`；JSON 数据域 `https://www.chinamoney.com.cn/ags/ms/…`。
- 什么时候用：要**人民币汇率中间价、外汇即期/远期、Shibor、LPR、回购定盘利率、债券收益率**等货币市场与汇率行情；要外汇交易中心口径的官方数据。
- 怎么搜：站点有**免登录 JSON 接口**（`/ags/ms/cm-u-*`，带桌面 UA + `Referer`）——
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -s -A "$UA" -H 'Referer: https://www.chinamoney.com.cn/chinese/sddshl' \
    'https://www.chinamoney.com.cn/ags/ms/cm-u-bk-fx/RefRateHis?lang=CN&pageNum=1&pageSize=5'
  ```
  返回统一信封 `{head, data, records}`；`records[]` 为按时点展开的行情。
- 覆盖：银行间外汇市场汇率（USD/EUR/JPY/GBP/HKD 对 CNY）历史；其余利率/债券行情以各数据页为准（未逐项实测）。
- 门槛：页面浏览免费；**程序化/批量接口需会员**（`dataInterfaceService` 列明"外汇/本币接口服务"须银行间市场会员申请）；页面级 JSON 接口匿名可读（实测）。
- 实测：2026-10-03，macOS arm64 curl 8.x——`GET https://www.chinamoney.com.cn/` → `302 → /chinese/index.html` `200/13 KB`（`<title>中国货币网-中国外汇交易中心主办`）；`GET /ags/ms/cm-u-bk-fx/RefRateHis?lang=CN&pageNum=1&pageSize=5` → `200/46 KB application/json`，`head.rep_code=200`、`data.currencyList=[USD.CNY,EUR.CNY,JPY.CNY,GBP.CNY,HKD.CNY]`、`records[]` 含 `ccyPair/dealDate/rateOf09hour…rateOf23hour`。
- 上游：`https://www.chinamoney.com.cn/`（中国外汇交易中心暨全国银行间同业拆借中心主办）。

## 细节

### `RefRateHis`（人民币汇率中间价历史）实测响应

```
{
  "head": {"version":"2.0","provider":"CWAP","rep_code":"200","tstext":"…"},
  "data": {"flag":"0","startDateTool":"04 Sep 2026","endDateTool":"03 Oct 2026",
           "currencyList":[{"currValue":"ALL","currValueDesc":"全部"},
                           {"currValue":"USD.CNY","currValueDesc":"USD/CNY"}, …]},
  "records":[{"ccyPair":"USD/CNY","dealDate":"2026-09-30",
             "rateOf09hour":"---","rateOf10hour":"…", …}]
}
```

| 参数 | 说明 |
|---|---|
| `lang` | `CN` |
| `pageNum` / `pageSize` | 分页（实测 5） |
| `currency`（推测） | 券种/币种过滤，页面下拉同 `currencyList` 值 |

- 同一域下另有 `cm-u-bk-*`（银行间）、`cm-u-fx-*`（外汇）等命名族，端点需在对应数据页抓包确认。

### 其他数据页（上游声明，未本机实测）

- 汇率数据（SDDS）：`/chinese/sddshl`；利率数据：同栏目。
- LPR、Shibor、回购定盘利率在首页/行情页动态展示（页面数据来自上述 JSON 域）。

## 坑

1. 首页 `https://www.chinamoney.com.cn/` 会 `302` 到 `/chinese/index.html`；直接写后者。
2. `records` 是**按时点展开**（`rateOf09hour`…`rateOf23hour`，"---" 表示未到/无报价），按汇率序列分析前需 reshape 成时间序列。
3. 页面级 JSON 免登录可读，但**批量/实时订阅**属会员服务（`dataInterfaceService`），别把匿名接口当正式数据授权。
4. 响应为 `application/json;charset=UTF-8`，含中文，注意 UTF-8 读取。
