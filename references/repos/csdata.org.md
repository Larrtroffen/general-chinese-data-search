# csdata.org —— 数据论文与配套数据集期刊

- 去哪找：`https://www.csdata.org/`（**会 301 跳到** `https://www.sciengine.com/CSD/home`）；期刊页 `https://www.sciengine.com/CSD/home`；文章页 `https://www.sciengine.com/CSD/doi/<DOI>`
- 什么时候用：要找**「数据论文」**——用一篇正式论文把一份数据集发表出来、可引用的场合；核国内数据集的规范引用格式（中英双语）；顺藤摸到论文配套的数据集（多在 ScienceDB）。
- 怎么取：期刊在 SciEngine 平台上，是 SPA：
  - 文章直链模板 `https://www.sciengine.com/CSD/doi/10.11922/11-6035.csd.2025.0204.zh`（首页实测列出多条，DOI 前缀 `10.11922/11-6035.*`）。
  - 期刊页有「Journal Search」输入框；提交后走 `POST https://www.sciengine.com/sci-open/api/v1/open/router/query`（浏览器 XHR 捕获，**请求体未录得**）；全站检索后端为 `POST /sci-open/api/v1/open/SciSearch/searchNew`。
- 覆盖：《中国科学数据》（China Scientific Data）2016 年创刊，中英双语数据论文，覆盖地球 / 生态 / 生物 / 材料 / 信息等；每篇论文对应一份带 DOI 或 CSTR 的数据集。
- 门槛：**开放获取**，阅读 / 下载 PDF 免费；投稿需注册。
- 实测：2026-10-03，macOS arm64：`curl -k https://www.csdata.org/` → **200 但最终 URL 是 `https://www.sciengine.com/CSD/home`**（301）；不加 `-k` 时报 `SSL certificate problem: certificate has expired`（**csdata.org 证书已过期**）；CSD 首页 **200**，2,998 B（SPA 壳）；浏览器渲染后首页列出文章（首条 DOI `10.11922/11-6035.csd.2026.0121.zh`）。
- 上游：`https://www.sciengine.com/CSD/home`（中国科技出版传媒 / 中科院计算机网络信息中心）

## 坑

- **`csdata.org` 已迁到 SciEngine**，且自身 TLS 证书**已过期**：老书签会报证书错误，直接用 `sciengine.com/CSD`。
- **DataCite 查不到它**：`prefix=10.11922` 在 DataCite API 命中 **0**（实测 `{"total":0}`）——CSD 的 DOI 不在 DataCite 注册。别指望用 DataCite 收敛 CSD 数据论文；改走站内检索或 CNKI。
- 通用检索 URL `https://www.sciengine.com/plat/search?q=<词>&journal=CSD` **对该刊返回 0 Results**（实测）：期刊内检索要用页面内「Journal Search」，不是这个通用检索页。
- 页面是 SPA：`curl` 只拿到壳（2,998 B），条目必须经 API 或浏览器渲染。
