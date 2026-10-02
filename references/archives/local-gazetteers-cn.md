# local-gazetteers-cn —— 全国省级方志省情站总表

31 个省级地方志机构 + 兵团的官网/省情网/地情网入口总表；其中浙江、广东、山东、湖南四省已挖出可直接调用的检索接口。

- 去哪找：
  - 官方名录（机构名，逐省）：`https://www.difangzhi.cn/zzjg/jgsz/qgsjgzjg/`
  - 友情链接（站点 URL，逐省）：`https://www.difangzhi.cn/` 页脚「方志系统网站群」
  - 逐省 URL 与实测见下方「细节 · 省级总表」；可调接口见「细节 · 检索接口」
- 什么时候用：查**某省**的志书/年鉴/省情/地方史、省级方志办动态、数字方志馆。分层选路：
  - **国家层**（全国方志新闻、志书/年鉴书目选介）→ `difangzhi.cn`，见 `difangzhi.cn.md`
  - **北京市**（区综合年鉴在线）→ `bjdsdfz.cn`，见 `bjdsdfz.cn.md`
  - **上海市**（上海数字方志 REST API）→ `shtong.gov.cn`，见 `shtong.md`
  - **本卡补其余省份**（津冀晋蒙吉黑苏浙皖闽赣鲁豫鄂湘粤桂琼渝川黔滇藏陕甘青宁新 + 兵团 + 港澳）
- 怎么搜：
  - 先按「省级总表」定位省站，能直连 API 的省**优先用「检索接口」**（浙/粤/鲁/湘已探明，返回 JSON 或可解析 HTML）。
  - 无接口的省：用站内搜索框，或 `web_search site:<省站域名> <关键词>`。
  - 志书/年鉴全文：多数省站为**扫描 PDF 在线阅读**（非文本检索）；仅浙江（`book/search2`）、广东（省情数据库）探到**正文库**。
- 覆盖：31 省级机构 + 兵团（官方名录齐全）；2026-10-03 实测 26 个省级站在线、2 省源站宕机（江苏/甘肃）、4 省区无独立省级站（辽宁/西藏/宁夏/新疆，另有兵团）。年代/粒度随各站，志书年鉴多覆盖 1949 后新方志，部分含旧志古籍（浙江、广东）。
- 门槛：省级站普遍**免费、免登录**；四川站内检索带**验证码**；部分站志书全文阅读需注册（如北京，见 `bjdsdfz.cn.md`）；商业方志全文库需**单位 IP/订阅**（见「细节 · 大型方志平台」）。
- 实测：2026-10-03，macOS（arm64），curl/urllib + 桌面 UA。① `https://www.difangzhi.cn/zzjg/jgsz/qgsjgzjg/` → 200，取到 31 条机构名。② 逐省 GET 首页见「省级总表」状态列。③ `POST https://search.gd.gov.cn/api/search/all`（JSON body `{"keywords":"年鉴","site_id":191,"range":"site","position":"title","page":1,"sort":"smart"}`）→ 200 / 43 KB，`errcode:0`，`data.news.list[].title/url/pub_time`。④ `GET https://dfz.zj.gov.cn/api/api/book/search2?limit=5&page=1&classId=1&content=年鉴` → 200，`data.records[].content` 带红色高亮。⑤ `GET https://dfz.gd.gov.cn/dfz/api/book/findBook/api?suffix=pdf&pageNo=1&pageSize=5&bookName=年鉴` → 200，`count:2386`。
- 上游：`https://www.difangzhi.cn/zzjg/jgsz/qgsjgzjg/`（全国省级地方志工作机构名录）· `https://www.difangzhi.cn/`（友情链接）

## 细节

### 省级总表（机构名取自官方名录；状态 = 2026-10-03 本机 GET 首页）

