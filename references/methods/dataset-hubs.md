# dataset-hubs —— 免费数据集市的 JSON 检索接口

- 去哪找：天池 `https://tianchi.aliyun.com/dataset`；和鲸 `https://www.heywhale.com/home/dataset`；ScienceDB `https://www.scidb.cn/`；ModelScope `https://modelscope.cn/datasets`；HF-Mirror `https://hf-mirror.com/datasets`。五站检索端点见「细节」速查表。
- 什么时候用：解决「**有没有人已经把这份数据整理成数据集**」（CSV/JSON/图片/语料都算）；找中文产业 / NLP 竞赛数据集、中文统计整编表格、带 DOI 的科研数据、HF 生态中文数据集；与 `../stats/` 的官方统计口径互补。
- 怎么搜：五站都提供**免登录的 JSON 列表 / 检索接口**（不是只能点页面）——天池 `POST /api/notebook/getDatasetList`、和鲸 `GET /api/datasets?Title=`、ScienceDB `POST /api/sdb-query-service/query?q=`、ModelScope `GET /api/v1/dolphin/datasets?Query=`、HF-Mirror `GET /api/datasets?search=`。**批量找数据集走接口，别做页面抓取**；参数与返回字段见「细节」。
- 覆盖：5 个数据集市（天池 / 和鲸 / ScienceDB / ModelScope / HF-Mirror）；条目含竞赛、社区上传、科研数据与 HF 生态数据集。
- 门槛：检索 / 浏览多免登录；**下载需登录**（天池阿里云账号、和鲸社区登录、ModelScope 登录 + AccessToken、HF `gated` 库需 token）；许可须逐条核（尤其二次分发的许可）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，同主机间隔 ≥1.5 s）；各站逐条观测见「细节」。
- 上游：天池、和鲸、ScienceDB、ModelScope、HF-Mirror（入口见上）。

> 数据本体质量与 license 必须逐条核（尤其二次分发的许可）；不确定就只当线索，正式引用换官方源。

## 细节

### 速查表

| 站 | 检索接口 | 匿名 | 关键词参数 | 结果形态 |
|---|---|---|---|---|
| 天池 tianchi.aliyun.com | `POST /api/notebook/getDatasetList` | ✅ 需先取 csrf cookie | `keywords` | JSON，`data.list[].datalab` |
| 和鲸 heywhale.com | `GET /api/datasets` | ✅ | `Title` | JSON，`data[]`/`totalNum` |
| ScienceDB scidb.cn | `POST /api/sdb-query-service/query?q=` | ✅ | `q`（查询串） | JSON，`data.data[]`/`data.total` |
| ModelScope modelscope.cn | `GET /api/v1/dolphin/datasets` | ✅ | `Query` | JSON，`Data[]`/`TotalCount` |
| HF-Mirror hf-mirror.com | `GET /api/datasets` | ✅ | `search` | JSON 数组（HF Hub 同构） |

### 1. 天池数据集（tianchi.aliyun.com/dataset）—— 阿里系数据分享平台

- 去哪找：`https://tianchi.aliyun.com/dataset`；详情页 `https://tianchi.aliyun.com/dataset/{datalab.id}`（实测 `…/dataset/213581` → 200，title「2019餐饮数据集_数据集-阿里云天池」；`…/dataset/dataDetail?dataId=213581` 会 **302** 到前者）。
- 什么时候用：找**中文产业/中文 NLP 竞赛数据集**（CBLUE 医疗语料、行业指令数据、A股财报、城市 POI、气象…），或找带 baseline 的可复现数据集。
- 怎么搜（**curl 全流程，实测可复现**）：
  ```bash
  # 1) 先拿匿名 cookie（含 x-csrf-token）
  curl -s -c /tmp/tc.jar -o /dev/null -A "$UA" 'https://tianchi.aliyun.com/dataset'
  TOK=$(awk '/x-csrf-token/{print $7}' /tmp/tc.jar)
  # 2) POST 列表/检索；csrf-token 头必须回传
  curl -s -b /tmp/tc.jar -A "$UA" -X POST \
    -H 'Content-Type: application/json' -H "csrf-token: $TOK" \
    -H 'Referer: https://tianchi.aliyun.com/dataset' \
    --data-binary '{"my":false,"official":false,"sortby":"top","industryId":"","fieldId":"","source":"","pageSize":10,"pageNum":1,"keywords":"GDP"}' \
    'https://tianchi.aliyun.com/api/notebook/getDatasetList'
  ```
  - 响应：`{"code":"SUCCESS","data":{"total":39,"list":[{"datalab":{id,title,description,gmtCreate,uploaYear,area,attributeType,…},"datalabDownloadCount":…,"fieldTags":[…],"industryTags":[…],"detail":{…},"notebook":…}],"pageNum":1,"pageSize":10,"pages":…}}`
  - 分页 `pageNum`/`pageSize`；排序 `sortby`（实测值 `top`）；标签过滤 `industryId` / `fieldId` / `source`；`my`/`official` 是"我的/官方"开关（`false,false` = 全部）。
  - **筛选项树**：`GET https://tianchi.aliyun.com/v2/notebook/dataListSelection` → `{code:"SUCCESS",data:{fieldTags:[{tagId,tagName,tagNameCn,tagType:"DATALAB_FIELD"}],industryTags:[…]}}`，用返回的 `tagId` 回填 `industryId`/`fieldId`。
