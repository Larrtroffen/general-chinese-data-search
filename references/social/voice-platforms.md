# 问政与民生平台 —— 领导留言板·百姓呼声·网上民声

- 去哪找：
  - **人民网·领导留言板**：`http://liuyan.people.com.cn/`（PC 端 SPA，列表页 `/threads/list`、详情 `/threads/content?tid=<tid>`）。
  - **红网·百姓呼声**（湖南）：`https://people.rednet.cn/`（列表页 `/front/messages/list`）。
  - **胶东在线·网上民声**（烟台）：`https://ms.jiaodong.net/front/minsheng/questionList_all`。
  - **麻辣社区**（四川）：`https://www.mala.cn/`；**大河号（大河论坛，河南）**：`https://bbs.dahe.cn/`。
- 什么时候用：
  - 关键词式需求：某地「物业/欠薪/拆迁/教育/环保/供暖/办证」等**具体民生诉求的原始文本**；
  - 要「**某地群众反映 + 官方回复**」成对文本做舆情/治理研究；
  - 要**未上新闻**的基层诉求原文（留言板往往比媒体报道更早、更细）；
  - 不适用：机构任免（→ `../gov/renshi-sources.md`）、政策原文（→ `../gov/`）、公众号发文（→ `../wechat/`）。
- 怎么搜：
  - **领导留言板（需按官方签名规则发请求，已复现）**：前端是 SPA，检索走 JSON 接口，请求体须带 `appCode/token/signature/param` 四件套。签名规则（从 `pcjs/app.*.js` 反查）：`signature = md5(路径(去 query) + JSON.stringify(业务参数) + md5(appCode)[:16] + token)`，`appCode` 硬编码在页面 `SITE_CONFIG`（`PC42ce3bfa4980a9`，改版会换），匿名 `token` 为空。
    ```bash
    # ① 全文检索（Python 生成签名，避免手拼）
    python3 - <<'PY'
    import hashlib,json,subprocess
    app="PC42ce3bfa4980a9"; url="/v2/threads/search"
    data={"position":0,"keywords":"物业","fid":None,"domainId":None,"typeId":None,
          "timeRange":None,"ansChecked":False,"stTime":None,"sortType":"0","page":1,"rows":10}
    js=json.dumps(data,ensure_ascii=False,separators=(',',':'))          # 键序须与前端一致
    key=hashlib.md5(app.encode()).hexdigest()[:16]
    sig=hashlib.md5((url+js+key).encode()).hexdigest()
    body=json.dumps({"appCode":app,"token":"","signature":sig,"param":js},ensure_ascii=False,separators=(',',':'))
    subprocess.run(["curl","-sS","-m","25","-H","Content-Type: application/json",
      "-H","Referer: https://liuyan.people.com.cn/threads/list",
      "https://liuyan.people.com.cn/v2/threads/search?sortType=0","--data",body])
    PY
    # 只搜「已办理」：业务参数追加 "threadsStatus":2（前端勾选“已回复”时加的）
    # ② 详情（含官方回复）：POST https://liuyan.people.com.cn/v1/threads/content  业务参数 {"tid":<tid>}
    ```
    结果形态：**JSON**。检索返回 `data.data[]`（`tid/subject/content/forumName/typeName/domainName/stateInfo/createDateline` 等）；详情返回 `resultData.contentList[]`，`dataType=1` 为网友留言、`dataType=4` 为官方回复。
  - **免签名的 JSONP 兜底**（只给「某留言对象最新几条」，不做关键词）：`https://messageboard.people.cn/new_threads_<fid>.jsonp`（回调 `IndexThreads`）、`newIndex_stat.jsonp`（总量）、`provinceAnswerRate.jsonp`（各省回复率）；`fid` 可由 `https://liuyan.people.com.cn/cms/getFidByRequestIP?callback=getFid` 取（按来访 IP 归属地，本机得 `{"fid":"4"}`）。
  - **红网百姓呼声（免登录 JSON，最省事）**：
    ```bash
    # 全文检索（关键词字段是 search；/front/msg/list 不认 search，别用错）
    curl -sS -m 20 -H 'Content-Type: application/json' -H 'Referer: https://people.rednet.cn/' \
      -X POST 'https://rapi.rednet.cn/front/msg/index' -d '{"search":"物业","page":1,"page_num":10}'
    # 列表（按办理状态）：is_reply 0=未办理 1=已办理 2=办理中 3=最新回应
    curl -sS -m 20 -H 'Content-Type: application/json' -H 'Referer: https://people.rednet.cn/' \
      -X POST 'https://rapi.rednet.cn/front/msg/list' -d '{"is_list":1,"is_reply":1,"page":1,"page_num":20}'
    # 详情（含官方回复）：GET /front/msg/detail?id=<id>
    curl -sS -m 20 -H 'Referer: https://people.rednet.cn/' 'https://rapi.rednet.cn/front/msg/detail?id=4710762'
    ```
    结果形态：**JSON**（`{"status":"1","data":{...}}`）。检索/列表 `data.rows[]`（`id/title/created_at/type_name/nickname/city_id/area_id/is_reply/reply_name/reply_time/click_num`）；详情 `data.content`（留言 HTML）、`data.reply[]`（官方回复，`content/reply_time/name`）、`data.comment[]`。
  - **胶东在线网上民声（免登录，但慢）**：API 基址 `https://ms.app.jiaodong.net/public/index.php`。
    ```bash
    curl -sS -m 30 'https://ms.app.jiaodong.net/public/index.php/pc/v1/home/askList/0?page=1&size=25'      # 最新留言
    curl -sS -m 30 'https://ms.app.jiaodong.net/public/index.php/pc/v1/searchAll?page=1&size=25&keyword=物业' # 全文检索
    curl -sS -m 30 'https://ms.app.jiaodong.net/public/index.php/pc/v1/askInfo/1302370'                      # 详情（data.master/one/two）
    ```
    结果形态：**JSON**（`{"code":200,...,"data":{...}}`）。
  - **麻辣社区 / 大河号**：见「细节」，匿名只读、检索基本要登录，按「仅浏览器」对待。
