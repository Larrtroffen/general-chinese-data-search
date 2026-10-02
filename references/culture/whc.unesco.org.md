# whc.unesco.org —— 世界遗产名录与中国项目

- 去哪找：**UNESCO 世界遗产中心**世界遗产名录 `https://whc.unesco.org/en/list/`；按国筛选 `https://whc.unesco.org/en/list/?iso=cn`；地图 GeoJSON `https://whc.unesco.org/?cid=31&l=en&mode=geojson`；单遗产页 `https://whc.unesco.org/en/list/<id>/`。
- 什么时候用：要**世界遗产名录**（全球与中国项目、类别、列入时间、濒危状态、跨国项目、组成部分坐标）；核对「中国第 N 项世界遗产」「某地是否为世界遗产/其官方英文名与 `id_no`」；做遗产空间分布图。
- 怎么搜：站点**有 Cloudflare 拦截**，curl 直连 403（`Just a moment...`），须用**真实浏览器**（无头 Chromium 可过），再在同源页面内 `fetch` GeoJSON：
  ```js
  // 在 whc.unesco.org 页面上下文内
  const j = await fetch('https://whc.unesco.org/?cid=31&l=en&mode=geojson').then(r=>r.json());
  // j.features: 6346 个「组成部分」点，properties = {id_no,title,component_state,component_name,cat,icon,danger}
  const cn = j.features.filter(f => /china/i.test(f.properties.component_state));   // 237 个组成部分
  new Set(cn.map(f=>f.properties.id_no)).size                                        // 61 个独立遗产
  ```
  结果形态：**JSON（GeoJSON FeatureCollection，Point 几何）**。属性页与列表页为 HTML。`cat`：1 文化遗产、2 自然遗产、3 混合（双/三 遗产）。
- 覆盖：全球 **1273 项**遗产（首页自述），本机 GeoJSON 快照 6346 个组成部分；中国 **237 个组成部分 → 61 项**独立遗产（含长城、泰山等跨组成项目）；字段含 `danger`（濒危）、`component_state`（归属缔约国）、`id_no`（唯一遗产号）。更新随世遗大会（年度）。
- 门槛：**免费、无 key**；但**Cloudflare 拦 CLI**，须浏览器取数。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA + Chromium 无头——`curl https://whc.unesco.org/en/list/?iso=cn` → **403**（Cloudflare `Just a moment...`，3.3 KB）；Chromium 打开同 URL → **200**，`<title>UNESCO World Heritage Centre - World Heritage List</title>`，页内计数 `1273 Properties`；页面内 `fetch('https://whc.unesco.org/?cid=31&l=en&mode=geojson')` → **200 GeoJSON**，`features` 6346 条；`?iso=cn&mode=geojson` 该站返 **520**，但全量 GeoJSON 按 `component_state` 过滤即得中国 237 组成部分 / 61 项（例 `id_no:438 The Great Wall`、`id_no:437 Mount Taishan`）。
- 上游：<https://whc.unesco.org/en/list/>（UNESCO World Heritage Centre）。

## 细节

- 地图端点 `?cid=31&l=en&mode=geojson`（`cid=31` 为名录）；本机实测 `iso` 参数不改变返回，须**自行按 `component_state` 过滤**。
- Feature 属性：`id_no`（遗产号）、`title`（英文名）、`component_name`（组成部分名）、`component_state`（缔约国）、`cat`（1 文化/2 自然/3 混合）、`icon`、`danger`（0/1）。
- 单遗产详情（含坐标、列入年、标准、地图、文档）：`/en/list/<id_no>/`。
- 国际组织统计口径（教科文/世行等）见 `../intl/` 层；世界遗产的中文名录另见 `ncha.gov.cn.md` 与中国联合国教科文组织全国委员会。

## 坑

1. **Cloudflare 拦 CLI**：curl/wget 一律 403「Just a moment...」，无头 Chromium 可通过；换 UA 无效。
2. GeoJSON 是**组成部分级**（一遗产多点），统计「遗产项数」必须按 `id_no` 去重（中国 237→61）。
3. 名单/计数以世遗中心官网为准；`1273` 为 2026-10 页面值，随大会变动。
4. 中国项目的**中文名**不在该 GeoJSON 内（仅英文 `title`），中文口径回 `ncha.gov.cn.md` 与文化和旅游部。
5. `/en/list/json/` 非 JSON（返回 HTML），勿误用。
