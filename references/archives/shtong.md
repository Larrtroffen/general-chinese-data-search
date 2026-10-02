# shtong.gov.cn —— 上海通 上海数字方志

上海市地方志办公室新版站点（标题「上海数字方志-智服」）。**首页是纯前端壳**（HTML 只有 3.5 KB，内容全靠 JS），但**底层 REST 接口是开放的**：`/api/zhifu/open/...`，GET、无需 cookie/token，返回 JSON（含全文 `content`）。对上海相关检索（年鉴、区志、方志动态、大事记）这是**直连可用的正路**——别去点页面。

- 去哪找：
  - 站点：`https://www.shtong.gov.cn/`
  - 接口基址：`https://www.shtong.gov.cn/api/zhifu/open`
  - **全文/标题检索**（主力）：`GET /api/zhifu/open/record/search`
  - 详情（完整正文 HTML）：`GET /api/zhifu/open/record/{id}`
  - 其余端点（分页列表、展览、大事记、历史上的今天、场馆活动）见「细节」。
- 什么时候用：
  - 查**上海**的地方志/年鉴内容、方志办动态、大事记、线上展览；
  - 需要**程序化全文检索上海方志系统语料**（关键词 → 标题/正文/ID）；
  - 对照北京同类源（`bjdsdfz.cn.md`、`difangzhi.cn.md`）做「市/区两级方志」交叉核对。
- 怎么取：
  ```bash
  BASE=https://www.shtong.gov.cn/api/zhifu/open
  # 检索（返回 {total, rows:[{zhifuId, zhifuType, title, content, ...}]}）
  curl -s "$BASE/record/search?keyword=%E5%B9%B4%E9%89%B4&pageNum=1&pageSize=20" | python3 -m json.tool | head -40
  # 列表分页
  curl -s "$BASE/record/list/1?pageNum=2&pageSize=10"
  # 详情（正文是 HTML，含 <p>/<img>，图片在 https://www.shtong.gov.cn/books/shanghaioss/image/<hash>.jpg）
  curl -s "$BASE/record/900135"
  ```
  解析要点：`total` = 命中总数；`rows[].zhifuId` 作详情键；`content` 已是正文（`&nbsp;`/`&ldquo;` 等实体需 unescape）；`zhifuType` 是内容类型（实测见 `1` 与 `9`，语义未标注）。
  **接口路径怎么找到的**（复用时站点改版可照做）：首页 → `/static/index-*.js` → 动态 chunk `/static/index-*.js` → grep `"/api/…"` → 得到 `/api/zhifu/open/...` 前缀。
- 覆盖：上海方志系统**站内内容**（新闻/动态/年鉴相关文章/大事记/展览）。实测 `record/list/1` 总数 **4265**、`keyword=年鉴` 命中 **562**、`keyword=上海` 命中 **2806**。**是否含志书原文全文未确认**（图片资源在 `/books/shanghaioss/`，站点可能另有阅读器）。粒度：文章级（标题+正文 HTML+ID）；无结构化字段（无日期/作者独立字段——日期多在正文里，需自行解析）。更新：动态站，随官网更新。
- 门槛：**无需 key / 无 cookie / 无登录**；未观测到反爬（GET 稳定 200）。请求要带浏览器 UA 更稳；正文含 HTML 与实体，入库前要清洗（可接 `../tools/defuddle.md` 或简单正则）。老 URL（`/newsite/`、`/search`、`robots.txt`、`sitemap.xml`）**全部返回同一 SPA 壳**（3538 B）→ 别按老路径抓；`robots.txt`/`sitemap.xml` 实际不存在。
- 实测：2026-10-02，macOS 27（arm64），curl 8.x，UA=`Mozilla/5.0`。① `curl -o shtong_home.html https://www.shtong.gov.cn/` → **200 / 3538 B**，只有 `/static/index-D7kywHWi.js`（1.33 MB）与 `index-DoinsssY.css` → 判定 SPA。② 抓 15 个动态 chunk（共 872 KB）后 `grep -rohE '"/[a-zA-Z0-9_/\-]{3,50}"'` → 命中 `"/api/zhifu/open/record/search"`、`".../record/list/1"`、`"/api/zhifu/open/exhibition/list"`、`"/api/zhifu/open/memorabilia/years/"` 等。③ `curl "$BASE/record/search?keyword=上海&pageNum=1&pageSize=3"` → **200**，`{"total":2806,"rows":[{"zhifuId":900135,"zhifuType":"1","title":"从记录城市到服务城市…",...}]}`；`record/search?keyword=年鉴&pageSize=50` → total **562**（zhifuType 分布 `1`:44、`9`:6）。④ `curl "$BASE/record/900135"` → `{"msg":"操作成功","code":200,"data":{...content:"<p>…<img src=\"https://www.shtong.gov.cn/books/shanghaioss/image/28d0f703248a41d9833a2f6513c86dbb.jpg\"…"}}`。⑤ `record/list/1?pageNum=2&pageSize=3` → total **4265**；`exhibition/list` → total **8**。⑥ 对照：`/robots.txt`、`/sitemap.xml`、`/newsite/`、`/api/search` 全部落到 SPA 壳或 `{"code":500,"msg":"404 NOT_FOUND"}`。
- 上游：https://www.shtong.gov.cn/

## 细节

### 端点表（全部 GET，实测）

| 接口 | 用途 | 参数 |
|---|---|---|
| `/api/zhifu/open/record/search` | **全文/标题检索**（主力） | `keyword`、`pageNum`、`pageSize` |
| `/api/zhifu/open/record/list/{type}` | 按类型分页列表 | 路径 `{type}`（样例 `1`、`5`）、`pageNum`、`pageSize` |
| `/api/zhifu/open/record/{id}` | **详情（完整正文 HTML）** | 路径 `{zhifuId}` |
| `/api/zhifu/open/exhibition/list` | 线上展览列表 | — |
| `/api/zhifu/open/memorabilia/list`、`/memorabilia/years/` | 大事记 | — |
| `/api/zhifu/open/todayInHistory`、`/weeklyChronicle/list` | 历史上的今天 / 一周纪事 | — |
| `/api/zhifu/open/museumActivity/list` | 场馆活动 | — |
