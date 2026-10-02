# person-databases —— 人物·荣誉·英烈名录库

- 去哪找：
  - **中华英烈网**（退役军人事务部）：名录 `https://www.chinamartyrs.gov.cn/shengji_lsyml/`；检索结果页 `…/shengji_lsyml/lsymlsearchresult/index.html?id=<关键词>`。区域（省/市/区县）代号树 `https://www.chinamartyrs.gov.cn/v2/JSON/allQyJSON/000000000000/000000000000.json`。
  - **两院院士**：中科院 `https://casad.cas.cn/ysxx2022/ysmd/qtys/`（7 学部 + 已故/外籍）；工程院 `https://www.cae.cn/cae/html/main/col48/column_48_1.html`（按拼音首字母 A–Z，另有学部/资深/外籍/已故等分类）。
  - **国家荣誉 / 道德模范 / 好人**：中国文明网先进人物总库 `http://www.wenming.cn/wmsjk/xjrw/`；中国好人榜评选平台 `https://zghr.wenming.cn/`（JSON 接口，见 `## 细节`）。
  - **地方党史人物**：湖南 `hndsyjy.cn`、上海 `ccphistory.org.cn`、湖北 `hbdsw.org.cn`、广东 `gddsw.com.cn`、江西红土魂英烈网 `jxhth.cn`（列于 `## 细节`）。
  - **图书馆人物图像**：国图读者云门户·前尘旧影 `http://read.nlc.cn/allSearch/searchList?searchType=36`；上海文化总库 `https://memory.library.sh.cn/`。
- 什么时候用：查**革命烈士**（按姓名/籍贯/牺牲年代）；核**两院院士**身份、届次、学部；查**全国道德模范/时代楷模/中国好人/新时代好少年**名单；查**地方党史人物/革命先辈**；找**历史人物照片/画像**。要的是「在册名单/生平条目」，不是新闻。
- 怎么搜：一句话——**英烈**走中华英烈网（检索 API 需浏览器，见 §1）；**院士**两站名录均为静态 HTML，curl 直接抓列表再 grep 姓名（§2）；**荣誉/好人**静态总库直接读、好人榜走 JSON API（§3）；**地方党史**四省入口与江西英烈 JSON API 见 §4；**人物图像**国图前尘旧影可匿名翻页（§5）。
- 覆盖：英烈（全国约 196 万，按行政区划+牺牲年代组织）；两院院士（中科院在册+已故+外籍；工程院按学部/首字母分类）；国家荣誉与道德模范（第 1–9 届全量 + 年度好人榜）；地方党史人物（湖南/上海/湖北/广东/江西等省名录）；历史照片（国图老照片、上图老照片）。
- 门槛：**全部免费、免登录**为主；中华英烈网**检索接口需真实浏览器**（curl 503）；上海文化总库为 JS SPA；好人榜点赞/评论需登录（名单 JSON 匿名可读）；上海图书馆开放数据 API 需注册 APIKey。
- 实测：2026-10-03，macOS 27（arm64），curl 8.x（`-sSk -L -m 20`，桌面 Chrome UA，单主机 ≤3 请求、间隔 ≥1.5s）。**状态码**：中华英烈网名录页 200、检索 API 503；CAS `qtys/` 200（883 人名链接）、已故 200（758）、站内检索 200；CAE 全体 200、字母页 200、`search.jsp` 200；文明网总库 200（884 KB）、模范子库 200（330 KB）、好人榜 API 200（JSON）；湖南/上海/湖北/广东/江西党史均 200，广东 `/content/page` JSON 200，江西 `get_yml_list.html` POST 200；国图前尘旧影列表/详情 200；浙图图像库 `diglweb.zjlib.cn` 连接超时 000。逐条见 `## 细节`。
- 上游：<https://www.chinamartyrs.gov.cn/>、<https://casad.cas.cn/>、<https://www.cae.cn/>、<http://www.wenming.cn/>、<https://zghr.wenming.cn/>、<http://read.nlc.cn/>（读者云门户）、<https://memory.library.sh.cn/>。

## 细节

> 探测纪律（本机实测）：≤3 请求/主机、间隔 ≥1.5s、20s 超时、桌面 Chrome UA。`✅`=本机 curl 200；`⚠️`=有但需浏览器/条件；`❌`=不可达/被拦。未 curl 的入口标「搜索所得」。

### 1. 中华英烈网（退役军人事务部）—— 全国烈士名录

