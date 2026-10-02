# globalcarbonproject.org —— 全球碳预算数据集

- 去哪找：全球碳计划主页 `https://www.globalcarbonproject.org/`；年度全球碳预算 `https://globalcarbonbudget.org/`；数据中枢 `https://globalcarbonbudget.org/datahub/`；最新数据页 `https://globalcarbonbudget.org/data-hub/the-latest-gcb-data-2025/`；数据文件托管在 **Zenodo**（2025 版 DOI `10.5281/zenodo.17579107`）。
- 什么时候用：要**全球/各国碳排放时间序列**（化石燃料、土地利用变化、海洋与陆地碳汇、大气增长）做跨国对比或给中国排放找国际口径基准；要 IPCC 报告引用的权威碳预算数字；CSV/xlsx/netCDF 原始表。
- 怎么取：① 站点 `datahub` → `The Latest GCB Data (YYYY)` 页给出当年 Zenodo DOI；② 直接走 **Zenodo REST API**（免费、JSON）：
  ```bash
  # 元数据 + 文件清单（注意：Zenodo API 拒绝桌面浏览器 UA，用默认 curl UA）
  curl -sS 'https://zenodo.org/api/records/17579107' | head -c 500
  # 检索录（按标题/关键词）
  curl -sS 'https://zenodo.org/api/records?q=global+carbon+budget&size=5'
  ```
  结果形态：Zenodo 返回 JSON（含 `files[]`：`.nc`/`.xlsx`/`.csv`，单文件可达数百 MB）。
- 覆盖：全球 + 各国 · 化石燃料/水泥 1959–2024（部分数据产品 1982/1980–2024）· 年度 · 海洋模式逐格点 fCO₂/海气通量（netCDF，1959–2024）。
- 门槛：**免费**（数据 CC-BY-4.0，需按规范署名）。
- 实测：2026-10-03，macOS arm64，curl 8.x——`https://globalcarbonbudget.org/` → 200；`/datahub/` → 200；`/fossil-fuels/` → **404**、`/data/` → **404**（旧路径已废）；`/data-hub/the-latest-gcb-data-2025/` → 200，页内唯一数据 DOI 为 `10.5281/zenodo.17579107`；`https://zenodo.org/api/records/17579107`（默认 curl UA）→ 200，标题 `Global Carbon Budget 2025 …`、`license {id: cc-by-4.0}`、`files` 含多个 `GCB2025_*.nc`（1959–2024）；同一 URL 用桌面浏览器 UA → **403 Forbidden**。
- 上游：Global Carbon Project（Future Earth / IGBP 等联合）；年度预算论文见 *Earth System Science Data*（ESSD）。

## 细节

- 2025 版部分录（record 21223061）是 concept DOI `17579107` 的最新版本；`conceptrecid` 指向整套，`id` 指向具体版本，版本更新时 DOI 后缀会变，引用请用页面给的 DOI。
- 数据文件分两类：**`.nc`**（海洋模式逐格点，数百 MB）与 **汇总表**（各国/全球年度碳收支，通常 xlsx/csv，在 Global Carbon Budget 论文的 Zenodo 录里）。
- Zenodo 检索对中文/长句效果差，用英文短词（`global carbon budget`、`GCB 2025`）。

## 坑

1. **Zenodo API 挡浏览器 UA**：桌面 Chrome UA 返回 403，默认 `curl` UA 才 200；脚本里别统一套浏览器 UA。
2. `globalcarbonbudget.org` 的 `/fossil-fuels/`、`/data/` 等猜测路径是 404；数据下载页路由为 `/datahub/` 与 `/data-hub/the-latest-gcb-data-YYYY/`。
3. Zenodo 文件体积大（数百 MB 到 1 GB 级），先看 `files[].size` 再下；本机到 Zenodo 往返慢，脚本设 ≥30 s 超时。
4. 署名与口径：引用 GCB 要同时给「数据 DOI + 对应 ESSD 论文」；各国排放为**国界内**口径，与 CEADs（`ceads.net.md`）的省份加总口径不同，别直接相减。
