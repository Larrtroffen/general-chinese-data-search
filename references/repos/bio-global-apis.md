# bio-global-apis —— 国际生物与地学数据接口

- 去哪找：GBIF `https://api.gbif.org/v1/`；NASA 地球观测 CMR `https://cmr.earthdata.nasa.gov/search/`；WorldClim 文档站 `https://www.worldclim.org/data/`，真实文件在 `https://geodata.ucdavis.edu/climate/worldclim/`。
- 什么时候用：要**物种分布记录 / 分类名核对**（GBIF）、**全球气候栅格**（WorldClim）、**NASA 及合作机构对地观测数据集与 granule 清单**（CMR）。
- 怎么搜：GBIF 与 CMR 免 key 直接 curl JSON；WorldClim 无检索接口，只能按 URL 模板直下 zip。
- 覆盖：GBIF 全球生物多样性（occurrence / dataset / species）；CMR 全球对地观测 collection 与 granule（示例关键词命中 3,037 / 3,047,540）；WorldClim 2.1 历史与情景气候，10m/5m/2.5m/30s 分辨率，变量 tmin/tmax/tavg/prec/srad/wind/vapr/bio。
- 门槛：三家**检索**全免费免 key；NASA **下载 granule** 需 Earthdata Login（免费注册）；WorldClim 直下无门槛。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20s 超时，同主机请求间隔 ≥1.5s）——`GET https://api.gbif.org/v1/species/match?name=Ailuropoda%20melanoleuca` → 200（usageKey 2433399 / matchType EXACT / confidence 99）；`GET https://api.gbif.org/v1/dataset/search?q=amphibian&limit=2` → 200（count 2136）；`GET https://cmr.earthdata.nasa.gov/search/collections.json?keyword=precipitation&page_size=2` → 200（响应头 `cmr-hits: 3037`）；`GET .../granules.json?short_name=MOD11A1&page_size=2` → 200（`cmr-hits: 3047540`）；`HEAD https://geodata.ucdavis.edu/climate/worldclim/2_1/base/wc2.1_10m_bio.zip` → 200 `application/zip`。
- 上游：GBIF `https://www.gbif.org/developer/summary`；CMR `https://cmr.earthdata.nasa.gov/search/`；WorldClim `https://www.worldclim.org/`。

## 细节

### GBIF —— 物种、occurrence、数据集

```bash
curl -sS 'https://api.gbif.org/v1/species/match?name=Ailuropoda%20melanoleuca'
# → {"usageKey":2433399,"canonicalName":"Ailuropoda melanoleuca","rank":"SPECIES","status":"ACCEPTED",
#    "confidence":99,"matchType":"EXACT","kingdom":"Animalia",...}
curl -sS 'https://api.gbif.org/v1/dataset/search?q=amphibian&limit=2'
# → {"offset":0,"limit":2,"endOfRecords":false,"count":2136,"results":[...],"facets":...}
curl -sS 'https://api.gbif.org/v1/occurrence/search?q=Ailuropoda&limit=2'
# → {"offset":0,"limit":2,"endOfRecords":false,"count":500,"results":[{key,datasetKey,taxonKey,
#    kingdomKey,basisOfRecord,individualCount,countryCode,...}]}
```

- 常用端点：`/v1/species/match?name=`、`/v1/species/search?q=`、`/v1/occurrence/search?`、`/v1/occurrence/<key>`、`/v1/dataset/search?q=`、`/v1/dataset/<uuid>`；分页 `offset` + `limit`。
- 结果形态：JSON；`count` = 命中总数，`results` = 当页数组。

### NASA Earthdata CMR —— collection 与 granule

```bash
curl -sS 'https://cmr.earthdata.nasa.gov/search/collections.json?keyword=precipitation&page_size=2'
# → 200；body 为 {"feed":{"updated","id","title","entry":[collection,...]}}
#   命中总数只在响应头：cmr-hits: 3037
curl -sS 'https://cmr.earthdata.nasa.gov/search/granules.json?short_name=MOD11A1&page_size=2'
# → 200；cmr-hits: 3047540；entry[] 字段 producer_granule_id,time_start,time_end,id,
#   collection_concept_id,granule_size,data_center,links
```

- 参数：`keyword` / `short_name` / `version` / `provider` / `collection_concept_id` / `temporal` / `bounding_box`；分页 `page_size`、`page_num`。
- **granule 查询必须限定 collection**：不带限定直接查会 400 `The CMR does not allow querying across granules in all collections`。

### WorldClim —— 无 API，URL 模板直下

```
页面  https://www.worldclim.org/data/worldclim21.html        （Sphinx 文档站，列出全部下载链接）
模板  https://geodata.ucdavis.edu/climate/worldclim/2_1/base/wc2.1_<分辨率>_<变量>.zip
      分辨率 10m / 5m / 2.5m / 30s ； 变量 tmin tmax tavg prec srad wind vapr bio
例    https://geodata.ucdavis.edu/climate/worldclim/2_1/base/wc2.1_10m_bio.zip
```

- 实测 `HEAD wc2.1_10m_bio.zip` → 200 `application/zip`（文件存在、可取）。
- 另有分幅目录 `.../2_1/tiles/` 与生物气候变量说明 `bioclim.html`。

## 坑

1. GBIF `occurrence/search` 拉不动全量：`offset`/`count` 触顶后要靠 download API（需账号）。（上游声明，未本机实测）
2. GBIF 的 `q` 是全文模糊匹配；要精确请先 `species/match` 拿 `usageKey`，再用 `occurrence/search?taxonKey=`。
3. CMR 的 JSON 是 OpenSearch Atom 风格——**总数在响应头 `CMR-Hits`，body 里没有**；只读 body 会误判成「只有 page_size 条」。
4. WorldClim 官网只是文档站，文件在 `geodata.ucdavis.edu`；30s 全球包单变量可达数百 MB。
5. NASA granule 下载除登录外一般还需带 token（`Authorization: Bearer`）。（上游声明，未本机实测）
