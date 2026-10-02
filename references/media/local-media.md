# 地方融媒体与区县新闻 —— 党媒平台·澎湃·闪电·封面

- 去哪找：
  - **全国党媒信息公共平台**（人民日报社）：`https://www.hubpd.com/`（地方党媒与县级融媒体号的内容汇聚，检索走 API）。
  - **澎湃新闻**：`https://www.thepaper.cn/`（含全国地方频道）。
  - **齐鲁网/闪电新闻**（山东台）：`https://www.iqilu.com/`、检索页 `https://s.iqilu.com/cse/search`。
  - 各省级客户端：闪电新闻 `https://sdxw.iqilu.com/`、我苏 `https://www.ourjiangsu.com/`、潮新闻（原天目）`https://tidenews.com.cn/`、华声在线/新湖南 `https://www.voc.com.cn/`、川观新闻 `https://cbgc.scol.com.cn/`。
  - 封面新闻 `https://www.thecover.cn/`、极目新闻 `https://www.ctdsb.net/`、上游新闻 `https://www.cqcb.com/`、红星新闻 `https://www.hongxingnews.com/`。
- 什么时候用：
  - 关键词式需求：某地「区县/乡镇」的本地新闻、通报、活动稿；
  - 要找**原发稿的媒体与链接**（党媒平台检索结果带 `reprintedUrl` 原链接）；
  - 要**地方媒体对某话题的报道集合**（澎湃/闪电可按词检索）；
  - 不适用：央媒专稿（→ `people.com.cn.md`、`xinhuanet.com.md`）、公众号原文（→ `../wechat/`）、报纸原版（→ `epaper/`）。
- 怎么搜：
  - **全国党媒信息公共平台（首选，免登录 JSON，覆盖县级融媒）**：
    ```bash
    curl -sS -m 25 -H 'Content-Type: application/json' -H 'Referer: https://www.hubpd.com/' \
      -X POST 'https://api-m.hubpd.com/main_station/search' \
      -d '{"keyword":"物业","pageNum":1,"pageSize":10}'
    # 可选：contentType、keywordSearchScope；话题另走 GET https://api-m.hubpd.com/topics/search?keyword=物业&pageNum=1&pageSize=20
    ```
    结果形态：**JSON** `{"errCode":0,"data":[...]}`；每条含 `title`、`mpName`（媒体号，如「湖南日报」）、`reprintedUrl`（**原文链接**）、`createdAt`、`transCodingObjKey`（封面）、`type`。
  - **澎湃新闻**：
    ```bash
    curl -sS -m 20 -H 'Content-Type: application/json' -H 'Referer: https://www.thepaper.cn/' \
      -X POST 'https://api.thepaper.cn/search/web/news' -d '{"word":"物业","pageNum":1,"pageSize":10}'
    ```
    结果形态：**JSON** `{"code":200,"data":{"list":[...]}}`；字段含 `name`（标题，含 `<font>` 高亮）、`contId`（详情 `https://www.thepaper.cn/newsDetail_forward_<contId>`）、`summary`、`pubTimeLong`、`nodeInfo.name`（频道）、`praiseTimes`。关键词字段是 **`word`**（不是 `keyword`）。
  - **齐鲁网/闪电新闻**：
    ```bash
    curl -sS -m 20 -H 'Referer: https://s.iqilu.com/' \
      'https://s.iqilu.com/api/search?q=物业&page=1&size=10&sort=1&nsid=1&method=1&range=0'
    ```
    结果形态：**JSON** `{"code":200,"data":{"items":[{docType,id,title,url,description}],"total":N}}`；`url` 指向 `sdxw.iqilu.com`（闪电新闻）。参数：`sort` 1 默认/2 按时间，`nsid` 1 综合/2 新闻/3 视频/4 时评，`method` 1 标题/2 全文，`range` 0 全部/60/1440/10080/43200（分钟）。
  - **封面/极目/上游/红星**：匿名检索不可直取（见「坑」），只能用浏览器或 `../engines/` 的 `site:` 点查。
- 覆盖：
  - 党媒平台：全国各级党媒 + **县级融媒体中心号**聚合，条目带原媒体名与原文链接；时间到分钟；动态更新。
  - 澎湃：全站（含本地频道）稿件，历史可回溯到早期；闪电：山东广电系稿件（本机检索命中「成都双晒…物业」等跨地稿亦收录）。
  - 省级客户端：各省市县稿，网页以 App 内容为主，检索能力弱。
