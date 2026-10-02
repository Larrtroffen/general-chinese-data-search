# 农产品价格 —— 批发市场价与 200 指数接口

- 去哪找：**中国农业农村信息网（农业农村部信息中心）数据频道** `https://www.agri.cn/sj/`（价格指数总入口）；**全国农产品批发市场价格信息系统**（公众查询端）`https://pfsc.agri.cn/`；报送端 `https://jgsb.agri.cn/`；批发价格 200 指数说明见农业农村部数据门户 `https://data.moa.gov.cn/`。
- 什么时候用：要**农产品批发价格 200 指数**（日度/旬度）及粮油、菜篮子、畜产、水产、蔬菜、水果分项；要**批发市场名录与品种目录**；要价格走势/分析报告；做农产品价格监测、CPI 食品项、农业行情脚本。
- 怎么搜：全是 **GET/POST JSON 接口**，无 key、免登录（少数为 POST-only，GET 返 405）。可直接 curl：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
  # ① 批发价格 200 指数（日度，含农产品/粮油/菜篮子三条）
  curl -s -A "$UA" -X POST -H 'Content-Type: application/json' -d '{}' \
    'https://pfsc.agri.cn/price_portal/pi-info-day/getPortalPiInfoDay'
  # ② 批发市场名录（分页，totalCount≈301）
  curl -s -A "$UA" -X POST -H 'Content-Type: application/json' -d '{"pageNum":1,"pageSize":3}' \
    'https://pfsc.agri.cn/api/priceQuotationController/marketPageList'
  # ③ 品种分类树（蔬菜/水果/…，免参）
  curl -s -A "$UA" -X POST -H 'Content-Type: application/json' -d '{}' \
    'https://pfsc.agri.cn/price_portal/web/portal-product/getProductClass'
  # ④ 农产品品种树（A>AA粮食>AA01谷物…），GET 即可
  curl -s -A "$UA" 'https://pfsc.agri.cn/price_portal/sys-user-relation/getVarietiesTree'
  # ⑤ 农业农村部 200 指数十日报（POST 需页面内置 token，会轮换）
  curl -s -A "$UA" -X POST -d 'token=3cec8829-8aba-452e-8c9a-e0deca77853b' \
    'https://www.agri.cn/nyb/getIndexByTenDay'
  # ⑥ 单品种指数（capes.agri.cn，GET）
  curl -s -A "$UA" 'https://www.agri.cn/indexFB/getHHCRawMaterialsIndex'
  ```
  结果形态：全为 **JSON**（`{"code":200,"message":"请求处理成功","content":[…]}` 或 `{"code":0,"data":[…]}`）。产业指数卡片页 `https://www.agri.cn/sj/` 与走势页 `/sj/jgzs/qgbtzr/` 为 HTML（数值由 JS 填充）。
- 覆盖：批发价格 200 指数**日度**（如 2026-09-30 农产品 115.36 / 粮油 114.04 / 菜篮子 115.58）；旬度「十日报」；批发市场名录约 **301 家**、品种数百个；单品种/地方产业指数（葡萄、石榴、柑桔、蔬菜、猪肉、野生菌、肉鸭…）各自频率不一。200 指数编制方案 2026-05-25 起优化调整（剔除 48 家、新增 53 家市场）。
- 门槛：**免费、免登录、无 key**；仅 `jgsb.agri.cn` 报送端需账号（非取数用）。`data.moa.gov.cn` 目录页有防爬挑战。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20 s 超时）——`POST pfsc…/getPortalPiInfoDay` → 200 JSON，首条 `publishDate:2026-09-30`；`POST pfsc…/marketPageList` → 200，`totalCount:301`；`POST pfsc…/getProductClass` → 200，返回蔬菜/水果等大类品种名；`GET pfsc…/getVarietiesTree` → 200 品种树；`POST www.agri.cn/nyb/getIndexByTenDay`（带 token）→ 200，含「农产品批发价格200指数 115.36」「菜篮子 115.58」等；`GET www.agri.cn/indexFB/getHHCRawMaterialsIndex` → 200 `{"code":"200","hb":"1.21","pushDate":"2026年第38周","zhiShu":"84.66"}`；`GET www.agri.cn/indexFB/getRawMaterialsIndex?indexVarietyType=2` → 200。
- 上游：中国农业农村信息网 `https://www.agri.cn/`（农业农村部信息中心）；全国农产品批发市场价格信息系统 `https://pfsc.agri.cn/`；农业农村部数据门户 `https://data.moa.gov.cn/`。

