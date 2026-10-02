# science-data-apis —— 七大科学数据中心检索接口

- 去哪找：`national-data-centers.md` 给入口，本卡给**逐个实测过的检索/目录接口**。JSON 可直连的三家：微生物 `nmdc.cn`、基因组 `ngdc.cncb.ac.cn`、地球系统 `geodata.cn`。
- 什么时候用：要**按学科取国内权威数据本体**（天文 / 海洋 / 空间 / 极地 / 微生物 / 基因组 / 地球系统），且想先用命令行把目录与命中数摸清，再决定是否走浏览器与注册。
- 怎么搜：三家有 JSON API 的按下方模板直接 curl；其余四家（NADC / NMDIS / NSSDC / 极地）检索是**服务端渲染页或 SPA**，只能给入口，后端接口见「细节」表并注明是否跑通。
- 覆盖：国家科学数据中心体系里**除人口健康 / 农业 / 气象 / 地震 / 生态等**（见各自卡片与 `national-data-centers.md`）之外的七家；数据形态为观测记录、元数据目录、数据集清单，多带 DOI / CSTR。
- 门槛：浏览与目录检索基本免费免登录；**下载普遍要注册 / 实名**（极地、地球系统、微生物），部分子库需登录会话。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20s 超时，同主机请求间隔 ≥1.5s）——`GET https://ngdc.cncb.ac.cn/search/api/ngdc?q=tp53` → 200 JSON（hitCount 85,821）；`GET https://nmdc.cn/api/services/nmdcweb/api/dataset/metadata/page?pageNum=1&pageSize=3` → 200（totalElements 365）；`GET http://www.geodata.cn/service/scidata/entry/search/?word=地震&page=1&pageSize=5` → 200（total 260）；`GET https://nadc.china-vo.org/essearch?endpoint=&keyword=FAST&fuzziness=1` → 200 HTML/27,984 B 结果页（命中 FAST 数据发布消息）；`POST https://vsso.nssdc.ac.cn/nssdc/coreMetadata/coreMetadataList` → 200 `{"msg":null,"code":500}`；`GET https://www.chinare.org.cn/api/dif/?page=1` → 200 但为 SPA 壳；`GET https://mds.nmdis.org.cn/sinfo/front/solr/getSiteSearchList?keyWords=海洋&page=1&pageSize=5` → 404。
- 上游：各中心门户；体系名录 `https://www.escience.org.cn/data-center`。

## 细节

### 逐站探测结果（2026-10-03）

| 中心 | 可用的检索接口 | 形态 | 跑通 |
|---|---|---|---|
| 天文 NADC | `nadc.china-vo.org/essearch`（全站）+ `/res/resource/?tag=N`（数据资源） | HTML | ✅ 结果页可读 |
| 海洋 NMDIS | 前端调 `/sinfo/front/solr/getSiteSearchList`（Solr） | JS 声明 | ❌ 两域名均 404 |
| 空间 NSSDC | `POST vsso.nssdc.ac.cn/nssdc/coreMetadata/coreMetadataList` | JSON | ⚠️ 200 但 `code:500` |
| 极地 chinare | `/api/dif/`、`/api/news/`（记录 URL 由 JS 内嵌） | SPA 壳 | ❌ 匿名只回 index.html |
| 微生物 NMDC | `GET nmdc.cn/api/services/nmdcweb/api/dataset/metadata/page` | JSON | ✅ 365 条 |
| 基因组 NGDC | `GET ngdc.cncb.ac.cn/search/api/ngdc?q=` | JSON | ✅ 85,821 命中 |
| 地球系统 geodata | `GET www.geodata.cn/service/scidata/entry/search/` | JSON | ✅ 260 命中 |

### JSON 三家的最小命令与结果形态

```bash
# 微生物 NMDC —— 元数据/数据集检索（pageNum 必填，缺则报 Required Integer parameter 'pageNum'）
curl -sS 'https://nmdc.cn/api/services/nmdcweb/api/dataset/metadata/page?pageNum=1&pageSize=10&keyword=&sortType=&sortOrder=&group='
# → {"data":{"content":[{id,chineseName,englishName,group,identifier,subject,secondSubject,threeLvlSubject,keyword,description,...}],
#          "totalElements":365,"pageNumber":0,"pageSize":10,...},"status":0,"msg":"成功"}
#   实测 pageNum=1&pageSize=3 → totalElements=365；keyword=coli / 基因组 均未见过滤（前端参数名 keyword）

# 基因组 NGDC —— 跨库聚合检索（NGDC + 合作库 + EBI + NCBI，一次全打）
curl -sS 'https://ngdc.cncb.ac.cn/search/api/ngdc?q=tp53'
# → {"code":..,"message":..,"result":{"hitCount":85821,"dbHits":76,
#      "databases":[{"hitCount":2252,"name":"VarClear","description":..,"id":"genekang","categories":[..],"url":..}]}}
#   兄弟端点：/search/api/owner/ngdc?q=  /search/api/owner/partner?q=  /search/api/ebi?q=  /search/api/ncbi?q=  /search/api/dbs  /search/api/search/popular  /search/api/recommendation?keyword=
#   注意 /search/api/search 是 404，正确是 /search/api/ngdc

# 地球系统 geodata —— 数据条目检索 + 分面
curl -sS 'http://www.geodata.cn/service/scidata/entry/search/?word=%E5%9C%B0%E9%9C%87&page=1&pageSize=5'
# → {"op_read":{"data":[{guid,title,disciplineName,organizationName,ownerName,ownerOrganization,filesize,hits,createdTime,...}],
#               "total":260},"boundBox":...}
#   分面：/service/scidata/entry/searchwithfacets/（params word/dataStartTime/dataEndTime，响应 op_read.{主题词,学科}）
#   分类树：/service/scidata/category/tree/?publisherGuid=&categoryId=&hierarchyLevelNo=
#   文件：/service/filestorage/download?fileId=  /service/filestorage/get?fileId=；缩略图与文档走 http://img.data.ac.cn/
```