- 检索入口：`https://www.chinamartyrs.gov.cn/shengji_lsyml/`（烈士英名录首页，✅ 200 / 28,925 B）；检索结果页 `…/shengji_lsyml/lsymlsearchresult/index.html?id=<姓名>`（✅ 200 / 46,833 B，静态壳、结果由 JS 渲染）。
- 匿名：**页面与地区树匿名可读；检索 API 需浏览器**。
- 结果形态：HTML 列表（烈士姓名/籍贯/出生日期/牺牲日期）→ 详情；接口为 **POST JSON**。
- 怎么搜（源码级，来自 `/v2/static/lsyml/js/search-result.js`）：
  ```bash
  # ① 先取令牌
  curl -sSk -X POST 'https://yinglie.chinamartyrs.gov.cn/web-api/getToken'   # 200 {"code":200,"data":{"token":"eyJ…"}}
  # ② 再查（参数：mmdrName 姓名、pageNum、pageSize、Params JSON、mmdrShengId 省代号）
  curl -sSk -X POST 'https://yinglie.chinamartyrs.gov.cn/web-api/api/martyrs/search' \
    --data-urlencode 'mmdrName=王' --data 'pageNum=1&pageSize=10' \
    --data-urlencode 'Params={"beginTime":"","endTime":""}' --data 'mmdrShengId='
  # 本机实测：无论带 user-token/token/Authorization 或 Origin/Referer，均返回 {"msg":"您没有权限访问此地址。","code":503} → 需真实浏览器（TLS/签名门）
  ```
- 区域树（✅ 可直接取）：`https://www.chinamartyrs.gov.cn/v2/JSON/allQyJSON/000000000000/000000000000.json` → JSON 树，节点含 `orgId`（12 位行政区划码）、`deptName`、`children`（省→市→区县）。
- 省级名录页：`…/shengji_dqlsyml/shengji_dqlsymlnamelist/index.html?id=<orgId>`（✅ 200 / 39,771 B；JS 渲染，其依赖的全局变量 `allMartyrsJSON` 在页面脚本中未定义 → 列表不渲染）。
- 地方英烈网（首页友链，可作分省替代）：江西红土魂 `http://www.jxhth.cn/`、山东 `http://www.sdmartyrs.cn`、河南 `http://www.hnylw.org.cn/`、广东 `https://service.dva.gd.gov.cn/gdylw/index.shtml`、重庆 `https://tyjrswj.cq.gov.cn/martyrs_memorial/`、四川 `https://www.scmartyrs.cn`、贵州 `byjn.tyjrfwpt.tyjrswt.guizhou.gov.cn`、新疆 `xjylw.tyjr.xinjiang.gov.cn`。
- 实测：2026-10-03。`/shengji_lsyml/`→200；`lsymlsearchresult/index.html?id=test`→200（46,833 B）；`/web-api/getToken`→200（返回 JWT）；`/web-api/api/martyrs/search`→**503**（`您没有权限访问此地址。`）；`allQyJSON/…/000000000000.json`→200。

### 2. 两院院士名录

| 院 | 入口（名单） | 匿名 | 结果形态 | 备注 |
|---|---|---|---|---|
| 中科院 | `https://casad.cas.cn/ysxx2022/ysmd/qtys/` | ✅ | 静态 HTML，**883 条人名链接**、按 7 学部排列 | 已故 `…/ygys/`（758 链接）、外籍 `…/wjys/`；`…/ysmd/` 用 `location.replace('./qtys/')` 跳转 |
| 中科院（检索） | `https://casad.cas.cn/qwjs/index.html?searchword=<kw>` | ✅ | HTML 全文检索 | 200 / 55,806 B，title《全文检索》 |
| 工程院 | `https://www.cae.cn/cae/html/main/col48/column_48_1.html` | ✅ | 静态 HTML + 首字母分页 | 字母页 `column_48_A.html`…`_Z.html`；详情 `/cae/html/main/colys/<id>.html` |
| 工程院（检索） | `POST https://www.cae.cn/cae/app/search/search.jsp` | ✅ | HTML 结果页 | 参数 `area=3&webid=main&q=<kw>`；实测 `q=院士`→「共 11067 条」 |