## 细节

### pfsc.agri.cn 已探明端点（前端 JS 提取 + 实测）

| 端点 | 方法 | 参数/说明 |
|---|---|---|
| `/price_portal/pi-info-day/getPortalPiInfoDay` | POST | `{}` 即可；日度 200/粮油/菜篮子指数序列 |
| `/price_portal/pi-info-day/getPortalPiInfoMonth` | POST | 月度指数 |
| `/price_portal/pi-info-day/getIndexByLevel` | POST | 分级指数（GET 返 405） |
| `/price_portal/pi-info-day/getPiDataPigCarcassDay` / `…Days` | POST | 瘦肉型白条猪肉出厂价指数 |
| `/price_portal/pi-info-day/getPiDataHotPepperList` | POST | 辣椒等单品指数 |
| `/api/priceQuotationController/marketPageList` | POST | `{pageNum,pageSize}`；批发市场名录（totalCount≈301） |
| `/api/priceQuotationController/getMarketByProvinceCode` / `getTodayMarketByProvinceCode` | GET/POST | 按省取市场；参数名敏感，错参会返 `code:500` |
| `/price_portal/region/selectList` | POST | 省市区划下拉 |
| `/price_portal/sys-user-relation/getVarietiesTree` | GET | 品种树（含 code/label） |
| `/price_portal/sys-user-relation/getTreeByProvinceName` | GET | 省级市场树（POST 返 405） |
| `/price_portal/web/portal-product/getProductClass` | POST | 品种分类（大白菜、番茄…） |
| `/price_portal/web/portal-product/selectList` | POST | 品种百科；字段用 `currentPage/pageSize/name`，**不是** `pageNum`（写错返 400） |
| `/price_portal/index/getMarketReportPriceChart`、`/index/growthRanking` | POST | 市场价格图/涨幅榜 |
| `/api/FarmDaily/list`、`/api/farmWeekly/pageList`、`/api/portal-analysis-report/selectListByPage` | POST | 日/周度分析报告 |

### www.agri.cn / capes.agri.cn 指数端点

- `/nyb/getIndexByTenDay`（POST，`data:token=<页面内置值>`）→ 农产品批发价格 200 指数十日报，多条 `indexName/indexValue/indexType`（A 农产品、AX 菜篮子、AJ 粮油、AO 畜产、B 水产、AE 蔬菜、AF 水果、AA 粮食…）。
- `/indexFB/getHHCRawMaterialsIndex` → 最新周指数（`pushDate` 形如「2026年第38周」）。
- `/indexFB/getRawMaterialsIndex?indexVarietyType={1,2,3,5,6,7}` → 分类别产业指数（1 为葡萄产业指数等地方/单品指数）。
- `/indexFB/bhIndexPublish`、`gjIndexPublish`、`hcIndexPublish`、`hhcIndexPublish`、`ptIndexPublish`、`slIndexPublish`、`ydjIndexPublish` → 各指数发布数据。
- `/jgzssj/porkAgri?flag=1&type=empty1`（JSONP）→ 生猪价格走势（本机多次超时 rc 28，未取到）。

## 坑

1. **POST-only 接口**：`getIndexByLevel`、`growthRanking`、`region/selectList` 等用 GET 直接返 **405**，须 `-X POST`（多数给 `{}` 即可）。
2. **参数名不一致**：同一站内 `marketPageList` 用 `pageNum`，`portal-product/selectList` 却用 `currentPage`，字段名写错返 400 并在 message 里回显实体字段表。
3. **token 会轮换**：`/nyb/getIndexByTenDay` 的 token 硬编码在 `www.agri.cn` 首页内联脚本里，改版/轮换即失效；失效时改从首页重新抓。
4. **WAF 对爬虫敏感**：`pfsc.agri.cn` 对搜索引擎爬虫返回「您的访问请求可能对网站造成安全威胁，请求已被阻断」；带正常桌面 UA 的 curl 正常，但别高频。
5. **`jgsb.agri.cn` 是报送端**（登录/填报），公众查询走 `pfsc.agri.cn`；`/api/priceQuotationController/queryMarket` 参数不明，传错一律 `code:500`（勿当接口挂了）。
6. 部分产业指数**更新滞后**（如 `indexVarietyType=1` 停在 2025 年 9 月），引用前先看 `pushDate/lastOneYearWeek`。
7. 页面数值（`agri.cn/sj/` 指数卡片）默认渲染为 0，需 JS 加载后才显示——离线抓 HTML 拿不到数，改走上面的 JSON 接口。
