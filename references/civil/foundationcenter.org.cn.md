# foundationcenter.org.cn —— 基金会数据库与透明指数接口

- 去哪找：**基金会中心网** `https://www.foundationcenter.org.cn/`；**数据接口基址** `https://api.foundationcenter.org.cn/api`（前端 `assets/index.*.js` 里 `baseURL` 明写）。
- 什么时候用：要**全国基金会名录**（名称→内部 OID）、**业务领域/项目议题/开展地/主导方类型/捐赠收入等分面计数**、**FTI 中基透明指数（年度）**、基金会**财务排行/年报索引**、行业**数据报告与行业资讯**。
- 怎么搜：免登录的 JSON 接口（GET/POST，桌面 UA + `Referer: https://www.foundationcenter.org.cn/`）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  REF='Referer: https://www.foundationcenter.org.cn/'
  B='https://api.foundationcenter.org.cn/api'
  # ① 全站分面树 + 各值命中数（免参，~185 KB）
  curl -s -A "$UA" -H "$REF" "$B/HomeAPI/SearchConditionsList?client="
  # ② 基金会名称联想（Key=关键词）→ 名称 + 加密 OID
  curl -s -A "$UA" -H "$REF" -H 'Content-Type: application/json' -X POST \
    -d '{"Key":"教育","Client":""}' "$B/HomeAPI/SearchTipList"
  # ③ 按 Key 反查单个条件的 ID/类型
  curl -s -A "$UA" -H "$REF" -H 'Content-Type: application/json' -X POST \
    -d '{"Key":"","Client":""}' "$B/HomeAPI/GetSearchConditions"
  # ④ 首页资讯/行业报告外链；⑤ 数据报告入口外链
  curl -s -A "$UA" -H "$REF" "$B/HomeAPI/SearchDefault"
  curl -s -A "$UA" -H "$REF" "$B/HomeAPI/FoundationIndustryLink"
  # ⑥ FTI 透明指数年度统计（免参）
  curl -s -A "$UA" -H "$REF" -H 'Content-Type: application/json' -X POST -d '{}' "$B/Visualization/FTI"
  ```
  结果形态：全为 **JSON** `{"code":1,"success":true,"data":…}`。**需登录**的接口统一返 `{"code":10,"success":false,"msg":"登录验证失败"}`。
- 覆盖：全国基金会名录与分面统计（13 个顶级分面、共约 **787** 个取值，含命中数）；FTI 透明指数按年度（实测 `Annual:2025`，公募/非公募与分数段分布）；行业数据报告、财务排行、机构年报（报告/详情接口需登录）。
- 门槛：**分面统计、名称联想、报告外链、FTI 统计免登录**；**基金会列表检索、单机构详情/年报/财务** 需登录（接口返 `code:10`）。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20 s 超时）——`GET …/HomeAPI/SearchConditionsList?client=` → **200**，185 078 B，`code:1`，13 个顶级分面（基金会业务领域/项目议题领域/项目开展地/基金会主导方类型/年度捐赠收入/年度公益活动支出…），如「教育发展」`SearchCount:2164`；`POST …/HomeAPI/SearchTipList` `{"Key":"教育"}` → **200**，返回「福建教育学院教育发展基金会」等名称+`OID`；`POST …/HomeAPI/GetSearchConditions` → **200**，返回按 Key 命中的条件（`Names/TypeName/SCID/SCPID`）；`GET …/HomeAPI/SearchDefault`、`GET …/HomeAPI/FoundationIndustryLink` → **200** 资讯/报告外链；`POST …/Visualization/FTI {}` → **200**，`Annual:2025` + 透明指数分布；`POST …/HomeAPI/SearchList {}`、`POST …/FTIAPI/GetBasicInfo`、`POST …/FTIAPI/GetFoundationBaseInfoCSZG`、`POST …/HomeAPI/GetShuSuoClass/List` → **200**，均 `code:10 登录验证失败`。
- 上游：基金会中心网（中国基金会中心网/北京基业长青社会组织服务中心体系）；`https://www.foundationcenter.org.cn/`。

## 细节

### api.foundationcenter.org.cn 已探明端点（前端 JS 提取 + 实测）

| 端点（`…/api` 之后） | 方法 | 登录 | 说明 |
|---|---|---|---|
| `/HomeAPI/SearchConditionsList?client=` | GET | 免 | 全站分面树 + 各值 `SearchCount`（13 顶级分面 / 787 值） |
| `/HomeAPI/SearchTipList` | POST | 免 | `{Key,Client}`；名称联想 → `{OID,FoundationName}` |
| `/HomeAPI/GetSearchConditions` | POST | 免 | `{Key,Client}`；按 Key 反查条件 `{SCID,SCPID,Names,TypeName}` |
| `/HomeAPI/SearchDefault` | GET | 免 | 首页资讯/数据观察外链 |
| `/HomeAPI/FoundationIndustryLink` | GET | 免 | 数据报告/行业观察入口外链（dataReport/foundationRankings/dataDashboard…） |
| `/HomeAPI/News` `/HomeAPI/NewsTop` `/FTIAPI/NewsTop` | POST/GET | 免 | 资讯列表/头条 |
| `/Visualization/FTI` | POST | 免 | FTI 透明指数年度统计（`Annual`/`Summary`/`ScoreDistribution`） |
| `/HomeAPI/SearchList`、`/HomeAPI/SearchProjectList` | POST | 需 | 基金会/项目检索（`code:10`） |
| `/FTIAPI/GetBasicInfo`、`GetFoundationBaseInfoCSZG`、`GetFoundationBaseInfo_Affair` | POST | 需 | 单机构基本信息/年报（`code:10`） |
| `/HomeAPI/GetShuSuoClass`、`/HomeAPI/GetShuSuoList` | POST | 需 | 年报/报告中心（`code:10`） |
| `/HomeAPI/GetFinancialRanking`、`GetFinancialProportion` | POST | 需 | 财务排行/构成（参数 `{FoundationID,Client}`/`{Annual,…}`） |
| `/UserAPI/*` | POST/GET | — | 账号、微信扫码登录、绑定等 |

前端为 Vue 单页应用（`assets/index.bTr9FBFS.js`，`BUILD_VERSION 1.0.73`）；接口路径与参数名由该 bundle 反查。`SearchList` 请求体沿用分面检索（字段含 `Key/Client/PageIndex/PageSize` 一类），未登录不通。

## 坑

1. **详情类接口一律 `code:10`**：`SearchList`、`GetBasicInfo`、`GetFoundationBaseInfoCSZG`、`GetShuSuo*` 直连被登出，需浏览器登录态。
2. 组织标识是**加密 `OID`**（SearchTipList 返回，如 `bzgvUjNlek1tMFpRakVUWEN0V3NvZz09`），不是登记证号；跨接口沿用同值。
3. 分面里部分条件的 `SearchCount` 为 **-1/0**（如「项目议题领域」「项目开展地」），非实时计数，别当名录规模。
4. 页面 `dataReport`/`dataDashboard`/`foundationRankings` 为前端渲染，离线抓 HTML 无数据；结构化数走上述接口。