- 中科院名单元数据：`curl -s https://casad.cas.cn/ysxx2022/ysmd/qtys/ | grep -oE 't20[0-9]{6}_[0-9]+\.html'` → 详情页形如 `http://casad.cas.cn/ysxx2022/ysmd/sxwl/202312/t20231205_4990208.html`（数学物理学部 sxwl / 化学 hxb / 生命科学和医学 smkx / 地学 dxb / 信息技术 xxjs / 技术科学 jskx）。
- 工程院分类栏目：学部 `/cae/html/main/col53/column_53_1.html`、资深 `col49`、香港 `col51`、澳门 `col337`、台湾 `col52`、外籍 `col50`、已故 `col56`、已故外籍 `col57`、中央委员等 `col54`、两会代表 `col55`、历次增选 `col248`。
- 实测：2026-10-03。CAS `qtys/`→200 / 269,682 B（883 人名链接）；`ygys/`→200 / 228,179 B（758）；`qwjs/index.html?searchword=王`→200。CAE `col48/column_48_1.html`→200 / 128,648 B；`column_48_A.html`→200 / 20,254 B（`艾兴`→`/cae/html/main/colys/93910906.html` 等）；`search.jsp`→200 / 21,194 B。

### 3. 国家荣誉称号 / 道德模范 / 中国好人（中国文明网）

| 库 | 入口 | 匿名 | 形态 | 实测 |
|---|---|---|---|---|
| 先进人物总库（单页内嵌） | `http://www.wenming.cn/wmsjk/xjrw/` | ✅ | 静态 HTML（884 KB，含道德模范 1–9 届、时代楷模、中国好人、新时代好少年、诚信之星等） | 200 / 884,366 B |
| 全国道德模范子库 | `http://www.wenming.cn/wmsjk/xjrw/xjrwqgddmf/index.html` | ✅ | 静态 HTML 名单（含提名奖） | 200 / 330,325 B |
| 新时代好少年库 | `http://www.wenming.cn/wmsjk/xjrw/xjrwxsdhsn/index.html` | ✅ | 静态 HTML 年度名单表 | 搜索所得（同域总库内链） |
| 身边好人频道 | `http://www.wenming.cn/sbhr_pd/`；单期 `…/sbhr_pd/zghrb/bd/<期次>/index.html` | ✅ | 静态 HTML（姓名+省+市+事迹+链接） | 搜索所得 |
| 中国好人榜评选平台 | `https://zghr.wenming.cn/`（Vue SPA）| ✅ 名单 / 需登录点赞 | **JSON API** | 见下 |
| 全站检索 | `POST http://search.wenming.cn/pc/search/simple` | ✅ | JSON | 源码级（`search.wenming.cn/js/config.js`） |

- 中国好人榜 JSON（实测可匿名拉名单）：
  ```bash
  curl -s 'https://zghr.wenming.cn/api/v2/candidates?activityId=xvmYwlVJPO72&pageNum=1&pageSize=20'
  # 200 → {"code":200,"msg":"操作成功","rows":[{"username":"艾合买提·吾甫尔","gender":"男",
  #   "category":"dedicated","activityId":11,"activityTitle":"2026年第三批中国好人宣传选树",
  #   "candidateSid":"dDwrogB2","activitySid":"xvmYwlVJPO72","photoUrl":"http://zghr.wenming.cn/…jpg",…}]}
  ```
  活动元数据 `GET /api/v2/activities/<activitySid>`；类别字典 `GET /api/v2/dict/category_name`（altruistic/brave/honest/dedicated/filial）；支持 `category`、`regionId`、`pageNum`、`pageSize`。实测活动 `xvmYwlVJPO72`（第 11 期）名单共 **372 人**。
- 实测：2026-10-03。`wmsjk/xjrw/`→200 / 884,366 B；`xjrwqgddmf/index.html`→200 / 330,325 B；`zghr.wenming.cn/api/v2/candidates?...`→200（返回 `rows` 列表）。
- 说明：**「国家勋章/国家荣誉称号」无独立人物库**，仅在文明网/新华网新闻专题中出现（如「共和国勋章」「人民楷模」报道），需靠新闻检索，不在本站结构性库内。

### 4. 地方党史人物 / 革命先辈名录（分省）