- 覆盖：
  - 领导留言板：全国 31 省 + 部委 + 央地各级领导，**累计留言约 753 万条**（`newIndex_stat.jsonp` 实测 `totalThreadsNum`），本年新留言约 69.8 万；按地区到「市委书记/县委书记」层级；动态更新（日）。例：本机 IP 归属北京时 `fid=4`，最新条目含「房山区委书记/大兴区委书记」等。
  - 红网百姓呼声：湖南为主（`province_id=430000`，含省本级/长沙/郴州…）；**总量约 94 万条**（`msg/list` 实测 `total≈944797`）；每条含正文与官方回复。
  - 胶东在线网上民声：烟台市及其县市区、市直部门，含部门回复与回复率统计。
  - 麻辣社区：四川（含各地市州）论坛帖；大河号：河南。
- 门槛：**免费、免登录**（领导留言板需按上述签名规则自建请求；胶东在线接口偏慢，单次 15–25 s）；无验证码；领导留言板**发表留言/点赞需登录**，只读取数不需要。
- 实测：2026-10-03，macOS arm64，curl 8.x（桌面 UA，20–30 s 超时）——
  - 领导留言板 `POST /v2/threads/search?sortType=0`（`keywords=物业`）→ **200**，`{"code":0,"msg":"ok"}`，返回 10 条（首条 `tid=26239890`、`forumName=江苏省南通市如皋市委书记`、`stateInfo=待回复`）；追加 `threadsStatus=2` → 5 条均 `已办理`；`POST /v1/threads/content`（`tid=26109861`）→ `contentList` 2 条（`dataType=1` 留言 + `dataType=4` 官方回复，正文完整）。
  - 红网 `POST rapi.rednet.cn/front/msg/index`（`{"search":"ZZZ不存在"}`）→ **200 `total:0`**；`{"search":"物业"}` → 有结果；`GET /front/msg/detail?id=4710762` → **200**，`reply[0].content` 为「长沙县市场监督管理局」完整答复。
  - 胶东在线 `GET .../pc/v1/home/askList/0` → **200**（首条 `标题=占用公共场地资源`、`city_name=烟台市`）；`GET .../pc/v1/searchAll?...&keyword=物业` → **200**（首条「关于万科物业违规无故停水、服务失职的投诉」）；`GET .../pc/v1/askInfo/1302370` → **200**（`data` 含 `master/one/two`）。
  - 麻辣社区 `https://www.mala.cn/forum-126-1.html` → **200**（匿名可读帖列表，含 `thread-…-1-1.html` 链接）；`/search.php?mod=forum&srchtxt=物业` → **302 跳登录**（检索需登录）。
  - 大河号 `bbs-api.dahe.cn/pc/index/search`（`{"keywords":"物业",...}`）→ **200** 但返回默认全量（`total=187163`），关键词未生效（疑似需登录 token）。
- 上游：<http://liuyan.people.com.cn/>、<https://people.rednet.cn/>、<https://ms.jiaodong.net/front/minsheng/questionList_all>、<https://www.mala.cn/>、<https://bbs.dahe.cn/>

