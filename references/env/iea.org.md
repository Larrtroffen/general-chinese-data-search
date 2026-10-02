# iea.org —— 国际能源统计与平衡表

- 去哪找：IEA 数据与统计 `https://www.iea.org/data-and-statistics`；数据浏览器/工具 `https://www.iea.org/data-and-statistics/data-tools`；API 服务 `https://api.iea.org/`。
- 什么时候用：要**国际能源署口径**的跨国能源数据——世界能源平衡表、石油/天然气/煤炭/电力统计、可再生能源、能源价格与排放（CO₂ from fuel combustion）、能源效率指标；做跨国能源结构、能源转型、IEA 情景对标。
- 怎么搜：站点为浏览器交互（数据浏览器需点选后导出）；本机 **Cloudflare 拦截**，`curl` 直连 403。已知有 `api.iea.org` 服务（根路径 404，说明是 API 主机），但端点文档与鉴权**未本机取得**。批量数据多经 IEA 的付费/订阅数据集发布。
- 覆盖：全球 + 成员国/主要经济体 · 1971–至今（视数据集）· 年度/月度 · 国家 × 能源品种 × 部门。
- 门槛：**混合**——部分汇总/月度数据免费（注册后可下），完整平衡表与详细数据集**付费/订阅**；有机构订阅渠道。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA）——`https://www.iea.org/data-and-statistics` → **403**（Cloudflare `Just a moment...`，5,715 B 挑战页）；`https://api.iea.org/` → 404 `Cannot GET /`（Express 响应，主机存在）。
- 上游：International Energy Agency。

## 细节

- 相关但不重复的源：EIA（[`eia.gov.md`](eia.gov.md)）有免费 API 与大量国际能源数据；世界银行（[`../intl/worldbank.org.md`](../intl/worldbank.org.md)）有能源指标码；UN Data / `comtrade`（[`../intl/comtrade.un.org.md`](../intl/comtrade.un.org.md)）可替代部分贸易口径。中国国内能源口径见 [`nea.gov.cn.md`](nea.gov.cn.md) 与国家统计局。

## 坑

1. **Cloudflare 强制挑战**：`curl`/无头请求 403；只能浏览器访问，或用带完整浏览器指纹的会话。
2. 免费区与付费区**边界经常变**（数据集名称带 "Free"/"Licensed"），引用前确认当前许可，别把摘要当全量。
3. `api.iea.org` 存在不等于公开：根 404，鉴权/端点未公开取得，按「需订阅/需 key」处理。
4. IEA 与 EIA/UN 对同一能源量**计量口径不同**（吨标煤 vs 油当量、总一次能源构成），跨国合并前统一单位与口径。
