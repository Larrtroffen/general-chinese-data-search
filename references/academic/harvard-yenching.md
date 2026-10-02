# harvard-yenching —— 哈佛燕京汉籍与中文善本检索

- 去哪找：
  - 哈佛燕京图书馆：`https://library.harvard.edu/libraries/yenching`
  - 全哈佛馆藏目录 HOLLIS：`https://hollis.harvard.edu/`
  - LibraryCloud API（JSON）：`https://api.lib.harvard.edu/v2/items.json?q=<词>&limit=N`
  - 中文善本数字展 CURIOSity：`https://curiosity.lib.harvard.edu/chinese-rare-books`
  - 费正清中心：`https://fairbank.fas.harvard.edu/`；其藏书：`https://library.harvard.edu/collections/fairbank-center-chinese-studies-collection`
- 什么时候用：找**中文善本/古籍**（宋元明清刻本、地方志、民国书刊）、拓片、东亚外文书目，或定位哈佛所藏中国研究文献、拿中文古籍图像时。
- 怎么搜：优先 API（**本机 curl 对 Harvard 域多返 429**，改浏览器，见坑）：
  1. LibraryCloud：`https://api.lib.harvard.edu/v2/items.json?q=民国&limit=2` → JSON（`pagination.numFound`、`items.mods[]`）。
  2. HOLLIS（Primo VE）：`https://hollis.harvard.edu/discovery/search?vid=01HVD_INST:HVD2&tab=Everything&query=any,contains,<词>`。
  3. 中文善本：`https://curiosity.lib.harvard.edu/chinese-rare-books/catalog.json?q=<词>&per_page=N` → JSON（`meta.pages.total_count`、`data[].id`）。
  4. 图像/IIIF：`https://iiif.lib.harvard.edu/manifests/ids:<id>` → 302 到 `https://nrs.lib.harvard.edu/URN-3:…:MANIFEST:2`（IIIF Presentation 2，`sc:Manifest`）。
- 覆盖：Harvard-Yenching Library（哈佛燕京图书馆，东亚藏书重镇）+ 费正清中心藏书；含 Chinese Rare Books Digitization Project（善本，按系列如 Hart Collection 分组）、地方志、拓片；HOLLIS 覆盖全哈佛馆藏；粒度=书目/册/图像。
- 门槛：免费、检索免登录；善本部分图像在线可看（CURIOSity）；原件到馆阅览/外借需哈佛 ID 或馆际互借。
- 实测：2026-10-03，无头 Chromium 打开 `https://api.lib.harvard.edu/v2/items.json?q=民国&limit=2` → JSON，`numFound 405401`；同 URL `curl` → **429**。`https://curiosity.lib.harvard.edu/chinese-rare-books/catalog.json?q=論語&per_page=3` 浏览器 → 200 JSON，`total_count 46`（curl 对 CURIOSity → 202 空体）。`https://iiif.lib.harvard.edu/manifests/ids:11927378` → 302 至 NRS，manifest 内容为 `sc:Manifest`。
- 上游：<https://library.harvard.edu/libraries/yenching>、<https://fairbank.fas.harvard.edu/>、<https://library.harvard.edu/services-tools/iiif-manifests-digital-objects>

## 细节

- LibraryCloud v2 端点族：`/v2/items.json`、`/v2/collections.json`、`/v2/items/<id>.json`（本机仅实测 items.json）。
- HOLLIS 为 Ex Libris Primo VE，`vid=01HVD_INST:HVD2`；结果页是 SPA，需浏览器。
- CURIOSity 是 Blacklight 展览平台，`catalog.json`/`catalog.html` 都可直取；中文善本按项目系列过滤（如 `f[series_ssim][]=Harvard-Yenching+Library+Chinese+Rare+Books+Digitization+Project-Hart+Collection`）。
- IIIF：旧 `iiif.lib.harvard.edu/manifests/…` 现统一 302 到 `nrs.lib.harvard.edu`（新 DRS 命名空间，URN 形如 `URN-3:HUAM:INV204583_DYNMC:MANIFEST:2`）。

## 坑

1. **本机 curl 对 Harvard 域普遍 429**：`api.lib.harvard.edu`、`iiif.lib.harvard.edu` 实测均 429（浏览器同 URL 正常）；CURIOSity curl → 202 空体。统一用无头 Chromium。
2. HOLLIS 直接 `curl` 拿不到结果（JS SPA）。
3. 善本原件不外借；数字图像版权与使用条件以各记录页声明为准。
4. LibraryCloud、CURIOSity、HOLLIS 三处索引范围不同，需交叉查。