## 细节

### 领导留言板接口与签名

| 项 | 内容 |
|---|---|
| 检索 | `POST /v2/threads/search?sortType=<0/1>`，`sortType` 也随 body 传；body 为四件套 `{appCode,token,signature,param}` |
| 业务参数 `param`（JSON 字符串） | `position`(0) `keywords`(关键词) `fid`(留言对象 id，null=全部) `domainId`(领域) `typeId`(类型) `timeRange` `ansChecked`(bool) `stTime`(起始秒) `sortType` `page` `rows`；勾选「已回复」时追加 `threadsStatus:2` |
| 详情 | `POST /v1/threads/content`，业务参数 `{"tid":<tid>}` → `resultData.contentList`（`dataType` 1=留言 4=回复） |
| 其他 | `POST /v1/forum/getTopForums`、`GET /v1/forum/getTopBwForums`（留言对象/板块） |
| 签名 | `signature=md5(路径(去?后) + JSON.stringify(param) + md5(appCode)[:16] + token)`；`appCode` 见页面内联 `window.SITE_CONFIG["appCode"]`；`token` 匿名留空 |
| 前端资源 | 壳页 `/threads/*`（Vue SPA，~4.5 KB）；逻辑在 `/pcjs/app.<hash>.js` 与懒加载 `chunk-*.js`（检索 chunk 含 `/v2/threads/search`） |

### 红网百姓呼声端点

| 端点 | 方法 | 参数/说明 |
|---|---|---|
| `/front/msg/index` | POST | `{search,page,page_num}` → **全文检索**（认 `search`） |
| `/front/msg/list` | POST | `{is_list:1,is_reply,page,page_num,cate_id,area_id,type_id,start_time,end_time}` → 按状态/栏目列表（**不认 `search`**） |
| `/front/msg/detail` | GET | `?id=<id>` → 留言正文 + `reply[]` 官方回复 |
| `/front/common/area` `/areas` `/types` `/cates` | GET | 地区/栏目/类型字典 |
| `/front/home/*` | GET | 首页各板块（`reply/newest/hot/lawyer…`） |

`is_reply` 取值：`0` 未办理、`1` 已办理、`2` 办理中、`3` 最新回应。

### 其他两家的取数姿势

- **麻辣社区（Discuz）**：版块列表 `https://www.mala.cn/forum-<fid>-<page>.html`、帖子 `thread-<tid>-1-1.html` 匿名可读；站内搜索 `https://www.mala.cn/search.php?mod=forum&srchtxt=<kw>` **跳登录**，需账号或改用 `../engines/` 的 `site:www.mala.cn`。
- **大河号（原大河论坛）**：`https://bbs.dahe.cn/` 为 Vue SPA，API 基址 `https://bbs-api.dahe.cn/`；`POST /pc/index/article/list`、`/pc/index/article/detail`（均 POST，JSON）可取内容；检索 `POST /pc/index/search`（`{keywords,current,size,type}`）本机匿名**未生效**，按需登录 cookie 或退回 `site:` 点查。

## 坑

1. **领导留言板签名不能省**：不带四件套直接 POST 会返回 `{"code":"SN0006","msg":"数据格式错误"}`（HTTP 仍 200）；`signature` 依赖 `JSON.stringify(param)` 的**键顺序**，键序/字段变体（多/少一个 key）都会验签失败。
2. `appCode`（`PC42ce3bfa4980a9`）与签名算法随前端改版会变，失效时从 `https://liuyan.people.com.cn/pcjs/app.<hash>.js` 重新提取。
3. 领导留言板检索接口**默认不筛已回复**；要「已办理」须显式加 `threadsStatus:2`。回复正文只在**详情**接口里，检索结果只有留言。
4. 红网 **检索走 `/front/msg/index`、列表走 `/front/msg/list`，两者参数不同**；`msg/list` 传 `search` 会被静默忽略并返回全量（易误判"搜索无过滤"）。
5. 胶东在线接口**很慢**（`searchAll` 单次可达 20 s+），且 `ms.jiaodong.net` 前端页为 SPA、旧入口 `a.jiaodong.net` 对无头 UA 返 **403**；`www.jiaodong.net/minsheng/` 页面为 **GB2312**（须转码），新一代取数只认 `ms.app.jiaodong.net` 的 JSON。
6. 各平台回复文本多为**留言对象单位自述**，含个案信息，引用时注意脱敏与「某单位答复」的归属；平台可能下撤/编辑留言，正文以抓取时为准。
