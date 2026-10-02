# zhongguoyuyan.cn —— 方言与民族语言采录数据

- 去哪找：**中国语言资源保护工程采录展示平台**（语保平台）`https://www.zhongguoyuyan.cn/`；匿名 JSON 接口在 `/api/mongo/query/*`；检索记录接口 `/api/mongo/get/searchRecord`。
- 什么时候用：要**汉语方言/少数民族语言调查点**的空间分布与统计（调查点数、发音人数、覆盖省份）；要语言点编号（如 `35N14`）、方言文化条目编号（`OCM…`/`OCD…`）；做语言地理、方言普查相关脚本取数。
- 怎么搜：站点为 umi/React SPA（`/index`、`/province/<码>/<名>`、`/point/<码>`），页面直抓无数据，须打 XHR。**两个接口匿名可用（GET/POST JSON）**：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  # ① 工程总量统计（免参）
  curl -sS -A "$UA" -X POST -H 'Content-Type: application/json' -d '{}' \
    'https://www.zhongguoyuyan.cn/api/mongo/query/latestSurveyMongo'
  # ② 调查点坐标与行政区（免参，全量）
  curl -sS -A "$UA" -X POST -H 'Content-Type: application/json' -d '{}' \
    'https://www.zhongguoyuyan.cn/api/mongo/query/indexLocations'
  ```
  结果形态：**JSON**。其余页面/语料（`/api/mongo/search/province?pc=21`、媒体 `/api/mongo/media/*`、`/api/user/current`）**须注册登录**，匿名返 `{"code":401,"status":"FAIL","description":"Unauthorized"}`。
- 覆盖：`latestSurveyMongo` 自报 `provinceCount:34`、`surveyCount:1329`、`dialectSounders:8581`、`minorityCount:8`、`minoritySurveyCount:429`、`minoritySounders:1091`、`culturalProvinceCount:32`、`culturalSurveyCount:102`、`culturalSounders:407`（汉语方言点 1329、少数民族语言点 429、方言文化点 102）；`indexLocations` 给逐点经纬度与省/市/县/村（如 `_id:"01004"` 广西百色田东平马街）。更新随工程采录入库。
- 门槛：**匿名仅统计与点位**；具体语料/音视频/词表需**注册登录（401）**。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA、Chromium 无头——`POST /api/mongo/query/latestSurveyMongo` `{}` → **200 JSON**，返回上述计数字段与 `dialectObj[]` 分省清单；`POST /api/mongo/query/indexLocations` `{}` → **200 JSON** 数组，首条 `location._id:"01004"`、`province:"广西壮族自治区"`、`point.longitude/latitude`；`GET /api/mongo/search/province?pc=21` → 200 `{"code":401,…}`；浏览器打开 `/province/21/安徽` 落权限页「本页仅对注册用户开放」。
- 上游：中国语言资源保护工程（教育部/国家语委主管）；`https://www.zhongguoyuyan.cn/`。

## 细节

### 已探明端点

| 端点 | 方法 | 匿名 | 说明 |
|---|---|---|---|
| `/api/mongo/query/latestSurveyMongo` | POST `{}` | ✅ | 工程总量统计 + 分省 `dialectObj[]` |
| `/api/mongo/query/indexLocations` | POST `{}` | ✅ | 调查点经纬度 + 行政区 + `filepath` |
| `/api/mongo/get/searchRecord` | GET | ✅ | 站内搜索历史/热搜记录 |
| `/api/mongo/search/province?pc=21` | GET | ❌ 401 | 省级语言点清单（需登录） |
| `/api/mongo/media/imageConvertion/small?tag=&token=&id=` | GET | ❌ | 图片缩略（带 token） |
| `/api/common/media/dialectCulture/small?id=OCM…&serial=1` | GET | ❌ | 方言文化媒体 |

- 页面路由：`/province/<省码>/<省名>`（如 `/province/21/安徽`）、`/point/<点码>`（如 `/point/35N14` 尤溪街面话）、`/draw/custom`、`/standard`。
- 界面为 React SPA（`umi.<hash>.js`），路由路径≠接口路径，直接抓 HTML 拿不到数据。

## 坑

1. **多数内容要登录**：省/点详情、语料、音视频一律 401；能匿名取的只有总量统计与点位坐标。
2. 接口是 **POST 才生效**（`-X POST -H 'Content-Type: application/json' -d '{}'`），当 GET 用会失败。
3. 首页 HTML 仅 1.5 KB（SPA 壳），任何「抓首页找数据」的思路都不通。
4. 点位 `filepath` 暴露内部文件路径（`…/0001调查点概况.xls`），仅作线索，勿据此构造下载地址。
5. 语言种类/使用人口等结论请以工程公报与《中国语言资源集》为准，平台计数随采录进度变动。
