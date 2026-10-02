# escience.org.cn —— 科技资源与数据中心总入口

- 去哪找：门户 `https://www.escience.org.cn/`；**国家科学数据中心名录** `https://www.escience.org.cn/data-center`；元数据检索 `https://www.escience.org.cn/metadata/search`；**检索 API** `https://api.escience.org.cn/metadata/global-search/open/page?keyword=<词>&pageNum=1&pageSize=10`
- 什么时候用：**先在这里定位「该去哪个国家数据中心找」**（名录含依托单位、平台网址、联系电话、标识注册机构码）；跨中心检索科技资源（科学数据、大型科研仪器、种质、标本）；核一家数据中心的官方身份。
- 怎么搜：
  ```bash
  curl -s -H 'Origin: https://www.escience.org.cn' \
    'https://api.escience.org.cn/metadata/global-search/open/page?keyword=%E6%B0%94%E5%80%99&pageNum=1&pageSize=2'
  # keyword=%E6%B0%94%E5%80%99 即「气候」的 URL 编码
  # → {"code":200,"msg":"success","data":{"metaTotal":4440,"page":{
  #     "records":[{"oid":"774e715a1ac511e980780242ac120006:202115",
  #       "title":"<font color='#dd4b39'>气候</font>试验箱","resourceType":"meta",
  #       "utime":"2024-06-14 20:34:16","descr":"产品气候试验 大型科研仪器设备是指价值在50万元以上的…"}]}}}
  ```
  - 参数：`keyword`、`pageNum`、`pageSize`。**不带 `keyword` 时返回全量 `metaTotal`（实测 3,416,157）**，可用于判量。
  - 高亮直接写在 `title` 的 `<font color='#dd4b39'>` 里，脚本要剥标签。
  - 其他端点（从站点 bundle 还原，未逐个实测）：`/metadata/global-search/open/aggr`（分面聚合）、`/metadata/metadata/search/page`。
- 覆盖：科技资源元数据 **341 万+** 条（科学数据、大型科研仪器、生物种质、标本等），并汇总国家科学数据中心名录。
- 门槛：**免登录、无 key**。
- 实测：2026-10-03，macOS arm64，curl：门户与 `/data-center` → **200**；`api.escience.org.cn/metadata/global-search/open/page?keyword=%E6%B0%94%E5%80%99&pageNum=1&pageSize=2` → **200**，83,016 B，`metaTotal=4440`；去掉 `keyword` → **200**，`metaTotal=3416157`；**偶发 `{"code":500,"msg":"系统忙，请稍后再试！","data":null}`（63 B）**，重试即通。
- 上游：`https://www.escience.org.cn/`（科技部 国家科技资源共享服务平台）

## 坑

- API 主机是 **`api.escience.org.cn`**，与门户 `www.escience.org.cn` 不同域；浏览器里跨域要带 `Origin` 头（实测带 `Origin: https://www.escience.org.cn` 返回 200）。
- 名录页是 Vue SPA（`/js/chunk-*.js` + `app.97fed0ab.js`）：**直接 curl HTML 拿不到中心条目**，要条目数据走 API 或用浏览器渲染。
- **会偶发「系统忙」**：同一 URL 先后两次请求，先返回 `{"code":500,"msg":"系统忙，请稍后再试！","data":null}`（63 B）、后返回正常 83 KB —— 脚本必须判 `code` 并重试，别把 200 状态码当成功。
- 带上 `Origin: https://www.escience.org.cn` 与 `Referer: https://www.escience.org.cn/` 更稳（实测正常返回的那次带了这两个头）。
- `title` 带 HTML 高亮标签，入库前必须清洗。
- 名录里的「平台网址」才是各中心真实入口；本层 `national-data-centers.md` 是逐站实测过的入口表。
