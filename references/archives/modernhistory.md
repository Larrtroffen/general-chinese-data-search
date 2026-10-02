# modernhistory.org.cn —— 抗战与近代中日文献平台

国家社科基金抗日战争研究专项工程，中国历史研究院近代史研究所承办（版权页：中国社会科学院、中国历史研究院、国家图书馆、国家档案局版权所有）。前端是 Vue SPA，但**后端 REST 接口完全匿名开放**，浏览器里能点的检索都能用 curl 复现。民国文献主力：**免费、免登录的 JSON 检索 + IIIF 图像直取**。

> **一句话用法**：`POST https://www.modernhistory.org.cn/backend-prod/esBook/findByPage`，body 里放 `keyword` + `docType`，拿 `fileCode`；再用 `findAllPage/{fileCode}` + IIIF 取页面高清图。

- 去哪找：
  - 首页（SPA）：`https://www.modernhistory.org.cn/`
  - 前端检索结果页（**只在浏览器可用**，hash 路由）：`https://www.modernhistory.org.cn/#/SearchResult_list?searchValue=抗战&selectType=`
  - **检索 API**：`POST /backend-prod/esBook/findByPage`
  - 详情元数据：`GET /backend-prod/esBook/findDetailInfo/{fileCode}`
  - **全册页码表（阅读用）**：`GET /backend-prod/esBook/findAllPage/{fileCode}`
  - IIIF 图像：`https://iiif.modernhistory.org.cn/iiif/2/<urlencode(path)>/info.json`、`.../full/512,/0/default.jpg`
  - 其余端点（类型总量、年代直方图、二次筛选、目录、清单、馆藏）见「细节」。
- 什么时候用：
  - 找 **1931–1945（及晚清民国）书/刊/报/档案/图片/音视频** 的原件影像与题录：抗战、近代中日关系、民国期刊、老报纸、革命文献；
  - 需要**篇目级**定位（结果里带 `directory` 树，篇名同样带高亮）；
  - 需要**程序化批量**做「关键词 → 文献清单 → 页码 → 高清图」流水线，且不想碰登录墙。
- 怎么搜：
  ```bash
  # 1) 主检索：抗战相关期刊，第 1 页 10 条
  curl -sS -X POST 'https://www.modernhistory.org.cn/backend-prod/esBook/findByPage' \
    -H 'Content-Type: application/json' \
    -d '{"keyword":"抗战","docType":"total","currentPage":1,"pageSize":10,
         "startDate":"","endDate":"","firstFieldName":"","firstFieldValue":"",
         "secondFieldName":"","secondFieldValue":"","secondKeyword":"",
         "orderByDownload":"","orderByGmtCreate":"","orderByPublishTime":""}' | python3 -m json.tool | head -40

  # 2) 只看报纸 + 限定年份（docType 可多值逗号分隔：ts图书 da档案 bz报纸 qk期刊 tp图片 sp视频 yp音频 ztk专题库）
  curl -sS -X POST 'https://www.modernhistory.org.cn/backend-prod/esBook/findByPage' \
    -H 'Content-Type: application/json' \
    -d '{"keyword":"抗战","docType":"qk,bz","currentPage":1,"pageSize":2,"startDate":"1937-01-01","endDate":"1945-12-31"}'

  # 3) 拿页码表 → 逐页 IIIF 图
  curl -sS 'https://www.modernhistory.org.cn/backend-prod/esBook/findAllPage/9999_qk_21450'
  #   返回 result.result[].imageUrl（iiif-json.modernhistory.org.cn/...jpg）与 content（/fileCode/目录/页.jpg）
  ```
  **结果形态**：JSON。`{"code":"200","result":{"totalSize":"13383","totalPage":"3334","dataList":[…]}}`。`dataList[]` 关键字段：`fileCode`（详情/页码表主键）、`docType`、`title`（**含 `<span style='color:#981722'>` 高亮，入库要剥标签**）、`originalTitle`、`publishTime`/`publishTimeAll`、`firstResponsible`、`directory`（篇目树，篇名同样带高亮）、`pageAmount`、`iiifObj{imgUrl,jsonUrl,uniqTag,content}`、`url`（页图相对路径）、`orgName`。
  **图像**：`findAllPage` 给的路径去掉前导 `/` 再 URL-encode，拼到 IIIF 上即可，例：`https://iiif.modernhistory.org.cn/iiif/2/9999_qk_21450%2F9999_qk_21450_0004%2F9999_qk_21450_0004_0001.jpg/full/512,/0/default.jpg`（Cantaloupe 5.0.5，`info.json` 报单页 3262×4412；CORS `*`）。**注意是图像不是文字**，要文本得自己 OCR（见 `../tools/macos-vision-ocr.md`、`../tools/mineru.md`）。
- 覆盖：
  - 平台类型统计（`GET /backend-prod/esBook/findTypeNum`，2026-10-03 实测）：**总量 185994**；图书 `ts` 173059、期刊 `qk` 11625、报纸 `bz` 1206、专题库 `ztk` 35、档案 `da` 30、图片 `tp` 24、音频 `yp` 11、视频 `sp` 4。
  - 年代：`dateAggs` 返回 1883–1973 的逐年分布（1937–1945 明显高企）；关键词「抗战」命中 13383。
  - 粒度：册/种（`fileCode`）→ 卷期（`uniqTag`）→ 页（`findAllPage`）；期刊还带篇目树。
  - 更新：动态站，`Cache-Control: max-age=14400`；有 `/esBook/findNewUpper`（最新上架）。