- 覆盖：行业（商业/互联网/金融/医疗/政务文化/计算机/工程交通/安全/自然科学/农业/电商/教育/生物基因/环境…）× 技术（CV/NLP/多模态/语音/推荐/图/回归/可靠性…）；含竞赛数据集与用户上传；页脚分页实测 **446 页**（约 4k+ 条，"All" 视图）。
- 门槛：检索/浏览免登录；**下载要登录阿里云账号**，部分数据集需申请或同意协议（页内 `dataset.dataDetail.ApplyDataset`）——本机未登录实测下载流程。
- 实测：2026-10-03，curl 8.x（`keywords=GDP` → `total 39`，首条「A股上市公司季度营收预测数据集」；`keywords=年鉴` → `total 1`）；无 csrf-token 头时 → **403 `code: EBADCSRFTOKEN`**；`GET /api/dataset/*` 一律回落 SPA HTML（该站无 GET 列表接口）。
- 上游：`https://tianchi.aliyun.com/dataset`（接口名与 body 由无头 Chromium 抓包还原 + curl 复现）。

### 2. 和鲸社区（heywhale.com）—— 国内数据科学社区数据集

- 去哪找：`https://www.heywhale.com/home/dataset`；详情页走 `data[]._id`（形如 `646fffd1df77d23a6dc9fa0f`）。
- 什么时候用：找**中文统计整编数据**（如「中国主要城市经济统计数据 2012-2021」）、比赛/教学数据集、带 notebook 的复现包。中文社会经济类数据集比天池更"表格化"。
- 怎么搜（匿名，实测可直接 curl）：
  ```bash
  curl -s 'https://www.heywhale.com/api/datasets?page=1&perPage=20&Visible=true&sort=-SortWeight&Title=%E7%BB%8F%E6%B5%8E' \
    -H 'Accept: application/json' -H 'Referer: https://www.heywhale.com/home/dataset'
  # → {"totalNum":48,"page":1,"perPage":20,"data":[{_id,Title,ShortDescription,Tags,Creator,
  #    DownloadCount,ViewsCount,License,Files,Official,Private,EnableDownload,Visible,Zones}]}
  ```
  - 参数（bundle 内实测读到）：`page`、`perPage`、`Visible=true`、`sort`（首页用 `-SortWeight`）、`Title=<关键词>`；筛选还有 `usageRange`、`ZoneSections`、`StickyInZones`、`noIds`。
  - 联想词：`GET /api/associativeWords?Word=<kw>&perPage=6`；标签树 `GET /api/metaTags?type=tree&MetaData=<id>`；许可字典 `GET /api/datasetLicenses?perPage=10000`。
- 覆盖：社区上传为主（社会经济、气象、图像、文本、金融…），条目带 `License`、`Files`（文件清单）、`DownloadCount`，可据此判可用性。
- 门槛：检索免登录；**下载多数需登录**（`EnableDownload`/`Private` 字段可先判）；部分数据集限社区等级。
- 实测：2026-10-03，curl 匿名 `Title=经济` → **200**，`totalNum=48`，首两条「中国主要城市经济统计数据 2012-2021」「中国主要城市经济统计分析」；无 `Title` 时返回默认列表（首页请求为 `/api/datasets?page=1&Visible=true&needMeta=true&sort=-SortWeight`）。
- 上游：`https://www.heywhale.com/home/dataset`（前端 bundle `static.heywhale.com/bundle/home/static/index-*.js` 内查询参数 + curl 复现）。