| 省 | 栏目入口 | 匿名 | 形态 / 接口 | 实测 |
|---|---|---|---|---|
| 湖南 | `http://www.hndsyjy.cn/channel/22961.html`（三湘将帅）、`…/22962.html`（湖湘群英）；湘籍伟人 `22959`、殷切关怀 `22960` | ✅ | 静态 HTML 列表 | 200 / 15,842 B；命中 彭绍辉/杨得志/左权/李贞；正文 `/content/<a>/<b>/<id>.html` |
| 上海 | `https://www.ccphistory.org.cn/shds/hsrw/hsrw.html`（海上人物） | ✅ | 单页内嵌 **115 条**（`<ul id="initData">` 隐藏 + jpage 前端分页） | 200 / 13,998 B；正文 `/shds/hsrw/content/<uuid>.html` |
| 湖北 | `http://www.hbdsw.org.cn/jcfb/fhqy/`（烽火群英）、`http://www.hbdsw.org.cn/zxyd/wgmxs/`（为革命献身的湖北省委书记） | ✅ | 静态 HTML 列表（`.shtml`，**GBK 编码**） | 200 / 27,054 B（fhqy）、26,465 B（wgmxs）；命中 陈潭秋/恽代英 |
| 广东 | `https://www.gddsw.com.cn/lybwcjjgmjzgd`（老一辈无产阶级革命家在广东）、`/nyyj`（南粤英杰） | ✅ | HTML 壳 + **JSON XHR** | 页面 200 / 14,922 B |
| 江西 | 红土魂·江西英烈网 `https://www.jxhth.cn/yinglieminglu/`（全省烈士近 26 万） | ✅ | 表单检索 + **JSON API**（见下） | 页面 200 / 39,447 B |
| 江苏 | `http://s.jsdsw.org.cn/web/index.html` | ⚠️ | Vue SPA，静态为模板占位 | 搜索所得（未挖到接口） |

- 广东列表 JSON（实测 200）：
  `curl -s 'https://www.gddsw.com.cn/content/page?channelIds=2476&page=1&size=15'` → `{"code":200,"data":{"content":[{title,shortTitle,url,releaseTime}…],"totalElements":N}}`。
- 江西红土魂英烈检索（实测可用、字段最全）：
  ```bash
  # 列表（POST，参数 page/limit，limit 可选 10/20/50/100/150；lsxm=姓名, cym=曾用名, jg=籍贯）
  curl -s -X POST 'https://www.jxhth.cn/index/ylml/get_yml_list.html' --data-urlencode 'lsxm=方志敏' --data 'page=1&limit=10'
  # → {"data":[{"ID":"…","烈士姓名":"方志敏","籍贯":"弋阳县","政治面貌":"中共党员","出生时间":"1899",
  #     "参加革命时间":"1922","牺牲时间":"19350806","牺牲年龄":"36","生前职务":"…"}]}
  # 详情（GET id=<uuid>）
  curl -s 'https://www.jxhth.cn/index/ylml/get_yml_detail.html?id=<ID>'
  # → {"Info":{"烈士姓名":…,"曾用名":…,"性别":…,"籍贯":…,"出生时间":…,"参加革命时间":…,"牺牲时间":…,
  #     "牺牲年龄":…,"生前单位":…,"生前职务":…,"牺牲地点":…,"牺牲原因":…},"Photo":{…}}
  # 籍贯字典 GET /index/ylml/get_yml_jg.html
  ```
- 实测：2026-10-03。湖南 `22961`/`22962`→200；上海 `hsrw.html`→200（`totalrecord=115`）；广东 `lybwcjjgmjzgd`→200，`/content/page?...`→200 JSON；江西 `yinglieminglu/`→200、`get_yml_list.html`→200（`lsxm=方志敏` 命中）、`get_yml_detail.html?id=…`→200（`{"Info":{…}}`）。湖北 `fhqy`/`wgmxs`→200（GBK，陈潭秋/恽代英）；江苏/四川为搜索所得。

### 5. 图书馆历史人物图像库

| 库 | 入口 | 匿名 | 形态 | 实测 |
|---|---|---|---|---|
| 国图·前尘旧影（老照片，含人物照） | `http://read.nlc.cn/allSearch/searchList?searchType=36&showType=1&pageNo=1` | ✅ | HTML 列表（15 条/页）+ 详情直出 JPG | 200 / 26,583 B |
| 国图·中国学汉学家 | `…?searchType=66` | ✅ | HTML 人物小传（非画像） | 200 / 25,188 B |
| 上海文化总库（老照片，含「上海年华/历史原照」） | `https://memory.library.sh.cn/`（同构 `https://scc.library.sh.cn/`） | ⚠️ 需浏览器 | Vue SPA；数据侧 API `data1.library.sh.cn` 需 APIKey | 200 / 2,527 B（纯 JS 壳） |
| 浙图·中国历代人物图像数据库 | `http://diglweb.zjlib.cn:8081/zjtsg/zgjcj/index1.htm` | ❌ | 原 HTML+扫描图库（约 5800 人/1 万余幅） | 连接超时 **000**（上游称已撤免费网络版） |
| 首图·旧影尘踪 | `https://www.clcn.net.cn/resources/default/detail?id=454` | ❌ | 馆内访问 | detail 404 |