- 门槛：
  - **检索、题录、详情、页码表、IIIF 图像：全部匿名可用**（无 cookie/token，不限 IP，实测裸 curl 通过）。
  - **下载（整册/整篇）：必须登录**。`GET /backend-prod/downLoad/downloadQkLiterature/{fileCode}` → `401 {"message":"认证失败"}`；分类型有 `downloadBzLiterature`(GET，带 `way` 参数)、`downloadDaLiterature`(POST) 等。
  - 上游声明（北大图书馆 2018-05-30 通知）：**所有数据公开免费获取；免费注册后获得下载权限，每月下载不超过 2000 页**；浙大图书馆标注「不限IP…注册登录后可下载，免费资源」。
  - 无验证码、无 WAF 拦截（本机 curl 稳定 200），**不需要 Referer/Origin/cookie**（与 `guji.nlc.cn.md` 相反——那边**必须**带 Referer）。
- 实测：2026-10-03，macOS 27（arm64），curl 8.x，桌面 Chrome UA。① 首页 `GET /` → **200 / 6091 B**，`<title>` 为空（SPA），内联 config 暴露 `/backend-prod` 与 `iiif.modernhistory.org.cn/iiif/2`。② `findByPage`（`keyword=抗战`, `docType=total`, `pageSize=3`）→ **200 / 74 KB**，`totalSize=13383`，命中《抗战评论》(`9999_qk_21450`, 期刊)。③ `findTypeNum` → 200，总量 185994（分型见上）。④ `dateAggs` → 200，`dates[0]="1883"`、1938 年计 548。⑤ `findByPage` `docType=bz` + `keyword=申报` → 200，`totalSize=5`，返回 1938-01-15 头版页图路径。⑥ `findDetailInfo/9999_qk_21450` → 200 / 12.5 KB（题名、责任者、org_code=9999「社会来源」）。⑦ `findAllPage/9999_bz_00000203` → 200 / 160 KB，400 条页记录，含 `imageUrl`。⑧ IIIF：`.../iiif/2/<enc>/info.json` → **200**，`width=3262,height=4412`；`full/512,/0/default.jpg` → **200 image/jpeg**（header `x-powered-by: Cantaloupe/5.0.5`, `access-control-allow-origin: *`）。`.../iiif/2/<fileCode>/manifest` → 404（无 manifest 路由）；清单走 `iiif-json…/{fileCode}/{uniqTag}/{uniqTag}.json` → **200**（`"@type":"sc:Manifest"`）。⑨ `downLoad/downloadQkLiterature/9999_qk_21450` → **401 认证失败**（未登录）。⑩ 无 header 裸 curl（只带 Content-Type）同样 200 → 确认无 cookie 依赖。
- 上游：https://www.modernhistory.org.cn/ ；北大图书馆通知 https://www.lib.pku.edu.cn/portal/cn/news/0000001773

## 细节

### 端点表

| 用途 | URL / 端点 |
|---|---|
| 首页（SPA） | `https://www.modernhistory.org.cn/` |
| 前端检索结果页（**只在浏览器可用**，hash 路由） | `https://www.modernhistory.org.cn/#/SearchResult_list?searchValue=抗战&selectType=` |
| 文献详情页（浏览器） | `https://www.modernhistory.org.cn/#/DocumentDetails_qk?fileCode=<fileCode>&title=<title>`（报纸/图书把 `qk` 换成 `bz` / `ts_da`） |
| **检索 API** | `POST /backend-prod/esBook/findByPage` |
| 类型总量 | `GET /backend-prod/esBook/findTypeNum` |
| 年代直方图（聚类） | `POST /backend-prod/esBook/dateAggs` |
| 二次筛选（聚类） | `POST /backend-prod/esBook/secondChoose` |
| 详情元数据 | `GET /backend-prod/esBook/findDetailInfo/{fileCode}` |
| **全册页码表（阅读用）** | `GET /backend-prod/esBook/findAllPage/{fileCode}` |
| 目录/篇目 | `GET /backend-prod/esBook/findDirectory/{fileCode}?docType=fileCode`、`GET /backend-prod/esBook/findDirectoryByYear/{fileCode}` |
| IIIF 图像（单页任意尺寸） | `https://iiif.modernhistory.org.cn/iiif/2/<urlencode(path)>/info.json`、`.../full/512,/0/default.jpg` |
| IIIF 清单（Presentation v2） | `https://iiif-json.modernhistory.org.cn/{fileCode}/{uniqTag}/{uniqTag}.json` |
| 馆藏/公告 | `GET /backend-prod/friendlyLink/getAll` |

接口地址怎么找到的（站点改版可照做）：首页 HTML 内联 `<script>var config={url:"/backend-prod", iiifUrl:"https://iiif.modernhistory.org.cn/iiif/2"}` → `js/app.905de2d8.js` 里 grep 路由 → `/SearchResult_list` 对应 `chunk-73582064`/`chunk-529f5c38` → grep `url:"/esBook/…"`。

## 坑

1. 路由是 **hash**（`#/…`），`curl https://www.modernhistory.org.cn/search?q=…` 之类拼 URL 只会拿到 6 KB 空壳；要"在浏览器里可复现的检索 URL"就用 `#/SearchResult_list?searchValue=…`。
2. `title`/`directory.label` 里是**高亮 HTML**，入库必须剥标签，否则同一文献会因高亮分裂。
3. 日期筛选要 `startDate`/`endDate`（`YYYY-MM-DD`）；不少条目 `publishTime="--"`（无日期），筛选会漏掉它们。
4. 下载量按月限额（上游口径 2000 页/月），批量抓图请走 IIIF 而不是下载接口。
5. 图片是扫描件，无 OCR 文本层；要全文得自行 OCR。