### 3. ScienceDB 科学数据银行（scidb.cn，中科院）—— 带 DOI 的科研数据仓储

- 去哪找：`https://www.scidb.cn/`；检索页 `https://www.scidb.cn/list?searchList={URL编码关键词}`（中文，实测 200）/ 英文 `https://www.scidb.cn/en/list?searchList=…&ordernum=`。
- 什么时候用：要**可引用的 DOI 数据**（论文配套数据、面板/遥感/生物/材料数据集），或要 `pid`/`doi` 做正式引用；也是找"中国学者上传的原始数据"的首选。
- 怎么搜（匿名，实测可直接 curl）：
  ```bash
  curl -s -X POST 'https://www.scidb.cn/api/sdb-query-service/query?queryCode=&q=%E4%BA%BA%E5%8F%A3' \
    -H 'Content-Type: application/json' -H 'Referer: https://www.scidb.cn/list' -H 'Origin: https://www.scidb.cn' \
    --data-binary '{"fileType":[],"dataSetStatus":[],"copyrightCode":[],"publishDate":[],"ordernum":"6","rorId":[],"ror":"","taxonomyEn":[],"journalNameEn":[],"page":1,"size":10}'
  # → {"code":20000,"message":"成功","data":{"total":357,"fileTypeList":[{count,name}...],"data":[
  #     {pid,doi,titleZh,titleEn,taxonomy:[{code,nameZh}],download,size,dataSetType,dataSetPublishDate,author,categoryLabels,...}]}}
  ```
  - 关键词走查询串 `q=`（URL 编码），筛选走 JSON body（`fileType`/`dataSetStatus`/`copyrightCode`/`publishDate`/`rorId`/`taxonomyEn`/`journalNameEn`）；分页 `page`/`size`；`ordernum` 是排序（页面 URL 里同名参数，值 `6` 为默认）。
  - 其他公开接口：`GET /api/sdb-query-service/latest`、`GET /api/sdb-statistics-service/totalStatistics`、`GET /api/gin-sdb-news/public/newlist`。
- 覆盖：全学科科研数据（`taxonomy` 学科码 + 中英名），条目含 `pid`（如 `21.86116.6/sciencedb.06893`）、`doiStatus`、`download` 计数、`size`、`language`（`zh_CN`/…）。
- 门槛：检索/元数据**免登录**（实测）；下载本机未实测（按仓储通例多为免登录直下，gated 数据集除外）——**未验证**。
- 实测：2026-10-03，curl 匿名 `q=人口` → **200**，15,496 B，`code=20000`、`data.total=357`；无头 Chromium 抓包确认页面检索即打该接口（`POST /api/sdb-query-service/query?queryCode=&q=人口`，body 同上）。
- 上游：`https://www.scidb.cn/`（中科院科学数据银行）。

### 4. ModelScope 数据集广场（modelscope.cn/datasets）—— 魔搭

- 去哪找：列表 `https://modelscope.cn/datasets`；带词页面 `https://modelscope.cn/datasets?page=1&query={关键词}`。
- 什么时候用：找 **AI 训练/评测数据集**（含中文语料、指令数据、评测集）；要"中文 NLP 数据集"时它是天池之外的第二个大池子。**不是统计数据源**（宏观数值请回 `../stats/`）。
- 怎么搜（匿名，实测可直接 curl）：
  ```bash
  curl -s 'https://modelscope.cn/api/v1/dolphin/datasets?PageSize=30&PageNumber=1&Target=&Query=%E7%BB%8F%E6%B5%8E' \
    -H 'Accept: application/json' -H 'Referer: https://modelscope.cn/datasets'
  # → {"Code":200,"TotalCount":22,"Data":[{Id,Namespace,Name,ChineseName,License,Downloads,Likes,
  #     UserDefineTags,Visibility,Type,Description,...}]}
  ```
  - 参数：`PageSize`、`PageNumber`、`Target`（分组/过滤，空=全部）、**`Query`=关键词**（`Name` 参数会被忽略——实测传 `Name=` 结果不变）。
  - 其他：`GET /api/v1/dolphin/dataset/query`（推荐位）、`GET /api/v2/tags?depth=4`（标签树）。
