# gesis.org —— 德国社科数据与变量检索

- 去哪找：统一检索台 `https://search.gesis.org/`（按类型切：`/research_data?q=`、`/variables?q=`、`/publications?q=`）；数据服务 `https://www.gesis.org/en/services/data`；**检索后端** `https://search.gesis.org/searchengine?source=<ES 查询 JSON>`
- 什么时候用：找**德国 / 欧洲的社科调查**（ALLBUS、SOEP、ISSP、Eurobarometer）与中国主题的比较研究；做**变量级**检索（哪个研究测过某变量）；找 DDI 代码本与量表。
- 怎么搜：
  - 网页：`https://search.gesis.org/research_data?q=china`（实测 → research data **227** 条 / variables **2,335** / instruments **14** / publications **8,501** / library **416**）。
  - 后端（Elasticsearch 直连，**在页面上下文里 fetch 实测 200**）：
    ```
    GET https://search.gesis.org/searchengine?source=<URL编码的 ES 查询 JSON>&source_content_type=application/json
    # 最小 source：{"query":{"query_string":{"query":"china","default_operator":"AND"}},"size":20}
    # 限类型：再加 "filter":[{"term":{"type":"research_data"}}]
    #   类型取值：research_data / variable / publication / gesis_product
    ```
    返回标准 ES 结构：`hits.total` / `hits.hits[]._id` / `hits.hits[]._source`。
- 覆盖：GESIS 自 1960s 起收藏的德国 / 国际社科数据与文献；类型含 research data、variables、instruments、publications、GESIS library。
- 门槛：检索免登录；**部分数据下载需注册或机构许可**（数据保护条款另签）。
- 实测：2026-10-03，macOS arm64：curl 直连 `https://search.gesis.org/api/search?q=china` → **403**（Cloudflare `Just a moment...`）；无头 Chromium 打开 `/research_data?q=china` → **200**，计数如上；再由页面上下文 `fetch('/searchengine?source=…&source_content_type=application/json')` → **200**，`{"status":200,"total":{"value":10000,"relation":"gte"},"hit0":{"id":"bibsonomy-meng2019chinas","title":"China's Pension Reforms …"}}`。
- 上游：`https://search.gesis.org/`（GESIS – Leibniz Institute for the Social Sciences）

## 坑

- 后端是**裸 Elasticsearch 代理**：`source` 要写 ES DSL（`query` / `aggs` / `size`），不是简单的 `q=`；抄网页 URL 里的 `source=` 参数即可复现其检索逻辑。
- curl 被 Cloudflare 拦；**必须在浏览器上下文调用**（或带 `cf_clearance` cookie）。
- 别用 `search.gesis.org/api/search`——本机 403，实测有效的只有 `/searchengine`。
- `total` 到 10,000 就截断（`relation:"gte"`），做量级判断要配合分面聚合而不是硬翻页。
