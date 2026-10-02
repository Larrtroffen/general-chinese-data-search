# religious-bodies —— 五大宗教团体官网与院校名录

- 去哪找：**国家宗教事务局宗教基础信息查询系统**（院校）`https://www.sara.gov.cn/resource/common/zjjcxxcxxt/zjyxjbxx.html`（按宗教分行，明细页 `religious.html?religionTypeId=<id>`），数据域 `https://api.sara.gov.cn/mis//web/religionInstitution/list`；**全国性宗教团体官网**——中国佛教协会 `https://www.chinabuddhism.com.cn/`、中国道教协会 `http://taoist.org.cn/`、中国伊斯兰教协会 `http://www.chinaislam.net.cn/`、中国天主教一会一团 `https://www.chinacatholic.cn/`、中国基督教两会（中国基督教网）`https://www.ccctspm.org/`。
- 什么时候用：要**全国宗教院校名录**（佛教/道教/伊斯兰教/天主教/基督教，含主办单位、院校名称、地址、负责人）；要**五大宗教团体的组织架构与人事名录**（理事会/监事会/专门委员会、主席会长副主席、部门设置）；要团体官网的制度、公告、经学院/神学院校专栏作团体口径佐证。
- 怎么搜：**院校名录走匿名 JSON**（先取宗教字典拿 `religionTypeId`，再按宗教分页）：
  ```bash
  UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
  # ① 宗教类别字典 → religionTypeId
  curl -sS -A "$UA" --compressed 'https://api.sara.gov.cn/mis//web/religion/getAllReligion?pageNum=1&pageSize=999'
  # ② 宗教院校名录（religionTypeId 可省，省则全部；pageSize 可放大到 999999 一次取全）
  curl -sS -A "$UA" --compressed \
    'https://api.sara.gov.cn/mis//web/religionInstitution/list?pageNum=1&pageSize=999999&religionTypeId=1166691628950224896'
  ```
  各团体官网为**静态 HTML**（`/web/…/list.shtml`、`/ccic/…-1.htm`、`/church/<n>`）；伊斯兰教协会另有站内检索 JSON：`GET /cms/custom/query_yixie_wangzhan.jsp?keyWord=<kw>&pageNumber=1&pageSize=10`；基督教两会站内检索 `GET https://www.ccctspm.org/search?title=<kw>`（HTML）。结果形态：**JSON**（院校/检索）+ **HTML**（团体栏目）。
- 覆盖：**全国宗教院校 94 所**（`total:94`；佛教 43、基督教 21、道教 11、伊斯兰教 10、天主教 9，2026-10-03 实测）；字段 `religionType`、`sponsorName`（主办单位）、`institutionName`（院校名）、`address`、`personCharge`（负责人）、`siteId`、`id`。团体官网覆盖协会概况/理事会/部门/制度/院校专栏与新闻，更新随官网发稿。
- 门槛：院校名录与各团体官网**免费、免登录、无 key**；团体官网的「信息查询」是另一套**需登录**的系统（见坑 2）。
- 实测：2026-10-03，macOS arm64，curl 8.x 桌面 UA——`GET GetAllReligion` → 200 JSON，5 类及其 `id`；`GET religionInstitution/list?pageSize=999999` → 200 `total:94`，行如「中南神哲学院｜中南六省（区）天主教“两会”」；`GET http://www.chinaislam.net.cn/index1.shtml` → 200 `<title>中国伊斯兰教协会</title>`；`GET https://www.chinacatholic.cn/` → 200 `<title>首页 - 中国天主教</title>`；`GET https://www.ccctspm.org/church/2` → 200（「神学院校」列表，`/churchinfo/203`＝华东神学院）；`GET /cms/custom/query_yixie_wangzhan.jsp?keyWord=经学院&pageSize=3` → 200 JSON `allCount:108`；`GET https://www.ccctspm.org/search?title=神学院` → 200 HTML `result-count">(2109)`。
- 上游：<https://www.sara.gov.cn/resource/common/zjjcxxcxxt/zjyxjbxx.html>（国家宗教事务局宗教基础信息查询系统）；团体官网见上。

