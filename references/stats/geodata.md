# geodata —— 标准地图与地球科学数据

- 去哪找：**标准地图** `http://bzdt.ch.mnr.gov.cn/`（JSON 检索接口见「细节」）；**天地图** 门户 `https://www.tianditu.gov.cn/`、API 文档 `http://lbs.tianditu.gov.cn/`；**全国地理信息资源目录** `https://www.webmap.cn/`；**国家地球系统科学数据中心** `https://www.geodata.cn/`；**中国气象数据网** `https://data.cma.cn/`；**国家地震科学数据中心** `https://data.earthquake.cn/`、地震目录 `https://www.ceic.ac.cn/`；**国家海洋科学数据中心** `https://mds.nmdis.org.cn/`；**国家青藏高原科学数据中心** `https://data.tpdc.ac.cn/`。
- 什么时候用：要带**审图号**的标准地图（中国全图/分省/世界/G20）、行政区划底图、瓦片地图与 POI/地理编码检索；要 DEM、土地利用/覆被、气象观测、地震目录、海洋实测、地质资料等**科研空间数据**；要可引用（DOI）的数据集。
- 怎么搜：**能直接 curl 的只有少数**——
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 标准地图检索（JSON，无需登录/无需 key）
  curl -s -A "$UA" 'http://bzdt.ch.mnr.gov.cn/sbsm/supermap/searchPicture.do?seachText=中国&pageNum=1&orderSearch='
  # ② 青藏高原数据中心检索（JSON，POST）
  curl -s -A "$UA" -X POST -H 'Content-Type: application/json' -d '{"page":1,"size":2}' \
       'https://data.tpdc.ac.cn/view/metadataView/list'
  # ③ 天地图检索（需 tk=申请到的 key，参数非法会回 JSON 错误码）
  curl -s 'http://api.tianditu.gov.cn/v2/search?postStr=%7B%22keyWord%22%3A%22北京%22%7D&type=query&tk=<KEY>'
  ```
  其余门户（geodata、cma、ceic、nmdis、resdc）是 SPA 或表单检索，**结果形态为 HTML/需浏览器**，走页面检索框或「数据资源」导航；分平台入口与字段清单见「细节」。
- 覆盖：标准地图 2000+ 幅（JSON 实测 `totalNum=2048`，字段含审图号与年份）；地球系统科学/青藏高原/海洋/地震/地质为**分平台联盟**，各自按学科与年份收数，粒度从全国栅格到单站时序列不等；气象数据需按数据集申请。
- 门槛：标准地图 **免费无 key**（可直接下载 jpg/eps）；天地图 **需 key**（注册申请）；geodata/earthquake/nmdis/tpdc/agridata/forestdata **需注册**（上游页面自述多为实名，下载数据前登录）；cma **需注册**、部分数据走 API 需 token；resdc/webmap **WAF 拦截**（见「坑」）。
- 实测：2026-10-03，macOS（arm64），curl 8.x，桌面 UA：
  - 标准地图 `searchPicture.do?seachText=&pageNum=1` → 200 JSON，`totalNum=2048`、`pageSize=12`、`pageNum=171`，字段含 `id/name/scale/mapNumber(审图号)/mapYear/jpgPath`；
  - TPDC `POST /view/metadataView/list`（`{"page":1,"size":2}`）→ 200 JSON `{"code":"200",…,"context":{"latestSortList":[…]}}`；同路径 GET → 405 JSON；
  - 天地图 `api.tianditu.gov.cn/v2/search?...&tk=test` → 400 `{"code":308011,"message":"请求参数非法长度或不合规"}`（证明端点存在且校验 tk）；
  - `www.geodata.cn/` → 200（标题「国家地球系统科学数据中心首页」）；`data.cma.cn/` → 200（SPA）；`data.earthquake.cn/` → 200；`mds.nmdis.org.cn/` → 200；`data.tpdc.ac.cn/` → 200；`www.ngac.cn/` → 200；`www.agridata.cn/` → 200；`www.forestdata.cn/` → 200；`lbs.tianditu.gov.cn/` → 200（标题「天地图API」）；
  - `www.webmap.cn/` → **502**（华为云 WAF）；`www.resdc.cn/` → 200 但正文为 `WebShieldSessionVerify` 跳转（安全狗）；`www.ceic.ac.cn/ajax/google` → 404（旧 JSONP 接口已下线）；`console.tianditu.gov.cn` 本机 **NXDOMAIN**。
- 上游：自然资源部标准地图服务 `http://bzdt.ch.mnr.gov.cn/`；天地图 `https://www.tianditu.gov.cn/`；各数据中心首页见上。

## 细节

### 一、全国/区域数据中心速查

