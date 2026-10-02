# ncmi.cn —— 国家人口健康科学数据中心

- 去哪找：门户 `https://www.ncmi.cn/`（英文版 `https://www.ncmi.cn/index.html?language=en`）；数据浏览 `https://www.ncmi.cn/phda/browse.html`；高级检索 `https://www.ncmi.cn/advancedSearch/advanced_search.html`；数据证书检索 `https://www.ncmi.cn/dataSearch/certificate_search.html`。
- 什么时候用：要**国内人口健康领域的科研数据集**（人体成分、糖尿病并发症、胸片标注、HIV/AIDS、体质健康、流动人口、心理、PM2.5/NO2 等环境暴露…）；要带**数据凭证/证书**、可正式引用的共享数据集；要按学科/来源/年份/产生方式/地理范围组配的高级检索。
- 怎么搜：浏览/检索以 **HTML + 前端渲染**为主，另有底层 JSON 接口（从页面 JS `data_search*.js` 还原）——
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 浏览（type=1）/ 关键词检索（type=2），实测 200
  curl -s -A "$UA" 'https://www.ncmi.cn/phda/browse.html?type=2&searchField=keyword&keyword=%E9%AB%98%E8%A1%80%E5%8E%8B'
  # ② 底层检索（POST，参数多，见「细节」）；本机最小参数返回 500
  curl -s -A "$UA" -X POST -H 'Referer: https://www.ncmi.cn/advancedSearch/advanced_search.html' \
    --data 'searchFields=&keywords=%E9%AB%98%E8%A1%80%E5%8E%8B&pageNumber=1' \
    'https://www.ncmi.cn/dataSearch/search_data.do'
  ```
- 覆盖：首页统计卡标注「数据集总数 19239 个 / 6558 个」「数据总量 863.929 千万条」「数据记录 970.109 千万条」（口径以站方为准）；主题覆盖临床、影像、组学、环境、体育、心理、公共卫生等。
- 门槛：浏览/检索部分免登录；**下载数据需注册/登录**（部分需申请授权）。
- 实测：2026-10-03，macOS arm64，curl 8.x：`https://www.ncmi.cn/` 200（218,638 B，`<title>国家人口健康科学数据中心`）；`/phda/browse.html` 200（94,959 B）；`/phda/browse.html?type=2&searchField=keyword&keyword=高血压` 200（94,968 B，结果由前端渲染）；`/advancedSearch/advanced_search.html` 200（71,798 B）；`https://www.ncmi.cn/index.html?language=en` 200（136,622 B）；POST `/dataSearch/search_data.do`（最小参数）→ **500**「页面错误」。
- 上游：国家人口健康科学数据中心（ncmi.cn）；关联平台 `phsciencedata.cn`（见 `phsciencedata.cn.md`）。

## 细节

### 接口（从 `/modules/datasearch/js/data_search.js`、`data_search_new.js` 还原）

| 用途 | 端点 | 方法 | 备注 |
|---|---|---|---|
| 关键词检索 | `/dataSearch/search_data.do` | POST | 参数见下 |
| 结果计数/汇总 | `/dataSearch/allDataSum.do` | POST | 同组参数 |
| 检索面元 | `/dataSearch/getProjectFacet.do` | POST | `searchFields/keywords/tureandfales` |
| 热词 | `/dataSearch/hotkeyword.do` | — | 首页词云 |
| 分类统计 | `/dataSearch/getStatisticsProjectData.do` | POST | `type=` |
| 数据详情 | `/phda/dataDetails.do?id=`、`/phda/dataDetails.do?type=project_data&id=` | GET | |
| 数据表 | `/phda/dataTable.do?type=data_table&tableId=<id>` | GET | |
| 项目详情 | `/phda/projectDataDetail.do?id=` | — | |
| 证书检索 | `/dataSearch/certificate_search.html` | 页面 | |

`search_data.do` 主要参数（`data_search.js` 第 796–833 行）：

```
searchFields, keywords, tureandfales, orand, searchField, keyword,
fkSubjectId(学科分类), fkScienceDataId(科学数据分类), departmentId(数据来源),
publishYear(发布时间), modeProduction(产生方式), dataType, speciesType,
humanGeneticsType, dataSource, entityDataFlag, dataQualityType, dataAuthority,
chargingMethod, dataSize, dataSuffix, submitDateOrder, sizeOrder,
downloadOrder, clickOrder, organ(器官), keywordMenu, subjectheadings,
geographicRange(地理范围), startTime, endTime, timeType, pageNumber
```

- 浏览页 URL 参数：`type=1` 全部、`type=2&searchField=keyword&keyword=<词>` 关键词；另有 `searchField` 可换其他字段。
- 返回为 HTML（结果卡片由前端 JS 填充）；接口 JSON 结构未取到（POST 需完整参数/会话）。

## 坑

1. 探索到的最小 POST 组合返回 **500**，说明 `search_data.do` 需要配套参数/会话，**匿名裸调不可用**；稳妥路径是浏览器打开 `browse.html?type=2&…` 或高级检索页。
2. `browse.html` 页面体积固定（~95 KB），**关键词结果不在 HTML 里**，是前端渲染；curl 只能拿到壳。
3. 下载门槛：多数资源需注册；部分限机构/需申请，商用与公益收费口径并存（站点有「免费/公益免费、商业收费」筛选项）。
4. 站点分中英文两套（`?language=en`），英文版条目更少。

## 相关

- 同源平台「公共卫生科学数据中心」见 `phsciencedata.cn.md`（ncmi.cn 首页亦链接 `www.phsciencedata.cn`）。
