# psych-data —— 心理学数据、预注册与存缴入口

- 去哪找：
  - **心理科学数据中心**（中科院心理所）`https://data.psych.ac.cn/`，匿名 JSON 检索 API `https://data.psych.ac.cn/api/index/getIndexAllResourceByES`
  - **心理科学数据银行 / ScienceDB 心理学频道** `https://www.scidb.cn/psych`（CSTR 前缀 `31253.11.sciencedb.psych.*`）
  - **国民心理健康数据库** `https://mhdata.psych.ac.cn/`（API 基址 `http://mhdata.psych.ac.cn/api`）
  - **心理科学云空间** `http://yun.psych.ac.cn/`；**open-science-for-psychology** `https://os.psych.ac.cn/`
  - 国际：OSF / PsyArXiv 见 [`../repos/osf.io.md`](../repos/osf.io.md)、ICPSR 见 [`../repos/icpsr.umich.edu.md`](../repos/icpsr.umich.edu.md)；ScienceDB 检索见 [`../methods/dataset-hubs.md`](../methods/dataset-hubs.md)
  - 学会/期刊：中国心理学会 `https://www.cpsbeijing.org/`；《心理学报》数据存缴政策 `https://journal.psych.ac.cn/xlxb/CN/column/column15.shtml`
- 什么时候用：找**中国心理学的可引用数据集**（量表、行为、脑影像、心理测量，带 CSTR/DOI）、国民心理健康监测数据、心理学预注册/预印本、投稿前的**数据存缴**；关键词：心理学数据、开放科学、预注册、PsyArXiv、脑影像、心理健康数据库、数据共享。
- 怎么搜：`data.psych.ac.cn` 免登录 POST 检索（页面用 axios/XHR 打同一接口）：
  ```bash
  curl -s -X POST 'https://data.psych.ac.cn/api/index/getIndexAllResourceByES' \
    -H 'Content-Type: application/json' \
    --data-binary '{"aggregations":[],"esParameter":[{"field":"name","fieldType":"text","connector":"and","operator":"LK","value":"抑郁","type":"search"}],"highlight":[{"color":"red","highlightField":"name"},{"color":"red","highlightField":"description"}],"page":0,"pageSize":5,"sorts":[{"field":"","fieldType":"","order":""}]}'
  # → {"message":"成功","code":200,"data":{"page":0,"pageSize":5,"total":7,
  #     "sourceList":[{"cstr":"31253.11.sciencedb.psych.01155","keywords":["亚临床抑郁","注意偏向",...],
  #                    "subject":["心理学"],"description":"...","storageNum":135617,...}]}}
  ```
  辅助端点：`GET /api/index/getResourceByType?resourceType=11`（按类型列数据集，`resourceType=11` 为数据集）、`GET /api/index/getIndexSearchitems?type=search`（检索字段配置）、`GET /api/index/get/basicConfig`（站点信息）。其他库走各自接口 / 浏览器。
- 覆盖：心理科学数据中心汇聚心理所及所外心理学数据（数据集 / 文献 / 工具等，带 CSTR）；国民心理健康数据库为心理健康监测类数据；ScienceDB 心理学频道为带 DOI 的全学科+心理数据；OSF/PsyArXiv 覆盖全球预注册与预印本（含中国作者）。
- 门槛：检索 / 元数据**免登录**；`data.psych.ac.cn` **资源依申请下载**（页面资源「可依申请下载」）；ScienceDB 检索免登录；OSF / PsyArXiv 免费；ICPSR 需机构订阅或注册。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA + 无头 Chromium 抓包：`https://data.psych.ac.cn/` → 200（16 468 B，Vue SPA，raw HTML 无标题，浏览器标题「心理科学数据中心」）；XHR 确认打 `/api/index/getIndexAllResourceByES` 等；匿名 curl POST `value=抑郁` → 200，`data.total=7`、`sourceList[]` 含 `cstr`/`keywords`/`subject`；`getResourceByType?resourceType=11` → 200（60 414 B）；`getIndexSearchitems?type=search` → 200（1 144 B）；`get/basicConfig` → 200。`https://www.scidb.cn/psych` → 200（778 294 B，跳 `www.scidb.cn/psych`）；`https://mhdata.psych.ac.cn/` → 200（3 406 B，JS 里 `baseURL="http://mhdata.psych.ac.cn/api"`）；`http://yun.psych.ac.cn/` → 200（标题 `DataSpace`）；`https://os.psych.ac.cn/` → 200（5 597 B，标题 `open-science-for-psychology`）；`https://api.osf.io/v2/preprints/?filter[provider]=psyarxiv` → 200（9 667 B，JSON:API）；`https://journal.psych.ac.cn/xlxb/CN/column/column15.shtml` → 200（数据存缴政策）。
- 上游：中国科学院心理研究所科学数据中心（心理所网信/科学数据中心）；ScienceDB（中科院）；OSF（COS）；ICPSR（密歇根大学）。

## 细节

### 心理所科学数据服务系列平台（2023-02 上线，见 `https://psych.cas.cn/news/zhxw/202302/t20230201_6670178.html`）

| 平台 | 地址 | 用途 / 开放范围 |
|---|---|---|
| 心理科学数据中心 | `data.psych.ac.cn` | 数据发布与展示，**依申请下载**，所内外可用 |
| 心理科学云空间 | `yun.psych.ac.cn` | 数据存储与管理、上传/下载/分享，所内外可用 |
| 心理所网盘 | — | 日常存储，**仅单位网络** |
| 心理所存档库 | — | 科研原始数据归档，**仅单位网络** |
| 心理科学数据银行（早期） | `scidb.cn/psych` | ScienceDB 心理学频道，带 DOI/CSTR |

### 可用的匿名 JSON 接口（`data.psych.ac.cn`）

| 方法 | 端点 | 说明 |
|---|---|---|
| GET | `/api/index/get/home` | 首页聚合 |
| GET | `/api/index/get/basicConfig` | 站点配置（名称、备案、版权） |
| GET | `/api/index/getIndexSearchitems?type=search` | 检索字段定义（field/fieldType/operator） |
| GET | `/api/index/getResourceByType?resourceType=<n>` | 按资源类型列条目（11=数据集） |
| POST | `/api/index/getIndexAllResourceByES` | 全文检索/列表；body 含 `esParameter[]{field,operator,value}`、`page`、`pageSize` |

### 其他

- 《心理学报》《心理科学进展》均设**论文关联数据存缴共享政策**（支撑结论的数据必须共享），推荐存缴即为上述数据中心 / ScienceDB。
- ICPSR 心理学经典数据（如 ANES 相关）走 ICPSR，见 `../repos/icpsr.umich.edu.md`；跨国预注册走 OSF，见 `../repos/osf.io.md`。

## 坑

- `data.psych.ac.cn` 是 Vue SPA，**raw HTML 无标题、无内容**——不要按普通 HTML 抓；检索要么用上面 POST 接口，要么浏览器渲染。
- 接口返回外层是 `{code,message,data}`，检索结果的条目在 `data.sourceList`（**不是**扁平数组，也非 `total` 同级）；`total` 在 `data.total`。
- `getIndexAllResourceByES` 传错 body（如 `{}`、`{"page":1}`）会返回 `data:null`；必须带上 `esParameter` 才会命中。
- `mhdata.psych.ac.cn` 的 API 基址是 **http**（`http://mhdata.psych.ac.cn/api`），https 下部分路径不稳；`os.psych.ac.cn` 首次请求偶发超时，重试可达。
- 网盘 / 存档库**只在心理所内网**开放，公网别指望；国民心理健康数据库与数据中心是两个不同系统，别混用。