| 平台 | 入口 | 检索方式 | 门槛 | 实测 |
|---|---|---|---|---|
| 标准地图服务（自然资源部） | `http://bzdt.ch.mnr.gov.cn/` | JSON 接口 `searchPicture.do` / `getMapCategorys.do` | 免费无 key | ✅ 200，2048 幅 |
| 天地图 | `https://www.tianditu.gov.cn/`（文档 `http://lbs.tianditu.gov.cn/`） | REST 服务，`tk=<key>` | 需 key | ✅ 门户/文档 200；API 无 key 报 308011 |
| 全国地理信息资源目录 | `https://www.webmap.cn/` | 页面检索（1:100 万地形/测绘成果目录） | 免费（部分需注册） | ⚠️ 502（WAF） |
| 国家地球系统科学数据中心 | `https://www.geodata.cn/data/`（帮助 `/help/dataRetrieval.html`） | 关键词/分类/筛选，Kendo 网格；数据接口 `service/scidata/entry/manage` | 注册（下载） | ✅ 200；裸接口 400 |
| 中国气象数据网 | `https://data.cma.cn/` | 数据集目录 + 检索；JS 内出现 `/api/user/login`、`dataService/getDataCategory` 等端点（**未本机实测**） | 注册 | ✅ 200（SPA，直接请求 API 路径回落首页） |
| 国家地震科学数据中心 | `https://data.earthquake.cn/` | 按科学数据/产出单位分类，资源手册 | 注册 | ✅ 200 |
| 中国地震台网（地震目录） | `https://www.ceic.ac.cn/` | 新版 SPA「地震目录」 | 免费 | ✅ 200；旧 `/ajax/google` 404 |
| 国家海洋科学数据中心 | `https://mds.nmdis.org.cn/` | 站内 `pages/totalSearch.html?query=<词>` | 注册 | ✅ 200 |
| 国家青藏高原科学数据中心 | `https://data.tpdc.ac.cn/` | `POST /view/metadataView/list` | 注册（下载） | ✅ 200 JSON |
| 国家农业科学数据中心 | `https://www.agridata.cn/` | 页面检索 | 注册 | ✅ 200 |
| 国家林业和草原科学数据中心 | `http://www.forestdata.cn/` | 页面检索（Vue SPA） | 注册 | ✅ 200 |
| 全国地质资料馆 | `https://www.ngac.cn/` | 地质资料目录检索 | 免费（部分登录） | ✅ 200 |
| 资源环境科学数据中心（中科院） | `https://www.resdc.cn/` | 页面检索（GB2312） | 注册 | ⚠️ WAF（WebShieldSessionVerify） |

### 二、标准地图 JSON 接口（唯一可直接批量的）

```bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
# 检索：seachText=关键词(可空)，pageNum 从 1 起，pageSize 固定 12，orderSearch 可空
curl -s -A "$UA" 'http://bzdt.ch.mnr.gov.cn/sbsm/supermap/searchPicture.do?seachText=中国&pageNum=1&orderSearch='
# 分类：superclass（中国全图/世界地图/G20国家/长江经济带区域/审图号…）
curl -s -A "$UA" 'http://bzdt.ch.mnr.gov.cn/sbsm/supermap/getMapCategorys.do?seachText=&scale=&size=&superclass='
```

返回字段（`message.result[]`）：`id 名称 比例尺 开本 content 分类(superclass/subclass/smallclass) 审图号(mapNumber) 年份(mapYear) 缩略图(jpgPath，华为云 OBS) 浏览/下载量`。
页面入口：`download.html?superclassName=中国全图`（分类列表，内容由 `view/download/*.html` 片段 + 上述接口渲染）。

### 三、天地图 key 与常用服务

- 申请：门户 `https://www.tianditu.gov.cn/` → 注册/登录（`https://passport.tianditu.gov.cn/register`）→ 控制台取 key（页面内链 `https://console.tianditu.gov.cn/api/key`；本机解析 NXDOMAIN，需浏览器访问）。
- 文档：`http://lbs.tianditu.gov.cn/`（二次开发/服务列表，200）。
- 常用端点：地理编码/逆编码 `.../geocoder`、POI 检索 `http://api.tianditu.gov.cn/v2/search`、行政区划 `.../server/administrative2.html`、静态图 `.../staticapi/`；均带 `tk=<key>`。
- 底图瓦片：门户内链出现 `https://t4.tianditu.gov.cn/`（矢量/影像，`tk` 必填）——**上游声明，未本机实测**。

### 四、青藏高原科学数据中心（TPDC）检索接口

```bash
curl -s -X POST -H 'Content-Type: application/json' -d '{"page":1,"size":20}' \
  'https://data.tpdc.ac.cn/view/metadataView/list'
```
返回 `{"code":"200","context":{"latestSortList":[…title/description…]}}`；GET 同路径返回 **405 Method Not Allowed**（JSON），可作端点判活。前端配置 `https://data.tpdc.ac.cn/config.js` 给出分区 base：`/view`(数据) `/my`(个人) `/geoserver`(地图) `/file`(附件)。

## 坑

1. **`www.webmap.cn` 挂在华为云 WAF 后**，本机多次 502（`vip1.huaweicloudwaf.com`）——目录检索请改用浏览器或稍后重试。
2. **`www.resdc.cn`（资源环境数据中心）** 返回 `WebShieldSessionVerify` 跳转（安全狗），curl 拿不到内容；且为 **GB2312** 编码。
3. **中国气象数据网 `data.cma.cn` 是 Vue SPA**：直接请求 API 路径会回落成 index.html；检索/下载须登录并走页面。旧式免登录抓取不成立。
4. **中国地震台网改版**：`www.ceic.ac.cn` 现为 React SPA，「地震目录」需浏览器；旧的 `http://www.ceic.ac.cn/ajax/google`（JSONP）已 404，`news.ceic.ac.cn` 本机连接失败（000）。
5. **标准地图 JSON 接口无频控提示**，但 `pageSize` 固定 12、翻页成本高；批量请按 `superclass` 分类拉取并 ≥1.5s 间隔。下载页有 `updataBrowseNum.do`/`updataBownloadNum.do` 计数接口，**不要调用**（会污染站点统计）。
6. **多数科研数据中心（geodata/earthquake/nmdis/tpdc/agridata/forestdata）下载需实名注册**，且部分数据仅限「离线申请」；检索目录通常匿名可见，**取数前先确认许可与引用要求**。
7. `data.earthquake.cn` 的下载/服务链路（产品定制、速报订阅）多为表单流程，无公开 REST；引用地震目录前请核对该台网最终测定结果（速报值会修订）。
8. 天地图 key 按域名/IP 绑定并限配额，**勿在共享脚本里硬编码他人 key**；服务返回错误码以 `308xxx` 提示参数/key 问题。