- 覆盖：43,275 条数据集（实测 `TotalCount`，默认列表）；ML/AI 为主，`ChineseName` 字段对中文检索友好。
- 门槛：检索免登录；**下载需登录 + AccessToken**（模型/数据集下载共用 SDK 凭证）。
- 实测：2026-10-03，curl 匿名 `Query=经济` → **200**，`TotalCount=22`，首条 `mingyue0915/InternationalEconomicNews`（"中国经济网"国际经济新闻，Apache-2.0）；无头 Chromium 抓包确认搜索交互即 `GET /api/v1/dolphin/datasets?…&Query=经济`。
- 上游：`https://modelscope.cn/datasets`。

### 5. HF-Mirror（hf-mirror.com）—— Hugging Face 的国内镜像

- 去哪找：`https://hf-mirror.com/`（镜像门户）；数据集页 `https://hf-mirror.com/datasets`；仓库页 `https://hf-mirror.com/datasets/{author}/{name}`。
- 什么时候用：**HF 上的中文数据集下载不下来时**的中转；也用来搜 HF 生态里的中文/多语数据集（规模远大于国内平台）。CLI：`HF_ENDPOINT=https://hf-mirror.com huggingface-cli download <repo>`。
- 怎么搜：
  ```bash
  curl -s 'https://hf-mirror.com/api/datasets?search=chinese&limit=3'
  # → [{"_id","id":"DataoceanAI/Chinese_Male_Speech_...","author","likes","downloads","lastModified","gated","sha",...}]
  ```
  - **API 与 HF Hub 同构**：`/api/datasets?search=&author=&sort=downloads&direction=-1&limit=&full=true`；单库信息 `/api/datasets/{repo}`；文件树 `/api/datasets/{repo}/tree/main`。模型同理 `/api/models`。
  - 文件直链 `https://hf-mirror.com/datasets/{repo}/resolve/main/{path}`。
- 覆盖：Hugging Face Hub 的数据集/模型镜像（含 gated 元数据）；镜像只做加速，**筛选能力 = HF Hub**。
- 门槛：公开库免登录；`gated` 库仍需 HF token（镜像转发不了权限）。
- 实测：2026-10-03，`GET https://hf-mirror.com/` → **200**，14,062 B，`<title>HF-Mirror</title>`；`GET /api/datasets?search=chinese&limit=3` → **200**，返回 3 条（首条 `DataoceanAI/Chinese_Male_Speech_Synthesis_Corpus_Live_Streaming_for_Sales`，likes 6）。
- 上游：`https://hf-mirror.com/`（公益镜像，自述"加速访问 Hugging Face 的门户"）。

### 探测记录（2026-10-03，macOS arm64，curl 8.x，桌面 UA，同主机间隔 ≥1.5s）

| host | 状态码 | 观察 |
|---|---|---|
| tianchi.aliyun.com | 200 / 200 / 403 | 首页与详情页 200；无 csrf 的 POST → 403 EBADCSRFTOKEN；带 csrf 后列表接口 200 |
| www.heywhale.com | 200 | `/api/datasets?Title=经济` 直出 JSON（48 条） |
| www.scidb.cn | 200 | 首页 852 KB SSR；`/api/sdb-query-service/query` 匿名 200（357 条） |
| modelscope.cn | 200 | `Query=经济` → 22 条；`Name=` 不生效 |
| hf-mirror.com | 200 | HF Hub 同构 API 可用 |

### 用法建议

1. **先算量再决定口径**：用 `total`/`TotalCount`/`totalNum` 判"这个话题有没有现成数据集"，别一上来就下载。
2. **看许可**：和鲸看 `License`、天池看 `datalabLicense`、ModelScope 看 `License`、HF 看仓库 README 的 license 字段；ScienceDB 看 `copyRight`。**不确定就只当线索，正式引用换官方源**（`../stats/README.md` 的选型）。
3. **交叉检索**：同一主题在天池（产业/竞赛）+ 和鲸（表格整编）+ ModelScope（NLP 语料）+ HF（大规模语料）+ ScienceDB（带 DOI 的科研数据）各搜一遍，五个池子的重叠很小。
4. **不要爬页面**：五个站都有上述 JSON 接口；页面是 SPA/SSR，抓 HTML 既慢又易漏。