| 省/区 | 机构（官方名录） | 站点 | 实测 |
|---|---|---|---|
| 北京 | 中共北京市委党史研究室、北京市地方志编纂委员会办公室 | `https://www.bjdsdfz.cn/` | ✅ 见 `bjdsdfz.cn.md` |
| 天津 | 天津市档案馆（天津市地方志工作办公室） | `https://www.tjdag.cn/` | ✅ 200 |
| 河北 | 河北省档案馆（河北省地方志编纂委员会办公室） | `https://hebdag.org.cn/` | ✅ 200（http→https） |
| 山西 | 中共山西省委党史研究院（山西省地方志研究院） | `https://www.shanxidsfz.gov.cn/Browse/` | ✅ 200（SPA 壳 3.6 KB，需 JS） |
| 内蒙古 | 中共内蒙古自治区委党史和地方志研究室 | `https://www.nmgqq.com.cn/` | ✅ 200（内蒙古党史方志网/区情网） |
| 辽宁 | 辽宁省地方志编纂中心 | — | ❌ 无独立省级站 |
| 吉林 | 吉林省地方志编纂委员会 | `https://dfz.jl.gov.cn/` | ✅ 200 |
| 黑龙江 | 中共黑龙江省委史志研究室 | `https://www.hljszw.org.cn/` | ✅ 200 |
| 上海 | 上海市地方志办公室 | `https://www.shtong.gov.cn/` | ✅ 见 `shtong.md` |
| 江苏 | 江苏省地方志工作办公室 | `http://jssdfz.jiangsu.gov.cn/` | ❌ 521（Cloudflare 源站宕机） |
| 浙江 | 浙江省地方志工作办公室 | `https://dfz.zj.gov.cn/` | ✅ 200，有全文库 |
| 安徽 | 中共安徽省委党史研究院（安徽省地方志研究院） | `http://www.anhuids.gov.cn/` | ✅ 200 |
| 福建 | 中共福建省委党史研究和地方志编纂办公室 | `http://www.fjdsfzw.org.cn/` | ✅ 200 |
| 江西 | 中共江西省委党史研究室（江西省地方志工作办公室） | `http://www.jxdys.cn/` | ✅ 200 |
| 山东 | 中共山东省委党史研究院（山东省地方史志研究院） | `https://www.sddsw.org.cn/` | ✅ 200，有站群检索 |
| 河南 | 中共河南省委党史和地方史志研究室 | `http://www.hndsfz.cn/` | ✅ 200 |
| 湖北 | 湖北省文化和旅游厅地方志工作处 | `https://wlt.hubei.gov.cn/bmdt/ztzl/zshb/` | ✅ 200（专题页「志说湖北」） |
| 湖南 | 湖南省地方志编纂院 | `http://dfz.hunan.gov.cn/` | ✅ 200，站群检索 |
| 广东 | 广东省人民政府地方志办公室 | `http://dfz.gd.gov.cn/` | ✅ 200，有省情数据库 |
| 广西 | 广西壮族自治区地方志编纂委员会办公室 | `http://www.gxdfz.org.cn/` | ✅ 200 |
| 海南 | 中共海南省委党史研究室（海南省地方志办公室） | `https://www.hnszw.org.cn/` | ✅ 200 |
| 重庆 | 重庆市地方志办公室 | `https://dfz.cq.gov.cn/` | ✅ 200 |
| 四川 | 四川省地方志工作办公室 | `https://www.scsqw.cn/` | ✅ 200（站内检索带验证码） |
| 贵州 | 贵州省档案馆（贵州省地方志编纂委员会办公室） | `https://www.gzdafzxx.cn/` | ✅ 200 |
| 云南 | 云南省地方志编纂委员会办公室 | `https://dfz.yn.gov.cn/` | ✅ 200 |
| 西藏 | 西藏自治区党委党史研究室（西藏自治区地方志办公室） | — | ❌ 无独立省级站 |
| 陕西 | 陕西省地方志办公室 | `https://dfz.shaanxi.gov.cn/` | ✅ 200 |
| 甘肃 | 甘肃省地方史志办公室 | `http://www.gsdfszw.org.cn/` | ❌ 502/超时（宕机） |
| 青海 | 中共青海省委党史研究室（青海省地方志工作办公室） | `http://www.qinghai.gov.cn/sdfz/` | ✅ 200（省政府站频道） |
| 宁夏 | 宁夏社会科学院地方志编纂处 | — | ❌ 无独立省级站 |
| 新疆 | 新疆维吾尔自治区地方志编纂委员会 | — | ❌ 无独立省级站 |
| 兵团 | 新疆生产建设兵团党委党史研究室（兵团志办公室） | — | ❌ 无独立省级站 |
| 香港 | 香港地方志中心 | `https://www.hkchronicles.org.hk/` | ✅ 200（Drupal 10） |

### 检索接口（深入 4 省，均已本机实测）

**浙江 —— 浙江省志全文库（荐，有正文检索）**

| 接口 | 方法 | 参数 | 返回 |
|---|---|---|---|
| `https://dfz.zj.gov.cn/api/api/book/bookCategory` | GET | — | `data[]` 分类：1 方志、2 年鉴、3 旧志古籍、4 省级志书… |
| `https://dfz.zj.gov.cn/api/api/book/search` | GET | `classId` `limit` `page` `name` `author` `title` `content` | 书目级 `data.records[]`（name/press/author/isbn/hits） |
| `https://dfz.zj.gov.cn/api/api/book/search2` | GET | 同上 | **正文全文** `data.records[]`（book/name/directoryName/title/author/`content` 带 `<span style='color:red'>` 高亮） |

人用入口 `https://dfz.zj.gov.cn/search.html`（Vue，读 `?search=<json>`）。返回 JSON，无 key、无验证码。

**广东 —— 站群检索 + 广东省情数据库**