- 门槛：党媒平台/澎湃/闪电检索 **免费、免登录、无 key**（党媒平台的 `appKey` 内嵌在前端 `https://www.hubpd.com/js/config.js`，检索接口匿名可用）；封面站 `/search` 被 WAF 拦、极目 API 需 `token`。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20–30 s 超时）——
  - 党媒平台 `POST api-m.hubpd.com/main_station/search`（`{"keyword":"物业"}`）→ **200** `{"errCode":0}`，首条 `title=长沙物业哪家强？`、`mpName=湖南日报`、`reprintedUrl=https://m.voc.com.cn/portal/news/show?id=31011869`。
  - 澎湃 `POST api.thepaper.cn/search/web/news`（`{"word":"物业",...}`）→ **200**，`data.list` 5 条（首条标题「上海住宅物业管理新规11月起将施行…」、`contId=34097815`、`nodeInfo.name=浦江头条`）；`https://www.thepaper.cn/newsDetail_forward_34097815` → **200**（26 951 B）。
  - 闪电 `GET s.iqilu.com/api/search?q=物业` → **200**，首条 `title=成都“双晒升级”动真格：数家物业被公开曝光`、`url=https://sdxw.iqilu.com/w/article/…`。
  - 封面 `https://www.thecover.cn/search?keyword=物业` → **200 但返回 “Access Verification” 拦截页**；极目 `https://www.ctdsb.net/amc/client/webSearchContent?...keywords=物业` → **200 `{"suc":0,"message":"token为空"}`**；上游 `https://www.cqcb.com/search?keyword=物业` → 落回首页（SPA）；红星 `https://www.hongxingnews.com/` → 本机 **curl 连接失败**（rc 000）。
  - 省级客户端首页：`sdxw.iqilu.com` 200 / `ourjiangsu.com` 200 / `tidenews.com.cn` 200 / `voc.com.cn` 200 / `cbgc.scol.com.cn` 200（`nfapp.southcn.com` 本机不可达）。
- 上游：<https://www.hubpd.com/>、<https://www.thepaper.cn/>、<https://s.iqilu.com/cse/search>、<https://www.thecover.cn/>、<https://www.ctdsb.net/>、<https://www.cqcb.com/>

## 细节

### 全国党媒信息公共平台（hubpd）

| 项 | 内容 |
|---|---|
| 首页/壳 | `https://www.hubpd.com/`（Vue SPA，静态资源在 `img.hubpd.com/hubpd/www/<ver>/js/`） |
| 配置 | `https://www.hubpd.com/js/config.js` → `window.BASEURL='https://api-m.hubpd.com'`、`APP_KEY`、`RONGHEHAO_BASEURL='https://api-mp.hubpd.com'` |
| 全站检索 | `POST {BASEURL}/main_station/search`，JSON `{keyword,pageNum,pageSize,contentType?,keywordSearchScope?}`（前端 `needToken:true`，但**匿名实测可通**） |
| 话题检索 | `GET {BASEURL}/topics/search?keyword=&pageNum=&pageSize=` |
| 信息流 | `POST {BASEURL}/get_contents`（需 `appKey`）、`GET /get_mcontents` |
| 结果字段 | `trueId,title,mpName(媒体号),mpIcon,reprintedUrl(原文),createdAt/updatedAt(秒),type,transCodingObjKey(封面),covers[]` |

### 澎湃新闻（thepaper）

- 检索：`POST https://api.thepaper.cn/search/web/news`，JSON `{"word":"…","pageNum":1,"pageSize":10}`。
- 详情：`https://www.thepaper.cn/newsDetail_forward_<contId>`（静态 HTML）。
- 另：图片/视频等另有 `search/web/*` 子路径；分页由 `pageNum/pageSize` 控制。
- 前端检索页 `https://www.thepaper.cn/searchResult?...` 亦调该 API。

### 齐鲁网/闪电新闻（iqilu）

- 检索 API：`GET https://s.iqilu.com/api/search`，参数 `q,page,size,sort,nsid,method,range`（见上）。
- 结果 `data.items[].url` 多为 `sdxw.iqilu.com`（闪电新闻）；`docType` 标识稿件类型。
- 前端检索页：`https://s.iqilu.com/cse/search`（JS 渲染，接口即上面这个）。

### 县级融媒体中心的入口

- **内容汇聚**：县级融媒体号稿件主要经**全国党媒信息公共平台**（`mpName` 即媒体号）与各省**省级技术平台/客户端**分发，用 `hubpd` 检索最省事。
- **省级平台/客户端入口**（本机 200）：闪电新闻 `sdxw.iqilu.com`（山东「闪电云」）、我苏 `ourjiangsu.com`（江苏「荔枝云」）、潮新闻 `tidenews.com.cn`（浙江，原天目云）、华声在线/新湖南 `voc.com.cn`（湖南）、川观新闻 `cbgc.scol.com.cn`（四川）。
- **区县报/新闻网**：多为各地「XX新闻网 / XX发布」，无统一检索；惯用 `site:` 点查（`../engines/`），报纸原版走 `epaper/`，县级「XX发布」公众号走 `../wechat/`。

## 坑

1. **党媒平台前端标 `needToken:true`**：网页调用会带登录 token；本机匿名 `POST /main_station/search` 仍返回完整结果，若日后被收紧，需按登录态处理。
2. **澎湃检索字段是 `word`**：传 `keyword` 会得到 `{"code":10001,"desc":"搜索词不能为空"}`；传表单编码也会飘（`99998 系统繁忙`），须 JSON。
3. **封面新闻 `/search` 有 WAF**：返回 `Access Verification` 拦截页（非 403 但无内容）；只用浏览器访问，或改 `site:thecover.cn`。
4. **极目新闻 API 需 token**：`/amc/client/webSearchContent` 匿名返 `{"suc":0,"message":"token为空"}`；token 由页面下发，命令行不可直取。
5. **上游/红星**：上游 `cqcb.com` 检索为 SPA 且未探到匿名接口；红星 `hongxingnews.com` 本机 curl 不可达（可能限流/需浏览器指纹）。
6. 地方稿源**时效性与可撤**：客户端稿件可能被删改，引用前保留抓取时间与 `reprintedUrl` 快照；同一事件党媒平台/澎湃/闪电可能各有一版，注意区分原发与转载。
