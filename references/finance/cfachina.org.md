# cfachina.org —— 期货市场成交与公司数据

- 去哪找：门户 `http://www.cfachina.org/`；统计数据 `http://www.cfachina.org/servicesupport/researchandpublishin/statisticalsdata/`；期货公司月度经营数据 `http://www.cfachina.org/informationpublicity/qhgsydjysj/`。
- 什么时候用：要**中期协口径**的全国期货市场月度/年度**成交量与成交额**（总量 + 分交易所）、期货公司月度经营数据（营业收入、净利润、客户权益、手续费收入）、期货行业服务实体经济数据、品种成交持仓排名。
- 怎么搜：**有匿名 JSON 检索接口**（同源，GET）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  curl -s -A "$UA" -H 'Referer: http://www.cfachina.org/servicesupport/researchandpublishin/statisticalsdata/' \
    'http://www.cfachina.org/qx-search/api/wcmSearch/searchDocsByProgram?programName=月度交易数据&pageNo=1&pageSize=5'
  ```
  返回 `{"errcode":0,"data":{"dataList":[{docId,docTitle,docContent,…}]}}`，`docContent` **直接是含数字的正文**（成交量/成交额/同比），免再开文章页。结果形态：JSON。栏目页另有 PDF 简报（`P0{时间戳}.pdf`）。
- 覆盖：全国期货市场月度成交量/额（含各交易所份额、月末持仓）、期货公司经营数据、行业服务实体经济；月度滚动；全国口径。
- 门槛：无（JSON 免 key、免登录）。
- 实测：2026-10-03，桌面 UA curl——`GET http://www.cfachina.org/` `200/163,535 B`；`GET /servicesupport/researchandpublishin/statisticalsdata/` `200/81,612 B`；`GET /qx-search/api/wcmSearch/searchDocsByProgram?programName=月度交易数据&pageNo=1&pageSize=5`（带 Referer）→ `200/17,905 B`，`application/json`，`docTitle` = "2026年8月全国期货市场交易情况"，`docContent` 含"8月全国期货交易市场成交量为1,087,011,317手，成交额为850,392.18亿元…上海期货交易所8月成交量为211,180,653手…"。
- 上游：`http://www.cfachina.org/`（中国期货业协会）。

## 细节

### 检索接口

| 项 | 值 |
|---|---|
| 路径 | `/qx-search/api/wcmSearch/searchDocsByProgram` |
| 方法 | GET |
| 参数 | `programName`（栏目名，如"月度交易数据"）、`pageNo`、`pageSize`、`keyword`（可选） |
| 返回 | `{errcode,data:{dataList:[{docId,docChannel,docTitle,docContent,…}]}}` |

- 页面内出现的 `programName` 取值：`月度交易数据`、`月度`、`交易`（三处列表各一，按需试）。
- 栏目入口：统计数据 `/servicesupport/researchandpublishin/statisticalsdata/`、期货市场月度成交情况 `/informationpublicity/qhgsydcjqk/`、期货公司月度经营数据 `/informationpublicity/qhgsydjysj/`、期货行业服务实体经济数据 `/informationpublicity/qhhyfwstjjsj/`。
- PDF 简报规律：`/{栏目}/{YYYYMM}/P0{20位时间戳}.pdf`。

## 坑

1. **接口路径有前缀 `/qx-search/`**（页内是 `URL+'/qx-search/api/…'`），漏掉会 `404`；本机首发用无前缀路径即 404。
2. `programName` 中文须 URL 编码；只给 `keyword` 不给 `programName` 结果口径不定。
3. `docContent` 是**新闻稿正文**（含数字但夹叙述），要精确序列仍以交易所口径为准：见 `futures-exchanges.md`（日行情/持仓/仓单）。
4. 期货公司**单体**财务在「期货公司月度经营数据」栏目（PDF/文章），非 JSON；接口只覆盖检索到的正文。