| 接口 | 方法 | 参数 | 返回 |
|---|---|---|---|
| `https://search.gd.gov.cn/api/search/all` | POST JSON | `keywords` `site_id`（191=省志办）`range`（`site`/`province`）`position`（`title`）`page` `sort`（`smart`/`time`） | `{errcode:0,data:{news:{list:[{title,content,url,pub_time}],total}}}`，无需 CSRF |
| `https://dfz.gd.gov.cn/dfz/api/book/findBook/api` | GET | `suffix=pdf` `pageNo` `pageSize` `bookName`（按书名）；或 `topId`（按栏目） | `({count,list:[{id,topicname,topcode,nav,sitename,filePath,bookMenuUrl}]})` |
| `https://dfz.gd.gov.cn/dfz/book/{id}/0.pdf` | GET | 路径 `{id}` | 单册志书/年鉴 PDF 全文 |

人用入口：省志办站群搜索 `https://search.gd.gov.cn/search/all/191`；省情数据库 `https://dfz.gd.gov.cn/dfz/html/gdsqsj/sxnj/pc/page1.shtml`（「广东省情数据库」，Vue SPA）。

**山东 —— 山东党史史志网站群检索**

```bash
# POST，x-www-form-urlencoded；content 直接明文
curl -s https://www.sddsw.org.cn/gentleCMS/do/cmssearch/searchBySite \
  -d 'siteId=54f25385-11d3-44e3-b659-27c2c3b85053&content=年鉴&currentpage=1&size=10&sort=&date=0&range=0'
# → {"totalNumber":2111,"totalPage":423,"words":[...],"page":{"data":[{"CONTENT":"…<span style='color:red'>年鉴</span>…","OPENFUNC":"/articles/…","channelName":"…","pubdate":…}]}}
```

人用入口 `https://www.sddsw.org.cn/channels/ch00053/?content=<base64(utf8(关键词))>`（关键词先 base64 再拼 URL）。

**湖南 —— 湖南站群检索（siteId 制）**

| 接口 | 方法 | 参数 | 返回 |
|---|---|---|---|
| `http://searching.hunan.gov.cn/hunan/{siteId}/news` | GET | `q`=关键词（`291000000`=省地方志编纂院；`183000000`=省政府） | HTML，总数在 `var total`，结果 `li` 列表 |
| `http://searching.hunan.gov.cn/hunan/agg/data` | GET | `q` `websiteName={siteId}` `t=news` `searchfields` `sm` `timetype` | JSON `{aggr_list:[{name,count}]}` 栏目分面计数 |

### 大型方志平台

| 平台 | 入口 | 说明 | 门槛 |
|---|---|---|---|
| 中国方志网（国家层） | `https://www.difangzhi.cn/` | 全国方志新闻、志书/年鉴书目选介、TRS 全文检索 | 免费（见 `difangzhi.cn.md`） |
| 浙江省志全文库 | `https://dfz.zj.gov.cn/` | 方志/年鉴/旧志正文检索 | 免费（见上） |
| 广东省情数据库 | `https://dfz.gd.gov.cn/dfz/html/gdsqsj/sxnj/pc/page1.shtml` | 新方志/年鉴 PDF + 书目检索 | 免费（见上） |
| 万方《中国地方志数据库》 | `https://fz.wanfangdata.com.cn/` | 新方志 6.5 万部、旧方志 10 万余卷全文（上游声明） | 单位 IP / 订阅 |
| 《中国数字方志库》 | 高校图书馆入口（如北大/浙大/中山大学） | 1949 前地志 1.1 万种、15 万册，影像+全文（上游声明） | 高校图书馆 IP |
| 中国地情网 / 中国国情网 | `https://www.zhongguodiqing.cn/` · `https://www.zhongguoguoqing.cn/` | 无可用检索：地情网 `dfz_search/search.do` 已 404、首页表单被注释；均为介绍性内容 | 免费（见 `difangzhi.cn.md`） |

## 坑

1. **江苏、甘肃本机不可用**：江苏 `jssdfz.jiangsu.gov.cn` 返 521（Cloudflare 源站宕机）；甘肃 `gsdfszw.org.cn` 502/连接超时。访问前先看状态。
2. **辽宁/西藏/宁夏/新疆/兵团无独立省级站**：官方名录只有机构名，无网站（宁夏由宁夏社科院地方志编纂处承担，新疆设编纂委员会）。
3. **广东 `findBook/api` 返回体外包圆括号**：`({...})` 非严格 JSON，`json.loads` 会失败，需先 `strip('()')`（或 `re.sub(r'^\(|\)$','')`）。
4. **山西站是 SPA**：`shanxidsfz.gov.cn` 首页仅 3.6 KB「正在加载」壳，须 JS 渲染或另找 XHR。
5. **四川站内检索带验证码**：scsqw.cn 搜索走 `/captcha/validate`，未定位到免验证码入口（`/search`、`/search/index` 均 404）。
6. **湖南检索是 siteId 制**：换 `{siteId}` 即换站群站点；`agg/data` 只给分面计数，正文结果在 `/{siteId}/news?q=` 页面。
7. **山东关键词先 base64(utf8)** 再拼 `content=`，否则人用入口取不到词。
8. **多数志书全文是扫描件**：无文本层时无法关键词检索（浙江、广东除外，有正文库）。旧志/古籍年代与版权随馆，商用前核对各站声明。
