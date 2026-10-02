# who-gho —— 世界卫生组织全球卫生指标 API

- 去哪找：**OData API 基址** `https://ghoapi.azureedge.net/api/`；门户 `https://www.who.int/data/gho`；指标浏览 `https://www.who.int/data/gho/data/indicators`。
- 什么时候用：要**WHO 全球卫生指标**（预期寿命、健康预期寿命、死亡率、免疫、营养、卫生人力、卫生支出…）；要按国家（ISO3）/年份/性别取跨国对照或中国纵向序列；要免 key 的机器可读接口。
- 怎么搜：整个目录与数据都是 **OData JSON，匿名免 key**——
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 全部指标（3099 条），拿 IndicatorCode
  curl -s -A "$UA" 'https://ghoapi.azureedge.net/api/Indicator' | jq -r '.value[] | .IndicatorCode+"\t"+.IndicatorName'
  # ② 按名称模糊搜索
  curl -s -A "$UA" 'https://ghoapi.azureedge.net/api/Indicator?$filter=contains(IndicatorName,%27life%20expectancy%27)'
  # ③ 取数据（分国家/年份/性别）
  curl -s -A "$UA" 'https://ghoapi.azureedge.net/api/WHOSIS_000001?$filter=SpatialDim%20eq%20%27CHN%27&$top=5'
  ```
  返回：`value[]`，字段 `IndicatorCode / SpatialDim(ISO3) / SpatialDimType / ParentLocation / TimeDim / Dim1Type(SEX) / Dim1 / NumericValue / Low / High / Value("48.1 [45.4-50.8]")`。支持 `$filter / $top / $skip / $select / $orderby`。
- 覆盖：**3099 个指标**（实测）；国家/地区 × 年份（多数 2000–2023）× 性别/年龄分组；WHO 官方口径，按年滚动更新。
- 门槛：免费，**无需 key**。
- 实测：2026-10-03，macOS arm64，curl 8.x 匿名：`https://ghoapi.azureedge.net/api/Indicator` 200（414,703 B，`value` 长度 **3099**）；`…/Indicator?$filter=contains(IndicatorName,'life expectancy')` 200（命中 4 条 `WHOSIS_0000xx`）；`…/WHOSIS_000001?$top=2` 200（`SpatialDim:"SOM"`、`Value:"48.1 [45.4-50.8]"`、`TimeDim:2008`）；旧 `https://apps.who.int/gho/athena/api/…` 301 → `https://www.who.int/data/gho/legacy`（已弃用）。
- 上游：WHO Global Health Observatory（GHO）。

## 细节

### 常用 IndicatorCode

| 代码 | 指标 |
|---|---|
| `WHOSIS_000001` | Life expectancy at birth (years) |
| `WHOSIS_000002` | Healthy life expectancy (HALE) at birth (years) |
| `WHOSIS_000015` | Life expectancy at age 60 (years) |
| `WHOSIS_000007` | Healthy life expectancy (HALE) at age 60 (years) |

- 端点是 OData v4 风格：元数据 `…/api/$metadata`；集合名即 `Indicator`、`{IndicatorCode}` 等。
- 中国取数：加 `$filter=SpatialDim eq 'CHN'`；ISO3 代码见 WHO 国家表。
- 分页：默认返回整表（有的指标几十万行），务必配 `$top`/`$skip` 或 `$filter`。

## 坑

1. 旧 `apps.who.int/gho/athena/api/*.json` **已下线**（301 到 legacy 页），网上老教程里的 athena 接口不要再用。
2. `{IndicatorCode}` 数据集可能很大（百万行级），**不要整表拉**；先 `Indicator` 定位代码，再带 `$filter`。
3. `Value` 是带区间的字符串（`"48.1 [45.4-50.8]"`），数值用 `NumericValue/Low/High`。
4. 门户 `who.int/data/gho` 是 JS SPA，curl 抓不到指标列表——**列表走 API，不走门户页**。

## 相关

- 跨国卫生/人口对照：与 `../intl/` 的国际统计源交叉；全球人口分母见 `population.un.org.md`。