### 无公开 JSON 的四家（入口与后端线索）

| 中心 | 检索入口 / URL 模板 | 后端线索 |
|---|---|---|
| 天文 NADC | `https://nadc.china-vo.org/essearch?endpoint=<端点>&keyword=<词>&fuzziness=1`；资源列表 `/res/resource/?tag=<分类号>`；论文数据 `/res/paperdata` | `endpoint` 取值取自页面下拉：空=全部、`astrocloud_cms,explore_cms,psp_cms,astrodict_cms`=新闻文章、`metadata`=元数据、`meeting`=会议。首页模板里的 `/registry/api/resources/{hot,latest,paperdata}` 与 `/getstat?type=registry-api-resources-stats` 实测 404（该段调用已被注释） |
| 海洋 NMDIS | 搜索页 `https://mds.nmdis.org.cn/pages/totalSearch.html?query=haiyang`（`query` 或 `input`/`haiyang`/`shengwu`/`huaxue`/`wuli`）；数据详情 `/pages/dataViewDetail.html?type=1&did=..&dataSetId=..` | `totalSearch.js` 调 `GET /sinfo/front/solr/getSiteSearchList?keyWords=&page=1&pageSize=10&dataType=`（`dataType` 空=全部 / `dataSet`=平台数据 / `article`=平台动态）；另有 `/sdm/front/directory/getDirectoryList`、`/scms/front/statistics/list` |
| 空间 NSSDC | `https://vsso.nssdc.ac.cn/nssdc_zh/html/vssolist.html?searchKeywords=<urlencoded>`（亦支持 `keyWord`/`querysourceProjectCh`/`queryObservationPlatform`/`queryObservationEquipment`） | `POST /nssdc/coreMetadata/coreMetadataList`，body `{searchKeywords,keywords,sourceProjectCh,observatoryCh,instrumentCh,pageSize,pageNum,releaseStatus:5,releaseDateSort:"DESC",slidervalue}` → `{code,data:{datasetPage:{total,pageSize}}}`；`POST /nssdc/userLogin/getHostNames` 返 JSON 主机信息 |
| 极地 chinare | `https://www.chinare.org.cn/data-center/metadata`（SPA）；样本库 `/sample/{biology,rock,sediment,snow,meteorite,gene}` | 记录字段带 `url: /api/dif/<uuid>/`、`/api/news/<uuid>/`（DIF 元数据，字段 entry_title/data_author/organization）；匿名 GET `/api/dif/?page=1` 与 `/api/dif/<uuid>/` 均回 SPA 壳 |

## 坑

1. **别照抄首页 JS 里的接口**：NADC 首页模板里 4 个 `registry/api` 调用全被注释且实测 404；NGDC 的 `/search/api/search` 是 404，真名是 `/search/api/ngdc`。
2. **NMDC 的 `pageNum` 是硬必填**，且从 1 起；返回体里 `pageNumber` 却是 0 起（`number`/`pageNumber` 字段勿当请求参数用）。
3. **NGDC 一次请求打四库**（NGDC + partner + EBI + NCBI），`searchAll` 会并发 5 个 XHR；脚本里只调 `/api/ngdc` 更省。
4. **NSSDC / 极地是 SPA**：`code:500`（NSSDC）与 SPA 壳（极地）说明**匿名直连拿不到数据**，需真实浏览器会话或登录；不要把这些状态当作「该库无数据」。
5. **geodata 是 http（非 https）且走 `.json`/`.swf` 老式 REST**，`contextURL='/'`；分页用 `page`/`pageSize`，响应恒为 `{op_read:{...}}` 包一层。
6. 下载侧：NMDC / NGDC 子库（GSA 等）要注册，极地页面明示「数据仅限科学研究使用」，geodata 下载跳登录（`/home/login?url=%2Fdata%2F`）。**检索可匿名 ≠ 数据可取**。
