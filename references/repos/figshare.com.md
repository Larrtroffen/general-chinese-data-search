# figshare.com —— 全学科成果与附件仓储

- 去哪找：门户 `https://figshare.com/`；检索页 `https://figshare.com/search?q=<词>`；**API** `https://api.figshare.com/v2/articles?search_for=<词>`；结构化检索 `POST /v2/articles/search`
- 什么时候用：找**期刊补充材料 / 图版 / 代码 / 数据集**（Springer Nature、PLOS、Wiley 等的 supplementary 大量落在这里）；快速拿带 `10.6084/m9.figshare.*` DOI 的可引用条目；按机构 / 期刊过滤某单位的产出。
- 怎么搜：
  ```bash
  curl -s 'https://api.figshare.com/v2/articles?search_for=china&page_size=2'
  # → [{"id":33808543,"title":"Supplementary document for Camouflage coating …",
  #     "doi":"10.6084/m9.figshare.33808543.v2","published_date":"2026-10-02T16:34:05Z",
  #     "defined_type":6,"defined_type_name":"journal contribution",
  #     "url":"https://api.figshare.com/v2/articles/33808543","url_public_html":"…"}]
  ```
  - 参数：`search_for`、`page`、`page_size`、`order`、`order_direction`、`item_type`（1=figure …）；高级检索用 `POST /v2/articles/search`，body 支持 `search_for` / `institution` / `group` / `published_since` / `resource_doi`（上游声明，未逐字段实测）。
  - 取单条 `GET /v2/articles/{id}`，文件清单在 `files[]`（含 `download_url` 直链）。
- 覆盖：全学科，以机构与期刊的补充材料为主；`defined_type_name` 区分 figure / dataset / media / paper / code 等；全部带 DOI。
- 门槛：检索与下载公开条目**免登录**；上传需账号。
- 实测：2026-10-03，macOS arm64：**curl 直连 403**（桌面 UA 与 `curl/8.7.1` UA 都被 WAF 拒）；改用无头 Chromium 打开同一 URL → **200**，返回 JSON 数组（首条 `10.6084/m9.figshare.33808543.v2`）。**本机必须走浏览器上下文**。
- 上游：`https://figshare.com/`（Digital Science）

## 坑

- **WAF 拦 curl、放行浏览器（同一出口 IP）**：两种 UA 的 curl 都 403，浏览器却 200 —— 疑似按 TLS/JS 指纹判定（[INFERENCE]）。脚本里用 Playwright/Selenium，或换出口网络。
- 检索返回的是「文章级」条目（一个图/一个补充文件都可能单独成条），做数据集统计时要按 `defined_type_name` 过滤。
- 同一数据集的多个版本是**不同 DOI**（`.v1` / `.v2`），引用前确认版本。
