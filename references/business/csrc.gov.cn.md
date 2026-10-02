# csrc.gov.cn —— 证监统计信息与行政处罚

- 去哪找：门户 `https://www.csrc.gov.cn/`；**统计信息总栏** `http://www.csrc.gov.cn/csrc/tjsj/index.shtml`；**证券市场快报** `http://www.csrc.gov.cn/csrc/c100119/common_list.shtml`、**月报** `.../c100120/common_list.shtml`、**期货市场周报/月报** `.../c100121`、`.../c100122`；**行政处罚** 栏目 `http://www.csrc.gov.cn/csrc/c101928/…`。
- 什么时候用：要**证券/期货市场统计**（成交、市值、投资者、期货品种周/月报）；要**上市公司行业分类结果**、合法机构名录、辖区统计数据；要**行政处罚决定书**原文。
- 怎么搜：栏目页多可直读（统计栏目列表为服务端渲染，直接出条目与内链）；行政处罚栏目列表与站内检索为 JS 渲染，另有 JSON 端点（见「细节」），但本机匿名返回空。
- 覆盖：证监会机关统计口径（周报/月报/快报/行业分类/机构名录）；行政处罚决定书（按发布机构+文号）。年份范围以栏目页为准。
- 门槛：免费、免登录；站内检索端点匿名可连但**实测返回 total 0**（可能需会话/正确 `channelId`）。
- 实测：2026-10-03，macOS arm64 curl 8.x——门户 `200/221 KB`；`csrc/tjsj/index.shtml` `200/19 KB`，页面内链实测列出 `c100119`（证券市场快报，条目如「2026年9月14日-9月18日证券市场快报」）、`c100120`（月报，条目如「2026年8月统计数据」）；行政处罚栏目 `csrc/c101928/zfxxgk_zdgk.shtml` `200/152 KB` 但**内联处罚链接 0 条**（JS 渲染）；`/searchList/a1a078ee…?_isAgg=true&_isJson=true&_pageSize=10&_template=index&page=1&keyword=行政处罚` → `200 {"data":{"total":0,…}}`；`POST /getSearch`（`type=title&searchContent=行政处罚&…`）→ `200 {"code":200,"data":{"total":0,…}}`。
- 上游：`https://www.csrc.gov.cn/`（中国证券监督管理委员会）。

## 细节

### 统计信息栏目（已实测 200，服务端出条目）

| 栏目 | URL 前缀 | 条目示例 |
|---|---|---|
| 统计信息总栏 | `/csrc/tjsj/index.shtml` | 汇总导航 |
| 证券市场快报 | `/csrc/c100119/common_list.shtml` | 2026年9月14日-9月18日证券市场快报 |
| 证券市场月报 | `/csrc/c100120/common_list.shtml` | 2026年8月统计数据 |
| 期货市场周报 | `/csrc/c100121/common_list.shtml` | — |
| 期货市场月报 | `/csrc/c100122/common_list.shtml` | — |
| 上市公司行业分类结果 / 合法机构名录 / 辖区统计数据 | 见 `tjsj` 页导航 | — |

- 文章正文 URL 形态：`/csrc/c{栏目号}/c{文章id}/content.shtml`。

### 站内检索端点（形态由 `render.js` 确证）

```js
// 栏目列表（GET）
'/searchList/' + _id + '?_isAgg=true&_isJson=true&_pageSize=' + pageSize + '&_template=index&_rangeTimeGte=&_channelName=&page=' + curPage
// 全站关键词检索（POST）
'/getSearch'  // data: {type:'title', searchContent:<kw>, channelId:<id>, isAgg:true, isIdentifier:true, page:1, size:10}
```
- 返回 `{"data":{"total":N,"results":[…]}}`；`locationUrl` 字段回带 `/common/searchList/{id}?…`。
- 相关 JS：`/csrc/xhtml/js/render.js`、`/csrc/xhtml/js/zfxxgk.js`（后者含 `/api/query?siteCode=bm2900xxgk&…`）。

## 坑

1. 站内检索与行政处罚栏目列表**由 JS 渲染**，`curl` 直读 HTML 拿不到条目；两个 JSON 端点本机匿名 **total=0**（未跑通），需在真实浏览器里抓 `channelId`/会话后再试。
2. 行政处罚决定书正文页形如 `/csrc/c101928/c{id}/content.shtml`（搜索结果可见），可**按 id 直取正文**，但**列表页不能直接枚举**。
3. 统计栏目页是**服务端渲染**，可 `curl` + 解析内链，是本站最稳的取数路径。
