# nlc.cn —— 国家图书馆数字资源入口

国家图书馆门户及其知识服务平台。**多数全文库需读者卡登录或到馆**，此处只记录「入口 + 是否公网可达」，供需要民国期刊、古籍、地方文献时定位。

- 去哪找：
  - 门户首页：`https://www.nlc.cn/`（301 → `/web/index.shtml`）
  - 读者云门户（数字资源）：`http://read.nlc.cn/user/category`
  - 数字资源列表：`http://dportal.nlc.cn:8332/zylb/zylb.htm`
  - **民国时期地方文献知识库**：`http://mg.nlc.cn/`（Vue SPA；**API 基址 `/api/` 已实测匿名可用**）
  - 革命文献与民国时期文献保护计划：`http://mgwxbh.nlc.cn/`
  - 中华古籍智慧化服务平台：`https://guji.nlc.cn/`（**检索 API 已单独写卡 `guji.nlc.cn.md`**）
  - 中国历史文献总库·民国图书数据库：`http://mg.nlcpress.com/`（商业库，需授权）
  - 政府公开信息整合服务平台：`http://govinfo.nlc.cn/`
- 什么时候用：需要**民国期刊/民国图书/古籍/地方文献**时定位入口；做「人物—机构—地点」关系探索（`mg.nlc.cn`）。
- 怎么搜：
  - `mg.nlc.cn` 为前端 SPA、`config.js` 给出 `window.CONFIG.baseSever = "https://mg.nlc.cn/api/"`（`appId 90059`，SSO 走 `sso1.nlc.cn`）；实测匿名可取的接口均为 **GET**（POST 会报 `Request method 'POST' not supported`）。
  - 想找具体某个库，先查 `dportal.nlc.cn:8332/zylb/zylb.htm` 名录页（实测页面内可搜到「民国图书馆学文献数据库」等条目）。
- 覆盖：国民图书/期刊/古籍/地方文献入口；`mg.nlc.cn` 知识图谱型（人物/事件/机构/地理/产物五类实体），**不是全文书库**。
- 门槛：多数全文库需**读者卡登录或到馆**；`mg.nlc.cn` 知识库 API 匿名可用；`mg.nlcpress.com` 付费；数字资源全文普遍受登录/馆内限制，**不要承诺公网可下载**。
- 实测：2026-10-02，macOS（arm64），curl 8.x。逐个 `curl -sL -o /dev/null -w '%{http_code}'` 探测：`www.nlc.cn` 200（落到 `/web/index.shtml`）；`read.nlc.cn/user/category` 200（25 KB，标题「读者云门户」）；`mg.nlc.cn` 200（2.4 KB SPA 外壳）；`guji.nlc.cn` 200（5.9 KB SPA 外壳）；`mgwxbh.nlc.cn` 200；`dportal.nlc.cn:8332/zylb/zylb.htm` 200（~560 KB）；`mg.nlcpress.com` 200；`govinfo.nlc.cn` 200。2026-10-03 补测（桌面 Chrome UA，`Referer: https://mg.nlc.cn/`）：`GET http://mg.nlc.cn/` → 301 → `https://mg.nlc.cn/` 200 / 2380 B（`<title>民国时期地方文献知识库</title>`）；`GET /config.js` → 200，`baseSever=https://mg.nlc.cn/api/`；`GET /api/knowledge/commonApi/getCountForReader` → 200（5 类实体计数）；`GET /api/map/visualization/historyEvent/events?pageNum=1&pageSize=3` → 200，`total=8025`；同路径 POST → 200 但 body `{"msg":"Request method 'POST' not supported","code":500}`。
- 上游：`https://www.nlc.cn/` ；`http://mg.nlc.cn/` ；`https://guji.nlc.cn/`

## 细节

### 可用性矩阵（均为公网 GET 探测，不代表可看全文）