- 国图详情：`http://read.nlc.cn/allSearch/searchDetail?searchType=36&showType=3&indexName=data_410&fid=<fid>`（实测 200 / 20,752 B），直出大图 `http://read.nlc.cn/doc1/data02/picture_gezhongtupian/picture/oldpic/2005/S/<fid>.jpg`，元数据含拍摄时间/主题/中图分类/索取号；另有 IIIF 阅读器 `/OutOpenBook/OpenObjectPic?aid=410&bid=…`。
- 实测：2026-10-03。国图 `searchType=36`→200（15 条详情链接）、`searchType=66`→200、详情页→200（图 URL 见上）；上海 `memory.library.sh.cn`→200 但仅 2,527 B 壳；浙图 `diglweb.zjlib.cn`→**超时 000**。

### 6. 与既有卡的分工（避免重复查）

| 要查的人 | 去哪 |
|---|---|
| 唐—清历史人物（官職/亲属/社會關係/关系型查询） | `cbdb.md`（CBDB SQLite，`c_personid` 锚点） |
| 台湾/民国人物、日治台湾职员 | `sinica.md` + `../methods/officials-research.md` §五（人名權威檔、总督府职员录、近现代整合系统） |
| **当下**官员/干部（任期、任免、任前公示） | `../methods/officials-research.md` + `../gov/renshi-sources.md` |
| 革命烈士、两院院士、国家荣誉/道德模范/好人、地方党史人物、历史人物照片 | **本卡** |

## 坑

- **中华英烈网检索 API 有反爬门**：`getToken` 可匿名拿到 JWT，但携带令牌直接 POST `search` 仍返回 `{"code":503,"msg":"您没有权限访问此地址。"}` → 必须真实浏览器（`tools/agent-browser.md` / `tools/playwright-cli.md`）。`lsymlsearchresult` 与省级 `namelist` 页均为 JS 渲染的空壳，别指望 curl 出名单。
- **两院院士两站结构不同**：中科院是「一页全量 + 7 学部子页 + 客户端筛选」，工程院是「按拼音首字母分页 + 分类栏目」；工程院字母页正文人名在 `.ysxx_namelist .name_list`，链接指向 `/cae/html/main/colys/<id>.html`（不是 `col48`），直接 grep `colys` 最稳。
- **文明网人物库体量大但无字段检索**：`wmsjk/xjrw/` 是**单页内嵌 88 万字节**、无查询 API/分页参数；要「按年份/类别」筛需自己在本地解析该页表格。中国好人榜才有真正的 JSON 检索（`zghr.wenming.cn`）。
- **地方党史站形态杂**：上海「海上人物」正文在 `display:none` 的 `<ul id="initData">` 里再 JS 分页，普通正文抽取器易只拿到面包屑，需抓原始 HTML；江苏为 Vue SPA 仅浏览器；红网/荆楚网 CMS 的列表多**无分页控件**（单页约 15–25 条）。
- **编码陷阱**：湖北党史网（`hbdsw.org.cn`）为 **GBK/GB2312**，curl 抓到的是乱码，须 `iconv -f gb18030 -t utf-8`（或用 Python `.decode('gb18030')`）再匹配人名——否则会误判「查无此人」。
- **江西红土魂接口**：响应 `Content-Type` 标 `text/html` 但正文是 JSON，且带 BOM（`\ufeff`），`json.load` 前先 `strip('\ufeff')`；列表接口是 **POST**、详情是 GET。
- **图像库多数不可直取**：浙图《中国历代人物图像数据库》已下线（连接超时）；上海老照片为 SPA、开放数据 API 要注册 APIKey（无 key 返回 `{"result":"2","data":"????Key"}`）；上图人名规范库 `names.library.sh.cn` 有 WAF（412）。**目前唯一可匿名直取的馆藏人物照片是国图「前尘旧影」**（`searchType=36`）。
- **国图前尘旧影关键词命中差**：`searchWord=鲁迅` 实测 0 条，宜按主题/时间浏览；同门户 `searchType=48` 为「地方馆老照片」聚合、`searchType=66` 为汉学家小传。
