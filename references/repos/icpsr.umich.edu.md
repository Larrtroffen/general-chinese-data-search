# icpsr.umich.edu —— 社科数据档案与变量级检索

- 去哪找：门户 `https://www.icpsr.umich.edu/`；研究检索 `https://www.icpsr.umich.edu/web/ICPSR/search/studies?q=<词>`；变量检索 `https://www.icpsr.umich.edu/web/ICPSR/search/variables?q=<词>`
- 什么时候用：找**美国及跨国的经典社科数据**（ANES、GSS、ICPSR 系列研究）、中国主题调查；做**变量级**检索（哪个研究的哪个变量问过什么、怎么编码）；要 study 号 + 代码本。
- 怎么搜：官网被 Cloudflare 全域拦，本机 curl 与无头/有头浏览器都过不去；用两条替代路：
  1. **DataCite API 按 ICPSR 前缀检索**（实测可用，ICPSR 数据 DOI 前缀固定 `10.3886`）：
     ```bash
     curl -s 'https://api.datacite.org/dois?query=china&prefix=10.3886&page%5Bsize%5D=5'
     # → {"data":[{"id":"10.3886/icpsr03552.v2","attributes":{"doi":"10.3886/icpsr03552.v2",
     #     "creators":[{"givenName":"Xueguang","familyName":"Zhou",…}],…}}]}
     ```
     拿到 DOI 即可 `https://doi.org/10.3886/icpsr03552.v2`。
  2. 浏览器人工访问检索页（变量级检索只能走网页）；下载走机构 IP / OpenAthens / 或注册账号。
- 覆盖：ICPSR 建于 1962，社科最大的数据档案之一（政治学 / 犯罪学 / 人口 / 老龄化 / 教育）；条目 = study + 变量 + 代码本；中国相关为其中一个专门子集。
- 门槛：检索公开；**下载多数需机构订阅或注册**（部分开放研究可直接下）；变量级检索公开。
- 实测：2026-10-03，macOS arm64：`curl 'https://www.icpsr.umich.edu/icpsrweb/ICPSR/studies?q=china&rows=2&format=json'` → **403**，Cloudflare `Just a moment...`；无头（`headed:false`）与有头（`headed:true`）Chromium 打开 `/web/ICPSR/search/studies?q=china` 均停在 `Just a moment...`（挑战未通过）。**DataCite 通道**：`prefix=10.3886` → **200**，命中 `10.3886/icpsr03552.v2`（作者 Xueguang Zhou，Duke）。
- 上游：`https://www.icpsr.umich.edu/`（密歇根大学 ICPSR）

## 坑

- 官网在本机出口被 Cloudflare 拦死：**先走 DataCite**（只需知道前缀 `10.3886`），需要变量 / 代码本再换网络或浏览器手动过挑战。
- 旧接口 `/icpsrweb/ICPSR/studies?format=json` 文档稀缺、且现在直接 403，不要依赖它做自动化。
- DataCite 只给到 study 级元数据（标题 / 作者 / DOI），**没有变量清单与代码本**——那两个必须进官网。