| 入口 | URL | 状态 | 说明 |
|---|---|---|---|
| 门户首页 | `https://www.nlc.cn/` | ✅ 200（301→`/web/index.shtml`） | 全网导航 |
| 读者云门户（数字资源） | `http://read.nlc.cn/user/category` | ✅ 200 | 资源分类页；**看全文需登录读者卡** |
| 数字资源列表 | `http://dportal.nlc.cn:8332/zylb/zylb.htm` | ✅ 200 / ~560 KB | 全量数据库名录（含民国、方志类） |
| **民国时期地方文献知识库** | `http://mg.nlc.cn/` | ✅ 200（301→https） | Vue SPA；**API 基址 `/api/` 已实测匿名可用** |
| 革命文献与民国时期文献保护计划 | `http://mgwxbh.nlc.cn/` | ✅ 200 | 项目站/资源导航 |
| 中华古籍智慧化服务平台 | `https://guji.nlc.cn/` | ✅ 200 | 古籍 SPA；**检索 API 已单独写卡：`guji.nlc.cn.md`** |
| 中国历史文献总库·民国图书数据库 | `http://mg.nlcpress.com/` | ✅ 200 | 商业库（国图出版社），需授权 |
| 政府公开信息整合服务平台 | `http://govinfo.nlc.cn/` | ✅ 200 | 政策文件 |

### mg.nlc.cn 民国时期地方文献知识库 —— 前端 SPA，但 `/api/` 匿名可用（2026-10-03 实测）

实测匿名可取的接口（**GET**，POST 会报 `Request method 'POST' not supported`）：

| 端点 | 说明 | 实测 |
|---|---|---|
| `GET /api/knowledge/commonApi/getCountForReader` | 知识库实体计数 | 200：`personal 20280`、`event 8025`、`org 5514`、`geographical 4803`、`product 14984` |
| `GET /api/map/visualization/historyEvent/events?pageNum=&pageSize=` | 历史事件列表（结构化：`chiEventName`、`constructionUnits`、`identifier`…） | 200，`total 8025` |
| `GET /api/map/visualization/historyEvent/{types,timeEcho,eventTypeEcho}` | 事件类型/年代聚类 | 未逐条验证 |
| `GET /api/map/visualization/historyEvent/lenovoSearch?keyword=抗战` | 联想检索 | 200，但用 `keyword` 返回 `data:[]`（**参数名未确证**） |

- 这是**知识图谱型**库（人物/事件/机构/地理/产物五类实体），**不是全文书库**；适合做民国人物—机构—事件的关系拆解，不指望拿到文献全文。
- 全文仍在 `read.nlc.cn`（民国期刊库，需读者卡）与付费库 `mg.nlcpress.com`（民国图书）。
- 前端 JS：`https://mg.nlc.cn/assets/index.4a24319f.js`（`grep '"/[a-z]'` 可复现端点清单）。

### 定位与替代

- **民国期刊全文**：国图「民国时期期刊全文数据库」在 `read.nlc.cn` 数字资源内，公网一般仅见题录，**全文需登录/到馆**；替代方案见 `difangzhi.cn.md` 与 CNKI 民国期刊库。
- **民国图书**：`mg.nlcpress.com`（中国历史文献总库·民国图书数据库）为付费库。
- **民国地方文献**：`mg.nlc.cn` 知识库可公网打开，适合做「人物—机构—地点」关系探索。
- **古籍**：`guji.nlc.cn`。

## 坑

1. `https://www.nlc.cn/` 会 301 到 `/web/index.shtml`；直接拼 `/web/index.html` 会 404。
2. 旧路径 `dportal.nlc.cn:8332/…` 带端口号 8332，是历史遗留入口，能用但可能变动。
3. `mg.nlc.cn`、`guji.nlc.cn` 均为前端 SPA，`curl` 只能拿到外壳；**但其 API 基址（均以 `/api/` 开头、POST/GET + JSON）已实测匿名可用**——`guji.nlc.cn.md` 与本文上节给了可用端点，别再只看外壳页面。
4. 数字资源全文普遍受登录/馆内限制，**不要承诺公网可下载**。
