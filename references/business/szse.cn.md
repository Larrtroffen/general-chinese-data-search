# szse.cn —— 深交所公告与市场统计

- 去哪找：门户 `https://www.szse.cn/index/index.html`；**上市公司公告** `https://www.szse.cn/disclosure/listed/notice/index.html`；**市场统计/概览** `https://www.szse.cn/market/overview/index.html`；数据接口 `https://www.szse.cn/api/disc/announcement/annList`、`https://www.szse.cn/api/report/ShowReport/data`。
- 什么时候用：要深市**上市公司公告**（逐条、可翻页、带 PDF 附件路径）；要深市**证券类别/交易/市值统计**（结构化表格，可导 xlsx）；作为南方中心与 cninfo 交叉核对。
- 怎么搜：两个**免登录 JSON 接口**（`https://www.szse.cn`，POST 需 `Content-Type: application/json` + `Referer`）——
  ```bash
  UA='Mozilla/5.0 (...) Chrome/124.0.0.0 Safari/537.36'
  # ① 公告列表（POST JSON）
  curl -s -A "$UA" 'https://www.szse.cn/api/disc/announcement/annList?random=0.5' \
    -H 'Content-Type: application/json' \
    -H 'Referer: https://www.szse.cn/disclosure/listed/notice/index.html' \
    --data-binary '{"seDate":["2024-01-01","2024-01-31"],"channelCode":["listedNotice_disc"],"pageSize":10,"pageNum":1}'
  # ② 统计报表（GET，CATALOGID 选表）
  curl -s -A "$UA" 'https://www.szse.cn/api/report/ShowReport/data?SHOWTYPE=JSON&CATALOGID=1803_sczm&TABKEY=tab1&PAGENO=1&random=0.3' \
    -H 'Referer: https://www.szse.cn/market/overview/index.html'
  ```
- 覆盖：深市（含创业板）公告；`announceCount` 给总量，`ShowReport` 按 `CATALOGID` 出各类统计表（实测 `1803_sczm`=证券类别统计）。
- 门槛：免费、免登录（实测）。
- 实测：2026-10-03，macOS arm64 curl 8.x——门户 `302 → /index/index.html 200/90 KB`；`annList` POST JSON `200/5153 B`，`data[]` 首条 `annId=1219056613`「*ST越博：2024-014股票可能被终止上市的风险提示公告」、`attachPath=/disc/disk03/finalpage/2024-01-31/0f8fe500-….PDF`；`ShowReport/data?CATALOGID=1803_sczm` `200/3196 B` JSON（`metadata.catalogid=1803_sczm`，`name=证券类别统计`，`excel=xlsx`）。
- 上游：`https://www.szse.cn/`（深圳证券交易所）。

## 细节

### ① 公告接口 `/api/disc/announcement/annList`

| 参数 | 说明 |
|---|---|
| `seDate` | `["YYYY-MM-DD","YYYY-MM-DD"]`（数组） |
| `channelCode` | 频道，如 `["listedNotice_disc"]`（上市公司公告） |
| `pageSize` / `pageNum` | 分页 |
| `random` | 查询串随机数（防缓存），可任意 |

- **必须 `Content-Type: application/json`**；用表单编码会 `500`。
- 响应：`{announceCount, data:[{id, annId, title, publishTime, attachPath, attachFormat, attachSize, secCode[], secName[], bigCategoryId, smallCategoryId, channelCode}]}`。
- 附件直链 = `https://disc.szse.cn/download` + `attachPath`（本机未验证该前缀，`attachPath` 形如 `/disc/disk03/finalpage/…`）。

### ② 统计报表接口 `/api/report/ShowReport/data`

- 参数：`SHOWTYPE=JSON`、`CATALOGID=<表号>`、`TABKEY=tab1`、`PAGENO`、`random`。
- 响应为数组：`[{metadata:{catalogid,name,excel,pagetype,tabkey,pagesize,conditions:[{label,name,inputType,...}]}, data:[...]}]`；`excel=xlsx` 表示该表可导 Excel。
- 实测 `CATALOGID=1803_sczm` = 证券类别统计；其他表号需在 `market/` 各栏目页内点击时抓包获取。

## 坑

1. `annList` 必须 POST + `application/json`，否则 `500 Internal Server Error`。
2. 门户 `https://www.szse.cn/` 会 `302` 到 `/index/index.html`，脚本里直接写后者更稳。
3. 公告附件下载前缀与鉴权未本机验证（`attachPath` 仅路径片段）。
4. `ShowReport` 的 `CATALOGID` 与栏目一一对应，换表要重抓；`conditions` 里 `required:true` 的查询日期参数缺失时可能返回空表。
