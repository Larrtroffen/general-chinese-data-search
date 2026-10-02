# who.int —— 世卫组织数据总入口

- 去哪找：**GHO 门户** `https://www.who.int/data/gho`；指标浏览 `https://www.who.int/data/gho/data/indicators`；《世界卫生统计》`https://www.who.int/data/gho/publications/world-health-statistics`；新门户 `https://data.who.int/`；机构知识库 IRIS `https://iris.who.int/`。
- 什么时候用：要 WHO 口径的跨国卫生对照（预期寿命、死亡率、免疫、卫生人力与经费）；要官方年度出版物《World Health Statistics》及其附表的现成表格；要 WHO 报告/指南全文（IRIS）。
- 怎么搜：
  ```bash
  # 机器可读取数走 GHO 的 OData 接口（本机实测可用，完整语法见 ../health/who-gho.md）
  curl -s 'https://ghoapi.azureedge.net/api/Indicator?$top=5'
  curl -s "https://ghoapi.azureedge.net/api/WHOSIS_000001?\$filter=SpatialDim eq 'CHN'&\$top=5"
  # 出版物与报告检索走 IRIS 网页（其 REST API 对本机匿名 403）
  curl -sI 'https://iris.who.int/'
  ```
  - GHO = 指标数据库（3099 个指标，OData v4，免 key）；WHS = 年度汇编报告（含 Annex 统计表 PDF/Excel）；IRIS = DSpace 7 机构库（报告/指南全文）。
- 覆盖：GHO 覆盖 190+ 国家/地区 × 年度（多数 2000 年至今）× 性别/年龄分组；WHS 自 2005 年起年度出版；IRIS 收录 WHO 全部出版物。
- 门槛：GHO 与门户免费无 key；WHS 报告 PDF 免费；IRIS 网页免费、**其 REST API 需认证且对本机匿名 403**。
- 实测：2026-10-03，macOS arm64，curl 8.x：`ghoapi.azureedge.net/api/Indicator?$top=2` → 200；`…/WHOSIS_000001?$filter=SpatialDim eq 'CHN'&$top=1` → 200（中国 2022 年记录，`Dim1=SEX_BTSX`）；`who.int/data/gho/publications/world-health-statistics` → 200 / 134 KB；`data.who.int/` → 200 / 56 KB（Sitefinity CMS 页面，**不是**新数据 API）；`data.who.int/api/`、`/api/indicators` → **404**；`iris.who.int/` → 200（DSpace 7，title "DSpace"）；`iris.who.int/server/api/core/items` → **401**；`iris.who.int/server/api/discover/search/objects?query=malaria` → **403 Forbidden**（WAF）。
- 上游：WHO；`https://www.who.int/data/gho`。

## 细节

### 与 health 层的关系

GHO OData 接口的**完整语法、指标码表与坑**已收在 `../health/who-gho.md`（本层不重复）；本卡只做"WHO 有哪些数据产品 + 从哪进"的总览。

### WHO 数据产品分工

| 产品 | 用途 | 形态 |
|---|---|---|
| GHO（`ghoapi.azureedge.net`） | 指标级跨国序列 | OData JSON，免 key |
| World Health Statistics | 年度汇编 + 附表 | 报告 PDF / Excel |
| Global Health Estimates | 死因与疾病负担估计 | 报告 + 数据表 |
| IRIS（`iris.who.int`） | 报告/指南/技术文件全文 | DSpace 网页（API 受限） |

## 坑

1. `apps.who.int/gho/athena/api/*.json` 是**已弃用的旧接口**（301 到 legacy 页），老教程别照抄。
2. `data.who.int` 只是 CMS 门户页，**没有 `/api/`**（实测 404）；取数仍回 `ghoapi.azureedge.net`。
3. IRIS 的 DSpace REST API 对本机匿名 **403/401**，全文检索只能用网页（或换网络重试）。
4. WHO 报告年份 ≠ 数据覆盖年份；引用附表时注明 WHS 版次。