## 细节

### 五大团体官网与入口（2026-10-03 实测）

| 团体 | 官网 | 组织/人事栏目 | 院校 |
|---|---|---|---|
| 中国佛教协会 | `www.chinabuddhism.com.cn` | 另见 `chinabuddhism.com.cn.md`（WAF，需浏览器） | 佛学院见 sara 名录 |
| 中国道教协会 | `taoist.org.cn`（裸域） | 另见 `taoist.org.cn.md` | 中国道教学院 `getDjzsByC2Action.do?c2=xy` |
| 中国伊斯兰教协会 | `www.chinaislam.net.cn` | `/web/abouts/a/list.shtml` 本会介绍、`/d/list.shtml` 理事会、`/e/list.shtml` 监事会、`/f/a..c/list.shtml` 三个专委会、`/c/*/list.shtml` 部门设置 | 中国伊斯兰教经学院 `/web/zbyx/index.shtml`；招生 `zs.chinaislam.net.cn` |
| 中国天主教一会一团 | `www.chinacatholic.cn` | 爱国会 `/ccic/report/1806/0552-1.htm`、主教团 `/ccic/report/1806/0553-1.htm` | 神哲学院见 sara 名录 |
| 中国基督教两会 | `www.ccctspm.org` | 全国两会 `/cppcc`、`/personnel` 人员组成、`/department` 部门设置 | 神学院校 `/church/2`（详情 `/churchinfo/<id>`）、院校事工 `/news/5` |

### 基督教两会「各地教会」三页

- `/church/1` 教堂风采、`/church/2` 神学院校、`/church/3` 各地两会；详情页统一 `/churchinfo/<id>`（HTML）。
- 检索：`GET /search?title=<kw>`，正文含 `result-count">(N)`；无需 key。

### 伊斯兰教协会站内检索（JSON）

- `GET /cms/custom/query_yixie_wangzhan.jsp?keyWord=<kw>&pageNumber=1&pageSize=10` → `{"code":200,"allCount":N,"totalPages":M,"data":[{title,href,summary,publishDate,photo}]}`。
- 检索页 `/search/search.shtml?keyWord=<kw>`；条目 `href` 指向站内 `.shtml` 详情。
- 站内亦有维吾尔文版 `uyghur.chinaislam.net.cn`、赞助院校板块、朝觐事务、经学思想（新卧尔兹）等栏目。

## 坑

1. **「信息查询」是登录系统**：各团体官网右上角「信息查询」跳 `info.<团体域名>/commonSearch/login?relaff=<机构码>`（如 `info.chinaislam.net.cn`、`info.chinacatholic.cn`、`info.ccctspm.org`），为 Vue SPA，标题「宗教基础信息查询」；其 API 为 `POST /api/im/siteInfo/pub/list`（场所）、`POST /api/im/tchInfo/pub/list`（教职人员），匿名返回 **HTTP 500 / status 4011**（未授权），须用机构发放的账号。公开场所名录仍回匿名接口 `sara.gov.cn.md`。
2. **院校名录是登记快照**：`updateTime` 参差、部分为 `null`；为团体报送口径，非当年实际招生数。全国院校 94 所与本层其他卫生/教育口径不可混用。
3. **佛教协会 WAF、道教协会 www 被拦**：详见 `chinabuddhism.com.cn.md`、`taoist.org.cn.md`；本卡不重复。
4. **chinacatholic.cn 无院校名录**：官网仅新闻/牧灵福传/神学灵修等栏目与爱国会/主教团两页；天主教院校须走 sara 名录。
5. 团体官网栏目为 `.shtml` / `-1.htm` 静态路径，条数大时不提供分页 API，逐页抓列表即可；检索走各自的 `search` 入口。
